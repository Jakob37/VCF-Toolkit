#!/usr/bin/env python

import argparse
from pysam import VariantFile, VariantHeader, tabix_index


def main():
    args = parse_arguments()
    add_prefix(args.input, args.output, args.pattern)
    tabix_index(args.output, present="vcf", force=True)


def add_prefix(in_fp, out_fp, prefix):
    new_header = VariantHeader()
    vcf_in = VariantFile(in_fp)

    # Inspired by: https://github.com/pysam-developers/pysam/issues/1170
    for header_rec in vcf_in.header.records:
        if header_rec.type == "CONTIG":
            existing_id = header_rec["ID"]
            new_header.contigs.add(
                f"{prefix}{existing_id}", length=header_rec["length"]
            )
        else:
            new_header.add_record(header_rec)

    for sample in vcf_in.header.samples:
        new_header.add_sample(sample)

    vcf_out = VariantFile(out_fp, "w", header=new_header)

    for rec in vcf_in.fetch():
        new_rec = vcf_out.new_record()
        new_rec.contig = f"{prefix}{rec.chrom}"
        new_rec.alleles = rec.alleles
        vcf_out.write(new_rec)

    vcf_in.close()
    vcf_out.close()


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
