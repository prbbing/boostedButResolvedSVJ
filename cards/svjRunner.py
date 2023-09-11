import os, math, sys, shutil
from string import Template
from glob import glob
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from svjHelper import svjHelper

if __name__=="__main__":
    helper = svjHelper()

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("--mMediator", required=True, type=float, help="mediator mass (GeV)")
    parser.add_argument("--mDark", required=True, type=float, help="dark hadron mass (GeV)")
    parser.add_argument("--rinv", required=True, type=float, help="invisible fraction")
    parser.add_argument("--boost", default=0.0, type=float, help="boost cut")
    parser.add_argument("--boostvar", default=None, type=str, choices=helper.allowed_boostvars, help="boost variable")
    args = parser.parse_args()

    helper.setModel("s", args.mMediator, args.mDark, args.rinv, "peak", generate=False, boost=args.boost, boostvar=args.boostvar)
    oname = helper.getOutName(outpre="SVJ")

    mg_name = "DMsimp_SVJ_s_spin1"
    lhaid = 325300
    nevents = 10000
    data_path = os.path.expandvars("$PWD/"+mg_name)
    mg_dir = os.path.join(os.getcwd(),oname)
    # remove output directory if it already exists
    if os.path.isdir(mg_dir):
        shutil.rmtree(mg_dir)
    shutil.copytree(data_path,mg_dir)
    mg_model_dir, mg_input_dir = helper.getMadGraphCards(mg_dir,lhaid,events=nevents)
    print("MadGraph settings: {}, {}".format(mg_model_dir,mg_input_dir))

    pythia_lines = helper.getPythiaSettings()
    matching_lines = helper.getJetMatchSettings()

    fname = "pythia_{}.txt".format(oname)
    with open(fname,'w') as file:
        file.write('\n'.join(pythia_lines)+'\n')
        file.write('\n'.join(matching_lines))
    print("Pythia settings: {}".format(fname))
