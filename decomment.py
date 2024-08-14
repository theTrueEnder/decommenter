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

    def decomment(self):
        # get original file
        lines = self._get_code()
        
        dc_code, comments = [], []
        block_comment = False
        
        start_sym, end_sym = self.block_symbol
        
        for linenum, line in enumerate(lines, start=1):
            # Handle block comment start
            res = re.search(r'(?<!\\)' + re.escape(start_sym) + r'(.*)', line)
            
            
            # NOT BLOCK comment and START symbol found
            if not block_comment and res:
                print('Start symbol found;\n\tLine: ', line)
                block_comment = True
                s = res.group(1)
                # this logic might leak certain situations involving a one-line block comment
                # probably should convert to regex logic
                # end_sym_idx = s.index(end_sym, res.pos) if end_sym in s else None
                
                end_sym_idx = re.search(r'(.*)(?<!\\)' + re.escape(end_sym), s).span()[0] if re.search(r'(.*)(?<!\\)' + re.escape(end_sym), s) else None
                print('\tEnd idx:', end_sym_idx)
                # if end symbol found on same line (one-line block comment), extract 
                # the block comment from the line and treat it as an inline comment
                if end_sym_idx:
                    print('End symbol found on same line')
                    block_comment = False
                    comments.append({
                        "inline":  True,
                        "linenum": linenum,
                        "comment": start_sym + s[:end_sym_idx]
                    })
                    code_line = line[:res.span()[0]] + line[end_sym_idx + len(end_sym_idx):] # TODO: make regex?
                    dc_code.append(code_line.rstrip() + '\n')  # Remove trailing whitespace only
                
                # IN BLOCK comment and START symbol found
                else:
                    print('\tNo end symbol found on same line\n')
                    comments.append({
                            "inline":  True,
                            "linenum": linenum,
                            "comment": start_sym + res.group(1)
                        })
                
                    # get whitespace of current line to indent the code and push code
                    ws = re.match(r"\s*", line).group()
                    code_line = re.sub(r'(?<!\\)' + re.escape(start_sym) + r'(.*)$', '', line)
                    print('\tCode:', code_line)
                    dc_code.append(ws + code_line.rstrip() + '\n')
                    # Remove trailing whitespace only        
                    
                continue    
            
            # IN BLOCK comment and END symbol found (not on same line as start symbol)
            res = re.search(r'(.*)(?<!\\)' + re.escape(end_sym), line)
            if block_comment and res:
                s = res.group(1)
                print('End symbol found:\n\tLine:', line)
                print('\tComment:', s[:end_sym_idx] + ' ' + end_sym)
                block_comment = False
                comments.append({
                    "inline":  True,
                    "linenum": linenum,
                    "comment": s[:end_sym_idx] + ' ' + end_sym
                })
                # assumes that there is no code on the same line as the end symbol
                # code_line = line[:res.span()[0]] + line[end_sym_idx + len(end_sym_idx):]
                # dc_code.append(code_line.rstrip() + '\n')  # Remove trailing whitespace only
                    
            
            # IN BLOCK comment and NO END symbol found
            elif block_comment:
                print('In block comment:\n\tLine:', line)
                comments.append({
                    "inline":  False,
                    "linenum": linenum,
                    "comment": line.strip()
                })
                
                
            # NOT BLOCK comment and NO START symbol found
            else:
                print('Normal line:\n\tLine:', line)
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