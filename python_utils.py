from collections import defaultdict
from typing import Callable
from pysam import VariantFile, VariantRecord

from classes.rankmodel import RankModel
from classes.utils import chromosome_sort


def print_rankscore(
    vcf: str,
    comp_val: int,
    comp_type: str | None,
    print_full: bool,
    rank_model_fp: str | None,
    columns_str: str | None,
    head: int,
):
    assert (
        comp_type == "equal"
        or comp_type == "greater"
        or comp_type == "less"
        or comp_type == "lessorequal"
        or comp_type == "greaterorequal"
        or comp_type is None
    )

    columns = None
    if columns_str is not None:
        columns = [int(col) for col in columns_str.split(",")]

    rank_model = None
    if rank_model_fp is not None:
        rank_model = RankModel(rank_model_fp)

    is_first_line = True
    printed_entries = 0

    fh = VariantFile(vcf)
    for record in fh:

        if is_first_line:
            header_fields = str(record.header).rstrip().split("\n")[-1].split("\t")
            if print_full:
                print("\t".join(header_fields))
            elif columns is not None:
                selected_fields = [header_fields[i] for i in columns]
                selected_fields.append("RankScore")

                if rank_model is not None:
                    selected_fields = selected_fields + rank_model.categories

                print("\t".join(selected_fields))
            else:
                if rank_model is not None:
                    header = ["RankScore"] + rank_model.categories
                    print("\t".join(header))
            is_first_line = False

        rank_score_field = record.info.get("RankScore")[0]
        rank_score = float(rank_score_field.split(":")[1])

        rank_subscores = None
        if rank_model is not None:
            rank_subscore_field = record.info.get("RankResult")[0]
            rank_subscores = [int(score) for score in rank_subscore_field.split("|")]

        if comp_type == "equal" and rank_score == comp_val:
            print_helper(record, rank_score, print_full, columns, rank_subscores)
            printed_entries += 1
        elif comp_type == "greater" and rank_score > comp_val:
            print_helper(record, rank_score, print_full, columns, rank_subscores)
            printed_entries += 1
        elif comp_type == "less" and rank_score < comp_val:
            print_helper(record, rank_score, print_full, columns, rank_subscores)
            printed_entries += 1
        elif comp_type == "lessorequal" and rank_score <= comp_val:
            print_helper(record, rank_score, print_full, columns, rank_subscores)
            printed_entries += 1
        elif comp_type == "greaterorequal" and rank_score >= comp_val:
            print_helper(record, rank_score, print_full, columns, rank_subscores)
            printed_entries += 1
        elif comp_type is None:
            print_helper(record, rank_score, print_full, columns, rank_subscores)
            printed_entries += 1

        if printed_entries > head:
            break


def print_helper(
    record: VariantRecord,
    rank_score: float,
    print_full: bool,
    columns: list[int] | None,
    rank_subscores: list[int] | None,
):

    # breakpoint()
    if print_full:
        print(record, end="")
    elif columns is not None:
        rec_fields = str(record).rstrip().split("\t")
        subset = [rec_fields[i] for i in columns]
        subset.append(str(rank_score))

        if rank_subscores is not None:
            subset = subset + [str(score) for score in rank_subscores]

        print("\t".join(subset))
    else:
        if rank_subscores is not None:
            print([rank_score] + [str(score) for score in rank_subscores])
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
    assert (
        type == "equal"
        or type == "greater"
        or type == "less"
        or type == "greaterorequal"
        or type == "lessorequal"
    )

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


def snv_single_diff(
    vcf1_keys: set[str],
    vcf2_keys: set[str],
    vcf1_recs: dict[str, VariantRecord],
    vcf2_recs: dict[str, VariantRecord],
    print_recs: bool,
    simple: bool,
    has_header: bool,
    prefix: str | None
):

    vcf1_only = vcf1_keys.difference(vcf2_keys)
    vcf2_only = vcf2_keys.difference(vcf1_keys)

    if print_recs and simple:
        raise ValueError("Cannot be both simple and in print_recs mode")

    if simple:
        header = ["prefix", "vcf1_nrec", "vcf2_nrec", "vcf1_only", "vcf2_only"]
        values = [str(len(vcf1_keys)),  str(len(vcf2_keys)), str(len(vcf1_only)), str(len(vcf2_only))]
        if prefix:
            header.insert(0, "prefix")
            values.insert(0, prefix)
        
        if has_header:
            print("#" + "\t".join(values))
        print("\t".join(values))

    elif not print_recs:
        string_prefix = ""
        if prefix:
            string_prefix = f"{prefix}: "
        print(f"{string_prefix}{len(vcf1_only)} only in VCF1, {len(vcf2_only)} only in VCF2")
    else:
        for key in vcf1_only:
            rec = vcf1_recs[key]
            print(f"vcf1\t{rec}")
        for key in vcf2_only:
            rec = vcf2_recs[key]
            print(f"vcf2\t{rec}")


def snv_diff(vcf1: str, vcf2: str, print_recs: bool, simple: bool, per_contig: bool, header: bool):
    vcf1_recs = make_recs_dict(vcf1, trim_chr=True)
    vcf2_recs = make_recs_dict(vcf2, trim_chr=True)

    vcf1_keys = set(vcf1_recs.keys())
    vcf2_keys = set(vcf2_recs.keys())

    if per_contig:
        vcf1_keys_per_contig: dict[str, set[str]] = defaultdict(set)
        for vcf1_key in vcf1_keys:
            vcf1_contig, _ = vcf1_key.split("_", 1)
            vcf1_keys_per_contig[vcf1_contig].add(vcf1_key)

        vcf2_keys_per_contig: dict[str, set[str]] = defaultdict(set)
        for vcf2_key in vcf2_keys:
            vcf2_contig, _ = vcf2_key.split("_", 1)
            vcf2_keys_per_contig[vcf2_contig].add(vcf2_key)

        all_contigs = set(vcf1_keys_per_contig.keys()).union(vcf2_keys_per_contig.keys())
        for contig in sorted(all_contigs, key=chromosome_sort):
            vcf1_only = vcf1_keys_per_contig[contig]
            vcf2_only = vcf2_keys_per_contig[contig]
            snv_single_diff(vcf1_only, vcf2_only, vcf1_recs, vcf2_recs, print_recs, simple, header, prefix=contig)
    else:
        snv_single_diff(vcf1_keys, vcf2_keys, vcf1_recs, vcf2_recs, print_recs, simple, header, prefix=None)


def score_diff(vcf1: str, vcf2: str):
    vcf1_recs = make_recs_dict(vcf1)
    vcf2_recs = make_recs_dict(vcf2)

    shared_keys = vcf1_recs.keys() & vcf2_recs.keys()

    def sort_lambda(key: str):
        (chrom, pos, _ref, _alt) = key.split("_")
        return (chrom, int(pos))

    nbr_skipped = 0
    for key in sorted(shared_keys, key=sort_lambda):

        vcf1_rec = vcf1_recs[key]
        vcf2_rec = vcf2_recs[key]
        if vcf1_rec.info.get("RankScore") is None or vcf2_rec.info.get("RankScore") is None:
            nbr_skipped += 1
            continue

        vcf1_rank_score = int(vcf1_rec.info["RankScore"][0].split(":")[1].replace(".0", ""))
        vcf1_rank_result = [int(val) for val in vcf1_rec.info["RankResult"][0].split("|")]

        vcf2_rank_score = int(vcf2_rec.info["RankScore"][0].split(":")[1].replace(".0", ""))
        vcf2_rank_result = [int(val) for val in vcf2_rec.info["RankResult"][0].split("|")]

        if vcf1_rank_score != vcf2_rank_score:
            (chrom, pos, ref, alt) = key.split("_")
            fields = [
                chrom,
                str(pos),
                ref,
                alt,
                str(vcf1_rank_score),
                str(vcf2_rank_score),
                "|".join([str(val) for val in vcf1_rank_result]),
                "|".join([str(val) for val in vcf2_rank_result]),
            ]
            print("\t".join(fields))
    print(f"Number skipped: {nbr_skipped}")


def make_recs_dict(vcf_path: str, trim_chr: bool = False) -> dict[str, VariantRecord]:

    fh = VariantFile(vcf_path)
    variant_recs: dict[str, VariantRecord] = dict()
    for record in fh:
        if record.alts is None:
            continue
        chrom = record.chrom
        if trim_chr:
            if chrom.startswith("chr"):
                chrom = chrom.replace("chr", "", 1)
        key = f"{chrom}_{record.pos}_{record.ref}_{'/'.join(record.alts)}"
        variant_recs[key] = record
    return variant_recs
