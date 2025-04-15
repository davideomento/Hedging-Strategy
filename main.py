import numpy as np
import pandas as pd

from DataServer import DataServer
from GenerateScenarios import GenerateScenarios
from PricingDerivatives import PricingDerivatives
from HedgingModel import HedgingModel


dataServer = DataServer()
pricingDerivatives = PricingDerivatives()
hedgingModel = HedgingModel(dataServer, pricingDerivatives)
generateScenarios = GenerateScenarios(dataServer)

num_scenarios = 20000
p_T_scenarios = generateScenarios.get_price_scenarios(num_scenarios)
V_T_scenarios = generateScenarios.get_volume_scenarios(num_scenarios)

opt_cvar, opt_decisions = hedgingModel.opt_cvar_hedging_model(p_T_scenarios=p_T_scenarios, V_T_scenarios=V_T_scenarios, alpha=0.05, show_results=True)