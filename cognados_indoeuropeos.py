#!/usr/bin/env python3
"""
cognados_indoeuropeos.py — tabla de cognados IE sánscrito/hindi <-> romance/inglés.

Motivación: los conceptos funcionales (nuevo, nombre, madre, padre, hermano,
numerales, dar) NO están en la fase-1 de `lexico` (264 conceptos temáticos),
pero son precisamente donde el paralelismo sánscrito<->romance es más evidente:
    náman ~ name/nombre (PIE *h₁nómn̥)
    mātár ~ mother/mater (PIE *méh₂tēr)
    pitár ~ father/pater (PIE *ph₂tḗr)
    bhrātar ~ brother/frater (PIE *bʰréh₂tēr)
    nakt ~ noche/night/noctem (PIE *nókʷts)   [ya en lexico]
    diva ~ día/dies (PIE *dyew-)              [ya en lexico]

Se almacena como tabla REFERENCIAL independiente (igual que lenguas_referenciales):
no participa en el consenso y no altera `lexico`. La similitud se calcula con
difflib sobre formas normalizadas (NFD, sin diacríticos) solo como indicio; la
relación real es genética (descendencia común del PIE), no superficial.
"""
import sqlite3, unicodedata, difflib, os

DB = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lexico.db')

def norm(s):
    s = unicodedata.normalize('NFD', (s or '').lower())
    return ''.join(ch for ch in s if unicodedata.category(ch) not in ('Mn','Mc'))

def sim(a, b):
    return round(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio(), 2)

# concepto, sa(IAST), sa_dev, hi, hi_dev, bo_wylie, bo_tib, pie, {lengua: forma}
DATOS = [
 ('nuevo',  'náva',      'नव',      'navā̃',  'नवाँ',   'gsar pa', 'གསར་པ', '*néwos',
   dict(es='nuevo', en='new', fr='nouveau', it='nuovo', pt='novo', ro='nou', ia='nove', eo='nova', latin='novus')),
 ('nombre', 'náman',     'नामन्',   'nām',    'नाम',    'ming',    'མིང', '*h₁nómn̥',
   dict(es='nombre', en='name', fr='nom', it='nome', pt='nome', ro='nume', ia='nomine', eo='nomo', latin='nomen')),
 ('madre',  'mātár',     'मातृ',    'mā̃',     'माँ',    'ma',      'མ', '*méh₂tēr',
   dict(es='madre', en='mother', fr='mère', it='madre', pt='mãe', ro='mamă', ia='matre', latin='mater')),
 ('padre',  'pitár',     'पितृ',    'pitā',   'पिता',   'pha',     'ཕ', '*ph₂tḗr',
   dict(es='padre', en='father', fr='père', it='padre', pt='pai', ro='tată', ia='patre', eo='patro', latin='pater')),
 ('hermano','bhrā́tar',   'भ्रातृ',   'bhāī',   'भाई',    'jo bo',   'ཇོ་བོ', '*bʰréh₂tēr',
   dict(es='hermano', en='brother', fr='frère', it='fratello', pt='irmão', ro='frate', ia='fratre', eo='frato', latin='frater')),
 ('dos',    'dá',        'द्वे',    'do',     'दो',     'gnyis',   'གཉིས', '*dwóh₁',
   dict(es='dos', en='two', fr='deux', it='due', pt='dois', ro='două', ia='duo', eo='du', latin='duo')),
 ('tres',   'tráyas',    'त्रयस्',  'tīn',    'तीन',    'gsum',    'གསུམ', '*tréyes',
   dict(es='tres', en='three', fr='trois', it='tre', pt='três', ro='trei', ia='tres', eo='tri', latin='tres')),
 ('cuatro', 'catvā́ras',  'चत्वारस्','cār',    'चार',    'bzhi',    'བཞི', '*kʷetwóres',
   dict(es='cuatro', en='four', fr='quatre', it='quattro', pt='quatro', ro='patru', ia='quatro', eo='kvar', latin='quattuor')),
 ('cien',   'śatám',     'शतम्',   'sau',    'सौ',     'brgya',   'བརྒྱ', '*ḱm̥tóm',
   dict(es='cien', en='hundred', fr='cent', it='cento', pt='cem', ro='sute', ia='cente', eo='cent', latin='centum')),
 ('dar',    'dadāti',    'ददाति',   'denā',   'देना',    'sbyin pa','སྦིན་པ', '*deh₃-',
   dict(es='dar', en='give', fr='donner', it='dare', pt='dar', ro='da', ia='dar', eo='doni', latin='dare')),
 # refuerzo de pares ya presentes en lexico (fase-1) para completar el cuadro:
 ('noche',  'nakt',      'नक्ति',   'rat',    'रात',    'mi gam',  'མི་གམ', '*nókʷts',
   dict(es='noche', en='night', fr='nuit', it='notte', pt='noite', ro='noapte', ia='nocte', eo='nokto', latin='nox')),
 ('pie',    'pád',       'पाद',     'pair',   'पैर',    'rkang pa','རྐང་པ', '*ped-',
   dict(es='pie', en='foot', fr='pied', it='piede', pt='pé', ro='picior', ia='pede', eo='pedo', latin='pes')),
 ('viento', 'váta',      'वात',     'hawa',   'हवा',    'rlung',   'རླུང', '*weh₂t-',
   dict(es='viento', en='wind', fr='vent', it='vento', pt='vento', ro='vânt', ia='vento', eo='vento', latin='ventus')),
]

DDL = """
CREATE TABLE IF NOT EXISTS cognados_ie (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  concepto      TEXT NOT NULL,
  sanscrito     TEXT NOT NULL,          -- transliteración IAST
  sa_devanagari TEXT,
  hindi         TEXT,
  hi_devanagari TEXT,
  tibetano      TEXT,                    -- Wylie
  bo_script     TEXT,
  etimo_pie     TEXT,
  lengua_contraste TEXT NOT NULL,        -- romance/inglatín frente al cual se compara
  forma_contraste  TEXT NOT NULL,
  similitud     REAL,                    -- orientativa (Levenshtein-like); relación real = genética
  en_lexico     INTEGER DEFAULT 0,       -- 1 si el concepto ya está en la fase-1 de lexico
  nota          TEXT,
  UNIQUE(concepto, lengua_contraste)
);
"""

def main():
    c = sqlite3.connect(DB)
    c.executescript(DDL)
    en_lex = {r[0] for r in c.execute("SELECT concepto_es FROM lexico")}
    n = 0
    for (concepto, sa, sad, hi, hid, bo, bos, pie, contrastes) in DATOS:
        for leng, forma in contrastes.items():
            c.execute("""INSERT OR REPLACE INTO cognados_ie
                (concepto, sanscrito, sa_devanagari, hindi, hi_devanagari,
                 tibetano, bo_script, etimo_pie, lengua_contraste, forma_contraste,
                 similitud, en_lexico, nota)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (concepto, sa, sad, hi, hid, bo, bos, pie, leng, forma,
                 sim(sa, forma), 1 if concepto in en_lex else 0,
                 'referencial: no participa en el consenso'))
            n += 1
    c.commit()
    print(f'cognados_ie: {n} filas actualizadas')
    print('\nTop parejas por similitud:')
    for r in c.execute("""SELECT concepto, sanscrito, lengua_contraste, forma_contraste, similitud
                          FROM cognados_ie ORDER BY similitud DESC LIMIT 15"""):
        print('  %-9s %-10s ~ %-8s %-10s %.2f' % r)
    c.close()

if __name__ == '__main__':
    main()
