#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""제출 패키지 생성 전 금칙어 검사. 지시서 7-2.

회사 실명, 클라이언트명 같은 G1 데이터가 응모작에 들어가면 제출 패키지를 만들지 않는다.
목록 자체는 G1-B라 저장소에 커밋하지 않는다(evals/blocklist.txt, .gitignore 처리).
저장소가 private으로 전환되기 전까지는 이 목록이 비어 있어 검사가 항상 통과만 한다 —
그 상태에서는 사람이 제출 전 직접 확인해야 한다는 뜻으로 읽는다.

사용: python3 evals/blocklist_check.py draft.md [ledger.md ...]
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCKLIST_PATH = os.path.join(HERE, 'blocklist.txt')


def load_blocklist():
    if not os.path.exists(BLOCKLIST_PATH):
        return []
    with io.open(BLOCKLIST_PATH, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


def check(paths):
    terms = load_blocklist()
    if not terms:
        print('경고: evals/blocklist.txt가 없거나 비어 있다. 금칙어 검사가 사실상 통과만 한다.')
        print('제출 전 사람이 회사 실명·클라이언트명 노출 여부를 직접 확인해야 한다.')
        return 0
    hits = []
    for path in paths:
        text = io.open(path, encoding='utf-8').read()
        for term in terms:
            if term in text:
                hits.append((path, term))
    if hits:
        print('금칙어 발견 — 제출 패키지를 만들지 않는다.')
        for path, term in hits:
            print('   %-30s %s' % (path, term))
        return 1
    print('통과: 금칙어 %d건 검사, 발견 없음' % len(terms))
    return 0


if __name__ == '__main__':
    sys.exit(check(sys.argv[1:]))
