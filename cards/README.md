# SVJ cards for generation

## Environment

Some of the Python code is Python2-only, so an older LCG environment is used:
```bash
source init.sh
```

## Running

Example command:
```bash
python svjRunner.py --mMediator 500 --mDark 20 --rinv 0.3
```

This produces:
1. MadGraph output directory `SVJ_s-channel_mMed-500_mDark-20_rinv-0.3_alpha-peak_13TeV-madgraphMLM-pythia8`
2. Pythia output card `pythia_SVJ_s-channel_mMed-500_mDark-20_rinv-0.3_alpha-peak_13TeV-madgraphMLM-pythia8.txt`
