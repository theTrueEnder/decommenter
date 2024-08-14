# decommenter
Automatically decomment code, for use cases including minimization, removal of PII, and cleanup.

Additionally, `decommenter` supports recommenting the decommented code by exporting the extracted comments to a separate file. Using the `recomment` mode, those comments can be reinserted.

## Usage

**Requires Python 3.8+ to be installed** 

> It is possible older versions work, but I cannot guarantee functionality. `decommenter` was developed in 3.12.
```c
python cli.py [-h] [--mode {decomment,recomment}] [--file [FILE]]

options:
  -h, --help            show this help message and exit
  -m, --mode {decomment,recomment}
                        select mode of operation (decomment or recomment)
  f, --file [FILENAME]
                        filename or path to the target file
```

## Supported Languages:

- [X] Python-style comments*
- [X] C-style comments: UNSTABLE (see below)

<!-- - [X] Python
- [ ] JS
- [ ] Java
- [ ] C
- [ ] C++
- [ ] Go
- [ ] Custom
- ...
-->

### Python-Style Comments

This program assumes that comments adhere to the [PEP8](https://peps.python.org/pep-0008/#comments) standard for Python comments. This means that comments should follow the `# .*` pattern. Technically, inline comments should have two spaces between the `#` and the end of the code, but the `decommenter` regex does adjust for inlines that do not follow this (the recommenter follows the two-space pattern). 

Docstring removal is not implemented at this time. Block comments using `'''` or `"""` is not in adherence to PEP8 (see above) and will not be removed.

> *Python-style comments in other languages (e.g. Ruby, Perl, and R) are allowed to run but have not been tested and are therefore not guaranteed to work.

### C-Style Comments

Inline and newline C-style comments (i.e. non-block comments) work fine with the code on `dev`. There is a tenative processor for block comments, but it is unstable and inconsistent. A fix will arrive in the near future (this requires restructuring the entire processor from a line-by-line regex logic to multiline regex logic). If you want to try it out, clone the code on the `dev` branch.
