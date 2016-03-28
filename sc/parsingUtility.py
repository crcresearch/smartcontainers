

class parsingUtility:

    def __init__(self):
        self.data = {}

    def parseCommand(self,cmdString):
        #Directs the command processing to the appropriate function,
        #based on the type of command received.

        #Get the command type from the cmdString
        thisCommand = self.getCommand(cmdString)
        #Call the appropriate routine based on the command type
        if thisCommand == 'FROM':
            self.parseFROM(cmdString)
        elif thisCommand == 'MAINTAINER':
            self.parseMAINTAINER(cmdString)
        elif thisCommand == 'RUN':
            self.parseRUN(cmdString)
        elif thisCommand == 'CMD':
            self.parseCMD(cmdString)
        elif thisCommand == 'LABEL':
            self.parseLABEL(cmdString)
        elif thisCommand == 'EXPOSE':
            self.parseEXPOSE(cmdString)
        elif thisCommand == 'ENV':
            self.parseENV(cmdString)
        elif thisCommand == 'ADD':
            self.parseADD(cmdString)
        elif thisCommand == 'COPY':
            self.parseCOPY(cmdString)
        elif thisCommand == 'ENTRYPOINT':
            self.parseENTRYPOINT(cmdString)
        elif thisCommand == 'VOLUME':
            self.parseVOLUME(cmdString)
        elif thisCommand == 'USER':
            self.parseUSER(cmdString)
        elif thisCommand == 'WORKDIR':
            self.parseWORKDIR(cmdString)
        elif thisCommand == 'ARG':
            self.parseARG(cmdString)
        elif thisCommand == 'ONBUILD':
            self.parseONBUILD(cmdString)
        elif thisCommand == 'STOPSIGNAL':
            self.parseSTOPSIGNAL(cmdString)
        else:
            print "Error parsing command"

    def getCommand(self, cmdString):
        #returns command from cmdString, with the assumption
        #that the command is always the first word in the string
        return cmdString.split()[0]

    def get_command_data(self, command):
        """Obtains the second part of the command string.

        Args:
            command (str): The command string.

        Returns: The second part of the command string.

        """
        return command.split(" ", 1)[1]

    def parseFROM(self, cmdFROM):
        pass

    def parseMAINTAINER(self, cmdMAINTAINER):
        pass

    def parseRUN(self, cmdRUN):
        pass

    def parseCMD(self,cmdCMD):
        pass

    def parseLABEL(self, cmdLABEL):
        pass

    def parseEXPOSE(self, cmdEXPOSE):
        pass

    def parseENV(self, cmdENV):
        pass

    def parseADD(self, cmdADD):
        pass

    def parseCOPY(self,cmdCOPY):
        pass

    def parseENTRYPOINT(self, cmdENTRYPOINT):
        pass

    def parseVOLUME(self, cmdVOLUME):
        pass

    def parseUSER(self, cmdUSER):
        pass

    def parseWORKDIR(self, cmdWORKDIR):
        pass

    def parseARG(self, cmdARG):
        pass

    def parseONBUILD(self, cmdONBUILD):
        pass

    def parseSTOPSIGNAL(self, cmdSTOPSIGNAL):
        pass


