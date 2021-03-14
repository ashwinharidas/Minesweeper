import numpy as np
import sys
from random import *

def generate_board(dimension, density):
    board = np.zeros((dimension, dimension), dtype=int)

    # while mines > 0:
    #     x = randint(0, dimension - 1)
    #     y = randint(0, dimension - 1)

    #     if board[x][y] == 9:
    #         continue

    #     board[x][y] = 9
    #     mines -= 1

    totalMines = 0

    for x in range(board.shape[0]):
        for y in range(board.shape[0]):
            if random() < density:
                board[x][y] = 9
                totalMines += 1
    
    for x in range(0, dimension):
        for y in range(0, dimension):
            if board[x][y] == 9:
                continue

            mines = 0

            if x - 1 >= 0:
                if board[x - 1][y] == 9:
                    mines += 1
                if y - 1 >= 0:
                    if board[x - 1][y - 1] == 9:
                        mines += 1
                if y + 1 < dimension:
                    if board[x - 1][y + 1] == 9:
                        mines += 1
            
            if x + 1 < dimension:
                if board[x + 1][y] == 9:
                    mines += 1
                if y - 1 >= 0:
                    if board[x + 1][y - 1] == 9:
                        mines += 1
                if y + 1 < dimension:
                    if board[x + 1][y + 1] == 9:
                        mines += 1
            
            if y - 1 >= 0:
                if board[x][y - 1] == 9:
                    mines += 1
            
            if y + 1 < dimension:
                if board[x][y + 1] == 9:
                    mines += 1

            board[x][y] = mines
    
    return board, totalMines

def markSafe(agent, board, safeList, moves, knowledge_base):
    while len(safeList) > 0:
        currSafe = safeList.pop()
        print('make a safe move at')
        print(currSafe)
        x, y = currSafe
        agent[x][y] = board[x][y]
        # add to knowledge base since we make a new move
        knowledge_base.append((currSafe, agent[x][y], 
        get_safe_neighbors(agent, currSafe), 
        get_mine_neighbors(agent, currSafe), get_hidden_neighbors(agent, currSafe)))
        # once we make a move we should remove it from moves list
        moves.remove(currSafe)

def basic_agent(board, totalMines):
    agent = np.zeros((board.shape[0], board.shape[0]), int)
    dimension = board.shape[0]
    agent[:] = -1 # -1 represents an unknown cell

    defused = 0
    total = 0

    moves = []
    
    knowledge_base = []

    for x in range(agent.shape[0]):
        for y in range(agent.shape[0]):
            moves.append((x, y))

    while len(moves) > 0:
        # Update knowledge base with most updated information before making a move
        knowledge_base = [(kb[0], kb[1], get_safe_neighbors(agent, kb[0]), 
        get_mine_neighbors(agent, kb[0]), get_hidden_neighbors(agent, kb[0])) for kb in knowledge_base]

        # try to make a move through basic inference
        if len(knowledge_base) > 0:
            removedItems = []
            inferenceMade = False
            moveMade = False

            for kb in knowledge_base:
                coord = kb[0]
                clue = kb[1]
                safe = kb[2]
                mines = kb[3]
                hidden = kb[4]

                # everything around is a mine
                if clue - mines == hidden:
                    newMines = get_all_hidden_neighbors(agent, coord)
                    for coord in newMines:
                        moves.remove(coord)
                        agent[coord[0]][coord[1]] = 9
                        defused += 1
                        total += 1
                    
                    inferenceMade = True
                    removedItems.append(kb)
                    
                
                # corner cell
                elif (x == 0 and y == 0) or (x == 0 and y == dimension - 1) or (x == dimension - 1 and y == 0) or (x == dimension - 1 and y == dimension - 1):
                    if (3 - clue) - safe == hidden:
                        safeList = get_all_hidden_neighbors(agent, coord)
                        markSafe(agent, board, safeList, moves, knowledge_base) # make a bunch of safe moves
                        inferenceMade = True
                        moveMade = True
                        removedItems.append(kb)
                        
                
                # border cell
                elif x == 0 or y == 0:
                    if (5 - clue) - safe == hidden:
                        safeList = get_all_hidden_neighbors(agent, coord)
                        markSafe(agent, board, safeList, moves, knowledge_base) # make a bunch of safe moves
                        inferenceMade = True
                        moveMade = True
                        removedItems.append(kb)
                        

                else:
                    if (8 - clue) - safe == hidden:
                        safeList = get_all_hidden_neighbors(agent, coord)
                        markSafe(agent, board, safeList, moves, knowledge_base)
                        inferenceMade = True
                        modeMade = True
                        removedItems.append(kb)
                        

            if inferenceMade == True:
                for item in removedItems:
                    knowledge_base.remove(item)

            if moveMade == True:
                continue # Since we have made a move(s) through our basic inference, no need to pick a random move

            # if we don't need to remove anything from the knowledge base, that means we didn't make any moves through basic inference
            # so, we must make a random choice

        # once we run out of moves, we end
        if len(moves) <= 0:
            break
        
        # pick random move
        i = randint(0, len(moves) - 1)
        coord = moves[i]
        x, y = coord
        agent[x][y] = board[x][y]

        # if we didn't pick a mine, add to knowledge base
        if agent[x][y] != 9:
            print('random safe move at')
            print(coord)
            knowledge_base.append((coord, agent[x][y], 
            get_safe_neighbors(agent, coord), 
            get_mine_neighbors(agent, coord), get_hidden_neighbors(agent, coord)))
        else:
            total += 1
            print('you picked a mine (random) at:')
            print(coord)
        
        moves.remove(coord)
    
    print(agent)
    return defused

def advanced_agent(board):
    '''
    agent = np.zeros((board.shape[0], board.shape[0]))
    agent[:] = -1
    print(agent)

    count = 0

    num_to_coord = {}
    coord_to_num = {}

    for x in range(agent.shape[0]):
        for y in range(agent.shape[0]):
            num_to_coord[count] = (x, y)
            coord_to_num[(x, y)] = count
            count += 1
    
    print(coord_to_num)
    print(num_to_coord)
    '''
    agent = np.zeros((board.shape[0], board.shape[0]), int)
    dimension = board.shape[0]
    agent[:] = -1 # -1 represents an unknown cell

    defused = 0
    total = 0

    moves = []
    
    knowledge_base = []

    for x in range(agent.shape[0]):
        for y in range(agent.shape[0]):
            moves.append((x, y))

    while len(moves) > 0:
        # Update knowledge base with most updated information before making a move
        knowledge_base = [(kb[0], kb[1], get_safe_neighbors(agent, kb[0]), 
        get_mine_neighbors(agent, kb[0]), get_hidden_neighbors(agent, kb[0])) for kb in knowledge_base]

        # try to make a move through basic inference
        if len(knowledge_base) > 0:
            removedItems = []
            inferenceMade = False
            moveMade = False

            for kb in knowledge_base:
                coord = kb[0]
                clue = kb[1]
                safe = kb[2]
                mines = kb[3]
                hidden = kb[4]

                # everything around is a mine
                if clue - mines == hidden:
                    newMines = get_all_hidden_neighbors(agent, coord)
                    for coord in newMines:
                        moves.remove(coord)
                        agent[coord[0]][coord[1]] = 9
                        defused += 1
                        total += 1
                    
                    inferenceMade = True
                    removedItems.append(kb)
                    
                
                # corner cell
                elif (x == 0 and y == 0) or (x == 0 and y == dimension - 1) or (x == dimension - 1 and y == 0) or (x == dimension - 1 and y == dimension - 1):
                    if (3 - clue) - safe == hidden:
                        safeList = get_all_hidden_neighbors(agent, coord)
                        markSafe(agent, board, safeList, moves, knowledge_base) # make a bunch of safe moves
                        inferenceMade = True
                        moveMade = True
                        removedItems.append(kb)
                        
                
                # border cell
                elif x == 0 or y == 0:
                    if (5 - clue) - safe == hidden:
                        safeList = get_all_hidden_neighbors(agent, coord)
                        markSafe(agent, board, safeList, moves, knowledge_base) # make a bunch of safe moves
                        inferenceMade = True
                        moveMade = True
                        removedItems.append(kb)
                        

                else:
                    if (8 - clue) - safe == hidden:
                        safeList = get_all_hidden_neighbors(agent, coord)
                        markSafe(agent, board, safeList, moves, knowledge_base)
                        inferenceMade = True
                        modeMade = True
                        removedItems.append(kb)
                        

            if inferenceMade == True:
                for item in removedItems:
                    knowledge_base.remove(item)
            else:
                # dictionary
                knowledge_base = [(kb[0], kb[1], get_safe_neighbors(agent, kb[0]), 
                get_mine_neighbors(agent, kb[0]), get_hidden_neighbors(agent, kb[0])) for kb in knowledge_base]
                colToCoordList = {} 
                coordToCol = {}

                count = 0
                for kb in knowledge_base:
                    coord = kb[0] 

                    hiddenList = get_all_hidden_neighbors(agent, coord)
                    for neighbor in hiddenList:
                        if neighbor not in colToCoordList.values():
                            colToCoordList[count] = neighbor
                            coordToCol[neighbor] = count
                            count += 1

                matrix = []

                # list of equations
                print(knowledge_base)
                for kb in knowledge_base:
                    coord = kb[0]
                    clue = kb[1]
                    safe = kb[2]
                    mines = kb[3]
                    hidden = kb[4]
                
                    equation = []
                    hiddenList = get_all_hidden_neighbors(agent, coord)

                    for i in range(0, count):
                        if colToCoordList[i] in hiddenList:
                            equation.append(1)
                        else:  
                            equation.append(0)
                    equation.append(clue - mines)
                    matrix.append(equation)
                
                print (matrix)



            
            if moveMade == True:
                continue # Since we have made a move(s) through our basic inference, no need to pick a random move

            # if we don't need to remove anything from the knowledge base, that means we didn't make any moves through basic inference
            # so, we must make a random choice

        # once we run out of moves, we end
        if len(moves) <= 0:
            break
        
        # pick random move
        i = randint(0, len(moves) - 1)
        coord = moves[i]
        x, y = coord
        agent[x][y] = board[x][y]

        # if we didn't pick a mine, add to knowledge base
        if agent[x][y] != 9:
            print('random safe move at')
            print(coord)
            knowledge_base.append((coord, agent[x][y], 
            get_safe_neighbors(agent, coord), 
            get_mine_neighbors(agent, coord), get_hidden_neighbors(agent, coord)))
        else:
            total += 1
            print('you picked a mine (random) at:')
            print(coord)
        
        moves.remove(coord)
    
    print(agent)
    return defused

def get_all_hidden_neighbors(agent, coord):
    neighbors = []
    dimension = agent.shape[0]
    x, y = coord

    if x - 1 >= 0:
        if agent[x - 1][y] == -1:
            neighbors.append((x - 1, y))
        if y - 1 >= 0:
            if agent[x - 1][y - 1] == -1:
                neighbors.append((x - 1, y - 1))
        if y + 1 < dimension:
            if agent[x - 1][y + 1] == -1:
                neighbors.append((x - 1, y + 1))
        
    if x + 1 < dimension:
        if agent[x + 1][y] == -1:
            neighbors.append((x + 1, y))
        if y - 1 >= 0:
            if agent[x + 1][y - 1] == -1:
                neighbors.append((x + 1, y - 1))
        if y + 1 < dimension:
            if agent[x + 1][y + 1] == -1:
                neighbors.append((x + 1, y + 1))
    
    if y - 1 >= 0:
        if agent[x][y - 1] == -1:
            neighbors.append((x, y - 1))
    
    if y + 1 < dimension:
        if agent[x][y + 1] == -1:
            neighbors.append((x, y + 1))
    
    return neighbors

def get_safe_neighbors(agent, coord):
    safe = 0
    dimension = agent.shape[0]
    x, y = coord

    if x - 1 >= 0:
        if agent[x - 1][y] != 9 and agent[x - 1][y] != -1:
            safe += 1
        if y - 1 >= 0:
            if agent[x - 1][y - 1] != 9 and agent[x - 1][y - 1] != -1:
                safe += 1
        if y + 1 < dimension:
            if agent[x - 1][y + 1] != 9 and agent[x - 1][y + 1] != -1:
                safe += 1
    
    if x + 1 < dimension:
        if agent[x + 1][y] != 9 and agent[x + 1][y] != -1:
            safe += 1
        if y - 1 >= 0:
            if agent[x + 1][y - 1] != 9 and agent[x + 1][y - 1] != -1:
                safe += 1
        if y + 1 < dimension:
            if agent[x + 1][y + 1] != 9 and agent[x + 1][y + 1] != -1:
                safe += 1
    
    if y - 1 >= 0:
        if agent[x][y - 1] != 9 and agent[x][y - 1] != -1:
            safe += 1
    
    if y + 1 < dimension:
        if agent[x][y + 1] != 9 and agent[x][y + 1] != -1:
            safe += 1

    return safe

def get_mine_neighbors(agent, coord):
    mines = 0
    dimension = agent.shape[0]
    x, y = coord

    if x - 1 >= 0:
        if agent[x - 1][y] == 9:
            mines += 1
        if y - 1 >= 0:
            if agent[x - 1][y - 1] == 9:
                mines += 1
        if y + 1 < dimension:
            if agent[x - 1][y + 1] == 9:
                mines += 1
    
    if x + 1 < dimension:
        if agent[x + 1][y] == 9:
            mines += 1
        if y - 1 >= 0:
            if agent[x + 1][y - 1] == 9:
                mines += 1
        if y + 1 < dimension:
            if agent[x + 1][y + 1] == 9:
                mines += 1
    
    if y - 1 >= 0:
        if agent[x][y - 1] == 9:
            mines += 1
    
    if y + 1 < dimension:
        if agent[x][y + 1] == 9:
            mines += 1

    return mines

def get_hidden_neighbors(agent, coord):
    hidden = 0
    dimension = agent.shape[0]
    x, y = coord

    if x - 1 >= 0:
        if agent[x - 1][y] == -1:
            hidden += 1
        if y - 1 >= 0:
            if agent[x - 1][y - 1] == -1:
                hidden += 1
        if y + 1 < dimension:
            if agent[x - 1][y + 1] == -1:
                hidden += 1
    
    if x + 1 < dimension:
        if agent[x + 1][y] == -1:
            hidden += 1
        if y - 1 >= 0:
            if agent[x + 1][y - 1] == -1:
                hidden += 1
        if y + 1 < dimension:
            if agent[x + 1][y + 1] == -1:
                hidden += 1
    
    if y - 1 >= 0:
        if agent[x][y - 1] == -1:
            hidden += 1
    
    if y + 1 < dimension:
        if agent[x][y + 1] == -1:
            hidden += 1

    return hidden

if __name__ == '__main__':
    board, totalMines = generate_board(20, 0.3)
    print(totalMines)
    defused = advanced_agent(board)
    print(defused)
    print(totalMines)