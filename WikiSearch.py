import wikipedia

class wikiSearch:

	def __init__(self):
		return
		
	def search(query):
		results = wikipedia.search(query)
		pages = []
		for r in results:
			try:
				p = wikipedia.page(r)
				pages.append(p)
			except:
				continue
		return pages
		
	def page(query):
		try:
			p = wikipedia.page(query)
			return p
		except:
			return NULL
