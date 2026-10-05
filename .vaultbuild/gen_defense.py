#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build
ORDER = [
 ('Cuenta y seguridad', ['Authentication flow', 'Tokens and email links', 'Password recovery flow', 'Security and authorization']),
 ('Correo', ['Mail delivery']),
 ('Venta', ['Inquiry and sale flow', 'Contact flow', 'Conversation flow', 'Reviews flow', 'Cart flow', 'Addresses and payment flow']),
 ('Catálogo y publicaciones', ['Landing flow', 'Search suggestions flow', 'Post detail flow', 'Publish flow', 'Edit and delete flow', 'Cover image flow', 'Gallery flow']),
 ('Perfiles', ['Profile flow', 'Public profile flow']),
 ('Arquitectura y datos', ['Domain and identity', 'Architecture', 'Startup and dependency injection', 'Database schema', 'Schema history and seeds', 'Transactions and concurrency', 'Validation and errors', 'Paginated listings', 'Status filters flow']),
 ('Interfaz', ['UI components', 'UI styles and tokens', 'Views and assets']),
 ('Operación', ['Build and dependencies', 'Configuration and running', 'Localization', 'Logging', 'Testing and evidence']),
]
out = []; total = 0; used = set()
for theme, notes in ORDER:
    out.append('\n### %s\n' % theme)
    for n in notes:
        p = os.path.join(build.VAULT, n + '.md')
        s = open(p, encoding='utf-8').read()
        m = re.search(r'^## Preguntas de defensa\n(.*?)(?=^## )', s, re.S | re.M)
        if not m:
            raise SystemExit('sin preguntas: ' + n)
        qs = re.findall(r'^\*\*(¿.*?)\*\*\s*$', m.group(1), re.M)
        if not qs:
            raise SystemExit('sin preguntas en formato: ' + n)
        used.add(n); total += len(qs)
        out.append('**[[%s#Preguntas de defensa|%s]]**\n' % (n, n))
        out.extend('- %s' % q for q in qs)
        out.append('')
SKIP = {'Defense guide', 'Note template', 'AGENTS', 'CLAUDE'}
others = sorted(f[:-3] for f in os.listdir(build.VAULT) if f.endswith('.md') and f[:-3] not in used and f[:-3] not in SKIP
                and re.search(r'^## Preguntas de defensa', open(os.path.join(build.VAULT, f), encoding='utf-8').read(), re.M))
if others:
    raise SystemExit('notas con preguntas fuera del índice: %s' % others)
intro = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defense_intro.md'), encoding='utf-8').read()
draft = '@title: Defense guide\n@categories: Navigation, Testing\n@tags: codemap, navigation\n\n' + intro + '\n'.join(out) + '\n\nTotal: %d preguntas en %d notas.\n' % (total, len(used))
open(os.path.join(build.DRAFTS, 'Defense guide.md'), 'w', encoding='utf-8').write(draft)
print('preguntas', total, 'notas', len(used))
