import getopt, sys
import math
import numpy as np
from scipy.stats import norm
from alive_progress import alive_bar

class ipe:
    def __init__(self, x, p):
        self.est = x   # current estimate of the pth percentile
        self.p = p     # percentile of interest
        self.min = x   # min value observed thus far
        self.max = x   # max value observed thus far
        self.n = 1     # number of observations
        self.delta = 1 # value by which to adjust the estimate
        self.sumx = x
        self.sumxsq = x**2

    def update(self, x):
        if (abs(x - self.est) < self.delta):
            self.delta = abs(x - self.est)

        if (x < self.est):
            self.est = self.est - self.delta * (1 - self.p)
        elif (x > self.est):
            self.est = self.est + self.delta * (self.p)
        #else # being pedantic if (x == self.est):
        #    self.est = self.est

        self.min = min(self.min, x)
        self.max = max(self.max, x)
        self.sumx = self.sumx + x
        self.sumxsq = self.sumxsq + x**2
        self.n = self.n + 1

def usage():
    print("Usage:  ipe.py [options]")
    print("Options:")
    print("  -h --help     Print this help and exit")
    print("  -N=n          Number of data points to generate defaults to n = 1000")
    print("  --percentile  The percentile to estimate, defaults to 0.90")
    print("  --trace       Print the iterative estimate of the percentile, defaults to False")

if __name__ == "__main__":

    # Defualts
    N = 1000
    p = 0.9
    trace = False
    loc = 2.86     # for a random guassian
    scale = 3.188  # for a random guassian

    # get arguments from the command line
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hv", ["help", "N=", "p=",
                                                        "percentile=", "trace"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("--N="):
            N = int(arg)
        elif opt in ("--percentile="):
            p = float(arg)
            if (p < 0.0) or (p > 1.0):
                raise ValueError ("percentile need to be between 0.0 and 1.0")
        elif opt in ("-v", "--trace"):
            trace = True

    # generate first data obseration and initialize the tracker
    pest = ipe(np.random.normal(loc = loc, scale = scale), p)

    # generate data
    if (trace):
        for i in range(1,N):
            pest.update(np.random.normal(loc = loc, scale = scale))
            print("(" + str(i) + "/" + str(N) + ") estimate: " + str(pest.est))
    else:
        with alive_bar(N) as bar:
            for _ in range(N):
                pest.update(np.random.normal(loc = loc, scale = scale))
                bar()

    print("After " + str(pest.n) + " data observations")
    print("  Estiamte of the mean " + str(pest.sumx / pest.n))
    print("  Expected value: " + str(loc))
    print("")
    print("  Estiamte of the standard deviation " + str( math.sqrt((pest.sumxsq - (pest.sumx)**2 / pest.n) / (pest.n - 1) ) ))
    print("  Expected value: " + str(scale))
    print("")
    print("  Estiamte of the " + str(p*100) + "th percentile is " + str(pest.est))
    print("  Expected " + str(p*100) + "th percentile: " + str(norm.ppf(p, loc = loc, scale = scale)))


################################################################################
#                                 End of File                                  #
################################################################################
