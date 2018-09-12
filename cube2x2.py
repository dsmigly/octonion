import random

class State(object):
  """docstring for State"""
  def __init__(self, perm, label):
    self.perm = perm
    self.label = label

  def __mul__(self, other):
    new_label = (self.label + other.label) % 2
    if other.label == 0:
      return State(concatenate_permutations(self.perm, other.perm), new_label)
    else:
      return State(concatenate_permutations(other.perm, self.perm), new_label)

  def __rmul__(self, other):
    return __mul__(other, self)


  def __str__(self):
    return str((self.perm, self.label))

  def __hash__(self):
    return hash(self.perm) + hash(self.label)

  def __eq__(self, other):
    return self.perm == other.perm and self.label == other.label

    

def single_move(state, move_name):
  new_state = list(state)
  if move_name == 'u' or move_name == 'U':
    new_state[0], new_state[1], new_state[2], new_state[3] = new_state[1], new_state[2], new_state[3], new_state[0]
  elif move_name == 'r' or move_name == 'R':
    new_state[1], new_state[2], new_state[6], new_state[5] = new_state[5], new_state[1], new_state[2], new_state[6]
  elif move_name == 'f' or move_name == 'F':
    new_state[0], new_state[1], new_state[5], new_state[4] = new_state[4], new_state[0], new_state[1], new_state[5]
  return tuple(new_state)


def concatenate_permutations(perm1, perm2):
  return tuple([perm1[index] for index in perm2])


def generate_loop(generators, generation_limit = 30):
  elements = set([g for g in generators])

  for generation_index in xrange(generation_limit):
    elements_list = list(elements)
    generation_start_count = len(elements)
    elements_next_gen = set(elements_list)
    for generator in generators: # only from generators in each step
    # for generator in elements_list:
      new_elements = []
      new_elements.extend([element * generator for element in elements]) # right multiply
      new_elements.extend([generator * element for element in elements]) # left multiply
      for el in new_elements:
        elements_next_gen.add(el)
    elements = elements_next_gen
    print "Generation #" + repr(generation_index), ": ", len(elements)
    generation_end_count = len(elements)
    if generation_end_count == generation_start_count:
      break
  return elements

initial_perm = tuple(range(8))

f = State(single_move(initial_perm, 'f'), 1)
r = State(single_move(initial_perm, 'r'), 0)
u = State(single_move(initial_perm, 'u'), 0)

elements = generate_loop([f, r, u])
print len(elements)

elements = list(elements)

for random_loop_index in range(10):
  random_indices = [random.randrange(len(elements)) for index in xrange(3)]
  a, b, c = [elements[index] for index in random_indices]

  print "random_indices: ", random_indices

  print "Commutativity:", a * b == b * a
  print "Associativity:", (a * b) * c == a * (b * c)
  print "Moufang properties:", c * (a * (c * b)) == (((c * a) * c) * b)
  print

# right multiply only by generators: 480 elements. Consistent with 120 * 4, (Group generated by U, R) * (4 states of F)
# left and right multiply by generators: 10080 elements. 2 labels * 7! permutations
# right multiply by any element: 10080
