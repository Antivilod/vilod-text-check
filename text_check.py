"""Read-only UTF-8 hygiene checks without printing file contents."""
import argparse
import json
from pathlib import Path
import re

VERSION = '0.1.0'
MAX_BYTES = 16 * 1024 * 1024
MAX_ISSUES = 1000


def check(raw, max_line_length=None, allow_long_dashes=False):
    if len(raw) > MAX_BYTES:
        raise ValueError('Input too large')
    if max_line_length is not None and max_line_length < 1:
        raise ValueError('max_line_length must be positive')
    bom = raw.startswith(b'\xef\xbb\xbf')
    text = raw.decode('utf-8-sig')
    issues = []
    total = 0

    def add(issue_type, line=None, column=None):
        nonlocal total
        total += 1
        if len(issues) < MAX_ISSUES:
            item = {'type': issue_type}
            if line is not None:
                item['line'] = line
            if column is not None:
                item['column'] = column
            issues.append(item)

    if bom:
        add('utf8_bom')
    crlf = text.count('\r\n')
    lf = text.count('\n') - crlf
    cr = text.count('\r') - crlf
    if sum(count > 0 for count in (crlf, lf, cr)) > 1:
        add('mixed_line_endings')
    if cr:
        add('bare_carriage_return')
    if text and not text.endswith(('\n', '\r')):
        add('missing_final_newline')
    normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    lines = normalized.split('\n')
    if lines[-1] == '':
        lines.pop()
    for number, line in enumerate(lines, 1):
        trailing = re.search(r'[ \t]+$', line)
        if trailing:
            add('trailing_whitespace', number, trailing.start() + 1)
        if '\x00' in line:
            add('nul_character', number, line.index('\x00') + 1)
        if max_line_length is not None and len(line) > max_line_length:
            add('line_too_long', number, max_line_length + 1)
        if not allow_long_dashes:
            for match in re.finditer(r'[\u2013\u2014]', line):
                add('long_dash', number, match.start() + 1)
    return {'ok': total == 0, 'lines': len(lines), 'issue_count': total,
            'truncated': total > MAX_ISSUES,
            'line_endings': {'lf': lf, 'crlf': crlf, 'cr': cr}, 'issues': issues}


def main(argv=None):
    parser = argparse.ArgumentParser(description='Inspect UTF-8 text without changing it')
    parser.add_argument('--version', action='version', version=VERSION)
    parser.add_argument('--max-line-length', type=int)
    parser.add_argument('--allow-long-dashes', action='store_true')
    parser.add_argument('file')
    args = parser.parse_args(argv)
    if args.max_line_length is not None and args.max_line_length < 1:
        parser.error('--max-line-length must be positive')
    try:
        with Path(args.file).open('rb') as stream:
            raw = stream.read(MAX_BYTES + 1)
        result = check(raw, args.max_line_length, args.allow_long_dashes)
    except (ValueError, OSError):
        parser.exit(2, 'Cannot inspect input. Use UTF-8 text up to 16 MiB.\n')
    print(json.dumps(result, indent=2))
    return 0 if result['ok'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
