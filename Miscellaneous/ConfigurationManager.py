# Import libraries necessary for this custom library that I have written.

import PySimpleGUI as framework # The framework for all of the app development. This is essentially multiple libraries such as TKinter put all into one library, with more simplicity at the same time.
import Miscellaneous.LaunchAspectsOfPeckerMgr as LaunchAspectsOfPeckerMgr # This will be used for launching certain parts of PeckerMgr that may be ran more than once.
import __main__ # Import the main script, which will be used to reach out for a few things.

DefaultEnclosedVariables = [] # Create the base enclosed variables list.

def OverrideEnclosedVariables(String, AdditionalEnclosedVariables = []):
    """Override variables enclosed in curly brackets {} with their true specifications.
    The first variable depicts the string to modify.
    The second variable specifies additional values to override. These should be organised in lists."""
    AllEnclosedVariables = DefaultEnclosedVariables + AdditionalEnclosedVariables # Add on the additional enclosed variables to the default enclosed variables list.
    for Options in AllEnclosedVariables: # Go through all of the specified options in the DefaultEnclosedVariables list.
        String = String.replace(Options[0], Options[1]) # Override any enclosed variables with whatever has been found in the AllEnclosedVariables list.
    return String # Return the final string.

def OverrideValues(String, AdditionalValues = []):
    """Override variables enclosed in curly brackets {} with their true specifications.
    The first variable depicts the string to modify.
    The second variable specifies additional values to override. These should be organised in lists."""
    AllEnclosedVariables = DefaultEnclosedVariables + AdditionalValues # Add on the additional enclosed variables to the default enclosed variables list.
    TemporaryString = "" # Create a temporary string that can be used as a placeholder for modified string values.
    ValueToStartFrom = 0 # Create a starting-point value.
    CurrentPlace = 0 # Create a value that will be used for the for loop at the second phase of value detection.
    while True: # Initiate the main loop!
        FoundOption = False # Create a new bool variable called FoundOption, which will have a default value of False.
        for Char in range(ValueToStartFrom, len(String)): # First phase of value detection!
            TemporaryString = TemporaryString + String[Char] # Add onto the TemporaryString variable.
            for Options in AllEnclosedVariables: # Go through all options in the AllEnclosedVariables list.
                TemporaryStringEntry = TemporaryString.find(Options[1], ValueToStartFrom, len(String) - 1) # Check if Options[1] is present in the TemporaryString value from the ValueToStartFrom entry point. The value returned from this function will be added onto the TemporaryStringEntry variable. If no instance of Options[1] was found, this function will return -1.
                if TemporaryStringEntry != -1: # Check if an instance of Options[1] has been found.
                    CurrentPlace = Char + 1 # Set the CurrentPlace value to Char, then increment it.
                    ValueToStartFrom = TemporaryStringEntry # Set the ValueToStartFrom value to be the same as TemporaryStringEntry.
                    FoundOption = True # Set FoundOption to true.
                    break # End the for loop.
            if FoundOption == True: break # If FoundOption is true, end the foor loop. This will end the first phase of value detection.
        if FoundOption: # Check if FoundOption is true.
            TemporaryString = String[ValueToStartFrom : CurrentPlace] # Set TemporaryString to hold a substring in String, with an entry point of ValueToStartFrom and an ending point of CurrentPlace.
            for Char in range(CurrentPlace, len(String)): # Second phase of value detection!
                TemporaryString = TemporaryString + String[Char] # Add onto the TemporaryString value.
                StringInOption = False # Create a new bool value called StringInOption, then set it to False.
                if Char != len(String) - 1: # Check if Char does not equal the length of the string decremented.
                    for Options in AllEnclosedVariables: # Go through all possible options in the AllEnclosedVariables list.
                        if TemporaryString in Options[1]: # Check if TemporaryString is found in Options[1]
                            StringInOption = True # Set StringInOption to True.
                IsDone = False # Create a new bool variable called IsDone, with a default value of False.
                if not StringInOption: # Check if StringInOption is False.
                    while True: # Create another while loop.
                        TemporaryString = TemporaryString[0:-1] # Set TemporaryString to hold all of its current data except the last character.
                        for Options in AllEnclosedVariables: # Go through all possible options in the AllEnclosedVariables list.
                            if Options[1] == TemporaryString: # Check if Options[1] is the same as TemporaryString.
                                String = String[:ValueToStartFrom] + Options[0] + String[Char:] # Set the string to contain its data up to ValueToStartFrom, then concatenate Options[0], then concatenate the data of the string unmodified starting from Char.
                                ValueToStartFrom = ValueToStartFrom + len(Options[0]) # Set ValueToStartFrom to be itself plus the length of Options[0].
                                IsDone = True # Set IsDone to True.
                                break # End the for loop.
                        if IsDone: # Check if IsDone is True.
                            break # End the while loop.
                        Char = Char - 1 # Take away 1 from char, so once the string is modified it doesn't disclude necessary characters.
                    break # End the for loop. This will end the second phase of value detection.
        TemporaryString = "" # Reset the TemporaryString variable.
        if not FoundOption: break # If FoundOption is False, end the continuously-going while loop. This will end the entire process of value detection.
    return String # Return the final string.

def CheckForValidCharacter(String, SemiColonPlacement, Character = ";"):
    "Ensure that semi-colons can still be used without marking the end of a variable."
    if String[SemiColonPlacement] != Character: return False # Check if the character of String at position SemiColonPlacement is a semi-colon.
    if SemiColonPlacement != 0 and String[SemiColonPlacement - 1] == "\\": return False # Check if SemiColonPlacement is not 0 and the character of String at position SemiColonPlacement take away 1 is black slash.
    return True

def AppendToConfigurationFile(AppendInfo, ConfigFileToUse):
    """Append information to a configuration file.
    The first variable for this function depicts the information you'd like to append to a configuration file.
    The second variable is the exact configuration file to use. PLEASE ENSURE THAT THE CONFIGRATION FILE YOU'RE LOOKING FOR DOES EXIST!
    This function will handle all of the changes depending on what is already there on the configuration file."""
    AppendInfo = AppendInfo.rstrip() # Trim off all of the whitespaces at the end of AppendInfo.
    if not CheckForValidCharacter(AppendInfo, len(AppendInfo) - 1): AppendInfo += ";" # If the final character of AppendInfo is not a semi-colon, add a semi-colon onto it.
    CurrentConfig = open(ConfigFileToUse).read()
    if AppendInfo != "":
        AppendInfo = AppendInfo.replace(__main__.os.path.normpath(__main__.os.getcwd()), __main__.os.path.normpath("{CurrentWorkingDirectory}/")) # Replace a few bits of information in the AppendInfo variable with safer-to-use variants.
    # Check if the variable already exists but the value is different:
    Variable = ""
    for i in AppendInfo:
        Variable = Variable + i # Append to Variable string.
        if i == "=": # The equals sign, which will mark the end of the variable.
            break
    OriginalVariable = Variable
    integer = CurrentConfig.find(Variable, 0, len(CurrentConfig))
    if integer != -1: # If the variable is present, then the find function will return someting that isn't -1.
        ValueOfVariable = ""
        HasDoneFine = False
        for i in range(integer + len(Variable), len(CurrentConfig)):
            ValueOfVariable = ValueOfVariable + CurrentConfig[i]
            if CheckForValidCharacter(CurrentConfig, i): # This defines the end of the configuration variable, much like if you were coding where the semicolon would define the end of a statement.
                SyntaxCorrect = True
                HasDoneFine = True
                break
        assert(HasDoneFine), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. FF", "Error", 2) # If HasDoneFine is still False, then there will be an assertion.
        Variable = Variable + ValueOfVariable
        open(ConfigFileToUse, "w").write(CurrentConfig.replace(Variable, AppendInfo))
        NewValueOfVariable = ""
        for Char in range(len(ValueOfVariable)):
            if not CheckForValidCharacter(ValueOfVariable, Char):
                NewValueOfVariable += ValueOfVariable[Char]
        return OverrideEnclosedVariables(NewValueOfVariable) # If one was to require the value for variable assigning without having to use the CheckForStatementInConfigurationFile function.
    elif CurrentConfig.find(AppendInfo, 0, len(CurrentConfig)) == -1:
        if CurrentConfig == "":
            open(ConfigFileToUse, "w").write(AppendInfo)
        else:
            open(ConfigFileToUse, "a").write("""
""" + AppendInfo)
        return OverrideEnclosedVariables(AppendInfo) # If one was to require the value for variable assigning without having to use the CheckForStatementInConfigurationFile function.

def CheckForStatementInConfigurationFile(WhatToSearchFor, ConfigFileToUse, AllowCommas, AllowNothingFound, ReturnTrueValue):
    """Search for a certain variable located inside of a configuration file. 
    The first variable for this function depicts what you'd like to search for in a configuration file. 
    The second variable is the exact configuration file to use. PLEASE ENSURE THAT THE CONFIGRATION FILE YOU'RE LOOKING FOR DOES EXIST!
    The third variable is there if you would like to split values of a variable into several values with commas in between.
    If the third variable is set to "Ignore" then all commas will just be left alone.
    The forth variable is to depict whether there will be an exception for no result in the configuration file.
    The fifth variable will depict whether all enclosed variables should be overrided to represent their true values."""
    WhatToSearchFor = WhatToSearchFor.rstrip() # Trim off all of the whitespaces at the end of WhatToSearchFor.
    if WhatToSearchFor[len(WhatToSearchFor) - 1] != "=": WhatToSearchFor += "="  # If the final character of WhatToSearchFor is not an equal sign, add an equal sign onto it.
    SyntaxCorrect = AllowNothingFound
    if AllowCommas == True:
        WordBeingFound = []
    else:
        WordBeingFound = ""
    Pointer = 0
    if __main__.os.path.isfile(ConfigFileToUse): # Check if the configuration file is present in the configuration directory and that the configuration directory is present.
        ConfigText = open(ConfigFileToUse).read() # Read the configuration file
        integer = ConfigText.find(WhatToSearchFor, 0, len(ConfigText)) # Check if what to search for is present.
        if integer != -1: # -1 = not present, any other integer = present
            SyntaxCorrect = False
            for i in range(integer + len(WhatToSearchFor), len(ConfigText)):
                if CheckForValidCharacter(ConfigText, i): # This defines the end of the configuration variable, much like if you were coding where the semicolon would define the end of a statement.
                    SyntaxCorrect = True
                    break
                elif CheckForValidCharacter(ConfigText, i, Character = ","):
                    assert(AllowCommas), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. F1", "Error", 2) # If allowcommas is false and there has been a comma detected, this will initiate an assert.
                    if AllowCommas == True:
                        if ReturnTrueValue: WordBeingFound[Pointer] = OverrideEnclosedVariables(WordBeingFound[Pointer]) # Replace a few bits of information with their true values.
                        WordBeingFound[Pointer] = WordBeingFound[Pointer].replace("\;", ";").replace("\,", ",")
                        Pointer = Pointer + 1
                    elif AllowCommas == "Ignore":
                        WordBeingFound = WordBeingFound + ConfigText[i]
                elif AllowCommas == True: # Add onto the WordBeingFound variable.
                    try:
                        WordBeingFound[Pointer] = WordBeingFound[Pointer] + ConfigText[i] 
                    except Exception:
                        WordBeingFound.append(ConfigText[i])
                else:
                    WordBeingFound = WordBeingFound + ConfigText[i]
            if type(WordBeingFound) == str:
                WordBeingFound = WordBeingFound.replace("\;", ";").replace("\,", ",")
    if AllowCommas != True and ReturnTrueValue: WordBeingFound = OverrideEnclosedVariables(WordBeingFound) # Replace a few bits of information with their true values.
    return SyntaxCorrect, WordBeingFound # Finally, return the final information!

def QuickCheck(WhatToSearchFor, ConfigFileToUse):
    """Quickly check for a variable in a configuration file.
    PLEASE NOTE THAT THIS IS ONLY RECOMMENDED FOR SIMPLE CHECKS SUCH AS IF YOU WERE TO FIND A VARIABLE HOLDING BOOL DATA.
    OTHERWISE, PLEASE USE ConfigurationManager.CheckForStatementInConfigurationFile().

    The first variable depicts what variable you'll want to search for.
    The second variable is the exact configuration file to use. PLEASE ENSURE THAT THE CONFIGRATION FILE YOU'RE LOOKING FOR DOES EXIST!
    """
    ConfigText = open(ConfigFileToUse).read()
    return ConfigText.find(WhatToSearchFor, 0, len(ConfigText))