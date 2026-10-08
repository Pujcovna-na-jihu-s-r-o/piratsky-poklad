# -*- coding: utf-8 -*-
"""Přegeneruje žensky znějící klipy průvodce na mužský hlas: generuj → změř gender → opakuj,
dokud skóre < TARGET (jasně muž). Bere klipy od nejvíc ženských. Rotuje modely, přeskakuje
vyčerpané (429/den), průběžně loguje a ukládá postup → dá se kdykoli znovu spustit."""
import io, json, os, sys, time, shutil
import gemini_tts as g
import gender

TARGET     = 0.40     # přijmout, když skóre < TARGET (jasně muž)
ACCEPT_MAX = 0.50     # i nejlepší pokus přepíše originál jen pokud je pod tímhle (jinak nechat být)
PROC_ABOVE = 0.55     # zpracovat klipy se skóre nad tímhle (sestupně, nejvíc ženské první)
MAXTRY     = 6        # max pokusů na klip
SLEEP      = 1.5
MODELS = ['gemini-3.1-flash-tts-preview', 'gemini-2.5-flash-preview-tts', 'gemini-2.5-pro-preview-tts']

HERE = os.path.dirname(os.path.abspath(__file__))
def P(*a): os.path.join(HERE, *a)

key = g.load_key()
man = {it['id']: it for it in json.load(io.open(os.path.join(HERE,'manifest.json'), encoding='utf-8'))}
scores = json.load(io.open(os.path.join(HERE,'gender-scores.json')))          # [[id,score],...] sestupně
orig = {i: s for i, s in scores}
targets = [i for i, s in scores if s > PROC_ABOVE]

prog_path = os.path.join(HERE, 'regen-progress.json')
done = {}
if os.path.exists(prog_path):
    try: done = json.load(io.open(prog_path))
    except Exception: done = {}

logf = io.open(os.path.join(HERE,'regen-log.txt'), 'a', encoding='utf-8')
def log(m):
    line = time.strftime('%H:%M:%S ') + m
    print(line); logf.write(line+'\n'); logf.flush()

dead = set()
tmp = os.path.join(HERE, 'tmp_regen.mp3')
log('=== START, cilu: %d (skore>%.2f), uz hotovo: %d ===' % (len(targets), PROC_ABOVE, len(done)))

fixed = partial = 0
for n, cid in enumerate(targets, 1):
    if cid in done:  # z dřívějšího běhu
        continue
    it = man[cid]
    best_score = 9.0; best_file = None
    tries = 0
    while tries < MAXTRY:
        live = [m for m in MODELS if m not in dead]
        if not live:
            log('VSECHNY MODELY VYCERPANE – koncim, zbytek po resetu kvot.')
            json.dump(done, io.open(prog_path,'w'), ensure_ascii=False, indent=0)
            log('HOTOVO tento beh: opraveno=%d castecne=%d, zbyva=%d' % (fixed, partial, len(targets)-len(done)))
            sys.exit(0)
        model = live[tries % len(live)]
        tries += 1
        try:
            g.synth(key, model, it['text'], role=it.get('role','ukol'), voice=it.get('voice'),
                    style=it.get('style'), out=tmp, mp3=True, sleep=SLEEP)
        except SystemExit as e:
            if 'HTTP 429' in str(e):
                dead.add(model); log('  model vycerpan: %s' % model); continue
            log('  CHYBA %s: %s' % (cid, str(e)[:80])); continue
        except g.NoAudioError:
            log('  bez audia (%s) – zkousim znovu' % model); time.sleep(SLEEP); continue
        except Exception as e:
            log('  VYJIMKA %s: %s' % (cid, str(e)[:80])); time.sleep(SLEEP); continue
        d = gender.analyze_clip(tmp)
        sc = gender.score(d) if d else 1.0
        log('  [%d/%d] %-16s pokus%d %-28s skore=%.2f (orig %.2f)' %
            (n, len(targets), cid, tries, model.split('-preview')[0], sc, orig.get(cid,0)))
        if sc < best_score:
            best_score = sc
            best_file = os.path.join(HERE, 'best_'+cid+'.mp3')
            shutil.copyfile(tmp, best_file)
        if sc < TARGET:
            break
    # vyhodnocení
    if best_file and best_score < ACCEPT_MAX:
        shutil.copyfile(best_file, os.path.join(HERE,'audio', cid+'.mp3'))
        done[cid] = round(best_score,3)
        if best_score < TARGET: fixed += 1
        else: partial += 1
        log('  -> PREPSANO %s skore %.2f' % (cid, best_score))
    else:
        done[cid] = 'nezlepseno'
        log('  -> NEZLEPSENO %s (nejlepsi %.2f) – nechavam original' % (cid, best_score))
    if best_file and os.path.exists(best_file): os.remove(best_file)
    if n % 5 == 0:
        json.dump(done, io.open(prog_path,'w'), ensure_ascii=False, indent=0)

json.dump(done, io.open(prog_path,'w'), ensure_ascii=False, indent=0)
log('=== KONEC: opraveno=%d castecne=%d nezlepseno=%d, celkem zpracovano=%d/%d ===' %
    (fixed, partial, sum(1 for v in done.values() if v=='nezlepseno'), len(done), len(targets)))
