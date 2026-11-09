"""組成本機課堂版與 GitHub 公開版；第三方作品圖片不寫進公開版。"""
from pathlib import Path
import base64,html,json,subprocess,tempfile
ROOT=Path(__file__).resolve().parent
SKILL=Path('/Users/pinhechen/.codex/skills/art-lesson-prep')
records=json.loads((ROOT/'課堂參考作品/list.json').read_text())
assert len(records)>=4
src=(ROOT/'教材底稿.html').read_text()
# Reviewed pronunciations: 著=˙ㄓㄜ、還=ㄏㄞˊ、個=˙ㄍㄜ、處=ㄔㄨˋ、稱=ㄔㄣˋ。
for a,b in [('著','著\U000e01e2'),('還','還\U000e01e1'),('個','個\U000e01e1'),('兩處','兩處\U000e01e1'),('對稱','對稱\U000e01e1'),('放得下','放得\U000e01e1下'),('接得','接得\U000e01e1')]:
 src=src.replace(a,b)
def gallery(local):
 cards=[]
 for i,r in enumerate(records[:4],1):
  e=lambda key:html.escape(r[key],quote=True)
  if local:
   data=base64.b64encode((ROOT/'課堂參考作品'/r['file']).read_bytes()).decode()
   mime='image/png' if r['file'].endswith('.png') else 'image/jpeg'
   uri=f'data:{mime};base64,{data}'
   visual=f'<button data-full-image="{uri}" aria-label="放大作品{i}"><img src="{uri}" alt="{e("title")}：照片與繪畫延伸作品"></button>'
  else:
   visual=f'<a class="placeholder" href="{e("image_url")}" target="_blank" rel="noopener noreferrer" aria-label="開啟作品{i}原圖">看作品 {i:02d} ↗</a>'
  cards.append(f'<article class="work">{visual}<h3>{i:02d} {e("title")}</h3><p>{e("idea")}</p><p class="photo-credit">{e("credit")}</p><div class="teacher-links"><a href="{e("image_url")}" target="_blank" rel="noopener noreferrer">開原作大圖 ↗</a><a href="{e("source")}" target="_blank" rel="noopener noreferrer">來源網頁 ↗</a></div></article>')
 mode='點圖片放大，一起找照片與接畫的交界。' if local else '四件真實作品，點選開原作大圖；需要網路。'
 return '<section class="unit leaf gallery-unit" data-u="6"><h2>四種風景，四種接法</h2><p class="lead">'+mode+'</p><div class="gallery">'+''.join(cards)+'</div><p class="tip">前兩件為教學網站示例；後兩件為 Antoine Doly 藝術家作品。中文為觀察標題。<br>照片向四周延伸，也是在練習接線與接色；不必照抄精細程度。</p></section>'
with tempfile.TemporaryDirectory() as tmp:
 for local,target in [(False,ROOT/'index.html'),(True,ROOT.parent/'貼一半畫一半-互動教材.html')]:
  draft=Path(tmp)/('local.html' if local else 'public.html')
  draft.write_text(src.replace('<!--@@GALLERY@@-->',gallery(local)))
  subprocess.run([str(SKILL/'.venv/bin/python3'),'-I',str(SKILL/'assets/互動教材範本/組裝.py'),str(draft),str(target),str(ROOT/'參考素材')],check=True)
print('公開版只含四件作品原站連結；課堂離線版含四件成品圖片。')
