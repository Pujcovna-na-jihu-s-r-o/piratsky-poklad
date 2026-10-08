# -*- coding: utf-8 -*-
"""Odhad genderu klipu z F0 + formantů (F1,F2 přes LPC). Diagnostika konzistence hlasu."""
import numpy as np, subprocess, os, io, json, sys
from scipy.linalg import solve_toeplitz
SR = 16000

def pcm(path):
    r = subprocess.run(['ffmpeg','-v','error','-i',path,'-ac','1','-ar',str(SR),'-f','s16le','-'], capture_output=True)
    return np.frombuffer(r.stdout, dtype=np.int16).astype(np.float64)/32768.0

def f0_frame(x, fmin=70, fmax=350):
    x = x - x.mean()
    ac = np.correlate(x, x, 'full')[len(x)-1:]
    if ac[0] <= 0: return None
    lo, hi = SR//fmax, SR//fmin
    seg = ac[lo:hi]
    if len(seg) == 0: return None
    k = int(np.argmax(seg)) + lo
    if ac[k] < 0.35*ac[0]: return None     # slabá periodicita → neznělé
    return SR/k

def formants(x, order=18):
    y = np.append(x[0], x[1:] - 0.97*x[:-1])   # pre-emfáze
    y = y * np.hamming(len(y))
    ac = np.correlate(y, y, 'full')[len(y)-1:len(y)+order]
    if ac[0] == 0: return []
    try:
        a = solve_toeplitz(ac[:order], -ac[1:order+1])
    except Exception:
        return []
    a = np.concatenate([[1.0], a])
    rts = np.roots(a)
    rts = rts[np.imag(rts) > 0]
    out = []
    for r in rts:
        f = np.arctan2(np.imag(r), np.real(r)) * SR/(2*np.pi)
        bw = -0.5 * SR/(2*np.pi) * np.log(np.abs(r) + 1e-9)
        if 90 < f < 4000 and bw < 400:
            out.append(f)
    return sorted(out)

def analyze_clip(path):
    x = pcm(path)
    if len(x) < SR//4: return None
    win, hop = int(0.025*SR), int(0.010*SR)
    f0s, f1s, f2s = [], [], []
    for i in range(0, len(x)-win, hop):
        fr = x[i:i+win]
        if np.sqrt(np.mean(fr*fr)) < 0.02: continue   # ticho
        f0 = f0_frame(fr)
        if f0 is None: continue                        # jen znělé rámce
        f0s.append(f0)
        fm = formants(fr)
        if len(fm) >= 1: f1s.append(fm[0])
        if len(fm) >= 2: f2s.append(fm[1])
    if len(f0s) < 3: return None
    med = lambda a: float(np.median(a)) if a else None
    return dict(f0=med(f0s), f1=med(f1s), f2=med(f2s), nvoiced=len(f0s))

def score(d):
    """Skóre ženskosti 0..1 (čím vyšší, tím ženštější). Práh ~0.5."""
    if not d: return None
    f0, f1 = d['f0'], d['f1'] or 0
    # logistická kombinace: ženy mají vyšší F0 i F1
    z = 0.045*(f0-150) + 0.006*(f1-500)
    return float(1/(1+np.exp(-z)))

def run(ids, audiodir='audio'):
    rows = []
    for i in ids:
        p = os.path.join(audiodir, i+'.mp3')
        if not os.path.exists(p): rows.append((i, None)); continue
        d = analyze_clip(p); rows.append((i, d))
    return rows

if __name__ == '__main__':
    for i, d in run(sys.argv[1:]):
        if d is None: print('%-16s  (bez dat)' % i); continue
        s = score(d)
        tag = 'ZENA' if s > 0.5 else 'muz'
        print('%-16s  F0=%3.0f  F1=%4.0f  F2=%4.0f  skore=%.2f  %s' % (i, d['f0'], d['f1'] or 0, d['f2'] or 0, s, tag))
