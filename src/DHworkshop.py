#!/usr/bin/python3


from __future__ import division
import random
import numpy as np

import matplotlib.pyplot as plt
plt.style.use('ggplot') # makes graphs pretty

# initialisation 
MAX_TIME = 1000
t = 0               # initial time
N = 100          # population size
A = 59            # initial proportion of believers A
B = N-A             # initial proportion of believers B

"""
!!!!!!!!!!!
Q: should we keep 'attractiveness' normalised? I don't think it matters too much 
cause we take a relative value anyways so it's more a question of 'do we want to make it pretty, pretty' 
it may be an overkill - it's gonna add an unnecessary line of code. 

!!!!!!!!!!!
"""
Ta = 1.0            # initial attractiveness of option A
Tb = 1.5            # initial attractiveness of option B
alpha = 0.1         # strength of the transmission process
believersA = [A]    # the first value is equal to the initialisation value (defined above)
believersB = [B]
attractA = [Ta]
attractB = [Tb]

    
def transmission(believers, Tx,Ty):
    """ transmission is the rate of 'conversion' of believers from one option (religion) to another.
        It depends on the current proportion between believers in the populaiton (no_adopters).
        And it's attractiveness to believers (defined in the 'attractiveness' function).
    """
    no_adopters = (believers / N) 
    attraction = (Tx) / (Ty + Tx)
    return no_adopters * attraction

def attractiveness(Ta, Tb):
    """ attractiveness is a dynamically changing feature of each cultural soption. 
    The function is composed of the current value for each option (Ta, Tb)
    and a small stochastic change defined by the function K
    """

    ####### different options for modelling attractiveness  ########
    # OPTION 1 - fixed attractiveness
    Ka = 0
    Kb = 0

    Ta = Ta+Ka
    Tb = Tb+Ka

    """
    # OPTION 2 - gaussian noise
    Ka, Kb = np.random.normal(0, 1, 2)    
    # the winner is the difference between the 2
    minValue = min(Ka,Kb)
    Ka = Ka - minValue
    Kb = Kb - minValue

    Ta = Ka
    Tb = Kb
    """

    """
    # OPTION 3 - anti-conformist behavior 
    # sort of lotka-volterra where diff of attractiveness is negatively correlated with diff of populations
    # we use gamma to add some stochasticity
    diffPop = np.random.gamma(0.1*believersA[t]) - np.random.gamma(0.1*believersB[t])
    if diffPop<0:
        Ka = -diffPop
    else:
        Kb = diffPop

    # add 1 to avoid dividing by 0 if both are 0        
    Ta = 1+Ka
    Tb = 1+Kb
    """

    return Ta, Tb

while t < MAX_TIME: 
    """ Main loop. Repeat until stop condition is met.
    1. define the current attractiveness of each option 
    2. define proportion of population swithching from B to A and vice versa
    3. calculate current numbers of practicioners of each option
    4. output the numbers to two lists for plotting    
    
    """
   
    print('next step:',t,'with pops:',A,B)

    # define the current attractiveness of each option
    Ta, Tb= attractiveness(Ta, Tb)
    attractA.append(Ta)
    attractB.append(Tb)
    
    # calculate the change between believers A and B in the current time step       
    finalDiff = alpha*(transmission(A, Ta, Tb) - transmission(B, Tb, Ta))

    # B -> A
    if finalDiff > 0:
        change = finalDiff*B
    # A -> B        
    else:
        change = finalDiff*A

    # update the population    
    A = A + change
    B = B - change
    
    # save the values to a list for plotting    
    believersA.append(A)
    believersB.append(B)
        
    # time = time + 1        
    t+=1 
    
# plot the results   
plt.figure(1)

plt.subplot(211)    
plt.ylim(0,1.1*N)    
plt.plot(believersA)
plt.plot(believersB) 

plt.subplot(212)
plt.plot(attractA)
plt.plot(attractB) 

plt.show()
#plt.savefig('DH2016.png')
