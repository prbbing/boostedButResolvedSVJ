from ROOT import *
from RootPlottingCore import *
import optparse
import os
import re

parser = optparse.OptionParser()
parser.add_option('-l','--localConfig',   dest='localConfig', help='Specify a local config file to use.', default='')
parser.add_option('-b','--batchMode',   dest='batchMode', help='Run in batch mode.', action="store_true", default=False)
(arguments, args) = parser.parse_args()

if arguments.batchMode:
  gROOT.SetBatch(True) 

if arguments.localConfig:
  sys.path.append(os.getcwd())
  sys.path.append(os.path.dirname(arguments.localConfig))
  exec("from " + re.sub (r".py$", r"", os.path.basename(arguments.localConfig)) + " import *")
else:
  print("Local configuration file not given. Aborting!")
  sys.exit(0)

outputFile = TFile(outputPath, "RECREATE","")

outputFile.cd()
drawComparisonPlot(taskSetup, compareSources, outputFile)

outputFile.Close()
