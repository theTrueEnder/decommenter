import re
import json


class Decommenter():
    def __init__(self, fname, mode):
        self.fname = fname
        self.symbol = None
        self.block_symbol = None
        match(mode):
            case 'python':
                self.symbol = '#'
                self.block_symbol = None
            
            case 'cstyle':
                self.symbol = '//'
                self.block_symbol = ('/*', '*/')
                
            case _:
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
    
    # # decomment code
    # def decomment(self):
    #     # get original file
    #     lines = self._get_code()
        
    #     dc_code, comments = [], []
    #     for linenum, line in enumerate(lines, start=1):
    #         # match comment that starts with a given symbol followed by exactly one space
    #         # and the symbol is not preceded by a backslash
    #         res = re.search(r'(?<!\\)' + self.symbol + r'\s(.*)', line)
            
    #         start_sym, end_sym = self.block_symbol
    #         # TODO: handle block comments
            
    #         if res is not None:
    #             # determine if it's an inline comment (if there's code before the comment)
    #             inline = bool(line[:res.start()].strip())
    #             comments.append({
    #                 "inline":  inline,
    #                 "linenum": linenum,
    #                 "comment": res.group(1).strip()
    #             })
    #             if not inline:
    #                 continue
            
    #         # remove comment from the code while retaining escaped cymbols
    #         code_line = re.sub(r'(?<!\\)' + self.symbol + r'\s.*', '', line)
    #         dc_code.append(code_line.rstrip() + '\n')  # Remove trailing whitespace only                 

    #     self._write_code(dc_code)
    #     self._write_comments(comments)
            
    #     print(f'{self.fname} decommented.')

    def decomment(self):
        # get original file
        lines = self._get_code()
        
        dc_code, comments = [], []
        block_comment = False
        block_comment_lines = []
        
        start_sym, end_sym = self.block_symbol
        
        for linenum, line in enumerate(lines, start=1):
            # Handle block comment start
            res = re.search(r'(?<!\\)' + re.escape(start_sym) + r'(.*)', line)
            
            
            # if not already in block comment and start symbol found
            if not block_comment and res:
                block_comment = True
                s = res.group(1)
                # this logic might leak certain situations involving a one-line block comment
                # probably should convert to regex logic
                # end_sym_idx = s.index(end_sym, res.pos) if end_sym in s else None
                
                end_sym_idx = re.search(r'(.*)(?<!\\)' + re.escape(end_sym), s).span()[0]
                
                # if end symbol found on same line (one-line block comment), extract 
                # the block comment from the line and treat it as an inline comment
                if end_sym_idx:
                    block_comment = False
                    comments.append({
                        "inline":  True,
                        "linenum": linenum,
                        "comment": s[:end_sym_idx]
                    })
                    code_line = line[:res.span()[0]] + line[end_sym_idx + len(end_sym_idx):] # TODO: make regex?
                    dc_code.append(code_line.rstrip() + '\n')  # Remove trailing whitespace only
                    continue
                                
                
            # if in block comment and end symbol found (not on same line as start symbol)
            if block_comment and res:
                block_comment = False
                comments.append({
                        "inline":  True,
                        "linenum": linenum,
                        "comment": res.group(1)
                    })
                
                # get whitespace of current line to indent the code and push code
                ws = re.match(r"\s*", line).group(1)
                code_line = re.sub(r'(.*)' + re.escape(end_sym), '', line)
                dc_code.append(ws + code_line.rstrip() + '\n')  # Remove trailing whitespace only
                    
            
            # if in block comment and no end symbol found
            elif block_comment:
                block_comment_lines.append({
                    "inline":  False,
                    "linenum": linenum,
                    "comment": line.strip()
                })
                
            # if not in block comment and no start symbol found
            else:
                # match inline comment that starts with a given symbol followed by exactly one space
                # and the symbol is not preceded by a backslash
                res = re.search(r'(?<!\\)' + re.escape(self.symbol) + r'\s(.*)', line)
                
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
                
                # remove comment from the code while retaining escaped symbols
                code_line = re.sub(r'(?<!\\)' + re.escape(self.symbol) + r'\s.*', '', line)
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
                ws = re.match(r"\s*", lines[linenum-1]).group(1)
                lines.insert(linenum - 1, f'{ws}# {comment}\n')
        
        # write changes over original code
        self._write_code(lines)

        print(f'{self.fname} recommented.')