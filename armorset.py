#! python
import os.path

import constants as con
import functions as fnc


class ArmorSet:
    def __init__(self, data):
        self.model = data['model']
        self.name = data['name']
        self.pack = data['pack']
        self.rank = data['rank']
        self.rarity = data['rarity']
        self.slots = data['slots']
        self.recs = data['base_swaps']
        self.set_notes = data['set_notes']

        self.label = 'AFA {}'.format(self.name)
        self.is_rec = len(self.recs) > 0

    def empty_mod(self, mode=0):
        if self.pack == 0:
            pkg = con.packs[(self.pack, self.rarity)]
            mod_path = '{}AFA {}\\'.format(pkg.pack_path(mode), self.name)

        else:
            pkg = con.packs[self.pack]
            mod_path = '{}AFA {}\\'.format(pkg.pack_path(), self.name)

        if not os.path.exists(mod_path):
            os.makedirs(mod_path)

        with open('{}{}'.format(mod_path, 'modinfo.ini')) as m:
            m.write(fnc.modinfo(
                name='AFA {}'.format(self.name),
                desc=self.set_notes,
                parent='Rarity {}'.format(self.rarity)
            ))
