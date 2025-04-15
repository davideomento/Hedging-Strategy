import numpy as np
import scipy as sp

class PricingDerivatives:

    def get_forward_price(self, p_0, r_eur, r_usd, T):
        """ 
        INPUT: 
        - p_0: price observed in t=0
        - r_eur: eur risk free rate
        - r_usd: usd risk free rate
        - T: horizon
        """
        
        F_0 = p_0 * np.exp( (r_usd - r_eur)*T )

        return F_0


    def get_option_price(self, p_0, sigma, r_eur, r_usd, T, K):
        """ 
        pricing using B&S formula
        
        ASSUMPTION: 
        - price dynamic: dp_t = mu * p_t * dt + sigma * p_t * dW_t

        INPUT:
        - p_0: price observed in t=0
        - sigma: volatility of percentage return 
        - r_eur: eur risk free rate
        - r_usd: usd risk free rate
        - T: horizon
        - K: strike prices of call options
        """

        d1 = (np.log(p_0/K) + (r_usd - r_eur + 0.5*(sigma**2))*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma*np.sqrt(T)
        N_d1 = sp.stats.norm.cdf(d1)
        N_d2 = sp.stats.norm.cdf(d2)
        c_0 = p_0 * np.exp(-r_eur*T) * N_d1 - K * np.exp(-r_usd*T) * N_d2

        return c_0