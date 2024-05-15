#! python
import os

import constants as con
import functions as fnc


class PackBuilder:
    pass


class Pack:
    def __init__(self, name):
        self.name = name

    def pack_path(self):
        p = con.base_path.substitute(con.dest_keys, s2=self.name)
        if not os.path.exists(p):
            print('Making {}'.format(p))
            # os.makedirs(p)

        return p


class SubPack(Pack):
    def __init__(self, name):
        super().__init__(name)
        self.name_e = '{} - Extended'.format(name)
        self.name_r = '{} - Recommended'.format(name)

    def pack_path(self, mode=0):
        p = con.base_path.substitute(
            con.dest_keys,
            s2=self.name_r if mode == 1 else self.name_e
        )
        if not os.path.exists(p):
            os.makedirs(p)

        return p


class Rank:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent

    def rank_mod(self):
        p = '{}{}\\'.format(self.parent.pack_path(), self.name)

        if not os.path.exists(p):
            os.makedirs(p)

        with open('{}{}'.format(p, 'modinfo.ini')) as m:
            m.write(fnc.modinfo(
                name=self.name,
                desc=con.dummy_desc,
                parent=self.parent.name
            ))


class Rarity:
    def __init__(self, lvl, pkg, parent):
        self.name = 'Rarity {}'.format(lvl)
        self.pkg = pkg
        self.parent = parent
        self.sub = isinstance(pkg, SubPack)
        self.subsub = (pkg == parent)

    def rarity_mod(self, mode=0):
        if self.sub:
            p = self.pkg.pack_path(mode)
        else:
            p = self.pkg.pack_path()
        p1 = '{}{}\\'.format(p, self.name)

        if not os.path.exists(p1):
            os.makedirs(p1)

        with open('{}{}'.format(p1, 'modinfo.ini')) as m:
            if self.sub:
                if mode == 1:
                    pname = self.pkg.name_r
                else:
                    pname = self.pkg.name_e
            elif self.subsub:
                pname = self.pkg.name
            else:
                pname = self.parent.name

            m.write(fnc.modinfo(
                name=self.name,
                desc=con.dummy_desc,
                parent=pname,
                mode=0 if self.subsub else 1
            ))
