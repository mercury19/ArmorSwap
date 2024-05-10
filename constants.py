#! python
import re
import string

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

packs = ['Low Rank', 'High Rank', 'Master Rank']

parts = {
    'arm': 'Arms',
    'body': 'Body',
    'hand': 'Arms',
    'helm': 'Headgear',
    'leg': 'Legs',
    'wst': 'Waist',
}

group_key = re.compile(r'^[a-zA-Z]+')
