#!/usr/bin/env python

from pysam import VariantFile
import seaborn as sns
import argparse
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description="View histogram of qual scores")
parser.add_argument("-i", "--input", help="Input VCF file", required=True)
parser.add_argument("-o", "--output", help="Output histogram", required=True)
parser.add_argument("--version", action="version", version="v0.1")
args = parser.parse_args()

vcf = VariantFile(args.input)

# Get qualities
quals = list()
nbr_missing = 0
for rec in vcf:
    if rec.qual is not None:
        # max_qual_in_data = rec.qual
        quals.append(rec.qual)
    else:
        nbr_missing += 1


print(f"Number of quals: {len(quals)}, number of missing: {nbr_missing}")
sns.histplot(quals).set(title=f"Number missing: {nbr_missing}")
plt.savefig(args.output, bbox_inches="tight")
plt.close()

# vcf_out = VariantFile(args.output, "w", header=vcf.header)
# # Update qualities
# for rec in vcf:
#     if rec.qual is not None:
#         rec.qual = rec.qual / max_qual_in_data * args.max
#     vcf_out.write(rec)
