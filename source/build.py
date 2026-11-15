import json,base64
t=open('template.html',encoding='utf-8').read()
packs=json.load(open('packs.json',encoding='utf-8'))
hero='data:image/webp;base64,'+base64.b64encode(open('hero.webp','rb').read()).decode()
t=t.replace('%%PACKS%%',json.dumps(packs,ensure_ascii=False,separators=(',',':'))).replace('%%HERO%%',hero)
open('tts-edu-crossword-challenge.html','w',encoding='utf-8').write(t)
print(len(t))
