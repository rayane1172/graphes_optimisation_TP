from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

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
      visited = {node: float('inf') for node in self.graph} # all values with -1
      visited[start_node] = 0

      while len(laFile) > 0:
         racine = laFile.popleft()
         current_distance = visited[racine]
         ordered_list.append(racine) # to stock the result of FIFO

         for voisin in self.graph[racine]:
            if visited[voisin] == float('inf'):
               laFile.append(voisin) # enfiler les voisins des racine precedant
               visited[voisin] = current_distance + 1

      # print(f"ordered list -> {ordered_list}")
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

      visited = set()
      def DFS(node, parent): # chercher for cycles
         visited.add(node)
         for voisin in self.graph[node]:
            if voisin not in visited:
               if not DFS(voisin, node):
                  return False
            elif voisin != parent: #todo -->  bcz of graph indirectionnel -> verification des cycles (if the source is not from the last parent only )
               return False # there is a cycle
         return True # sans cycle

      first_node = list(self.graph.keys())[0] # first case of list of nodes (keys) : so first node in graph
      if not DFS(first_node,None):
         return False

      if len(visited) != nbr: #todo--> visit all nodes
         return False


   def fermeture_transitive(self):
      # print("\tFermeture Transitive du graphe est : ")
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


# todo -> print graph

   def visualize(self, nodes_color=None):
      G = nx.Graph()
      for node, neighbors in self.graph.items():
         for neighbor in neighbors:
            G.add_edge(node, neighbor)

      pos = nx.spring_layout(G)

      # dictionnary of colors provided
      if nodes_color:
         colors = [nodes_color.get(node, -1) for node in G.nodes()]
         # print(colors)
      else:
         colors = "skyblue"

      nx.draw(G, pos, with_labels=True, node_size=700, node_color=colors, font_size=8, font_weight="bold", edge_color="grey")
      plt.show()


# todo -> welsh and powel algorithm

   def welsh_powell(self):
   # sort the nodes
      sorted_nodes = sorted(self.graph, key=lambda node: len(self.graph[node]), reverse=True)
      # print(sorted_nodes)
      nodes_colors = {}
      color = 0

      for node in sorted_nodes:

         neighbor_colors = set()
         for neighbor in self.graph[node]:
            if neighbor in nodes_colors:
               neighbor_colors.add(nodes_colors[neighbor])

         while color in neighbor_colors: #Tq color used by neighbors
            color += 1

         nodes_colors[node] = color
         #for next node
         color = 0

      print(f"Number of colors :{max(nodes_colors.values())+1}")
      self.visualize(nodes_colors)
      # print(type(nodes_color))
      return nodes_colors


# todo-> DSATUR algorithm

   def dsatur_algo(self):
      nodes_colors = {} # todo -> dict for nodes colored
      saturation_degree = {node: 0 for node in self.graph}  # saturation degree of each node

      degree = {node: len(neighbors) for node, neighbors in self.graph.items()}  # Tracks the degree of each node
      uncolored_nodes = set(self.graph.keys())  # Set of uncolored nodes

      current_node = max(degree, key=degree.get) # node with highest degree (lot of neighbors)

      nodes_colors[current_node] = 0  # Assign the first color
      uncolored_nodes.remove(current_node)

      # Update saturation degree for neighbors
      for neighbor in self.graph[current_node]:
         saturation_degree[neighbor] += 1

      while uncolored_nodes:
         #todo -> find the node with the highest saturation degree (if equal we choose the highest degree )
         current_node = max(uncolored_nodes, key=lambda node: (saturation_degree[node], degree[node]))

         #todo -> Find the lowest possible color not used by its neighbors
         neighbor_colors = {nodes_colors[neighbor] for neighbor in self.graph[current_node] if neighbor in nodes_colors}
         #! set() of neighbors colors

         color = 0
         # print(neighbor_colors)

         while color in neighbor_colors:
            color += 1

         nodes_colors[current_node] = color #todo -> give it the color

         #todo -> update the saturation degree of its neighbors
         for neighbor in self.graph[current_node]:
            if neighbor not in nodes_colors: # todo -> to update only uncolored neighbors
               neighbor_colors = {nodes_colors[node] for node in self.graph[neighbor] if node in nodes_colors}
               saturation_degree[neighbor] = len(neighbor_colors)

         uncolored_nodes.remove(current_node) # node colored finally

      print(f"Number of colors :{max(nodes_colors.values())+1}")
      self.visualize(nodes_colors)
      return nodes_colors


# todo -> recursive largest first algorithm

   def RLF(self):

      nodes_colors = {}
      color = 0

      while len(nodes_colors)<len(self.graph): #todo -> WH all nodes are colored
         uncolored_nodes = [node for node in self.graph if node not in nodes_colors]
         independent_set = set() #todo -> everytime generate empty set to test again

         while uncolored_nodes:
            #todo -> find node with max not colored neighbors
            node = max(uncolored_nodes,
                  key=lambda anyNode: sum (1 for neighbor in self.graph[anyNode] if neighbor not in nodes_colors))
            independent_set.add(node)

            # todo -> remove it and his neighbors
            uncolored_nodes = [n for n in uncolored_nodes if n != node and n not in self.graph[node]]

         for node in independent_set:
            nodes_colors[node] = color

         color+=1

      nbr_color = max(nodes_colors.values()) + 1
      print(f"Number of color is :{nbr_color} ")
      self.visualize(nodes_colors)
      return nodes_colors