#!/usr/bin/env python3
"""Regenera las notas de codigo (una por archivo Java) desde los objetos Git."""
import os, re, sys, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import summaries, build

HOME = build.HOME; REPO = build.REPO; VAULT = build.VAULT
ABS = build.ABS
COMMIT = build.COMMIT; SHORT = COMMIT[:7]; SNAPSHOT = build.SNAPSHOT
# Commit anterior del vault: las clases que existian ahi y ya no existen quedan como notas historicas.
OLD = os.environ.get('PAW_OLD_COMMIT', '8929aeaa59b250e6c7119212f96437e153e815ac')
KEYWORDS = {'if', 'for', 'while', 'switch', 'return', 'new', 'catch', 'throw', 'else', 'super', 'this', 'try', 'do', 'case', 'assert', 'synchronized'}

def git(*args):
    return subprocess.run(['git', '--no-optional-locks', '-C', REPO] + list(args), capture_output=True, text=True, check=True).stdout

def strip_code(src):
    """Sin comentarios ni literales, para contar referencias lexicas reales."""
    out = re.sub(r'/\*.*?\*/', ' ', src, flags=re.S)
    out = re.sub(r'"(?:\\.|[^"\\\n])*"', '""', out)
    out = re.sub(r"'(?:\\.|[^'\\\n])'", "''", out)
    out = re.sub(r'//[^\n]*', ' ', out)
    return out

def fields_of(code):
    names = []
    for m in re.finditer(r'(?m)^[ \t]+(?:private|protected|public|static)\s+(?:(?:static|final|volatile|transient)\s+)*[\w.<>\[\], ?]+?\s+(\w+)\s*(?:=|;)', code):
        if m.group(1) not in names:
            names.append(m.group(1))
    return names

def methods_of(code):
    names = []
    pat = r'(?m)^[ \t]+(?:(?:public|private|protected|static|final|abstract|default|synchronized)\s+)*(?:<[\w, ?]+>\s+)?(?:[\w.]+(?:<[^()\n]*?>)?(?:\[\])*)\s+(\w+)\s*\('
    for m in re.finditer(pat, code):
        n = m.group(1)
        first = m.group(0).strip().split()[0]
        if n in KEYWORDS or first in KEYWORDS or first.startswith('@'):
            continue
        if n not in names:
            names.append(n)
    return names

def tests_of(src):
    return re.findall(r'@(?:Test|ParameterizedTest)\b[^{;]*?\bvoid\s+(\w+)\s*\(', src, flags=re.S)

def default_categories(path, is_test):
    module = path.split('/')[0]
    base = {'models': 'Domain', 'persistence-contracts': 'Persistence', 'persistence': 'Persistence',
            'services-contracts': 'Services', 'services': 'Services', 'webapp': 'Web'}[module]
    return [base, 'Testing'] if is_test else [base]

def existing_categories(name):
    p = os.path.join(VAULT, name + '.md')
    if not os.path.exists(p):
        return None
    t = open(p, encoding='utf-8').read()
    if not re.search(r'^type: "(code|test)"', t, re.M) or re.search(r'^status: "historical"', t, re.M):
        return None
    m = re.search(r'^categories: (\[.*\])$', t, re.M)
    return json.loads(m.group(1)) if m else None

def main():
    paths = [p for p in git('ls-tree', '-r', '--name-only', COMMIT).split('\n') if p.endswith('.java')]
    name_of = {p: os.path.basename(p)[:-5] for p in paths}
    all_names = sorted(name_of.values())
    src = {p: git('show', COMMIT + ':' + p) for p in paths}
    code = {p: strip_code(src[p]) for p in paths}
    refs = {}
    token = re.compile(r'[A-Za-z_]\w*')
    for p in paths:
        used = set(token.findall(code[p]))
        refs[name_of[p]] = sorted(n for n in all_names if n in used and n != name_of[p])
    rev = {n: [] for n in all_names}
    for n, lst in refs.items():
        for r in lst:
            rev[r].append(n)
    q = lambda s: json.dumps(s, ensure_ascii=False)
    written = 0
    for p in paths:
        name = name_of[p]; is_test = '/src/test/' in p; module = p.split('/')[0]
        cats = existing_categories(name) or default_categories(p, is_test)
        lines = src[p].rstrip('\n').split('\n')
        cases = tests_of(src[p]) if is_test else []
        if is_test and name not in ('TestConfiguration', 'InMemoryImageService'):
            summary = 'Tests de `%s` en `%s`: %d casos declarados. Cubre: %s No se ejecutaron en esta actualización del Vault; ver [[Testing and evidence]].' % (
                name[:-4] if name.endswith('Test') else name, module, len(cases), summaries.T[name][0].lower() + summaries.T[name][1:])
        else:
            summary = summaries.T.get(name) or summaries.S[name]
        out = ['---', 'title: ' + q(name), 'categories: [' + ', '.join(q(c) for c in cats) + ']',
               'type: ' + q('test' if is_test else 'code'), 'module: ' + q(module), 'project: "quieroVinilos"',
               'snapshot: ' + q(SNAPSHOT), 'commit: ' + q(COMMIT), 'status: "documented"',
               'sources: [' + q(p) + ']', '---', '', '# ' + name, '', summary, '', '## Guía de lectura', '']
        fl = fields_of(code[p]); ml = [m for m in methods_of(code[p]) if m != name and m not in cases]
        if fl:
            out += ['Datos y dependencias declaradas: ' + ', '.join('`%s`' % f for f in fl) + '.', '']
        if ml:
            out += ['Operaciones para localizar en la fuente: ' + ', '.join('`%s`' % m for m in ml) + '.', '']
        if not fl and not ml:
            out += ['Sin campos ni métodos propios: el archivo completo está abajo.', '']
        if is_test:
            out += ['Casos declarados: %d.' % len(cases), '']
            if cases:
                out += ['- `%s`' % c for c in cases] + ['']
        out += ['## Conexiones', '',
                'Referencias estáticas a tipos del proyecto: ' + (', '.join('[[%s]]' % r for r in refs[name]) if refs[name] else 'ninguna') + '.', '',
                'Referenciado por: ' + (', '.join('[[%s]]' % r for r in sorted(rev[name])) + '.' if rev[name] else 'sin referencias léxicas desde otros archivos Java.'), '',
                'Las conexiones se calculan sobre el código sin comentarios ni literales. No incluyen resolución dinámica de Spring, JSP ni un grafo de ejecución.', '',
                '## Fuente completa', '',
                'Fuente exacta en `%s`: [%s](<%s/%s>), líneas 1–%d.' % (SHORT, p, ABS, p, len(lines)), '',
                '```java', '\n'.join(lines), '```', '']
        with open(os.path.join(VAULT, name + '.md'), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(out))
        written += 1
    print('notas de código escritas:', written)
    # clases que dejaron de existir entre los dos commits: quedan como historicas
    old_paths = [p for p in git('ls-tree', '-r', '--name-only', OLD).split('\n') if p.endswith('.java')]
    gone = [p for p in old_paths if os.path.basename(p)[:-5] not in all_names]
    renamed = {'ContactFormValidator': 'Fue renombrado a [[ShippingAddressValidator]] cuando el carrito empezó a compartir el formulario de dirección.',
               'ValidContactForm': 'Fue renombrada a [[ValidShippingAddress]] cuando el carrito empezó a compartir el formulario de dirección.'}
    for p in gone:
        name = os.path.basename(p)[:-5]; module = p.split('/')[0]
        old_src = git('show', OLD + ':' + p).rstrip('\n'); n = len(old_src.split('\n'))
        out = ['---', 'title: ' + q(name), 'categories: ["History"]', 'type: "code"', 'module: ' + q(module),
               'project: "quieroVinilos"', 'snapshot: ' + q(SNAPSHOT), 'commit: ' + q(OLD), 'status: "historical"',
               'sources: [' + q(p) + ']', '---', '', '# ' + name, '',
               '> Histórico. Este archivo ya no existe con ese nombre en `%s`. El código inferior conserva su revisión en `%s`. %s' % (SHORT, OLD[:7], renamed.get(name, '')), '',
               '## Fuente completa', '',
               'Fuente exacta en `%s`: `%s`, líneas 1–%d.' % (OLD[:7], p, n), '', '```java', old_src, '```', '']
        with open(os.path.join(VAULT, name + '.md'), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(out))
        print('histórica:', name)

if __name__ == '__main__':
    main()
