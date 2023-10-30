#!/usr/bin/env python3

# from pysam import VariantFile
import argparse

def main():
    args = parse_arguments()

    # vcf = VariantFile(args.input)

    csq_labels = None
    target_rec = None

    curr_rec = 1
    with open(args.input) as in_fh:
        for line in in_fh:
            line = line.rstrip()

            if line.startswith("##INFO=<ID=CSQ"):
                csq_labels = line.split("Format: ")[1].rstrip("\">").split("|")
            elif not line.startswith("#"):
                if curr_rec == args.target_rec:
                    target_rec = line
                    break
                curr_rec += 1

    # curr_rec = 1
    # target_rec = next(vcf)
    # while curr_rec != args.target_rec:
    #     target_rec = next(vcf)
    #     curr_rec += 1

    assert target_rec is not None
    assert csq_labels is not None

    info_field = target_rec.split("\t")[7]
    info_content = info_field.split(";")

    csq_values = None

    print("---- INFO -----")
    # first_rec = next(vcf)
    for info_field in info_content:
    # for label, vals in target_rec.info.items():

        (label, value) = info_field.split("=")

        if label == "CSQ":
            csq_values = value.split("|")
            continue

        # if isinstance(vals, tuple):
        #     str_vals = [str(val) for val in vals]
        # else:
        #     str_vals = str(vals)
        print(f"{label:{args.padding}}\t{','.join(value)}")
    
    # csq_description = target_rec.header.info['CSQ'].description # type: ignore
    # csq_description: str = target_rec.header.info['CSQ'].description # type: ignore
    # labels = csq_description.split("Format: ")[1].split("|")
    # values = target_rec.info['CSQ'][0].split("|")
    assert csq_values is not None
    assert len(csq_labels) == len(csq_values)

    print("----- CSQ  -----")
    for i in range(0, len(csq_labels)):
        label = csq_labels[i]
        value = csq_values[i]
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
