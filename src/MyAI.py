# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent

class MyAI ( Agent ):

    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        # Direction agent faces
        self.direction = "E"

        # List of previous moves
        self.previousMoves = []

        # Number of total moves
        self.numberOfMoves = 0

        # Location of agent in coordinate form (x, y)
        self.x_Coordinate = 0
        self.y_Coordinate = 0

        # Right and top boundary value (4x4 or 6x6 board)
        self.rightBoundary = 0
        self.topBoundary = 0

        # Found gold or not found gold
        self.gold = False

        # Lists of types of coordinates
        self.breezeCoordinates = []
        self.stenchCoordinates = []
        self.safeCoordinates = []
        self.maybePitCoordinates = []
        self.maybeWumpusCoordinates = []
        self.visitedCoordinates = [(0,0)]

        self.wumpusCoordinates = ()
        self.killedWumpus = False
        self.found = False
        self.stenchOnly = False

        self.shotArrow = False
        
        self.map = [[0] * 8 for _ in range(8)]

        self.movesToBackTrack = []
        self.nodeToNodeBackTrack = []

        self.justBackTracked = False

        pass
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter, bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        # Check each new position if there's a bump
        self.bumpCheck(bump)

        # Test if the program actually runs
        # print(self.direction)
        # print(self.x_Coordinate, self.y_Coordinate)

        # Increment total number of moves
        self.numberOfMoves += 1
        # print(self.numberOfMoves)

        # if self.numberOfMoves > 50:
        #     return self.climbOut()

        # for i in range(len(self.map))[::-1]:
        #     for row in self.map:
        #         print(row[i], ", ", end = "")
        #     print()
        # print("VISITED: ", self.visitedCoordinates)
        # print("BREEZE: ", self.breezeCoordinates)
        # print("STENCH: ", self.stenchCoordinates)
        # print("CURRENT: ", self.x_Coordinate, self.y_Coordinate)
        # print("PREVIOUS MOVES: ", self.previousMoves)

        # print("DIRECTION: ", self.direction)


        # print(self.movesToBackTrack)
        
        return self.nextMove(stench, breeze, glitter, bump, scream)
        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================
    
    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    
    # Coordinate class stores coordinates of itself and coordinates of nodes around it
    class Coordinate:
        def __init__(self, x, y):
            self.coordinates = (x,y)
            self.aboveCoordinates = (x, y + 1)
            self.rightCoordinates = (x + 1, y)
            self.belowCoordinates = (x, y - 1)
            self.leftCoordinates = (x - 1, y)
            self.state = None

        def getX(self):
            return self.coordinates[0]
        def getY(self):
            return self.coordinates[1]

        def getCurrent(self):
            return self.coordinates
        def getAbove(self):
            return self.aboveCoordinates
        def getRight(self):
            return self.rightCoordinates
        def getBelow(self):
            return self.belowCoordinates
        def getLeft(self):
            return self.leftCoordinates

    # Converting direction to coordinate value (x, y)
    def direction_to_coordinate(self, direction):
        if direction == "N":
            return (0, 1)
        elif direction == "E":
            return (1, 0)
        elif direction == "S":
            return (0, -1)
        elif direction == "W":
            return (-1, 0)

    # Methods to move the agent and adjust direction
    def moveUp(self):
        if self.direction == "N":
            self.previousMoves.append("FORWARD")
            self.x_Coordinate += self.direction_to_coordinate(self.direction)[0]
            self.y_Coordinate += self.direction_to_coordinate(self.direction)[1]
            return Agent.Action.FORWARD
        elif self.direction == "E":
            self.previousMoves.append("FORWARD")
            self.x_Coordinate += self.direction_to_coordinate(self.direction)[0]
            self.y_Coordinate += self.direction_to_coordinate(self.direction)[1]
            return Agent.Action.FORWARD
        elif self.direction == "S":
            self.previousMoves.append("FORWARD")
            self.x_Coordinate += self.direction_to_coordinate(self.direction)[0]
            self.y_Coordinate += self.direction_to_coordinate(self.direction)[1]
            return Agent.Action.FORWARD
        elif self.direction == "W":
            self.previousMoves.append("FORWARD")
            self.x_Coordinate += self.direction_to_coordinate(self.direction)[0]
            self.y_Coordinate += self.direction_to_coordinate(self.direction)[1]
            return Agent.Action.FORWARD

    # def moveDown(self):
    #     if self.direction == "N":
    #         self.direction = "W"
    #         self.previousMoves.append("TURN_LEFT")
    #         return Agent.Action.TURN_LEFT
    #     elif self.direction == "E":
    #         self.direction = "S"
    #         self.previousMoves.append("TURN_RIGHT")
    #         return Agent.Action.TURN_RIGHT
    #     elif self.direction == "S":
    #         self.previousMoves.append("FORWARD")
    #         self.x_Coordinate += self.direction_to_coordinate(self.direction)[0]
    #         self.y_Coordinate += self.direction_to_coordinate(self.direction)[1]
    #         return Agent.Action.FORWARD
    #     elif self.direction == "W":
    #         self.direction = "S"
    #         self.previousMoves.append("TURN_LEFT")
    #         return Agent.Action.TURN_LEFT

    def moveRight(self):
        if self.direction == "N":
            self.direction = "E"
            self.previousMoves.append("TURN_RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.direction == "E":
            self.direction = "S"
            self.previousMoves.append("TURN_RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.direction == "S":
            self.direction = "W"
            self.previousMoves.append("TURN_RIGHT")
            return Agent.Action.TURN_RIGHT
        elif self.direction == "W":
            self.direction = "N"
            self.previousMoves.append("TURN_RIGHT")
            return Agent.Action.TURN_RIGHT

    def moveLeft(self):
        if self.direction == "N":
            self.direction = "W"
            self.previousMoves.append("TURN_LEFT")
            return Agent.Action.TURN_LEFT
        elif self.direction == "E":
            self.direction = "N"
            self.previousMoves.append("TURN_LEFT")
            return Agent.Action.TURN_LEFT
        elif self.direction == "S":
            self.direction = "E"
            self.previousMoves.append("TURN_LEFT")
            return Agent.Action.TURN_LEFT
        elif self.direction == "W":
            self.direction = "S"
            self.previousMoves.append("TURN_LEFT")
            return Agent.Action.TURN_LEFT

    # Check if agent hit a top/right boundary
    def bumpCheck(self, bump):
        if bump == True:
            self.x_Coordinate -= self.direction_to_coordinate(self.direction)[0]
            self.y_Coordinate -= self.direction_to_coordinate(self.direction)[1]
            if self.direction == "N":
                self.topBoundary = self.y_Coordinate
            elif self.direction == "E":
                self.rightBoundary = self.x_Coordinate
            self.previousMoves.pop()

    def climbOut(self):
        if len(self.previousMoves) != 0:
            current = self.previousMoves[-1]
            if current == "TURN_LEFT":
                self.previousMoves.pop()
                if self.direction == "N":
                    self.direction = "E"
                elif self.direction == "E":
                    self.direction = "S"
                elif self.direction == "S":
                    self.direction = "W"
                elif self.direction == "W":
                    self.direction = "N"
                return Agent.Action.TURN_RIGHT
            elif current == "TURN_RIGHT":
                self.previousMoves.pop()
                if self.direction == "N":
                    self.direction = "W"
                elif self.direction == "W":
                    self.direction = "S"
                elif self.direction == "S":
                    self.direction = "E"
                elif self.direction == "E":
                    self.direction = "N"
                return Agent.Action.TURN_LEFT
            elif current == "FORWARD":
                self.previousMoves.pop()
                self.movesToBackTrack.append(Agent.Action.TURN_RIGHT)
                self.movesToBackTrack.append(Agent.Action.TURN_RIGHT)
                self.movesToBackTrack.append(Agent.Action.FORWARD)
                self.movesToBackTrack.append(Agent.Action.TURN_RIGHT)
                if self.direction == "N":
                    self.direction = "E"
                elif self.direction == "E":
                    self.direction = "S"
                elif self.direction == "S":
                    self.direction = "W"
                elif self.direction == "W":
                    self.direction = "N"
                return Agent.Action.TURN_RIGHT
        return Agent.Action.CLIMB

    # Function to undo previous move
    def backOneStep(self):
        self.justBackTracked = True
        previousMove = self.previousMoves.pop()
        if previousMove == "TURN_LEFT":
            if self.direction == "N":
                self.direction = "E"
            elif self.direction == "E":
                self.direction = "S"
            elif self.direction == "S":
                self.direction = "W"
            elif self.direction == "W":
                self.direction = "N"
            return Agent.Action.TURN_RIGHT
        elif previousMove == "TURN_RIGHT":
            if self.direction == "N":
                self.direction = "W"
            elif self.direction == "W":
                self.direction = "S"
            elif self.direction == "S":
                self.direction = "E"
            elif self.direction == "E":
                self.direction = "N"
            return Agent.Action.TURN_LEFT
        elif previousMove == "FORWARD":
            self.movesToBackTrack.append(Agent.Action.TURN_RIGHT)
            self.movesToBackTrack.append(Agent.Action.TURN_RIGHT)
            self.movesToBackTrack.append(Agent.Action.FORWARD)
            self.movesToBackTrack.append(Agent.Action.TURN_RIGHT)
            if self.direction == "N":
                self.direction = "E"
            elif self.direction == "E":
                self.direction = "S"
            elif self.direction == "S":
                self.direction = "W"
            elif self.direction == "W":
                self.direction = "N"
            return Agent.Action.TURN_RIGHT

    def nextMove(self, stench, breeze, glitter, bump, scream):
        if len(self.movesToBackTrack) != 0:
            if self.movesToBackTrack[-1] == Agent.Action.TURN_RIGHT:
                if self.direction == "N":
                    self.direction = "E"
                elif self.direction == "E":
                    self.direction = "S"
                elif self.direction == "S":
                    self.direction = "W"
                elif self.direction == "W":
                    self.direction = "N"
            elif self.movesToBackTrack[-1] == Agent.Action.TURN_LEFT:
                if self.direction == "N":
                    self.direction = "W"
                elif self.direction == "E":
                    self.direction = "N"
                elif self.direction == "S":
                    self.direction = "E"
                elif self.direction == "W":
                    self.direction = "S"
            if len(self.movesToBackTrack) == 3:
                self.x_Coordinate += self.direction_to_coordinate(self.direction)[0]
                self.y_Coordinate += self.direction_to_coordinate(self.direction)[1]

            if self.gold == True and self.x_Coordinate == 0 and self.y_Coordinate == 0:
                return Agent.Action.CLIMB
            return self.movesToBackTrack.pop()

        if len(self.nodeToNodeBackTrack) != 0:
            return self.nodeToNodeBackTrack.pop()

        if glitter:
            self.gold = True
            self.visitedCoordinates.append((self.x_Coordinate, self.y_Coordinate))
            if not breeze and not bump and not stench:
                self.addToSafeCoordinates(self.x_Coordinate, self.y_Coordinate)
            return Agent.Action.GRAB

        if self.gold == True and self.x_Coordinate == 0 and self.y_Coordinate == 0:
            return Agent.Action.CLIMB
        
        if self.gold == True:
            return self.climbOut()

        if not breeze and not bump and not stench:
            self.addToSafeCoordinates(self.x_Coordinate, self.y_Coordinate)

        if breeze:
            self.addToBreezeCoordinates(self.x_Coordinate, self.y_Coordinate)

        if stench and not self.killedWumpus:
            self.addToStenchCoordinates(self.x_Coordinate, self.y_Coordinate)

        if (stench or breeze) and self.x_Coordinate == 0 and self.y_Coordinate == 0:
            return Agent.Action.CLIMB

        if bump:
            if self.direction == "N":
                self.topBoundary = self.y_Coordinate
                for coordinate in self.safeCoordinates:
                    if coordinate[1] > self.topBoundary:
                        self.safeCoordinates.remove(coordinate)
            elif self.direction == "E":
                self.rightBoundary = self.x_Coordinate
                for coordinate in self.safeCoordinates:
                    if coordinate[0] > self.rightBoundary:
                        self.safeCoordinates.remove(coordinate)
            #return self.backOneStep()
            return self.findNewPath()

        if breeze or stench:
            return self.backOneStep()

        # print("JUST BACK TRACKED: ", self.justBackTracked)

        if not self.justBackTracked:
            return self.moveUp()
        else:
            return self.findNewPath()

    # def turnToWumpus(self,stench, breeze, glitter, bump, scream):
    #     currentLocation = self.Coordinate(self.x_Coordinate, self.y_Coordinate)
    #     nextLocation = self.Coordinate(self.wumpusCoordinates[0], self.wumpusCoordinates[1])
    #     return self.nodeToNode(nextLocation, currentLocation)

    def getNeighbors(self, x, y):
        if x == 0 and y == 0:
            return [(x + 1, y), (x, y + 1)]
        elif y == 0 and x == self.rightBoundary:
            return [(x, y + 1), (x - 1, y)]
        elif x == 0 and y == self.topBoundary:
            return [(x + 1, y), (x, y - 1)]
        elif y == 0:
            return [(x + 1, y), (x - 1, y), (x, y + 1)]
        elif x == 0:
            return [(x, y + 1), (x, y - 1), (x + 1, y)]
        elif x == self.rightBoundary and y == self.topBoundary:
            return [(x, y - 1), (x - 1, y)]
        elif x == self.rightBoundary:
            return [(x, y + 1), (x, y - 1), (x - 1, y)]
        elif y == self.topBoundary:
            return [(x + 1, y), (x - 1, y), (x, y - 1)]
        else:
            return [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

    def findNewPath(self):
        placesToGo = []
        self.justBackTracked = False

        # print("NEIGHBORS: ", self.getNeighbors(self.x_Coordinate, self.y_Coordinate))

        for neighbor in self.getNeighbors(self.x_Coordinate, self.y_Coordinate):
            if neighbor not in self.visitedCoordinates:
                placesToGo.append(neighbor)

        # print("PLACES TO GO: ", placesToGo)

        if len(placesToGo) == 0:
            if self.x_Coordinate == 0 and self.y_Coordinate == 0:
                return Agent.Action.CLIMB
            return self.backOneStep()
        else:
            self.visitedCoordinates.append(placesToGo[0])
            return self.nodeToNode(placesToGo[0], (self.x_Coordinate, self.y_Coordinate))

    def nodeToNode(self, nextLocation, currentLocation):
        xDifference = nextLocation[0] - currentLocation[0]
        yDifference = nextLocation[1] - currentLocation[1]
        # print("NEXT LOCATION: ", xDifference, yDifference)
        if (xDifference, yDifference) == (0,1):
            if self.direction == "N":
                return self.moveUp()
            elif self.direction == "W":
                return self.moveRight()
            elif self.direction == "E":
                return self.moveLeft()
            elif self.direction == "S":
                self.nodeToNodeBackTrack.append(Agent.Action.TURN_LEFT)
                self.direction = "E"
                self.previousMoves.append("TURN_LEFT")
                return self.moveLeft()
        elif (xDifference, yDifference) == (0,-1):
            if self.direction == "S":
                return self.moveUp()
            elif self.direction == "W":
                return self.moveLeft()
            elif self.direction == "E":
                return self.moveRight()
            elif self.direction == "N":
                self.nodeToNodeBackTrack.append(Agent.Action.TURN_LEFT)
                self.previousMoves.append("TURN_LEFT")
                self.direction = "W"
                return self.moveLeft()
        elif (xDifference, yDifference) == (1,0):
            if self.direction == "E":
                return self.moveUp()
            elif self.direction == "N":
                return self.moveRight()
            elif self.direction == "S":
                return self.moveLeft()
            elif self.direction == "W":
                self.nodeToNodeBackTrack.append(Agent.Action.TURN_LEFT)
                self.direction = "S"
                self.previousMoves.append("TURN_LEFT")
                return self.moveLeft()
        elif (xDifference, yDifference) == (-1,0):
            if self.direction == "W":
                return self.moveUp()
            elif self.direction == "N":
                return self.moveLeft()
            elif self.direction == "S":
                return self.moveRight()
            elif self.direction == "E":
                self.nodeToNodeBackTrack.append(Agent.Action.TURN_LEFT)
                self.direction = "N"
                self.previousMoves.append("TURN_LEFT")
                return self.moveLeft()
        else:
            return self.moveUp()

    def addToBreezeCoordinates(self, x, y):
        self.map[self.x_Coordinate][self.y_Coordinate] = 2
        
        if (self.x_Coordinate, self.y_Coordinate) not in self.visitedCoordinates:
            self.visitedCoordinates.append((self.x_Coordinate, self.y_Coordinate))

        # Adding the breezy pit to a list of breezy pits
        if (x, y) not in self.breezeCoordinates:
            self.breezeCoordinates.append((x, y))

        # Making a list of all adjacent pits which may have a pit
        possibleNeighborPits = []
        if x - 1 >= 1:
            if (x - 1, y) not in self.safeCoordinates: 
                possibleNeighborPits.append((x - 1, y))
        if x + 1 <= self.rightBoundary:
            if (x + 1, y) not in self.safeCoordinates:
                possibleNeighborPits.append((x + 1, y))
        if y - 1 >= 1:
            if (x, y - 1) not in self.safeCoordinates:
                possibleNeighborPits.append((x, y - 1))
        if y + 1 <= self.topBoundary:
            if (x, y + 1) not in self.safeCoordinates:
                possibleNeighborPits.append((x, y + 1))

        # Adding all possible pits to the possible pit list
        for pit in possibleNeighborPits:
            if pit not in self.maybePitCoordinates:
                self.maybePitCoordinates.append(pit)

    def addToSafeCoordinates(self, x, y):
        self.map[self.x_Coordinate][self.y_Coordinate] = 1
        if (self.x_Coordinate, self.y_Coordinate) not in self.visitedCoordinates:
            self.visitedCoordinates.append((self.x_Coordinate, self.y_Coordinate))

        # Checking boundaries and adding to safe coordinates
        # Also removing from potential dangerous coordinates
        if (x, y) not in self.safeCoordinates:
            self.safeCoordinates.append((x, y))
            if (x, y) in self.maybeWumpusCoordinates:
                self.maybeWumpusCoordinates.remove((x, y))
            if (x, y) in self.maybePitCoordinates:
                self.maybePitCoordinates.remove((x, y))

        if (x - 1 >= 1) and (x - 1, y) not in self.safeCoordinates:
            self.safeCoordinates.append((x - 1, y))
            if (x - 1, y) in self.maybeWumpusCoordinates:
                self.maybeWumpusCoordinates.remove((x - 1, y))
            if (x - 1, y) in self.maybePitCoordinates:
                self.maybePitCoordinates.remove((x - 1, y))

        if (y - 1 >= 1) and (x, y - 1) not in self.safeCoordinates:
            self.safeCoordinates.append((x, y - 1))
            if (x, y - 1) in self.maybeWumpusCoordinates:
                self.maybeWumpusCoordinates.remove((x, y - 1))
            if (x, y - 1) in self.maybePitCoordinates:
                self.maybePitCoordinates.remove((x, y - 1))

        if (x + 1 <= self.rightBoundary) and ((x + 1), y) not in self.safeCoordinates:
            self.safeCoordinates.append((x + 1, y))
            if (x + 1, y) in self.maybeWumpusCoordinates:
                self.maybeWumpusCoordinates.remove((x + 1, y))
            if (x + 1, y) in self.maybePitCoordinates:
                self.maybePitCoordinates.remove((x + 1, y))

        if (y + 1 <= self.topBoundary) and (x, (y + 1)) not in self.safeCoordinates:
            self.safeCoordinates.append((x, y + 1))
            if (x, y + 1) in self.maybeWumpusCoordinates:
                self.maybeWumpusCoordinates.remove((x, y + 1))
            if (x, y + 1) in self.maybePitCoordinates:
                self.maybePitCoordinates.remove((x, y + 1))

    # def facingWumpus(self):
    #     if self.direction == "N":
    #         if self.wumpusCoordinates[1] > self.y_Coordinate:
    #             return True
    #     elif self.direction == "S":
    #         if self.wumpusCoordinates[1] < self.y_Coordinate:
    #             return True
    #     elif self.direction == "W":
    #         if self.wumpusCoordinates[0] < self.x_Coordinate:
    #             return True
    #     elif self.direction == "E":
    #         if self.wumpusCoordinates[0] > self.x_Coordinate:
    #             return True
    #     return False

    def addToStenchCoordinates(self, x, y):
        self.map[self.x_Coordinate][self.y_Coordinate] = 2

        if (self.x_Coordinate, self.y_Coordinate) not in self.visitedCoordinates:
            self.visitedCoordinates.append((self.x_Coordinate, self.y_Coordinate))

        if (x, y) not in self.stenchCoordinates:
             self.stenchCoordinates.append((x, y))

        possibleNeighborWumpus = []
        if self.found == False:
            if x - 1 >= 1:
                if (x - 1, y) not in self.safeCoordinates:
                    possibleNeighborWumpus.append((x - 1, y))
            if x + 1 <= self.rightBoundary:
                if (x + 1, y) not in self.safeCoordinates:
                    possibleNeighborWumpus.append((x + 1, y))
            if y - 1 >= 1:
                if (x, y - 1) not in self.safeCoordinates:
                    possibleNeighborWumpus.append((x, y - 1))
            if y + 1 <= self.topBoundary:
                if (x, y + 1) not in self.safeCoordinates:
                    possibleNeighborWumpus.append((x, y + 1))

        for wumpus in possibleNeighborWumpus:
            if wumpus in self.maybeWumpusCoordinates:
                self.found = True
                self.maybeWumpusCoordinates = []
                self.maybeWumpusCoordinates.append(wumpus)
                self.wumpusCoordinates = wumpus
                break
            else:
                self.maybeWumpusCoordinates.append(wumpus)

        if self.found and (self.stenchOnly == False):
            for coordinate in self.stenchCoordinates:
                if coordinate not in self.breezeCoordinates:
                    self.stenchOnly = True
                    break
        

    
    
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================