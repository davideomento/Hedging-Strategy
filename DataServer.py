import numpy as np
import scipy as sp


class DataServer:

    def __init__(self, 
                 p_0=1.03, 
                 sigma=0.20, 
                 r_eur=0.03, 
                 r_usd=0.02, 
                 T=0.5, 
                 K=np.array([1.01, 1.03, 1.05]), 
                 V_dist=sp.stats.triang(c=0.75, loc=10000*1000, scale=20000*1000)):

        self.p_0 = p_0
        self.sigma = sigma
        self.r_eur = r_eur
        self.r_usd = r_usd
        self.T = T
        self.K = K
        self.V_dist = V_dist

        return
    
    
    def get_data(self):

        return self.p_0, self.sigma, self.r_eur, self.r_usd, self.T, self.K, self.V_dist