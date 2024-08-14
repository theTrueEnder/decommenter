# decommenter
Automatically decomment code, for use cases including minimization, removal of PII, and cleanup.

Additionally, `decommenter` supports recommenting the decommented code by exporting the extracted comments to a separate file. Using the `recomment` mode, those comments can be reinserted.

## Usage

**Requires Python 3.10+ to be installed**
> 3.10+ specifically due to match-case statements being used in the code

```c
python cli.py [-h] [--mode {decomment,recomment}] [--file [FILE]]

options:
  -h, --help            show this help message and exit
  -m, --mode {decomment,recomment}
                        select mode of operation (decomment or recomment)
  f, --file [FILENAME]
                        filename or path to the target file
```

#### Supported Languages:

- [X] Python
- [ ] JS
- [ ] Java
- [ ] C
- [ ] C++
- [ ] Go
- [ ] Custom
- ...


### Python

This program assumes that comments adhere to the [PEP8](https://peps.python.org/pep-0008/#comments) standard for Python comments. This means that comments should follow the `# .*` pattern. Technically, inline comments should have two spaces between the `#` and the end of the code, but the `decommenter` regex does adjust for inlines that do not follow this (the recommenter follows the two-space pattern). 

Docstring removal is not implemented at this time. Block comments using `'''` or `"""` is not in adherence to PEP8 (see above) and will not be removed.
