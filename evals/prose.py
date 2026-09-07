#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""한국어 원고 문체 검사기. 사용법: python3 check.py 파일.md [파일2.md ...]"""
import io, re, sys, statistics

RULES = [
 ('이중피동',    r'되어지|보여지|불려지|나뉘어지|쓰여지|잊혀지|읽혀지|닫혀지', 0, '금지'),
 ('에 의해',     r'에 의해|에 의하여|에 의한',                              0, '금지'),
 ('을 통해',     r'[을를] 통해|[을를] 통한|[을를] 통하여',                    0, '금지'),
 ('에 있어',     r'에 있어서|에게 있어|함에 있어',                           0, '금지'),
 ('로 인해',     r'로 인해|로 인한|로 인하여',                              0, '금지'),
 ('로부터',      r'로부터',                                              0, '금지'),
 ('에도 불구',   r'에도 불구하',                                          0, '금지'),
 ('겹조사',      r'에의 |로의 |에서의 |와의 |과의 |로서의 ',                  0, '금지'),
 ('했었다',      r'했었|였었|었었',                                       0, '금지'),
 ('것이 가능',   r'것이 가능|것은 가능',                                    0, '금지'),
 ('화되다',      r'화되어지|화시키',                                       0, '금지'),
 ('뿐만 아니라', r'뿐만 아니라',                                          0, '금지'),
 ('라는 점에서', r'[다라]는 점에서',                                       0, '금지'),
 ('라고 할 수',  r'라고 할 수 있|이라 할 수 있|평가된다|주목할 만',            0, '금지'),
 ('em dash',    r'—',                                              0, '금지'),
 ('가운데점',    r'·',                                              0, '금지(각주 서지 제외)'),
 ('물결표',      r'(?<![0-9])~|~(?![0-9])',                              0, '금지(수치 범위는 제외)'),
 ('AI 상투어',   r'혁신적|획기적|효과적으로|성공적으로|전략적으로|시사하는 바|무한한 가능성', 0, '금지'),
 ('결론 봉합',   r'결론적으로|요약하자면|정리하자면|살펴보았|하는 것이 중요하|것이 바람직하|주목할 필요가', 0, '금지'),
 ('다양한',      r'다양한',                                             0.5, '인용 안이면 허용'),
 ('대구 A아니라B', r'[가이은는을를로서고]\s*아니라',                        2.5, ''),
 ('대구 A아니다.B', r'아니다\.\s*[^.\n]{4,45}다\.',                        5.0, '가장 놓치기 쉬움'),
 ('대구 반대다',   r'(반대다|다르다)\.',                                   2.5, ''),
 ('서수 블록',     r'첫째',                                              2.0, '한 장에 두 번까지'),
 ('~적(的)',      r'[가-힣]적(인|으로|\s|,|\.)',                          5.0, ''),
 ('~고 있다',     r'고 있[다는으었]',                                     5.0, ''),
 ('~들 복수',     r'것들|사람들|회사들|일들|자료들|문서들|조직들|기업들',      8.0, ''),
 ('~성(性)',      r'[가-힣]성[을이의은,\.\s]',                            2.0, ''),
 ('가지고 있다',  r'가지고 있|갖고 있',                                    0.5, ''),
 ('에 대해/대한', r'에 대해|에 대한|에 관해|에 관한',                        1.0, ''),
 ('하기 위해',    r'하기 위해|[을를] 위해',                                0.5, ''),
]

def strip(s):
    s = re.sub(r'^\*아래 머리.*$', '', s, flags=re.M)   # 집필용 메모
    s = re.sub(r'^\[\^[\w]+\]:.*$', '', s, flags=re.M)  # 각주(서지 표기 예외)
    return s

def run(paths):
    body = ''
    for p in paths:
        body += strip(io.open(p, encoding='utf-8').read()) + '\n'
    n = len(body); scale = n / 10000.0
    print('검사 대상 %d자 (%.1f만자)\n' % (n, n / 10000))
    fail = []
    print('%-14s %5s %8s %8s  %s' % ('항목', '건수', '만자당', '한계', '판정'))
    print('-' * 62)
    for name, pat, limit, note in RULES:
        k = len(re.findall(pat, body)); d = k / scale if scale else 0
        ok = d <= limit
        if not ok: fail.append((name, k, d, limit, pat))
        print('%-14s %5d %8.1f %8.1f  %s' % (name, k, d, limit, 'OK' if ok else 'X'))
    anti = (len(re.findall(r'[가이은는을를로서고]\s*아니라', body))
          + len(re.findall(r'아니다\.\s*[^.\n]{4,45}다\.', body))
          + len(re.findall(r'(반대다|다르다)\.', body)))
    ad = anti / scale if scale else 0
    print('\n대구 총지수 %d건, 만자당 %.1f (한계 10.0). 문단당 한 번을 넘으면 틱이다.' % (anti, ad))
    if ad > 10.0: fail.append(('대구 총지수', anti, ad, 10.0, r'[가이은는을를로서고]\s*아니라'))
    sents = [x.strip() for x in re.split(r'(?<=다)\.\s|\.\n|\n\n', body) if 8 < len(x) < 400]
    if sents:
        L = [len(x) for x in sents]; long_n = sum(1 for x in L if x > 60)
        print('문장 평균 %.1f자 / 60자 초과 %d개 (%.1f%%)' % (statistics.mean(L), long_n, long_n / len(L) * 100))
    ends = re.findall(r'([가-힣]{2})\.(?:\s|$)', body)
    runs, cur, mx = 1, None, []
    for e in ends:
        if e == cur: runs += 1
        else:
            if runs >= 4: mx.append((cur, runs))
            cur, runs = e, 1
    if mx: print('같은 종결어미 4연속 이상: %d곳 %s' % (len(mx), mx[:6]))
    if fail:
        print('\n=== 한계 초과 항목의 실제 위치 ===')
        for name, k, d, limit, pat in fail:
            print('\n[%s] %d건, 만자당 %.1f (한계 %.1f)' % (name, k, d, limit))
            for m in list(re.finditer(pat, body))[:4]:
                a, b = max(0, m.start() - 35), min(n, m.end() + 35)
                print('   …' + body[a:b].replace('\n', ' ') + '…')
    print('\n%s' % ('통과' if not fail else '수정 필요 %d항목' % len(fail)))
    return 1 if fail else 0

if __name__ == '__main__':
    sys.exit(run(sys.argv[1:]))
