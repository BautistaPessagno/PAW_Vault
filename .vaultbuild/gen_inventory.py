#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera 'Source inventory': cada archivo versionado, la nota que lo explica y su etapa del roadmap."""
import os, re, sys, subprocess, fnmatch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, roadmap_data as D
REPO, COMMIT, ABS = build.REPO, build.COMMIT, build.ABS
def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, check=True).stdout
tracked = [t for t in git('ls-tree', '-r', '--name-only', COMMIT).split('\n') if t]
classmap = {os.path.basename(p)[:-5]: p for p in tracked if p.endswith('.java')}
notes = {os.path.splitext(f)[0] for f in os.listdir(build.VAULT) if f.endswith('.md')}
W = 'webapp/src/main/webapp/'
VIEWFLOW = {'auth': 'Authentication flow', 'cart': 'Cart flow', 'error': 'Validation and errors', 'inquiry': 'Inquiry and sale flow',
            'landing': 'Landing flow', 'publish': 'Publish flow', 'post': 'Post detail flow', 'profile': 'Profile flow'}
RULES = [
 ('.agents/*', ['Repository tooling']), ('.claude/*', ['Repository tooling']), ('.codex/*', ['Repository tooling']),
 ('.gitignore', ['Repository tooling', 'Configuration and running']), ('.worktreeinclude', ['Repository tooling']),
 ('AGENTS.md', ['Repository tooling']), ('CLAUDE.md', ['Repository tooling']),
 ('CONTEXT.md', ['Domain and identity', 'History and specifications']),
 ('README.md', ['Configuration and running', 'Known gaps and document drift']),
 ('TODO.md', ['History and specifications', 'Known gaps and document drift']),
 ('docs/setup.md', ['Build and dependencies', 'Configuration and running']),
 ('docs/*', ['History and specifications']),
 ('database/*', ['Schema history and seeds']), ('tools/sql/*', ['Schema history and seeds']),
 ('tools/seed_local_data.sh', ['Schema history and seeds', 'Development tools']),
 ('tools/setup_local_postgres.sh', ['Configuration and running', 'Development tools']),
 ('tools/*', ['Development tools']),
 ('*/.mvn/*', ['Repository tooling']), ('*pom.xml', ['Build and dependencies']),
 ('models/src/main/resources/.gitkeep', ['Build and dependencies']),
 ('persistence/src/main/resources/db/migration/*', ['Schema history and seeds', 'Database schema']),
 ('persistence/src/test/resources/populator.sql', ['Schema history and seeds', 'Testing and evidence']),
 ('services/src/main/resources/mail/*', ['Mail delivery']),
 ('webapp/src/*/resources/*.properties.example', ['Configuration and running']),
 ('webapp/src/main/resources/i18n/*', ['Localization']),
 ('webapp/src/main/resources/logback*', ['Logging']),
 (W + 'WEB-INF/web.xml', ['Startup and dependency injection', 'Security and authorization']),
 (W + 'WEB-INF/tags/*', ['UI components']),
 (W + 'css/*', ['UI styles and tokens']),
 (W + 'WEB-INF/views/*', ['Views and assets']),
 (W + 'js/*', ['Views and assets']), (W + 'images/*', ['Views and assets']),
]
def explain(p):
    if p.endswith('.java'):
        n = os.path.basename(p)[:-5]
        assert n in notes, n
        return ['%s' % n]
    for pat, ns in RULES:
        if fnmatch.fnmatchcase(p, pat):
            ns = list(ns)
            m = re.match(re.escape(W) + r'WEB-INF/views/([a-z]+)/', p)
            if m and VIEWFLOW.get(m.group(1)):
                ns.append(VIEWFLOW[m.group(1)])
            return ns
    raise SystemExit('sin regla: ' + p)
# etapa del roadmap
stage = {}
def resolve(item):
    if item in classmap: return [classmap[item]]
    if '**' in item: return [t for t in tracked if t.startswith(item.replace('**', ''))]
    if '*' in item: return [t for t in tracked if fnmatch.fnmatchcase(t, item) and t.count('/') == item.count('/')]
    return [item]
for i, (_, _, _, _, groups) in enumerate(D.STAGES):
    for _, items in groups:
        for it in items:
            for p in resolve(it):
                stage[p] = i
groups = {}
for p in tracked:
    parts = p.split('/')
    top = '(raíz)' if len(parts) == 1 else parts[0]
    if p.endswith('.java'):
        top = '%s · Java%s' % (parts[0], ' de test' if '/src/test/' in p else '')
    groups.setdefault(top, []).append(p)
out = ['''> [!summary] En una frase
> Registro de los %d archivos versionados en `c3e2a4c`: dónde está cada uno, qué nota del vault lo explica y en qué etapa del [[Roadmap de lectura]] se lee.

Se genera a partir de `git ls-tree`; el generador falla si un archivo no tiene nota asignada. Las %d clases Java tienen una nota propia con su código completo. Los demás archivos se explican en una nota temática, que en muchos casos también embebe su contenido.

No se incluyen archivos ignorados (propiedades con credenciales, compilados) ni el estado interno de Git.

## Resumen

| Grupo | Archivos |
|---|---|''' % (len(tracked), len(classmap))]
order = sorted(groups, key=lambda g: (g != '(raíz)', g.lower()))
for g in order:
    out.append('| %s | %d |' % (g, len(groups[g])))
out.append('| **Total** | **%d** |\n' % len(tracked))
for g in order:
    out.append('## %s\n' % g)
    out.append('| Archivo | Nota del vault | Etapa |')
    out.append('|---|---|---|')
    for p in groups[g]:
        label = p if not p.endswith('.java') else '/'.join(p.split('/')[-2:])
        out.append('| [%s](<%s/%s>) | %s | %d |' % (label, ABS, p, ' · '.join('[[%s]]' % n for n in explain(p)), stage[p]))
    out.append('')
missing_notes = sorted({n for p in tracked for n in explain(p)} - notes)
if missing_notes:
    raise SystemExit('notas inexistentes: %s' % missing_notes)
draft = '@title: Source inventory\n@categories: Navigation\n@type: index\n@tags: codemap, navigation\n\n' + '\n'.join(out)
open(os.path.join(build.DRAFTS, 'Source inventory.md'), 'w', encoding='utf-8').write(draft)
print('archivos', len(tracked), 'grupos', len(groups))
