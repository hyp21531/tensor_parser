

import sys
from collections import OrderedDict

class index_map:
  '''
    This class constructs and maintains a mapping of strings to contiguous
    indices in a tensor. All keys are converted to strings (`str()`) before
    insertion/access. Indices start from 1.

    After all keys have been added with `add()`, the map to continuous indices
    must be built with `build_map()`. Mappings of keys -> indices can then be
    accessed with `__getitem__()` (i.e., `my_map['apple']` will return its
    index in the tensor).

    The map supports several sorting modes to be specified at initialization.
    If no sorting is specified, keys are mapped based on their order of
    insertion.
  '''

  #
  # Static members
  #
  SORT_NONE = 0
  SORT_LEX  = 1
  SORT_NUM  = 2

  def __init__(self, sort=SORT_NONE):
    self._keys = OrderedDict()
    self._map  = dict()

    self._sort = sort
    self._is_mapped = False


  def add(self, key):
    '''
      Add a key to the map. If already present, this is a no-op.
    '''
    if not isinstance(key, str):
      key = str(key)
    self._keys[key] = 1


  def build_map(self):
    '''
      Build a mapping of keys -> indices. This should only be called after all
      keys have been added to the structure.
    '''
    uniques = list(self._keys)
    
    # sort keys if requested
    if self._sort == index_map.SORT_LEX:
      uniques = [str(x) for x in uniques]
      uniques.sort()
    elif self._sort == index_map.SORT_NUM:
      try:
        uniques = [int(x) for x in uniques]
      except ValueError as e:
        print('ERROR: discovered key that cannot be cast as integer.')
        print(e)
        sys.exit(1)
      uniques.sort()
    
    for i in range(len(uniques)):
      self._map[str(uniques[i])] = i+1

    self._is_mapped = True

  def is_mapped(self):
    return self._is_mapped


  def write_file(self, fout):
    '''
      Write an index map to a file. The map is inverted such that if map[X]=I,
      then X is written to the Ith line of `fout`.
    '''
    for key in sorted(self._map, key=self._map.get) :
      print(key, file=fout)


  def __getitem__(self, key):
    if not isinstance(key, str):
      key = str(key)

    if not self._is_mapped:
      raise Exception('ERROR: must use `build_map()` before accessing mapping.')
    
    if key not in self._map:
      raise IndexError('ERROR: key "{}" not found in map.'.format(key))

    return self._map[key]


  def __len__(self):
    return len(self._map)
