import matplotlib.pyplot as plt

def showHeurPlot(answerChain, algo):
	dataX = list(range(len(answerChain)))
	dataF = [el.F for el in answerChain]
	dataH = [el.H for el in answerChain]
	dataG = [el.G for el in answerChain]
	if algo == 'aStar':
		plt.plot(dataX, dataG, 'ob', label='G')
		plt.plot(dataX, dataF, 'or', label='F')
		plt.plot(dataX, dataH, 'og', label='H')
	if algo == 'uniformCost':
		plt.plot(dataX, dataG, 'ob', label='G')
	if algo == 'greedy':
		plt.plot(dataX, dataH, 'og', label='H')
	plt.axis([-2, len(answerChain) + 2, -2, max(dataF) + 2])
	plt.legend()
	plt.show()

def showCompareHeurs(stats):
	plt.rcParams['ytick.labelsize'] = 5
	plt.rcParams['xtick.labelsize'] = 7
	fig, bar = plt.subplots(nrows = 2, ncols = 2)
	fig.subplots_adjust(hspace = 0.3, wspace = 0.3)
	bars = bar.flatten().tolist()
	labels = ['Time', 'Taken vertices', 'Total vertices', 'Moves']
	for i, l in enumerate(labels):
		sub = [stats[x][i] for x in stats.keys()]
		bars[i].bar(stats.keys(), sub)
		bars[i].set_ylabel(l)
	plt.show()
