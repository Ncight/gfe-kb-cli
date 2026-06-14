# -*- coding: utf-8 -*-
"""GFE 知识库查询核心: raw 精确 / wiki 双链关联 / 全文语义。纯标准库。"""
import re
import pathlib

KB = pathlib.Path(__file__).resolve().parent.parent / 'kb'
RAW = KB / 'raw'
WIKI = KB / 'wiki'
APIREF = RAW / 'GFE-CmdKB-APIref.src.md'


def _read(f):
    try:
        return f.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ''


# ---------- 精确层: API 签名 (解析 APIref) ----------
def parse_api():
    """APIref → {fn: [(module, obj, signature)]}"""
    idx = {}
    if not APIREF.exists():
        return idx
    mod = obj = None
    for line in _read(APIREF).splitlines():
        m = re.match(r'^##\s+(GFE\.\S+)', line)
        if m:
            mod = m.group(1); obj = None; continue
        m = re.match(r'^\*\*`(.+?)`\*\*', line)
        if m:
            obj = m.group(1); continue
        m = re.match(r'^-\s+`([\w.]+)`\s+(.+)', line)
        if m:
            idx.setdefault(m.group(1), []).append((mod, obj, m.group(2).strip()))
    return idx


def api(name):
    """returns (hits_dict, fallback_grep). APIref 未收录则 fallback 到 raw grep。"""
    idx = parse_api()
    name_l = name.lower()
    exact = {k: v for k, v in idx.items() if k.lower() == name_l}
    if exact:
        return exact, []
    part = {k: v for k, v in idx.items() if name_l in k.lower()}
    if part:
        return part, []
    return {}, grep(name, 'raw', 15)


# ---------- 全文层: grep ----------
def _dirs(where):
    return {'raw': [RAW], 'wiki': [WIKI], 'all': [RAW, WIKI]}.get(where, [RAW, WIKI])


def grep(kw, where='all', limit=40):
    kw_l = kw.lower(); res = []
    for d in _dirs(where):
        for f in sorted(d.rglob('*.md')):
            for i, l in enumerate(_read(f).splitlines(), 1):
                if kw_l in l.lower():
                    res.append((str(f.relative_to(KB)), i, l.strip()))
                    if len(res) >= limit:
                        return res
    return res


# ---------- 语义层(轻): 多词相关度排序 (真向量可接 qmd) ----------
def ask(words, where='all', top=8):
    scores = {}
    for d in _dirs(where):
        for f in d.rglob('*.md'):
            t = _read(f).lower()
            if not t:
                continue
            total = sum(t.count(w.lower()) for w in words)
            if total:
                hit = sum(1 for w in words if w.lower() in t)
                scores[f] = (hit, total)
    ranked = sorted(scores.items(), key=lambda x: (-x[1][0], -x[1][1]))[:top]
    return [(str(f.relative_to(KB)), h, c) for f, (h, c) in ranked]


# ---------- 关联层: wiki 双链图 ----------
def parse_links():
    """{node: {'out':set, 'in':set, 'path':str|None, 'type':str}}"""
    g = {}
    for f in WIKI.rglob('*.md'):
        node = f.stem
        text = _read(f)
        outs = set(re.findall(r'\[\[([^\]|#]+)', text))
        tm = re.search(r'^type:\s*(\S+)', text, re.M)
        g.setdefault(node, {'out': set(), 'in': set(), 'path': None, 'type': ''})
        g[node]['out'] |= outs
        g[node]['path'] = str(f.relative_to(KB))
        g[node]['type'] = tm.group(1) if tm else ''
        for o in outs:
            o = o.strip()
            g.setdefault(o, {'out': set(), 'in': set(), 'path': None, 'type': ''})
            g[o]['in'].add(node)
    return g


def related(topic):
    g = parse_links()
    tl = topic.lower()
    keys = [k for k in g if k.lower() == tl] or [k for k in g if tl in k.lower()]
    return {k: g[k] for k in keys}


# ---------- 避坑层: 优先易错清单 ----------
def pitfall(kw, limit=50):
    pf = RAW / 'GFE-CmdKB-pitfalls.src.md'
    res = []
    if pf.exists():
        for i, l in enumerate(_read(pf).splitlines(), 1):
            s = l.strip()
            if not s:
                continue
            if not kw or kw.lower() in s.lower():
                res.append(('raw/GFE-CmdKB-pitfalls.src.md', i, s))
                if len(res) >= limit:
                    return res
    if not res:
        res = grep(kw or u'⚠', 'raw', limit)
    return res


# ---------- 文件读取(给 case/show) ----------
def show(relpath):
    f = KB / relpath
    return _read(f) if f.exists() else None
