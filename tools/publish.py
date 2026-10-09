"""Validate the data-only source tree and prepare one immutable icon release."""
import argparse, hashlib, json, math, re, struct, zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ASSET=re.compile(r'anip/icons/[a-f0-9]{64}\.(png|json)')

def commands(values):
    i=0;opened=False
    if not isinstance(values,list) or len(values)>100000:raise ValueError('Path size')
    while i<len(values):
        op=values[i];i+=1
        if type(op)!=int or op not in (0,1,2,3):raise ValueError('Path command')
        n={0:2,1:2,2:6,3:0}[op];points=values[i:i+n];i+=n
        if len(points)!=n or any(type(x) not in (int,float) or not math.isfinite(x) or abs(x)>4096 for x in points):raise ValueError('Path coordinate')
        if op==0:
            if opened:raise ValueError('Unclosed path')
            opened=True
        else:
            if not opened:raise ValueError('Unopened path')
            if op==3:opened=False
    if opened:raise ValueError('Unclosed path')

def build(revision):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}',revision):raise ValueError('Invalid release label')
    rules=json.loads((ROOT/'anip/index.json').read_text(encoding='utf8'))
    if not 1<=len(rules)<=2000:raise ValueError('Rules count')
    names={'anip/index.json'};checked=set()
    for pkg,rule in rules.items():
        if pkg!='android' and not re.fullmatch(r'[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+',pkg):raise ValueError('Package')
        asset,vector=rule['asset'],rule['vector']
        if not ASSET.fullmatch(asset) or not asset.endswith('.png') or vector!=asset[:-4]+'.json':raise ValueError('Asset reference')
        if not re.fullmatch(r'#[a-fA-F0-9]{6}',rule['color']) or type(rule['overlay'])!=bool:raise ValueError('Rule format')
        names.update((asset,vector))
        if vector in checked:continue
        checked.add(vector);png=(ROOT/asset).read_bytes();v=json.loads((ROOT/vector).read_text(encoding='utf8'))
        if len(png)<33 or not png.startswith(b'\x89PNG\r\n\x1a\n') or hashlib.sha256(png).hexdigest()!=v['source']:raise ValueError('PNG source mismatch')
        if struct.unpack('>II',png[16:24])!=(v['width'],v['height']):raise ValueError('PNG/vector size mismatch')
        if not 1<=v['width']<=1024 or not 1<=v['height']<=1024 or not 1<=len(v['layers'])<=4:raise ValueError('Vector shape')
        for layer in v['layers']:
            if not 1<=layer['alpha']<=255:raise ValueError('Vector alpha')
            commands(layer['path'])
        if 'desktopPath' in v:commands(v['desktopPath'])
        if 'notificationPath' in v:commands(v['notificationPath'])
    out=ROOT/'dist';out.mkdir(exist_ok=True);total=0
    with zipfile.ZipFile(out/'icons.zip','w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in sorted(names):
            raw=(ROOT/name).read_bytes();total+=len(raw)
            if len(raw)>1024*1024:raise ValueError('Entry limit')
            info=zipfile.ZipInfo(name,(2026,10,9,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
            z.writestr(info,raw,compresslevel=9)
    raw=(out/'icons.zip').read_bytes()
    if len(raw)>=4*1024*1024 or total>=16*1024*1024:raise ValueError('Runtime size limit')
    manifest={'schema':1,'revision':revision,'minApi':36,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
    (ROOT/'channel').mkdir(exist_ok=True)
    (ROOT/'channel/stable.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--revision',required=True)
    print(json.dumps(build(parser.parse_args().revision)))
