# Setup the word frequency dict.
import codecs
import os
import json
from itertools import product

def file_path(name):
  return os.path.join(os.path.dirname(__file__), name)


en_to_ar = json.loads(open(file_path('mapping.manual.json')).read())

NWORDS = {}
path = file_path('ar.txt')
word_counts = codecs.open(path, encoding='utf-8').read().split("\n")
for word_count in word_counts:
  if word_count:
    [word, n] = word_count.split()
    NWORDS[word] = int(n)

def sort_by_frequency(words):
  return sorted(words, key=lambda x: -1 if NWORDS.get(x) is None else NWORDS.get(x), reverse=True)


def transliterate_word(english):
  ret = set()

  def recur(letters, word, start=False):
    if len(letters) == 0:
      ret.add(word)
      return
    if start:
      table = en_to_ar['start']
    else:
      table = en_to_ar['other']
    max_key_len = len(max(list(table), key=len))
    for i in range(1, max_key_len + 1):
      l = letters[:i]
      if l in table:
        for ar in table[l]:
          recur(letters[i:], word + ar)

  recur(english, '', True)
  return ret

def transliterate(sentence, max=3, verbose=False):
  words = sentence.lower().split()
  rets = []
  for word in words:
    candidates = list(transliterate_word(word))

    if verbose:
      for word in candidates:
        print(word)

    freq_sort = sort_by_frequency(candidates)
    rets.append(freq_sort)

  # Take smallest of (word with least variations) or (max limit)
  shortest = min([len(ret) for ret in rets])
  shortest = max if shortest > max else shortest
  rets = [ret[:shortest] for ret in rets]

  # Generate list of strings from most to least likely
  combinations_list = list(product(*rets))
  combinations = []
  for combination in combinations_list:
    combinations.append(' '.join(combination))

  return combinations
