import random
import numpy as np 

class OU(object):

    def function(self, x, mu, theta, sigma):
        # mu represents the mean value, or the average value we'd expect it to be over a full run
        #   (typcially: 0 for an event that varies between -1 and 1, 0.5 for an event that varies between 0 and 1, etc.)
        # theta defines how fast we revert to the mean (typically between 0.5 and 1)
        # sigma represents the volatility (typically: 0.05 to 0.30)

        return theta * (mu - x) + sigma * np.random.randn(1)