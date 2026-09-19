"""Resolve explicit project identity without network access or name-based guesses."""
from pathlib import Path
from urllib.parse import urlparse
from html import escape
import base64
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from brands import BRANDS
from themes import FAMILIES, MODES

FORMATS = ('document', 'chapters', 'presentation')
STYLES = ('editorial', 'sobrio', 'tecnico', 'libro', 'revista', 'bitacora')
OWNERS = {'liftitapp': 'liftit', 'tikinis': 'tikin', 'catabum-sas': 'catabum'}


def remote_identity(remote):
    """Only exact, documented GitHub organizations identify a company."""
    if remote.startswith('git@github.com:'):
        path = remote[len('git@github.com:'):]
    else:
        parsed = urlparse(remote)
        if parsed.hostname != 'github.com' or parsed.scheme not in ('https', 'ssh'):
            return {}
        path = parsed.path.lstrip('/')
    parts = path.removesuffix('.git').split('/')
    if len(parts) != 2 or not all(re.fullmatch(r'[\w.-]+', p) for p in parts):
        return {}
    owner, repo = parts
    result = {'project': {'id': (owner+'-'+repo).lower(), 'name': repo}, 'source': 'git-origin'}
    brand = OWNERS.get(owner.lower())
    if brand:
        result.update(company={'brand': brand, 'name': BRANDS[brand]['nombre']},
                      preferences={'theme': brand, 'mode': 'system', 'typography': 'sobrio', 'themePolicy': 'project'})
    return result


def validate_profile(profile):
    if not isinstance(profile, dict) or profile.get('version') != 1:
        raise ValueError('Project profile requires version: 1.')
    if set(profile) - {'version', 'project', 'company', 'preferences'}:
        raise ValueError('Unknown project profile field.')
    project = profile.get('project', {})
    if not isinstance(project, dict) or set(project) - {'id', 'name'}:
        raise ValueError('Project must contain only id and name.')
    for key, value in project.items():
        if not isinstance(value, str) or not value.strip() or len(value) > 120:
            raise ValueError('Invalid project '+key+'.')
    if project.get('id') and not re.fullmatch(r'[a-zA-Z0-9_-]+', project['id']):
        raise ValueError('Project id accepts letters, numbers, underscores and hyphens.')
    company = profile.get('company', {})
    if not isinstance(company, dict) or set(company) - {'brand', 'name', 'logo'}:
        raise ValueError('Company accepts brand, name and logo.')
    if company.get('brand') is not None and company['brand'] not in [*BRANDS, 'margen']:
        raise ValueError('Unknown company brand.')
    if 'name' in company and (not isinstance(company['name'], str) or not company['name'].strip() or len(company['name']) > 120):
        raise ValueError('Invalid company name.')
    if 'logo' in company:
        logos = company['logo']
        if not company.get('name') or company.get('brand'):
            raise ValueError('Custom logos require a company name and no registered brand.')
        if not isinstance(logos, dict) or set(logos) - {'light', 'dark'} or not logos.get('light') or not all(isinstance(v,str) and v for v in logos.values()):
            raise ValueError('Logo requires a light path and an optional dark path.')
    prefs = profile.get('preferences', {})
    if not isinstance(prefs, dict) or set(prefs) - {'theme','mode','typography','format','themePolicy'}:
        raise ValueError('Unknown project preference.')
    for key, allowed in [('theme',FAMILIES),('mode',MODES),('typography',STYLES),('format',FORMATS),('themePolicy',('project','reader'))]:
        if key in prefs and prefs[key] not in allowed:
            raise ValueError('Invalid project preference: '+key)
    return profile


def resolve(start, profile_path=None):
    start = Path(start).resolve()
    if not start.is_dir():
        raise ValueError('Project root must be an existing directory.')
    explicit = Path(profile_path).resolve() if profile_path else None
    if not explicit:
        for directory in [start, *start.parents]:
            candidate = directory / '.margen.json'
            if candidate.is_file():
                explicit = candidate
                break
            if (directory / '.git').exists():
                break
    if explicit:
        if explicit.stat().st_size > 32768:
            raise ValueError('Project profile exceeds 32 KB.')
        profile = validate_profile(json.loads(explicit.read_text()))
        brand=profile.get('company',{}).get('brand')
        defaults={'theme':brand,'mode':'system','typography':'sobrio','themePolicy':'project'} if brand in BRANDS else {}
        return {**profile, 'preferences':{**defaults,**profile.get('preferences',{})}, 'source': 'profile', '_root': explicit.parent}
    try:
        remote = subprocess.run(['git','-C',str(start),'config','--get','remote.origin.url'],capture_output=True,text=True,timeout=3,check=False)
        result = remote_identity(remote.stdout.strip()) if remote.returncode == 0 else {}
    except (OSError, subprocess.TimeoutExpired):
        result = {}
    return {**result, '_root': start}


def company_logo(company, root):
    """Embed a bounded local image. SVGs cannot contain executable or remote content."""
    images = []
    for mode in ('light','dark'):
        path = (Path(root) / company['logo'].get(mode,company['logo']['light'])).resolve()
        if not path.is_relative_to(Path(root).resolve()) or not path.is_file():
            raise ValueError('Company logo must be a file within the project profile directory.')
        blob = path.read_bytes()
        if len(blob) > 512000:
            raise ValueError('Company logo exceeds 500 KB.')
        if path.suffix.lower() == '.svg':
            if b'<!DOCTYPE' in blob.upper() or b'<!ENTITY' in blob.upper():
                raise ValueError('SVG entities are not supported.')
            try:
                svg = ET.fromstring(blob)
            except ET.ParseError:
                raise ValueError('Invalid SVG logo.') from None
            if svg.tag.rsplit('}',1)[-1] != 'svg':
                raise ValueError('Invalid SVG logo.')
            for node in svg.iter():
                if node.tag.rsplit('}',1)[-1] in ('script','foreignObject','style','image','use'):
                    raise ValueError('Logo SVG must be self-contained geometry.')
                for key,value in node.attrib.items():
                    if key.lower().startswith('on') or key.rsplit('}',1)[-1] == 'href' or re.search(r'url\(|javascript:|@import',value,re.I):
                        raise ValueError('Executable or referenced SVG content is not supported.')
            mime = 'image/svg+xml'
        elif blob.startswith(b'\x89PNG\r\n\x1a\n'):
            mime = 'image/png'
        elif blob.startswith(b'\xff\xd8\xff'):
            mime = 'image/jpeg'
        else:
            raise ValueError('Company logos support SVG, PNG or JPEG.')
        uri = 'data:'+mime+';base64,'+base64.b64encode(blob).decode()
        images.append('<img class="marca-logo marca-logo-'+mode+'" src="'+uri+'" alt="" width="140" height="32">')
    return '<span class="marca-firma" data-company-logo>'+''.join(images)+'<span class="sr-only">'+escape(company['name'])+'</span></span>'
