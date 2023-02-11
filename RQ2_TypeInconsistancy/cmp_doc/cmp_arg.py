import json
import os

P1='data_adobe'
P3='data_doc'

global_fname = 'tmpresult.txt'
TypeNum2Str = {'0': "Boolean", '1': "Number", '2': "builtin-obj", '3': "String", '220': "Array", '221': "Array", '222': "Array", '223': "Array", '231': "Object",'5': "Value", '50': "Value", '51': "Value", '210': "Value", '52': "Value", '53': "Value"}

def convert_num2str(type_number):
    res = ''
    if type_number.startswith('5'):
        res = 'Value'
    elif type_number.startswith('22'):
        res = 'Array'
    elif type_number.startswith('23'):
        res = 'Object'
    else:
        res = TypeNum2Str[type_number]

    return res

def dump_file(content):
    with open(global_fname, 'a') as f:
        f.write(content)


def parse_type(typeid):
    if typeid == '2':
        return '20'
    elif typeid == '5':
        return '50'
    elif typeid[0] == '5' and len(typeid) > 1:
        return '51'
    elif len(typeid) > 1:
        return typeid[:2]
    else:
        return typeid


def compare_value(typeid1, typeid2):
    t1 = parse_type(str(typeid1))
    t2 = parse_type(str(typeid2))
    if t1 == t2:
        return True
    else:
        return False


def print_info(typeid, dic):
    if typeid in dic['info']:
        # return repr(dic['info'][typeid])
        return convert_num2str(str(typeid))
    else:
        return convert_num2str(str(typeid))


def compare_setter(dic1, dic2):
    apiname = dic1['api']
    t1 = dic1['root']
    t2 = dic2['root']
    flag = compare_value(t1, t2)
    if flag == False:
        tmp = 'setter:%s\n- TypeOracle: %s\n- Manual: %s\n' % (
            apiname, print_info(t1, dic1), print_info(t2, dic2))
        dump_file(tmp)


def compare_json(dic1, dic2):
    apiname = dic1['api']
    r1 = dic1['info'][dic1['root']]
    r2 = dic2['info'][dic2['root']]
    d1 = {}
    d2 = {}
    for k, v in zip(r1['req_key'], r1['req_type']):
        d1[k] = v
    for k, v in zip(r1['opt_key'], r1['opt_type']):
        d1[k] = v
    for k, v in zip(r2['req_key'], r2['req_type']):
        d2[k] = v
    for k, v in zip(r2['opt_key'], r2['opt_type']):
        d2[k] = v
    sumk = set(d1.keys()) | set(d2.keys())
    flag = 0
    content = 'method json-json: %s\n' % apiname
    if len(d1.keys()) != len(d2.keys()):
        flag = 1
        content += '- diff in arg length: TypeOracle - %s , Manual - %s\n' % (
            len(d1.keys()), len(d2.keys()))
    for k in sumk:
        if k not in d1:
            content += '- TypeOracle lack key: %s\n' % (k)
            flag = 1
        elif k not in d2:
            content += '- Manual lack key: %s\n' % (k)
            flag = 1
        else:
            tp = compare_value(d1[k], d2[k])
            if tp == False:
                flag = 1
                content += '- key:%s\tTypeOracle: %s\tManual: %s\n' % (
                    k, print_info(d1[k], dic1), print_info(d2[k], dic2))
    if flag == 1:
        dump_file(content)


def compare_array(dic1, dic2):
    apiname = dic1['api']
    r1 = dic1['info'][dic1['root']]
    r2 = dic2['info'][dic2['root']]
    l1 = []
    l2 = []
    l1.extend(r1['req_type'])
    l1.extend(r1['opt_type'])
    l2.extend(r2['req_type'])
    l2.extend(r2['opt_type'])

    sumk = min(len(l1), len(l2))

    flag = 0
    content = 'method arr-arr: %s\n' % apiname

    if len(l1) != len(l2):
        flag = 1
        content += '- diff in arg length: TypeOracle - %s , Manual - %s\n' % (
            len(l1), len(l2))

    for ind in range(sumk):
        t1 = l1[ind]
        t2 = l2[ind]
        tp = compare_value(t1, t2)
        if tp == False:
            flag = 1
            content += '- ind:%d\tTypeOracle: %s\tManual: %s\n' % (
                ind, print_info(t1, dic1), print_info(t2, dic2))

    if flag == 1:
        dump_file(content)


def compare_json_and_array(dic1, dic2):
    apiname = dic1['api']
    r1 = dic1['info'][dic1['root']]
    r2 = dic2['info'][dic2['root']]
    # print(r1)
    l1 = []
    l2 = []
    k1 = []
    l1.extend(r1['req_type'])
    l1.extend(r1['opt_type'])
    k1.extend(r1['req_key'])
    k1.extend(r1['opt_type'])
    l2.extend(r2['req_type'])
    l2.extend(r2['opt_type'])

    sumk = min(len(l1), len(l2))

    flag = 0
    content = 'method json-arr: %s\n' % apiname

    if len(l1) != len(l2):
        flag = 1
        content += '- diff in arg length: TypeOracle - %s , Manual - %s\n' % (
            len(l1), len(l2))

    for ind in range(sumk):
        t1 = l1[ind]
        t2 = l2[ind]
        tp = compare_value(t1, t2)
        if tp == False:
            flag = 1
            content += '- ind:%d key:%s\tTypeOracle: %s\tManual: %s\n' % (
                ind, k1[ind], print_info(t1, dic1), print_info(t2, dic2))

    if flag == 1:
        dump_file(content)


def readjson(fname):
    with open(fname, 'r') as f:
        return json.loads(f.read())
    
def compare_full(dic1,dic2):
    if dic1['apitype'] == 1:
        compare_setter(dic1, dic2)
        return
    f1 = dic1['root']
    f2 = dic2['root']

    if f1.startswith('22') or f1.startswith('21'):
        flag1 = 0 # array
    else:
        flag1 = 1 # json

    if f2.startswith('22') or f2.startswith('21'):
        flag2 = 0
    else:
        flag2 = 1
    
    if flag1 == 0 and flag2 == 0:
        compare_array(dic1, dic2)
    elif flag1 == 1 and flag2 == 1:
        compare_json(dic1, dic2)
    elif flag1 == 0 and flag2 == 1:
        compare_json_and_array(dic2, dic1)
    else:
        compare_json_and_array(dic1, dic2)
    
def main(dir1,dir2,output):
    global global_fname
    global_fname = output
    d1 = {}
    d2 = {}
    for fname in os.listdir(dir1):
        fpath = os.path.join(dir1,fname)
        tmp = readjson(fpath)
        apiname = tmp['api']
        d1[apiname] = tmp
    for fname in os.listdir(dir2):
        fpath = os.path.join(dir2,fname)
        tmp = readjson(fpath)
        apiname = tmp['api']
        d2[apiname] = tmp
    commonkey = set(d1.keys())&set(d2.keys())
    for key in sorted(list(commonkey)):
        print(key)
        compare_full(d1[key],d2[key])

if __name__ == '__main__':
    # d1 = readjson('this_app_alert1.json')
    # d2 = readjson('this_app_alert2.json')
    # compare_json(d1, d2)
    main(P1,P3,'adobe_doc.txt')
