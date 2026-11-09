"""組成含六件兒童作品圖片的單檔教材，公開版與本機版內容一致。"""
from pathlib import Path
import base64,html,json,subprocess,tempfile
ROOT=Path(__file__).resolve().parent
SKILL=Path('/Users/pinhechen/.codex/skills/art-lesson-prep')
records=json.loads((ROOT/'課堂參考作品/list.json').read_text())
assert len(records)>=6
src=(ROOT/'教材底稿.html').read_text()
# Reviewed pronunciations: 著=˙ㄓㄜ、還=ㄏㄞˊ、個=˙ㄍㄜ、處=ㄔㄨˋ、稱=ㄔㄣˋ。
for a,b in [('著','著\U000e01e2'),('還','還\U000e01e1'),('個','個\U000e01e1'),('兩處','兩處\U000e01e1'),('對稱','對稱\U000e01e1'),('放得下','放得\U000e01e1下'),('接得','接得\U000e01e1')]:
 src=src.replace(a,b)
def gallery():
 cards=[]
 for i,r in enumerate(records[:6],1):
  e=lambda key:html.escape(r[key],quote=True)
  data=base64.b64encode((ROOT/'課堂參考作品'/r['file']).read_bytes()).decode()
  uri=f'data:image/jpeg;base64,{data}'
  visual=f'<button data-full-image="{uri}" aria-label="放大作品{i}"><img src="{uri}" alt="{e("title")}：國小學生風景作品"></button>'
  cards.append(f'<article class="work">{visual}<h3>{e("title")}</h3><p>{e("idea")}</p><p class="photo-credit">{e("style")} · <a href="{e("source")}" target="_blank" rel="noopener noreferrer">{e("credit")}</a></p></article>')
 return '<section class="unit leaf gallery-unit" id="gallery" data-u="6"><h2>別的小朋友怎麼畫？</h2><p class="lead">點圖片放大，看看線條和顏色。</p><div class="gallery">'+''.join(cards)+'</div><p class="tip">作品版權屬原作者，僅供課堂參考。</p></section>'
with tempfile.TemporaryDirectory() as tmp:
 for local,target in [(False,ROOT/'index.html'),(True,ROOT.parent/'貼一半畫一半-互動教材.html')]:
  draft=Path(tmp)/('local.html' if local else 'public.html')
  spm='data:image/jpeg;base64,'+base64.b64encode((ROOT/'課堂參考作品/sun-pei-mao-coiled-dragon.jpg').read_bytes()).decode()
  draft.write_text(src.replace('<!--@@GALLERY@@-->',gallery()).replace('@@SPM_IMAGE@@',spm))
  subprocess.run([str(SKILL/'.venv/bin/python3'),'-I',str(SKILL/'assets/互動教材範本/組裝.py'),str(draft),str(target),str(ROOT/'參考素材')],check=True)
print('公開版與課堂離線版皆已內嵌六件兒童作品，可直接點圖放大。')
