# SPDX-FileCopyrightText: 2021 Aaron Dewes <aaron.dewes@protonmail.com>
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import re

# Helper functions
# Return a list of env vars in a string, supports both $NAM§ and ${NAME} format for the env var
# This can potentially be used to get around permissions, so this check is critical for security
# Please report any security vulnerabilities you find in this check to aaron.dewes@protonmail.com
def getEnvVars(string: str):
    string = str(string)
    envVars = re.findall(r'\$\{.*?\}', string)
    newEnvVars = re.findall(r"\$(?!{)([A-z1-9]+)", string)
    return [envVar[2:-1] for envVar in envVars] + newEnvVars


# Check if an array only contains values which are also in another array
def checkArrayContainsAllElements(array: list, otherArray: list):
    for element in array:
        if element not in otherArray:
            return False
    return True

# Parse a dotenv file
# Values can either be KEY=VALUE or KEY="VALUE" or KEY='VALUE'
# Returns all env vars as a dict
def parse_dotenv(file_path):
  envVars: dict = {}
  with open(file_path, 'r') as file:
    for line in file:
      line = line.strip()
      if line.startswith('#') or len(line) == 0:
        continue
      if '=' in line:
        key, value = line.split('=', 1)
        value = value.strip('"').strip("'")
        envVars[key] = value
      else:
        print("Error: Invalid line in {}: {}".format(file_path, line))
        print("Line should be in the format KEY=VALUE or KEY=\"VALUE\" or KEY='VALUE'")
        exit(1)
  return envVars

# Combines two objects
# If the key exists in both objects, the value of the second object is used
# If the key does not exist in the first object, the value from the second object is used
# If a key contains a list, the second object's list is appended to the first object's list
# If a key contains another object, these objects are combined
def combineObjects(obj1: dict, obj2: dict):
    for key in obj2:
        if key in obj1:
            if isinstance(obj1[key], list):
                obj1[key] = obj1[key] + obj2[key]
            elif isinstance(obj1[key], dict):
                obj1[key] = combineObjects(obj1[key], obj2[key])
            else:
                obj1[key] = obj2[key]
        else:
            obj1[key] = obj2[key]
    return obj1
