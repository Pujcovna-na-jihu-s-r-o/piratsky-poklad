# -*- coding: utf-8 -*-
"""
Vyrobí manifest klipů pro Gemini TTS (manifest.json) a vloží do hry blok textů
(`const T={...}; const AUDIO_IDS=[...];` mezi značky /*AUDIO-DATA-START*/ a /*AUDIO-DATA-END*/).
Jediný zdroj textů: gen_symbols.py (značky, ostrovy, otázky, posádka, moře, chvály) + tabulka UI níže.
Klipy: n_<id> jméno značky, say_<id> výklad, cheer_<id> povzbuzení, intro_<ostrov>, iname_<ostrov>,
crew_<člen>, les_<n> výklad popisu kontrol, pdn_<číslo>/pds_<číslo> jména a výklady piktogramů, q_<k>/hint_<k> otázky, praise_<k>, sea_<k>, seadone_<k>, rank_<k>, story_<n>, quest_<n>,
qhint_<n>, qok_<n>, qwrong_*, ui_* a fragmenty fr_* pro skládané věty.
"""
import io, json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gen_symbols as g

N = len(g.ISL)
RANKS = ["Plavčík", "Námořník", "Lodník", "Kormidelník", "Kapitán", "Admirál"]
NAME_STYLE = ("Přečti nahlas jen následující český název, správnou českou výslovností, klidně a jasně, nepřidávej žádná další slova.")

UI = {
 # domov, mapa ostrovů
 "ui_home_new": "Ahoj, plavčíku! Já jsem papoušek Pepík. Klepni na Začít příběh a dozvíš se, proč musí každý hledač pokladů umět číst mapu.",
 "ui_home_first": "Vítej zpátky, plavčíku! Ještě nemáme žádný kousek mapy. Vyplujeme k Ostrovu papoušků?",
 "ui_home_back": "Vítej zpátky, plavčíku! Další kousek mapy čeká na ostrově:",
 "ui_home_won": "Vítej zpátky, kapitáne! Zlatý kompas máme, ale na Volném moři čeká další dobrodružství. Zvládneš delší sérii než minule?",
 "ui_world": "Tohle je mapa ostrovů. Je nakreslená jako trať v orientačním běhu: start, kontroly a cíl. Na každém ostrově je schovaný kousek mapy. Klepni na první ostrov!",
 "ui_locked": "Sem se dostaneš, až vyluštíš předchozí ostrov.",
 "ui_daily": "Denní poklad! Zlaťáky navíc do truhly. Přijď zase zítra, bude jich ještě víc!",
 "ui_newsyms": "Tohle jsou nové značky. Klepni na ně a poslechni si je. Až budeš připravený, vypluj!",
 "ui_boss_rules": "Já ti vždycky řeknu jméno značky a ty na ni rychle klepni. Vyhraje ten, kdo jich najde víc, než dohoří svíčka.",
 "mlha_challenge": "Arr! Tak ty chceš kousek mapy, plavčíku? Poraz mě v souboji, jestli to dokážeš!",
 "ui_endless": "Volné moře! Kolik značek přečteš v řadě bez chyby?",
 # souboj
 "ui_duel": "Souboj! Najdi značku dřív než Mlha, než dohoří svíčka.",
 "ui_duel_start": "Souboj začíná! Tři, dva, jedna, teď!",
 "mlha_score_0": "Cha chá, mám další!",
 "mlha_score_1": "Jsi pomalý jako želva!",
 "mlha_score_2": "Ten poklad bude můj!",
 "mlha_gloat": "Cha chá! Tentokrát jsem vyhrál já!",
 "mlha_lost": "Ne! To není možné! Tak dobře, tady máš ten kousek mapy.",
 "res_lose": "Mlha tentokrát vyhrál o fous. Zkus to znovu, příště ho porazíš! Už je unavený.",
 # režimy úkolů
 "ui_what": "Co je to za značku? Vyber správné jméno.",
 "ui_pexeso": "Pexeso! Otoč dvě karty a najdi značku a její jméno. Za každou dvojici je zlaťák.",
 "ui_pexeso_done": "Všechny dvojice! Bonus do truhly!",
 "ui_desc_a": "V popisech kontrol je tenhle obrázek. Najdi, jak to vypadá na mapě.",
 "ui_shared": "Kterým značkám na mapě patří tenhle obrázek? Najdi všechny.",
 "ui_shared_intro": "Pozor, plavčíku! Popis kontrol říká, co to je, a mapa ukazuje, jak to vypadá. Proto jeden obrázek v popisu někdy patří víc značkám na mapě.",
 "ui_shared_more": "Správně! Ještě nějaká chybí.",
 "ui_desc_yes": "V popisech kontrol má svůj obrázek.",
 "ui_desc_no": "V popisech kontrol se tahle značka nepoužívá, je jen v mapě.",
 # fragmenty (skládané věty: fragment + jméno značky + fragment)
 "fr_find": "Najdi na mapě:",
 "fr_toneni": "To není",
 "fr_ale": "ale",
 "fr_znovu": "Zkus to znovu.",
 "fr_anojeto": "Ano, je to",
 "fr_ne": "Ne,",
 "fr_vypada": "vypadá jinak. Tohle je",
 "fr_spravne": "Správně!",
 "fr_netoje": "Ne, to je",
 "fr_kdeje": "Kde je na mapě",
 "fr_klepni": "Klepni na to.",
 "fr_presnetam": "Přesně tam!",
 "fr_toje": "To je",
 "fr_hledej": "Hledej:",
 "fr_rozkaz": "Kapitánův rozkaz! Nejdřív",
 "fr_potom": "potom",
 "fr_nakonec": "a nakonec",
 "fr_ated": "A teď:",
 "fr_tedhledej": "Teď hledej:",
 "fr_splnen": "Rozkaz splněn!",
 "fr_namapeje": "Na mapě je",
 "fr_jaktovypada": "Jak to vypadá v popisech kontrol?",
 "fr_anonamape": "Ano! Na mapě je to",
 "fr_presnetak_popisy": "Přesně tak! V popisech kontrol je",
 "fr_takhle": "takhle.",
 "fr_tohlejevpopisech": "Tohle je v popisech",
 "fr_learned1": "Jupí! Značku",
 "fr_learned2": "už umíš!",
 "ui_all_learned": "Hurá! Umíš všechny značky! Jsi opravdový čtenář map!",
 # výsledek ostrova
 "res_win_1": "Ostrov vyluštěn! Máš jednu hvězdu.",
 "res_win_2": "Ostrov vyluštěn! Máš dvě hvězdy.",
 "res_win_3": "Ostrov vyluštěn! Máš tři hvězdy!",
 "res_retry": "Zahraj ho znovu bez chyb a budou tři.",
 "res_duel_1": "Porazil jsi kapitána Mlhu! Máš jednu hvězdu.",
 "res_duel_2": "Porazil jsi kapitána Mlhu! Máš dvě hvězdy.",
 "res_duel_3": "Porazil jsi kapitána Mlhu! Máš tři hvězdy!",
 "res_piece": "Získal jsi kousek mapy!",
 "res_map": "Mapa je celá! Teď ji přečti a najdi poklad!",
 # zkouška moře, procvičení chyb, opakování (klipy zatím nejsou namluvené, hra čte hlasem prohlížeče)
 "exam_intro": "Zkouška moře! Na každou značku se zeptám jen jednou a nápovědu nedám. Ukaž, co umíš, námořníku!",
 "exam_round2": "Ještě jednou projdeme ty, které se ti pletly. Tentokrát se zeptám obráceně.",
 "exam_gold": "Zlatá medaile! Tohle moře znáš jako své boty. Jsi opravdový kapitán!",
 "exam_silver": "Stříbrná medaile! Skoro všechno si pamatuješ. Tak se pluje!",
 "exam_bronze": "Bronzová medaile! Dobrý začátek. Pár značek ještě procvičíme a bude zlatá.",
 "exam_none": "Tentokrát bez medaile, ale nevěš hlavu! Procvičíme, co se pletlo, a zkusíš to znovu.",
 "fix_intro": "Pojď si procvičit značky, které ti dělaly potíže. Tentokrát ti pomůžu.",
 "fix_done": "Hotovo! Tyhle značky už půjdou líp. Můžeš zkusit zkoušku znovu.",
 "review_offer": "Co kdybychom si zopakovali značky z minulých ostrovů? Ať ti žádná neuplave!",
 "review_intro": "Zopakujeme si značky z minulých ostrovů, hlavně ty, co se ti pletou.",
 "review_done": "Výborně, značky z minulých ostrovů máš zase čerstvé!",
 # krám a ovládání
 "ui_shop_intro": "Vítej v krámu! Klobouk si nasadíš na hlavu, vlajku dáš na loď a poklady ti zůstanou v truhle.",
 "ui_shop_poor": "Ještě nemáš dost zlaťáků. Vylušti další ostrov a budeš je mít!",
 "ui_shop_bought": "Paráda! Je to tvoje!",
 "ui_shop_treasure": "Krásný poklad! Už je v truhle.",
 "ui_shop_equipped": "Hotovo, už je to na lodi.",
 "ui_mute_on": "Zvuk je zapnutý, námořníku.",
 "ui_reset": "Hotovo! Můžeš začít znovu od začátku.",
 # příběh
 "story_0": "Před dávnými časy schovali piráti na ostrově poklad. Aby ho zase našli, nakreslili mapu. A hádej co: použili úplně stejné značky, jaké se dnes používají v orientačním běhu! Modrá je voda, žlutá louka, černá tečka balvan a křížek v kolečkách je poklad.",
 "story_1": "Jenže zlý kapitán Mlha mapu ukradl, roztrhal ji na %d kousků a každý schoval na jiném ostrově. Bez mapy poklad nikdo nenajde." % N,
 "mlha_story": "Cha chá! Tu mapu už nikdy neuvidíte!",
 "story_2": "Kdo chce poklad najít, musí umět značky číst: poznat, kde je voda, kde bažina a kudy vede cesta. A pak vymyslet, kudy se k pokladu dostat, aby nezapadl do bažiny a neztratil se v hustníku.",
 "story_3": "Já jsem papoušek Pepík a budu ti pomáhat. Za každý vyluštěný ostrov získáš kousek mapy. Až budeš mít všechny, mapu přečteš, dojdeš k pokladu a Zlatý kompas bude tvůj!",
 # finále – cesta k pokladu
 "quest_0": "Tohle je celá pirátská mapa pokladu. Každá cesta začíná na startu, to je fialový trojúhelník vlevo dole. Klepni na start.",
 "quest_1": "Od startu vede pěší cesta, ta černá přerušovaná čára. Běž po ní až k balvanu, k černé tečce u kontroly jedna. Klepni na balvan.",
 "qhint_1": "Drž se černé přerušované čáry, cesta tě dovede k balvanu.",
 "quest_2": "Od balvanu vyběhni na kopec. Kopec poznáš podle hnědých vrstevnic, vrchol je uprostřed nejmenšího kroužku. Klepni na vrchol kopce.",
 "qhint_2": "Hledej hnědé kroužky v sobě, to je kopec.",
 "quest_3": "Z kopce vidíš žlutou louku a na ní velký strom, zelený kroužek u kontroly dva. Klepni na strom.",
 "qhint_3": "Velký strom je zelený kroužek na žluté louce.",
 "quest_4": "A teď pozor. Bažinu s modrými čárkami obejdi, ta je nebezpečná. Pod loukou jsou dvě fialová kolečka s křížkem. Tam je poklad! Klepni na něj.",
 "qhint_4": "Poklad je v cíli, ve dvou fialových kolečkách s křížkem.",
 "qok_0": "Správně!",
 "qok_1": "Přesně tak!",
 "qok_2": "Výborně, čteš mapu jako kapitán!",
 "quest_done": "Hurá! Našel jsi poklad! Přečetl jsi celou mapu jako opravdový pirát. A v truhle je Zlatý kompas!",
 "qwrong_bazina": "To je bažina, tam bys promokl a zapadl.",
 "qwrong_voda": "To je voda, tam se neběží, tu obejdi.",
 "qwrong_housti": "To je hustník, tam se zamotáš do větví.",
 "qwrong_poklad": "Poklad je tam, ale nejdřív musíš doběhnout po trati.",
 "qwrong_nothing": "Tam nic není.",
 "qwrong_again": "Poslechni si to znovu.",
 "ui_final": "Přečetl jsi celou pirátskou mapu, našel poklad a porazil kapitána Mlhu. Zlatý kompas je tvůj a ty jsi opravdový kapitán! Na Volném moři na tebe čekají další dobrodružství.",
}

# 5. moře „Jak mluví popis I“ – zadání a zpětná vazba nových typů úkolů (id jsou závazná pro herní logiku).
# Jména piktogramů se za fragmenty skládají z klipů PD[i].clip (znovupoužité n_<značka>, jinak pdn_<číslo>).
UI5 = {
 # mapa × popis
 "ui_mp": "Je tohle značka z mapy, nebo obrázek z popisu kontrol?",
 "fr_zmapy": "To je značka z mapy.",
 "fr_zpopisu": "To je obrázek z popisu kontrol.",
 # piktogram ↔ jméno
 "ui_pd_name": "Co znamená tenhle obrázek v popisu kontrol?",
 "ui_pd_pic": "Najdi v popisu kontrol:",
 "fr_vpopisu": "V popisu kontrol je to",
 # řádek popisu: dítě ťuká na část lístku
 "ui_row_a": "Ťukni na pořadí kontroly.",
 "ui_row_b": "Ťukni na kód kontroly.",
 "ui_row_d": "Ťukni na obrázek, který říká, co na kontrole najdeš.",
 "ui_row_len": "Ťukni na délku tratě.",
 "ui_row_climb": "Ťukni na převýšení.",
 "ui_row_name": "Ťukni na název tratě.",
 "fr_row_a": "To je pořadí kontroly. Stejné číslo najdeš na mapě u kolečka.",
 "fr_row_b": "To je kód kontroly. Stejné číslo najdeš na lampionu.",
 "fr_row_d": "To je obrázek, který říká, co na kontrole najdeš.",
 "fr_row_len": "To je délka tratě. Říká, kolik kilometrů poběžíš.",
 "fr_row_climb": "To je převýšení. Říká, kolik metrů celkem vystoupáš do kopce.",
 "fr_row_name": "To je název tratě.",
 # navíc: stávající texty říkají „značka“, tady jde o obrázky z popisu
 "ui_locked5": "Druhá plavba se otevře, až najdeš Zlatý kompas. Nejdřív dohraj a přečti pirátskou mapu!",
 "ui_newpds": "Tohle jsou nové obrázky z popisu kontrol. Klepni na ně a poslechni si je. Až budeš připravený, vypluj!",
 "ui_boss_rules5": "Já ti řeknu jméno a ty rychle klepni na jeho obrázek v popisu kontrol. Vyhraje ten, kdo jich najde víc, než dohoří svíčka.",
 "ui_duel_pd": "Souboj! Najdi v popisu kontrol správný obrázek dřív než Mlha, než dohoří svíčka.",
 "exam5_intro": "Zkouška moře! Na každý obrázek z popisu kontrol se zeptám jen jednou a nápovědu nedám. Ukaž, co umíš, námořníku!",
}

def build():
    items = []
    def add(id, text, role="pepik", style=None):
        it = dict(id=id, role=role, text=text)
        if style: it["style"] = style
        items.append(it)
    for s in g.S:
        add("n_" + s["id"], g.sname(s), style=NAME_STYLE)
        add("say_" + s["id"], s["say"])
        if s.get("cheer"): add("cheer_" + s["id"], "Správně! " + s["cheer"])
    for i, isl in enumerate(g.ISL):
        add("intro_" + isl["id"], g.intro_of(i))
        add("iname_" + isl["id"], isl["name"], style=NAME_STYLE)
        c = g.crew_of(i); add("crew_" + c["id"], c["say"])
    for k, c in enumerate(g.CON):
        add("q_%d" % k, c["q"]); add("hint_%d" % k, c["hint"])
    for k, p in enumerate(g.PRAISE): add("praise_%d" % k, p)
    for k, sname_ in enumerate(g.SEAS): add("sea_%d" % k, sname_, style=NAME_STYLE)
    nseas = (N + 5) // 6
    for k in range(max(0, nseas - 1)): add("seadone_%d" % k, "Proplul jsi celé %s! Otevírá se %s." % (g.SEAS[k], g.SEAS[k + 1]))
    for k in range(1, len(RANKS)): add("rank_%d" % k, "Povýšení! Teď jsi %s!" % RANKS[k])
    for id, text in UI.items(): add(id, text, role=("mlha" if id.startswith("mlha_") else "pepik"))
    # 5. moře: ostrovy (úvod, jméno, posádka), kroky výkladu, jména a výklady piktogramů, mapová značka 704, zadání úkolů
    for isl in g.ISL5:
        add("intro_" + isl["id"], isl["intro"])
        add("iname_" + isl["id"], isl["name"], style=NAME_STYLE)
        add("crew_" + isl["crew"]["id"], isl["crew"]["say"])
        for les in isl.get("lesson", []): add(les["id"], les["text"])
    for pd in g.PD:
        if pd["clip"].startswith("pdn_"): add(pd["clip"], pd["name"], style=NAME_STYLE)
        if pd["new"]: add(pd["sclip"], pd["say"])
    add("n_" + g.SYM704["id"], g.SYM704["name"], style=NAME_STYLE)
    add("say_" + g.SYM704["id"], g.SYM704["say"])
    for id, text in UI5.items(): add(id, text)
    # Rozdělení hlasů: kapitán Mlha (mlha_*), "ukol" = hlas, který během úkolů čte zadání
    # a jména značek (ty se skládají do jedné věty, musí být jedním hlasem), Pepík = zbytek.
    TASK_UI = {"ui_mp", "ui_pd_name", "ui_pd_pic", "ui_row_a", "ui_row_b", "ui_row_d", "ui_row_len", "ui_row_climb", "ui_row_name",
               "ui_duel_pd", "exam5_intro", "ui_what", "ui_pexeso", "ui_pexeso_done", "ui_desc_a", "ui_desc_yes", "ui_desc_no", "ui_shared", "ui_shared_more", "ui_duel", "ui_endless",
               "exam_intro", "exam_round2", "fix_intro", "fix_done", "review_intro", "review_done"}
    def role_for(i):
        if i.startswith("mlha_"): return "mlha"
        if i.startswith(("fr_", "n_", "pdn_", "q_", "hint_", "praise_", "cheer_")) or i in TASK_UI: return "ukol"
        return "pepik"
    for it in items: it["role"] = role_for(it["id"])
    ids = [it["id"] for it in items]
    assert len(ids) == len(set(ids)), "duplicitní id klipu"
    return items

def js_str(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def main():
    items = build()
    io.open(os.path.join(HERE, "manifest.json"), "w", encoding="utf-8").write(json.dumps(items, ensure_ascii=False, indent=1))
    T = {it["id"]: it["text"] for it in items if not it["id"].startswith(("n_", "say_", "cheer_", "intro_", "crew_", "q_", "hint_", "praise_"))}
    # iname_/sea_/seadone_/rank_/ui_/fr_/story_/quest_/qhint_/qok_/qwrong_/res_/mlha_ → do T (texty, které hra zobrazuje nebo čte)
    block = "/*AUDIO-DATA-START*/\nconst T={" + ",".join("%s:%s" % (js_str(k), js_str(v)) for k, v in T.items()) + "};\n" + \
            "const AUDIO_IDS=[" + ",".join(js_str(it["id"]) for it in items) + "];\n/*AUDIO-DATA-END*/"
    html = io.open(g.HTML, encoding="utf-8").read()
    a = html.index("/*AUDIO-DATA-START*/"); b = html.index("/*AUDIO-DATA-END*/") + len("/*AUDIO-DATA-END*/")
    html = html[:a] + block + html[b:]
    io.open(g.HTML, "w", encoding="utf-8", newline="\n").write(html)
    chars = sum(len(it["text"]) for it in items)
    print("klipů:", len(items), "| textů v T:", len(T), "| znaků celkem:", chars)

if __name__ == "__main__":
    main()
