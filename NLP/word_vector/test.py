from similarity.levenshtein import Levenshtein
from similarity.normalized_levenshtein import NormalizedLevenshtein
from similarity.cosine import Cosine
lev = Levenshtein()
nolev = NormalizedLevenshtein()
cosine = Cosine(4)
str1='I enjoy playing football'
str2='I love to play soccer'

print(lev.distance(str1,str2))
print('Levenshtein distance:')
print(nolev.similarity(str1,str2))
print('Cosine similarity:')
print(cosine.similarity(str1,str2))