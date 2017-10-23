# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    some Directions.X for some X in the set {North, South, West, East, Stop}
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
    #print action
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    "*** YOUR CODE HERE ***"
    if action == 'Stop':
      return -10000

    foods = newFood.asList()
    if not foods:
      return 10000

    if successorGameState.getCapsules():
      distance = min(manhattanDistance(newPos, cap) for cap in successorGameState.getCapsules())
    else:
      distance = min(manhattanDistance(food, newPos) for food in foods)

    if not distance:
      score = 100
    else: 
      score = 1.0/distance
    #use of len(foods)**2 to make pacman work harder, but if squared too large pacman may be eaten
    score -= len(foods)**2
    for ghost in newGhostStates:
      distance = manhattanDistance(newPos, ghost.getPosition())
      if not distance:
        return -10000
      if ghost.scaredTimer:
        if ghostState.scaredTimer == 40:
          return 10000
        score -= 100*distance
      elif distance < 5:
        score += 2*distance
    return score




    '''nearestFood = 0; score = 0; dis_nearestFood = 'inf'
    for food in currentGameState.getFood().asList():
      dis = manhattanDistance(food, currentGameState.getPacmanPosition())
      if dis_nearestFood > dis:
        dis_nearestFood = dis
        nearestFood = food
        
    for ghost in newGhostStates:
      if ghost.scaredTimer <= 0:
        if not manhattanDistance(newPos,ghost.getPosition()) > 1:
          score += manhattanDistance(newPos, ghost.getPosition())
        else:
          score += 10
            
    return score - manhattanDistance(nearestFood,newPos)'''

    #return successorGameState.getScore()

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
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
  """

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (question 2)
  """
  def maxValue(self, gameState, level):
    if level == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    actions = gameState.getLegalActions(0)
    actions.remove('Stop')
    return max(self.minValue(gameState.generateSuccessor(0, action),
                            1, level) for action in actions)

  def minValue(self, gameState, ghost_id, level):
    if level == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    v = float('inf')
    actions = gameState.getLegalActions(ghost_id)
    for action in actions:
        if ghost_id < gameState.getNumAgents()-1:
            v = min(v, self.minValue(
                gameState.generateSuccessor(ghost_id, action), ghost_id+1, level))
        else:
            v = min(v, self.maxValue(
                gameState.generateSuccessor(ghost_id, action), level+1))
    return v

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    actions = gameState.getLegalActions(0)
    actions.remove('Stop')
    
    actions_val = {action: self.minValue(gameState.generateSuccessor(0, action), 1, 0)
                    for action in actions}
    return max(actions_val, key=actions_val.get)

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """
  def maxValue(self, gameState, level, a, b):
    if level == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    actions = gameState.getLegalActions(0)
    actions.remove('Stop')
    v = float('-inf')
    for action in actions:
        v = max(v, self.minValue(
                gameState.generateSuccessor(0, action), 1, level, a, b))
        if v >= b:
            return v
        a = max(a, v)
    return v

  def minValue(self, gameState, ghost_id, level, a, b):
    if level == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    actions = gameState.getLegalActions(ghost_id)
    v = float('inf')
    for action in actions:
        if ghost_id < gameState.getNumAgents()-1:
            v = min(v, self.minValue(
                gameState.generateSuccessor(ghost_id, action), ghost_id+1, level, a, b))
            if v <= a:
                return v
            b = min(b, v)
        else:
            v = min(v, self.maxValue(
                    gameState.generateSuccessor(ghost_id, action), level+1, a, b))
            if v <= a:
                return v
            b = min(b, v)
    return v

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    actions = gameState.getLegalActions(0)
    actions.remove('Stop')

    v = float('-inf')
    act = None
    a = float('-inf'); b = float('inf')
    for action in actions:
        val = self.minValue(
            gameState.generateSuccessor(0, action), 1, 0, a, b)
        if val > v:
            v = val
            act = action
        if v >= b:
            return act
        a = max(a, v)
    return act

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def maxValue(self, gameState, level):
    if level == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    actions = gameState.getLegalActions(0)
    actions.remove('Stop')
    return max(self.minValue(gameState.generateSuccessor(0, action),
                            1, level) for action in actions)

  def minValue(self, gameState, ghost_id, level):
    if level == self.depth or gameState.isWin() or gameState.isLose():
        return self.evaluationFunction(gameState)

    actions = gameState.getLegalActions(ghost_id)
    if ghost_id < gameState.getNumAgents()-1:
        return sum(self.minValue(
            gameState.generateSuccessor(ghost_id, action), ghost_id+1, level) for action in actions)/len(actions)
    else:
        return sum(self.maxValue(
            gameState.generateSuccessor(ghost_id, action), level+1) for action in actions)/len(actions)

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    actions = gameState.getLegalActions(0)
    actions.remove('Stop')
    
    actions_val = {action: self.minValue(gameState.generateSuccessor(0, action), 1, 0)
                    for action in actions}
    return max(actions_val, key=actions_val.get)

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This evaluation consists of three features:
                  1. distance to closest capsule and food
                    - consider capsules first
                    - consider foods only if no capsules left
                  2. number of food
                    - the fewer the better
                  3. distance to ghosts
                    - during hunting, shorter distance has much higher score
                    - in normal mode, prefer longer distance
  """
  "*** YOUR CODE HERE ***"
  if currentGameState.isLose():
      return -10000
  if currentGameState.isWin():
      return 10000
      
  pos = currentGameState.getPacmanPosition()
  foods = currentGameState.getFood().asList()
  ghostStates = currentGameState.getGhostStates()
  capsules = currentGameState.getCapsules()

  # let see if there're capsules
  score = 0
  if capsules:
      distance = min(manhattanDistance(pos, cap) for cap in capsules)
  else:
      # if no capsules, look for the closest food
      distance = min(manhattanDistance(pos, food) for food in foods)
  if not distance:
      score = 1000
  else:
      score = 1.0/distance

  # few foods, better
  score -= len(foods)**2

  # see how far the ghosts are
  for ghostState in ghostStates:
      distance = manhattanDistance(pos, ghostState.getPosition())
      # eat up the ghosts as fast as possible after eating capsules
      if ghostState.scaredTimer:
          if ghostState.scaredTimer > 37:
              #the timer is set to be 37, so that pacman would choose capsules
              #without worrying losing points as timer = 40
              return 10000
          else:
              score -= 100*distance
      # only count if ghosts are close
      elif distance < 5:
          score += 2*distance
  return score

better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

