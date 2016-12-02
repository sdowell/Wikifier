import sqlite3
import wikipedia
import pickle
import argparse
#from wikisearch import WikiSearch
from sqlalchemy import Table, Column, ForeignKey, Integer, String, PickleType, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import exists
Base = declarative_base()

query_results = Table('query_results', Base.metadata, Column('query_id', ForeignKey('queries.input'), primary_key=True), Column('page_id', ForeignKey('wikipages.pageid'), primary_key=True) )

class MyQuery(Base):
	__tablename__ = 'queries'
	
	input = Column(Text, primary_key=True)
	
	wikipages = relationship('MyWikiPage', secondary=query_results, back_populates='queries')
	
class MyWikiPage(Base):
	__tablename__ = 'wikipages'
	
	pageid = Column(Integer, primary_key=True)
	
	queries = relationship('MyQuery', secondary=query_results, back_populates='wikipages')
	
	title = Column(String(250))
	url = Column(String(250))
	isDisambiguation = Column(Boolean)
	content = Column(Text)
	outlinks = Column(PickleType)
	inlinks = Column(Integer)

class Redirect(Base):
	__tablename__ = 'redirects'
	
	originalPage = Column(String(250), primary_key=True)
	redirectPage = Column(String(250))
	
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
		
def create(name):
	#print(name[-3:])
	if name[-3:] != ".db":
		name = name + ".db"
	engine = create_engine('sqlite:///' + name)
	Base.metadata.create_all(engine)
	# categories, content, images, links, title, url, summary, 
if __name__ == "__main__":
	#sqlalchemy
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--create", help="create database file (default: reddit.db)")
	args = parser.parse_args()
	if args.create:
		create(args.create)
	exit()
	create()
	exit()
	engine = create_engine('sqlite:///sqlalchemy_example.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind = engine)
	
	session = DBSession()

	ws = WikiSearch()
	query = "WSJ"
	row = session.query(MyQuery).filter(MyQuery.input == query).first()
	if row == None:
		print("WSJ not found in table")
		newquery = MyQuery(input=query)
		pgs = ws.mwSearch(query)
		print("Done quering mediawiki")
		for pg in pgs:
			dbpage = session.query(MyWikiPage).filter(MyWikiPage.pageid == pg.pageid).first()
			if dbpage is None:
				dbpage = MyWikiPage(pageid = pg.pageid, title = pg.title, url = pg.url, isDisambiguation = pg.isDisambiguation, content = pg.content, outlinks = pg.outlinks, inlinks = pg.inlinks)
			newquery.wikipages.append(dbpage)
		session.add(newquery)
	else:
		print("WSJ found in table")
		print(row.wikipages[0].content)
		for pg in row.wikipages:
			try:
				print(pg.title)
			except:
				pass
	#print(exists().where(MyQuery.input == query))#session.query(MyQuery).filter(MyQuery.input == query))
	#print "Times found in db"
	query = "Clinton"
	row = session.query(MyQuery).filter(MyQuery.input == query).first()
	if row == None:
		print("Clinton not found in table")
	else:
		print("Clinton found in table")
	#print "Clinton found in db"
	session.commit()
	exit()
	#sqlite
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