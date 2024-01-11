from typing import Callable
from pysam import VariantFile, VariantRecord


def filter_info(
    vcf: str,
    info_field: str,
    comp_val: str,
    type: str,
    preparser_fn: Callable[[str], str],
):
    assert type == "equal" or type == "greater" or type == "less"

    fh = VariantFile(vcf)
    nbr_missing = 0
    for record in fh:
        info_val = record.info.get(info_field)
        if info_val is None:
            nbr_missing += 1
        else:
            info_val = preparser_fn(info_val[0])

            if type == "equal":
                if info_val == comp_val:
                    print(record, end="")
            elif type == "greater" or type == "less":
                valid_float = True
                try:
                    float(info_val)
                except ValueError:
                    valid_float = False

                if valid_float:
                    info_val_float = float(info_val)
                    comp_val_float = float(comp_val)

                    if type == "greater" and info_val_float >= comp_val_float:
                        print(record, end="")
                    elif type == "less" and info_val_float <= comp_val_float:
                        print(record, end="")


def snv_diff(vcf1: str, vcf2: str, print_recs: bool):
    vcf1_recs = make_recs_dict(vcf1)
    vcf2_recs = make_recs_dict(vcf2)

    vcf1_keys = set(vcf1_recs.keys())
    vcf2_keys = set(vcf2_recs.keys())

    vcf1_only = vcf1_keys.difference(vcf2_keys)
    vcf2_only = vcf2_keys.difference(vcf1_keys)

    if not print_recs:
        print(f"{len(vcf1_only)} only in VCF1, {len(vcf2_only)} only in VCF2")
    else:
        for key in vcf1_only:
            rec = vcf1_recs[key]
            print(f"vcf1\t{rec}")
        for key in vcf2_only:
            rec = vcf2_recs[key]
            print(f"vcf2\t{rec}")


def make_recs_dict(vcf_path: str) -> dict[str, VariantRecord]:
    fh = VariantFile(vcf_path)
    variant_recs = dict()
    for record in fh:
        key = f"{record.chrom}:{record.pos}:{'/'.join(record.alts)}"
        variant_recs[key] = record
    return variant_recs
