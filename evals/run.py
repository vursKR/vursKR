#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""eval 하네스 실행기.

python3 evals/run.py              양방향 검증: 정상본 오탐 0, 주입본 8종 전건 검출. 골든케이스가 있으면 함께
python3 evals/run.py check draft.md ledger.md
python3 evals/run.py diff prev.md cur.md
python3 evals/run.py verify report.json cur.md      반영 검증
python3 evals/run.py prose draft.md                  korean-prose 문체 검사(경고)
"""
import glob
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks    # noqa: E402
import inject    # noqa: E402

read = lambda p: io.open(p, encoding='utf-8').read()


def show(found):
    for code, ln, msg in found:
        print('   %-4s %4d  %s' % (code, ln, msg))


def bidirectional():
    draft, ledger = read(os.path.join(HERE, 'samples/clean.md')), read(os.path.join(HERE, 'samples/ledger.md'))
    ok = True
    found = checks.check(draft, ledger)
    hard = [f for f in found if f[0] != 'D5?']
    print('정상본  %s' % ('오탐 0' if not hard else '오탐 %d건' % len(hard)))
    show(hard)
    ok &= not hard
    print('%-6s %-6s %s' % ('주입', '검출', '그 외 판정'))
    for code, d, l in inject.variants(draft, ledger):
        found = checks.check(d, l)
        if code == 'D7':
            found += checks.stale_values(draft, d)
        hit = [f for f in found if f[0] == code]
        other = sorted({f[0] for f in found} - {code})
        print('%-6s %-6s %s' % (code, '검출' if hit else '누락', ' '.join(other)))
        if not hit:
            show(found)
        ok &= bool(hit)
    return ok


def golden():
    """evals/golden/GC-*/ 에 input.md, ledger.md, expected.json 이 있으면 검출률을 잰다."""
    ok = True
    for case in sorted(glob.glob(os.path.join(HERE, 'golden', 'GC-*'))):
        paths = [os.path.join(case, n) for n in ('input.md', 'ledger.md', 'expected.json')]
        if not all(os.path.exists(p) for p in paths):
            continue
        found = checks.check(read(paths[0]), read(paths[1]))
        expected = json.load(io.open(paths[2], encoding='utf-8'))
        lines = read(paths[0]).splitlines()
        hits = 0
        for e in expected:
            if any(f[0] == e['code'] and e['anchor'] in lines[f[1] - 1] for f in found if f[1] > 0):
                hits += 1
        name = os.path.basename(case)
        print('%s  검출 %d / %d' % (name, hits, len(expected)))
        base_path = os.path.join(HERE, 'baseline.json')
        base = json.load(io.open(base_path, encoding='utf-8')) if os.path.exists(base_path) else {}
        if name in base and hits < base[name]:
            print('   회귀: 기준선 %d보다 줄었다' % base[name])
            ok = False
    return ok


def prose(path):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'prose.py'), path],
                       capture_output=True, text=True)
    last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()
    print('문체(경고)  %s' % last)


def main(argv):
    if not argv:
        ok = bidirectional()
        ok &= golden()
        print('\n%s' % ('PASS' if ok else 'FAIL'))
        return 0 if ok else 1
    cmd = argv[0]
    if cmd == 'check':
        found = checks.check(read(argv[1]), read(argv[2]))
    elif cmd == 'diff':
        found = checks.stale_values(read(argv[1]), read(argv[2]))
    elif cmd == 'verify':
        found = checks.check_revision(json.load(io.open(argv[1], encoding='utf-8')), read(argv[2]))
    elif cmd == 'prose':
        prose(argv[1])
        return 0
    else:
        print(__doc__)
        return 2
    show(found)
    print('%s' % ('통과' if not found else '%d건' % len(found)))
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
