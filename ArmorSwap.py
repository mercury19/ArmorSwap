#! python
import itertools
import json
import operator
import os.path
import re
import shutil

import constants as con
import functions as fnc
from collections import namedtuple

# fields are defined in constants.py
ArmorSet = namedtuple('ArmorSet', con.fields)

# read json file into a list of named tuples
with open('ArmorSets.json') as f:
    raw_data = json.load(f)
    armor_data = [ArmorSet(**o) for o in raw_data]


def main():
    # sort the data for grouping
    armor_data.sort(key=operator.itemgetter(2, 3, 4, 0))
    # First, group by packs
    pack_groups = [(k, list(g)) for k, g in itertools.groupby(armor_data, key=operator.itemgetter(2))]

    for p in pack_groups:
        # This is the really complex? Tedious? pack style
        if p[0] == 0:
            # group by ranks for further subdivision
            rank_groups_a = [(k, list(g)) for k, g in itertools.groupby(p[1], key=operator.itemgetter(3))]

            for r in rank_groups_a:
                if r[0] == 0:
                    # All pack: 0 armor sets get put into a 'rank - extended' pack, one folder for each slot in slots
                    for x in r[1]:
                        for v in con.version:
                            for s in con.streaming:
                                dest_1 = con.base_path.substitute(con.dest_keys, s2='Low Rank - Extended')

                                src_path = '{}{}'.format(con.base_path.substitute(con.src_keys, s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                if os.path.exists(src_path):
                                    files = os.listdir(src_path)
                                    files.sort(key=lambda y: fnc.file_sort_key(y))
                                    parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                    for slot in x.slots:
                                        full_dest = '{}{} {}\\{}'.format(dest_1, x.name, slot['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                        for part_id in slot['ids']:
                                            for part_file in parts_dict[part_id]:
                                                renamed = re.sub('m_', 'f_', part_file)

                                                shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest, renamed))

                        # If there are base swaps, then the armor set also gets a 'rank - recommended' pack, with fodlers for the designated parts
                        if len(x.base_swaps) > 0:
                            for b in x.base_swaps:
                                # Parsing the multi-digit items. There has to be a better way to split them, but I haven't figured it out yet.
                                # This whole section is really messy and rough.
                                if len(str(b)) > 1:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Low Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                folder_name = x.name
                                                for i in str(b):
                                                    folder_name = (folder_name + ' {}'.format(x.slots[i]['name']))

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, folder_name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_a in b:
                                                    for part_id in part_a['ids']:
                                                        for part_file in parts_dict[part_id]:
                                                            renamed = re.sub('m_','f_', part_file)

                                                            shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                # If 5 is an item, it should be the only item, and all 'slots' will go in one folder
                                elif b == 5:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Low Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, x.name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_file in files:
                                                    renamed = re.sub('m_','f_', part_file)

                                                    shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                # Otherwise, it should be a single digit matching an index in 'slots' that can be copied to a folder with that slot name.
                                else:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Low Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                full_dest_2 = (
                                                    '{}{} {}\\{}').format(dest_2, x.name, x.slots[b]['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_id in x.slots[b]['ids']:
                                                    for part_file in parts_dict[part_id]:
                                                        renamed = re.sub('m_', 'f_', part_file)

                                                        shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                # Now the above needs to be done all over again, with the only difference being the 'rank' part of the pack name!
                # This can obviously be collapsed into one or more functions using a list of pack names and index numbers as funciton arguments or something,
                # but I'm not sure how to break it up yet.
                if r[0] == 1:
                    for x in r[1]:
                        for v in con.version:
                            for s in con.streaming:
                                dest_1 = con.base_path.substitute(con.dest_keys, s2='High Rank - Extended')

                                src_path = '{}{}'.format(con.base_path.substitute(con.src_keys, s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                if os.path.exists(src_path):
                                    files = os.listdir(src_path)
                                    files.sort(key=lambda y: fnc.file_sort_key(y))
                                    parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                    for slot in x.slots:
                                        full_dest = '{}{} {}\\{}'.format(dest_1, x.name, slot['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                        for part_id in slot['ids']:
                                            for part_file in parts_dict[part_id]:
                                                renamed = re.sub('m_', 'f_', part_file)

                                                shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest, renamed))

                        if len(x.base_swaps) > 0:
                            for b in x.base_swaps:
                                if len(str(b)) > 1:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='High Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                folder_name = x.name
                                                for i in str(b):
                                                    folder_name = (folder_name + ' {}'.format(x.slots[i]['name']))

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, folder_name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_a in b:
                                                    for part_id in part_a['ids']:
                                                        for part_file in parts_dict[part_id]:
                                                            renamed = re.sub('m_','f_', part_file)

                                                            shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                elif b == 5:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='High Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, x.name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_file in files:
                                                    renamed = re.sub('m_','f_', part_file)

                                                    shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                else:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='High Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                full_dest_2 = (
                                                    '{}{} {}\\{}').format(dest_2, x.name, x.slots[b]['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_id in x.slots[b]['ids']:
                                                    for part_file in parts_dict[part_id]:
                                                        renamed = re.sub('m_', 'f_', part_file)

                                                        shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                if r[0] == 2:
                    for x in r[1]:
                        for v in con.version:
                            for s in con.streaming:
                                dest_1 = con.base_path.substitute(con.dest_keys, s2='Master Rank - Extended')

                                src_path = '{}{}'.format(con.base_path.substitute(con.src_keys, s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                if os.path.exists(src_path):
                                    files = os.listdir(src_path)
                                    files.sort(key=lambda y: fnc.file_sort_key(y))
                                    parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                    for slot in x.slots:
                                        full_dest = '{}{} {}\\{}'.format(dest_1, x.name, slot['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                        for part_id in slot['ids']:
                                            for part_file in parts_dict[part_id]:
                                                renamed = re.sub('m_', 'f_', part_file)

                                                shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest, renamed))

                        if len(x.base_swaps) > 0:
                            for b in x.base_swaps:
                                if len(str(b)) > 1:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Master Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                folder_name = x.name
                                                for i in str(b):
                                                    folder_name = (folder_name + ' {}'.format(x.slots[i]['name']))

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, folder_name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_a in b:
                                                    for part_id in part_a['ids']:
                                                        for part_file in parts_dict[part_id]:
                                                            renamed = re.sub('m_','f_', part_file)

                                                            shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                elif b == 5:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Master Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, x.name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_file in files:
                                                    renamed = re.sub('m_','f_', part_file)

                                                    shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                else:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Master Rank - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                full_dest_2 = (
                                                    '{}{} {}\\{}').format(dest_2, x.name, x.slots[b]['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_id in x.slots[b]['ids']:
                                                    for part_file in parts_dict[part_id]:
                                                        renamed = re.sub('m_', 'f_', part_file)

                                                        shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                if r[0] == 3:
                    for x in r[1]:
                        for v in con.version:
                            for s in con.streaming:
                                dest_1 = con.base_path.substitute(con.dest_keys, s2='Layered - Extended')

                                src_path = '{}{}'.format(con.base_path.substitute(con.src_keys, s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                if os.path.exists(src_path):
                                    files = os.listdir(src_path)
                                    files.sort(key=lambda y: fnc.file_sort_key(y))
                                    parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                    for slot in x.slots:
                                        full_dest = '{}{} {}\\{}'.format(dest_1, x.name, slot['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                        for part_id in slot['ids']:
                                            for part_file in parts_dict[part_id]:
                                                renamed = re.sub('m_', 'f_', part_file)

                                                shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest, renamed))

                        if len(x.base_swaps) > 0:
                            for b in x.base_swaps:
                                if len(str(b)) > 1:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Layered - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                folder_name = x.name
                                                for i in str(b):
                                                    folder_name = (folder_name + ' {}'.format(x.slots[i]['name']))

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, folder_name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_a in b:
                                                    for part_id in part_a['ids']:
                                                        for part_file in parts_dict[part_id]:
                                                            renamed = re.sub('m_','f_', part_file)

                                                            shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                elif b == 5:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Layered - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)

                                                full_dest_2 = ('{}{}\\{}').format(dest_2, x.name, con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_file in files:
                                                    renamed = re.sub('m_','f_', part_file)

                                                    shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

                                else:
                                    for v in con.version:
                                        for s in con.streaming:
                                            dest_2 = (con.base_path.substitute(con.dest_keys, s2='Layered - Recommended'))

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                full_dest_2 = (
                                                    '{}{} {}\\{}').format(dest_2, x.name, x.slots[b]['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                                for part_id in x.slots[b]['ids']:
                                                    for part_file in parts_dict[part_id]:
                                                        renamed = re.sub('m_', 'f_', part_file)

                                                        shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))

        # The next two pack styles are done identically, will be made into a function.
        # However I want it to share a function with the previous step, as much of the process is identical, or close to it.
        elif p[0] == 1:
            for x in p[1]:
                for v in con.version:
                    for s in con.streaming:
                        dest_1 = con.base_path.substitute(con.dest_keys, s2='Partial')

                        src_path = '{}{}'.format(con.base_path.substitute(con.src_keys, s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                        if os.path.exists(src_path):
                            files = os.listdir(src_path)
                            files.sort(key=lambda y: fnc.file_sort_key(y))
                            parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                            for slot in x.slots:
                                full_dest = '{}{} {}\\{}'.format(dest_1, x.name, slot['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                for part_id in slot['ids']:
                                    for part_file in parts_dict[part_id]:
                                        renamed = re.sub('m_', 'f_', part_file)

                                        shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest, renamed))

        elif p[0] == 2:
            for x in p[1]:
                for v in con.version:
                    for s in con.streaming:
                        dest_1 = con.base_path.substitute(con.dest_keys, s2='Minimal')

                        src_path = '{}{}'.format(con.base_path.substitute(con.src_keys, s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=x.model))

                        if os.path.exists(src_path):
                            files = os.listdir(src_path)
                            files.sort(key=lambda y: fnc.file_sort_key(y))
                            parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                            for slot in x.slots:
                                full_dest = '{}{} {}\\{}'.format(dest_1, x.name, slot['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=x.model))

                                for part_id in slot['ids']:
                                    for part_file in parts_dict[part_id]:
                                        renamed = re.sub('m_', 'f_', part_file)

                                        shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest, renamed))


if __name__ == '__main__':
    main()
