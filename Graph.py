from collections import deque


class Graph:
   def __init__(self, graph_dict=None):
      if graph_dict is None:
         graph_dict = {}
      self.graph = graph_dict

# add edge btw two nodes
   def add_edge(self, node1, node2):
      if node1 not in self.graph:
         self.graph[node1] = []
      if node2 not in self.graph:
         self.graph[node2] = []

      if node2 not in self.graph[node1]: # not repeat the node in list of (voisins)
         # print(f"\n --> {type(self.graph[node1])}<=")
         self.graph[node1].append(node2)
      if node1 not in self.graph[node2]:
         self.graph[node2].append(node1)

   def display_graph(self):
      for node, neighbors in self.graph.items():
         print(f"{node} : {neighbors}")


#todo //////////////////////////////////////////////////////////////////
   def BFS(self, start_node):
      laFile = deque()
      ordered_list = []
      laFile.append(start_node)


      visited = {node: -1 for node in self.graph} # all values with -1
      visited[start_node] = 0

      # visited = {
      #    start_node: 0
      #    }

      while len(laFile) > 0:
         racine = laFile.popleft()
         current_distance = visited[racine]
         ordered_list.append(racine) # to stock the result of FIFO

         for voisin in self.graph[racine]:
            if visited[voisin] == -1:
               laFile.append(voisin) # enfiler les voisins des racine precedant
               visited[voisin] = current_distance + 1

      # inaccessible = False
      # for node in visited.keys(): # when a node is not connected with the starting node
      #    # if node not in visited:
      #    if visited[node] == -1:
      #       # visited[node] = 0
      #       inaccessible = True

      # print(f"-----> {ordered_list}")
      # if inaccessible:
      #    # print(f"Node -> {start_node} is inaccessible")
      #    return f"Node -> {start_node} is inaccessible"
      print(f"ordered list -> {ordered_list}")
      return visited

# todo: ////////////////////////////////////////////////////////

   def is_tree(self):
      # three conditions for a tree :
      # nbr edges = n -1
      # without cycls
      # connex -> visit all graph nodes

      if not self.graph:
         return False
      nbr = len(self.graph)
      edge_nbr = sum(len(voisin) for voisin in self.graph.values()) // 2

      if edge_nbr != nbr - 1: # nbr arcs < node - 1
         return False

      visited = set() # track visited node
      def DFS(node, parent): # cherche for cycles
         visited.add(node)
         for voisin in self.graph[node]:
            if voisin not in visited:
               if not DFS(voisin, node):
                  return False
            elif voisin != parent: #todo -->  bcz of graph indirectionnel -> verification des cycles
               return False # there is a cycle
         return True # sans cycle

      first_node = list(self.graph.keys())[0] # first case of list of nodes (keys) : so first node in graph
      if not DFS(first_node,None):
         return False

      if len(visited) != nbr: #todo--> visit all nodes
         return False


   def fermeture_transitive(self):
      print("\tFermeture Transitive du graphe est : ")
      new_graph = Graph(self.graph)

      for node in self.graph:
         stack = list(self.graph[node])
         # visited = set()
         while stack:
            current = stack.pop()
            # if current not in visited:
            #    visited.add(current)
            for voisin in self.graph[current]:
               if voisin not in self.graph[node]:
                  new_graph.add_edge(node,voisin)
      return new_graph



      # def dfs2(self, start_node): # not completed 
      #    stack = [] # empty stack
      #    stack.append(start_node)
      #    ordered_list = []
      #    visited = {
      #       start_node : 0
      #    }

      #    while len(stack) > 0:
      #       racine = stack.pop()
      #       ordered_list.append(racine)
      #       current_distance = visited[racine]

      #       for voisin in sorted(self.graph[racine], reverse=True):
      #          if voisin not in visited:
      #             stack.append(voisin)
      #             visited[voisin] = current_distance + 1
      #       inacessible = False
      #       for node in self.graph.keys():
      #          if node not in visited:
      #             inacessible = True

      #       if inacessible:
      #          print(f"node { start_node} incaccessible ")
      #    return visited
      return True