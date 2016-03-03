from __future__ import print_function, division
__author__ = 'george'
import sys,os
sys.path.append(os.path.abspath("."))
sys.dont_write_bytecode = True
import random
from jmoo_objective import *
from jmoo_decision import *
from jmoo_problem import jmoo_problem

t =  1
f = -1

def coin_toss():
  return random.choice([t, f])

def percent(num, den):
  if den==0:
    return 0
  return round(num*100/den, 2)

def shuffle(lst):
  if not lst:
    return []
  random.shuffle(lst)
  return lst

def eval_roots(model):
  return model.evaluate_score()

def eval_goals(model):
  return model.evaluate_type(node_type="goal", is_percent=model.is_percent)

def eval_softgoals(model):
  return model.evaluate_type(node_type="softgoal", is_percent=model.is_percent)

def eval_all_goals(model):
  return model.evaluate_type(node_type=["softgoal", "goal"], is_percent=model.is_percent)

def eval_coverage(model):
  covered = len(model.get_tree().get_nodes_covered())
  if model.is_percent:
    return percent(covered, len(model.get_tree().get_nodes()))
  else:
    return len(model.get_tree().get_nodes_covered())

class RE(jmoo_problem):
  def __init__(self, tree, obj_funcs=None, **settings):
    jmoo_problem.__init__(self)
    if not obj_funcs:
      obj_funcs = [eval_softgoals, eval_goals, eval_coverage]
    self.name = tree.name
    self.obj_funcs = obj_funcs
    self._tree = tree
    self.roots = self._tree.get_roots()
    self.bases = self._tree.get_bases()
    obj_names = [func.__name__.split("_")[1] for func in obj_funcs]
    dec_names = [base.id for base in self.bases]
    self.decisions = [jmoo_decision(dec_names[i], f, t) for i in range(len(dec_names))]
    self.objectives = [jmoo_objective(obj_names[i], False) for i in range(len(obj_names))]
    self.chain = set()
    self.is_percent = settings.get("obj_is_percent", True)

  def get_tree(self):
    return self._tree

  def generateInput(prob):
    point_map = {}
    for node in prob.bases:
      point_map[node.id] = random.choice([t, f])
    return point_map.values()

  def clear_nodes(self):
    for node in self._tree.nodes:
      node.value = None
      node.is_random = False

  def reset_nodes(self, values):
    self.clear_nodes()
    for node, value in zip(self.bases, values):
      node.value = value

  def evaluate_score(self, initial_node_map):
    self.clear_nodes()
    for key in initial_node_map.keys():
      node = self._tree.get_node(key)
      node.value = initial_node_map[key]
    return self.score()

  def evaluate_type(self, node_type, is_percent=False):
    count = 0
    nodes = self._tree.get_nodes(node_type=node_type)
    for node in nodes:
      self.chain = set()
      self.eval(node)
      if node.value > 0:
        count += 1
    if is_percent:
      return percent(count, len(nodes))
    else:
      return count

  def evaluate(self, input=None):
    if input:
      rounded_input = [t if i > 0 else f for i in input]
      self.reset_nodes(rounded_input)
      for _ in range(len(self._tree.nodes)//2):
        self.chain = set()
        self.eval(random.choice(self._tree.nodes))
      return [obj_func(self) for obj_func in self.obj_funcs]
    else:
      assert False , "Input Not Provided"


  def eval_node(self, node):
    self.chain=set()
    self.eval(node)


  def score(self):
    """
    Back Propagation
    Count how many root nodes are covered
    :return: root nodes covered
    """
    count = 0
    for node in self.roots:
      self.chain = set()
      self.eval(node)
      if node.value > 0:
        count += 1
    return count

  def dep_and_rest(self, edges):
    """
    Split edges into dependencies and the rest
    :param edges:
    :return:
    """
    deps = []
    rest = []
    for edge_id in edges:
      edge = self._tree.get_edge(edge_id)
      if edge.type == "dependency":
        deps.append(edge)
      else:
        rest.append(edge)
    return shuffle(deps), shuffle(rest)

  @staticmethod
  def random_node_val(node):
    """
    Return a random value for a node
    :param node:
    :return:
    """
    if node.type in ["goal", "softgoal"]:
      return t
    return coin_toss()

  def eval(self, node):
    if not (node.value is None):
      return node.value

    if node.id in self.chain:
      node.value = RE.random_node_val(node)
      node.is_random = True
      return
    self.chain.add(node.id)
    if not node.from_edges:
      node.value = RE.random_node_val(node)
      node.is_random = True
      return
    else:
      # First check for dependencies from the edges and evaluate it
      # Ask @jenhork about it

      deps, rest= self.dep_and_rest(node.from_edges)
      # if rest and rest[0].type == "contribution":
      #   exit()
      # Check if all dependencies are satisfied
      dep_nodes = [self._tree.get_node(dep.source) for dep in deps]


      if not rest:
        node.value = self.eval_and(dep_nodes)
        return

      # Evaluate the rest. We assume the rest are of same kind
      edge_type = rest[0].type
      if edge_type == "decompositions":
        status = self.eval_and(dep_nodes)
        if status < 0:
          node.value = status
          return
        kids = [self._tree.get_node(edge.source) for edge in rest]
        if rest[0].value == "and":
          # Evaluate all children
          status = self.eval_and(kids)
        elif rest[0].value == "or":
          status = self.eval_or(kids)
      elif edge_type == "contribution":
        status = self.eval_contribs(rest, deps)
      else:
        raise Exception("Unexpected edge type %s"%edge_type)
      node.value = status
      return

  def eval_and(self, nodes):
    """
    Evaluate all the nodes in the tree
    :param nodes: Nodes to be evaluated
    :return: status
    """
    status = t
    for node in nodes:
      if status <= 0: break
      self.eval(node)
      status = node.value
    return status

  def eval_or(self, nodes):
    """
    Evaluate all the nodes in the tree
    till a node is evaluated as true
    :param nodes: Nodes to be evaluated
    :return: status
    """
    for node in nodes:
      self.eval(node)
      status = node.value
      if status > 0:
        return status
    return f

  def eval_contribs(self, edges, dependencies=None):
    """
    Evaluate cumulative of contributions
    based on the weight.
    :param edges: Nodes to be evaluated
    :return: status
    """
    kids = []
    for edge in edges:
      if edge.type != "contribution":
        continue
      node = self._tree.get_node(edge.source)
      self.eval(node)
      kids += [RE.soft_goal_val(node.value, edge.value)]
    if dependencies:
      for dep in dependencies:
        dep_node = self._tree.get_node(dep.source)
        self.eval(dep_node)
        kids += [RE.soft_goal_val(dep_node.value, "make")]
    return random.choice(kids)

  @staticmethod
  def soft_goal_val(kid, edge):
    """
    Check out src/img/prop_rules.png
    :param kid:
    :param edge:
    :return:
    """
    if edge in ["someplus", "someminus"]:
      return random.choice([t/2, f/2])
    if kid == t:
      if edge == "make"   : return t
      if edge == "help"   : return t/2
      if edge == "hurt"   : return f/2
      if edge == "break"  : return f
    elif kid == t/2:
      if edge == "make"   : return t/2
      if edge == "help"   : return t/2
      if edge == "hurt"   : return f/2
      if edge == "break"  : return f/2
    elif kid == f/2:
      if edge == "make"   : return f/2
      if edge == "help"   : return f/2
      if edge == "hurt"   : return t/2
      if edge == "break"  : return t/2
    elif kid == f:
      if edge == "make"   : return f
      if edge == "help"   : return f/2
      if edge == "hurt"   : return t/2
      if edge == "break"  : return t/2

    raise RuntimeError("Either node value %s or edge %s is unknown"%(kid, edge))

  def evalConstraints(prob,input = None):
    return False