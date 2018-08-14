# English to other multiple language Word to Word Dictionary
Vocabulary learning is one of the first thing to do for learning any foreign language because it is the process acquiring building blocks in second language acquisition.
Flash cards are helpful for learning and memorizing things that are simple but numerous, like vocabulary.
When we create bilingual flash cards for vocabulary, the one side of the card will be a foreign word and an image like 
http://www.eslkidslab.com/flashcards/set2/toyflashcards/toys%20flashcardsmall0000.jpg, and the other side will be the equivalant word in native language.
Because example usage of the word is also helpful for vocabulary learning, we need structured data as below.
* Foreign word (text)
  * meaning of the word (image)
  * example phrases/sentences in foreign language (text + image)
  * level of word (from difficulty and frequency)
  * equivalant word(s) in native language (text)

If we build English vocabulary contents for multiple other native languages.
Then the first three records will be the same for all native languages.
Only the fourth records are different for each language.
It is not the lengthy explanation of the English that can be seen in the dictionary book.
For multiple native languages, preparing the third column will be the most time consuming.
I am going to build English dictionaries for multiple other languages in programmatic way for the third record.
Japanese is the first and other asian languages will be followed.

## Homograph and Polysemes (from the definition of wikipedia)
Homographs are words that have two or more different meanings.
Two types of homographs are homonym and heteronym, distinguished by the prononciation.
An example of homonym is tire and an example of heteronym is desert.
A polyseme is a word or phrase with different, but related senses.
Offline dictionaries have sepereted entry for homographs and unified entry for polysemes.
But some online dictionary like Wiktionary does not follow this policy, it has only one entry for homograph.
Though the former policy is better for vocabulary learning, it is assumed that the homograph policy is post-processed manually in this project.
So there will be only one entry for each homograph and the meanings will be unified, for the time being.

## Software requiremants of the projects
* Language utilities for the native/foreign language (Japanese, English)
  * alphabet check, symbol replacement, locale, etc.,
* Scraping on-line dictionaries
  * english dictionary which has japanese translation (wiktionary)
  * japanese dictionary (wiktionary, koto, weblio)
* Translation(equivalant word) extractor
  * extract native explanations for each word of the foreign language
    * 1 or more etymologies
      * 1 or more pos's(part of speech)
        * 1 or more corresponding native words
  * elect short representative words from many candidates
  * neet to process special symbols to connect each meaning (, : ;) in dictionaries
  * need to define policy for choosing representative word
    * common policy is choosing short word
    * preferences for japanese are kanji > hiragana > katagana > english

## Dependencies (external resources)
### wikt2dict https://github.com/juditacs/wikt2dict
The document format for wiktionary is wikimedia.
English wikitionary in xml file can be downloaded from the wikimedia archive.
With wikt2dict, we can get xml parsed wikimedia files for multiple languages at once.
However, it is needed to add some code in config.py for downloading wiktionary of asian countries.

### Unihan_IRGSources.txt
Wiktionary is user-generated dictionary and thus it has lots of errors.
One type of error for Japanese string is using wrong kanji, which is usually from Chinese simplified character set.
The file has the information about the dictionary source of each han character for each asian country.
We can check for each unified han character whether they are used in Japanese or not with the file.
The file is included in the following zip file. http://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip

### Online Japanese dictionaries (for English words)
There is possibility that we cannot get all translation from the Wiktionary.
We can use online Japanese dictionary services for English words.
Because this project needs short translating words, one service has selected and prepared for crawling.

## Translation examples
Japanese equivalent words will be provided by this project as the table below.
Meanings of homograph will be unified by one word as the row for the word 'bear'.

English word | Japanese equivalent words
------------ | ------------
a.m. | 午前
abdominal | 腹の,腹筋
bear | 支える,クマ

## How to use
1. download python files.
2. create a sub directory /words and put a text file all_words.csv where each line has a english word to be translated.
3. prepare dictionaries in plain text
   * create a sub directory /dict for the dictionary
   * put english and japanese wiktionary (with wikt2dict).
   * crawl online Japanese dictionary by executing crawl_jdict.py
4. extract translations from each dictionary
   * extract translation from wiktionary by executing extract_trans_enwikt.py and extract_trans_jawikt.py
   * extract translation from online dictionary by executing extract_trans_jdict.py
5. build the output dictionary that has simple equivalent Japanese words for each English word
   * create a sub directory /out
   * elect equivalent words from traslations by executing elect_words.py
   * build a English2Japanese word to words output dictionary by executing build_jd_jw_ew.py

## Caveats
* Finding wrong Chinese character is done automatically but correcting should be done manually.
* Differenct punctuation marks are used in different dictionaries or different entries of dictionary. They should be normalized.

## License
To be determined.
