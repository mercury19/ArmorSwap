#! python
import itertools
import json
import operator
import os.path
import re
import shutil

import constants as con
import functions as fnc

from pack import Rank, Rarity
from armorset import ArmorSet

# read json file into a list of named tuples
with open('ArmorSets.json') as data_file:
    raw_data = json.load(data_file)
    armor_data = [ArmorSet(d) for d in raw_data]


def build_modular(item, pak):
    item.empty_mod()
    for v in con.version:
        for s in con.streaming:
            src_path = fnc.get_src_path(v, s, item.model)

            if os.path.exists(src_path):
                files = os.listdir(src_path)
                files.sort(key=lambda y: fnc.file_sort_key(y))
                parts_dict = {k: list(g) for k, g in itertools.groupby(
                    files,
                    lambda z: fnc.file_sort_key(z)
                )}

                for slot in item.slots:
                    slot_name = '{} {}'.format(item.name, slot['name'])
                    full_dest = '{}{}\\{}'.format(
                        pak.pack_path(),
                        slot_name,
                        con.files_path.substitute(
                            con.dest_keys,
                            s4=s,
                            s6=item.model
                        )
                    )

                    with open('{}{}'.format(pak.pack_path(), slot_name)) as m:
                        m.write(fnc.modinfo(
                            name=slot_name,
                            desc=slot['notes'],
                            parent=item.label
                        ))

                    fnc.copy_and_rename(slot['ids'], parts_dict, src_path, full_dest)


def main():
    # sort the data for grouping
    armor_data.sort(key=lambda x: (x.pack, x.rank, x.rarity, x.model))
    # First, group by packs
    pack_groups = [(k, list(g)) for k, g in itertools.groupby(
        armor_data,
        key=operator.itemgetter(2)
    )]

    for p in pack_groups:
        # This is the really complex? Tedious? pack style
        if p[0] == 0:
            # group by ranks for further subdivision
            rank_groups = fnc.get_groups(p[1], 3)

            for rnk in rank_groups:
                pkg = con.packs[(p[0], rnk[0])]

                rarity_groups = fnc.get_groups(rnk[1], 4)
                for rar in rarity_groups:
                    cur_ra = Rarity(rar[0], pkg, pkg)
                    cur_ra.rarity_mod()
                    for armor_set in rar[1]:
                        build_modular(armor_set, pkg)

                        if armor_set.is_rec > 0:
                            for b in armor_set.recs:
                                if len(str(b)) > 1:
                                    for v in con.version:
                                        for s in con.streaming:
                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=armor_set.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                folder_name = armor_set.name
                                                for i in str(b):
                                                    folder_name = (folder_name + ' {}'.format(armor_set.slots[int(i)]['name']))

                                                full_dest_2 = '{}{}\\{}'.format(pkg.pack_path(1), folder_name, con.files_path.substitute(con.dest_keys, s4=s, s6=armor_set.model))

                                                for part_a in str(b):
                                                    for part_id in armor_set.slots[int(part_a)]['ids']:
                                                        for part_file in parts_dict[part_id]:
                                                            renamed = re.sub('m_','f_', part_file)

                                                            # shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))
                                                            print(
                                                                'Copying {}\\{} '.format(
                                                                    src_path,
                                                                    part_file),
                                                                'to {}\\{}'.format(
                                                                    full_dest_2,
                                                                    renamed))

                                # If 5 is an item, it should be the only item, and all 'slots' will go in one folder
                                elif b == 5:
                                    for v in con.version:
                                        for s in con.streaming:

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=armor_set.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)

                                                full_dest_2 = ('{}{}\\{}').format(pkg.pack_path(1), armor_set.name, con.files_path.substitute(con.dest_keys, s4=s, s6=armor_set.model))

                                                for part_file in files:
                                                    renamed = re.sub('m_','f_', part_file)

                                                    # shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))
                                                    print(
                                                        'Copying {}\\{} '.format(
                                                            src_path,
                                                            part_file),
                                                        'to {}\\{}'.format(
                                                            full_dest_2,
                                                            renamed))

                                # Otherwise, it should be a single digit matching an index in 'slots' that can be copied to a folder with that slot name.
                                else:
                                    for v in con.version:
                                        for s in con.streaming:

                                            src_path = '{}{}'.format(con.base_path.substitute(con.src_keys,s2=v), con.files_path.substitute(con.src_keys, s4=s, s6=armor_set.model))

                                            if os.path.exists(src_path):
                                                files = os.listdir(src_path)
                                                files.sort(key=lambda y: fnc.file_sort_key(y))
                                                parts_dict = {k: list(g) for k, g in itertools.groupby(files, lambda z: fnc.file_sort_key(z))}

                                                full_dest_2 = (
                                                    '{}{} {}\\{}').format(pkg.pack_path(1), armor_set.name, armor_set.slots[b]['name'], con.files_path.substitute(con.dest_keys, s4=s, s6=armor_set.model))

                                                for part_id in armor_set.slots[b]['ids']:
                                                    if part_id in parts_dict:
                                                        for part_file in parts_dict[part_id]:
                                                            renamed = re.sub('m_', 'f_', part_file)

                                                            # shutil.copy2('{}\\{}'.format(src_path, part_file), '{}\\{}'.format(full_dest_2, renamed))
                                                            print(
                                                                'Copying {}\\{} '.format(
                                                                    src_path,
                                                                    part_file),
                                                                'to {}\\{}'.format(
                                                                    full_dest_2,
                                                                    renamed))

        else:
            pkg = con.packs[p[0]]

            rank_groups = fnc.get_groups(p[1], 3)

            for rnk in rank_groups:
                cur_rank = Rank(con.ranks[rnk[0]], pkg)
                cur_rank.rank_mod()
                rarity_groups = fnc.get_groups(rnk[1], 4)

                for rar in rarity_groups:
                    cur_rarity = Rarity(rar[0], pkg, cur_rank)
                    cur_rarity.rarity_mod()
                    for armor_set in rar[1]:
                        build_modular(armor_set, pkg)


if __name__ == '__main__':
    main()
