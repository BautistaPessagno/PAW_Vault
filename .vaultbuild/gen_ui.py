#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Genera los borradores de UI components, UI styles and tokens y Views and assets."""
import os, re, sys, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build, roadmap_hints as HN
REPO, COMMIT = build.REPO, build.COMMIT
W = 'webapp/src/main/webapp/'
def git(*a):
    return subprocess.run(['git', '-C', REPO] + list(a), capture_output=True, text=True, check=True).stdout
tracked = [t for t in git('ls-tree', '-r', '--name-only', COMMIT).split('\n') if t]
def show(p):
    return git('show', '%s:%s' % (COMMIT, p))
tags = sorted(t for t in tracked if t.startswith(W + 'WEB-INF/tags/'))
views = sorted(t for t in tracked if t.startswith(W + 'WEB-INF/views/'))
js = sorted(t for t in tracked if t.startswith(W + 'js/'))
css = [W + 'css/tokens.css', W + 'css/components.css', W + 'css/style.css']
imgs = sorted(t for t in tracked if t.startswith(W + 'images/'))
ctrl = {t: show(t) for t in tracked if '/webapp/controller/' in t or '/webapp/security/' in t or '/webapp/config/' in t}
src = {t: show(t) for t in tags + views}
name = lambda p: os.path.splitext(os.path.basename(p))[0]

def users_of(tag):
    n = name(tag)
    pat = re.compile(r'<ui:%s[\s/>]' % re.escape(n))
    return [p for p in tags + views if p != tag and pat.search(src[p])]
def short(p):
    return p.replace(W + 'WEB-INF/views/', '').replace(W + 'WEB-INF/tags/', '').replace('.jsp', '').replace('.tag', '')
def attrs(tag):
    return re.findall(r'<%@\s*attribute\s+name="([^"]+)"([^%]*)%>', src[tag])

# ---------------- UI components
o = []
o.append('''> [!summary] En una frase
> Las páginas no repiten HTML: se arman con %d componentes propios (tag files de JSP) que encapsulan el marcado, el escape de datos, las URL y los textos traducidos.

## Herramientas

| Herramienta | Para qué |
|---|---|
| Tag files (`WEB-INF/tags/*.tag`) | Componentes reutilizables escritos en JSP, sin clases Java |
| `<%%@ taglib prefix="ui" tagdir="/WEB-INF/tags" %%>` | Importarlos en una vista: `<ui:button .../>` |
| `<%%@ attribute %%>` | Declarar los parámetros de un componente, con tipo y obligatoriedad |
| `<jsp:doBody/>` | Insertar el contenido que la vista puso dentro del tag |
| JSTL `c:` | Condicionales, bucles, `c:out` y `c:url` |
| `spring:message` | Textos traducidos |
| `form:` de Spring | Campos ligados al formulario y sus errores |
| `sec:` de Spring Security | Mostrar u ocultar según la sesión y agregar el token CSRF |

## Reglas que cumplen todos

- **Sin scriptlets.** Solo tags y expresiones EL.
- **Todo dato se escapa** con `<c:out>` (o con los tags `form:`, que escapan solos). Es la defensa contra XSS: un nombre o una descripción con HTML se muestra como texto.
- **Toda URL pasa por `<c:url>`**, que antepone el context path. En el servidor de la cátedra la aplicación no cuelga de la raíz.
- **Ningún texto literal**: todo sale de `spring:message`.
- **Accesibilidad**: etiquetas asociadas a sus campos, `aria-describedby` para pistas y errores, `aria-current` en la navegación, iconos decorativos ocultos a lectores de pantalla.

## Catálogo

| Componente | Qué es | Atributos | Lo usan |
|---|---|---|---|''' % len(tags))
for t in tags:
    a = ', '.join('`%s`' % n for n, _ in attrs(t)) or '—'
    u = users_of(t)
    us = ', '.join(short(p) for p in u[:6]) + (' y %d más' % (len(u) - 6) if len(u) > 6 else '') if u else '—'
    o.append('| `%s` | %s | %s | %s |' % (name(t), HN.H.get(t, '').rstrip('.'), a, us))
o.append('''
"Lo usan" se calculó buscando `<ui:nombre` en las vistas y en los demás tags de `8929aea`.

## Decisiones y por qué

| Decisión | Motivo | Fuente |
|---|---|---|
| Tag files en vez de `include` | Parámetros con nombre y tipo; el componente no depende de variables sueltas de la página | Estructura del código; inferencia |
| El escape vive dentro del componente | Una vista no puede olvidarse del `c:out` si usa el tag | `CLAUDE.md` del repo |
| `button` acepta `href` (ruta) o `url` (ya resuelta) | Poder agregar parámetros o un ancla con `c:url` antes de pasarla | Comentario en `button.tag` |
| Lista cerrada de iconos | Un nombre desconocido no dibuja nada en vez de romper la página | Comentario en `icon.tag` |
| Controles ligados (`text-input`, `select`, `textarea`) y sin ligar (`input-control`, `select-control`) | Los ligados usan `form:` y muestran errores; los otros sirven fuera de un `form:form`, como el buscador | Atributos de cada tag |
| El estado se muestra con texto, no solo con color | Accesibilidad | Comentarios en `inquiry-status.tag` e `inquiry-nav.tag` |

## Preguntas de defensa

**¿Cómo evitan XSS en las vistas?**
Todo dato que viene de la base o de quien usa el sitio se imprime con `c:out` o con los tags `form:`, que escapan HTML. Los componentes lo hacen adentro.

**¿Por qué usan `c:url`?**
Porque antepone el context path. Con una URL escrita a mano la aplicación funcionaría en local y fallaría en el servidor.

**¿Qué es un tag file?**
Un fragmento JSP con atributos declarados que se usa como una etiqueta propia. Es la forma de tener componentes sin scriptlets ni clases Java.

**¿Dónde va el token CSRF?**
`form:form` lo agrega solo. Los formularios escritos con `<form>` lo agregan con `sec:csrfInput`.

## Código de cada componente
''')
for t in tags:
    o.append('### %s\n' % name(t))
    h = HN.H.get(t, '')
    if h: o.append(h + '\n')
    al = attrs(t)
    if al:
        o.append('Atributos: ' + ', '.join('`%s`%s' % (n, ' (obligatorio)' if 'required="true"' in rest else '') for n, rest in al) + '.\n')
    o.append('{{file:%s}}\n' % t)
draft = '@title: UI components\n@categories: Web\n@module: webapp\n@files: %s\n\n' % ', '.join(tags) + '\n'.join(o)
open(os.path.join(build.DRAFTS, 'UI components.md'), 'w', encoding='utf-8').write(draft)

# ---------------- Views and assets
def controllers_for(view):
    v = short(view)
    out = []
    for p, s in ctrl.items():
        if re.search(r'"%s"' % re.escape(v), s) or re.search(r'"/WEB-INF/views/%s' % re.escape(v), s):
            out.append(name(p))
    return sorted(out)
FLOW = {'auth': 'Authentication flow', 'cart': 'Cart flow', 'error': 'Validation and errors', 'inquiry': 'Inquiry and sale flow',
        'landing': 'Landing flow', 'publish': 'Publish flow'}
FLOWV = {'post/detail': 'Post detail flow', 'post/contact': 'Contact flow', 'profile/index': 'Profile flow', 'profile/public': 'Public profile flow',
         'auth/forgot-password': 'Password recovery flow', 'auth/reset-password': 'Password recovery flow'}
JSUSE = {'submit-once': 'Todas las páginas (lo carga `head.tag`)', 'catalog': 'Todas las páginas; actúa en el catálogo',
         'confirm-action': 'Todas las páginas; actúa donde hay `data-confirm-message`', 'autocomplete': 'Todas las páginas; actúa en el buscador y en el campo de artista',
         'post-gallery': 'Ficha (`pageScript`)', 'account-edit': 'Perfil privado (`pageScript`)', 'publish-preview': 'Publicar y editar (lo carga la propia vista)'}
o = []
o.append('''> [!summary] En una frase
> %d vistas JSP, %d scripts y %d imágenes: las vistas solo componen componentes y muestran lo que el controller dejó en el modelo, y cada script mejora algo que ya funciona sin JavaScript.

Los componentes compartidos están en [[UI components]] y los estilos en [[UI styles and tokens]].

## Cómo llega una vista al navegador

1. El controller devuelve un `ModelAndView` con un nombre lógico, por ejemplo `post/detail`.
2. El `viewResolver` lo convierte en `/WEB-INF/views/post/detail.jsp`. Al estar bajo `WEB-INF`, la JSP no se puede pedir directamente por URL.
3. La JSP lee el modelo con EL (`${post.title}` llama a `getTitle()`), compone tags `ui:` y escribe HTML.
4. `head.tag` enlaza los tres CSS y los scripts comunes con `defer`.

## Vistas

| Vista | Qué muestra | Controller | Flujo | Líneas |
|---|---|---|---|---|''' % (len(views), len(js), len(imgs)))
for v in views:
    s = short(v)
    flow = FLOWV.get(s) or FLOW.get(s.split('/')[0], '')
    o.append('| `%s` | %s | %s | %s | %d |' % (s, HN.H.get(v, '').rstrip('.'), ', '.join('[[%s]]' % c for c in controllers_for(v)) or '—',
             '[[%s]]' % flow if flow else '—', src[v].count('\n')))
o.append('''
"Controller" se calculó buscando el nombre lógico de la vista en las clases de `webapp`.

## Scripts

| Script | Qué hace | Dónde corre |
|---|---|---|''')
for j in js:
    o.append('| `%s` | %s | %s |' % (os.path.basename(j), HN.H.get(j, '').rstrip('.'), JSUSE.get(name(j), '')))
o.append('''
Todos son JavaScript sin dependencias ni framework, cargados con `defer`.

### Mejora progresiva

Cada script agrega comodidad sobre algo que ya anda con HTML y un POST:

| Sin JavaScript | Con JavaScript |
|---|---|
| El orden del catálogo se aplica con un botón | Se aplica al cambiar el select |
| El buscador envía el formulario | Ofrece sugerencias mientras se escribe |
| Un formulario destructivo se envía directo; el service valida estado y propiedad igual | Pide confirmación en un diálogo |
| Un doble clic podría enviar dos veces; el service lo resuelve con sus guardas | Los botones se deshabilitan al enviar |
| El perfil edita con enlaces y recargas | Las filas se abren y cierran en el lugar |
| En la ficha, cada miniatura es un enlace que abre esa foto | Las miniaturas cambian la foto principal sin salir de la página |

La seguridad nunca depende del script: confirmaciones y bloqueos de doble envío son comodidad; la regla está en el service.

## Imágenes

| Archivo | Uso |
|---|---|
| `images/logo.svg` | Isotipo y favicon |
| `images/covers/placeholder.svg` | Tapa cuando la publicación no tiene foto |

Las fotos subidas no son archivos: se guardan en la base y las sirve [[ImageController]] ([[Cover image flow]]).

## Preguntas de defensa

**¿Por qué las JSP están bajo `WEB-INF`?**
Para que solo se llegue a ellas a través de un controller, que arma el modelo y aplica la seguridad.

**¿Hay lógica en las vistas?**
Solo de presentación: condicionales y bucles de JSTL sobre datos ya resueltos. No hay scriptlets ni llamadas a services.

**¿Qué pasa si el navegador no tiene JavaScript?**
Todo funciona con formularios y enlaces. Los scripts solo mejoran la experiencia.

**¿Cómo evitan XSS en el JavaScript?**
Las sugerencias llegan como JSON y los nodos se arman con `textContent`, nunca con `innerHTML`.

## Código de las vistas
''')
for v in views:
    o.append('### %s\n' % short(v))
    h = HN.H.get(v, '')
    if h: o.append(h + '\n')
    o.append('{{file:%s}}\n' % v)
o.append('## Código de los scripts\n')
for j in js:
    o.append('### %s\n' % os.path.basename(j))
    o.append(HN.H.get(j, '') + '\n')
    o.append('{{file:%s}}\n' % j)
o.append('## Imágenes\n')
for i in imgs:
    o.append('### %s\n' % os.path.basename(i))
    o.append('{{file:%s}}\n' % i)
draft = '@title: Views and assets\n@categories: Web\n@module: webapp\n@files: %s\n\n' % ', '.join(views + js + imgs) + '\n'.join(o)
open(os.path.join(build.DRAFTS, 'Views and assets.md'), 'w', encoding='utf-8').write(draft)
print('tags', len(tags), 'views', len(views), 'js', len(js), 'imgs', len(imgs))
for v in views: print(short(v), controllers_for(v))
