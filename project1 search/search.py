# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
   
    start_state = problem.getStartState()
    visited_node = {start_state: []}
    DFS_stack = util.Stack()
    DFS_stack.push(start_state)
    expand_list = []

    while not DFS_stack.isEmpty():
        expand_node = DFS_stack.pop()
        if expand_node not in expand_list:
            expand_list.append(expand_node)
            if problem.isGoalState(expand_node):
                return visited_node[expand_node]

            pre_path = visited_node[expand_node]
            successor = problem.getSuccessors(expand_node)
            for next in successor:
                if next[0] not in expand_list:
                    DFS_stack.push(next[0])
                    visited_node[next[0]] = pre_path + [next[1]]

    return visited_node[expand_node]
  
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #print("Start:", problem.getStartState())
    #m =  problem.getSuccessors(problem.getStartState())
    #print("Start's successors:", m)
    #print("hahaha:", problem.getSuccessors(m[0][0]))
    
    start_state = problem.getStartState()
    visited_node = {start_state: []}
    BFS_queue = util.Queue()
    BFS_queue.push(start_state)

    while not BFS_queue.isEmpty():
        expand_node = BFS_queue.pop()
        if (problem.isGoalState(expand_node)):
            return visited_node[expand_node]
       
        pre_path = visited_node[expand_node]
        successor = problem.getSuccessors(expand_node)
        for next in successor:
            if next[0] not in visited_node:
                BFS_queue.push(next[0])
                visited_node[next[0]] = pre_path + [next[1]]

    return visited_node[expand_node]
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start_state = problem.getStartState()
    visited_node = {start_state: []}
    UCS_pq = util.PriorityQueue()
    UCS_pq.push(start_state, 0)

    while not UCS_pq.isEmpty():
        expand_node = UCS_pq.pop() #pop and get item (not a tuple with priority)
        if (problem.isGoalState(expand_node)):
            return visited_node[expand_node]
       
        pre_path = visited_node[expand_node]
        successor = problem.getSuccessors(expand_node)
        for next in successor:
            if next[0] not in visited_node or problem.getCostOfActions(visited_node[next[0]]) > problem.getCostOfActions(pre_path + [next[1]]):
                visited_node[next[0]] = pre_path + [next[1]]
                UCS_pq.update(next[0], problem.getCostOfActions(visited_node[next[0]]))
               

    return visited_node[expand_node]
    
    
    
def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    start_state = problem.getStartState()
    visited_node = {start_state: []}
    A_pq = util.PriorityQueue()
    A_pq.push(start_state, 0 + heuristic(start_state, problem))  #0 is g(n)

    while not A_pq.isEmpty():
        expand_node = A_pq.pop()
        if (problem.isGoalState(expand_node)):
            return visited_node[expand_node]
       
        pre_path = visited_node[expand_node]
        successor = problem.getSuccessors(expand_node)
        for next in successor:
            if next[0] not in visited_node or problem.getCostOfActions(visited_node[next[0]]) > problem.getCostOfActions(pre_path + [next[1]]):
                visited_node[next[0]] = pre_path + [next[1]]
                A_pq.update(next[0], problem.getCostOfActions(visited_node[next[0]]) + heuristic(next[0], problem))
               

    return visited_node[expand_node]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
                   