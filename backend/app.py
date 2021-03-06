#!/usr/bin/env python3
import copy

import pandas as pd
from flask import Flask, request
from pandas.io.json import json

from table import Table
from util.functions import intersection_safe, union, difference_safe, slice_df, intersection

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.tables = []
app.current_result = {}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/analyze_table', methods=['POST'])
def analyze_table():
    if request.method == 'POST':
        request_data = request.get_json()
        if not isinstance(request_data, dict):
            return 'error'
        if 'id' not in request_data.keys():
            return 'error'
        if 'col_name' not in request_data.keys():
            return 'error'
        if 'ids' not in request_data.keys():
            return 'error'
        table_id = int(request_data['id'])
        col_name = request_data['col_name']
        ids = request_data['ids']
        col_analyze = get_col_analysis(table_id, col_name)
        result = {
            'pie': get_pie_chart_options(col_analyze['data'], app.tables[table_id].table_name, col_name + '-信息统计'),
            'bar': get_bar_chart_options(col_analyze['data'], app.tables[table_id].table_name, col_name + '-分布'),
            'rates': get_all_rate(table_id, ids),
            'data_list': format_dict_to_list(col_analyze['data']),
            'other_info': get_chart_other_info(col_analyze['data'], col_analyze['other_info'], col_name)}
        return result
    return 'error'


@app.route('/get_table_rates', methods=['POST'])
def get_table_rates():
    if request.method == 'POST':
        table_id = int(request.form['id'])
        result = get_all_rate(table_id)
        return json.dumps(result)
    return 'error'


def format_dict_to_list(source_data):
    total = sum(set(source_data.values()))
    result = []
    for key, value in source_data.items():
        result.append({
            'col_name': key,
            'total': value,
            'pre': str(round(int(value) * 100 / total, 2)) + '%'
        })
    return result


def get_chart_other_info(source_data, other_info, chart_name):
    total = 0
    for value in source_data.values():
        total += value
    result = {}
    for key, value in source_data.items():
        result[key] = key + ': ' + str(value) + ' (' + str(round(value * 100 / total, 2)) + ')%'
    if other_info is not None:
        result['其他'] = ''
        for key, value in other_info.items():
            result['其他'] += key + ': ' + str(value) + ' (' + str(round(value * 100 / total, 2)) + ')%' + '<br/>'
    return result


def get_bar_chart_options(source_data, table_name, chart_name):
    data = list(source_data.values())
    keys = list(source_data.keys())
    chart = {
        'name': chart_name,
        'type': 'bar',
        'barWidth': '60%',
        'data': data,
    }
    legend = {
        'bottom': 10,
        'left': 'center',
        'data': keys
    }
    tooltip = {
        'trigger': 'axis',
        'axisPointer': {
            'type': 'shadow'
        }
    }
    toolbox = {
        'show': True,
        'feature': {
            'restore': {'show': True},
            'saveAsImage': {'show': True}
        }
    }
    title = {
        'text': chart_name,
        'subtext': table_name,
        'left': 'left'
    }
    result = {
        'title': title,
        'color': ['#3398DB'],
        'tooltip': tooltip,
        'grid': {
            'left': '1%',
            'right': '2%',
            'bottom': '1%',
            'containLabel': True,
        },
        'xAxis': [
            {
                'type': 'category',
                'data': keys,
                'axisTick': {
                    'alignWithLabel': True
                },
                'axisLabel': {
                    'showMaxLabel': True
                }
            }
        ],
        'yAxis': [
            {
                'type': 'value'
            }
        ],
        'toolbox': toolbox,
        'legend': legend,
        'series': [chart]
    }
    return result


def get_pie_chart_options(source_data, table_name, chart_name):
    data = []
    for key, value in source_data.items():
        data.append({
            'value': value,
            'name': key,
        })
    chart = {
        'name': chart_name,
        'type': 'pie',
        'radius': '65%',
        'data': data,
        'itemStyle': {
            'emphasis': {
                'shadowBlur': 10,
                'shadowOffsetX': 0,
                'shadowColor': 'rgba(0, 0, 0, 0.5)'
            }
        }
    }
    legend = {
        'orient': '',
        'x': 'left',
        'y': 'bottom',
        'data': list(source_data.keys())
    }
    tooltip = {
                  'trigger': 'item',
                  'formatter': "{a} <br/>{b} : {c} ({d}%)"
              },
    toolbox = {
        'show': True,
        'feature': {
            'restore': {'show': True},
            'saveAsImage': {'show': True}
        }
    }
    title = {
        'text': chart_name,
        'subtext': table_name,
        'x': 'left',
        'y': 'top'
    }
    result = {
        'title': title,
        'tooltip': tooltip,
        'toolbox': toolbox,
        'legend': legend,
        'series': [chart]
    }
    return result


def get_col_analysis(table_id, col_name):
    table = app.tables[table_id]
    col_analyze = table.analyze_col(col_name)
    result = {}
    data = {}
    if len(col_analyze) <= 7:
        for item in col_analyze.items():
            data[item[0]] = item[1]
        result['data'] = data
        result['other_info'] = None
        return result
    s = int(col_analyze.sum())
    list_all = list(sorted(col_analyze.items(), key=lambda x: -x[1]))
    data_list = list_all[0:6]
    temp_sum = 0
    for item in data_list:
        temp_sum += item[1]
    data_list.append(('其他', s - temp_sum))
    for item in data_list:
        data[item[0]] = item[1]
    result['data'] = data
    temp_list = {}
    for item in list_all[6:10]:
        temp_list[item[0]] = item[1]
    result['other_info'] = temp_list
    return result


def get_all_rate(table_id, ids):
    result = []
    fix_table = app.tables[table_id]
    fix_main_keys = fix_table[fix_table.main_key]
    # for table in app.tables:
    for table_id in ids:
        table = app.tables[table_id]
        main_keys = table[table.main_key]
        be_in = intersection(main_keys, fix_main_keys)
        len_ids = len(main_keys)
        len_be_in = len(be_in)
        result.append({
            'table_name': table.table_name,
            'total': len_ids,
            'in': len_be_in,
            'pre': str(round(len_be_in * 100 / len_ids, 2)) + '%',
        })
    return result


@app.route('/reset', methods=['POST'])
def reset():
    app.tables = []
    app.current_result = {}
    return 'success'


@app.route('/export', methods=['POST'])
def export():
    if request.method == 'POST':
        operation = request.form['operation']
        result = None
        if operation == 'funnel':
            result = app.current_result['funnel']['result'][0]
        elif operation == 'diff':
            result = app.current_result['diff']['result'][0]
        else:
            return 'error'
        if 'path' in request.form.keys():
            path = request.form['path']
            result.to_excel(path)
            return 'success'
        return 'error'
    return 'error'


@app.route('/load_data', methods=['POST'])
def load_data():
    if request.method == 'POST':
        path = request.form['path']
        try:
            table = Table(path)
        except:
            message = '请选择标准Excel文件'
            return json.dumps({
                'message': message,
                'error': True
            })
        status = table.check_columns()
        if status['error']:
            return status
        app.tables += [table]
        table_id = len(app.tables) - 1
        return json.dumps({
            "error": False,
            "id": table_id,
            "column_list": table.get_column_list()
        })
    return 'error'


@app.route('/get_column_list', methods=['POST'])
def get_column_list():
    if request.method == 'POST':
        table_id = int(request.form['id'])
        tables = app.tables
        if table_id >= len(tables):
            return 'error'
        table = tables[table_id]
        column_list = table.get_column_list()
        return json.dumps(column_list)
    return 'error'


@app.route('/set_main_key', methods=['POST'])
def set_main_key():
    if request.method == 'POST':
        table_id = int(request.form['id'])
        main_key = request.form['main_key']
        if table_id >= len(app.tables):
            return 'error'
        status = app.tables[table_id].set_main_key(main_key)
        if status:
            return 'success'
    return 'error'


@app.route('/funnel', methods=['POST'])
def funnel():
    if request.method == 'POST':
        request_data = request.get_json()
        if not isinstance(request_data, dict) or 'condition' not in request_data.keys():
            return 'error'
        condition = request_data['condition']
        if 'main_table_id' not in request_data.keys():
            return 'error'
        main_table_id = int(request_data['main_table_id'])
        if not isinstance(condition, list) or len(condition) > len(app.tables):
            return 'error'
        start = request_data['start'] if 'start' in request_data.keys() else 0
        num = request_data['num'] if 'num' in request_data.keys() else 10

        condition = sorted(condition, key=lambda x: x['id'])
        if 'funnel' not in app.current_result.keys() or app.current_result['funnel']['main_table_id'] != main_table_id \
                or app.current_result['funnel']['condition'] != condition:
            result_all, column_list = get_funnel_data(condition, main_table_id)
            app.current_result['funnel'] = {
                'main_table_id': main_table_id,
                'condition': condition,
                'result': (result_all, column_list)
            }
        else:
            result_all, column_list = app.current_result['funnel']['result']

        total = result_all.index.size
        end = start + num if start + num < total else total
        result = slice_df(result_all, start, end)

        response_data = dict()
        response_data['total'] = total
        response_data['page_now'] = int(end / num)
        response_data['page_total'] = int((total + num - 1) / num)
        response_data['next_start'] = end
        response_data['column_list'] = column_list
        response_data['data'] = result.to_dict('records')

        return json.dumps(response_data)


def get_funnel_data(condition, main_table_id):
    be_in = list()
    be_out = set()
    common_column = list()
    fixed_table = app.tables[main_table_id]
    for item in condition:
        table_id = item['id']
        exist = item['exist']
        table = app.tables[table_id]
        main_key = table.main_key
        if len(common_column) is 0:
            common_column = table.get_column_list()
        else:
            common_column = intersection_safe(common_column, table.get_column_list())
        if exist is 1:
            if len(be_in) is 0:
                be_in = table[main_key]
            else:
                be_in = intersection_safe(be_in, table[main_key])
        elif exist is 0:
            be_out = union(be_out, table[main_key])

    be_in = difference_safe(be_in, be_out)
    columns = fixed_table.get_column_list()
    if '序号' in columns:
        columns.remove('序号')
    result_all = fixed_table.get_list_by_list_columns(be_in, columns)
    index = pd.Series(range(1, len(result_all) + 1))
    index.rename('xh', inplace=True)
    result_all.index = index
    result_all.insert(0, '序号', result_all.index)
    return result_all, result_all.columns.tolist()


@app.route('/diff', methods=['POST'])
def diff():
    if request.method == 'POST':
        request_data = request.get_json()
        if not isinstance(request_data, dict) or 'ids' not in request_data.keys():
            return 'error'
        ids = request_data['ids']
        if not isinstance(ids, list) or len(ids) > len(app.tables) or len(ids) is not 2:
            return 'error'
        start = request_data['start'] if 'start' in request_data.keys() else 0
        num = request_data['num'] if 'num' in request_data.keys() else 10

        ids = sorted(ids, key=lambda x: int(x))
        if 'diff' not in app.current_result.keys() or app.current_result['diff']['ids'] != ids:
            result_all, column_list = get_diff_data(ids)
            app.current_result['diff'] = {
                'ids': ids,
                'result': (result_all, column_list)
            }
        else:
            result_all, column_list = app.current_result['diff']['result']

        total = len(result_all)
        end = start + num if start + num < total else total
        response_data = dict()
        response_data['total'] = total
        response_data['page_now'] = int(end / num)
        response_data['page_total'] = int((total + num - 1) / num)
        response_data['next_start'] = end
        response_data['column_list'] = column_list
        response_data['data'] = result_all[start:end].to_dict('records')

        return json.dumps(response_data)
    return 'error'


def get_diff_data(ids):
    be_in = list()
    common_column = list()
    fixed_table = None
    for table_id in ids:
        table = app.tables[table_id]
        main_key = table.main_key
        if len(common_column) is 0:
            common_column = table.get_column_list()
        else:
            common_column = intersection_safe(common_column, table.get_column_list())
        if fixed_table is None:
            fixed_table = table
        if len(be_in) is 0:
            be_in = table[main_key]
        else:
            # be_in = union_safe(be_in, table[main_key])
            be_in = intersection_safe(be_in, table[main_key])

    if '序号' in common_column:
        common_column.remove('序号')
    pre_diff_tables = list()
    for table_id in ids:
        table = app.tables[table_id]
        temp_common_column = [table.main_key] + common_column if table.main_key not in common_column \
            else common_column
        pre_table = copy.deepcopy(table)
        pre_table.data = table.get_list_by_columns(temp_common_column)
        pre_table.rename(columns={pre_table.main_key: fixed_table.main_key})
        pre_diff_tables += [pre_table]

    # ensure main_key is the first column
    if fixed_table.main_key in common_column:
        common_column.remove(fixed_table.main_key)
    common_column = [fixed_table.main_key] + common_column

    frames = list()
    for table in pre_diff_tables:
        frames.append(table.data[table.data.index.isin(be_in)])
    result_all = pd.concat(frames, axis=1, sort=False)
    new_columns = common_column + list(map(lambda x: x + '_对比', common_column))
    result_all.columns = new_columns

    periods = len(common_column)
    be_error = list()
    for index in be_in:
        for i in range(1, periods):
            if result_all.loc[index][i] != result_all.loc[index][i + periods]:
                be_error.append(index)
                break
    result_all = result_all[result_all.index.isin(be_error)]
    index = pd.Series(range(1, len(result_all) + 1))
    index.rename('序号', inplace=True)
    result_all.index = index
    return result_all, new_columns


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
