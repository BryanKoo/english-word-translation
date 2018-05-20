#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib
import pdb 
import sys
import time
import random
reload(sys)
sys.setdefaultencoding('utf-8')

# https://kotobank.jp/ejword/abjure
def query_jdict1(word):
  url = "https://kotobank.jp/ejword/" + word
  resp = urllib.urlopen(url).read()
  soup = BeautifulSoup(resp, "lxml")
  divs = soup.find_all("div", attrs={'class': 'word_foreign'}) 
  text = ""
  for div in divs:
    if div.text.strip() != "":
      text += div.text.strip() + "\n"
  return text.strip()

# https://dictionary.goo.ne.jp/word/en/abjure
# blocked
def query_jdict2(word):
  url = "https://dictionary.goo.ne.jp/word/en/" + word
  resp = urllib.urlopen(url).read()
  soup = BeautifulSoup(resp, "lxml")
  lis = soup.find_all("li", attrs={'class': 'in-ttl-b text-indent'})  # mixed class not working
  text = ""
  for li in lis:
    text += li.text.strip() + "\n"
  return text.strip()

# https://eow.alc.co.jp/search?q=abjure
# too many items, complex
def query_jdict3(word):
  url = "https://eow.alc.co.jp/search?q=" + word
  resp = urllib.urlopen(url).read()
  soup = BeautifulSoup(resp, "lxml")
  span = soup.find("span", attrs={'class': 'wordclass'}) 
  text = span.text
  return text.strip()

# https://ejje.weblio.jp/content/abjure
# not good for homographs (check out 'bear')
def query_jdict4(word):
  url = "https://ejje.weblio.jp/content/" + word
  resp = urllib.urlopen(url).read()
  soup = BeautifulSoup(resp, "lxml")
  td = soup.find("td", attrs={'class': 'content-explanation'}) 
  text = td.text
  pdb.set_trace()
  return text.strip()

def extract_jdict(wordfile):
  num_word = 0
  num_found_dict1 = 0
  num_not_found = 0
  src = open(wordfile, "r")
  dst = open("dict/koto_dict.txt", "w")
  while True:
    line = src.readline().decode("utf-8")
    if not line: break
    word = line.strip()
    if word == "": continue
    found = False
    num_word += 1
 
    result1 = query_jdict1(word)
 
    if result1 != "":
      found = True
      num_found_dict1 += 1
      dst.write(word + "|||\n")
      dst.write(result1 + "\n")
      print str(num_word), word
    if not found:
      num_not_found += 1
      print str(num_word), word
    time.sleep(random.randint(3,6))

  src.close()
  dst.close()
  print "num_word: " + str(num_word)
  print "num_found_dict1: " + str(num_found_dict1)
  print "num_not_found: " + str(num_not_found)

if __name__ == "__main__":
  extract_jdict('words/all_words.csv')
