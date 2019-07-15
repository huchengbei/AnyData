import copy
from io import StringIO

import pandas as pd
from flask import Flask, request, make_response
from pandas.io.json import json

from table import Table
from util.functions import intersection_safe, union, difference_safe, slice_df

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
app.tables = []
app.current_result = {}


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/reset', methods=['POST'])
def reset():
    app.tables = []
    return 'success'


# @app.route('/export', methods=['POST'])
@app.route('/export')
def export():
    # if request.method == 'POST':
    if True:
        # operation = request.form['operation']
        operation = request.args['operation']
        filename = 'output.csv'
        result = None
        if operation == 'funnel':
            result = app.current_result['funnel']['result'][0]
        elif operation == 'diff':
            result = app.current_result['diff']['result'][0]
        out = StringIO()
        result.to_csv(out)
        resp = make_response(out.getvalue())
        resp.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
        resp.headers["Content-type"] = "text/csv"
        return resp
    return 'error'


@app.route('/load_data', methods=['POST'])
def load_data():
    if request.method == 'POST':
        path = request.form['path']
        table = Table(path)
        app.tables += [table]
        table_id = len(app.tables) - 1
        return json.dumps({
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
        if not isinstance(condition, list) or len(condition) > len(app.tables):
            return 'error'
        start = request_data['start'] if 'start' in request_data.keys() else 0
        num = request_data['num'] if 'num' in request_data.keys() else 10

        condition = sorted(condition, key=lambda x: x['id'])
        if 'funnel' not in app.current_result.keys() or app.current_result['funnel']['condition'] != condition:
            result_all, column_list = get_funnel_data(condition)
            app.current_result['funnel'] = {
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
        response_data['next_start'] = end
        response_data['column_list'] = column_list
        response_data['data'] = result.to_dict('records')

        return json.dumps(response_data)


def get_funnel_data(condition):
    be_in = list()
    be_out = set()
    common_column = list()
    fixed_table = None
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
            if fixed_table is None:
                fixed_table = table
            if len(be_in) is 0:
                be_in = table[main_key]
            else:
                be_in = intersection_safe(be_in, table[main_key])
        elif exist is 0:
            be_out = union(be_out, table[main_key])

    if '序号' in common_column:
        common_column.remove('序号')
    be_in = difference_safe(be_in, be_out)
    if fixed_table.main_key not in common_column:
        common_column = [fixed_table.main_key] + common_column
    result_all = fixed_table.get_list_by_list_columns(be_in, common_column)
    return result_all, common_column


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
    common_column.remove('与户主关系')
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
    return result_all, new_columns


if __name__ == '__main__':
    app.run(debug=True)
    # app.run()
