import re
import json

# decomment python code
def dc_python(fname):
    # get original file
    with open(fname, mode='r') as f:
        lines = f.readlines()
    
    code, comments = [], []
    for linenum, line in enumerate(lines, start=1):
        # match a PEP8 comment that starts with a # followed by exactly one space and not preceded by a backslash
        res = re.search(r'(?<!\\)#\s(.*)', line)
        
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
        
        # remove comment from the code while retaining escaped #'s
        code_line = re.sub(r'(?<!\\)#\s.*', '', line)
        code.append(code_line.rstrip() + '\n')  # Remove trailing whitespace only                 

    with open(fname, mode='w') as f:
        f.writelines(code)
        
    with open(fname+'.dc.json', mode='w') as f:
        json.dump(comments, f)
        
    print(f'{fname} decommented.')


# recomment python code
def rc_python(fname):
    # load comments file
    with open(fname + '.dc.json', mode='r') as f:
        comments = json.load(f)
    
    # load decommented code file
    with open(fname, mode='r') as f:
        lines = f.readlines()
        
    for comment in comments:
        inline, linenum, comment = tuple(comment.values())
        
        # if inline, append to code line
        # otherwise, insert new line with comment (matches indentation of following line) 
        if inline:
            lines[linenum-1] = lines[linenum-1][:-1] + '  # ' + comment + '\n'
        else:
            ws = re.match(r"\s*", lines[linenum-1]).group()
            lines.insert(linenum - 1, ws + '# ' + comment + '\n')
    
    # write changes over original code
    with open(fname, mode='w') as f:
        f.writelines(lines)

    print(f'{fname} recommented.')
    
# https://peps.python.org/pep-0008/#block-comments





