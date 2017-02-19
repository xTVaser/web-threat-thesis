import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

parser = argparse.ArgumentParser()

parser.add_argument("-s", "--sqlNumber",
                    help="The number of SQL attacks to include in training")
parser.add_argument("-x", "--xssPercentage",
                    help="The number of XSS attacks to include in training")
parser.add_argument("-r", "--rfiPercentage",
                    help="The number of RFI attacks to include in training")
parser.add_argument("-n", "--nonthreatPercentage",
                    help="THe number of nonthreat attacks to include in training")

parser.add_argument("t", "--type",
                    help="What attack type we are trying to identify")

parser.add_argument("-op", "--optimize", action="store_true",
                    help="Whether or not the svm should optimize gamma and C values using a GridSearch")

parser.add_argument("-f", "--fileDirectory",
                    help="Directory containing the 4 threat files")
parser.add_argument("-o", "--output",
                    help="Output file name")

args = parser.parse_args()

