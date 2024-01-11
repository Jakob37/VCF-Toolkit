from typing import Callable
from pysam import VariantFile


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
