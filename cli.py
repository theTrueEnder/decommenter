from decomment import *
import argparse
parser = argparse.ArgumentParser()


parser.add_argument(
    "--mode", 
    "-m",
    action="store", 
    choices=["decomment", "recomment"],
    help="select mode of operation (decomment or recomment)"
)

parser.add_argument(
    "--file", 
    "-f",
    action="store", 
    help="filename or path to the target file",
    nargs="?"
)

args = parser.parse_args()

fname = args.file
# args.mode = 'decomment'
# fname = 'code.py'

if __name__ == '__main__':
    ext = fname[fname.find('.')+1:]
    match(ext):
        case 'py':
            if args.mode == 'decomment':
                print(f'Decommenting {fname}...')
                dc_python(fname)
            elif args.mode == 'recomment':
                print(f'Recommenting {fname}...')
                rc_python(fname)
        case _:
            print(f'Filetype "{ext}" not supported.')
