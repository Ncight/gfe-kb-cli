# -*- coding: utf-8 -*-
"""gfe — GFE 命令流知识库 CLI (OB 双层: raw精确 / wiki关联 / 全文语义)"""
import argparse
import sys
from . import core

if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def cmd_api(a):
    hits, fb = core.api(a.name)
    if hits:
        for fn in sorted(hits):
            print(u'\n● %s' % fn)
            for mod, obj, sig in hits[fn]:
                print(u'  [%s :: %s]' % (mod, obj))
                print(u'    %s' % sig)
    elif fb:
        print(u'APIref 未显式收录 "%s"，raw 中相关定义/用法:' % a.name)
        for path, ln, text in fb:
            print(u'  %s:%d: %s' % (path, ln, text[:150]))
    else:
        print(u'未找到 API: %s' % a.name)


def cmd_search(a):
    res = core.grep(a.kw, a.where, a.limit)
    if not res:
        print(u'无命中: %s' % a.kw); return
    for path, ln, text in res:
        print(u'%s:%d: %s' % (path, ln, text[:160]))
    print(u'\n(%d 条%s)' % (len(res), u', 已截断' if len(res) >= a.limit else u''))


def cmd_ask(a):
    q = ' '.join(a.q)
    words = a.q
    ranked = core.ask(words, a.where, a.top)
    if not ranked:
        print(u'无相关文档: %s' % q); return
    print(u'相关文档 (问: %s)：' % q)
    for path, hit, cnt in ranked:
        print(u'  [命中%d词/%d次] %s' % (hit, cnt, path))
    print(u'\n提示: 精确签名用 `gfe api`，整页内容用 `gfe show <路径>`；接 qmd 可做真向量语义。')


def cmd_related(a):
    hits = core.related(a.topic)
    if not hits:
        print(u'图中无节点: %s' % a.topic); return
    for node, d in hits.items():
        print(u'\n◆ %s%s%s' % (node, u'  <%s>' % d['type'] if d['type'] else u'', u'  (%s)' % d['path'] if d['path'] else u' (仅被引用)'))
        if d['out']:
            print(u'  → 指向: %s' % u', '.join(sorted(d['out'])[:20]))
        if d['in']:
            print(u'  ← 被引: %s' % u', '.join(sorted(d['in'])[:20]))


def cmd_case(a):
    res = core.grep(a.q, 'wiki', 60)
    res = [r for r in res if 'summaries' in r[0] or 'case' in r[2].lower()]
    seen = set()
    for path, ln, text in res:
        if path not in seen:
            seen.add(path); print(u'%s' % path)
    if not seen:
        print(u'无匹配案例: %s (试 gfe search %s --in wiki)' % (a.q, a.q))


def cmd_pitfall(a):
    res = core.pitfall(a.kw)
    for path, ln, text in res:
        print(u'%s:%d: %s' % (path, ln, text[:160]))
    if not res:
        print(u'无避坑命中: %s' % (a.kw or u'(全部)'))


def cmd_show(a):
    txt = core.show(a.path)
    if txt is None:
        print(u'文件不存在: %s' % a.path); return
    print(txt[:a.chars])
    if len(txt) > a.chars:
        print(u'\n... (截断, 全文 %d 字, --chars 调大)' % len(txt))


def main(argv=None):
    p = argparse.ArgumentParser(prog='gfe', description=u'GFE 命令流知识库 CLI — OB 双层(raw精确/wiki关联/全文语义)')
    sub = p.add_subparsers(dest='cmd')

    x = sub.add_parser('api', help=u'精确查 API 签名'); x.add_argument('name'); x.set_defaults(fn=cmd_api)
    x = sub.add_parser('search', help=u'全文检索'); x.add_argument('kw')
    x.add_argument('--in', dest='where', default='all', choices=['raw', 'wiki', 'all'])
    x.add_argument('--limit', type=int, default=40); x.set_defaults(fn=cmd_search)
    x = sub.add_parser('ask', help=u'语义检索(多词相关度排序)'); x.add_argument('q', nargs='+')
    x.add_argument('--in', dest='where', default='all', choices=['raw', 'wiki', 'all'])
    x.add_argument('--top', type=int, default=8); x.set_defaults(fn=cmd_ask)
    x = sub.add_parser('related', help=u'双链关联(wiki 图)'); x.add_argument('topic'); x.set_defaults(fn=cmd_related)
    x = sub.add_parser('case', help=u'案例(wiki summaries)'); x.add_argument('q'); x.set_defaults(fn=cmd_case)
    x = sub.add_parser('pitfall', help=u'避坑(raw ⚠/坑/红线)'); x.add_argument('kw', nargs='?', default=''); x.set_defaults(fn=cmd_pitfall)
    x = sub.add_parser('show', help=u'看整页 raw/wiki'); x.add_argument('path')
    x.add_argument('--chars', type=int, default=4000); x.set_defaults(fn=cmd_show)

    args = p.parse_args(argv)
    if not getattr(args, 'cmd', None):
        p.print_help(); return
    args.fn(args)


if __name__ == '__main__':
    main()
