#!/usr/bin/env python3

from pysam import VariantFile
import argparse

def main():
    args = parse_arguments()

    vcf = VariantFile(args.input)

    curr_rec = 1
    target_rec = next(vcf)
    while curr_rec != args.target_rec:
        target_rec = next(vcf)
        curr_rec += 1

    print("---- INFO -----")
    # first_rec = next(vcf)
    for label, vals in target_rec.info.items():

        if label == "CSQ":
            continue

        if isinstance(vals, tuple):
            str_vals = [str(val) for val in vals]
        else:
            str_vals = str(vals)
        print(f"{label:{args.padding}}\t{','.join(str_vals)}")
    
    csq_description: str = target_rec.header.info['CSQ'].description # type: ignore
    labels = csq_description.split("Format: ")[1].split("|")
    values = target_rec.info['CSQ'][0].split("|")
    assert len(labels) == len(values)

    print("----- CSQ  -----")
    for i in range(0, len(labels)):
        label = labels[i]
        value = values[i]
        print(f"{label:{args.padding}}\t{value}")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Extract first annotation line and pretty-display it"
    )
    parser.add_argument("-i", "--input", help="Input VCF file", required=True)
    parser.add_argument("--padding", default=20, type=int, help="Put space between columns")
    parser.add_argument("--target_rec", default=1, help="The n of the record to show annotations for")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
