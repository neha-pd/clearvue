import json,sys
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];axe=ROOT.parents[1]/'reports/qa-tools/node_modules/axe-core/axe.min.js';results={}
with sync_playwright() as p:
 b=p.chromium.launch();page=b.new_page(viewport={'width':1440,'height':1050});base=sys.argv[1] if len(sys.argv)>1 else 'http://127.0.0.1:8871'
 for theme in ['light','dark']:
  page.emulate_media(color_scheme=theme);page.goto(base,wait_until='networkidle');page.evaluate("localStorage.removeItem('clearvue-theme')");page.reload(wait_until='networkidle');page.add_script_tag(path=str(axe))
  for component in ['book','file','payment','charts','chat','dialog']:
   names={'book':'Book flip','file':'File picker','payment':'Payment states','charts':'Chart studio','chat':'AI chat UI','dialog':'Dialog'};page.get_by_role('navigation',name='Choose a component').get_by_role('button',name=names[component]).click();page.wait_for_timeout(450)
   result=page.evaluate("async()=>{const r=await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}});return r.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))}");results[theme+'-'+component]=result
 b.close()
(ROOT/'artifacts/axe-redesign.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2));assert not any(results.values()),'Automated WCAG violations remain'
