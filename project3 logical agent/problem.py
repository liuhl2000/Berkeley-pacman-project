 #define eat food process
    eat_all_food_list = []
    for food in food_list:
        one_food_list = []
        for t in range(MAX_TIME + 1):
            eat = logic.PropSymbolExpr(pacman_str, food[0], food[1], t)
            one_food_list.append(eat)
        one_food = atLeastOne(one_food_list)
        eat_all_food_list.append(one_food)
    
    eat_all_food = logic.conjoin(eat_all_food_list)
# 在外面定义不行