#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificaciones estaticas del vault contra el commit documentado. Imprime un resumen y sale con 1 si algo falla."""
import os, re, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
VAULT, REPO, COMMIT, ABS = build.VAULT, build.REPO, build.COMMIT, build.ABS
SHORT = COMMIT[:7]
def git(*a, ok=True):
    r = subprocess.run(['git', '--no-optional-locks', '-C', REPO] + list(a), capture_output=True, text=True)
    if ok and r.returncode: raise SystemExit('git %s: %s' % (a, r.stderr[:200]))
    return r.stdout if r.returncode == 0 else None
tracked = set(t for t in git('ls-tree', '-r', '--name-only', COMMIT).split('\n') if t)
full = {}
def resolve_commit(short):
    if short not in full:
        out = git('rev-parse', '--verify', short + '^{commit}', ok=False)
        full[short] = out.strip() if out else None
    return full[short]
cache = {}
def show(commit, path):
    k = (commit, path)
    if k not in cache:
        cache[k] = git('show', '%s:%s' % (commit, path), ok=False)
    return cache[k]
notes = {}
for f in sorted(os.listdir(VAULT)):
    p = os.path.join(VAULT, f)
    if f.endswith('.md') and not os.path.islink(p):
        notes[f[:-3]] = open(p, encoding='utf-8').read()
bases = {f[:-5] for f in os.listdir(os.path.join(VAULT, 'Categories')) if f.endswith('.base')}
errors = []; R = {}
def strip_code(s):
    s = re.sub(r'^(`{3,})[^\n]*\n.*?\n\1[ \t]*$', '', s, flags=re.S | re.M)
    return re.sub(r'`[^`\n]*`', '', s)
# 1. frontmatter
fm = {}; nofm = []
for n, s in notes.items():
    m = re.match(r'---\n(.*?)\n---\n', s, re.S)
    if not m:
        nofm.append(n); continue
    d = {}
    for line in m.group(1).split('\n'):
        k = re.match(r'([A-Za-z_]+):\s*(.*)$', line)
        if not k:
            errors.append('frontmatter: línea inválida en %s: %r' % (n, line)); continue
        v = k.group(2).strip()
        if v.startswith('['):
            try: v = json.loads(v)
            except Exception: v = [x.strip().strip('"') for x in v.strip('[]').split(',') if x.strip()]
        else:
            v = v.strip('"')
        d[k.group(1)] = v
    fm[n] = d
    cats = d.get('categories')
    if not isinstance(cats, list) or not cats:
        errors.append('frontmatter: %s sin categories' % n)
    else:
        for c in cats:
            if c not in bases: errors.append('categoría sin vista: %s en %s' % (c, n))
R['notas'] = len(notes); R['sin frontmatter'] = nofm
# 2. wikilinks
bad = []; nlinks = 0
for n, s in notes.items():
    for m in re.finditer(r'!?\[\[([^\]\|#]+)(#[^\]\|]*)?(\|[^\]]*)?\]\]', strip_code(s)):
        t = m.group(1).strip(); nlinks += 1
        if t in notes or t in ('CLAUDE',): continue
        if os.path.exists(os.path.join(VAULT, t)): continue
        bad.append((n, t))
R['wikilinks'] = nlinks
if bad: errors.append('wikilinks sin resolver: %s' % sorted(set(bad))[:20])
# 3. extractos
pat = re.compile(r'Fuente exacta en `([0-9a-f]{7})`: (?:\[([^\]]+)\]\(<[^>]+>\)|`([^`]+)`), líneas (\d+)–(\d+)\.\n\n(`{3,})[^\n]*\n(.*?)\n\6[ \t]*\n', re.S)
nex = 0; exbad = []; announced = 0
for n, s in notes.items():
    announced += len(re.findall(r'^Fuente exacta en `', s, re.M))
    for m in pat.finditer(s):
        nex += 1
        short, path, a, b, body = m.group(1), m.group(2) or m.group(3), int(m.group(4)), int(m.group(5)), m.group(7)
        c = resolve_commit(short)
        src = show(c, path) if c else None
        if src is None:
            exbad.append((n, path, 'no existe en ' + short)); continue
        lines = src.split('\n')
        if src.endswith('\n'): lines = lines[:-1]
        want = '\n'.join(lines[a - 1:b])
        if want != body:
            exbad.append((n, path, '%d-%d difiere' % (a, b)))
R['extractos verificados'] = nex; R['extractos anunciados'] = announced
if exbad: errors.append('extractos: %s' % exbad[:20])
if announced != nex: errors.append('extractos sin verificar: %d anunciados, %d comparados' % (announced, nex))
# 4. cobertura Java
java = sorted(t for t in tracked if t.endswith('.java'))
miss = [t for t in java if os.path.basename(t)[:-5] not in fm or fm[os.path.basename(t)[:-5]].get('commit') != COMMIT
        or t not in (fm[os.path.basename(t)[:-5]].get('sources') or [])]
R['clases Java con nota al commit'] = '%d de %d' % (len(java) - len(miss), len(java))
if miss: errors.append('Java sin nota al día: %s' % miss[:10])
# 5. sources y enlaces a archivos
badsrc = []; nsrc = 0
for n, d in fm.items():
    if d.get('commit') != COMMIT: continue
    for p in d.get('sources') or []:
        nsrc += 1
        if p not in tracked: badsrc.append((n, p))
    for m in re.finditer(r'\]\(<%s/([^>]+)>\)' % re.escape(ABS), notes[n]):
        nsrc += 1
        if m.group(1) not in tracked: badsrc.append((n, m.group(1)))
R['rutas citadas verificadas'] = nsrc
if badsrc: errors.append('rutas no versionadas: %s' % badsrc[:10])
# 6. commits por nota
bycommit = {}
for n, d in fm.items():
    bycommit.setdefault((d.get('commit') or '')[:7] or '(sin commit)', []).append(n)
R['notas por commit'] = {k: len(v) for k, v in sorted(bycommit.items(), key=lambda kv: -len(kv[1]))}
R['notas fuera del commit actual'] = sorted(n for k, v in bycommit.items() if k != SHORT for n in v)
# 7. mermaid
KINDS = ('flowchart', 'graph', 'sequenceDiagram', 'stateDiagram-v2', 'stateDiagram', 'erDiagram', 'classDiagram')
nm = 0
for n, s in notes.items():
    for m in re.finditer(r'^```mermaid\n(.*?)\n```', s, re.S | re.M):
        nm += 1
        first = m.group(1).strip().split('\n')[0].strip()
        if not first.startswith(KINDS): errors.append('mermaid: tipo desconocido en %s: %r' % (n, first))
R['diagramas Mermaid'] = nm
# 8. secretos
sec = sorted(n for n, s in notes.items() if re.search(r'\$2[aby]\$\d\d\$', s))
R['notas con hashes BCrypt (deben ser solo código de test)'] = sec
for n in sec:
    if fm.get(n, {}).get('type') != 'test': errors.append('hash fuera de una nota de test: ' + n)
# 9. inventario y roadmap
inv = notes.get('Source inventory', ''); road = notes.get('Roadmap de lectura', '')
R['archivos versionados'] = len(tracked)
R['filas del inventario'] = len(re.findall(r'^\| \[', inv, re.M))
R['casillas del roadmap'] = len(re.findall(r'^- \[ \] ', road, re.M))
if R['filas del inventario'] != len(tracked): errors.append('inventario incompleto')
if R['casillas del roadmap'] != len(tracked): errors.append('roadmap incompleto')
R['HEAD del repositorio'] = git('rev-parse', 'HEAD').strip()
if R['HEAD del repositorio'] != COMMIT: errors.append('el repositorio avanzó: HEAD %s' % R['HEAD del repositorio'][:7])
for k, v in R.items(): print('%-55s %s' % (k, v))
print('\nERRORES: %d' % len(errors))
for e in errors: print(' -', e)
sys.exit(1 if errors else 0)
