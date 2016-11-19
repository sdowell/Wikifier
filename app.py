import sys

def parseTrainFile(trainfile):
	with open(trainfile) as f:
		content = [x.split("\t") for line in f]
	return content
	

def train(weights, trainfile):
	return

def main(argv):
	if len(argv) == 0:
		print("Expected trainfile")
		return
	trainfile = argv[0]
	traindata = parseTrainFile(trainfile)
	print(traindata)
	weights = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
	train(weights, trainfile)

if __name__ == "__main__":
	main(sys.argv[1:])
