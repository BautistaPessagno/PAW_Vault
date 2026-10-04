#!/usr/bin/env python3
"""Arma notas del Vault a partir de borradores con marcadores, tomando el codigo de los objetos Git."""
import os, re, sys, glob, subprocess, json

HOME = os.path.expanduser('~')
HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.join(HERE, 'drafts')
# Rutas: por defecto, este directorio vive en <vault>/.vaultbuild y el repo es <vault>/../paw2026b.
# PAW_VAULT y PAW_REPO las pisan (por ejemplo, cuando las carpetas estan montadas en otro lado).
def _first(*cands):
    for c in cands:
        if c and os.path.isdir(c):
            return c
    return cands[-1]
VAULT = _first(os.environ.get('PAW_VAULT'), os.path.dirname(HERE) if os.path.basename(HERE) == '.vaultbuild' else None,
               os.path.join(HOME, 'mnt', 'PAW_Vault'))
REPO = _first(os.environ.get('PAW_REPO'), os.path.join(os.path.dirname(VAULT), 'paw2026b'), os.path.join(HOME, 'mnt', 'paw2026b'))
# Ruta absoluta del repo en la maquina del usuario: es la que llevan los enlaces de las notas.
ABS = os.environ.get('PAW_REPO_LINK', '/Users/bautistapessagno/Desktop/proyectos_itba/PAW/paw2026b')
# Commit documentado y fecha de inspeccion: se cambian en cada actualizacion del vault.
COMMIT = os.environ.get('PAW_COMMIT', '8929aeaa59b250e6c7119212f96437e153e815ac')
SHORT = COMMIT[:7]
SNAPSHOT = os.environ.get('PAW_SNAPSHOT', '2026-10-04')
LANG = {'java': 'java', 'sql': 'sql', 'xml': 'xml', 'jsp': 'jsp', 'tag': 'jsp', 'js': 'javascript',
        'css': 'css', 'properties': 'properties', 'html': 'html', 'py': 'python', 'sh': 'bash',
        'md': 'markdown', 'tsv': 'text', 'svg': 'xml', 'example': 'properties'}
_cache = {}
_tracked = None

def tracked():
    global _tracked
    if _tracked is None:
        out = subprocess.run(['git', '--no-optional-locks', '-C', REPO, 'ls-tree', '-r', '--name-only', COMMIT],
                             capture_output=True, text=True, check=True).stdout
        _tracked = set(l for l in out.split('\n') if l)
    return _tracked

def show(path):
    if path not in _cache:
        if path not in tracked():
            raise SystemExit('ruta no versionada en el commit: ' + path)
        _cache[path] = subprocess.run(['git', '--no-optional-locks', '-C', REPO, 'show', COMMIT + ':' + path],
                                      capture_output=True, text=True, check=True).stdout
    return _cache[path]

def lang_of(path):
    return LANG.get(path.rsplit('.', 1)[-1], 'text')

def fence(text, lang):
    ticks = '````' if '```' in text else '```'
    return ticks + lang + '\n' + text.rstrip('\n') + '\n' + ticks

def link(path):
    return '[%s](<%s/%s>)' % (path, ABS, path)

def build(draft_path, notes):
    raw = open(draft_path, encoding='utf-8').read()
    head, body = raw.split('\n\n', 1)
    meta = {}
    for line in head.split('\n'):
        m = re.match(r'@(\w+):\s*(.*)$', line)
        if not m:
            raise SystemExit('cabecera invalida en %s: %r' % (draft_path, line))
        meta[m.group(1)] = m.group(2).strip()
    sources = []
    def add(p):
        if p not in sources:
            sources.append(p)
    files = [p.strip() for p in meta.get('files', '').split(',') if p.strip()]
    for p in files:
        show(p); add(p)
    for p in [p.strip() for p in meta.get('extra_sources', '').split(',') if p.strip()]:
        show(p); add(p)

    def code(m):
        path, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        lines = show(path).split('\n')
        if lines and lines[-1] == '':
            lines = lines[:-1]
        if a < 1 or b > len(lines) or a > b:
            raise SystemExit('rango fuera del archivo: %s %d-%d (tiene %d)' % (path, a, b, len(lines)))
        add(path)
        return 'Fuente exacta en `%s`: %s, líneas %d–%d.\n\n%s' % (
            SHORT, link(path), a, b, fence('\n'.join(lines[a - 1:b]), lang_of(path)))

    def whole(m):
        path = m.group(1)
        text = show(path)
        n = len(text.rstrip('\n').split('\n')) if text.strip() else 0
        add(path)
        if n == 0:
            return 'Fuente exacta en `%s`: %s, archivo vacío.' % (SHORT, link(path))
        return 'Fuente exacta en `%s`: %s, líneas 1–%d.\n\n%s' % (SHORT, link(path), n, fence(text, lang_of(path)))

    body = re.sub(r'\{\{code:([^:}]+):(\d+)-(\d+)\}\}', code, body)
    body = re.sub(r'\{\{file:([^}]+)\}\}', whole, body)
    body = body.rstrip('\n') + '\n'
    if files:
        body += '\n## Archivos para seguir el flujo\n\n'
        for p in files:
            base = os.path.splitext(os.path.basename(p))[0]
            suffix = ' · [[%s]]' % base if base in notes and p.endswith('.java') else ''
            body += '- %s%s\n' % (link(p), suffix)
    if meta.get('footer', 'yes') != 'no':
        body += '\nFuente inspeccionada: `%s`, %s. Es evidencia estática; no implica ejecución de la aplicación. [[Source inventory]] · [[Roadmap de lectura]]\n' % (SHORT, SNAPSHOT)
    q = lambda s: json.dumps(s, ensure_ascii=False)
    fm = ['---', 'title: ' + q(meta['title']),
          'categories: [' + ', '.join(q(c.strip()) for c in meta['categories'].split(',')) + ']',
          'type: ' + q(meta.get('type', 'guide')), 'module: ' + q(meta.get('module', 'cross-cutting')),
          'project: "quieroVinilos"', 'snapshot: ' + q(SNAPSHOT), 'commit: ' + q(COMMIT),
          'status: ' + q(meta.get('status', 'documented'))]
    if meta.get('tags'):
        fm.append('tags: [' + ', '.join(q(t.strip()) for t in meta['tags'].split(',')) + ']')
    if sources:
        fm.append('sources: [' + ', '.join(q(s) for s in sources) + ']')
    fm.append('---')
    out = '\n'.join(fm) + '\n\n# ' + meta['title'] + '\n\n' + body
    target = os.path.join(VAULT, meta['title'] + '.md')
    with open(target, 'w', encoding='utf-8') as fh:
        fh.write(out)
    return meta['title'], out.count('\n')

def main(argv):
    notes = {os.path.splitext(f)[0] for f in os.listdir(VAULT) if f.endswith('.md')}
    drafts = argv[1:] or sorted(glob.glob(os.path.join(DRAFTS, '*.md')))
    for d in drafts:
        if not os.path.isabs(d):
            d = os.path.join(DRAFTS, d)
        title, n = build(d, notes)
        print('ok  %-40s %5d líneas' % (title, n))

if __name__ == '__main__':
    main(sys.argv)
