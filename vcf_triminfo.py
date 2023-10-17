#!/usr/bin/env python

import argparse
import re
from typing import NamedTuple


class ParseStats(NamedTuple):
    header_lines: int
    content_lines: int
    updated_lines: int


def main():
    args = parse_args()
    status = trim_info(args.input, args.output, args.pattern)
    print(
        f"{status['header_lines']} header lines, {status['content_lines']} content lines, {status['updated_lines']} updated content lines"
    )
    print(f"Written file to {args.output}")


def trim_info(in_fp: str, out_fp: str, pattern: str) -> ParseStats:
    header_lines = 0
    content_lines = 0
    updated_lines = 0
    compiled_pattern = re.compile(pattern)
    with open(in_fp) as in_fh, open(out_fp, "w") as out_fh:
        for line in in_fh:
            line = line.rstrip()
            if line.startswith("#"):
                header_lines += 1
                print(line, file=out_fh)
                continue

            content_lines += 1

            updated_line = compiled_pattern.sub("", line, 1)

            if updated_line != line:
                updated_lines += 1

            print(updated_line, file=out_fh)
    return {
        "header_lines": header_lines,
        "content_lines": content_lines,
        "updated_lines": updated_lines,
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Basic utility to remove redundant INFO field information"
    )
    parser.add_argument("-i", "--input", help="Input VCF file", required=True)
    parser.add_argument("-o", "--output", help="Output VCF file", required=True)
    parser.add_argument(
        "--pattern", help="Pattern to trim out content from INFO fields", required=True
    )
    parser.add_argument("--version", action="version", version="v0.1")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
