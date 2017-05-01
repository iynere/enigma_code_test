# set encoding to utf-8:
# -*- coding: utf-8 -*-

# MODULES
import csv # csv parsing
import sys # command line arguments
import os # filesystem access
import string # string manipulation
import re # for replacing spaces & newlines

# GLOBALS
valid_file = False
file = None
path = ""
data = []
states = {}
months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06", "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}

# FUNCTIONS
def check(input):
  '''
  1) is it a .csv file?
  2) does that file exist at the provided path?
  '''
  while not input.endswith(".csv") or not os.path.isfile(input):
    if input.endswith("csv"):
      print "Sorry, that .csv file doesn't seem to exist!"
    else:
      print "Sorry, that doesn't seem to be a .csv file!"
    print "Please provide the relative or absolute path to a .csv file:"
    input = string.rstrip(raw_input())
  return input
        
def find_path(file):
  # for use by the write() function—makes sure files are outputted in the same directory as the source .csv file
  if re.search(r"/", file) == None:
    # this indicates that the user provided a relative path
    path = os.getcwd()
  else:
    # absolute path: create a slice excluding the actual name of the file to get the directory
    path = "/".join(file.split("/")[:-1]) 
  return path
  
def read(file):
  # read the .csv file & save it in the 'data' list object
  with open(file) as file_obj:
    reader = csv.DictReader(file_obj, delimiter=",")
    for line in reader:
      data.append(line)
  
def read_states(file):
  # read the states .csv file & store it in the 'states' dictionary object
  with open(file) as file_obj:
    reader = csv.DictReader(file_obj, delimiter=",")
    for line in reader:
      states[line["state_abbr"]] = line["state_name"]
  print(states)

def add_leading_zeros(date_arr):
  # some otherwise valid dates have single-digit strings for days/months 1-9
  return map(lambda date: date if len(date) > 1 else "0" + date, date_arr)

def format_valid(date):
  year = ""
  month = ""
  day = ""
  '''
  three cases here:
  1) e.g., September 30, 1977
  2) e.g., 2012-06-11 (this is the desired format)
  3) e.g., 10/26/1988
  '''
  if len(re.findall(r"-", date)) == 2:
    # 2) e.g., 2012-06-11 (this is the desired format)
    return date
  elif len(re.findall(r"/", date)) == 2:
    # 3) e.g., 10/26/1988
    date_nums = date.split("/")
    year = date_nums[2]
    month = date_nums[0]
    day = date_nums[1]
  else:
    # 1) e.g., September 30, 1977
    month = months[date.split(" ")[0]]
    date_nums = re.findall(r"\d+", date)
    day = date_nums[0]
    year = date_nums[1] 
  return "-".join(add_leading_zeros([year, month, day]))

def normalize(date):
  is_valid = True
  data = "" # will store the invalid/valid date
  if len(re.findall(r"\d", date)) < 5:
    # invalid dates have at most four numbers (e.g., 03/84 or February 2009)
    is_valid = False
    data = date
  else:
    data = format_valid(date)
  return {"is_valid": is_valid, "data": data}

def parse(data):
  # manipulate the data as instructed
  for line in data:
    # 1) strip all whitespace from the 'bio' field
    line["bio"] = re.sub(r"\s+", " ", line["bio"].strip())
    # 2) substitute full state names for two-letter state abbreviations
    line["state"] = states[line["state"]]
    # 3) reformat valid dates to align with ISO 8601; move invalid dates into a new adjacent 'start_date_description' field
    date = normalize(line["start_date"])
    if date["is_valid"]:
      line["start_date"] = date["data"]
      line["start_date_description"] = "not applicable; valid date"
    else:
      if len(re.findall(r"\d", line["start_date"])) > 0:
        line["start_date"] = "incomplete date"
      else:
        line["start_date"] = "invalid date"
      line["start_date_description"] = date["data"]
      
def write(file, data):
  output = path + "/" + file # complete path to output file
  with open(output, "wb") as output:
    '''
    since we're reading/writing with dictionaries, we need to specify field order (although .DictReader & .DictWriter do return 'ordered dictionaries' by default in Python 3.6+)
    '''
    fieldnames = ["name", "gender", "birthdate", "address", "city", "state", "zipcode", "email", "bio", "job", "start_date", "start_date_description"]
    writer = csv.DictWriter(output, fieldnames)
    writer.writeheader()
    for line in data:
      writer.writerow(line)
  print "Thank you! Your parsed .csv file is called '%s' and has been created in the same directory as your input file: " % file + path

# PROGRAM
# run this loop until we get a valid .csv file, one way or another
while not valid_file:
  # for now we only process one .csv file at a time so we can ignore any additional arguments passed to parser
  if len(sys.argv) > 1:
    # argv[1] because argv[0] is the python interpreter itself
    input = string.rstrip(sys.argv[1])
    # why rstrip() here? because when dragging a file into the terminal window to provide its path as a string, the terminal appends a space (on a Mac, at least)
  else: # i.e., user provided no input
    print "Welcome to r0se's .csv parser! Please provide the relative or absolute path to a .csv file:"
    input = string.rstrip(raw_input())
  file = check(input)
  # once check(input) finishes, we've found a .csv valid file, so we assign valid_file to True & thus move into the next part of our program
  valid_file = True
  
# if there is a valid file, we can run all of our reading, parsing, & writing functions
if valid_file:
  read_states("state_abbreviations.csv")
  read(file)
  parse(data)
  path = find_path(file)
  write("solution.csv", data)