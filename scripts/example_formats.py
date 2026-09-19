"""Generate a chapter report and a presentation with separate article and slide compositions."""
import json
from contract_artifact import ROOT, build
from project_profile import resolve

def generate():
    folder=ROOT/'examples/content/project-formats'
    project=resolve(folder)
    prefs=project['preferences']
    for format in ('chapters','presentation'):
        config=json.loads((folder/(format+'.json')).read_text())
        pages=[{'id':p['id'],'titulo':p['title'],'html':(folder/p['content']).read_text()} for p in config['pages']]
        result=build(config['title'],pages,config['description'],document_id=config['document_id'],format=format,project=project,theme=prefs['theme'],mode=prefs['mode'],style=prefs['typography'],theme_policy=prefs['themePolicy'])
        (ROOT/'examples/generated'/('project-'+format+'.html')).write_text(result)
    print('Generated project chapter and presentation examples.')

if __name__=='__main__':generate()
