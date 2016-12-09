from query import Query
from wikisearch import WikiSearch
from ranking import simRank
from ranking import priorProbRank
from sklearn.neural_network import MLPRegressor
import mwclient
#from app import toAscii
import time


def getWikiName(url):
	return url.replace("https://en.wikipedia.org/wiki/", "")

	
class Disambiguator:
	
	def __init__(self, w, db, use_nn=False, trainfiles=None, ngrams=1):
		self.wiki = WikiSearch(db)
		self.simrank = simRank(ngrams)
		self.probrank = priorProbRank()
		self.weight = w
		self.failedSearches = 0
		self.use_nn = use_nn
		if use_nn == False:
			return
		self.NN = MLPRegressor(hidden_layer_sizes=(100,), batch_size=10, solver='lbfgs', activation='relu', tol=.0001)
		data = []
		target = []
		for t in trainfiles:
			with open(t) as f:
				content = f.readlines()
			for l in content:
				spl = l.split()
				data.append([float(spl[0]),float(spl[1])])
				target.append(int(spl[2]))
			f.close()
		self.train(data, target)
	
	def getRedirect(self, source):
		return self.wiki.getRedirect(source)
	
	def linearWeighting(self, pop, sim):
		return self.weight * pop + (1.0-self.weight) * sim
	
	def train(self, data, target):
		self.NN.fit(data, target)
		
	def neuralWeighting(self, pop, sim):
		return self.NN.predict([[pop,sim]])
	
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
		try:
			if truth is not None and self.getRedirect(truth).lower() not in [c.title.lower() for c in candidates]:
			#print(getRedirect(truth))
			#print(str([c.title for c in candidates]))
#			try:
#				print("Truth value (" + truth + ") not in " + str([c.url for c in candidates]))
#			except:
#				print("Couldn't find truth value for " + truth)
				self.failedSearches += 1
		except:
			print(truth)
			return ""
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
		tfidf = self.simrank.tfidf(query.context, [c.content for c in candidates])
		#print("Similarity")
		#print(similarity)
		rankings = {}
		best = candidates[0].url
		#twit_train = open("wise_trigramtrain.txt", 'a')
		for i in range(0,len(similarity)):
			#rankings[candidates[i].url] = self.weight * popularity[i] + (1.0-self.weight) * similarity[i]
			if self.use_nn:
				rankings[candidates[i].url] = self.neuralWeighting(popularity[i], similarity[i])
			else:
				rankings[candidates[i].url] = self.linearWeighting(popularity[i], similarity[i])
			#print("Pop: " + str(popularity[i]) + " Sim: " + str(similarity[i]) + " NN: " + str(self.neuralWeighting(popularity[i], similarity[i])) + " Linear: " + str(self.linearWeighting(popularity[i], similarity[i])))
			"""
			if candidates[i].title.lower() == self.getRedirect(truth).lower():
				#print(self.getRedirect(truth).lower() + " == "  + candidates[i].title.lower() + ": " + str(popularity[i]) + " " + str(similarity[i]))
				print(str(popularity[i]) + " " + str(similarity[i]) + " 1", file=twit_train)
			else:
				#print(self.getRedirect(truth).lower() + " =/= " + candidates[i].title.lower() + ": " + str(popularity[i]) + " " + str(similarity[i]))
				print(str(popularity[i]) + " " + str(similarity[i]) + " 0", file=twit_train)
				#train_str = train_str + str(popularity[i]) + " " + str(similarity[i]) + " 0\n"
			"""
			if rankings[candidates[i].url] > rankings[best]:
				best = candidates[i].url
		#twit_train.write(train_str)
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
		
