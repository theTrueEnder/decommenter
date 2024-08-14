import re
import json


class Decommenter():
    def __init__(self, fname, mode):
        self.fname = fname
        self.symbol = None
        self.block_symbol = None
        if mode == 'python':
            self.symbol = '#'
            self.block_symbol = None
        elif mode == 'cstyle':
            self.symbol = '//'
            self.block_symbol = ('/*', '*/')
                
        else:
            print('Unrecognized decomment mode')
            return
        
    def _get_code(self):
        with open(self.fname, mode='r') as f:
            lines = f.readlines()
        return lines
    
    def _write_code(self, lines):
        with open(self.fname, mode='w') as f:
            f.writelines(lines)
            
    def _get_comments(self):
        with open(self.fname + '.dc.json', mode='r') as f:
            comments = json.load(f)
        return comments
    
    def _write_comments(self, comments):
        with open(self.fname + '.dc.json', mode='w') as f:
            json.dump(comments, f)
    
    # decomment code
    def decomment(self):
        # get original file
        lines = self._get_code()
        
        dc_code, comments = [], []
        for linenum, line in enumerate(lines, start=1):
            # match comment that starts with a given symbol followed by exactly one space
            # and the symbol is not preceded by a backslash
            res = re.search(r'(?<!\\)' + self.symbol + r'\s(.*)', line)
            
            # TODO: handle block comments
            
            if res is not None:
                # determine if it's an inline comment (if there's code before the comment)
                inline = bool(line[:res.start()].strip())
                comments.append({
                    "inline":  inline,
                    "linenum": linenum,
                    "comment": res.group(1).strip()
                })
                if not inline:
                    continue
            
            # remove comment from the code while retaining escaped cymbols
            code_line = re.sub(r'(?<!\\)' + self.symbol + r'\s.*', '', line)
            dc_code.append(code_line.rstrip() + '\n')  # Remove trailing whitespace only                 

        self._write_code(dc_code)
        self._write_comments(comments)
            
        print(f'{self.fname} decommented.')


    # recomment python code
    def recomment(self):
        # load comments file
        comments = self._get_comments()
        
        # load decommented code file
        lines = self._get_code()
            
        for comment in comments:
            inline, linenum, comment = tuple(comment.values())
            
            # TODO: add support for block comments
            
            # if inline, append to code line
            # otherwise, insert new line with comment (matches indentation of following line) 
            if inline:
                lines[linenum-1] = lines[linenum-1][:-1] + f'  {self.symbol} {comment}\n'
            else:
                ws = re.match(r"\s*", lines[linenum-1]).group()
                lines.insert(linenum - 1, f'{ws}# {comment}\n')
        
        # write changes over original code
        self._write_code(lines)

        print(f'{self.fname} recommented.')