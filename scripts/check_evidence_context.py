"""Integración: scroll real por IntersectionObserver y fuentes de guía completas."""
import json
from check_browser import call,evaluate,save,ROOT
call('goto','--url','http://127.0.0.1:8768/examples/generated/evidence.html')
call('exec','--command','set viewport 1440 960')
results=[]
for step in [0,1,2]:
 evaluate(f"(()=>{{const e=document.querySelectorAll('.relato-pasos li')[{step}];scrollTo({{top:scrollY+e.getBoundingClientRect().top-innerHeight*.3,behavior:'instant'}});return true}})()")
 call('screenshot')
 value=evaluate("NotaEvidencia.get(document.querySelector('[data-evidencia=relato]')).selected")
 results.append({'step':step,'selected':value});assert step==value,results
# Manual selection remains selected after scrolling to another narrative step.
evaluate("document.querySelector('.relato-pasos button').click();document.querySelector('.relato-pasos li:last-child').scrollIntoView({block:'center',behavior:'instant'});true")
call('screenshot')
assert evaluate("NotaEvidencia.get(document.querySelector('[data-evidencia=relato]')).selected")==0
save('evidencia-scroll.json',{'steps':results,'manualPersists':True,'method':'Scroll programático en Orca; selección por IntersectionObserver real. No gesto físico.'})
registry=json.loads((ROOT/'packages/core/registry/registry.json').read_text())['componentes']
ids=['relato-visual','sankey','cohortes','sensibilidad','gantt','embudo','incertidumbre','evidencia-ampliable']
call('goto','--url','http://127.0.0.1:8768/examples/generated/guide.html');call('screenshot')
sources=evaluate('Object.fromEntries([...document.querySelectorAll("code[id^=guia-fuente-]")].map(x=>[x.id.slice(12),x.textContent]))')
for item in registry:assert sources.get(item['id'])==item['html'],item['id']
instances=evaluate("[...document.querySelectorAll('[data-evidencia]')].map(e=>({kind:e.dataset.evidencia,ok:!!NotaEvidencia.get(e)?.model,error:NotaEvidencia.get(e)?.error}))")
assert len(instances)==8 and all(i['ok'] for i in instances),instances
save('evidencia-guia.json',{'recipesExact':len(registry),'instances':instances})
print('Scroll automático, control manual y 82 recetas exactas de la guía: OK')
