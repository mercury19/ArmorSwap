#! python
import re
import string

from pack import Pack, SubPack

# Json Fields
# model: str - the model id
# name: str - the name of the armor set
# pack: int - the pack style for the armor set
# rank: int - the rank (low, high, master, layered)
# rarity: int - rarity in range 1 - 10
# slots: list[dicts] - data for the slots for the armor set (5 possible: Arm, Head, Body, Waist, Legs)
# base_swaps: list[int] - slots to be copied for the 'recommended' packs. multi-digit numbers represent multiple parts to be put in one folder. 5 is all in one.
# slot_ids: list[str] - this is only for the manual json editing process and is not used by the program.
# set_notes: str - Information for the armor set as a whole, to be put into an ini file.
fields = ['model', 'name', 'pack', 'rank', 'rarity', 'slots', 'base_swaps',
          'slot_ids', 'set_notes']


# s1 = source or destination
# s2 = dlc/base or bundle name
base_path = string.Template('D:\\The Drawer\\MHR Modding\\${s1}\\${s2}\\')

# s4 = streaming or not
# s5 = m or f
# s6 = set id
files_path = string.Template('natives\\STM\\${s4}player\\mod\\${s5}\\${s6}')

src_keys = {'s1': 'Base Files', 's5': 'm'}
dest_keys = {'s1': 'ArmorSwap\\Fluffy Packages', 's5': 'f'}
# ${s2} for source
version = ('re_chunk_000', 're_chunk_000.pak.patch_001')

# ${s4} streaming or not
streaming = ('', 'streaming\\')

packs = {
    (0, 0): SubPack('Low Rank'),
    (0, 1): SubPack('High Rank'),
    (0, 2): SubPack('Master Rank'),
    (0, 3): SubPack('Layered'),
    1: Pack('Partial'),
    2: Pack('Minimal')
}

parts = {
    'arm': 'Arms',
    'body': 'Body',
    'hand': 'Arms',
    'helm': 'Headgear',
    'leg': 'Legs',
    'wst': 'Waist',
}

ranks = [
    'Low Rank',
    'High Rank',
    'Master Rank',
    'Layered'
]

group_key = re.compile(r'^[a-zA-Z]+')

dummy_desc = ('This mod is empty! But you should activate it, otherwise you '
              'will get a bunch of annoying popups trying to activate the '
              'other parts of this pack.')
