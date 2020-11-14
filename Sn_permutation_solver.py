# Solves common problems for the Symmetric Group Sn when given a permutation of Sn (https://en.wikipedia.org/wiki/Symmetric_group)

# Author: Brian Blakely | github: https://github.com/bpblakely
# Theorems based on Contemporary Abstract Algebra SEVENTH EDITION by Joseph A. Gallian

# Requires Either CPython/PyPy 3.6, Python 3.7, or higher

import math
import numpy as np

def lcm(li):
    lcmm = li[0]
    for i in li[1:]:
      lcmm = lcmm*i//math.gcd(lcmm, i)
    return lcmm

def cycle_str(c):
    # input is 1 cycle as a list: [1,2,3,4,5]
    return str(c).replace("[","(").replace("]",")").replace(" ", "")

def output_builder(li):
    # should have already converted cycles to strings using cycle_str(cycle)
    string = ""
    for l in li:
        string += cycle_str(l)
    return string.replace(" ", "")

def permut_solv(permutation):
    # Given a permutation solve multiple aspects of the permutation
    # Input:
        # Type: Str
        # Example: '(1,2,3)(4,3,5,6)(8,3,2,1)'
    # Returns:
         # final_disjoint
             # Type: list of lists
                # The permutation expressed as a product of disjoint cycles
         # final_map
             # Type: dictionary
                # The final mapping of the permutation (which final_disjoint is based on)
                
    permutation = permutation.replace(" ", "")
    s = permutation.split(')')[:-1]
    s = [perm[1:] for perm in s]
    s = [seq.split(',') for seq in s]
    li = []
    for seq in s:
        temp=[]
        for num in seq:
            temp.append(int(num))
        li.append(temp)
    
    max_val = max([max(l) for l in li])
    
    r = list(reversed(li)) # reverse our permutation so we can traverse our functions in the correct order
    
    # build our list of functions based on the permutation 
    gens = [] 
    for seq in r:
        d = {}
        for i in range(len(seq)):
            # cycle back to first element if you hit the end
            if i == len(seq)-1:
                d[seq[i]] = seq[0]
            else:
                d[seq[i]] = seq[i+1]
        gens.append(d)
        
    final_map = {}
    
    # add all non-present values which are in Sn (expand the (i,j) notation)
    for g in gens:
        for i in range(1,max_val +1):
            if i not in g.keys():
                g[i]=i
    
    # for each value in Sn, traverse our set of functions to get the final mapping
    for i in range(1,max_val + 1):
        t = i
        for g in gens:
            #print('t: ',t,'->',g[t]) # debug to see function mapping
            t = g[t]
        final_map[i] = t
        
    print('\nFinal Mapping:')
    print(cycle_str(list(final_map.keys())))
    print(cycle_str(list(final_map.values())))
    
    # find unique cycles to build the permuation as a product of disjoint cycles.
    
    disjoint = np.array([]) # tracks the number of elements traversed until it reaches it's starting value
    cycles = [] # build all possible cycles
    
    for i in range(1,max_val + 1):
        t = final_map[i]
        track = 1
        local_cycle = [i,t]
        while i != t:
            t = final_map[t]
            track += 1
            local_cycle.append(t)
            
        disjoint = np.append(disjoint,track)
        cycles.append(local_cycle)
    
    max_distinct = len(np.unique(disjoint))
    
    # using sets because disjoint cycles will have unique elements, which a set can easily check
    uniq_cycles = [set(cycles[0])]
    
    # Only problem is that sets don't preserve order, which is important, so I will keep track of the index
    index = [0]
    for i, cycle in enumerate(cycles):
        if set(cycle) not in uniq_cycles:
            uniq_cycles.append(set(cycle))
            index.append(i)
        if len(uniq_cycles) >= max_distinct: 
            break
        
    final_disjoint =  [cycles[i][:-1] for i in index]  # -1 because there is an unneeded value at the end of cycles
    print('\nFinal Disjoint Result:')
    print(output_builder([cycle_str(d) for d in final_disjoint]))
    
    # product of transpositions
    transpo = []
    for cycle in final_disjoint:
        fixed = cycle[0] # select first value as base of transpositions
        for element in cycle[1:][::-1]:
            transpo.append([fixed,element])
            
    print('\nProduction of Transpositions')
    print(output_builder([cycle_str(tr) for tr in transpo]))

    # calculate order by taking the lcm of all disjoint sets
    order = lcm(np.unique(disjoint).astype(int))
    print('\nOrder: ', order)
    
    # parity
    if (np.unique(disjoint).astype(int)-1).sum() % 2:
        print('Parity: Even')
    else:
        print('Parity: Odd')
        
    # compute the inverse by inverting the final mapping
    inverse = dict([(value, key) for key, value in final_map.items()])
    inverse = dict(sorted(inverse.items())) # arrange keys in increasing order
    print('\nINVERSE of permutation: ') 
    print(cycle_str(list(inverse.keys())))
    print(cycle_str(list(inverse.values())))
    
    return final_disjoint, final_map

permutation = '(1,4,5,6,7,8)(7,9,10,3,2,1)'
disjoint_cycles, mapping = permut_solv(permutation)
