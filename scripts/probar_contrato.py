"""Regresiones de composición y omisiones reales; no instala dependencias."""
import json,unittest,re
from contrato_artefacto import build,validate,Document,ROOT,recipe,THREE
class ContractTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.pages=[{'id':'inicio','titulo':'Inicio','html':'<section id="evidencia"><h2>Evidencia</h2><p>Una observación.</p></section>'}]
  cls.html=build('Informe',cls.pages)
 def test_single_and_multi(self):
  self.assertEqual(validate(self.html),[])
  multi=build('Informe',self.pages+[{'id':'detalle','titulo':'Detalle','html':recipe('barras')}])
  self.assertEqual(validate(multi),[]);self.assertIn('data-nota-sin-js',multi)
  self.assertIn('data-nota-modulo="graficas.js"',multi);self.assertIn('href="#evidencia"',multi)
 def test_missing_controls_fail(self):
  for attr in ['data-apariencia-menu','data-revision','data-audio-prueba','data-audio-volumen']:
   with self.subTest(attr=attr):self.assertTrue(validate(re.sub(' '+attr+r'(?=[\s>])', ' data-ausente',self.html,count=1)))
 def test_stale_sources_and_missing_module(self):
  self.assertTrue(validate(self.html.replace('data-nota-modulo="revision.js"','data-no-modulo="revision.js"')))
  self.assertTrue(validate(self.html.replace('/* Sonido central:', '/* Versión anterior:')))
 def test_each_chapter_needs_its_index(self):
  multi=build('Informe',self.pages+[{'id':'detalle','titulo':'Detalle','html':'<section id="dato"><h2>El dato</h2></section>'}])
  broken=re.sub(r'(<article class="pagina"[^>]*>.*?)(<nav class="indice".*?</nav>)',r'\1',multi,count=1,flags=re.S)
  self.assertNotEqual(multi,broken);self.assertTrue(validate(broken))
 def test_refs_and_grid(self):
  for html in ['<section><h2>Sin ID</h2></section>','<section id="x"><h2>Figura</h2><figure class="ancho">Atrapada</figure></section>','<p id="x">Uno</p><p id="x">Dos</p>','<a href="#fantasma">Ir</a>']:
   with self.subTest(html=html),self.assertRaises(ValueError):build('Mal',[{**self.pages[0],'html':html}])
 def test_registry_can_be_composed(self):
  items=json.loads((ROOT/'registro.json').read_text())['componentes']
  for item in items:
   if item['id'] in {'apariencia','revision'}:continue # La base los incorpora una sola vez.
   html=item['html']+(recipe('archivo') if item['id']=='configuracion' else '')
   with self.subTest(recipe=item['id']):
    result=build(item['nombre'],[{**self.pages[0],'html':html}]);self.assertEqual(validate(result),[])
    if THREE in item['dependencias']:self.assertEqual(result.count('<script src="'+THREE+'">'),1)
if __name__=='__main__':unittest.main()
