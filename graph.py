# Use topological sort to check whether commits are cyclic or not

# https://www.geeksforgeeks.org/python-program-for-topological-sorting/

# Python program to print topological sorting of a DAG
from collections import defaultdict
from typing import List, Any
 
#Class to represent a graph
class Graph:
  graph: defaultdict[Any, list]
  V: int

  def __init__(self: 'Graph', vertices: int) -> None:
    self.graph = defaultdict(list) #dictionary containing adjacency List
    self.V = vertices #No. of vertices

  # function to add an edge to graph
  def addEdge(self: 'Graph', u: int, v: int) -> None:
    self.graph[u].append(v)

  # A recursive function used by topologicalSort
  def topologicalSortUtil(self: 'Graph', v: int, visited: List[bool], stack: List[int]) -> None:
    # Mark the current node as visited.
    visited[v] = True

    # Recur for all the vertices adjacent to this vertex
    for i in self.graph[v]:
      if visited[i] == False:
        self.topologicalSortUtil(i, visited, stack)

    # Push current vertex to stack which stores result
    stack.insert(0, v)

  # The function to do Topological Sort. It uses recursive
  # topologicalSortUtil()
  def topologicalSort(self: 'Graph') -> bool:
    # Mark all the vertices as not visited
    visited = [False]*self.V
    stack = []

    # Call the recursive helper function to store Topological
    # Sort starting from all vertices one by one
    for i in range(self.V):
      if visited[i] == False:
        self.topologicalSortUtil(i, visited, stack)

    return all(stack[i] > stack[i+1] for i in range(len(stack) - 1))