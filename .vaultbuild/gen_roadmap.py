#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera el borrador de 'Roadmap de lectura' y verifica que cubra todos los archivos versionados."""
import os, re, subprocess, fnmatch, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, summaries, roadmap_data as D, roadmap_hints as HN

REPO, COMMIT, ABS = build.REPO, build.COMMIT, build.ABS
def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, check=True).stdout
tracked = git('ls-tree', '-r', '--name-only', COMMIT).split('\n')
tracked = [t for t in tracked if t]
lines = {}
for row in git('grep', '-c', '', COMMIT, '--', '.').split('\n'):
    if row:
        _, path, n = row.split(':', 2) if row.count(':') == 2 else (None, ':'.join(row.split(':')[1:-1]), row.split(':')[-1])
        lines[path] = int(n)
classmap = {os.path.basename(p)[:-5]: p for p in tracked if p.endswith('.java')}
SUM = dict(summaries.S); SUM.update(summaries.T)

def hint_java(name):
    s = SUM.get(name, '')
    s = re.sub(r'\s*Ver \[\[.*$', '', s).strip()
    first = re.split(r'(?<=[.;])\s', s)[0] if s else ''
    return first.rstrip('.;') + '.' if first else ''

def resolve(item):
    if item in classmap:
        return [classmap[item]]
    if '**' in item:
        pre = item.replace('**', '')
        return sorted(t for t in tracked if t.startswith(pre))
    if '*' in item:
        got = [t for t in tracked if fnmatch.fnmatchcase(t, item) and t.count('/') == item.count('/')]
        def key(t):
            m = re.search(r'/V(\d+)__', t)
            return (int(m.group(1)) if m else 0, t)
        return sorted(got, key=key)
    if item in tracked:
        return [item]
    raise SystemExit('item sin resolver: ' + item)

def module(path):
    return path.split('/')[0]

def render(path):
    if path.endswith('.java'):
        name = os.path.basename(path)[:-5]
        kind = 'test' if '/src/test/' in path else module(path)
        return '- [ ] [[%s]] `%s` — %s' % (name, kind, hint_java(name))
    h = HN.H.get(path, '')
    if not h and path.startswith('services/src/main/resources/mail/'):
        h = HN.MAIL.get(os.path.basename(path)[:-5], '')
    tail = ' — ' + h if h else ''
    return '- [ ] [%s](<%s/%s>)%s' % (path, ABS, path, tail)

seen = {}
out = []
table = []
for i, (title, goal, notes, questions, groups) in enumerate(D.STAGES):
    body = []
    nfiles = nlines = 0
    for sub, items in groups:
        body.append('### %s\n' % sub)
        for it in items:
            for p in resolve(it):
                if p in seen:
                    raise SystemExit('repetido: %s (etapas %s y %d)' % (p, seen[p], i))
                seen[p] = i
                nfiles += 1; nlines += lines.get(p, 0)
                body.append(render(p))
        body.append('')
    table.append((i, title, nfiles, nlines))
    out.append('## Etapa %d — %s\n' % (i, title))
    out.append('*%d archivos · %s líneas*\n' % (nfiles, format(nlines, ',').replace(',', '.')))
    out.append('**Objetivo.** %s\n' % goal)
    out.append('**Primero, en el vault:** ' + ' · '.join('[[%s]]' % n for n in notes) + '\n')
    out.extend(body)
    out.append('**Al terminar deberías poder contestar:**\n')
    out.extend('- %s' % q for q in questions)
    out.append('')
missing = [t for t in tracked if t not in seen]
if missing:
    raise SystemExit('sin asignar (%d): %s' % (len(missing), ', '.join(missing[:40])))
total_lines = sum(lines.get(t, 0) for t in tracked)
intro = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roadmap_intro.md'), encoding='utf-8').read()
rows = '\n'.join('| %d | %s | %d | %s |' % (i, t, n, format(l, ',').replace(',', '.')) for i, t, n, l in table)
intro = intro.replace('{{TABLE}}', rows).replace('{{FILES}}', str(len(tracked))).replace('{{LINES}}', format(total_lines, ',').replace(',', '.')).replace('{{JAVA}}', str(len(classmap)))
draft = '@title: Roadmap de lectura\n@categories: Navigation\n@tags: codemap, navigation\n\n' + intro + '\n' + '\n'.join(out)
open(os.path.join(build.DRAFTS, 'Roadmap de lectura.md'), 'w', encoding='utf-8').write(draft)
print('etapas', len(table), 'archivos', len(seen), 'de', len(tracked), 'líneas', total_lines)
for r in table: print(r)
