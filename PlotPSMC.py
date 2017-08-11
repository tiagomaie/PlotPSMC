import matplotlib.pyplot as pplot
import matplotlib.ticker as mtick
import re as regex
from random import random as rnd


class OOMFormatter(mtick.ScalarFormatter):
    # https://stackoverflow.com/questions/42656139/set-scientific-notation-with-fixed-exponent-and-significant-digits-for-multiple

    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        mtick.ScalarFormatter.__init__(self, useOffset=offset, useMathText=mathText)

    def _set_orderOfMagnitude(self, nothing):
        self.orderOfMagnitude = self.oom

    def _set_format(self, vmin, vmax):
        self.format = self.fformat
        if self._useMathText:
            self.format = '$%s$' % mtick._mathdefault(self.format)


def parse_psmc_output(psmcInputList, representAsEffectiveSize):

    # TODO: apparently there is some sort of bug because my plots, when compared to Li's psmc_plot.pl plots
    # do not exactly match when the same data is used, especially when it comes to the population size.
    #
    allPsmcData = []
    for psmcFiles in psmcInputList:

        lastIteration = ""
        with open(psmcFiles[0], 'r') as psmcFile:
            inBlock = False
            timePoints, lambdaPoints, blockPoints = [], [], []
            estimatedTheta = n0 = 0

            for line in psmcFile:
                if line.split()[0] == "MM" and line.split()[1].split(":")[0] == "n_iterations":
                    # We could also iterate through the whole file and get the maximum RD value
                    lastIteration = line.split()[1].split(":")[1].strip(",")
                if line.split() == ['RD', lastIteration]:  # Last iteration
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
                        scaledTime = [generationTime * 2 * n0 * time_k for time_k in timePoints]
                        scaledSize = [n0 * lambda_k for lambda_k in lambdaPoints]
                    else:
                        scaledTime = [time_k * estimatedTheta / binSize for time_k in timePoints]  # pairwiseSequenceDivergence
                        scaledSize = [(lambda_k * estimatedTheta / binSize)*1e3 for lambda_k in lambdaPoints]  # scaledMutRate

                    blockPoints.append((scaledTime, scaledSize))
        allPsmcData.append(blockPoints)

    return allPsmcData


def plotPsmc(listOfOpt, yAsEffectiveSize,
             xmin=0, xmax=0,
             ymin=0, ymax=0,
             transparency=0.1, isLogScale=True,
             savePlotWithName="myPlot"):

    myFigure = pplot.figure(1)
    inFigure = myFigure.add_subplot(111)

    myData = parse_psmc_output(listOfOpt, representAsEffectiveSize=yAsEffectiveSize)

    for i_sample in range(0, len(myData)):

        # bootstraped psmc
        for j_bootStrap in range(0, len(myData[i_sample])):
            inFigure.step(myData[i_sample][j_bootStrap][0],
                          myData[i_sample][j_bootStrap][1],
                          color=listOfOpt[i_sample][5],
                          linewidth=1.0,
                          alpha=transparency)
        # original psmc
        inFigure.step(myData[i_sample][0][0],
                      myData[i_sample][0][1],
                      color=listOfOpt[i_sample][5],
                      label=listOfOpt[i_sample][4])
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
    if isLogScale:
        inFigure.set_xscale("log")
    else:
        inFigure.set_xscale("linear")

    myFigure.savefig(savePlotWithName)
    myFigure.clf()  # close/clear fig so that it doesnt keep using resources
    # pplot.close(1) # can't actually close figure because of current conflict with tkinter GUI


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

    return psmcOptions

# a list of inputs/options to plot the PSMC curve
#psmc_options = readPsmcOptions("./plotPSMC.csv")

#a = plotPsmc(psmc_options, yAsEffectiveSize=True, xmin=1e4, xmax=1e8, ymin=0, ymax=2e5, transparency=0.15)
# b = plotPsmc(psmc_options, yAsEffectiveSize=False, xmin=1e-7, xmax=1e-2, ymin=0, ymax=5e0)
