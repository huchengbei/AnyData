import pandas as pd
import yaml

from table import Table
from util.functions import intersection_safe, check_records


def test1():
    list1 = ['序号', '乡(镇)', '行政村', '自然村', '姓名', '证件号码', '脱贫年度', '人数', '与户主关系', '民族', '脱贫属性']
    list2 = ['序号', '县区', '镇', '村', '组', '合疗证号', '户主', '姓名', '成员属性', '身份证号', '是否新生儿', '性别', '出生日期', '与户主关系', '家庭地址']
    l = intersection_safe(list1, list2)
    print(l)


def test2():
    config_file = open('config.yaml', encoding='utf-8')
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    config_file.close()
    the_poors = open('the_poors.csv', encoding='utf-8')
    the_poors_config = config['thePoors']
    first_line = True
    index = 1
    iterms = {}
    for line in the_poors.readlines():
        if first_line:
            first_line = False
            continue
        data = line.strip().split(',')
        sfzid = (data[the_poors_config['sfzid'] - 1])
        iterms[sfzid] = data
        print(data)


def test3():
    a = ['b', 'a', 'c']
    b = ['d', 'b', 'c']
    from util.functions import union_safe
    c = union_safe(a, b)
    from util.functions import union
    c = union(a, b)
    print(c)


def test4():
    test = pd.read_csv('resources/test.csv', encoding='utf-8')
    print(test.to_dict('index'))
    print(type(test.to_dict('records')))
    print(test.slice_shift(2, 0))


def test5():
    dic = dict()
    dic['d'] = 'd'
    dic['a'] = 'a'
    print(dic)


def test6():
    test = pd.read_csv('resources/test.csv', encoding='utf-8')
    print(test.loc[0].tolist())
    l = list()
    l.append([1, 2])
    l.append([3, 4, 5])
    l.append([6, 7])
    print(check_records(l))


def test7():
    test = Table('resources/test.csv')
    print(test.data)
    test.set_main_key('证件号码')
    print(test.data)
    print(test.data.columns.values)
    print(test.data.loc['610328197102063319'].values.tolist())
    print(test.data.loc['610328197102063319'][0])
    print(test.data.loc['610328197102063319'][1])
    print(type(test.data.loc['610328197102063319'][0]))
    print(test.data[2:3])
    print(test.data[test.data.index.isin(['610328197102063319'])])
    test.data.drop(index='610328197102063319', inplace=True)
    test.data.columns = ['a', 'b']
    print(test.data)
    print(type(test.data.index[2]))
    print(test.data.index.tolist())


def test8():
    df = pd.DataFrame([[1, 2], [4, 5], [7, 8]],
                      index=['cobra', 'viper', 'sidewinder'],
                      columns=['max_speed', 'shield'])
    print(df.loc['cobra'])
    print(['']*3)


def test9():
    the_poor = Table('resources/the_poors.csv')
    ana = the_poor.analyze_col('民族')
    temp_list = list(sorted(ana.items(), key=lambda x: x[1]))
    print(temp_list)
    print(ana)


def test10():
    the_poor = Table('resources/the_poors.csv')
    columns = the_poor.data.columns
    print(columns)
    for item in columns:
        if '.1' in item:
            print('ddddddddddddddd')
    print(type(columns[7]))
    print(type(columns))
    print(columns.is_unique)


test10()
