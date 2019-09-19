#!/usr/bin/env python3

import os
import re


class InvalidFileFormatException(Exception):
    pass

def load_signed():
    signed = []
    pattern1 = re.compile(r'([^|]+)\|([^|]+)$')
    pattern2 = re.compile(r'\s*\|([^|]+)\|([^|]+)\|\s*$')

    dir = 'signed'
    for basename in os.listdir(dir):
        filename = os.path.join(dir, basename)
        if not os.path.isfile(filename):
            print('Skipping non-file "%s"' % filename)
            continue

        with open(filename) as inp:
            for i, line in enumerate(inp):
                line = line.strip()
                if not line:
                    continue
                m = re.match(pattern1, line) or re.match(pattern2, line)
                if not m and line:
                    raise InvalidFileFormatException(
                        'File "%s", line %d: line does not follow the format:\n\t"%s"'
                        % (filename, i + 1, line)
                    )

                signed.append((m.group(1).strip(), m.group(2).strip()))
    return signed


def write_signed(signed, outp):
    for signature in signed:
        outp.write('| %-30s | %-50s |\n' % signature)


def update_readme(signed):
    with open('pre-readme.md') as inp, open('README.md', 'w') as outp:
        for line in inp:
            if line.strip() == '<!-- Signed -->':
                write_signed(signed, outp)
            else:
                outp.write(line)


def main():
    signed = load_signed()
    update_readme(signed)


if __name__ == '__main__':
    main()
