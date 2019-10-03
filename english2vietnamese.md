# Vietnamese translation for English words
I will describe how to get vietnamese word(s) as translation of each english word.
An English word can be used as more than one pos(part-of-speech) and have more than one meanings.
An example sentence is needed to define meaning/pos of the word in enlish.
If an English word has only 1 pos and 1 meaning, it is easy to get the translation with on-line translator.
If an English word has multiple pos/meanings, we can get most popular translation by inputing the word to on-line translator.
For words with multiple pos/meanings, it is need to check multiple translations and determine one translation.

The best way of word2word translation is getting the word(s) mappings between two languages by inputing a sentence instead of a word with the neural machine tralslator. But there is no translator that provides this word(s) mappings.


## Manual translation without Vietamese language capability
1. prepare (word, key-example) tuple for translation
(once, They have a meeting once a week)

2. get a candidate from translators by typing word as input
Each translator outputs the most common candidates
(google outputs multiple candidates as well but they are too many and difficult to choose one.)

3. back translate the candidate to english for validation with translator or dictionary.
If the result is similar to the original english word then use the candidate as the translation.
We can use vietnamese to english dictionary if available. 

4. get candidates and choose one using dictionary if the back-translation is not okay
This may be the case when the word has multiple pos/meanings.
We should spend time to look up the dictionary and compare translations of multiple meanings.
Use the English-Vietnamese dictionary if English is the first language or Korean-Vietnamese dictionary if Korean is the first language.

5. back translate the candidate to english for validation (same as the step 3)


## Automating the translation
### Create a script for translation and back-translation of step 2, 3
There are web-scraping libraries to use for creating the translation script.


### Use pos-tagger for step 4, 5
If the source is only the (word, key-example) pair, it is need to find pos-tag of the word by NLP technology.
It is known that Stanford pos-tagger is one of the good NLP resource.
But it is not very correct and there are many error in finding pos-tag even for very simple sentences.

Usually a word with multiple pos-tag makes errors.
Cement in "The proportion of sand to cement used was three to one." is a noun but easy to mistake it as a verb.
https://dict.naver.com/vikodict/#/main

And also it is naturally hard to differenciate from verb and adjective and noun if a verb is used with -ing.
Hardworking in "he is hardworking and creative" is a adjective but hard to determine pos-tag.
Melting in "the ice is melting in the sun" is verb but hard to determine pos-tag.

Someone is usually pronoun in the dictionary but pos-tagger may take it noun instead of pronoun.

While in "Please be quiet while I am studying." is conjunction but pos-tagger may take it as preposition to differenciate subordinating conjunction from coordinating conjunction.


## On-line Resources
There are many on-line English dictionaries to check whether each English word has many meanings or not.

Glosbe is really helpful because it provides example sentences in both language for each translation.
* https://glosbe.com/vi/en/
* https://glosbe.com/en/vi/

Translators are helpful. Output is the translation of the most common meaning of the given word.
* https://translate.google.com/#view=home&op=translate&sl=en&tl=vi
* https://papago.naver.com/
* https://translate.kakao.com/

There are on-line Vietnamese dictionaries of non-Vietnam country. These are more helpful than the dictionaries of Vietnam because the meaning is explained in the mother tongue.
* https://dictionary.cambridge.org/dictionary/english-vietnamese/
* https://dict.naver.com/vikodict/#/main
* https://dic.daum.net/index.do?dic=vi&q=

There are 4 on-line English-Vietnamese Vietnamese-English dictionaries of Vietnam. Wiktionary can be regarded as one of these.
Dictionaries are not very helpful because they provide many different meanings of a given english word in vietnamese language, with which non-vietnamese cannot choose a most proper meaning.
* http://tratu.soha.vn/
* https://dict.laban.vn/
* https://tracau.vn/index.html
* https://vdict.com/
* https://vi.wiktionary.org/wiki/Trang_Ch%C3%ADnh

There is a dictionary list on Web.
* https://www.101languages.net/vietnamese/vietnamese-english-dictionary/


### Tips for using Vietnamese dictionary
There are cases that an English word cannot be found in the dictionary.
It is usually the case when there are multiple spells for an English word.
(catalog, catalogue; hardworking, hard-working; everyone, everybody; and so on)
