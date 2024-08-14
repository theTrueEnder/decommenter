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

cstyle_langs = {
    ".c",  # C 
    ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hh",  # C++
    ".cs",  # C#
    ".java",  # java
    ".js", ".mjs",  # javascript
    ".m", ".mm", ".h",  # objective-c
    ".go",  # go
    ".php", ".phtml",  # php
    ".rs",  # rust
    ".swift",  # swift
    ".scala", ".sc", ".sbt",  # scala
    ".kt", ".kts",  # kotlin
    ".d",  # d
    ".ts", ".tsx",  # typescript
    ".as",  # actionscript
    ".hx",  # haxe
    ".groovy", ".gvy", ".gy", ".gsh"  # groovy
    
}

pythonstyle_langs = {
    ".py",  # Python
    # ".rb",  # Ruby
    # ".pl", ".pm",  # Perl
    # ".r",   # R
    # ".sh", ".bash",  # Shell
    # ".ps1", ".psm1", ".psd1",  # PowerShell
    # # "Makefile", "Makefile"  # Makefile
    # # ".dockerfile", "Dockerfile"  # Dockerfile
    # ".yaml", ".yml",  # YAML
    # ".tcl",  # Tcl
    # ".jl",  # Julia
    # ".awk",  # Awk
    # ".m",   # MATLAB
    # ".coffee",  # CoffeeScript
    # ".ex", ".exs",  # Elixir
    # ".vim",  # Vim Script
    # ".hs",  # Haskell
}

if __name__ == '__main__':
    ext = fname[fname.find('.'):]
    if ext in pythonstyle_langs:
        dc = Decommenter(fname, 'python')
        if args.mode == 'decomment':
            print(f'Decommenting {fname}...')
            dc.decomment()
        elif args.mode == 'recomment':
            print(f'Recommenting {fname}...')
            dc.recomment()
            
    elif ext in cstyle_langs:
        dc = Decommenter(fname, 'cstyle')
        if args.mode == 'decomment':
            print(f'Decommenting {fname}...')
            dc.decomment()
        elif args.mode == 'recomment':
            print(f'Recommenting {fname}...')
            dc.recomment()
            
    else:
        print(f'Filetype "{ext}" not supported.')
