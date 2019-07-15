import pandas as pd
import yaml

pd.set_option('display.max_columns', None)
pd.set_option('max_colwidth', 1000)
the_poors = pd.read_csv('resources/the_poors.csv', dtype='str')
the_poors_with_cm = pd.read_csv('resources/the_poors_with_cm.csv', dtype='str')
# the_poors['证件号码'] = the_poors['证件号码'].map(lambda x: x[0:18])
# the_poors_with_cm['身份证号'] = the_poors_with_cm['身份证号'].map(lambda x: x[0:18])

# print(the_poors[the_poors['证件号码'].isin(['610328197102063319'])])
# print(the_poors[~the_poors['证件号码'].isin(map(lambda x: str(x), the_poors_with_cm['身份证号'].tolist()))])
print(the_poors[~the_poors['证件号码'].isin(the_poors_with_cm['身份证号'].tolist())])
