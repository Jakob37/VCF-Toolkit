#!/usr/bin/env python

import argparse
import re

parser = argparse.ArgumentParser(
    description="Basic utility to remove redundant INFO field information"
)
parser.add_argument("-i", "--input", help="Input VCF file", required=True)
parser.add_argument("-o", "--output", help="Output VCF file", required=True)
parser.add_argument("--pattern", help="Pattern to trim out content from INFO fields", required=True)
parser.add_argument("--version", action="version", version="v0.1")
args = parser.parse_args()

compiled_pattern = re.compile(args.pattern)

header_lines = 0
content_lines = 0
updated_lines = 0
with open(args.input) as in_fh, open(args.output, "w") as out_fh:
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

print(
    f"{header_lines} header lines, {content_lines} content lines, {updated_lines} updated content lines"
)
print(f"Written file to {args.output}")
