#!/usr/local/bin/python3

# evofinder : stdin input generator using evolutionary algorithms
#             Authors: Josiah Bruner <jsbruner@umich.edu>
#                      Callum Hutchinson <callumhutchinson@googlemail.com>
#
#             Usage: python3 evofinder.py <input python file> <target_line_num>
import ast
import astor
import os
import random
import re
import string
import sys
import math

POPULATION_SIZE = 50
INITIAL_STRING_MAX_SIZE = 50 
EVOLUTION_GENERATIONS = 10
input_dictionary = {}
target_location_id = None
execeptional_inputs = {}

def instrument_given_attr(node, attr, depth_id, target_line):
  global target_location_id

  to_add = []
  for i, child in enumerate(getattr(node, attr)):
    if isinstance(child,ast.Expr):
      if hasattr(child, 'lineno'):
        #print("Line: " + str(child.lineno))
        if child.lineno == target_line:
          target_location_id = str(depth_id) + "_" + str(i)

      # Add print node
      print_node = ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()),
           args=[
                  ast.Str("___UNIQUE_ID___: " + str(depth_id) + "_" + str(i)) 
               ],
           keywords=[
            
            ],
      ))
      to_add.append((i, print_node))

    else:
      instrument_node(child, depth_id + "_" + str(i), target_line)

  for i, thing in enumerate(to_add):
    getattr(node, attr).insert(thing[0] + i, thing[1])


def instrument_node(node, depth_id, target_line):
  #print(astor.dump(node))

  if hasattr(node, 'body'):
    instrument_given_attr(node, 'body', depth_id + "_" + '0', target_line)
  if hasattr(node, 'orelse'):
    instrument_given_attr(node, 'orelse', depth_id + "_" + '1', target_line)


# Reads python program from input, converts to AST, and adds instrumentation.
# Returns: AST with instrumentation
def instrument_file(input_loc, target_line):
  tree = None  
  tree = ast.parse(open(input_loc, 'r').read())
  instrument_node(tree, "", target_line)

  new_source = astor.to_source(tree)
  print(new_source)
  return tree 


# Helper functions
def write_ast(ast, file_name):
  new_source = astor.to_source(ast)
  out_file = open(file_name, "w")
  out_file.write(new_source)


def write_input(input_data, file_name):
  out_file = open(file_name, "w")
  out_file.write(input_data)


def exe_and_capture(python_file, input_file, input_data):
  global execeptional_inputs
  os.system("python3 " + python_file + " < " + input_file + " > tmp.bin 2> error.bin")
  output = open('tmp.bin', 'r').read()
  error_out = open('error.bin', 'r').read()

  if "Error:" in error_out:
    execeptional_inputs[input_data] = error_out

  os.remove('tmp.bin')
  os.remove('error.bin')
  return output


def collect_location_ids(exe_output_string):
  locations = []
  reg_exp_str = "___UNIQUE_ID___: (?:_\d+)+"
  p = re.compile(reg_exp_str)
  res = p.findall(exe_output_string)
  for val in res:
    locations.append(val.replace("___UNIQUE_ID___: ", ""))
  return locations

# Tries to find the closest we got to the target location.
# This is not trivial. Locations are represented using a specific encoding.
# _A_B_C_D... where each of A,B,C,D... represents the position of the child
# taken at each level. So a string with 4 values would have a depth of 4, etc.
#
# "Closeness" is defined as how many values match until they no longer do  
def find_closest_id(ids, target_id):
  target_vals = target_id.split("_")
  #print("Target: " + str(target_vals))
  best_score = -1
  best_id = None

  for val in ids:
    vals = val.split("_")
    #print("Val: " + str(vals))
    score = 0
    for i, idx in enumerate(vals):
      if idx == target_vals[i]:
        score += 1
      else:
        break

    if score > best_score:
      best_score = score
      best_id = val

  return (best_id, best_score)


def cleanup(files): # files should be an array of strings
  for a_file in files:
    try:
        os.remove(a_file)
    except OSError:
        pass    


# Evalutes the fitness of some input_data string. To do this:
#
#   1. Write out the instrumented AST to a file.
#   2. Write the input_data to a file.
#   3. Run the new python file and pipe the input data to stdin.
#   4. Capture output of execution.
#   5. Collect all of the unique location IDs printed.
#   6. Find the "closest" unique location and return distance as fitness
#   7. Cleanup files
#
def get_fitness(input_data, ast, target_id):
  global target_location_id
  write_ast(ast, "instrumented_program.py")
  write_input(input_data, "inter_input_for_program.bin")
  result = exe_and_capture("instrumented_program.py", 
                           "inter_input_for_program.bin", input_data)
  visited_locations = collect_location_ids(result)
  #print(visited_locations)
  closest_id_tuple = find_closest_id(visited_locations, target_location_id) # Returns (id, dist)
  
  cleanup(["instrumented_program.py", "inter_input_for_program.bin"])
  #print(closest_id_tuple[1])
  return closest_id_tuple[1] 

def mutate_ind(input_data, mutate_percentage=0):
  #store the mutated inputs
  global input_dictonary
  # list of possible mutations on the input data
  operations = ['insert','delete','swap']

  # cast string to a list for manipulation
  #print("Input data: " + input_data)
  input_list = list(input_data)
  #print(input_data)
  # choose which operation to apply. dont delete if 
  # string is empty or length 1
  while(True):
    operation_choice = random.choice(operations)
    if(not((len(input_list)==0 or len(input_list)==1) 
      and operation_choice=='delete' or operation_choice=='swap')):
      break

  # if mutate_percentage is not given we just apply
  # the operation to one element
  if mutate_percentage==0:
    num_iter = 1
  else:
    num_iter = int(math.ceil(len(input_list)*mutate_percentage))

  #apply the operation the given amount of times  
  for iter in range(num_iter):

    if operation_choice=='insert':
      #choose an insertion position randomly
      if len(input_list) != 0:
        insert_position = random.choice(list(range(0,len(input_list))))
      else:
        insert_position = 0
      #generate a list of all ascii characters
      ascii_chars = [chr(i) for i in range(0,127)]
      #choose a random ascii character to insert
      ascii_choice = random.choice(list(range(0,len(ascii_chars))))
      #insert the character
      input_list.insert(insert_position,ascii_chars[ascii_choice])

    elif operation_choice=='delete':
      #choose a delete position randomly
      delete_position = random.choice(list(range(0,len(input_list))))
      del input_list[delete_position]

    elif operation_choice=='swap':
      #choose positions to swap randomly
      first_position = random.choice(list(range(0,len(input_list))))
      second_position = random.choice(list(range(0,len(input_list))))
      #save first position in temporary variable
      temp_storage = input_list[first_position]
      #swap positions
      input_list[first_position] = input_list[second_position]
      input_list[second_position] = temp_storage

  #create a string from the mutated list
  input_data = ''.join(str(char) for char in input_list)

  #add to dictionary of words
  input_dictionary[input_data] = True

  return input_data

def mutate_population(input_data,mutate_percentage=0):
  for ind in input_data:
    ind = mutate_ind(ind)

  return input_data

# Takes as input a population of stuff, and the fitnesses assoicated with each
# Generates a new population of the same size, but using tournament selection.
def tournament_selection(population, fitnesses):
  #print(str(population))
  #print(str(fitnesses))
  #print(len(fitnesses))
  #print(len(population))
  new_pop = []
  for i in range(0, len(population)):
    # Pick two individuals to compete
    index_1 = random.randint(0, len(population) - 1)
    index_2 = random.randint(0, len(population) - 1)

    if fitnesses[index_1] > fitnesses[index_2]:
      new_pop.append(population[index_1])
    else:
      new_pop.append(population[index_2])

  return new_pop


# Takes the instrumented ast and evolves input strings.
# Initially starts with a population of random inputs
def start_evolution(ast, target_line, baseline_file_list=[]):
  global POPULATION_SIZE
  global INITIAL_STRING_MAX_SIZE
  global EVOLUTION_GENERATIONS

  input_data = []
  best_input = ""
  best_fitness = 0

  # go through each file in the list
  for files in baseline_file_list:
    try:
      file = open(files)
    except:
      print("File load error")
      break
    
    # add the baseline inputs to the input data
    if len(input_data)<POPULATION_SIZE:
      print("Added file contents: " + str(files))
      input_data.append(file.read())
    else:
      break

    file.close()
    # dont open the other files if our population is
    # already full 
    if(len(input_data)==POPULATION_SIZE):
      break

  # if the input files didn't have enough input we
  # generate random strings
  while len(input_data) < POPULATION_SIZE:
    string_len = random.randint(0, INITIAL_STRING_MAX_SIZE)
    input_str = ''.join(random.choice(string.printable) for x in range(string_len))
    input_data.append(input_str)


  for i in range(EVOLUTION_GENERATIONS):
    population_fitnesses = get_pop_fitnesses(input_data, ast, target_line)

    # Check to see if we have a new best individual
    for i, fitness in enumerate(population_fitnesses):
      if fitness > best_fitness:
        best_input = input_data[i]    
        best_fitness = fitness

    # Get new population using tournament selection
    input_data = tournament_selection(input_data, population_fitnesses)

    # Mutate population
    input_data = mutate_population(input_data)

  print("Best fitness value was: " + str(best_fitness))
  return best_input


def get_pop_fitnesses(input_data, ast, target_line):
  fitnesses = []
  for ind in input_data:
    fitnesses.append(get_fitness(ind, ast, target_line))

  return fitnesses


def main():
  global execeptional_inputs

  if len(sys.argv) < 3:
    print("Usage: python3 evofinder.py <input python file> <target_line_num> <example_file_1> <example_file_2> ...")
    exit(1)

  input_file_loc = sys.argv[1]
  target_line_num = sys.argv[2]
  example_files = []
  if len(sys.argv) > 3:
    for idx in range(3, len(sys.argv)):
      example_files.append(sys.argv[idx])

  instrument_ast = instrument_file(input_file_loc, int(target_line_num))
  if instrument_ast == None:
    print("Instrumentation Failed.")
    exit(2)
  elif target_location_id == None:
    print("Couldn't find target line number. Aborting....")
    exit(3)
   
  result = start_evolution(instrument_ast, target_line_num, example_files)

  print("Best result dumped to evolved_input.bin")
  out_file = open("evolved_input.bin", "w")
  out_file.write(result)

  if len(execeptional_inputs) > 0:
    print("Found crashing input(s):")
    for key, val in execeptional_inputs.items():
      print("Input: " + key)

  print("Exiting...")

main()
