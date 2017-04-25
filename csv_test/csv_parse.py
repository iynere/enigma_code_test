# set encoding to utf-8 text format:
# -*- coding: utf-8 -*-

# modules
import csv # csv parsing
import sys # command line arguments
import os # filesystem access

valid_file = False 

# test

def check_if_is_csv(input):
  if not input.endswith('.csv'):
    while not input.endswith('.csv'):
      print "Sorry, that doesn't appear to be a valid .csv file!\nPlease provide the relative or absolute path to a .csv file:"
      input = raw_input()
  return input
    
# run this loop until we get a valid .csv file, one way or another
while not valid_file:
  if len(sys.argv) > 1:
    input = sys.argv[1]
    check_if_is_csv(input)
  else: # i.e., user provided no input
    print "Welcome to r0se's .csv parser! Please provide the relative or absolute path to a .csv file:"
    input = raw_input()
    check_if_is_csv(input)
  valid_file = True
    
  


# if input.
# = open(sys.argv[1], 'rt')

# 'r'—open for reading
# 't'—text mode
# (these are both default settings and not strictly required)

# why argv[1]? argv[0] is the script itself ('csv_parse.py'), as passed to the python interpreter ('python'); thus, the input to the script is actually the 2nd argument

# try:
#   reader = csv.reader(input)
#   # read the csv file & save it as a variable 'reader'
  
#   for row in reader:
#     print row
    
# finally:
#   input.close()
