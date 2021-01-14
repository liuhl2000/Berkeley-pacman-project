"""
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    '''pacman_pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
   
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghost.scaredTimer for ghost in ghostStates]

    food_dis = []
    food_value = 0
    ghost_dis = []
    ghost_value = 0
    scared_value = 0
    if len(food_list) != 0:
        for food_pos in food_list:
            distance = util.manhattanDistance(food_pos, pacman_pos)
            food_dis.append(distance)
    
        food_value += 1/min(food_dis)
        second = food_dis.remove(min(food_dis))
        if len(second) != 0:
            second_value = min(second)
            food_value = 1/food_value + 1/second_value
    

    if len(ghostStates) != 0:
        for ghost in ghostStates:
            distance = util.manhattanDistance(ghost.getPosition(), pacman_pos)
            if distance <= 5:
                ghost_dis.append(distance)
    ghost_value = len(ghost_dis) * (-500)
    
    if len(scaredTimes) != 0:
        for time in scaredTimes:
            scared_value += time
    
    return currentGameState.getScore() + 50*food_value + ghost_value + scared_value'''
    '''newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newCapsules = currentGameState.getCapsules()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    #closestGhost = min([manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates])
    distance = float('inf')
    closestGhost = 0
    if len(newGhostStates) != 0:
        for ghost in newGhostStates:
            temp = util.manhattanDistance(ghost.getPosition(), newPos)
            if temp <= distance:
                distance = temp
    closestGhost = distance'''
    '''if newCapsules:
        closestCapsule = min([manhattanDistance(newPos, caps) for caps in newCapsules])
    else:
        closestCapsule = 0

    if closestCapsule:
        closest_capsule = -3 / closestCapsule
    else:
        closest_capsule = 100'''

    #if closestGhost:
        ghost_distance = -2 / closestGhost
    else:
        ghost_distance = -500


    foodList = newFood.asList()
    distance = float('inf')

    if foodList:
        if len(foodList) != 0:
            for food in foodList:
                temp = util.manhattanDistance(food, newPos)
                if temp <= distance:
                    distance = temp
        closestFood = distance
        
    else:
        closestFood = 0

    return -2 * closestFood + ghost_distance - 10 * len(foodList)'''