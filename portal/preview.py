"""Vista estática y aislada; nunca ejecuta código al recorrer la galería."""
import html
import json
import re
from html.parser import HTMLParser

class Preview(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.parts=[]; self.skip=0; self.size=0; self.settings={}
    def handle_starttag(self, tag, attrs):
        if tag in ('script','iframe','object','audio','video','template'):
            self.skip+=1; return
        if self.skip or self.size>750000: return
        if tag=='meta':
            values=dict(attrs)
            if values.get('name') in ('nota-tema-inicial','nota-modo-inicial','nota-estilo-inicial'):
                self.settings[values['name']]=values.get('content','')
        if tag in ('base','meta','link'): return
        safe=[]
        for key,value in attrs:
            if key.startswith('on') or key in ('href','srcdoc','action','formaction','autofocus'): continue
            if key in ('src','poster','srcset') and (not (value or '').startswith('data:image/') or len(value)>100000): continue
            safe.append(key if value is None else key+'="'+html.escape(value,quote=True)+'"')
        self.add('<'+tag+(' '+' '.join(safe) if safe else '')+'>')
    def handle_endtag(self,tag):
        if tag in ('script','iframe','object','audio','video','template'):
            self.skip=max(0,self.skip-1);return
        if not self.skip:self.add('</'+tag+'>')
    def handle_data(self,data):
        if self.skip:return
        data=re.sub(r'@font-face\s*\{[^}]*\}', '', data, flags=re.I)
        self.add(data)
    def handle_entityref(self,name):
        if not self.skip:self.add('&'+name+';')
    def handle_charref(self,name):
        if not self.skip:self.add('&#'+name+';')
    def add(self,text):
        if self.size+len(text)>1000000:return
        self.parts.append(text);self.size+=len(text)

def preview_html(source,title):
    p=Preview();p.feed(source)
    result=''.join(p.parts)
    family=p.settings.get('nota-tema-inicial','')
    mode='dark' if p.settings.get('nota-modo-inicial')=='dark' else 'light'
    theme=family
    if family:
        match=re.search(r'\{[^{}]*"id"\s*:\s*"'+re.escape(family)+r'"[^{}]*\}',source)
        if match:
            try:theme=json.loads(match[0]).get(mode,family)
            except ValueError:pass
        attrs=' data-theme="'+html.escape(theme,quote=True)+'" data-estilo="'+html.escape(p.settings.get('nota-estilo-inicial','editorial'),quote=True)+'"'
        if re.search(r'<html\b',result,re.I):result=re.sub(r'<html\b[^>]*>','<html'+attrs+'>',result,count=1,flags=re.I)
        else:result='<html'+attrs+'>'+result+'</html>'
    override='<style>html{scroll-behavior:auto!important}body{pointer-events:none!important}*{animation:none!important;transition:none!important;caret-color:transparent!important}[data-reveal],.reveal,.animar{opacity:1!important;transform:none!important}dialog,iframe,audio,video,[role="dialog"],.nota-revision,.nota-regla,.nota-indice{display:none!important}</style>'
    # Las apps cuyo contenido depende de JS conservan una portada identificable.
    text=re.sub(r'<style\b[^>]*>.*?</style>','',result,flags=re.S|re.I)
    text=re.sub(r'<[^>]+>','',text).strip()
    if len(text)<40:result='<html><body style="padding:64px;background:#f8f5ef;color:#272520;font:32px Georgia"><small>DOCUMENTO INTERACTIVO</small><h1>'+html.escape(title)+'</h1><p>Abre el artefacto para explorar su contenido.</p></body></html>'
    return result+override
