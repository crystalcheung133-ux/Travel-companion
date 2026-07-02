import re, json, os
root='/mnt/data/v24work'
places=json.load(open(os.path.join(root,'GUIDE_CONTENT_AUDIT_v2.4.json')))
# Remove guide/modal sheets from watermark overflow:hidden group by overriding strongly and transparently
css=open(os.path.join(root,'styles.css')).read()
patch='''\n/* v2.4 safety: keep card/modals scrollable after watermark layer */\n.guide-sheet,.moments-sheet,.unexpected-sheet,.tools-sheet,.trip-sheet,.mama-sheet{overflow-y:auto!important;overflow-x:hidden!important;}\n.dash-card,.prose-block,.trip-card,.timeline-item,.day-summary a{overflow:visible!important;}\n'''
if 'v2.4 safety: keep card/modals scrollable' not in css:
    css += patch
open(os.path.join(root,'styles.css'),'w').write(css)
# Sync hours in day timeline p lines for items that have PLACES keys
for fname in ['day1.html','day2.html','day3.html','day4.html','day5.html']:
    path=os.path.join(root,fname)
    txt=open(path).read()
    def repl(m):
        key=m.group(1)
        block=m.group(2)
        h=places.get(key,{}).get('hours')
        if not h: return m.group(0)
        block2=re.sub(r'<p>🕘[^<]*</p>', f'<p>🕘 {h}</p>', block, count=1)
        return f'<div class="timeline-item" id="{key}">{block2}</div>'
    txt=re.sub(r'<div class="timeline-item" id="([^"]+)">(.*?)</div>\s*</div>', lambda m: repl(m), txt)
    open(path,'w').write(txt)
