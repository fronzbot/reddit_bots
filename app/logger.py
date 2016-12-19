'''
Custom logging class (really dumb)
''' 
import os
import time
 
class Logger(object):
  def __init__(self, filename="log.txt", newFile=False):
    self.filename = filename
    if os.path.isfile(self.filename) and newFile:
      os.remove(self.filename)
      
    self.write("Starting on "+time.strftime("%Y-%m-%d %H:%M:%S"))
    
  def write(self, message, debug=False):
    self.log = open(self.filename, "a")
    self.log.write(message)
    self.log.write('\n')
    self.log.close()
    if debug:
      print(message)