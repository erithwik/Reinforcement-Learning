import random
import time

#-----------------------------------------------------------------
# This is the value space
#-----------------------------------------------------------------

POINTSLIST = [(0,1), (1,5), (5,6), (5,4), (1,2), (2,3), (2,7)]
INIT_STATE = 3 #This needs to change to give new starting point
GOAL = 7

NUM_SPOTS = 8
GAMMA = 0.9
NUM_EPISODES = 10

#-----------------------------------------------------------------
# This is the function space
#-----------------------------------------------------------------

def printMatrix(mat):
  for i in range(0, len(mat)):
    for j in range(0, len(mat[i])):
      print(str(mat[i][j])+ " ", end = '')
    print('\n')

def matrixMaker(rows, columns):
  tmp = []
  for i in range(0, rows):
    t = []
    for j in range(0, columns):
      t.append(0)
    tmp.append(t)
  return tmp

def rewardsMatrixMaker(points, matrix): #This needs to adjusted given a new ending point
  mat = matrix
  for i in range(0, len(mat)):
    for j in range(0, len(mat[i])):
      mat[i][j] = -1
  
  for (a,b) in points:
    mat[a][b] = 0
    mat[b][a] = 0

  mat[4][4] = 100
  mat[5][4] = 100
  return mat

def availableActions(rev, state):
  tmp = []
  for i in range(0, len(rev[state])):
    if(rev[state][i] >= 0):
      tmp.append(i)
  return tmp

def areAllZeros(a):
  isZero = True
  for i in range(0, len(a)):
    if(a[i] != 0):
      isZero = False
      break
  return isZero

def chooseAction(theQTable, state, rewards):
  potActions = availableActions(rewards, state)
  # print(potActions)
  checkList = []
  for i in range(0, len(potActions)):
    checkList.append(theQTable[state][potActions[i]])
  
  if(areAllZeros(checkList)):
    action = potActions[random.randint(0, len(potActions)-1)]
    # print('zeros')
  else:
    action = potActions[checkList.index(max(checkList))]
    # print('not random')
  return action

def envResponse(state, action): #This needs to adjusted to give a new ending point
  reward = 0
  if(action == 4):
    reward = 100
    state = 'end'
  else:
    reward = 0
    state = action
  return reward, state

def learning(): 
  rewards = matrixMaker(NUM_SPOTS, NUM_SPOTS)
  rewards = rewardsMatrixMaker(POINTSLIST, rewards) # This initia

  qMatrix = matrixMaker(NUM_SPOTS, NUM_SPOTS)

  for episodes in range(NUM_EPISODES):

    steps = 0
    isEnded = False
    currState = INIT_STATE
    print(currState)

    while(isEnded == False):
      A = chooseAction(qMatrix, currState, rewards)
      # print("Action: " + str(A))
      R, nextState = envResponse(currState, A)


      if(nextState != 'end'):
        nextStateVals = []
        for i in range(0, len(qMatrix[nextState])):
          nextStateVals.append(qMatrix[nextState][i])
        rewardVal = R + GAMMA * (max(nextStateVals))
      else:
        isEnded = True
        rewardVal = R

      qMatrix[currState][A] = rewardVal
      currState = nextState

      # print("-----------------------------")
      print(currState)
      time.sleep(.2)
      steps += 1
    
    print("Episode: " + str(episodes))
    print("Number of steps: " + str(steps))

  return qMatrix


#-----------------------------------------------------------------
# This is the work space
#-----------------------------------------------------------------

printMatrix(learning())