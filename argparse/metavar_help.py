import argparse

parser = argparse.ArgumentParser(description='about metavar')
parser.add_argument('-i', type=int, metavar='<input file path>', help='input file')
parser.add_argument('-r', '--radius', type=int, metavar='', help='Radius of cylinder')
parser.add_argument('-H', '--height', type=int, help='Height of cylinder')

args = parser.parse_args()
parser.print_help()

"""
usage: metavar_help.py [-h] [-r] [-H HEIGHT]

about metavar

optional arguments:
  -h, --help            show this help message and exit
  -i <input file path>  input file
        ^
    <metavar>
  -r , --radius         Radius of cylinder
  -H HEIGHT, --height HEIGHT
                        Height of cylinder
        ^               ^
    <metavar>        <metavar>
"""