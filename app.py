import sys
from query import Query
from disambiguator import Disambiguator
import time
import string

def parseTrainFile(trainfile):
	print("Parsing training file...")
	with open(trainfile) as f:
		content = [line.split("\t") for line in f]
	return content
	
def transform(s):
	translator = str.maketrans({key: None for key in string.punctuation})
	return s.translate(translator)
	#s2 = s2.translate(translator)
	
	
def train(weights, trainfile):
	print("Training...")
	results = {}
	output = ["" for i in range(0,len(trainfile))]
	print(len(output))
	for w in weights:
		d = Disambiguator(w)
		pos = 0
		tot = 0
		count = 0
		for t in trainfile:
			#print(t)
			fname = "wise_data/document_1500/" + t[0] + ".txt"
			#print("Reading file: " + fname)
			with open(fname, 'r') as f:
				content = f.read()
			q = Query(content, str(t[3]))
			e = d.disambiguate(q, str(t[2]))
			#print("Answer: " + e)
			tot += 1
			#if its correct, add 1 to pos
			answer = transform(t[2])
			guess = transform(e)
			if answer.lower() == guess.lower():
				try:
					print("Success: query: " + str(t[3].encode("utf-8")) + " resolved to " + str(answer.encode("utf-8")))
				except:
					print("Success")
				pos += 1
			else:
				try:
					print("Failure: query: " + str(t[3].encode("utf-8")) + " resolved to " + str(guess.encode("utf-8")) + " correct answer: " + str(answer.encode("utf-8")))
				except:
					print("Failure")
			output[count] = t[0] + "\t" + t[1] + "\t" + e + "\t" + t[3] + "\n"
			count += 1
			if count % 50 == 0:
				acc = float(pos) / float(count)
				print(str(count) + ": " + str(acc))
		print("Failed searches: " + str(d.failedSearches))
		outfile = open(str(w) + ".txt", "w")
		for line in output:
			outfile.write(line)
		outfile.close()
			
		results[w] = pos
	return results

def main(argv):
	if len(argv) == 0:
		print("Expected trainfile")
		return
	trainfile = argv[0]
	traindata = parseTrainFile(trainfile)
	#print(traindata[0:10])
	weights = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
	data = traindata[0:50]
	t0 = time.clock()
	results = train([0.5], data)
	t1 = time.clock()
	total = t1 - t0
	print("Training Time: " + str(total))
	for r in results:
		acc = float(results[r]) / float(len(data))
		print(str(r) + ": " + str(acc))

if __name__ == "__main__":
	main(sys.argv[1:])
