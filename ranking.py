from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.metrics.pairwise import linear_kernel

twenty = fetch_20newsgroups()

tfidf = TfidfVectorizer().fit_transform(twenty.data)
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
		tfidf = TfidfVectorizer().fit_transform(docs)
		cosine_similarities = linear_kernel(tfidf[0:1], tfidf).flatten()
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

	#class for calculating coreference ranking
class corefRank:
	def __init__(self):
		return
