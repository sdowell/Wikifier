import sqlite3
import wikipedia
import pickle

class DataBase:

	def __init__(self):
		self.conn = sqlite3.connect('wiki.db')
		print("Opened database successfully")
		
	def select(self, url):
		cursor = conn.execute("SELECT PAGE FROM PAGES WHERE URL = '" + url + "'")
		#page = None
		#for row in cursor:
			#return cloudpickle.
		return
	
	def insert(self, page):
		conn.execute("INSERT INTO PAGES (URL,PAGE) VALUES ('" + url + "', 'public sale wikipedia page')")
		return

	def close(self):
		conn.commit()
		conn.close()
		return
		
	
	# categories, content, images, links, title, url, summary, 
if __name__ == "__main__":
	conn = sqlite3.connect('test.db')
	print("Opened database successfully")
	conn.execute("DROP TABLE PAGES")
	print("Table dropped successfully")
	conn.execute("CREATE TABLE PAGES (URL TEXT PRIMARY KEY NOT NULL, TITLE TEXT, SUMMARY TEXT, CONTENT TEXT, CATEGORIES BLOB, IMAGES BLOB, LINKS BLOB, REFS BLOB, PAGEID INT, PARENT_ID INT, REVISION_ID INT);")

	print("Table created successfully")
	wp = wikipedia.page("Michael Jordan")
	wps = pickle.dumps(wp)
	print(wp.references)
	print(pickle.dumps(wp.references))
	ins = "INSERT INTO PAGES (URL, TITLE, SUMMARY, CONTENT, CATEGORIES, IMAGES, LINKS, REFS, PAGEID, PARENT_ID, REVISION_ID) VALUES ('%s', '%s', '%s', '%s','%s', '%s', '%s', '%s', %d, %d, %d)" % (wp.url, wp.title, wp.summary, wp.content, sqlite3.Binary(pickle.dumps(wp.categories)), sqlite3.Binary(pickle.dumps(wp.images)), sqlite3.Binary(pickle.dumps(wp.links)), sqlite3.Binary(pickle.dumps(wp.references)), int(wp.pageid), int(wp.parent_id), int(wp.revision_id))
	conn.execute(ins)
	print("Inserted page successfully")
	cursor = conn.execute("SELECT * FROM PAGES")
	
	print("Select called successfully:")
	#print(cursor[0][0])
	#print(len(cursor))
	for row in cursor:
		print("URL = " + row[0])
		print("Title = " + row[1])
		print("Summary = " + row[2])
		print("Content = " + row[3])
		print("Categories = " + str(row[4]))
		print("Images = " + str(row[5]))
		print("Links = " + str(row[6]))
		print("References = " + str(row[7]))
		print("Pageid = " + row[8])
		print("Parent_id = " + row[9])
		print("Revision_id = " + row[10])
	conn.commit()

	conn.close()