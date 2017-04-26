# set encoding to utf-8 text format:
# -*- coding: utf-8 -*-

# modules
import csv # csv parsing
import sys # command line arguments
import os # filesystem access
import string # string manipulation

valid_file = False
file = None

'''
csv_check checks two things:
1) is it a .csv file? &
2) does the file exist at the provided path?
for now we will assume that if the file exists & ends with .csv, it is actually a .csv file
'''

def csv_check(input):
  while not input.endswith(".csv") or not os.path.isfile(input):
    if input.endswith("csv"):
      print "Sorry, that .csv file doesn't seem to exist!"
    else:
      print "Sorry, that doesn't seem to be a .csv file!"
    print "Please provide the relative or absolute path to a .csv file:"
    input = string.rstrip(raw_input())
  return input  
  
def csv_parse(file): # 'file' here will be a .csv file opened in memory
  reader = csv.reader(file)
  for row in reader:
    print(" ".join(row))
    
# run this loop until we get a valid .csv file, one way or another
while not valid_file:
  # for now we will assume that we only ever want to process one .csv file at a time & will ignore any additional arguments passed to csv_parse
  if len(sys.argv) > 1:
    input = string.rstrip(sys.argv[1])
    # why rstrip() here? because when dragging a file into the terminal window to provide its path as a string, the terminal seems to append a space (on a Mac, at least)
    file = csv_check(input)
  else: # i.e., user provided no input
    print "Welcome to r0se's .csv parser! Please provide the relative or absolute path to a .csv file:"
    input = string.rstrip(raw_input())
    file = csv_check(input)
  valid_file = True
  if __name__ == "__main__": # if function is being executed directly rather than being imported
    with open(file, "rb") as file_obj:
      csv_parse(file_obj)
  
# now we can use our actual parsing function
# how to do template strings: print 'this is the file: %s' % file
