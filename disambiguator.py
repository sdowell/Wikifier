from query import Query
from wikisearch import WikiSearch
from ranking import simRank
from ranking import priorProbRank

class Disambiguator:

	self.weight = .5
	self.wiki = WikiSearch()
	self.simrank = simRank()
	self.probrank = priorProbRank()
	
	def __init__(self, w):
		self.weight = w
		
	def disambiguate(self, query):
		candidates = self.wiki.search(query.entity)
		rankings = {}
		for c in candidates:
			rankings[c.url] = 0
		
		popularity = probrank.rank(query, candidates)
		similarity = simrank.rank(query, candidates)
		rankings = {}
		for i in range(0,len(popularity)):
			rankings[candidates[i]] = popularity * w + similarity * (1 - w)
		return rankings
		
