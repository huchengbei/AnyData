import os

import pandas as pd
pd.set_option('display.max_columns', None)


class Table:
    main_key = ''
    table_name = ''
    index = set()

    def __init__(self, path):
        self.table_name = os.path.basename(path)
        suffix = os.path.splitext(path)[1]
        if suffix == '.csv':
            self.data = pd.read_csv(path, dtype='str')
        elif suffix == '.xlsx':
            self.data = pd.read_excel(path, dtype='str')
        elif suffix == '.xls':
            self.data = pd.read_excel(path, dtype='str')
        else:
            pass

    def set_main_key(self, main_key):
        if main_key not in self.get_column_list():
            return False
        else:
            self.main_key = main_key
            self.data.index = self.data[self.main_key]
            # self.data = self.data.set_index(self.main_key, inplace=True)
            # self.data.set_index(self.main_key, inplace=True)
            self.index = set(self.data.index.tolist())
        return True

    def rename(self, *args, **kw):
        self.data = self.data.rename(*args, **kw)
        if self.main_key in kw['columns'].keys():
            self.set_main_key(kw['columns'][self.main_key])

    def get_records_count(self):
        if self.main_key:
            return self.data[self.main_key].count()
        return max(self.data.count())

    def get_column_list(self):
        return self.data.columns.values.tolist()

    def get_one_row_by_name(self, name):
        if name not in self.index:
            return [''] * len(self.data.columns.values)
        return self.data.loc[name].values.tolist()

    def get_one_row_by_index(self, index):
        if index > self.data.index.size:
            return [''] * len(self.data.columns.values)
        name = self.data.index[index - 1]
        return self.get_one_row_by_name(name)

    def get_one_column_by_name(self, name):
        return self.data[name].values.tolist()

    def get_one_column_by_index(self, index):
        name = self.get_column_list()[index - 1]
        return self.data[name].values.tolist()

    def get_list_by_list(self, be_in):
        return self.data[self.data[self.main_key].isin(be_in)]

    def get_list_by_columns(self, columns):
        return self.data[list(columns)]

    def get_list_by_list_columns(self, be_in, columns):
        return self.data[self.data[self.main_key].isin(be_in)][list(columns)]

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.get_one_column_by_index(item)
        return self.get_one_column_by_name(item)
