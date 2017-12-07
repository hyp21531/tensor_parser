

import sys
import argparse
from .index_map import index_map
from .tensor_config import tensor_config


def parse_args(cmd_args=None):
  my_description = '''
    Construct a tensor from CSV-like files. The files can either be in plain
    text form or compressed (.gz or .bz2).

    Fields can be specified by their name if the CSV file has a header, or
    otherwise can be specified with a 1-indexed integer corresponding to their
    column in the CSV file.

    If no field is provided for tensor values ('--vals'), then a binary tensor
    is constructed.
  '''
  parser = argparse.ArgumentParser(description=my_description,
      formatter_class=argparse.RawTextHelpFormatter)


  #
  # Required positional arguments
  #
  parser.add_argument('csv', type=str, nargs='+', help='CSV files to parse')
  parser.add_argument('tensor',  type=str, help='output tensor file (.tns)')


  #
  # Adding and modifying tensor modes
  #
  parser.add_argument('-f', '--field', type=str, action='append',
      help='include FIELD as tensor mode')
  parser.add_argument('--vals', type=str,
      help='the field to use for values')

  parser.add_argument('-l', '--sort-lex', type=str, action='append',
      help="sort a fields's keys lexicographically")
  parser.add_argument('-n', '--sort-num', type=str, action='append',
      help="sort a fields's integer keys")


  #
  # CSV configuration
  #
  parser.add_argument('-F', '--field-sep', type=str, default=',',
      help='CSV field separator (default: auto)')

  #
  # Parse arguments.
  #
  args = None
  if cmd_args is not None:
    # parse provided args
    args = cmd_args=parser.parse_args(cmd_args)
  else:
    # parse sys.argv
    args = cmd_args=parser.parse_args()

  # fill in lists if not present
  if not args.field:
    print('WARN: tensor has no modes specified.', file=sys.stderr)
    args.field = []
  if not args.sort_lex:
    args.sort_lex = []
  if not args.sort_num:
    args.sort_num = []


  # Build tensor configuration
  config = tensor_config(csv_names=cmd_args.csv, tensor_name=cmd_args.tensor)
  config.set_delimiter(cmd_args.field_sep)
  for f in cmd_args.field:
    config.add_mode(f)
  for f in cmd_args.sort_lex:
    config.set_mode_sort(f, index_map.SORT_LEX)
  for f in cmd_args.sort_num:
    config.set_mode_sort(f, index_map.SORT_INT)
  config.set_vals(cmd_args.vals)

  return config


