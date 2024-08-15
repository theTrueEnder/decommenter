import re
import json

COMMENT_TYPES = {
    BLOCK := 'BLOCK',
    LINE := 'LINE',
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

    def decomment(self) -> dict:
        # get original file
        code = self._get_code()
        code_len = len(code)
        
        comments = []
        start_sym, end_sym = self.block_symbol

        # define regex patterns for line and block quotes
        r_line = re.compile(r'(?<!["\'])\s*(?<!\\)' + re.escape(self.symbol) + r'(.*)$', re.MULTILINE)
        r_block = re.compile(r'\s*' + re.escape(start_sym) + r'.*?' + re.escape(end_sym), re.MULTILINE | re.DOTALL)
                
        # get an iterator for all matches of the pattern (line/block comments)
        # then erase them from the code
        line_cmts = re.finditer(r_line, code)
        dc_code = re.sub(r_line, '', code, 0)
        
        block_cmts = re.finditer(r_block, dc_code)
        dc_code = re.sub(r_block, '', dc_code, 0)
        
        stats = {
            "orig_len": code_len,
            LINE: {
                "count": 0,
                "total_len": 0
            },
            BLOCK: {
                "count": 0,
                "total_len": 0
            }
        }
        
        # add line comments to list
        for match in line_cmts:
            comments.append({
                "span":  match.span(),
                "type":  LINE,
                "comment": match.group() # .strip()
            })
            stats[LINE]['count'] += 1
            stats[LINE]['total_len'] += len(match.group())
        
        # add block comments to list
        for match in block_cmts:
            print('Match:\n\t', match)
            comments.append({
                "span":  match.span(),
                "type":  BLOCK,
                "comment": match.group() # .strip()
            })
            stats[BLOCK]['count'] += 1
            stats[BLOCK]['total_len'] += len(match.group())
            
        # write results to files and exit
        self._write_code(dc_code)
        self._write_comments(comments)
        print(f'{self.fname} decommented.')
        return stats
        
        
        
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