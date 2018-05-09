#-*- coding: utf-8 -*-
import pdb 
import sys
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def is_all_english(text):
  for ch in text:
    if not is_english(ch):
      return False
  return True

def is_english(ch):
  if is_alphanum(ch) or is_punctuation(ch):
    return True
  return False

def is_alphanum(ch):
  if is_num(ch) or is_alpha(ch):
    return True
  return False

def is_num(ch):
  if ch >= '0' and ch <= '9':
    return True
  return False

def is_alpha(ch):
  if ch >= 'A' and ch <= 'Z':
    return True
  if ch >= 'a' and ch <= 'z':
    return True
  return False

def is_punctuation(ch):
  if ch == ' ' or ch == ',' or ch == '"' or ch == '.' or ch == '-' or ch == "'" or ch == ";" or ch == "?" or ch == "!":
   return True
  else:
   return False

def get_trans(line):
  line = line.replace("(̈", "(")
  line = line.replace("（", "(")
  line = line.replace("）", ")")
  line = re.sub(r" ?\([^)]+\)", "", line)
  line = line.replace("[", "")
  line = line.replace("]", "")
  trans = line.split('},')
  tran_words = ""

  # normally there are one double-braced string and the 1st token starts with t and the 3rd token is the translation
  # exceptional case - more than one double-braced strings (string starts with qualifer should be ignored)
  # exceptional case - if 3rd token starts with 'sc=' then the translation is 4th token
  # exceptional case - token with alt= has better translation
  for tran in trans:
    start_pos = tran.find('{{')
    stop_pos = start_pos + tran[start_pos:].find('}')
    token = tran[start_pos+2:stop_pos]
    if token.startswith('qualifier'):
      start_pos = stop_pos + tran[stop_pos:].find('{{')
      stop_pos = start_pos + tran[start_pos:].find('}')
      token = tran[start_pos+2:stop_pos]
    alt_pos = token.find('alt=')
    if alt_pos >= 0 :
      tran_word = token[alt_pos+4:]
      bar_pos = tran_word.find("|")
      if bar_pos > 0:
        tran_word = tran_word[:bar_pos]
        tran_words += tran_word + ", "
    elif token.startswith('t-needed'):
      continue
    elif token.startswith('t|') or token.startswith('t+'):
      tokens = token.split('|')
      if len(tokens) < 3:
        pdb.set_trace()
      elif tokens[2].startswith("sc="):
        tran_word = tokens[3]
        tran_words += tran_word + ", "
      else:
        tran_word = tokens[2]
        tran_words += tran_word + ", "
    if tran_words.find("maru") > 0:
      pdb.set_trace()
  if len(tran_words) > 0:
    tran_words = tran_words[:-2]
  tran_words = tran_words.replace("。,", ",")
  return tran_words

def extract_translation(filename):
  src = open(filename, "r")
  enko = open("./out/enwikt_trans_enko.txt", "w")
  enzh = open("./out/enwikt_trans_enzh.txt", "w")
  enja = open("./out/enwikt_trans_enja.txt", "w")
  envi = open("./out/enwikt_trans_envi.txt", "w")
  enth = open("./out/enwikt_trans_enth.txt", "w")
  noja = open("./out/enwikt_trans_noja.txt", "w")
  noko = open("./out/enwikt_trans_noko.txt", "w")
  nozh = open("./out/enwikt_trans_nozh.txt", "w")
  noth = open("./out/enwikt_trans_noth.txt", "w")
  novi = open("./out/enwikt_trans_novi.txt", "w")
  state = "none"
  num_line = 0
  num_en = 0
  num_word_trans = 0
  num_enja = 1
  num_enko = 1
  num_enzh = 1
  num_envi = 1
  num_enth = 1
  found_english = False
  found_trans = False
  found_no_entry = False
  found_ja_trans = False
  found_ko_trans = False
  found_zh_trans = False
  found_vi_trans = False
  found_th_trans = False
  pos = ""

  while True:
    line = src.readline().decode("utf-8")
    num_line += 1
    if not line: break
    line = line.strip()
    if line == "": continue
   
    # skip invalid titles and find title
    if line.startswith("%%#PAGE"):
      if found_english and pos == "" and found_no_entry == False:
        print "found english but no pos " + word
      found_english = False
      found_no_entry = False
      if found_trans:
        num_word_trans += 1
        if found_ja_trans == False:
          noja.write(word + '\n')
        else:
          num_enja += 1
        if found_ko_trans == False:
          noko.write(word + '\n')
        else:
          num_enko += 1
        if found_zh_trans == False:
          nozh.write(word + '\n')
        else:
          num_enzh += 1
        if found_vi_trans == False:
          novi.write(word + '\n')
        else:
          num_envi += 1
        if found_th_trans == False:
          noth.write(word + '\n')
        else:
          num_enth += 1
        found_trans = False
        found_no_entry = False
        found_ja_trans = False
        found_ko_trans = False
        found_th_trans = False
        found_zh_trans = False
        found_vi_trans = False
        pos = ""
      if line.startswith("%%#PAGE Wiktionary") or line.startswith("%%#PAGE Talk") or line.startswith("%%#PAGE User") \
        or line.startswith("%%#PAGE Appendix") or line.startswith("%%#PAGE Help") or line.startswith("%%#PAGE Reconstruction") \
        or line.startswith("%%#PAGE Thesaurus") or line.startswith("%%#PAGE Module") or line.startswith("%%#PAGE Index") \
        or line.startswith("%%#PAGE MediaWiki") or line.startswith("%%#PAGE Citations") or line.startswith("%%#PAGE Concordance") \
        or line.startswith("%%#PAGE Template") or line.startswith("%%#PAGE Rhymes") or line.startswith("%%#PAGE File") \
        or line.startswith("%%#PAGE Category") or line.startswith("%%#PAGE Unsupported") or line.startswith("%%#PAGE Transwiki") \
        or line.startswith("%%#PAGE Thread"):
        state = "skip"
      else:
        word = line[line.find(" ")+1:]
        if word.find('/translations') > 0:  # some word has separated translation page
          word = word.split('/')[0]
          state = "english"
          num_etymology = 0
        elif is_all_english(word):
          num_etymology = 0
          state = "title"
        else:
          state = "skip"
    elif state == "skip":
      continue

    # find english after title found
    if state == "title":
      if line.startswith("==English=="):
        state = "english"
        num_en += 1
        found_english = True
        found_trans = False
        found_ja_trans = False
        found_ko_trans = False
        found_zh_trans = False
        found_th_trans = False
        found_vi_trans = False
        is_trans = False
        pos = ""

    # etymology is not mandatory
    if state == "english":
      if line.startswith("===Etymology"):
        num_etymology += 1

      # pos is mandatory
      if (line.startswith("====") or line.startswith("=== ")) \
        and (line[4:].startswith("Verb") or line[4:].startswith("Noun") or line[4:].startswith("Pronoun") or line[4:].startswith("Preposition") \
        or line[4:].startswith("Conjunction") or line[4:].startswith("Interjection") or line[4:].startswith("Adverb") or line[4:].startswith("Adjective") \
        or line[4:].startswith("Numeral") or line[4:].startswith("Proper noun") or line[4:].startswith("Particle") or line[4:].startswith("Determiner") \
        or line[4:].startswith("Postposition") or line[4:].startswith("Prefix") or line[4:].startswith("Phrase") or line[4:].startswith("Acronym") \
        or line[4:].startswith("Abbreviation") or line[4:].startswith("Initialism") or line[4:].startswith("Suffix") or line[4:].startswith("Proverb") \
        or line[4:].startswith("Number") or line[4:].startswith("Contraction") or line[4:].startswith("Infix") or line[4:].startswith("Affix") \
        or line[4:].startswith("Symbol") or line[4:].startswith("Circumfix") or line[4:].startswith("Interfix") or line[4:].startswith("Idiom") \
        or line[4:].startswith("suffix") or line[4:].startswith("Proper Noun") or line[4:].startswith("initialism") or line[4:].startswith("Exclamation")):
        stop_pos = 4 + line[4:].find("=")
        pos = line[4:stop_pos]
      elif line.startswith("===Verb") or line.startswith("===Noun") or line.startswith("===Pronoun") or line.startswith("===Preposition") \
        or line.startswith("===Conjunction") or line.startswith("===Interjection") or line.startswith("===Adverb") or line.startswith("===Adjective") \
        or line.startswith("===Numeral") or line.startswith("===Proper noun") or line.startswith("===Particle") or line.startswith("===Determiner") \
        or line.startswith("===Postposition") or line.startswith("===Prefix") or line.startswith("===Phrase") or line.startswith("===Acronym") \
        or line.startswith("===Abbreviation") or line.startswith("===Initialism") or line.startswith("===Suffix") or line.startswith("===Proverb") \
        or line.startswith("===Number") or line.startswith("===Contraction") or line.startswith("===Infix") or line.startswith("===Affix") \
        or line.startswith("===Symbol") or line.startswith("===Circumfix") or line.startswith("===Interfix") or line.startswith("===Idiom") \
        or line.startswith("===suffix") or line.startswith("===Proper Noun") or line.startswith("===initialism") or line.startswith("===Exclamation"):
        pos = line.split("===")[1]
      elif line.startswith("=====Translations") or line.startswith("====Translations"):
        found_trans = True
      elif line.find('trans-top|') > 0:
        meaning = line.split('|')[-1][:-2]
        is_trans = True
        num_meaning_trans = 0
      elif line.find('trans-bottom') > 0:
        is_trans = False
      elif line.startswith("{{no entry"):
        found_no_entry = True

      if is_trans:
        if line.find('Korean:') > 0:
          ko_trans = get_trans(line)
          if len(ko_trans) > 0:
            found_ko_trans = True
            num_meaning_trans += 1
            enko.write(str(num_enko) + "\t" + word + "\t" + str(num_etymology) + "\t" + pos + "\t" + meaning + "\t" + ko_trans + '\n')
        elif line.find('Japanese:') > 0:
          ja_trans = get_trans(line)
          if len(ja_trans) > 0:
            found_ja_trans = True
            num_meaning_trans += 1
            enja.write(str(num_enja) + "\t" + word + "\t" + str(num_etymology) + "\t" + pos + "\t" + meaning + "\t" + ja_trans + '\n')
        elif line.find('Thai:') > 0 and line.find('Northern Thai:') < 0 and line.find('Phu Thai:') < 0 and line.find('Southern Thai') < 0:
          th_trans = get_trans(line)
          if len(th_trans) > 0:
            found_th_trans = True
            num_meaning_trans += 1
            enth.write(str(num_enth) + "\t" + word + "\t" + str(num_etymology) + "\t" + pos + "\t" + meaning + "\t" + th_trans + '\n')
        elif line.find('Vietnamese:') > 0:
          vi_trans = get_trans(line)
          if len(vi_trans) > 0:
            found_vi_trans = True
            num_meaning_trans += 1
            envi.write(str(num_envi) + "\t" + word + "\t" + str(num_etymology) + "\t" + pos + "\t" + meaning + "\t" + vi_trans + '\n')
        elif line.find('Mandarin:') > 0:
          zh_trans = get_trans(line)
          if len(zh_trans) > 0:
            found_zh_trans = True
            num_meaning_trans += 1
            enzh.write(str(num_enzh) + "\t" + word + "\t" + str(num_etymology) + "\t" + pos + "\t" + meaning + "\t" + zh_trans + '\n')

  src.close()
  enko.close()
  enja.close()
  enth.close()
  envi.close()
  enzh.close()
  noja.close()
  noko.close()
  nozh.close()
  noth.close()
  novi.close()
  print "num_word_trans " + str(num_word_trans)
  print "num_enja " + str(num_enja)
  print "num_enzh " + str(num_enzh)
  print "num_enko " + str(num_enko)
  print "num_envi " + str(num_envi)
  print "num_enth " + str(num_enth)

if __name__ == "__main__":
  extract_translation('src/enwiktionary.txt')
