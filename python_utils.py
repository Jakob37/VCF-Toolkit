from typing import Callable
from pysam import VariantFile, VariantRecord


def print_rankscore(vcf: str, comp_val: int, comp_type: str | None, print_full: bool):
    assert (
        comp_type == "equal"
        or comp_type == "greater"
        or comp_type == "less"
        or comp_type is None
    )

    print(comp_val)
    print(comp_type)

    fh = VariantFile(vcf)
    for record in fh:
        rank_score_field = record.info.get("RankScore")
        rank_score = float(rank_score_field[0].split(":")[1])

        if comp_type == "equal" and rank_score == comp_val:
            if print_full:
                print(record, end="")
            else:
                print(rank_score)
        elif comp_type == "greater" and rank_score > comp_val:
            if print_full:
                print(record, end="")
            else:
                print(rank_score)
        elif comp_type == "less" and rank_score < comp_val:
            if print_full:
                print(record, end="")
            else:
                print(rank_score)
        elif comp_type is None:
            if print_full:
                print(record, end="")
            else:
                print(rank_score)


def filter_info(
    vcf: str,
    info_field: str,
    comp_val: str,
    type: str,
    preparser_fn: Callable[[str], str],
    debug: bool,
):
    assert type == "equal" or type == "greater" or type == "less"

    first_record = True
    fh = VariantFile(vcf)
    nbr_missing = 0
    for record in fh:
        info_val = record.info.get(info_field)
        if debug and first_record:
            print(info_val)
        if info_val is None:
            nbr_missing += 1
        else:
            info_val = preparser_fn(info_val[0])

            if type == "equal":
                if info_val == comp_val:
                    if not debug:
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
                        if not debug:
                            print(record, end="")
                    elif type == "less" and info_val_float <= comp_val_float:
                        if not debug:
                            print(record, end="")
        if first_record:
            first_record = False

    if debug:
        print(f"Number missing: {nbr_missing}")


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
