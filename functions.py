#! python
import itertools
import operator
import os
import re
import string

import constants


def base_path():
    return string.Template('D:\\The Drawer\\MHR Modding\\${s1}\\${s2}\\${s3}')


def files_path():
    return string.Template('natives\\STM\\${s4}player\\mod\\${s5}\\${s6}')


def modinfo():
    return string.Template('name=${name}\ncategory=Armor\nauthor'
                           '=mercury19\nNameAsBundle=${bundle}')


def file_sort_key(item):
    return re.compile(r'^\D+').match(item).group()


def pack_path(pack):
    return constants.base_path.substitute(constants.src_keys, s2=pack)


def dummy_mod(parent, name):
    dir_path = '{}\\{}'.format(pack_path(parent), name)
    os.makedirs(dir_path)

    with open('{}\\modinfo.ini'.format(dir_path)) as f:
        ...


def mk_groups(data, x):
    return [list(g) for k, g in itertools.groupby(data,
                                                  key=operator.itemgetter(x))]

