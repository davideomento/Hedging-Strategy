import numpy as np
import scipy as sp
import gurobipy as gp
from gurobipy import GRB


class HedgingModel:

    def __init__(self, dataServer, pricingDerivatives):

        self.p_0, self.sigma, self.r_eur, self.r_usd, self.T, self.K, self.V_dist = dataServer.get_data()
        self.num_options = np.shape(self.K)[0]
        self.F_0 = pricingDerivatives.get_forward_price(self.p_0, self.r_eur, self.r_usd, self.T)
        self.c_0 = pricingDerivatives.get_option_price(self.p_0, self.sigma, self.r_eur, self.r_usd, self.T, self.K)

        return

    
    def opt_hedging_model_for_loops(self, p_T_scenarios, V_T_scenarios, alpha=0.05, show_results=True):
        
        self.model = gp.Model('model_cvar')

        num_scenarios = len(V_T_scenarios)
        probs = np.ones(len(V_T_scenarios))*(1/len(V_T_scenarios))

        # create variables
        x = self.model.addMVar(shape=1, name='eur_in_forward', lb=0)
        eta = self.model.addMVar(shape=1, name='V@R')
        y_vec = self.model.addMVar(shape=self.num_options, name='eur_in_call', lb=0)
        w_vec = self.model.addMVar(shape=num_scenarios, name='eur_sold_in_T', lb=0)
        z_vec = self.model.addMVar(shape=num_scenarios, name='eur_bought_in_T', lb=0)
        h_mat = self.model.addMVar(shape=(self.num_options, num_scenarios), name='exercised_call_in_T', lb=0)
        O_vec = self.model.addMVar(shape=num_scenarios, name='out_cash_flow_in_T')
        xi_vec = self.model.addMVar(shape=num_scenarios, name='aux_variable', lb=0)

        # add constraints using for loops
        for s in range(num_scenarios):
            self.model.addConstr( V_T_scenarios[s] == x + h_mat[:,s].sum() + z_vec[s] - w_vec[s], name='budget_constraint' )
            self.model.addConstr( O_vec[s] == (y_vec @ self.c_0)*np.exp(self.r_usd*self.T) + x*self.F_0 + h_mat[:,s]@self.K + (z_vec[s] - w_vec[s])*p_T_scenarios[s], name='out_cash_flow' )
            self.model.addConstr( xi_vec[s] >= ( O_vec[s] - self.p_0*V_T_scenarios[s] ) - eta )
            for i in range(self.num_options):
                self.model.addConstr( h_mat[i,s] <= y_vec[i], name='options_constraint')

        # objective function
        obj = eta + (probs @ xi_vec)/alpha
        self.model.setObjective(obj, GRB.MINIMIZE)

        # optimize model
        self.model.params.LogToConsole = 0
        self.model.optimize()

        # get results
        cvar = self.model.ObjVal
        opt_first_stage_dec = { var.VarName: var.X for var in self.model.getVars() if 'eur_in_forward' in var.VarName or 'eur_in_call' in var.VarName }

        # print results
        if show_results:
            print(f'************* RESULTS *************')
            print()
            print(f'CV@R = {cvar:.2f}')
            print()
            for k, v in opt_first_stage_dec.items():
                print(f'{k} = {v:.2f}')
            print()
            print(f'***********************************')

        return cvar, opt_first_stage_dec
    

    def opt_hedging_model_matrices(self, p_T_scenarios, V_T_scenarios, alpha=0.05, show_results=True):
        
        self.model = gp.Model('model_cvar')

        num_scenarios = len(V_T_scenarios)
        probs = np.ones(len(V_T_scenarios))*(1/len(V_T_scenarios))

        # create variables
        x = self.model.addMVar(shape=1, name='eur_in_forward', lb=0)
        eta = self.model.addMVar(shape=1, name='V@R')
        y_vec = self.model.addMVar(shape=self.num_options, name='eur_in_call', lb=0)
        w_vec = self.model.addMVar(shape=num_scenarios, name='eur_sold_in_T', lb=0)
        z_vec = self.model.addMVar(shape=num_scenarios, name='eur_bought_in_T', lb=0)
        h_mat = self.model.addMVar(shape=(self.num_options, num_scenarios), name='exercised_call_in_T', lb=0)
        O_vec = self.model.addMVar(shape=num_scenarios, name='out_cash_flow_in_T')
        xi_vec = self.model.addMVar(shape=num_scenarios, name='aux_variable', lb=0)

        # auxiliar matrix
        K_mat = np.tile(self.K, (num_scenarios, 1)).T

        # add constraints using matrix form
        self.model.addConstr(V_T_scenarios == x + h_mat.sum(axis=0) + z_vec - w_vec, name='budget_constraint')
        self.model.addConstr(O_vec == y_vec @ self.c_0 * np.exp(self.r_usd * self.T) + x * self.F_0 + (h_mat * K_mat).sum(axis=0) + (z_vec - w_vec) * p_T_scenarios, name='out_cash_flow')
        self.model.addConstr(xi_vec >= (O_vec - self.p_0 * V_T_scenarios) - eta, name='xi_constraint')
        self.model.addConstr(h_mat <= y_vec[:, np.newaxis], name='options_constraint')

        # objective function
        obj = eta + (probs @ xi_vec)/alpha
        self.model.setObjective(obj, GRB.MINIMIZE)

        # optimize model
        self.model.params.LogToConsole = 0
        self.model.optimize()

        # get results
        cvar = self.model.ObjVal
        opt_first_stage_dec = { var.VarName: var.X for var in self.model.getVars() if 'eur_in_forward' in var.VarName or 'eur_in_call' in var.VarName }

        # print results
        if show_results:
            print(f'************* RESULTS *************')
            print()
            print(f'CV@R = {cvar:.2f}')
            print()
            for k, v in opt_first_stage_dec.items():
                print(f'{k} = {v:.2f}')
            print()
            print(f'***********************************')

        return cvar, opt_first_stage_dec
    
    
    def evaluate_solution(self, opt_sol, p_T_scenarios, V_T_scenarios):
        
        num_scenarios = len(V_T_scenarios)

        x = opt_sol['eur_in_forward[0]']
        y = np.array([ opt_sol[f'eur_in_call[{i}]'] for i in range(self.num_options) ])

        K_mat = np.tile(self.K, (num_scenarios, 1)).T
        p_T_mat = np.tile(p_T_scenarios, (self.num_options, 1))
        when_exercise = (K_mat < p_T_mat).astype(int)
        exercised_call_eur = y.reshape((self.num_options, -1)) * when_exercise
        exercise_cost_usd = exercised_call_eur * K_mat
        delta_eur = V_T_scenarios - x - np.sum(exercised_call_eur, axis=0)

        O_vec = (self.c_0 @ y) * np.exp(self.r_usd * self.T) + x * self.F_0 + np.sum(exercise_cost_usd, axis=0) + delta_eur * p_T_scenarios

        return O_vec - self.p_0 * V_T_scenarios, exercised_call_eur, delta_eur