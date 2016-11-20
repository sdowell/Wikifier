import wikipedia
import threading
import time

threadLock = threading.Lock()


	


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

	def __init__(self):
		return
		
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