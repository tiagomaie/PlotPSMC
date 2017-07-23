import matplotlib.pyplot as pplot
import matplotlib.ticker as mtick
import re as regex
from random import random as rnd


class OOMFormatter(mtick.ScalarFormatter):
    # https://stackoverflow.com/questions/42656139/set-scientific-notation-with-fixed-exponent-and-significant-digits-for-multiple

    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        mtick.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)

    def _set_orderOfMagnitude(self, nothing):
        self.orderOfMagnitude = self.oom

    def _set_format(self, vmin, vmax):
        self.format = self.fformat
        if self._useMathText:
            self.format = '$%s$' % mtick._mathdefault(self.format)


def parse_psmc_output(psmcInputList, representAsEffectiveSize):

    allPsmcData = []
    for psmcFiles in psmcInputList:

        with open(psmcFiles[0], 'r') as psmcFile:
            inBlock = False
            timePoints, lambdaPoints, blockPoints = [], [], []
            estimatedTheta = n0 = 0

            for line in psmcFile:
                if line.split() == ['RD', '25']:  # Last iteration
                    inBlock = True
                    timePoints, lambdaPoints = [], []
                if inBlock and line[:2] == "RS":
                    timePoints.append(float(line.split('\t')[2]))
                    lambdaPoints.append(float(line.split('\t')[3]))
                elif inBlock and line[:2] == "PA":
                    inBlock = False
                    estimatedTheta = float(line.split()[2])
                    generationTime = psmcFiles[1]
                    mutRate = psmcFiles[2]
                    binSize = psmcFiles[3]
                    n0 = estimatedTheta/(4*mutRate)/binSize

                    scaledSize = scaledTime = 0

                    if representAsEffectiveSize:
                        scaledTime = [generationTime * 2 * n0 * t for t in timePoints]
                        scaledSize = [n0 * l for l in lambdaPoints]
                    else:
                        scaledTime = [t * estimatedTheta / binSize for t in timePoints]  # pairwiseSequenceDivergence
                        scaledSize = [(l * estimatedTheta / binSize)*1e3 for l in lambdaPoints]  # scaledMutRate

                    blockPoints.append((scaledTime, scaledSize))
        allPsmcData.append(blockPoints)

    return(allPsmcData)


def plotPsmc(listOfOpt, yAsEffectiveSize, xmin=0, xmax=0, ymin=0, ymax=0):

    myFigure = pplot.figure()
    inFigure = myFigure.add_subplot(111)

    myData = parse_psmc_output(listOfOpt, representAsEffectiveSize=yAsEffectiveSize)

    for i_sample in range(0, len(myData)):
        # original psmc
        inFigure.step(myData[i_sample][0][0],
                      myData[i_sample][0][1],
                      color=listOfOpt[i_sample][5],
                      label=listOfOpt[i_sample][4])
        # bootstraped psmc
        for j_bootStrap in range(0, len(myData[i_sample])):
            inFigure.step(myData[i_sample][j_bootStrap][0],
                          myData[i_sample][j_bootStrap][1],
                          color=listOfOpt[i_sample][5],
                          alpha=0.2)
    inFigure.legend(loc=0)
    myFigure.suptitle("PSMC estimate on real data")

    sumAxes = xmin+xmax+ymin+ymax

    if yAsEffectiveSize:
        pplot.xlabel("Years")
        pplot.ylabel("Effective population size")
        pplot.title("Y axis scaled as $N_e$")
        if sumAxes == 0:
            xmin = 1e3; xmax = 1e7; ymin = 0; ymax = 5e4
        inFigure.yaxis.set_major_formatter(OOMFormatter(4, "%1.0f"))
    else:
        pplot.xlabel(r'Time (scaled in units of 2$\mu$T)')
        pplot.ylabel("Population size\n(scaled in units of $4\mu N_e\ x\ 10^3$)")
        pplot.title("Y axis scaled as $4\mu N_e\ x\ 10^3$")
        if sumAxes == 0:
            xmin = 1e-6; xmax = 1e-2; ymin = 0; ymax = 5e0
        inFigure.yaxis.set_major_formatter(OOMFormatter(0, "%1.0f"))

    inFigure.grid(True)
    inFigure.set_xlim(xmin, xmax)
    inFigure.set_ylim(ymin, ymax)
    inFigure.set_xscale("log")

    myFigure.savefig("./testPlot")
    return myFigure


def readPsmcOptions(pathToOptionsFile):

    psmcOptions = []

    with open(pathToOptionsFile, 'r') as psmcOptionsFile:
        for line in psmcOptionsFile:
            if line[:1] != '#':  # if line doesnt start with a '#'
                # create a list of options from parameter file
                optTokens = regex.findall(r'[^\s\t\"]+', line)
                # could do it all in one line but this has better readability
                pathToPsmcFile = optTokens[0]
                generationTime = float(optTokens[1])
                mutationRate = float(optTokens[2])
                binSize = float(optTokens[3])
                sampleName = optTokens[4]
                if len(optTokens) == 6:
                    lineColor = optTokens[5]
                else:
                    # get random color
                    lineColor = (rnd(), rnd(), rnd())

                psmcOptions.append((pathToPsmcFile,
                                    generationTime,
                                    mutationRate,
                                    binSize,
                                    sampleName,
                                    lineColor))

    return(psmcOptions)


# a list of inputs/options to plot the PSMC curve
psmc_options = readPsmcOptions("./plotPSMC.csv")

a = plotPsmc(psmc_options, yAsEffectiveSize=True, xmin=1e3, xmax=1e7, ymin=0, ymax=3.5e6)
#b = plotPsmc(psmc_options, yAsEffectiveSize=False, xmin=1e-7, xmax=1e-2, ymin=0, ymax=5e0)

#pplot.subplot(1,2,1)
#pplot.plot(a,b)
#pplot.show()

#plotPsmc(psmc_options, yAsEffectiveSize=True)
