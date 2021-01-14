# logicPlan.py
# ------------
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
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game


pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'

class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined()
        
    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined()

def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr("A")
    B = logic.Expr("B")
    C = logic.Expr("C")

    p1 = A | B
    p2 = ~A % (~B|C)
    p3 = logic.disjoin(~A, ~B, C)
    return logic.conjoin(p1,p2,p3)


def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.
    
    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = logic.Expr("A")
    B = logic.Expr("B")
    C = logic.Expr("C")
    D = logic.Expr("D")

    p1 = C % (B|D)
    p2 = A >> (~B & ~D) 
    p3 = ~(B & ~C) >> A
    p4 = ~D >> C
    return logic.conjoin(p1, p2, p3, p4)
    

def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    A = logic.PropSymbolExpr("WumpusAlive[1]")
    B = logic.PropSymbolExpr("WumpusAlive[0]")
    C = logic.PropSymbolExpr("WumpusKilled[0]")
    D = logic.PropSymbolExpr("WumpusBorn[0]")

    p1 = A % ((B & ~C) | (~B & D))
    p2 = ~(B & D)
    p3 = D

    return logic.conjoin(p1, p2, p3)


def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    #A = logic.Expr("A")
    #sentence = A & ~A
    cnf = logic.to_cnf(sentence)
    result = logic.pycoSAT(cnf)
    #print(result)
    #if(str(result) == "False"):
        #return False
    return result
    


def atLeastOne(literals) :
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single 
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic 
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    return logic.disjoin(literals)


def atMostOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form) that represents the logic that at most one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    result = []

    for value in literals:
        for other in literals:
            if(other != value):
                result.append(logic.disjoin(~value, ~other))
    
    return logic.conjoin(result)



def exactlyOne(literals) :
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in 
    CNF (conjunctive normal form)that represents the logic that exactly one of 
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    result = []

    for value in literals:
        for other in literals:
            if(other != value):
                result.append(logic.disjoin(~value, ~other))
            
    result.append(logic.disjoin(literals))

    return logic.conjoin(result)

   

def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"

    unsort = []
    sort = []
   
    for key in model.keys():
        if model[key] == True:
            symbol = logic.PropSymbolExpr.parseExpr(key)
            if symbol[0] in actions:
               unsort.append(symbol)

    n = len(unsort)
    for i in range(n):
        for j in range(n - i - 1):
            if(int(unsort[j][1]) > int(unsort[j+1][1])):
                temp = unsort[j]
                unsort[j] = unsort[j + 1]
                unsort[j + 1] = temp
                
    for i in range(n):
        sort.append(unsort[i][0])
    
    return sort


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a 
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    current_pos = logic.PropSymbolExpr(pacman_str, x, y ,t)
    pre = []

    if not walls_grid[x][y-1]:
        pre_pos =  logic.PropSymbolExpr(pacman_str, x, y-1 ,t-1)
        move = logic.PropSymbolExpr("North", t-1)
        pre.append(move & pre_pos)

    if not walls_grid[x][y+1]:
        pre_pos =  logic.PropSymbolExpr(pacman_str, x, y+1 ,t-1)
        move = logic.PropSymbolExpr("South", t-1)
        pre.append(move & pre_pos)
    
    if not walls_grid[x-1][y]:
        pre_pos =  logic.PropSymbolExpr(pacman_str, x-1, y ,t-1)
        move = logic.PropSymbolExpr("East", t-1)
        pre.append(move & pre_pos)

    if not walls_grid[x+1][y]:
        pre_pos =  logic.PropSymbolExpr(pacman_str, x+1, y ,t-1)
        move = logic.PropSymbolExpr("West", t-1)
        pre.append(move & pre_pos)
    
    all_pre = logic.disjoin(pre)
    return current_pos % all_pre


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    MAX_TIME = 50
    start_pos = problem.getStartState()
    goal_pos = problem.getGoalState()
    actions = ['North', 'South', 'East', 'West']

    # pacman can only start at one position (with this and other constarin, there is no need to generate knowledge that pacman can not in two place at one time)
    start_one_list = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if (x,y) != start_pos:
                start_one_list.append(~logic.PropSymbolExpr(pacman_str, x, y, 0))
    
    start_one = logic.conjoin(start_one_list)

    #pacman start state
    start_state = logic.PropSymbolExpr(pacman_str, start_pos[0], start_pos[1], 0)

    #pacman is in start_pos and not in any other position
    start = logic.conjoin(start_state, start_one)

    one_action_list = []
    transition_list = []
    #update knowledge base through time 
    for t in range(1, MAX_TIME + 1):
        goal = logic.PropSymbolExpr(pacman_str, goal_pos[0], goal_pos[1], t)
        #can only take one action to get to current state
        temp = []
        for action in actions:
            one = logic.PropSymbolExpr(action, t - 1)
            temp.append(one)
        step_one_action = exactlyOne(temp)
        one_action_list.append(step_one_action)

        for x in range(1, width + 1):
            for y in range(1, height + 1):
                if not walls[x][y]:
                    transition_list.append(pacmanSuccessorStateAxioms(x, y, t, walls))

        one_action = logic.conjoin(one_action_list)
        one_action_list = [one_action]
        transition = logic.conjoin(transition_list)
        transition_list = [transition]

        result = findModel(logic.conjoin(start, one_action, transition, goal))
       
        if result is not False:
            return extractActionSequence(result, actions)


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth(), problem.getHeight()
    start_pos = problem.getStartState()[0]
    food_list = problem.getStartState()[1].asList()
    MAX_TIME = 50
    actions = ['North', 'South', 'East', 'West']

    # pacman can only start at one position (with this and other constarin, there is no need to generate knowledge that pacman can not in two place at one time)
    start_one_list = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            if (x,y) != start_pos:
                start_one_list.append(~logic.PropSymbolExpr(pacman_str, x, y, 0))
    
    start_one = logic.conjoin(start_one_list)

    #pacman start state
    start_state = logic.PropSymbolExpr(pacman_str, start_pos[0], start_pos[1], 0)

    #pacman is in start_pos and not in any other position
    start = logic.conjoin(start_state, start_one)

    one_action_list = []
    transition_list = []
    #update knowledge base through time 

    eat_all_food_dict = {}
    for food in food_list:
        eat_all_food_dict[food] = logic.PropSymbolExpr(pacman_str, food[0], food[1], 0)

    for t in range(1, MAX_TIME + 1):
        #can only take one action to get to current state
        temp = []
        for action in actions:
            one = logic.PropSymbolExpr(action, t - 1)
            temp.append(one)
        step_one_action = exactlyOne(temp)
        one_action_list.append(step_one_action)

        # update transition and food state
        for x in range(1, width + 1):
            for y in range(1, height + 1):
                if not walls[x][y]:
                    transition_list.append(pacmanSuccessorStateAxioms(x, y, t, walls))
                if (x,y) in food_list:
                    for food_key in eat_all_food_dict.keys():
                        if((x,y) == food_key):
                            eat_all_food_dict[food_key] = logic.disjoin(eat_all_food_dict[food_key], logic.PropSymbolExpr(pacman_str, x, y, t))

       
        eat_all_food = logic.conjoin(eat_all_food_dict.values())

        one_action = logic.conjoin(one_action_list)
        one_action_list = [one_action]
        transition = logic.conjoin(transition_list)
        transition_list = [transition]

        result = findModel(logic.conjoin(start, one_action, transition, eat_all_food))
       
        if result is not False:
            return extractActionSequence(result, actions)

    

# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit(100000)
    