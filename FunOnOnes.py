######################################
##
## FunOnOnes.py
##
## Author: Emily Wittrup
##
## Last Updated: 10/5/2020
##
## Copyright (c) Emily Wittrup, 2020
## Email: ewittrup@umich.edu
##
## Purpose of script: Generates pairwise permutations of a group using graph theory
##                      for unique one-one meetups over several weeks.
## ---------------------------

import numpy as np
from random import randint

class match:
    """
        Input: integer values that correspond to the index in the names array
        Usage: match(1,2)
    """
    def __init__(self, first = 100, second = 100):
        self.first = first
        self.second = second
    def print_match(self):
        print(self.first, ' ', self.second)

# Returns match object of a remaining edge
def findEdge(mat, invalid):
    """
        Purpose: Returns a match that has not been made yet
        Input: Boolean graph matrix (num_names)x(num_names)
    """
    ids = np.setdiff1d(np.array(range(len(mat))), np.array(invalid))
    x = ids[randint(0,len(ids)-1)]
    y = ids[randint(0,len(ids)-1)]
    it = 0
    while(mat[x][y] != 0):
        x = ids[randint(0,len(ids)-1)]
        y = ids[randint(0,len(ids)-1)]
        if it > 100:
            return None
        it +=1
    return match(x,y)

def findPath(mat, path, invalid = [], list_of_edges = []):
    """
        Purpose: Recursively find a path through the graph matrix to connect each pair of names exactly once
        Input:
            mat - Boolean graph matrix (num_names)x(num_names)
            list_of_edges - list of match objects corresponding to pairs matched
        Output: complete list of match objects
        Usage: findPath(mat, [1, 2])
    """
    # Base Case
    if len(list_of_edges) == len(mat)/2:
        markMatches(mat, list_of_edges)
        return list_of_edges
    
    #Find possible edge
    edge = findEdge(mat, invalid)
    if edge is not None:
        invalid.append(edge.first)
        invalid.append(edge.second)
        list_of_edges.append(edge)
        return findPath(mat, path, invalid, list_of_edges)
    elif len(list_of_edges) > 0:
        #undo previous week
        markMatches(mat, path[len(path)-1], 0)
        del path[len(path)-1]
        return findPath(mat, path, [], [])
    else:
        return None


def markMatches(mat,path, label=1):
    """
    Purpose: Mark matches in boolean mat matrix
        Input:
            mat - Boolean graph matrix (num_names)x(num_names)
            path - list of match objects
    """
    for m in path:
        mat[m.first][m.second] = label
        mat[m.second][m.first] = label


def main():
    names = ["Felicia", "Madelyn", "Emily", "Kaitlyn", "Lauren", "Rebecca", "Kyle", "Will", "Araba", "Cecilia"]
    
    num_names = len(names)
    
    #If an odd number of names is provided, each week someone will not have a partner
    if num_names % 2 != 0:
        names.append("None")
    
    #Create boolean graph matrix
    mat = np.zeros( (num_names,num_names) )
    for i in range(num_names):
        mat[i][i] = 1 #Each person doesn't need to meet with themselves

    start_week_num = 1 #Can be changed to match meaningful week number

    path = []
    while(len(path) != num_names-1):
        path.append(findPath(mat, path, [], []))
       
    for idx, week in enumerate(path):
        print('\n')
        print("Week: ", idx + start_week_num)
        for pair in week:
            print(names[pair.first], names[pair.second])


if __name__ == '__main__':
    main()
