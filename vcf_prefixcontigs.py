#!/usr/bin/env python3

import argparse
from pysam import tabix_index
import gzip
import subprocess
import re


def main():
    args = parse_arguments()

    out_fp_w_gz = args.output
    if out_fp_w_gz.split(".")[-1] != "gz":
        raise ValueError(f"Out file is expected to end with .gz, found: {out_fp_w_gz}")

    out_fp_wo_gz = ".".join(out_fp_w_gz.split(".")[0:-1])

    add_prefix(args.input, out_fp_wo_gz, args.prefix)
    subprocess.run(["bgzip", out_fp_wo_gz])
    tabix_index(out_fp_w_gz, preset="vcf", force=True)


def add_prefix(in_fp, out_fp, prefix):
    with gzip.open(in_fp, "rt") as in_fh, open(out_fp, "w") as out_fh:
        for line in in_fh:
            line = line.rstrip()
            if line.startswith("##contig"):
                contig_line = re.sub("ID=", f"ID={prefix}", line)
                print(contig_line, file=out_fh)
            elif line.startswith("#"):
                print(line, file=out_fh)
            else:
                rec_line = re.sub("^", f"{prefix}", line)
                print(rec_line, file=out_fh)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Add prefix to contigs in both header and records"
    )
    parser.add_argument("-i", "--input", help="Input VCF file", required=True)
    parser.add_argument("-o", "--output", help="Output VCF file", required=True)
    parser.add_argument(
        "-p", "--prefix", help="Prefix to add to each chromosome", default="chr"
    )
    parser.add_argument("--version", action="version", version="v0.1")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
