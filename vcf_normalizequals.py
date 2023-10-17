#!/usr/bin/env python

from pysam import VariantFile
import argparse

parser = argparse.ArgumentParser(
    description="Takes variant scores and recalculates them to the scale 0-100"
)
parser.add_argument("-i", "--input", help="Input VCF file", required=True)
parser.add_argument("-o", "--output", help="Output VCF file", required=True)
parser.add_argument("--max", help="Max resulting quality", default=100, type=float)
parser.add_argument("--version", action="version", version="v0.1")
args = parser.parse_args()

vcf = VariantFile(args.input)

# Highest quality
max_qual_in_data = 0
for rec in vcf:
    if rec.qual is not None and rec.qual > max_qual_in_data:
        max_qual_in_data = rec.qual

vcf_out = VariantFile(args.output, "w", header=vcf.header)
# Update qualities
vcf = VariantFile(args.input)
for rec in vcf:
    if rec.qual is not None:
        rec.qual = rec.qual / max_qual_in_data * args.max
    vcf_out.write(rec)
