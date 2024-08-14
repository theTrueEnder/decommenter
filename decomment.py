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
            return f.read()
    
    def _write_code(self, data):
        with open(self.fname, mode='w') as f:
            f.write(data)
            
    def _get_comments(self):
        with open(self.fname + '.dc.json', mode='r') as f:
            comments = json.load(f)
        return comments
    
    def _write_comments(self, comments):
        with open(self.fname + '.dc.json', mode='w') as f:
            json.dump(comments, f)

    def decomment(self):
        # get original file
        code = self._get_code()
        
        dc_code, comments = [], []
        # block_comment = False
        
        start_sym = re.escape(self.block_symbol[0])
        end_sym = re.escape(self.block_symbol[1])
        sym = re.escape(self.symbol)
        
        r_block = re.compile(r'(\s)*' + start_sym + r'(.|\n)*' + end_sym)
        r_newline = re.compile(r'$(\s)*' + sym + r'(.*)$')
        r_inline = re.compile(r'(?<!\\)' + sym + r'(.*)$')
        
        
        block_cmts = re.findall(r_block, code, re.MULTILINE)
        re.sub(r_block, '', code, 0, re.MULTILINE)
        
        newline_cmts = re.findall(r_newline, code)
        re.sub(r_newline, '', code, 0)
        
        inline_cmts = re.findall(r_inline, code)
        re.sub(r_inline, '', code, 0)
        
        
        # for linenum, line in enumerate(lines, start=1):
            # Handle block comment start
            # res = re.search(r'(?<!\\)' + re.escape(start_sym) + r'(.*)', line)
            # res = re.search(r'(?<!\\)' + re.escape(start_sym) + r'(.*)', line)
            
            
        
        
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
                # print(f'Inline comment:\n\tLine {linenum}:', lines[linenum])
                # print(f'\tCmnt:', comment)
                # print('\tPrev:', lines[linenum-1])
                try:
                    lines[linenum-1] = lines[linenum-1][:-1] + f'  {self.symbol} {comment}\n'
                except IndexError:
                    lines.insert(linenum-1, '\n')
                    lines[linenum-1] = lines[linenum-1][:-1] + f'  {self.symbol} {comment}\n'
            else:
                try:
                    ws = re.match(r"\s*", lines[linenum-1]).group()
                except IndexError:
                    lines.insert(linenum-1, '\n')
                    ws = re.match(r"\s*", lines[linenum-1]).group()
                    
                lines.insert(linenum - 1, f'{ws}{self.symbol} {comment}\n')
        
        # write changes over original code
        self._write_code(lines)

        print(f'{self.fname} recommented.')