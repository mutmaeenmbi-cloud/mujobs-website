"""Render MuJobs' search-and-people logo mark as square website icons."""
from pathlib import Path
from io import BytesIO
import subprocess
from PIL import Image
root = Path(__file__).resolve().parents[1]
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="192" height="192" viewBox="0 0 192 192" role="img" aria-label="MuJobs">
<rect width="192" height="192" rx="28" fill="#fff"/>
<circle cx="82" cy="82" r="54" fill="#fff" stroke="#080909" stroke-width="16"/>
<path d="M122 122L161 161" fill="none" stroke="#080909" stroke-width="19" stroke-linecap="round"/>
<circle cx="56" cy="81" r="9" fill="#aab6bd"/>
<path d="M42 110V103C42 94 49 92 56 92C63 92 70 95 70 103V113Z" fill="#aab6bd"/>
<circle cx="108" cy="81" r="9" fill="#aab6bd"/>
<path d="M94 113V103C94 95 101 92 108 92C115 92 122 94 122 103V110Z" fill="#aab6bd"/>
<circle cx="82" cy="72" r="13" fill="#087cff"/>
<path d="M60 115V105C60 93 70 89 82 89C94 89 104 93 104 105V115C90 123 74 123 60 115Z" fill="#087cff" stroke="#fff" stroke-width="3"/>
</svg>'''
(root/'favicon.svg').write_text(svg+'\n')
for name,size in [('favicon.png',192),('icon-512.png',512),('apple-touch-icon.png',180)]:
 subprocess.run(['node', '-e', "const sharp=require(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES+'/sharp'); sharp(Buffer.from(require('fs').readFileSync(process.argv[1]))).resize(Number(process.argv[3]),Number(process.argv[3])).png().toFile(process.argv[2]).catch(e=>{console.error(e.message);process.exit(1)});", str(root/'favicon.svg'),str(root/name),str(size)], check=True)
im=Image.open(root/'icon-512.png').convert('RGBA')
im.save(root/'favicon.ico',format='ICO',sizes=[(16,16),(32,32),(48,48),(64,64)])
print('Rendered square PNG, SVG, ICO and Apple touch icons from the MuJobs logo mark.')
