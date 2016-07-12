#!/usr/bin/python3

"""
Copyright (c) 2016
Xavier Rubio-Campillo
Jonàs Alcaina
Iza Romanowska

This file is part of free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This file is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public 
License along with this file.  If not, see <http://www.gnu.org/licenses/>.
"""

import random
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot') # makes graphs pretty

# initialisation 
N = 100     # population size
A = 65      # initial number of believers A
B = N-A     # initial number of believers B


MAX_TIME = 100
t = 0               # initial time
Ta = 1.0            # initial attractiveness of option A
Tb = 2.0            # initial attractiveness of option B
alpha = 0.1         # strength of the transmission process
believersA = []    
believersB = []

believersA.append(A)
believersB.append(B)

    
def payoff(believers, Tx,Ty):
    """ payoff is the interest of 'conversion' of believers from one option (religion) to another.
        It depends on the current proportion between believers in the population.
        And its attractiveness to believers (defined in the 'attractiveness' function).
    """
    proportionBelievers = (believers / N) 
    attraction = (Tx) / (Ty + Tx)
    return proportionBelievers * attraction

def attractiveness(Ta, Tb):
    """ attractiveness is a dynamically changing feature of each cultural option. 
    The function is composed of the current value for each option (Ta, Tb)
    and a small stochastic change defined by the function K
    

    ####### different options for modelling attractiveness  ########
    # OPTION 1 - fixed attractiveness
    """
    Ka = 0.1
    Kb = 0


    Ta = Ta+Ka
    Tb = Tb+Kb

    return Ta, Tb
    
    
def attractiveness2(Ta, Tb):   
    """
    # OPTION 2 - gaussian noise with strong tail (lognormal distribution)
    """
    Ka, Kb = np.random.normal(0, 1, 2)
    diff = Ka-Kb
    Ta += diff
    Tb -= diff
    return Ta, Tb

    
def attractiveness3(Ta, Tb):
    """
    # OPTION 3 - anti-conformist behavior 
    # sort of lotka-volterra where diff of attractiveness is negatively correlated with diff of populations
    # we use gamma to add some stochasticity
    """
    Ka = 0
    Kb = 0

    diffPop = np.random.gamma(believersA[t], 1) - np.random.gamma(believersB[t], 1)
    # if diffPop is negative it means that we have more believers of A than B
    # so we have to promote Kb
    if diffPop<0:
        Ka = -diffPop

    # else we should promote Ka        
    else:
        Kb = diffPop
    # add 1 to avoid dividing by 0 if both are 0        
    Ta += Ka
    Tb += Kb

    return Ta, Tb

while t < MAX_TIME: 
    """ Main loop. Repeat until stop condition is met.
    1. define the current attractiveness of each option 
    2. define proportion of population swithching from B to A and vice versa
    3. calculate current numbers of practicioners of each option
    4. output the numbers to two lists for plotting    
    
    """
   
    # define the current attractiveness of each option
    Ta, Tb = attractiveness2(Ta, Tb)
    
    # calculate the change between believers A and B in the current time step       
    variationBA = payoff(A, Ta, Tb)      
    variationAB = payoff(B, Tb, Ta)     
    difference = variationBA - variationAB

    # B -> A
    if difference> 0:
        variation = difference*B
    # A -> B        
    else:
        variation = difference*A

    # control the pace of variation with alpha
    variation = alpha*variation        
    # update the population    
    A = A + variation
    B = B - variation
    
    # save the values to a list for plotting    
    believersA.append(A)
    believersB.append(B)
        
    # time = time + 1        
    t+=1 
    
# plot the results   
plt.plot(believersA)
plt.plot(believersB) 

plt.show()
