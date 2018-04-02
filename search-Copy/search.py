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

import util, node

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
"""
    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    root = util.Node()
    root.state = problem.getStartState()
    fringe = util.Stack()
    fringe.push(root)
    closed_set = set()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            return node.path

        if node.state not in closed_set:
            closed_set.add(node.state)
            successors = problem.getSuccessors(node.state)
            for successor in successors:
                if successor[0] not in closed_set:
                    element = util.Node()
                    element.state = successor[0]
                    element.dir = successor[1]
                    element.path = node.path + [successor[1]]
                    fringe.push(element)

    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    root = util.Node()
    root.state = problem.getStartState()
    fringe = util.Queue()
    fringe.push(root)

    closed_set = set()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            return node.path

        if node.state not in closed_set:
            closed_set.add(node.state)
            successors = problem.getSuccessors(node.state)
            for successor in successors:
                if successor[0] not in closed_set:
                    element = util.Node()
                    element.state = successor[0]
                    element.dir = successor[1]
                    element.path = node.path + [successor[1]]
                    fringe.push(element)
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    root = util.Node()
    root.state = problem.getStartState()
    root.priority = 0
    fringe = util.PriorityQueue()
    fringe.push(root,0)
    closed_set = set()

    while not fringe.isEmpty():
        node = fringe.pop()
        if problem.isGoalState(node.state):
            return node.path

        if node.state not in closed_set:
            closed_set.add(node.state)
            successors = problem.getSuccessors(node.state)
            for successor in successors:
                if problem.isGoalState(successor[0]):
                    return node.path + [successor[1]]
                if successor[0] not in closed_set:
                    element = util.Node()
                    element.state = successor[0]
                    element.dir = successor[1]
                    element.path = node.path + [successor[1]]
                    element.priority = node.cost + successor[2]
                    fringe.push(element, element.priority)

    print(closed_set)
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def manhattanHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""

    root = util.Node()
    root.state = problem.getStartState()
    root.cost = 0
    fringe = util.PriorityQueue()
    fringe.push(root, 0)

    for successor in problem.getSuccessors(problem.getStartState()):
        element = util.Node()
        element.state = successor[0]
        element.dir = successor[1]
        element.path = [successor[1]]
        element.cost = successor[2] + heuristic(successor[0], problem)
        fringe.push(element, element.cost)

    closed_set = set()

    while not fringe.isEmpty():
        node = fringe.pop()
        print(node.state)
        if problem.isGoalState(node.state):
            return node.path

        if node.state not in closed_set:
            closed_set.add(node.state)
            successors = problem.getSuccessors(node.state)
            for successor in successors:
                if problem.isGoalState(successor[0]):
                    return node.path + [successor[1]]
                if successor[0] not in closed_set:
                    heurval = heuristic(successor[0], problem)
                    element = util.Node()
                    element.state = successor[0]
                    element.dir = successor[1]
                    element.path = node.path + [successor[1]]
                    element.cost = node.cost + successor[2] + heurval
                    fringe.push(element, element.cost)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
