import wikipedia
import threading
import time
import mwclient
from wikipage import WikiPage
import re
from database import MyQuery, MyWikiPage, Base, Redirect, create
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from nltk.corpus import stopwords


threadLock = threading.Lock()
	
#returns true if source redirects to dest, else false
def redirectsTo(source, dest):
	site = mwclient.Site('en.wikipedia.org')
	page = site.pages[source]
	page = page.resolve_redirect()
	if page.page_title == dest:
		return True
	return False


class myThread (threading.Thread):
	def __init__(self, pages, request):
		threading.Thread.__init__(self)
		self.pages = pages
		self.request = request
	def run(self):
		#print "Starting " + self.name
		# Get lock to synchronize threads
		try:
			p = wikipedia.page(self.request)
			threadLock.acquire()
			self.pages.append(p)
			#print_time(self.name, self.counter, 3)
			# Free lock to release next thread
			threadLock.release()
		except:
			pass



class WikiSearch:

	def __init__(self, db=None):
		if db is None:
			#self.engine = create_engine('sqlite:///wikipedia.db')
			db = "wikipedia.db"
		create(db)
		self.engine = create_engine('sqlite:///' + db)
		Base.metadata.bind = self.engine
		DBSession = sessionmaker(bind = self.engine)	
		self.session = DBSession()
		return
		
	def getRedirect(self, source):
		row = self.session.query(Redirect).filter(Redirect.originalPage == source).first()
		if row == None:
			site = mwclient.Site('en.wikipedia.org')
			page = site.pages[source]
			page = page.resolve_redirect()
			rd = Redirect(originalPage=source, redirectPage=page.page_title)
			self.session.add(rd)
			self.session.commit()
			return page.page_title
		else:
			return row.redirectPage
		
	def search(self, query):
		results = wikipedia.search(query)
		pages = []
		threads = []
		for r in results:
			t = myThread(pages, r)
			t.start()
			threads.append(t)
			#try:
			#	p = wikipedia.page(r)
			#	pages.append(p)
			#except:
			#	print("Couldn't find entry for " + r)
			#	continue
		for thread in threads:
			thread.join()
		return pages
	
	def dbSearch(self, q):
		query = re.sub(' +',' ', q)

		row = self.session.query(MyQuery).filter(MyQuery.input == query).first()
		if row == None:
			#print(query + " not found in local DB")
			newquery = MyQuery(input=query)
			pgs = self.mwSearch(query)
			#print("Done quering mediawiki")
			for pg in pgs:
				dbpage = self.session.query(MyWikiPage).filter(MyWikiPage.pageid == pg.pageid).first()
				if dbpage is None:
					dbpage = MyWikiPage(pageid = pg.pageid, title = pg.title, url = pg.url, isDisambiguation = pg.isDisambiguation, content = pg.content, outlinks = pg.outlinks, inlinks = pg.inlinks)
				newquery.wikipages.append(dbpage)
			self.session.add(newquery)
			self.session.commit()
			return newquery.wikipages
		else:
			#print(query + " found in local DB")
			return row.wikipages
	
	def mwSearch(self, q):
		query = re.sub(' +',' ', q)
		query = query.replace("]", "")
		#print("mwSearch: " + query + " (disambiguation)")
		site = mwclient.Site('en.wikipedia.org')
		page = site.pages[query + " (disambiguation)"]
		page = page.resolve_redirect()
		results = []
		ids = {}
		if page.exists:
			d = WikiPage(page)
			for l in d.outlinks:
				newpage = site.pages[l]
				newpage = newpage.resolve_redirect()
				if newpage.exists:
					if newpage.pageid in ids:
						#print("Page already in corpus")
						continue
					np = WikiPage(newpage)
					if np.pageid not in ids and not np.isDisambiguation:
						results.append(np)
						ids[np.pageid] = 1
		page = site.pages[query + " (surname)"]
		page = page.resolve_redirect()
		if page.exists:
			d = WikiPage(page)
			if d.isDisambiguation:
				for l in d.outlinks:
					newpage = site.pages[l]
					newpage = newpage.resolve_redirect()
					if newpage.exists:
						if newpage.pageid in ids:
							#print("Page already in corpus")
							continue
						np = WikiPage(newpage)
						if np.pageid not in ids and not np.isDisambiguation:
							results.append(np)
							ids[np.pageid] = 1
		#print([r.title for r in results])
		#print("mwSearch: " + query)
		page = site.pages[query]
		page = page.resolve_redirect()
		if page.exists:
			d = WikiPage(page)
			if not d.isDisambiguation and d.pageid not in ids:
				results.append(d)
				#print("results for " + query)
				#print([r.title for r in results])
				return results
			elif not d.isDisambiguation:
				#print("results for " + query)
				#print([r.title for r in results])
				return results
			#print("outlinks for " + d.title)
			#print(d.outlinks)
			#print("Treating " + query + " as disambiguous")
			for l in d.outlinks:
				newpage = site.pages[l]
				newpage = newpage.resolve_redirect()
				if newpage.exists:
					if newpage.pageid in ids:
						#print("Page already in corpus")
						continue
					np = WikiPage(newpage)
					if np.pageid not in ids and not np.isDisambiguation:
						results.append(np)
						ids[np.pageid] = 1
		#print("results for " + query)
		#print([r.title for r in results])
		
		return results
		
		
	def serialSearch(self, query):
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
if __name__ == "__main__":
	ws = WikiSearch()
	r = ws.page("George W. Bush")
	gwblinks = r.links
	r = ws.page("Al Gore")
	aglinks = r.links
	print(set(gwblinks).intersection(aglinks))
	print([p.title for p in r])
	print([p.isDisambiguation for p in r])
	#print([p.outlinks for p in r])
	exit()
	t0 = time.clock()
	ws.search("Michael Jordan")
	t1 = time.clock()
	total = t1 - t0
	print("Parallel time: " + str(total))
	t0 = time.clock()
	ws.serialSearch("Michael Jordan")
	t1 = time.clock()
	total = t1 - t0
	print("Serial time: " + str(total))