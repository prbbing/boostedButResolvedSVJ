# Boosted but resolved analysis

## Environment

A recent version of LCG is used:
```bash
source init.sh
```
## Options

`delphiAnalysis.py`:
```
usage: delphiAnalysis.py [-h] -i INPUT -o OUTPUT [-n NEVENTS]

optional arguments:
  -h, --help                     show this help message and exit
  -i INPUT, --input INPUT        input filename (default: None)
  -o OUTPUT, --output OUTPUT     output filename (default: None)
  -n NEVENTS, --nevents NEVENTS  restrict number of events (for testing) (default: -1)
```

`plot.py`:
```
usage: plot.py [-h] [-i INPUTS [INPUTS ...]] [-x SUFFIX] [-d DIR] [-n] [-q [QTYS ...]] [-Q QNAME]

optional arguments:
  -h, --help                                            show this help message and exit
  -i INPUTS [INPUTS ...], --inputs INPUTS [INPUTS ...]  input file(s) (default: None)
  -x SUFFIX, --suffix SUFFIX                            suffix for output plot filenames (default: )
  -d DIR, --dir DIR                                     directory for output plots (default: .)
  -n, --norm                                            draw normalized plots (default: False)
  -q [QTYS ...], --qtys [QTYS ...]                      quantity(s) to overlay (multiple qtys: one input file) (default: [])
  -Q QNAME, --qname QNAME                               axis name for overlaid quantities (default: None)
```
