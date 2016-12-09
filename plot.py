import matplotlib.pyplot as plt
import argparse
import numpy as np

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", help="input file")
	parser.add_argument("-o", "--output", help="output file name")
	args = parser.parse_args()
	input = "acc.txt"
	if args.input:
		input = args.input
	output = "linear.png"
	if args.output:
		output = args.output
		if output[-4:] != ".png":
			output = output + ".png"
	with open(input) as f:
		l = f.readlines()
	twitter_xvals = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
	twitter_yvals = [0.577, 0.586, 0.620, 0.642, 0.665, 0.679, 0.662, 0.656, 0.620, 0.518, 0.276]
	twitter_yvals = [float(f) for f in l[0].split()]
	twitter_nnval = 0.64957
	wise_xvals = [0.0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]
	wise_yvals = [0.651, 0.651, 0.654, 0.651, 0.640, 0.640, 0.640, 0.625, 0.6, 0.597, 0.566]
	wise_yvals = [float(f) for f in l[1].split()]
	wise_nnval = 0.8143
	#plt.subplot(1,2,1)
	#plt.title("Twitter Accuracy")
	plt.title("Linear Combination")
	#plt.ylim([0,1])
	plt.ylabel("Accuracy")
	plt.xlabel("Alpha")
	plt.xticks(np.arange(0, 1.1, 0.1))
	#plt.yticks(np.arange(0, 1.1, 0.1))
	plt.plot(twitter_xvals, twitter_yvals)
	#plt.subplot(1,2,2)
	#plt.title("WISE Accuracy")
	plt.ylabel("Accuracy")
	plt.xlabel("Alpha")
	plt.plot(wise_xvals, wise_yvals)
	
	plt.legend(["Twitter", "WISE"])
	plt.savefig(output)
	exit()
	plt.plot("NN", twitter_nnval)
	plt.plot("NN", wise_nnval)
	plt.savefig("nn.png")