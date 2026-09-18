"""Regresiones del sistema base con Orca; requiere el servidor local en 8766."""
from check_browser import call,evaluate,save

def run():
 checks=[]
 def check(name,data,valid):
  checks.append({'name':name,'ok':bool(valid),'data':data});save('base.json',checks);assert valid,(name,data)
 call('goto','--url','http://127.0.0.1:8766/examples/generated/checks.html')
 call('exec','--command','set media light')
 for width,height in [(320,740),(390,844),(1639,939)]:
  call('exec','--command',f'set viewport {width} {height}')
  for theme in ['light','dark','sea']:
   evaluate('document.documentElement.dataset.theme='+repr(theme)+';true')
   data=evaluate('(()=>{const bar=document.querySelector(".barra"),last=bar.querySelector("nav button:last-child").getBoundingClientRect(),theme=bar.querySelector(".temas").getBoundingClientRect();return {width:document.documentElement.scrollWidth,barContent:bar.scrollWidth,overlap:last.right>theme.left,focus:bar.tabIndex,name:bar.getAttribute("aria-label")}})()')
   check(f'Barra {width}/{theme}',data,data['width']==width and not data['overlap'] and data['focus']==0 and data['name'])
  evaluate('document.querySelector("[data-ir=p2]").click();scrollTo({top:0,behavior:"instant"});true');call('screenshot')
  data=evaluate('(()=>{const page=document.querySelector(".pagina.viva"),p=page.querySelector("p").getBoundingClientRect(),f=page.querySelector(".amplio").getBoundingClientRect();return {width:document.documentElement.scrollWidth,text:p.width,figure:f.width,center:Math.abs(p.x+p.width/2-f.x-f.width/2),page:page.id,visible:[...document.querySelectorAll(".pagina")].filter(e=>e.getClientRects().length).length}})()')
  check(f'Página y rejilla {width}',data,data['width']==width and data['page']=='p2' and data['visible']==1 and data['center']<1 and data['figure']==min(1216,width-80 if width>1000 else width-40))
  evaluate('document.querySelector("[data-ir=p1]").click();scrollTo({top:0,behavior:"instant"});true')
 call('exec','--command','set viewport 1639 939')
 evaluate('scrollTo({top:document.getElementById("dos").getBoundingClientRect().top+scrollY-80,behavior:"instant"});true');call('screenshot')
 data=evaluate('[...document.querySelectorAll(".indice a")].map(a=>({href:a.hash,current:a.getAttribute("aria-current"),weight:getComputedStyle(a).fontWeight,visible:!!a.getClientRects().length}))')
 check('Índice sólo en la página viva',data,[a['href'] for a in data if a['current']]=='#dos'.split() and next(a for a in data if a['current'])['weight']=='600')
 data=evaluate('(async()=>{Object.defineProperty(navigator,"clipboard",{configurable:true,value:{writeText:async text=>window.textoCopiado=text}});const button=document.querySelector("[data-copiar]");button.click();await new Promise(r=>setTimeout(r,30));const success={icon:!!button.querySelector("svg"),status:document.querySelector(".terminal [role=status]").textContent,exact:textoCopiado===document.getElementById(button.dataset.copiar).textContent};navigator.clipboard.writeText=async()=>{throw new Error("denegado")};button.click();await new Promise(r=>setTimeout(r,30));return {success,fallback:document.querySelector(".terminal [role=status]").textContent,selected:getSelection().toString()===textoCopiado};})()')
 check('Copia terminal: éxito y denegación controlados',data,data['success']['icon'] and data['success']['exact'] and 'copiado' in data['success']['status'] and data['selected'] and 'seleccionado' in data['fallback'])
 call('goto','--url','http://127.0.0.1:8766/examples/generated/checks.html#p2')
 check('Enlace directo a capítulo',evaluate('document.querySelector(".pagina.viva").id'),evaluate('document.querySelector(".pagina.viva").id')=='p2')
 # Fixture efímera de rejilla por sección; no modifica el catálogo ni los archivos.
 evaluate('window.fixtureSeccion=document.createElement("main");fixtureSeccion.className="hoja por-seccion";fixtureSeccion.innerHTML="<section class=seccion><p>Medida de texto</p><figure class=ancho>Figura ancha</figure><figure class=amplio>Figura amplia</figure></section>";document.body.append(fixtureSeccion);true')
 for width,height in [(320,740),(390,844),(1639,939)]:
  call('exec','--command',f'set viewport {width} {height}')
  data=evaluate('[...fixtureSeccion.querySelector("section").children].map(e=>e.getBoundingClientRect().width)')
  expected=[560,992,1216] if width==1639 else [width-40]*3
  check(f'por-seccion {width}',data,data==expected)
 evaluate('fixtureSeccion.remove();true')
 call('goto','--url','http://127.0.0.1:8766/examples/generated/template.html')
 evaluate('scrollTo({top:document.getElementById("evidencia").getBoundingClientRect().top+scrollY-80,behavior:"instant"});true');call('screenshot')
 data=evaluate('[...document.querySelectorAll(".indice a[aria-current]")].map(a=>({href:a.hash,weight:getComputedStyle(a).fontWeight}))')
 check('Índice de página única sigue marcando',data,len(data)==1 and data[0]['href']=='#evidencia' and data[0]['weight']=='600')
 return checks

if __name__=='__main__':print(f'{len(run())} regresiones verificadas')
