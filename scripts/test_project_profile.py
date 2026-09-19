"""Project discovery, precedence, portable branding and format regression tests."""
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from project_profile import resolve, remote_identity, company_logo, validate_profile
from contract_artifact import build, validate, Document, ROOT

class ProjectTests(unittest.TestCase):
    def test_exact_remote_organization(self):
        for url in ['git@github.com:Liftitapp/lms-web-app.git','https://github.com/Liftitapp/lms-web-app.git','ssh://git@github.com/Liftitapp/lms-web-app.git']:
            self.assertEqual(remote_identity(url)['company']['brand'],'liftit')
        for url in ['https://example.org/Liftitapp/demo','https://github.com/not-liftit/Liftitapp','https://github.com.evil.test/Liftitapp/demo']:
            self.assertNotIn('company',remote_identity(url))
    def test_nearest_profile_and_repository_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'.margen.json').write_text(json.dumps({'version':1,'project':{'id':'outer'}}))
            repo=root/'repo';repo.mkdir();(repo/'.git').mkdir();nested=repo/'docs';nested.mkdir()
            self.assertNotEqual(resolve(nested).get('project',{}).get('id'),'outer')
            (repo/'.margen.json').write_text(json.dumps({'version':1,'project':{'id':'inner','name':'Operations'},'company':{'brand':'liftit'}}))
            self.assertEqual(resolve(nested)['project']['id'],'inner')
    def test_custom_logo_bounds_and_embedded_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'logo.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"><path d="M0 0h10"/></svg>')
            company={'name':'Example & Co','logo':{'light':'logo.svg'}}
            html=company_logo(company,root);self.assertIn('data:image/svg+xml;base64,',html);self.assertIn('Example &amp; Co',html)
            for svg in ['<svg><script>alert(1)</script></svg>','<svg><path onclick="run()"/></svg>','<svg><image href="https://example.com/logo"/></svg>']:
                (root/'logo.svg').write_text(svg)
                with self.assertRaises(ValueError):company_logo(company,root)
            with self.assertRaises(ValueError):company_logo({'name':'No','logo':{'light':'../outside.svg'}},root)
    def test_english_config_profile_precedence_and_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'intro.html').write_text('<section id="point"><h2>Evidence</h2><p>Pending decision.</p></section>')
            (root/'.margen.json').write_text(json.dumps({'version':1,'project':{'id':'review','name':'Team review'},'company':{'brand':'tikin'},'preferences':{'theme':'tikin','mode':'dark','typography':'sobrio'}}))
            (root/'deck.json').write_text(json.dumps({'title':'Brief','document_id':'brief','format':'presentation','theme':'linear','pages':[{'id':'opening','title':'Decision','content':'intro.html'}]}))
            out=root/'out.html'
            subprocess.run(['python3',str(ROOT/'scripts/create_artifact.py'),'--config',str(root/'deck.json'),'--theme','blueprint','--output',str(out)],check=True,capture_output=True)
            html=out.read_text();self.assertEqual(validate(html),[])
            for value in ['name="nota-tema-inicial" content="blueprint"','data-marca="tikin"','name="margen-project-id" content="review"','name="margen-format" content="presentation"','data-presentation']:
                self.assertIn(value,html)
            self.assertNotIn(str(root),html)
            self.assertIn('packages/core/components/presentation.js',html)
    def test_profile_validation(self):
        for value in [{'version':2},{'version':1,'preferences':{'theme':'unknown'}},{'version':1,'company':{'logo':{'light':'a.svg'}}},{'version':1,'project':{'id':'../../x'}}]:
            with self.assertRaises(ValueError):validate_profile(value)
    def test_compact_brand_and_format_defaults(self):
        pages=[{'id':'intro','titulo':'Intro','html':'<p>Evidence.</p>'}]
        for mode in ['document','chapters','presentation']:
            html=build('Brief',pages,format=mode);self.assertEqual(validate(html),[])
            signature=next(n for n in Document(html).live if 'firma-editorial' in n.classes)
            self.assertEqual(signature.text(),'');self.assertIn('Margen',signature.attrs['aria-label'])
        with self.assertRaises(ValueError):build('Brief',pages+[{'id':'next','titulo':'Next','html':'<p>Decision.</p>'}],format='document')

if __name__=='__main__':unittest.main()
