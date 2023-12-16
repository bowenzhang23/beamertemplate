# Beamer template

## Usage

```text
usage: main.py [-h] -m MODULE [-v] [-f] output

positional arguments:
  output                The path to the output tex file.

options:
  -h, --help            show this help message and exit
  -m MODULE, --module MODULE
                        The module that cotains components to import.
  -v, --verbose         Show verbose print-outs.
  -f, --force           Force to update the tex file.
```

Example

```shell
python scripts/main.py output/example.tex -f -v -m test
```
