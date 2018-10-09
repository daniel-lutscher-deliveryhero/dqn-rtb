# -*- coding: utf-8 -*-
"""
Created on Thu Oct  4 14:38:01 2018

@author: osksti
"""

import numpy as np
import tensorflow as tf
import os
#import matplotlib.pyplot as plt

###AGENT-----------------------------------------------------------------------
    
    
###ENVIRONMENT-----------------------------------------------------------------
        
class environment:
    """
    This class should create and describe the environment, e.g. by defining
    the actions, states etc. It should track the budget, the budget 
    consumption rate, the CTR-estimations, winning bids, the KPI-values
    attained in previous time periods etc.
    """
    def __init__(self, ctr_estimations, winning_bids):
        """
        This function should take as inputs the CTR-estimations and the 
        winning bids as vectors. They will make up the core of the 
        environment. 
        """
        self.ctr_estimations = ctr_estimations
        self.winning_bids = winning_bids
        
        #The environment also has to initialize all the state-relevant 
        #features:
        self.time_step = 0
        self.budget = 0
        self.n_regulations = 0
        self.budget_consumption_rate = 0
        self.cpm = 0
        self.winning_rate = 0
        self.winning_value = 0
        
        #We also have to define the space of allowed actions:
        self.actions = [-0.08, -0.03, -0.01, 0, 0.01, 0.03, 0.08]
        
        #We also have to define the length of a time-step and the length
        #of an episode:
        self.step_length = 1000
        self.episode_length = 100
        #This means that any episode will contain ten million bids
        
        #Finally, we have to initialize the Lambda:
        self.Lambda = 0
        
        #and the state:
        self.state = np.array([self.time_step, self.budget, self.n_regulations,
                                 self.budget_consumption_rate, self.cpm, 
                                 self.winning_rate, self.winning_value, 
                                 self.Lambda])
        
    def reset(self, budget, initial_Lambda):
        """
        This function should return an initial state, in the same format
        as those in the gym environment, i.e. with some state-relevant
        vector, a numerical reward and a boolean describing whether the
        episode has terminated or not.
        """
        self.budget = budget
        self.Lambda = initial_Lambda
        self.n_regulations = self.episode_length
        
        self.state = np.array([self.time_step, self.budget, self.n_regulations,
                                 self.budget_consumption_rate, self.cpm, 
                                 self.winning_rate, self.winning_value, 
                                 self.Lambda])
        
        reward = 0
        #We also need to consider the cost
        termination = False

        return (self.state, reward, termination)        
            
    
    def step(self, action_index):
        """
        This function should describe what happens when a certain action
        takes in a certain state. The function takes as an argument the 
        index of an action, e.g. 0:6 since we have 7 actions.
        """
        action = self.actions[action_index]
        self.Lambda = self.Lambda*(1 + action)
        
        ctr_estimations = self.ctr_estimations[self.step_length:]
        bids = ctr_estimations*self.Lambda
        winning_bids = self.winning_bids = self.winning_bids[self.step_length:]
        
        self.winning_rate = 0
        self.winning_value = 0
        self.cpm = 0
        
        new_budget = self.budget
        for i in range(self.step_length):
                if (bids[i] > winning_bids[i]):
                    new_budget -= bids[i]
                    self.winning_rate += 1/self.step_length
                    self.winning_value += ctr_estimations[i]
                    self.cpm += bids[i]*1000/self.step_length
                    
        self.budget_consumption_rate = (self.budget - new_budget)/self.budget
        self.budget = new_budget            
        
        self.n_regulations -= 1 #IS THSI NECESSARY??
        self.time_step += 1
        if (self.time_step == self.episode_length):
            termination = True
            #SHOULD THSI COME BEFORE? I.E. MAKE THE WHOLE FUNCTION AS
            #AS IF-ELSE STATEMENTS W.R.T TERMINATION.
        
        self.state = np.array([self.time_step, self.budget, self.n_regulations,
                                 self.budget_consumption_rate, self.cpm, 
                                 self.winning_rate, self.winning_value, 
                                 self.Lambda])
        
        reward = self.winning_value #IS THIS NECESSARY? CONSIDERING STATE!
        #We also need to consider the cost
    
        return (self.state, reward, termination)  


###DATA------------------------------------------------------------------------

#os.listdir(...)

camp_n = ['1458', '2259', '2261', '2821']
data_type = ['test.theta', 'train.theta']
imported_files = []

for i in camp_n:
    for j in data_type:
        imported_files.append(open(os.path.join\
                            ('', 
                             j+'_'+i+'.txt')))
        
###EXPERIMENTS-----------------------------------------------------------------

#convolutional_neural_network = True        
#target_network = True #HAVE TO CONSIDER variable scope and copying for this
#dueling_networks = True
#prioritized_experience_replay = True
#reward_net = True