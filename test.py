from WikiSearch import wikiSearch
import time
w = wikiSearch()

t0 = time.clock()
l = w.search("Michael Jordan")
t1 = time.clock()
total = t1 - t0
print(str(total))

for p in l:
	print(p.url)

d = w.page("Michael_Jordan_(disambiguation)")
print(d.url)