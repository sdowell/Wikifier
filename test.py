#from wikisearch import WikiSearch
import time
import string
import mwclient
import re


#import nltk
from nltk.corpus import stopwords
#nltk.download("stopwords")
#exit()
sws = stopwords.words("english")
#print(sws)
site = mwclient.Site('en.wikipedia.org')
page = site.pages["NBA"]
t0 = time.clock()
l1 = len(list(page.backlinks()))
t1 = time.clock()
total = t1 - t0
print("Result: " + str(l1))
print("Len function: " + str(total))
t0 = time.clock()
l2 = sum([1 for b in page.backlinks()])
t1 = time.clock()
total = t1 - t0
print("Result: " + str(l2))
print("Comprehension function: " + str(total))
exit()
#search = site.pages("Mrs Clinton")
#print(search)
#print(dir(search))
#for r in search:
#	print(r["title"])
#	print(dir(r))
#exit()
print(dir(site.search("student of the year")))
for p in site.ask("student of the year"):
	print(dir(p))
print([p.page_title for p in site.search("student of the year")])

exit()
page = site.pages['Michael Jordan (disambiguation)']
print(dir(page))
"""print page.can
print page.contentmodel
print page.name
print page.namespace
print page.normalize_title
print page.page_title
print page.pageid
print page.site
"""
outlinks = [l.page_title for l in page.links()]
links = page.links()
for l in links:
	print(l.page_title)
exit()
backlinks = page.backlinks(generator=False)
print(len(backlinks))
print(backlinks.count)
print(backlinks)
print(dir(backlinks))
for op in dir(backlinks):
	try:
		print(str(op) + ": " + str(backlinks[op]))
	except:
		pass
exit()
print(str(sum([1 for b in page.backlinks()])))
print([l.page_title for l in links])
#for link in links:
#	print(link.page_title)

print(page.categories(generator=False))
for c in page.categories():
	print(c.page_title)
exit()
page = page.resolve_redirect()
text = page.text()
text = re.sub(r'[^a-zA-Z0-9]',' ', text)
text = re.sub(r'\W*\b\w{1,3}\b', '', text)
text = ' '.join([word for word in text.split() if word not in sws])
print(text)
links = page.links()
#for link in links:
#	print(link)
exit()
bls = page.backlinks(generator=False)
print(bls)
print(dir(bls))
count = 0
print("Backlinks: " + str((bls.get_list())))
for bl in bls:
	print(bl.title())
	count += 1
print("Backlinks: " + str(count))

exit()
text = re.sub(r'[^a-zA-Z0-9\n]',' ', text)
#page = site.pages['Michael Jordan (disambiguation)']
#print(text)
links = page.links()
print(links)
print(dir(links))
print(links.get_list())
#links = links.get_list()
#for link in links:
	#print(link.backlinks().count)
#print(str(page.iwlinks()))

exit()

w = WikiSearch()

t0 = time.clock()
#l = w.search("Michael Jordan")
t1 = time.clock()
total = t1 - t0
print(str(total))

#for p in l:
#	print(p.url)

s = 'string with "punctuation" inside of it! Does this work? I hope so.'

d = w.page("Michael Jordan")
#translator = str.maketrans({key: None for key in string.punctuation})
#d.content.translate(translator)
#print(s.translate(translator))
#print(d.content.translate(translator).encode("utf-8"))
