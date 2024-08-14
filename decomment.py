import re
import json

COMMENT_TYPES = {
    BLOCK := 'BLOCK',
    INLINE := 'INLINE',
    DOC := 'DOC',
}
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
            self.docsymbol = '///'
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
        
        comments = []
        # block_comment = False
        
        start_sym = self.block_symbol[0]
        end_sym = self.block_symbol[1]
        sym = re.escape(self.symbol)
        # print('Sym:', sym)
        
        rx = r'(?<!["\'])\s*(?<!\\)' + sym + r'(.*)$'

        r_block = re.compile(r'\s*' + re.escape(start_sym) + r'.*?' + re.escape(end_sym), re.MULTILINE | re.DOTALL)
        # r_newline = re.compile(r'$(\s)*' + sym + r'(.*)$')
        r_inline = re.compile(rx, re.MULTILINE)
                
        
        inline_cmts = re.finditer(r_inline, code) # not getting everything it should
        dc_code = re.sub(r_inline, '', code, 0)
        
        block_cmts = re.finditer(r_block, dc_code)
        dc_code = re.sub(r_block, '', dc_code, 0)
        
        # newline_cmts = re.findall(r_newline, code)
        # re.sub(r_newline, '', code, 0)
        
        
        # print(dc_code)
        ###
        # just use inlines and blocks and then use the spans to replace it instead of linenums
        # this would mean managing whitespace and newlines correctly but dang
        ###
        
        for match in block_cmts:
            # add to comments with span
            print('Match:\n\t', match)
            comments.append({
                "span":  match.span(),
                "type":  BLOCK,
                "comment": match.group() # .strip()
            })
            
        for match in inline_cmts:
            # add to comments with span
            # print('Match:\n\t', match)
            comments.append({
                "span":  match.span(),
                "type":  INLINE,
                "comment": match.group() # .strip()
            })
            
        
        
        
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