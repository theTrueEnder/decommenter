from decomment import Decommenter
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

if __name__ == '__main__':
    ext = fname[fname.find('.')+1:]
    match(ext):
        case 'py':
            dc = Decommenter(fname, 'python')
            if args.mode == 'decomment':
                print(f'Decommenting {fname}...')
                dc.decomment()
            elif args.mode == 'recomment':
                print(f'Recommenting {fname}...')
                dc.recomment()
        case _:
            print(f'Filetype "{ext}" not supported.')
