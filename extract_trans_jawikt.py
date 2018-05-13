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

def remove_inner_double_brace(line):
  if line.count("{{") < 2:
    return line
  remains = ""
  first_open = line.find("{{")
  first_close = line.find("}}")
  second_open = first_open+2 + line[first_open+2:].find("{{")
  if second_open < first_close:
    return line[:second_open] + line[first_close+2:]
  else:
    return line

def get_trans(line):
  line = line.replace('"', "")
  line = line.replace("'''", "")
  line = line.replace("''", "")
  line = line.replace("（", "(")
  line = line.replace("）", ")")
  line = re.sub(r" ?\([^)]+\)", "", line)

  remains = line
  to_trans = ""
  while remains:
    start_pos = remains.find("[[")
    stop_pos = start_pos + remains[start_pos:].find("]]")
    if start_pos >= 0 and stop_pos > 0:
      token = remains[start_pos+2:stop_pos]
      if token.find("|") >= 0:
        to_trans += remains[:start_pos] + token.split("|")[1]
        remains = remains[stop_pos+2:]
      else:
        to_trans += remains[:start_pos] + token
        remains = remains[stop_pos+2:]
    else:
      to_trans += remains
      break

  # remove inner double brace if nested
  to_trans = remove_inner_double_brace(to_trans)

  # first token should be check for double braced phrase
  remains = to_trans
  to_trans = ""
  while remains:
    start_pos = remains.find("{{")
    stop_pos = start_pos + remains[start_pos:].find("}}")
    if start_pos >= 0 and stop_pos > 0:
      token = remains[start_pos+2:stop_pos]
      if token.find("|") >= 0:
        tokens = token.split("|")
        if tokens[0] == "ふりがな" or tokens[0] == "おくりがな" or tokens[0] == "w" or tokens[0] == "ruby":
          to_trans += remains[:start_pos] + tokens[1]
          remains = remains[stop_pos+2:]
        elif tokens[0] == "ふりがな2" or tokens[0] == "おくりがな2" or tokens[0] == "送り活2" or tokens[0] == "送り仮名2":
          to_trans += remains[:start_pos] + tokens[1] + tokens[3]
          remains = remains[stop_pos+2:]
        elif tokens[0] == "ふりがな3" or tokens[0] == "おくりがな3":
          to_trans += remains[:start_pos] + tokens[1] + tokens[4] + tokens[6]
          remains = remains[stop_pos+2:]
        elif tokens[0] == "l":
          to_trans += remains[:start_pos] + tokens[2]
          remains = remains[stop_pos+2:]
        elif tokens[0] == "サ変":
          to_trans += remains[:start_pos] + tokens[1] + "する"
          remains = remains[stop_pos+2:]
        elif tokens[0] == "ジル":
          to_trans += remains[:start_pos] + tokens[1] + "じる"
          remains = remains[stop_pos+2:]
        elif tokens[0].startswith("plural of"):
          to_trans += remains[:start_pos] + tokens[1] + "の複数形"
          remains = remains[stop_pos+2:]
        elif tokens[0].startswith("past of"):
          to_trans += remains[:start_pos] + tokens[1] + "の過去形"
          remains = remains[stop_pos+2:]
        elif tokens[0].startswith("wikipedia"):
          to_trans += remains[:start_pos] + tokens[1]
          remains = remains[stop_pos+2:]
        else: # skip
          to_trans += remains[:start_pos]
          remains = remains[stop_pos+2:]
      elif token.find(":") >= 0:
        tokens = token.split(":")
        if tokens[0] == "cat":
          to_trans += remains[:start_pos]
          remains = remains[stop_pos+2:]
        else:
          to_trans += remains[:start_pos] + token
          remains = remains[stop_pos+2:]
      else: # skip
        to_trans += remains[:start_pos]
        remains = remains[stop_pos+2:]
    else:
      to_trans += remains
      break

  if is_all_english(to_trans):
    to_trans = ""
  return to_trans.strip()

def extract_translation(filename):
  src = open(filename, "r")
  jaen = open("out/jawikt_trans_enja.txt", "w")
  state = "none"
  num_line = 0
  num_en = 0
  num_en_english = 0
  num_trans = 1
  found_english = False
  found_pos = False
  found_trans = False

  while True:
    line = src.readline().decode("utf-8")
    num_line += 1
    if not line: break
    line = line.strip()
    if line == "": continue
   
    # skip invalid titles and find title
    if line.startswith("%%#PAGE"):
      if found_english:
        num_en_english += 1
        if found_trans:
          num_trans += 1
        elif found_pos:
          print "found pos but no trans: " + word
      found_english = False
      found_pos = False
      found_trans = False
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
        if is_all_english(word):
          num_etymology = 0
          num_en += 1
          state = "title"
        else:
          state = "skip"
    elif state == "skip":
      continue

    if state == "english":
      if line.startswith("==") and line.count("=") == 4:
        if line.find("{{") > 0 or line.find("語"): # another language within page
          state = "title"

    # find english after title
    # english is not mandatory (parsely)
    if state == "title":
      if line.find("=={{en}}") >= 0 or line.find("=={{eng}}") >= 0 or line.find("== {{en}}") >= 0 or line.find("== {{eng}}") >= 0 \
        or line.find("==英語") >= 0 or line.find("== 英語") >= 0 or line.find("==[[英語]]") >= 0:
        state = "english"
        found_english = True
        pos = ""
        #print "english: " + line

    # etymology is not mandatory
    if state == "english":
      if line.find("==={{etym}}") >= 0 or line.find("===語源") >= 0:
        num_etymology += 1

      # pos is mandatory
      # pos with 1 double brace
      if (line.find("{{en-verb") >= 0 or line.find("{{en-noun") >= 0 or line.find("{{en-pronoun") >= 0 or line.find("{{en-prep") >= 0 \
        or line.find("{{en-conj") >= 0 or line.find("{{en-interj") >= 0 or line.find("{{en-adv") >= 0 or line.find("{{en-adj") >= 0 \
        or line.find("{{en-proper noun") >= 0 or line.find("{{en-det") >= 0 or line.find("{{adj}}") >= 0 or line.find("{{postposition") >= 0 \
        or line.find("{{noun}}") > 0 or line.find("{{det}}") > 0 or line.find("{{verb}}") > 0 or line.find("{{idiom}}") > 0 \
        or line.find("{{abbr}}") > 0 or line.find("{{acronym}}") > 0 or line.find("{{adv}}") > 0 or line.find("{{prefix}}") > 0\
        or line.find("{{adjective}}") > 0 or line.find("{{adjc}}") > 0 or line.find("{{auxverb}}") > 0) and \
        not line.startswith("#"):
        start = line.find("{{")
        stop = line.find("}}")
        pos = line[start+2:stop]
        found_pos = True
        #print "pos1: " + pos
      # pos with 2 double brace
      elif (line.find("{{en}}") >= 0 or line.find("{{eng}}") >= 0) and \
        (line.find("{{pronoun}}") > 0 or line.find("{{noun}}") > 0 or line.find("{{name}}") > 0 or line.find("{{verb}}") > 0 \
        or line.find("{{abbr}}") > 0 or line.find("{{pref}}") > 0 or line.find("{{contraction}}") > 0 or line.find("{{prep}}") > 0 \
        or line.find("{{conj}}") > 0):
        start = line.find("{{")
        stop = line.rfind("}}")
        pos = line[start+2:stop]
        found_pos = True
        #print "pos2: " + pos
      # pos with no double brace
      elif line.startswith("===") and \
        (line.find("名詞") > 0 or line.find("間投詞") > 0 or line.find("略語") > 0 or line.find("前置詞") > 0 or line.find("動詞") > 0 \
        or line.find("人名") > 0 or line.find("接頭辞") > 0 or line.find("他動詞") > 0 or line.find("縮約形") > 0 or line.find("形容詞") > 0 \
        or line.find("副詞") > 0):
        start = line.find("===")
        stop = line.rfind("===")
        pos = line[start+3:stop].strip()
        found_pos = True
        #print "pos3: " + pos
      elif pos != "" and ((line.startswith("#") and not line.startswith("#*") and not line.startswith("#:") and not line.startswith("##") and not line.startswith("#;")) \
        or (line.startswith("*#") and not line.startswith("*#:"))):
        line = line.replace("、、", "、")
        if len(line) > 1 and line[1] == "、":
          trans = get_trans(line[2:].strip())
        else:
          trans = get_trans(line[1:].strip())
        if len(trans) > 0:
          found_trans = True
          jaen.write(str(num_trans) + "\t" + word + "\t" + str(num_etymology) + "\t" + pos + "\t" + trans + "\n")
        else:
          print str(num_trans) + " " + word + ": no trans " + line
      #elif pos != "" and line.startswith("*") and not found_trans:  # for hiragana, ..
      #  trans = get_trans(line[1:].strip())
      #  if len(trans) > 0:
      #    found_trans = True
      #    print trans
      #    print "*trans: " + trans
      #    #enja.write(word + "\t" + str(num_etymology) + "\t" + pos + "\t" + meaning + "\t" + trans + '\n')

  src.close()
  jaen.close()
  print "num_en " + str(num_en)
  print "num_en_english " + str(num_en_english)
  print "num_trans " + str(num_trans)

if __name__ == "__main__":
  extract_translation('src/jawiktionary.txt')
