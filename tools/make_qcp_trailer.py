"""Capture real QCP verdicts and render a music-driven 50-second portrait trailer.

python tools/make_qcp_trailer.py --music PATH
Requires Pillow, numpy, Playwright/Chromium, ffmpeg and ffprobe.
No fabricated verdicts, no external generation service.
"""
import argparse
import json
import math
import subprocess
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'qcp-demo'
ASSETS = OUT / 'assets'
OUT.mkdir(exist_ok=True)
ASSETS.mkdir(exist_ok=True)
W, H, FPS, DURATION = 1080, 1920, 24, 50
FONTROOT = Path('C:/Windows/Fonts')
INK = '#080e1c'
WHITE = '#f5f8ff'
BLUE = '#6da5ff'
GREEN = '#63edab'
RED = '#ff6876'


def font(size, bold=False, mono=False):
    return ImageFont.truetype(str(FONTROOT / ('consolab.ttf' if mono else 'arialbd.ttf' if bold else 'arial.ttf')), size)


def capture():
    catalog = json.loads((ROOT/'qcp-qollab/catalog.json').read_text(encoding='utf-8'))
    receipts = {}
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={'width':1100,'height':1250},device_scale_factor=1)
        page.goto('https://qcp-arena.vercel.app/#problem/bv')
        page.wait_for_selector('#code')

        def submit(source, key, action='submitCode'):
            page.locator('#code').fill(source)
            page.locator('#'+action).click()
            page.wait_for_selector('#result h2',timeout=120000)
            receipts[key] = json.loads(page.evaluate("localStorage.getItem('qcp-arena-1')"))['history'][-1]
            page.locator('#result').screenshot(path=str(ASSETS/(key+'.png')))

        wrong = catalog['problems'][0]['solution'].replace('    qc.x(n)\n','')
        page.locator('#code').fill(wrong)
        page.locator('.editor-panel').screenshot(path=str(ASSETS/'bad-code.png'))
        submit(wrong,'wrong')
        assert receipts['wrong']['status']=='WA'
        good = catalog['problems'][0]['solution']
        page.locator('#code').fill(good)
        page.locator('.editor-panel').screenshot(path=str(ASSETS/'good-code.png'))
        submit(good,'accepted')
        assert receipts['accepted']['status']=='AC'
        assert receipts['accepted']['result']['passed']==124
        page.get_by_text('Resource report',exact=True).click()
        page.locator('#result').screenshot(path=str(ASSETS/'resources.png'))
        page.goto('https://qcp-arena.vercel.app/#catalog')
        page.locator('#content').screenshot(path=str(ASSETS/'catalog.png'))
        page.goto('https://qcp-arena.vercel.app/#problem/grover')
        submit(catalog['problems'][2]['solution'],'grover','runCode')
        assert abs(receipts['grover']['result']['worst_success']-.9453125)<1e-10
        page.goto('https://qcp-arena.vercel.app/#contest')
        page.locator('#participant').fill('Demo competitor')
        page.locator('#startContest').click()
        page.goto('https://qcp-arena.vercel.app/#problem/bv')
        submit(wrong,'round-wa')
        submit(good,'round-ac')
        page.goto('https://qcp-arena.vercel.app/#contest')
        page.locator('#content').screenshot(path=str(ASSETS/'contest.png'))
        assert page.locator('tbody tr td').nth(2).inner_text()=='20'
        browser.close()
    (OUT/'receipts.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
    return receipts


def music_segment(path):
    raw = subprocess.run(['ffmpeg','-v','error','-i',str(path),'-f','s16le','-ac','1','-ar','8000','pipe:1'],capture_output=True,check=True).stdout
    samples = np.frombuffer(raw,dtype=np.int16).astype(np.float32)/32768
    block = 800
    padded = samples[:len(samples)//block*block].reshape(-1,block)
    rms = np.sqrt(np.mean(padded*padded,axis=1))
    count = int(DURATION*10)
    if len(rms)<=count: return 0, np.pad(rms,(0,max(0,count-len(rms))))
    means = np.convolve(rms,np.ones(count)/count,mode='valid')
    start = int(np.argmax(means))
    return start/10, rms[start:start+count]


def text(draw, value, y, size, color=WHITE, center=True, bold=True, x=72):
    face=font(size,bold)
    box=draw.textbbox((0,0),value,font=face)
    if center:x=(W-(box[2]-box[0]))/2
    draw.text((x,y),value,font=face,fill=color)


def fit_asset(name, width=920, maxheight=730):
    im=Image.open(ASSETS/(name+'.png')).convert('RGB')
    ratio=min(width/im.width,maxheight/im.height)
    return im.resize((round(im.width*ratio),round(im.height*ratio)),Image.Resampling.LANCZOS)


SCENES=[
    (0,4,'bad-code',['YOUR CIRCUIT','LOOKS RIGHT.'],'A hidden string. One oracle query.',BLUE),
    (4,8,'wrong',['WRONG','ANSWER.'],'The judge checks the probability.',RED),
    (8,14,'good-code',['FIX THE','MISSING GATE.'],'Prepare the target. Make phases matter.',BLUE),
    (14,20,'accepted',['124 / 124','ACCEPTED.'],'A real submission. Every tested secret.',GREEN),
    (20,25,'catalog',['3 PROBLEMS.','382 TEST CASES.'],'Recover. Decide. Search.',BLUE),
    (25,31,'resources',['FEWER','ORACLE QUERIES.'],'Query cost is separate from simulator speed.',BLUE),
    (31,36,'grover',['94.53125%','IDEAL SUCCESS.'],'Grover example: n = 3, two iterations.',GREEN),
    (36,41,'contest',['60 MINUTES.','YOUR NEXT ROUND.'],'Local virtual contest. Real penalties.',BLUE),
    (41,45,'accepted',['WRITE. SUBMIT.','UNDERSTAND.'],'Python practice + a Qiskit edition for Qollab.',GREEN),
    (45,50,None,['QCP','ARENA'],'Train in quantum algorithms.',BLUE),
]


def render(music, start, rms):
    assets={name:fit_asset(name) for _,_,name,_,_,_ in SCENES if name}
    # Pre-render clean background. Animation responds to the soundtrack without
    # fabricating activity in the recorded product UI.
    backdrop=Image.new('RGB',(W,H),INK)
    bd=ImageDraw.Draw(backdrop)
    for x in range(60,W,120):bd.line((x,0,x,H),fill='#101c30',width=1)
    for y in range(100,H,120):bd.line((0,y,W,y),fill='#101c30',width=1)
    faces={s:font(s,True) for s in (18,24,30,32,38,40,62,90,96,110,125)}
    outfile=OUT/'qcp-trailer-vertical.mp4'
    log=(OUT/'render.log').open('w',encoding='utf-8')
    command=['ffmpeg','-hide_banner','-loglevel','warning','-y','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0',
             '-ss',str(start),'-stream_loop','-1','-i',str(music),'-map','0:v:0','-map','1:a:0','-t',str(DURATION),
             '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-threads','4',
             '-c:a','aac','-b:a','192k','-af',f'volume=0.85,afade=t=in:st=0:d=0.4,afade=t=out:st={DURATION-2}:d=2',
             '-movflags','+faststart',str(outfile)]
    process=subprocess.Popen(command,stdin=subprocess.PIPE,stderr=log)
    rms_peak=max(float(np.percentile(rms,90)),.001)
    begin=time.time()
    for frame in range(DURATION*FPS):
        t=frame/FPS
        scene=next(s for s in SCENES if s[0]<=t<s[1])
        a,b,name,lines,caption,color=scene
        age=t-a; ease=min(1,age/.45);ease=1-(1-ease)**3
        pulse=min(1,float(rms[min(len(rms)-1,int(t*10))])/rms_peak)
        im=backdrop.copy();draw=ImageDraw.Draw(im)
        # Frame, audio waveform and a progress strip tie the cuts together.
        draw.rectangle((0,H-10,int(W*t/DURATION),H),fill=color)
        draw.rounded_rectangle((64,90,1016,140),radius=18,fill='#152640')
        draw.text((87,100),'QCP ARENA',font=faces[24],fill=WHITE)
        draw.text((820,104),'PRODUCT REEL',font=font(18),fill='#a9bbd4')
        if name:
            ytitle=236+int(32*(1-ease))
            size=90 if max(map(len,lines))>14 else 110
            for i,line in enumerate(lines):text(draw,line,ytitle+i*125,size,color if i==0 else WHITE)
            asset=assets[name]
            # Slow camera movement applies to the real screenshot as a whole.
            scale=1+.025*max(0,min(1,age/(b-a)))
            picture=asset.resize((int(asset.width*scale),int(asset.height*scale)),Image.Resampling.BICUBIC)
            x=(W-picture.width)//2;y=662+int(45*(1-ease))
            draw.rounded_rectangle((x-9,y-9,x+picture.width+9,y+picture.height+9),radius=16,fill=color)
            im.paste(picture,(x,y))
            draw=ImageDraw.Draw(im)
            text(draw,'Real product capture',y+picture.height+27,24,'#9aacc7',bold=False)
            # Legible explanatory caption, separate from the evidence image.
            words=caption.split();line='';wrapped=[]
            for word in words:
                trial=(line+' '+word).strip()
                if draw.textbbox((0,0),trial,font=font(38))[2]>920:wrapped.append(line);line=word
                else:line=trial
            wrapped.append(line)
            for i,line in enumerate(wrapped):text(draw,line,1540+i*56,38,WHITE,bold=False)
            text(draw,'Small ideal simulations · Public test suites',1722,26,'#9aacc7',bold=False)
        else:
            for i,line in enumerate(lines):text(draw,line,550+i*165,150,color if i==0 else WHITE)
            text(draw,caption,975,42,WHITE,bold=False)
            draw.rounded_rectangle((65,1130,1015,1270),radius=14,fill='#17365e',outline=BLUE,width=2)
            text(draw,'qcp-arena.vercel.app',1176,60,WHITE)
            text(draw,'OPEN IT. ATTEMPT PROBLEM A.',1390,34,WHITE)
            text(draw,'Browser practice · Qiskit package available',1480,27,'#a9bbd4',bold=False)
        for bar in range(30):
            amplitude=(.18+.82*abs(math.sin(t*4+bar*.73)))*pulse
            x=300+bar*16;height=9+amplitude*40
            draw.rounded_rectangle((x,1806-height/2,x+7,1806+height/2),radius=3,fill=color)
        # A short exposure dip separates scenes; avoid white flashes.
        if age<.10:
            shade=Image.new('RGB',(W,H),INK)
            im=Image.blend(shade,im,.45+.55*age/.10)
        process.stdin.write(im.tobytes())
        if frame%(FPS*5)==0:print(f'Render {t:.0f}/{DURATION}s; elapsed {time.time()-begin:.1f}s',flush=True)
        if frame in (int(17*FPS),int(47*FPS)):im.save(OUT/('poster.png' if frame==int(17*FPS) else 'end-card.png'))
    process.stdin.close()
    code=process.wait();log.close()
    if code:raise RuntimeError(f'ffmpeg failed with {code}; see {OUT / "render.log"}')
    return outfile


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--music',required=True,type=Path)
    args=parser.parse_args()
    if not args.music.is_file():raise FileNotFoundError(args.music)
    print('Capturing real public-product evidence…',flush=True)
    receipts=capture()
    start,rms=music_segment(args.music)
    print(f'Music starts at {start:.1f}s; render starts',flush=True)
    output=render(args.music,start,rms)
    info=json.loads(subprocess.run(['ffprobe','-v','error','-show_format','-show_streams','-of','json',str(output)],capture_output=True,text=True,check=True).stdout)
    assert abs(float(info['format']['duration'])-DURATION)<.2
    assert any(s['codec_type']=='audio' for s in info['streams'])
    assert next(s for s in info['streams'] if s['codec_type']=='video')['width']==W
    (OUT/'manifest.json').write_text(json.dumps({'url':'https://qcp-arena.vercel.app','duration':DURATION,'width':W,'height':H,'fps':FPS,'music_file':args.music.name,'music_offset_seconds':start,'execution_source':'Public browser Python subset + ideal simulator','receipts':'receipts.json','video':output.name},indent=2),encoding='utf-8')
    subtitles=[]
    def stamp(s):return f'00:00:{int(s):02d},000'
    for i,(a,b,_,lines,caption,_) in enumerate(SCENES,1):subtitles.append(f'{i}\n{stamp(a)} --> {stamp(b)}\n'+ ' '.join(lines)+'\n'+caption+'\n')
    (OUT/'captions.srt').write_text('\n'.join(subtitles),encoding='utf-8')
    (OUT/'README.md').write_text('# QCP Arena trailer\n\n50-second portrait reel, 1080×1920, H.264/AAC.\n\nMusic: supplied Epic Song.mp3, selected offset in manifest.json.\nReal captures from qcp-arena.vercel.app; receipts.json records the verdicts.\nAll text is English. The music-only trailer includes burned-in explanatory text.\n\nRebuild: python tools/make_qcp_trailer.py --music PATH\n\nThis is a short trailer, not the full 2–3 minute hackathon presentation.\n',encoding='utf-8')
    print(f'DONE: {output} ({output.stat().st_size/1e6:.1f} MB)',flush=True)


if __name__=='__main__':main()
