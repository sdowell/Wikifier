import mwclient
import re
from nltk.corpus import stopwords
sws = stopwords.words("english")

class WikiPage:

	def __init__(self, page):
		#page = page.resolve_redirect()
		self.title = page.page_title
		#print("Recording " + self.title)
		self.url = self.constructURL(self.title)
		self.pageid = page.pageid
		categories = page.categories()
		self.isDisambiguation = False
		for c in categories:
			#print(c.page_title)
			if c.page_title.lower() == "disambiguation pages":
				self.isDisambiguation = True
				#print(self.title + " is disambiguous due to category:disambiguation pages")
			elif c.page_title.lower() == "surnames":
				self.isDisambiguation = True
				#print(self.title + " is disambiguous due to category:surnames")
			elif c.page_title.lower() == "given names":
				self.isDisambiguation = True
				#print(self.title + " is disambiguous due to category:given names")
		#print("Reading Content")
		self.content = self.parseContent(page.text(cache=False))
		#print("Reading outlinks")
		self.outlinks = [l.page_title for l in page.links()]
		self.inlinks = 0
		if not self.isDisambiguation:
			#print("Reading inlinks")
			self.inlinks = len(list(page.backlinks()))
			"""
			self.inlinks = 0
			for b in page.backlinks():
				self.inlinks += 1
				if self.inlinks >= 10000:
					break
					"""
			#print(self.title + " Inlinks: " + str(self.inlinks))
		return
			
	def parseContent(self, content):
		#text = re.sub(r'[^a-zA-Z0-9]',' ', content)
		#text = re.sub(r'\W*\b\w{1,3}\b', '', text)
		text = re.sub(r'[^\x00-\x7F]',' ', content)
		text = ' '.join([word for word in text.split() if word not in sws])
		return text
		
	def constructURL(self, title):
		return "https://en.wikipedia.org/wiki/" + title.replace(" ", "_")
		
if __name__ == "__main__":
	exit()