from query import Query
from wikisearch import WikiSearch
from ranking import simRank
from ranking import priorProbRank
import mwclient
#from app import toAscii
import time

def getWikiName(url):
	return url.replace("https://en.wikipedia.org/wiki/", "")

	
class Disambiguator:
	
	def __init__(self, w, db):
		self.wiki = WikiSearch(db)
		self.simrank = simRank()
		self.probrank = priorProbRank()
		self.weight = w
		self.failedSearches = 0
	
	def getRedirect(self, source):
		return self.wiki.getRedirect(source)
	
	def disambiguate(self, query, truth=None):
		try:
			st = str(query.entity.encode("utf-8"))
			#print("Disambiguating " + str(query.entity.encode("utf-8")))
		except:
			#print("Disambiguating: [unprintable entity]")
			return ""
		#t0 = time.clock()
		candidates = self.wiki.dbSearch(query.entity)
		if len(candidates) == 0:
			self.failedSearches += 1
#			print("Truth value (" + truth + ") not in " + str([c.url for c in candidates]))
			return ""
#		if truth is not None and truth.lower() not in [getWikiName(c.url).lower() for c in candidates]:
		if truth is not None and self.getRedirect(truth).lower() not in [c.title.lower() for c in candidates]:
			#print(getRedirect(truth))
			#print(str([c.title for c in candidates]))
#			try:
#				print("Truth value (" + truth + ") not in " + str([c.url for c in candidates]))
#			except:
#				print("Couldn't find truth value for " + truth)
			self.failedSearches += 1
		#t1 = time.clock()
		#total = t1 - t0
		#print("Search Time: " + str(total))
		#print("Candidates:")
		#print([c.url for c in candidates])
		#rankings = {}
		#for c in candidates:
		#	rankings[c.url] = 0
		
		#popularity = self.probrank.rank([c.references for c in candidates])
		ref = []
		for c in candidates:
			try:
				ref.append(c.inlinks)
			except:
				ref.append([])
		popularity = self.probrank.rank(ref)
		#print("Popularity")
		#print(popularity)
		similarity = self.simrank.rank(query.context, [c.content for c in candidates])
		#print("Similarity")
		#print(similarity)
		rankings = {}
		best = candidates[0].url
		for i in range(0,len(similarity)):
			rankings[candidates[i].url] = self.weight * popularity[i] + (1.0-self.weight) * similarity[i]
			if rankings[candidates[i].url] > rankings[best]:
				best = candidates[i].url
		#print("URL: " + best)
		name = getWikiName(best)
		#print(name)
		return getWikiName(best)
		best = candidates[0].url
		for key in rankings:
			if rankings[key] > rankings[best]:
				best = key
		print("URL: " + best)
		return getWikiName(best)
		
