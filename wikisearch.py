import wikipedia

class WikiSearch:

	def __init__(self):
		return
		
	def search(self, query):
		results = wikipedia.search(query)
		pages = []
		for r in results:
			try:
				p = wikipedia.page(r)
				pages.append(p)
			except:
				print("Couldn't find entry for " + r)
				continue
		return pages
		
	def page(self, query):
		try:
			p = wikipedia.page(query)
			return p
		except:
			return NULL
