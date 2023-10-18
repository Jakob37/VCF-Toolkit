#!/usr/bin/env python

from pysam import VariantFile, tabix_index
import argparse
import gzip
import subprocess


def main():
    args = parse_arguments()
    update_qualities(args.input, args.output, args.max)
    tabix_index(args.output, preset="vcf", force=True)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Takes variant scores and recalculates them to the scale 0-100"
    )
    parser.add_argument("-i", "--input", help="Input VCF file", required=True)
    parser.add_argument("-o", "--output", help="Output VCF file", required=True)
    parser.add_argument("--max", help="Max resulting quality", default=100, type=float)
    parser.add_argument("--version", action="version", version="v0.1")
    args = parser.parse_args()
    return args


def update_qualities(in_fp: str, out_fp: str, qual_max: int):
    vcf = VariantFile(in_fp)

    # Highest quality
    max_qual_in_data = 0
    for rec in vcf:
        if rec.qual is not None and rec.qual > max_qual_in_data:
            max_qual_in_data = rec.qual

    vcf_out = VariantFile(out_fp, "w", header=vcf.header)
    # Update qualities
    vcf = VariantFile(in_fp)
    for rec in vcf:
        if rec.qual is not None:
            rec.qual = rec.qual / max_qual_in_data * qual_max
        vcf_out.write(rec)


if __name__ == "__main__":
    main()
