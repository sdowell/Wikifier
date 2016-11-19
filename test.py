import WikiSearch

w = wikiSearch()

l = w.search("Michael Jordan")

for p in l:
    print p.url

