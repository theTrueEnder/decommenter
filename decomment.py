import re
import json

COMMENT_TYPES = {
    BLOCK := 'BLOCK',
    INLINE := 'INLINE',
    NEWLINE := 'NEWLINE',
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

        # define regex patterns for inline, newline, and block quotes
        # r_inline = re.compile( r'(?<=\w)(?<!["\'])[ \t]*(?<!\\)' + re.escape(self.symbol) + r'(.*)?(\Z)?', re.MULTILINE | re.DOTALL)
        r_inline = re.compile( r'(^.*?(\S))(?<!["\'])[ \t]*(?<!\\)' + re.escape(self.symbol) + r'(.*)?$', re.MULTILINE)
        r_newline = re.compile(r'(?<!["\'])[ \t]*(?<!\\)' + re.escape(self.symbol) + r'.*?\n', re.MULTILINE | re.DOTALL)
        r_block = re.compile(  r'(?<!["\'])[ \t]*' + re.escape(start_sym) + r'.*?' + re.escape(end_sym) + r'\n?', re.MULTILINE | re.DOTALL)
                
        # get an iterator for all matches of the pattern (line/block comments)
        # then erase them from the code
        
        inline_cmts = re.finditer(r_inline, code)
        code = re.sub(r_inline, '', code, 0) # TODO: it's subbing the whole inline match for '', but it should only be doing it for the code part of the match
        
        newline_cmts = re.finditer(r_newline, code)
        code = re.sub(r_newline, '', code, 0)
        
        block_cmts = re.finditer(r_block, code)
        code = re.sub(r_block, '', code, 0)
        
        stats = {
            "orig_len": code_len,
        }
        [stats.update({t: {"count": 0, "total_len": 0}}) for t in COMMENT_TYPES]
        
        cmt_and_type = [(NEWLINE, cmt.group(), cmt.span()) for cmt in newline_cmts] + \
                       [(BLOCK,   cmt.group(), cmt.span()) for cmt in block_cmts]
        # cmt_and_type = []
        for cmt in inline_cmts:
            inline_code, _, inline_cmt = cmt.groups()
            inline_cmt = self.symbol + inline_cmt
            # print(cmt.groups())
            cmt_and_type.append((INLINE, inline_cmt, [cmt.span()[0] + len(inline_code), cmt.span()[1]]))
        # + \
                    #    [(NEWLINE, cmt) for cmt in newline_cmts] + \
                    #    [(BLOCK, cmt) for cmt in block_cmts]
                       
        for cmt_type, cmt, span in cmt_and_type:
            comments.append({
                "type":  cmt_type,
                "comment": cmt,
                "span":  span
            })
            stats[cmt_type]['count'] += 1
            stats[cmt_type]['total_len'] += len(cmt)
            
        # write results to files and exit
        self._write_code(code)
        self._write_comments(comments)
        print(f'{self.fname} decommented.')
        return stats
        
        
        
    # recomment python code
    def recomment(self):
        # load comments file
        raw_comments = self._get_comments()
        raw_block_comments = [[cmt['span'][0], cmt['type'], cmt['comment']] for cmt in raw_comments if cmt['type'] == BLOCK]
        raw_newline_comments = [[cmt['span'][0], cmt['type'], cmt['comment']] for cmt in raw_comments if cmt['type'] == NEWLINE]
        raw_inline_comments = [[cmt['span'][0], cmt['type'], cmt['comment']] for cmt in raw_comments if cmt['type'] == INLINE]
        
        comments = sorted(raw_block_comments,   key=lambda x: x[0], reverse=True) + \
                   sorted(raw_newline_comments, key=lambda x: x[0], reverse=True) + \
                   sorted(raw_inline_comments,  key=lambda x: x[0], reverse=True)
        
        # load decommented code file
        code = self._get_code()
        [print(c) for c in comments]
        for left, cmt_type, comment in comments:
            # insert comment string into code using span info
            code = code[:left] + comment + code[left:]
            # print('Pre:\n\t', code[:span[0]])
            # print('Comment:\n\t', comment)
            # print('Post:\n\t', code[span[1]:])
        
        # write changes over original code
        self._write_code(code)

        print(f'{self.fname} recommented.')