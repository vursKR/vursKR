#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""결함 8종 기계 판정기. 규약은 evals/contract.md.

사용: python3 checks.py draft.md ledger.md
      python3 checks.py --diff prev.md cur.md
결과 한 건은 (코드, 행 번호, 메시지) 튜플이다.
"""
import io
import re
import sys

NUM = r'\d[\d,]*(?:\.\d+)?(?:\s?(?:억|만|천)\s?\d*(?:\.\d+)?)*'
UNIT = r'%p|%|만원|억원|명|원|건|개소|톤|면'
MARK = r'\[#([a-z]\d+)(?:\s*=\s*#([a-z]\d+)\s*([-+*/])\s*#([a-z]\d+))?\]'
VALMARK = re.compile(r'(' + NUM + r')\s*(?:' + UNIT + r')?\s*' + MARK)
UNMARKED = re.compile(r'(' + NUM + r')\s*(' + UNIT + r')')
CITE = re.compile(r'제\d+조(?:의\d+)?(?:제\d+항)?(?:제\d+호)?(?:[가-힣]목)?')
QUOTE = re.compile(r'"([^"]+)"')
HEDGE = ('확인되지 않', '추정', '으로 보인다', '것으로 보', '가능성', '미확인', '확인되면')
COMPARE = ('대비', '증가', '감소', '격차', '배 ', '늘', '줄')


def knum(s):
    """'52만 3천' → 523000.0, '48.6' → 48.6"""
    s = s.replace(',', '').replace(' ', '')
    total, rest = 0.0, s
    for word, mult in (('억', 1e8), ('만', 1e4), ('천', 1e3)):
        m = re.match(r'(\d+(?:\.\d+)?)' + word, rest)
        if m:
            total += float(m.group(1)) * mult
            rest = rest[m.end():]
    if rest:
        total += float(rest)
    return total


def table_rows(lines):
    """마크다운 표를 dict 목록으로. 첫 표 행이 헤더."""
    rows, header = [], None
    for line in lines:
        if not line.startswith('|'):
            header = None
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if header is None:
            header = cells
        elif set(''.join(cells)) <= set('-: '):
            continue
        else:
            rows.append(dict(zip(header, cells)))
    return rows


def parse_ledger(text):
    sections, cur = {}, None
    for line in text.splitlines():
        m = re.match(r'##\s+(\S+)', line)
        if m and not line.startswith('###'):
            cur = m.group(1)
            sections[cur] = []
        elif cur:
            sections[cur].append(line)
    values = {r['id']: r for r in table_rows(sections.get('수치', []))}
    unknown = table_rows(sections.get('미확인', []))
    laws, key = {}, None
    for line in sections.get('조문', []):
        if line.startswith('### '):
            m = CITE.search(line)
            key = m.group(0) if m else None
            laws[key] = ''
        elif key:
            laws[key] += line.strip() + ' '
    return values, laws, unknown


def sentences(text):
    """(행 번호, 문장) 목록. 표 행은 한 문장으로 본다."""
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith('|'):
            out.append((i, line))
            continue
        for s in re.split(r'(?<=다)\.\s*', line):
            if s.strip():
                out.append((i, s.strip()))
    return out


def check(draft, ledger):
    values, laws, unknown = parse_ledger(ledger)
    out = []
    sents = sentences(draft)
    lines = draft.splitlines()

    # C0 규약, D7 값 불일치, D1 행 이름, 산식(D2, D3, C0)
    for ln, s in sents:
        for m in VALMARK.finditer(s):
            num, cid, a, op, b = m.groups()
            row = values.get(cid)
            if row is None:
                out.append(('C0', ln, '원장에 없는 id #%s' % cid))
                continue
            if num.replace(' ', '') != row['값'].replace(' ', ''):
                out.append(('D7', ln, '#%s 본문 %s, 원장 %s' % (cid, num, row['값'])))
            kw = row.get('키워드', '-')
            if kw and kw != '-':
                missing = [k for k in kw.split(';') if k.strip() not in s]
                if missing:
                    out.append(('D1', ln, '#%s 문장에 행 이름 %s 없음' % (cid, '/'.join(missing))))
            if a:
                ra, rb = values.get(a), values.get(b)
                if not ra or not rb:
                    out.append(('C0', ln, '산식 피연산자 #%s #%s 중 원장에 없는 것' % (a, b)))
                    continue
                if ra['기준기간'] != rb['기준기간']:
                    out.append(('D3', ln, '#%s = #%s(%s) %s #%s(%s) 기준기간 불일치'
                                % (cid, a, ra['기준기간'], op, b, rb['기준기간'])))
                if op == '/' and ra['모집단'] != rb['모집단']:
                    out.append(('D2', ln, '#%s 분자 모집단 [%s] 분모 모집단 [%s]'
                                % (cid, ra['모집단'], rb['모집단'])))
                x, y = knum(ra['값']), knum(rb['값'])
                calc = {'+': x + y, '-': x - y, '*': x * y, '/': (x / y * 100 if y else 0)}[op]
                want = knum(row['값'])
                if abs(calc - want) > max(abs(want) * 0.01, 0.05):
                    out.append(('C0', ln, '#%s 재계산 %.2f, 원장 %s' % (cid, calc, row['값'])))
        # D3 비교 문장
        ids = [m.group(1) for m in re.finditer(MARK, s)]
        if len(ids) >= 2 and any(w in s for w in COMPARE):
            periods = {values[i]['기준기간'] for i in ids if i in values}
            if len(periods) > 1:
                out.append(('D3', ln, '비교 문장의 기준기간 %s' % '/'.join(sorted(periods))))
        # D6 미확인 충돌
        for u in unknown:
            kws = [k.strip() for k in u['키워드'].split(';')]
            if all(k in s for k in kws) and ('[?%s]' % u['id']) not in s \
                    and not any(h in s for h in HEDGE):
                out.append(('D6', ln, '미확인 %s(%s)을 단정: %s' % (u['id'], u['내용'], s[:40])))

    # D2 비율인데 모집단 없음
    for cid, row in values.items():
        if row['단위'] in ('%', '%p') and row['모집단'] in ('', '-') and not row['출처'].startswith('='):
            out.append(('D2', 0, '#%s 비율의 모집단이 원장에 없음' % cid))

    # D4 출처 없는 숫자
    for ln, line in enumerate(lines, 1):
        for m in UNMARKED.finditer(line):
            tail = line[m.end():m.end() + 20]
            if '[#' in tail or '[^' in tail:
                continue
            if re.search(r'제\s*$', line[:m.start()]):
                continue
            out.append(('D4', ln, '출처 없는 숫자 %s%s' % (m.group(1), m.group(2))))

    # D5 조문 인용
    for ln, line in enumerate(lines, 1):
        for cm in CITE.finditer(line):
            key = cm.group(0)
            qm = QUOTE.search(line, cm.end())
            if not qm:
                continue
            if key not in laws:
                out.append(('D5?', ln, '%s 원문이 원장에 없어 미대조' % key))
                continue
            # 중략(…)으로 나눈 조각이 원문에 순서대로 있어야 한다
            body, pos, ok = re.sub(r'\s+', '', laws[key]), 0, True
            for part in re.split(r'…|\.\.\.', re.sub(r'\s+', '', qm.group(1))):
                pos = body.find(part, pos)
                if pos < 0:
                    ok = False
                    break
                pos += len(part)
            if not ok:
                out.append(('D5', ln, '%s 인용문이 원문에 없음: %s' % (key, qm.group(1)[:30])))

    # D7 같은 id 값이 문서 안에서 다름
    seen = {}
    for ln, s in sents:
        for m in VALMARK.finditer(s):
            num, cid = m.group(1).replace(' ', ''), m.group(2)
            if cid in seen and seen[cid][0] != num:
                out.append(('D7', ln, '#%s 값이 %d행 %s, %d행 %s' % (cid, seen[cid][1], seen[cid][0], ln, num)))
            seen.setdefault(cid, (num, ln))

    # D8 상호참조
    secs, tabs, apps = set(), set(), set()
    for line in lines:
        m = re.match(r'##\s+(\d+)\.', line)
        if m:
            secs.add(m.group(1))
        m = re.match(r'###\s+(\d+-\d+)', line)
        if m:
            secs.add(m.group(1))
        m = re.match(r'표\s+(\d+)\.', line)
        if m:
            tabs.add(m.group(1))
        m = re.match(r'##\s+부록\s+(\S+?)\.', line)
        if m:
            apps.add(m.group(1))
    for ln, line in enumerate(lines, 1):
        if re.match(r'(#|표\s+\d+\.)', line):
            continue
        for m in re.finditer(r'(\d+-\d+)절', line):
            if m.group(1) not in secs:
                out.append(('D8', ln, '없는 절 %s' % m.group(1)))
        for m in re.finditer(r'(\d+)장', line):
            if m.group(1) not in secs:
                out.append(('D8', ln, '없는 장 %s' % m.group(1)))
        for m in re.finditer(r'표\s+(\d+)', line):
            if m.group(1) not in tabs:
                out.append(('D8', ln, '없는 표 %s' % m.group(1)))
        for m in re.finditer(r'부록\s+([A-Z가-힣])(?![가-힣])', line):
            if m.group(1) not in apps:
                out.append(('D8', ln, '없는 부록 %s' % m.group(1)))
    return sorted(set(out), key=lambda f: (f[1], f[0]))


def stale_values(prev, cur):
    """diff 모드 D7. 개정에서 바뀐 id의 옛 값이 새 문서에 남아 있으면 보고."""
    def vals(text):
        d = {}
        for ln, s in sentences(text):
            for m in VALMARK.finditer(s):
                d.setdefault(m.group(2), []).append((m.group(1).replace(' ', ''), ln))
        return d
    old, new = vals(prev), vals(cur)
    out = []
    for cid, occ in new.items():
        if cid not in old:
            continue
        old_vals = {v for v, _ in old[cid]}
        new_vals = {v for v, _ in occ}
        changed = new_vals - old_vals
        if not changed:
            continue
        for v, ln in occ:
            if v in old_vals:
                out.append(('D7', ln, '#%s 옛 값 %s 잔존 (새 값 %s)' % (cid, v, '/'.join(sorted(changed)))))
    return out


def check_revision(items, cur):
    """반영 검증. items: [{"old": 문자열, "new": 문자열 또는 ""}]"""
    out = []
    lines = cur.splitlines()
    for it in items:
        where = [i for i, l in enumerate(lines, 1) if it['old'] in l]
        if where:
            out.append(('R', where[0], '미반영: 옛 표현 잔존 %s행 %s' % (where, it['old'][:30])))
        if it.get('new') and it['new'] not in cur:
            out.append(('R', 0, '미반영: 새 표현 없음 %s' % it['new'][:30]))
    return out


def main(argv):
    read = lambda p: io.open(p, encoding='utf-8').read()
    if argv[0] == '--diff':
        found = stale_values(read(argv[1]), read(argv[2]))
    else:
        found = check(read(argv[0]), read(argv[1]))
    for code, ln, msg in found:
        print('%-4s %4d  %s' % (code, ln, msg))
    print('\n%s' % ('통과' if not found else '%d건' % len(found)))
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
