from __future__ import print_function
__author__ = 'panzer'
import os, sys, json
sys.path.append(os.path.abspath("."))
sys.dont_write_bytecode = True

# Edge Values
# make = "make"
# help = "help"
# someplus = "someplus"
# someminus = "someminus"
# hurt = "hurt"
# destroy = "break"
# conflict = "conflict"
# AND = "and"
# OR = "or"
# dep = dependency = "dependency"
#
# # Node Types
# softgoal = "softgoal"
# hardgoal = "goal"
# task = "task"
# resource = "resource"
# agent = "agent"
# role = "role"

def decode(input):
  if isinstance(input, dict):
    return {decode(key):decode(value) for key,value in input.iteritems()}
  elif isinstance(input, list):
    return [decode(element) for element in input]
  elif isinstance(input, unicode):
    return input.encode('utf-8')
  else:
    return input


class O(object):
  """
  Default class that gives
  kwargs properties
  """
  def __init__(self,**d): self.has().update(**d)
  def has(self): return self.__dict__
  def update(self,**d): self.has().update(d); return self
  def __repr__(self)   :
    def _name(val):
      if isinstance(val, list):
        return [v for v in val]
      if hasattr(val, '__call__'):
        return val.__name__
      return val
    show=[':%s %s' % (k,_name(self.has()[k]))
      for k in sorted(self.has().keys() )
      if k[0] is not "_"]
    txt = ' '.join(show)
    if len(txt) > 60:
      show=map(lambda x: '\t'+x+'\n',show)
    return '{'+' '.join(show)+'}'
  def __getitem__(self, item):
    return self.has().get(item, None)
  def __getattr__(self, item):
    return self.has().get(item, None)
  def to_json(self):
    def dflt(obj):
      if isinstance(obj, set): return list(obj)
      return obj.__dict__
    return json.dumps(self, default=dflt, sort_keys=True, indent=4)
  def clone(self):
    cloned = O()
    for key, val in self.has().iteritems():
      cloned.__dict__[key] = val
    return cloned

class Component(O):
  """
  All components of graph
  should extend this class
  """
  id = 0
  def __init__(self, component, **kwargs):
    O.__init__(self, **kwargs)
    self.id = Component.id
    self.component = component
    Component.id += 1

  def __hash__(self):
    if not self.id:
      return 0
    return hash(self.id)

  def __eq__(self, other):
    if not self.id or not other.id:
      return False
    return self.id == other.id

class Node(Component):
  """
  Node of a graph
  """
  def __init__(self, name, type, **kwargs):
    Component.__init__(self, "node", name=name, type=type, **kwargs)
    self.from_edges = []
    self.to_edges = []

  def add_edge(self, edge_id, type):
    if type == "from":
      self.from_edges.append(edge_id)
    else:
      self.to_edges.append(edge_id)

class Task(Node):
  """
  A Task node.
  """
  def __init__(self, name, container=None, **kwargs):
    Node.__init__(self, name, "task", container=container, **kwargs)

class Resource(Node):
  """
  A resource node
  """
  def __init__(self, name, container=None, **kwargs):
    Node.__init__(self, name, "resource", container=container, **kwargs)

class SoftGoal(Node):
  """
  A Soft goal node
  """
  def __init__(self, name, container=None, **kwargs):
    Node.__init__(self, name, "softgoal", container=container, **kwargs)

class HardGoal(Node):
  """
  A Hard Goal Node
  """
  def __init__(self, name, container=None, **kwargs):
    Node.__init__(self, name, "goal", container=container, **kwargs)

class Edge(Component):
  """
  Edge of a graph
  """
  def __init__(self, source, target, **kwargs):
    Component.__init__(self, "edge", **kwargs)
    self.source = source.id
    self.target = target.id

  @staticmethod
  def get_contribution_weight(key):
    if key == "make":
      return +3
    elif key == "help":
      return +2
    elif key == "someplus":
      return +1
    elif key == "someminus":
      return -1
    elif key == "hurt":
      return -2
    elif key == "break":
      return -3
    raise RuntimeError("Invalid contribution type %s"%key)

class Make(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "make"
    self.type = "contribution"

class Help(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "help"
    self.type = "contribution"

class SomePlus(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "someplus"
    self.type = "contribution"

class SomeMinus(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "someminus"
    self.type = "contribution"

class Hurt(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "hurt"
    self.type = "contribution"

class Break(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "break"
    self.type = "contribution"

class Conflict(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "conflict"
    self.type = "contribution"

class And(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "and"
    self.type = "decompositions"

class Or(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "or"
    self.type = "decompositions"

class Dep(Edge):
  """
  Make Contribution edge.
  """
  def __init__(self, source, target, **kwargs):
    Edge.__init__(self, source, target, **kwargs)
    self.value = "dependency"
    self.type = "dependency"

class Many:
  """
  An Array object
  """
  def __init__(self):
    self.all = []

  def __add__(self, other):
    self.all.append(other)
    return other

class Graph(O):
  """
  Graph object
  """
  def __init__(self, name, nodes, edges):
    O.__init__(self, name=name, nodes=nodes, edges=edges)
    self.update_nodes()

  def update_nodes(self):
    node_map = {}
    count = 0
    for node in self.nodes:
      node_map[node.id] = node
    for edge in self.edges:
      source = node_map.get(edge.source, None)
      target = node_map.get(edge.target, None)
      if source is None or target is None:
        count +=1;
        print(edge)
        continue
      node_map[edge.source].add_edge(edge.id, "to")
      node_map[edge.target].add_edge(edge.id, "from")
    if count: print(count)

  def get_edge(self, edge_id):
    for edge in self.edges:
      if edge.id == edge_id:
        return edge
    return None

  def get_node(self, node_id):
    for node in self.nodes:
      if node.id == node_id:
        return node
    return None

  def get_bases(self):
    """
    Get the base decisions of the graph
    :return:
    """
    nodes = []
    for node in self.nodes:
      if node.type in ['task', 'resource']:
        # We assume that decisions are either tasks or resources
        if not node.from_edges:
          nodes.append(node)
    return nodes

  def get_roots(self):
    """
    Get roots of the tree
    :return:
    """
    nodes = []
    for node in self.nodes:
      if not node.to_edges:
        nodes.append(node)
    return nodes

  def get_nodes_covered(self):
    return [node for node in self.get_nodes() if node.value]

  def get_nodes(self, node_type=None):
    """
    Get nodes of a certain type
    :param node_type:
    :return:
    """
    if isinstance(node_type, list):
      return [node for node in self.nodes if node.type in node_type]
    elif isinstance(node_type, str):
      return [node for node in self.nodes if node.type in [node_type]]
    else: return self.nodes

  @staticmethod
  def json(graph, file_path=None):
    if file_path:
      fl = open(file_path, 'w+')
      fl.write(graph.to_json())
      fl.close()
    else:
      print(graph.to_json())

  @staticmethod
  def read(file_path):
    with open(file_path) as json_file:
      data = decode(json.load(json_file))
      nodes, edges = [],[]
      for node_json in data["nodes"]:
        node_name = node_json["name"]
        container = node_json["container"]
        type = node_json["type"]
        node = Node(node_name, type, container=container)
        node.id = node_json["id"]
        nodes.append(node)
      for edge_json in data["edges"]:
        edge = Component("edge")
        edge.id = edge_json["id"]
        edge.value = edge_json["value"]
        edge.type = edge_json["type"]
        edge.source = edge_json["source"]
        edge.target = edge_json["target"]
        edges.append(edge)
      return Graph(name=data["name"], nodes=nodes, edges=edges)

  @staticmethod
  def from_dot(graph_name, path, resources=[], containers=[]):
    def trim(str):
      return str[1:-1]

    import pydot
    graph = pydot.graph_from_dot_file(path)
    graph_nodes = graph.get_node_list()
    nodes = []
    for graph_node in graph_nodes:
      name = trim(graph_node.get_name())
      if name in resources:
        node = Resource(name)
      elif name in containers:
        continue
      else:
        shape = graph_node.get_attributes()["shape"]
        if shape == "parallelogram":
          node = HardGoal(name)
        elif shape == "polygon":
          node = Task(name)
        elif shape == "box":
          node = SoftGoal(name)
        elif shape in ["circle", "ellipse"]:
          # containers
          continue
        else:
          print(name)
          continue
      node.id = node.name
      nodes.append(node)

    graph_edges = graph.get_edge_list()
    edges = []
    labels = set()
    for graph_edge in graph_edges:
      source = trim(graph_edge.get_source())
      target = trim(graph_edge.get_destination())
      if source in containers or target in containers:
        continue
      labels.add(graph_edge.get_attributes().get("label", None))
      label = graph_edge.get_attributes().get("label", None)
      if not label:
        value = "or"
        type = "decompositions"
      elif "make" in label.lower():
        value = "make"
        type = "contribution"
      elif "break" in label.lower():
        value = "break"
        type = "contribution"
      elif "help" in label.lower():
        value = "help"
        type = "contribution"
      elif "hurt" in label.lower():
        value = "hurt"
        type = "contribution"
      elif "some +" in label.lower():
        value = "someplus"
        type = "contribution"
      elif "some -" in label.lower():
        value = "someminus"
        type = "contribution"
      elif "d" in label.lower():
        value = "dependency"
        type = "dependency"
        source, target = target, source
      else:
        print(source, target, label)
        continue
      edge = Component("edge")
      edge.value = value
      edge.type = type
      edge.source = source
      edge.target = target
      edges.append(edge)
    return Graph(name=graph_name, nodes=nodes, edges=edges)

if __name__ == "__main__":
  resources = ["Service Resources", "Web Server", "Feedback Form Software", "Web Software",
                 "Strategic Blue Print", "Feedback", "Web Site Content", "Phone Library of Recorded Messages",
                 "Feedback1"]
  containers = ["CS", "Fund Development and Marketing", "Provincial government",
                "CS Technology Services", "CS Service", "Web Service", "Phone Service",
                "Counselling Management", "PHL Service", "Parents", "IT Department",
                "Web Task Force", "CS Web Services", "CS Phone Services", "PHL Phone Services",
                "PHL Web Services", "Counselling", "Kids and Youth"]
  graph = Graph.from_dot("CSServices", "pystar/CSServices.gv", resources, containers)
  Graph.json(graph, "pystar/json/%s.json"%graph.name)