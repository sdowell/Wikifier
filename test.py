from WikiSearch import wikiSearch
import time
import string
w = wikiSearch()

t0 = time.clock()
#l = w.search("Michael Jordan")
t1 = time.clock()
total = t1 - t0
print(str(total))

#for p in l:
#	print(p.url)

s = 'string with "punctuation" inside of it! Does this work? I hope so.'

d = w.page("Michael Jordan")
translator = str.maketrans({key: None for key in string.punctuation})
#d.content.translate(translator)
print(s.translate(translator))
print(d.content.translate(translator).encode("utf-8"))
