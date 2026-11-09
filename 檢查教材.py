"""確認六件作品皆已內嵌，來源、放大入口及教學互動完整。"""
from pathlib import Path
import json,re,subprocess,tempfile
root=Path(__file__).resolve().parent
text=(root/'index.html').read_text()
refs=json.loads((root/'課堂參考作品/list.json').read_text())
assert len(refs)==6 and len({r['file'] for r in refs})==6
assert text.count('class="work"')==6
assert all(r['source'].replace('&','&amp;') in text for r in refs)
assert text.count('data-full-image="data:image/')==6
assert text.count('<img src="data:image/')==6
assert len(set(re.findall(r'<img src="(data:image/[^\"]+)"',text)))==6
assert '@@' not in text
assert not re.search(r'<(?:script|link)[^>]+(?:src|href)=["\']https?://',text)
assert len(text.encode())<15_000_000
assert len(re.findall(r'data-reset="',text))==8
with tempfile.TemporaryDirectory() as d:
 script=Path(d)/'lesson.js'
 script.write_text(re.search(r'<script>(.*?)</script>',text,re.S)[1])
 subprocess.run(['node','--check',str(script)],check=True)
print('通過：六張不同內嵌作品、六個放大入口、來源、離線依賴、檔案大小、八個重置入口及程式語法。')
