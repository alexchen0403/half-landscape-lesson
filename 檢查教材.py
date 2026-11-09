"""確認公開版不夾帶受保護作品，且教學與四件作品入口完整。"""
from pathlib import Path
import json,re,subprocess,tempfile
root=Path(__file__).resolve().parent
text=(root/'index.html').read_text()
refs=json.loads((root/'課堂參考作品/list.json').read_text())
assert len(refs)==4 and len({r['image_url'] for r in refs})==4
assert text.count('class="work"')==4
assert all(r['image_url'].replace('&','&amp;') in text for r in refs)
assert 'data-full-image="data:image/' not in text
assert '@@' not in text
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=["\']https?://',text)
assert len(text.encode())<15_000_000
assert len(re.findall(r'data-reset="',text))==7
with tempfile.TemporaryDirectory() as d:
 script=Path(d)/'lesson.js'
 script.write_text(re.search(r'<script>(.*?)</script>',text,re.S)[1])
 subprocess.run(['node','--check',str(script)],check=True)
print('通過：四個不同作品入口、公開素材界線、離線依賴、檔案大小、七個重置入口及程式語法。')
