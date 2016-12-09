import sys
import argparse
from query import Query
from disambiguator import Disambiguator
import time
import string
import re
from nltk.corpus import stopwords
sws = stopwords.words("english")

def parseTrainFile(trainfile):
	print("Parsing training file...")
	with open(trainfile) as f:
		content = [line.split("\t") for line in f]
	return content

def parseContent(content):
	text = re.sub(r'[^a-zA-Z0-9]',' ', content)
	text = re.sub(r'\W*\b\w{1,3}\b', '', text)
	text = ' '.join([word for word in text.split() if word not in sws])
	return text
	
def transform(s):
	#translator = str.maketrans({key: None for key in string.punctuation})
	text = re.sub(r'[^a-zA-Z0-9]',' ', s)
	text = ' '.join([word for word in text.split()])
	return text
	#return str(s).translate(None, string.punctuation)#translator)
	#s2 = s2.translate(translator)
	
def toAscii(s):
	#text = re.sub(r'[^a-zA-Z0-9_]','', s)
	text = re.sub(r'[^\x00-\x7F]','', s)
	#text = ' '.join([word for word in text.split()])
	return text
	
def trainTwitter(weights, trainfile, db, ng):
	print("Training Twitter...")
	results = {}
	output = ["" for i in range(0,len(trainfile))]
	#print(len(output))
	fs = 0
	for w in weights:
		print("--------------------Solving for weight " + str(w) + "--------------------")
		if str(w) == "NN":
			d = Disambiguator(w, db, use_nn=True, trainfiles=["wise_trigramtrain.txt"], ngrams=ng)
		else:
			d = Disambiguator(w, db, ngrams=ng)
		pos = 0
		tot = 0
		count = 0
		for t in trainfile:
			#print(t)
			#print("Reading file: " + fname)
			#with open(fname, 'r') as f:
			#	content = parseContent(f.read())
				#print(content)
			content = parseContent(t[2])
			q = Query(content, str(t[1]))
			e = d.disambiguate(q, str(t[0]))
			#print("Answer: " + e)
			tot += 1
			#if its correct, add 1 to pos
			answer = transform(t[0])
			guess = transform(e)
			if answer.lower() == guess.lower():
			#	try:
			#		print("Success: query: " + toAscii(t[1]) + " resolved to " + toAscii(answer))
			#	except:
			#		print("Success")
				pos += 1
			#else:
			#	try:
			#		print("Failure: query: " + toAscii(t[1]) + " resolved to " + toAscii(guess) + " correct answer: " + toAscii(answer))
			#	except:
			#		print("Failure")
			#output[count] = t[0] + "\t" + t[1] + "\t" + toAscii(e) + "\t" + t[3] + "\n"
			count += 1
			if count % 50 == 0:
				acc = float(pos) / float(count)
				print(str(count) + ": " + str(acc))
		print("Failed searches: " + str(d.failedSearches))
		fs = d.failedSearches
		#outfile = open(str(w) + ".txt", "w")
		#for line in output:
		#	outfile.write(line)
		#outfile.close()
			
		results[w] = pos
		#break
	return (results, fs)
	
def train(weights, trainfile, db, ng):
	print("Training...")
	results = {}
	output = ["" for i in range(0,len(trainfile))]
	fs = 0
	#print(len(output))
	for w in weights:
		print("--------------------Solving for weight " + str(w) + "--------------------")
		if str(w) == "NN":
			d = Disambiguator(w, db, use_nn=True, trainfiles=["wise_trigramtrain.txt"], ngrams=ng)
		else:
			d = Disambiguator(w, db, ngrams=ng)
		pos = 0
		tot = 0
		count = 0
		for t in trainfile:
			#print(t)
			fname = "wise_data/document_1500/" + t[0] + ".txt"
			#print("Reading file: " + fname)
			with open(fname, 'r') as f:
				content = parseContent(f.read())
				#print(content)
			q = Query(content, str(t[3]))
			e = d.disambiguate(q, str(t[2]))
			#print("Answer: " + e)
			tot += 1
			#if its correct, add 1 to pos
			answer = transform(t[2])
			guess = transform(e)
			if d.getRedirect(answer).lower() == guess.lower():
				#try:
					#print("Success: query: " + toAscii(t[3]) + " resolved to " + toAscii(answer) + "\n")
				#except:
				#	print("Success")
				pos += 1
			#else:
				#try:
				#	print("Failure: query: " + toAscii(t[3]) + " resolved to " + toAscii(guess) + " correct answer: " + toAscii(answer) + "\n")
				#except:
				#	print("Failure")
			output[count] = t[0] + "\t" + t[1] + "\t" + toAscii(e) + "\t" + t[3] + "\n"
			count += 1
			if count % 50 == 0:
				acc = float(pos) / float(count)
				print(str(count) + ": " + str(acc))
		print("Failed searches: " + str(d.failedSearches))
		fs = d.failedSearches
		outfile = open(str(w) + ".txt", "w")
		for line in output:
			outfile.write(line)
		outfile.close()
	
		results[w] = pos
		#break
	return (results, fs)

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--twitter", help="file holding twitter dataset")
	parser.add_argument("-w", "--wise", help="file holding wise dataset")
	parser.add_argument("-d", "--database", help="name of database file")
	parser.add_argument("-g", "--weights", help="comma delimited list of weights")
	parser.add_argument("-n", "--neuralnet", help="use neural network model for ranking", action="store_true")
	parser.add_argument("-p", "--printfile", help="print output to file")
	parser.add_argument("-k", "--ngrams", help="print output to file")
	args = parser.parse_args()
	db = "wikipedia.db"
	ngrams = 1
	if args.printfile:
		outfile = open(args.printfile, "w")
	if args.database:
		db = args.database
	weights = []
	if args.weights:
		weights = [float(w) for w in args.weights.split(",")]
	if args.neuralnet:
		weights.append("NN")
	elif len(weights) == 0:
		weights = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
	if args.ngrams:
		ngrams = int(args.ngrams)
	if args.twitter:
		trainfile = args.twitter
		traindata = parseTrainFile(trainfile)
		#print(traindata[0:10])
		#weights = [0.05,.06,.07,.08,.09,.1,.11,.12,.13,.14,.15]
		data = traindata
		t0 = time.clock()
		results, fs = trainTwitter(weights, data, db, ngrams)
		t1 = time.clock()
		total = t1 - t0
		print("Training Time: " + str(total))
		print("Twitter accuracy results:")
		accs = []
		for w in weights:
			if w in results:
				acc = float(results[w]) / float(len(data) - fs)
				print(str(w) + ": " + str(acc))
				accs.append(str(acc))
		print(" ".join(accs))
		if args.printfile:
			print(" ".join(accs), file = outfile)
	if args.wise:
		trainfile = args.wise
		traindata = parseTrainFile(trainfile)
		#print(traindata[0:10])
		#weights = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
		data = traindata[:355]
		t0 = time.clock()
		results, fs = train(weights, data, db, ngrams)
		t1 = time.clock()
		total = t1 - t0
		print("Training Time: " + str(total))
		print("WISE accuracy results:")
		accs = []
		for w in weights:
			if w in results:
				acc = float(results[w]) / float(len(data) - fs)
				print(str(w) + ": " + str(acc))
				accs.append(str(acc))
		print(" ".join(accs))
		if args.printfile:
			print(" ".join(accs), file = outfile)
	return
	if len(argv) == 0:
		print("Expected trainfile")
		return
	trainfile = argv[0]
	traindata = parseTrainFile(trainfile)
	#print(traindata[0:10])
	weights = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
	data = traindata[0:355]
	t0 = time.clock()
	results = train(weights, data)
	t1 = time.clock()
	total = t1 - t0
	print("Training Time: " + str(total))
	for w in weights:
		if w in results:
			acc = float(results[w]) / float(len(data))
			print(str(w) + ": " + str(acc))
#	for r in results:
#		acc = float(results[r]) / float(len(data))
#		print(str(r) + ": " + str(acc))

if __name__ == "__main__":
	main(sys.argv[1:])
