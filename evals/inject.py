#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""결함 8종 주입. 정상본(draft, ledger)에서 결함 하나를 심은 변형본을 만든다.

각 주입 함수는 (draft, ledger) → (draft, ledger)를 돌려주고, 심은 결함 코드는 함수 이름이다.
실제로 발생한 오류만 모은 목록이다(지시서 5-2).
"""
import re


def D1(d, l):
    """표의 행 이름 오독: 다른 행의 이름을 가져다 쓴다."""
    return d.replace('현재 살고 있는 읍·면·동 밖에서', '현재 살고 있는 시군구 밖에서', 1), l


def D2(d, l):
    """분모 단정: 모집단이 다른 수치로 나눈다."""
    return d.replace('[#c2 = #b2 / #b1]', '[#c2 = #b2 / #b3]', 1), l


def D3(d, l):
    """기준연도 불일치: 관측 기간이 다른 수치를 뺀다."""
    return d.replace('[#c1 = #a2 - #a3]', '[#c1 = #a2 - #a4]', 1), l


def D4(d, l):
    """출처 없는 숫자: 마커를 뗀다."""
    return d.replace('21.1%[#a3]', '21.1%', 1), l


def D5(d, l):
    """조문 항 혼동: 제3항 인용문을 제2항이라고 쓴다."""
    return d.replace('제9조제3항은', '제9조제2항은', 1), l


def D6(d, l):
    """본문이 단정한 사실을 미확인 목록이 미확인이라고 적는다."""
    return d.replace('강북구 조례에는 구민 한정이 없는 것으로 보인다[?u1].',
                     '강북구 조례에는 구민 한정이 없다.', 1), l


def D7(d, l):
    """개정하면서 본문과 원장만 고치고 표를 안 고친다."""
    d = d.replace('수혜자는 3만 8천 명[#b2]', '수혜자는 4만 1천 명[#b2]', 1)
    l = l.replace('| b2 | 3만 8천 |', '| b2 | 4만 1천 |', 1)
    return d, l


def D8(d, l):
    """상호참조 깨짐: 없는 절을 가리킨다."""
    return d.replace('2-1절의', '2-4절의', 1), l


ALL = [D1, D2, D3, D4, D5, D6, D7, D8]


def variants(draft, ledger):
    for fn in ALL:
        d, l = fn(draft, ledger)
        assert (d, l) != (draft, ledger), '%s 주입이 문서를 바꾸지 못함' % fn.__name__
        yield fn.__name__, d, l
