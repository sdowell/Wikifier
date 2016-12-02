from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics.pairwise import linear_kernel
from nltk.stem import PorterStemmer
from math import log10

if __name__ == "__main__":
	#twenty = fetch_20newsgroups()
	data = ["Hello WOrld", "hello world."]
	tfidf = TfidfVectorizer().fit_transform(data)
	print(tfidf)
	print(tfidf[0:1])
	cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
	print(cosine_similarities)
	related_docs_indices = cosine_similarities.argsort()[:-5:-1]
	print(related_docs_indices)
	print(cosine_similarities[related_docs_indices])

# class for calculating similarity ranking (using tf-idf)
class simRank:
	def __init__(self):
		return

	def rank(self, query, docs):
		docs.insert(0, query)
		ps = PorterStemmer()
		#for doc in docs:
		#docs = [" ".join([ps.stem(w) for w in doc.split()]) for doc in docs]
		tfidf = TfidfVectorizer().fit_transform(docs)
		cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
		#print(cosine_similarities)
		return cosine_similarities[1:]
	
	def sim():
		return

	def tf(query, docs):
		return
	
	def idf(query, docs):
		return

# class for calculating prior probability ranking
class priorProbRank:
	
	def __init__(self):
		return
	
	def rank(self, docs):
		if len(docs) == 0:
			return []
		sum = 0.0
		results = []
		for d in docs:
			pop = float(d)
			pop = log10(1+pop)
			#print(d)
			sum += pop
			results.append(pop)
		#max = docs[0].url
		if sum == 0:
			return [1.0 / float(len(docs)) for d in docs]
		for i in range(0,len(results)):
			results[i] = results[i] / sum
		return results
				
		
		

	#class for calculating coreference ranking
class corefRank:
	def __init__(self):
		return
		
	def rank(self, candidates, corefs):
		results = []
		sum = 0
		for c in candidates:
			rnk = 0
			for r in corefs:
				sim = len(set(c.links).intersection(r.links))
				sum += sim
				rnk += sim
			results.append(float(rnk))
		if sum == 0:
			return [1.0 / float(len(docs)) for c in candidates]
		for r in results:
			r = r / sum
		return results
	
