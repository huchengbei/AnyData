from functools import reduce


def intersection(a, b):
    return list(set(a).intersection(set(b)))


def intersection_safe(a, b):
    if len(a) < len(b):
        b = set(b)
        return [val for val in a if val in b]
    else:
        a = set(a)
        return [val for val in b if val in a]


def union(a, b):
    return list(set(a).union(set(b)))


def union_safe(a, b):
    b = difference_safe(b, a)
    return a+b


def difference(a, b):
    return list(set(a).difference(set(b)))


def difference_safe(a, b):
    b = set(b)
    return [val for val in a if val not in b]


def slice_df(data, start, end):
    return data.head(end).tail(end-start)


def check_records(infos):
    if len(infos[0]) is not len(infos[1]):
        return False
    for i in range(len(infos[0])):
        if infos[0][i] is not infos[1][i]:
            return False
    return True

