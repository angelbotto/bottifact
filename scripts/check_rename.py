"""Continuidad real del store al cambiar marca en un documento sin ID explícito."""
import re,uuid
from html import escape
from check_browser import ROOT,call,evaluate,save
from contract_artifact import build
file=ROOT/'tests/evidence/renombre-prueba.html';url='http://127.0.0.1:8768/tests/evidence/renombre-prueba.html'
old_title='Nota Tikin · Prueba '+uuid.uuid4().hex
source=build(old_title,[{'id':'lectura','titulo':'Lectura','html':'<section id="idea"><h2>Una decisión</h2><p id="parrafo">Esta observación mantiene su contexto.</p></section>'}])
source=re.sub(r'<meta name="nota-documento"[^>]*>','',source)
try:
 file.write_text(source);call('goto','--url',url)
 evaluate('''(()=>{document.querySelector('.revision-barra [data-revision-modo]').click();document.querySelector('#parrafo').click();const i=document.querySelector('[data-revision-texto]');i.value='Conservar esta observación durante el cambio de marca.';i.dispatchEvent(new Event('input'));document.querySelector('[data-revision-guardar]').click();return true})()''')
 before=evaluate('NotaRevision.get(document.querySelector("[data-revision]")).exportData()')
 file.write_text(source.replace('<title>'+escape(old_title)+'</title>','<title>Margen · Prueba</title><meta name="nota-titulo-anterior" content="'+escape(old_title,quote=True)+'">'))
 call('goto','--url',url)
 after=evaluate('NotaRevision.get(document.querySelector("[data-revision]")).exportData()')
 comments=evaluate('NotaRevision.get(document.querySelector("[data-revision]")).comments')
 assert before==after and len(comments)==1 and 'Conservar esta observación' in comments[0]['text'],comments
 save('bottifact-continuity.json',{'documento_legacy_recuperado':True,'eventos_iguales':before==after,'comentarios':len(comments),'metodo':'Crear con título anterior y sin ID explícito, renombrar, recargar y comparar exportación.'})
 print('Cambio de marca: comentario y eventos completos recuperados tras recargar.')
finally:
 evaluate('''(()=>{const old=document.querySelector('meta[name="nota-titulo-anterior"]')?.content||document.title;const prefix='nota-revision-v2:'+encodeURIComponent(old+'@'+location.pathname)+':';Object.keys(localStorage).filter(k=>k.startsWith(prefix)).forEach(k=>localStorage.removeItem(k));return true})()''')
 file.unlink(missing_ok=True);call('goto','--url','http://127.0.0.1:8768/examples/generated/system.html')
