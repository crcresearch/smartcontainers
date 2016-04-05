import parsingUtility
import os

class buildProcessor:

    def __init__(self):
        self.PU = parsingUtility.parsingUtility()
        self.backslashChar = '\\'

    def processDF(self, path):
        #Processes the dockerfile at path
        try:
            #Open the file for reading
            with open(path, 'r') as DF:
                #Initialize the cmd variable
                cmd = ''
                #Read the first line in the file
                line = DF.readline()
                #So long as there are lines to read in the file,
                #process each line.
                while line:
                    #Trim off the line feed character
                    line = line[:-1]
                    #If the line is empty, read the next line
                    if line == '':
                        line = DF.readline()
                    #If the line ends with a backslash, the command is continued
                    #across mulitple lines
                    elif line.endswith(self.backslashChar):
                        #Remove the backslash character, and then:
                        #Append the command fragment to the cmd variable
                        #This will occur repeatedly until the entire command
                        #is assembled
                        cmd += line.replace(self.backslashChar, '')
                        #Read teh next line
                        line = DF.readline()
                    #If the cmd variable is not empty and we have a line without
                    #a backslash at the end, then the multi-line command is complete.
                    elif cmd != '':
                        #Append the line to the cmd variable
                        cmd += line
                        #Send the completed command for parsing
                        self.PU.parseCommand(cmd)
                        #Re-initialize the cmd variable
                        cmd = ''
                        #Read the next line in the file
                        line = DF.readline()
                    #If the cmd variable is empty and we have a line without
                    #a backslash at the end, then we have a complete command to process.
                    elif cmd == '':
                        #Send the command off for parsing
                        self.PU.parseCommand(line)
                        #Read the next line in the file
                        line = DF.readline()
                    else:
                        #We should never be here!
                        print 'Problem processing DockerFile'
                return 0
        except Exception as e:
            return 1

    def processFO(self, fileobj):
        #Processes a fileobject passed in
        pass