#! python
import itertools
import operator
import re
import shutil
import string

import constants as con


def get_src_path(version, streaming, model):
    keys = {'s2': version, 's4': streaming, 's6': model} | con.src_keys

    return '{}{}'.format(
        con.base_path.substitute(keys),
        con.files_path.substitute(keys)
    )


def modinfo(name, desc, parent, mode=0):
    modes = ['AddonFor', 'NameAsBundle']
    content = ('name={name}\ncategory=Armor\nauthor=mercury19'
               '\n{mode_label}={parent}\ndescription={desc}').format(
        name, modes[mode], parent, desc
    )
    return content


def file_sort_key(item):
    return re.compile(r'^\D+').match(item).group()


def copy_and_rename(ids, parts, source, dest):
    for part_id in ids:
        if part_id in parts:
            for file in parts[part_id]:
                new_file = re.sub('m_', 'f_', file)
                shutil.copy2(
                    '{}\\{}'.format(source, file),
                    '{}\\{}'.format(dest, new_file)
                )


def get_groups(data, key):
    return [(k, list(g)) for k, g in itertools.groupby(
        data,
        key=operator.itemgetter(key)
    )]
