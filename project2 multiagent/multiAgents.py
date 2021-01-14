# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        #print(successorGameState)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        #print(newFood)
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended. Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """
    '''def value(self, state, depth, agent_index):
        if(depth == self.depth or state.isWin() or state.isLose()):
            return self.evaluationFunction(state)
        elif(agent_index == state.getNumAgents - 1):
            return max_value(state, )'''

    def max_value(self, state, depth):  #pacman choose max, so agent index will always be 0
        if(depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(0) == []):
            return self.evaluationFunction(state)
        v = -float('inf')
        for action in state.getLegalActions(0):
            successor_state = state.generateSuccessor(0, action)
            v = max(self.min_value(successor_state, depth, 1),v)
        return v


    def min_value(self, state, depth, agent_index):
        if(depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(agent_index) == []):
            return self.evaluationFunction(state)
        v = float('inf')
        for action in state.getLegalActions(agent_index):
            successor_state =  state.generateSuccessor(agent_index, action)
            if(agent_index == state.getNumAgents() - 1):  
                v = min(self.max_value(successor_state, depth + 1), v)  #if there is pacman again, then depth + 1
            else:
                v = min(self.min_value(successor_state, depth, agent_index + 1),v)
        return v


    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        target_value = -float('inf')
        result_action = None
        for action in gameState.getLegalActions(0):
           successor_state = gameState.generateSuccessor(0, action)
           v = self.min_value(successor_state, 0, 1)
           if (v >= target_value):
               target_value = v
               result_action = action
       
        return result_action



       
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def max_value(self, state, depth, alpha, beta):  #pacman choose max, so agent index will always be 0
        if(depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(0) == []):
            return (self.evaluationFunction(state),None)
        v = -float('inf')
        result_action = None
        for action in state.getLegalActions(0):
            successor_state = state.generateSuccessor(0, action)
            #v = max(self.min_value(successor_state, depth, 1, alpha, beta),v)
            #alpha[0] = beta[0]
            #beta[0] = float('inf')
            if (self.min_value(successor_state, depth, 1, alpha, beta) >= v):
               v = self.min_value(successor_state, depth, 1, alpha, beta)
               result_action = action
            if v > beta:  #in this case, we must use ">", ">=" is not feasible
                return (v, action)
            alpha = max(v, alpha)
        return (v,result_action)


    def min_value(self, state, depth, agent_index, alpha, beta):
        if(depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(agent_index) == []):
            return self.evaluationFunction(state)
        v = float('inf')
        for action in state.getLegalActions(agent_index):
            successor_state =  state.generateSuccessor(agent_index, action)
            if(agent_index == state.getNumAgents() - 1):  
                v = min(self.max_value(successor_state, depth + 1, alpha, beta)[0], v)  #if there is pacman again, then depth + 1
            else:
                v = min(self.min_value(successor_state, depth, agent_index + 1, alpha, beta),v)
            if v < alpha:
                #print(alpha)
                return v
            beta = min(beta, v)
        return v

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #target_value = -float('inf')
        #result_action = None
        alpha = -float('inf')
        beta = float('inf')
        return self.max_value(gameState, 0, alpha, beta)[1]


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """
    def max_value(self, state, depth):  #pacman choose max, so agent index will always be 0
        if(depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(0) == []):
            return self.evaluationFunction(state)
        v = -float('inf')
        for action in state.getLegalActions(0):
            successor_state = state.generateSuccessor(0, action)
            v = max(self.expect_value(successor_state, depth, 1),v)
        return v


    def expect_value(self, state, depth, agent_index):
        if(depth == self.depth or state.isWin() or state.isLose() or state.getLegalActions(agent_index) == []):
            return self.evaluationFunction(state)
        v = float('inf')
        total_value = 0
        action_number = len(state.getLegalActions(agent_index))

        for action in state.getLegalActions(agent_index):
            successor_state =  state.generateSuccessor(agent_index, action)
            if(agent_index == state.getNumAgents() - 1):  
                v = self.max_value(successor_state, depth + 1) #if there is pacman again, then depth + 1
                total_value += v
            else:
                v = self.expect_value(successor_state, depth, agent_index + 1)
                total_value += v

        return total_value/action_number

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        target_value = -float('inf')
        result_action = None
        for action in gameState.getLegalActions(0):
           successor_state = gameState.generateSuccessor(0, action)
           v = self.expect_value(successor_state, 0, 1)
           if (v >= target_value):
               target_value = v
               result_action = action
       
        return result_action

        

def betterEvaluationFunction(currentGameState):
    pacman_pos = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()  
    food = currentGameState.getFood()
    foodList = food.asList()
    capsule = currentGameState.getCapsules()
    scaredTimes = [ghost.scaredTimer for ghost in ghostStates]

    
    ghost_value = 0
    for ghost in ghostStates:
        distance = manhattanDistance(pacman_pos, ghost.getPosition())
        if ghost.scaredTimer <= 0:
            if 5 < distance <= 10:
                ghost_value -= 2*(10 - distance)
            if 2 < distance <= 5:
                ghost_value -= 6*(10 - distance)
            if 0 <= distance <= 2:
                ghost_value -= 12*(10 - distance)
        

    food_1 = 0
    food_value = 0
    distance = float('inf')
    if len(foodList) != 0:
            for food in foodList:
                temp = util.manhattanDistance(food, pacman_pos)
                if temp <= distance:
                    food_1 = temp
            food_value = 1/food_1
    
    
    capsule_1 = 0
    capsule_value = 0
    distance = float('inf')
    if len(capsule) != 0:
            for pos in capsule:
                temp = util.manhattanDistance(pos, pacman_pos)
                if temp <= distance:
                    capsule_1 = temp
            capsule_value = 1/capsule_1

    return currentGameState.getScore() + ghost_value + 8*food_value + 20*capsule_value + 2*sum(scaredTimes)
  

# Abbreviation
better = betterEvaluationFunction
