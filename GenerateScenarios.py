import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

class GenerateScenarios:
    
    def __init__(self, dataServer):

        self.p_0, self.sigma, self.r_eur, self.r_usd, self.T, self.K, self.V_dist = dataServer.get_data()

        return


    def get_volume_scenarios(self, num_scenarios):

        self.V_T_scenarios = self.V_dist.rvs(size = num_scenarios)

        return self.V_T_scenarios
    

    def get_price_scenarios(self, num_scenarios):
        """ 
        ASSUMPTION: 
        - price dynamic: dp_t = (r_usd - r_eur) * p_t * dt + sigma * p_t * dW_t
        """
 
        eps_T_scenarios = np.random.normal(loc=0, scale=1, size=num_scenarios)
        self.p_T_scenarios = self.p_0 * np.exp( (self.r_usd - self.r_eur -0.5*(self.sigma**2))*self.T + self.sigma*np.sqrt(self.T)*eps_T_scenarios )

        return self.p_T_scenarios