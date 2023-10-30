#!/usr/bin/env python

import argparse

parser = argparse.ArgumentParser(description="View histogram of qual scores")
parser.add_argument("-i", "--input", help="Input VCF file", required=True)
parser.add_argument("-o", "--output", help="Output histogram", required=True)
parser.add_argument("--version", action="version", version="v0.1")
args = parser.parse_args()