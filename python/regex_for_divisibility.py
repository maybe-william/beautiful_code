# This solution is based on building a custom representation 
# of a Finite State Machine of any number modulus n and then 
# reducing out nodes from n-1 all the way to 0, exclusive.
#
# It currently works with 1 <= n <= 18
#
# When reducing out nodes, all edges coming in to the node
# being reduced out must be combined with all edges going out
# of the node to be reduced, creating all possible paths that
# might occur and pass through the node to be reduced out.
#
# Edges that directly loop from and to the node to be reduced
# out must also be considered. (This is the source of wildcards
# in the regex solution, because a loop that begins and ends in
# the same place can happen anywhere from zero to infinity times.)
#
# Also, after reducing out a node, any edges to and from the same
# nodes are put together with the "|" symbol inside parenthesis
# (because if both paths go from one node to another, then you can
# either take one path OR the other and you still end up in the same
# place.)
#
# The representation I've used here is a 3-tuple of (start, end, path)
# for every edge in the FSM. The edges are more emphasized than the 
# nodes for this particular representation.

def gen_states(top):
    """ Generate the starting states and edges for the FSM """
    states = []
    for i in range(0, top):
        s0 = (i * 2) % top
        s1 = ((i * 2) + 1) % top
        states.append((i,s0, "0"))
        states.append((i,s1, "1"))

    return states

def combine_identical(paths):
    """ Combine identical paths in parenthesis and with the pipe """
    all = "("
    for p in paths:
        all = all + p[2] + "|"
    all = all[:-1]
    if all != "":
        all = all + ")"
        
    return all
    
def combine(tos, loops, froms):
    """ Combine all possible paths to and from a node """
    # first, combine all in loops into one.
    loop = combine_identical(loops)
    if loop != "":
        loop = loop + "*"
    
    # next, make a new list with to, loop, from for each to and each from.
    
    allPathCombos = [(to, frm) for to in tos for frm in froms]
    newPaths = [(x[0][0], x[1][1], x[0][2] + loop + x[1][2]) for x in allPathCombos]

    return newPaths
  
def condense_duplicates(states, node):
    """ Condense out duplicate entries in states using combine_identical """
    nonDups = []
    for i in range(0, node):
      for j in range(0, node):
        matches = [y for y in states if y[0] == i and y[1] == j]
        if len(matches) == 1:
          nonDups.append(matches[0])
        if len(matches) <= 1:
          continue

        path = combine_identical(matches)
        nonDups.append((i,j,path))
      
    return nonDups
      
def reduc(states, node):
    """ Reduce out a node from the FSM """
    loops = [x for x in states if x[0] == x[1] and x[0] == node]
    states = list(set(states).difference(loops))

    tos = [x for x in states if x[1] == node]
    states = list(set(states).difference(tos))

    froms = [x for x in states if x[0] == node]
    states = list(set(states).difference(froms))

  
    states = states + combine(tos, loops, froms)

    states = condense_duplicates(states, node)

    return states


def regex_divisible_by(n):
    """ Return a regex string to check if a binary string is divisible by n """
    # Divisible by 1 is an edge case due to how the FSM works.
    if n == 1:
        return '^(?:0|1)+$'

    states = gen_states(n)
    for num in range(n - 1, 0, -1):
        states = reduc(states, num)
    
    reg = states[0][2]
    
    reg = '^' + reg + '+' + '$'
    reg = reg.replace('(','(?:')
    return reg
