#-*- coding: utf-8 -*-
import pdb 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

nc_dict = {}
nk_dict = {}
nj_dict = {}

def is_chinese_unihan(ch):
  global nc_dict
  if len(nc_dict) == 0:
    read_unihan()
  if ch in nc_dict:
    return False
  return True

def has_none_chinese_unihan(word):
  for ch in word:
    if not is_chinese_unihan(ch):
      return True
  return False

def is_japanese_unihan(ch):
  global nj_dict
  if len(nj_dict) == 0:
    read_unihan()
  if ch in nj_dict:
    return False
  return True

def has_none_japanese_unihan(word):
  for ch in word:
    if not is_japanese_unihan(ch):
      return True
  return False

def is_korean_unihan(ch):
  global nk_dict
  if len(nk_dict) == 0:
    read_unihan()
  if ch in nk_dict:
    return False
  return True

def has_none_korean_unihan(word):
  for ch in word:
    if not is_korean_unihan(ch):
      return True
  return False

# find hanja that is not japanese
def read_unihan():
  global nj_dict, nj_dict, nk_dict
  src = open("Unihan_IRGSources.txt", "r")
  last_code = ""
  num_nc = 0
  num_nj = 0
  num_nk = 0
  chinese = False
  japanese = False
  korean = False
  while True:
    line = src.readline().decode("utf-8")
    if not line: break
    line = line.strip()
    if line == "" or line.startswith("#"): continue

    tokens = line.split("\t")
    code = tokens[0]
    source = tokens[1]

    if last_code == "":
      last_code = code
      if source.startswith("kIRG_G"):
        chinese = True
      elif source.startswith("kIRG_J"):
        japanese = True
      elif source.startswith("kIRG_K"):
        korean = True
    elif last_code == code:
      if source.startswith("kIRG_G"):
        chinese = True
      elif source.startswith("kIRG_J"):
        japanese = True
      elif source.startswith("kIRG_K"):
        korean = True
    else:
      han = unichr(int(last_code[2:], 16))
      if not chinese:
        if han not in nc_dict:
          nc_dict[han] = 1
          num_nc += 1
      if not japanese:
        if han not in nj_dict:
          nj_dict[han] = 1
          num_nj += 1
      if not korean:
        if han not in nk_dict:
          nk_dict[han] = 1
          num_nk += 1
      chinese = False
      japanese = False
      korean = False
      if source.startswith("kIRG_G"):
        chinese = True
      elif source.startswith("kIRG_J"):
        japanese = True
      elif source.startswith("kIRG_K"):
        korean = True
      last_code = code

  src.close()

if __name__ == "__main__":
  zh1 =  is_chinese_unihan(u"说")  # U+8BF4 not in jk
  zh2 =  is_chinese_unihan(u"説")  # U+8AAC not in k
  zh3 =  is_chinese_unihan(u"說")  # U+8AAA not in j
  ja1 =  is_japanese_unihan(u"说")
  ja2 =  is_japanese_unihan(u"説")
  ja3 =  is_japanese_unihan(u"說")
  ko1 =  is_korean_unihan(u"说")
  ko2 =  is_korean_unihan(u"説")
  ko3 =  is_korean_unihan(u"說")
  print zh1, zh2, zh3, ja1, ja2, ja3, ko1, ko2, ko3 # shoule be TTT, FTF, F, F, T
