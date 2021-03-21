# This library will be used for launching several aspects of PeckerMgr that may be required more than once.

import __main__ # Import the main script, which is called PeckerMgr.py.
import PySimpleGUI as framework # Load in the PySimpleGUI library. This is already loaded in the main script but I'll do this again so I don't have to constantly use __main__.framework.

# The reason why I'm importing the entirety of PeckerMgr, rather than just using "from __main__ import *" is because the variables won't be updated if they are on the main script. With the whole script importing, that won't be so much of an issue.

# Specify base values that may be used across multiple methods.
AllByteAllocations = ("KB", "MB", "GB", "TB", "PB", "EB") # Specify storage allocation units.

def CreateDocumentary(Pages, Title, TextHeight):
    """Create a documentary window which can consist of multiple pages.
    The first argument will be a list of strings which will be used as each page.
    The second argument will be the title of the window.
    The third argument will be the amount of rows of text each page can hold."""
    PageCount = 0 # The page count. This starts on 0 since Python usually indicates the first thing in things such as lists with 0 instead of 1.
    DocumentaryLayout = [ # Create the layout for the tour window.
        [framework.Column([
            # Previous colours: #e3e4e8
            [framework.Text(Pages[0], justification = "center", background_color = "#ffffff", text_color = "#060e26", key = "Page", size = (42, TextHeight))]
        ], background_color = "#ffffff", scrollable = True, vertical_scroll_only = True, size = (350, 450))],
        [framework.Button(PageCount + 1 != len(Pages) and "Next" or "Finish", key = "Progress"), framework.Button("Exit", key = "Exit")],
        [framework.Text("Page 1 of " + str(len(Pages)), key = "PageNumber", size = (15, 1), justification = "center")]
    ]

    DocumentaryWindow = framework.Window(Title, DocumentaryLayout, element_justification = "central", debugger_enabled = False) # Create the documentary window.
    while True: # Initiate the loop so user input isn't recorded only once.
        Events, UserInput = DocumentaryWindow.read() # Check for user input and such.
        if Events == framework.WIN_CLOSED or Events == "Exit": # If the exit button has been pressed, the break command will function.
            break # Stop the loop.
        elif Events == "Progress": # Progress is the key for the Next/Finish button.
            PageCount = PageCount + 1 # Increase the page count by one, essentially switching to the next page.
            if PageCount == len(Pages): # Check if the pages count is equal to how many pages have been assigned to the pages list. Since this if statement is after the pages count increases, the PagesCount variable should define a non-existent page.
                break
        DocumentaryWindow["Page"].update(Pages[PageCount])
        DocumentaryWindow["PageNumber"].update("Page " + str(PageCount + 1) + " of " + str(len(Pages))) # Update the page information.
        DocumentaryWindow["Progress"].update(PageCount + 1 != len(Pages) and "Next" or "Finish") # Change the text of the progress button, depending on what the progress is like.
    if Title == "Tour": __main__.ConfigurationManager.AppendToConfigurationFile("TourDone=True;", __main__.ConfigFile) # Write to the configuration file that the tour has completed, if the title is Tour.
    DocumentaryWindow.close() # Close the window if it hasn't been closed already.

def CreatePopup(Text, Title, TextHeight, CustomLayout = [], CreateButtons = True):
    """Create a popup. This function has been made to maintain consistency while simplifying usage.
    The first variable will be the text that the popup will display.
    The second variable will be the title of the popup.
    The third variable will define the text element's height.
    The other variables are optional and simply define additional aspects of the popup."""
    PopupLayout = [ # Create the popup layout!
                    [framework.Text(Text, justification = "center", size = (45, TextHeight))], # Create the text element. This will display the text that the user would like to display.
                    [framework.Button("OK", key = "OK")] # Create a placebo button element displaying "OK".
    ]
    if CreateButtons: # Check if CreateButtons is true.
        if CustomLayout != []: # Check if CustomLayout is not an empty list.
            PopupLayout[1] = CustomLayout # Swap out PopupLayout[2] for the custom layout.
        Popup = framework.Window(Title, layout = PopupLayout, element_justification = "center", debugger_enabled = False) # Create the final window with the popup layout!
        Events, UserInput = Popup.read(close = True) # Read the window, and then close it.
    else:
        PopupLayout.pop(1) # Remove the second entry of the PopupLayout list.
        return framework.Window(Title, layout = PopupLayout, element_justification = "center", debugger_enabled = False, finalize = True) # Return a new window with all of the desired elements and also finalized.
    return Events

def VerifyQEMULocation():
    "Proceed to verify QEMU's location and all of the applications for QEMU."
    if __main__.os.path.isdir(__main__.QEMULocation.Get()): # Check if the QEMULocation variable depicts an existent directory.
        Succeeded = True # This will be used later.
        for Arch in __main__.Machines: # Get all sub-lists in the Machines list.
            if not __main__.os.path.isfile(__main__.QEMULocation.Get() + "\qemu-system-" + Arch[1] + ".exe"): # Check if qemu-system- and the CPU architecture name exists.
                Succeeded = False
                return ["qemu-system-" + Arch[1] + " does not exist. Please re-install QEMU and change the location for QEMU if installed in a different location.", "Error"]
        if Succeeded: # If Succeeded is still True then tell the user that QEMU is completely fine.
            return ["""Success! QEMU is good to go and thus you can use PeckerMgr safely!""", "Success"]
    else:
        return ["The directory currently allocated as your QEMU location does not exist.", "Error"]

def PromptUserToFindDirectory(Text, DisallowClosing, TextHeight):
    """Prompt the user to locate a directory.
    The first variable will be the text that will appear on the screen.
    The second variable will depict whether the window can be closed or not without browsing for a directory.
    The third variable will define the text element's height."""
    Events = ""
    UserInput = ""
    while True: # Just in case the window is closed.
        filebrowsepopup = framework.Window(DisallowClosing and "Error" or "Locate", [ # This will prompt the user to locate their folder.
            [framework.Text(Text, key = "Info", justification = "center", size = (45, TextHeight))],
            [framework.FolderBrowse(key = "Browse"), framework.Button("Continue", key = "Continue")]
        ], enable_close_attempted_event = DisallowClosing, element_justification = "center", debugger_enabled = False)
        while True: # Initiate application loop, since WINDOW.read() is a one-time thing only.
            Events, UserInput = filebrowsepopup.read()
            if Events == "Continue":
                if DisallowClosing and (UserInput["Browse"] == "" or not __main__.os.path.isdir(UserInput["Browse"])):
                    filebrowsepopup["Info"].update("Please choose a valid directory, as not specifying anything will lead to future issues. You may always check the error booklet if you encounter any errors.")
                else:
                    break
            if Events == framework.WIN_CLOSED:
                break
        filebrowsepopup.close() # Close the window if it hasn't been closed.
        if not Events == framework.WIN_CLOSED and UserInput["Browse"] != "" and __main__.os.path.isdir(UserInput["Browse"]):
            break # Stop this loop as well.
        elif not DisallowClosing:
            break
    return Events, UserInput

def ReturnListingOfDirectory(Directory, AllowFiles):
    """Return the listings of a directory.
    The first variable depicts the directory to search.
    The second variable depicts whether files should be returned or not."""
    Listing = []
    assert(__main__.os.path.isdir(Directory)), CreatePopup("""Application search error. FF
    
""" + Directory, "Error", 4)
    for instance in __main__.os.listdir(Directory):
        if AllowFiles or __main__.os.path.isdir(Directory + "/" + instance):
            Listing.append(instance)
    return Listing

def ReturnBatchScriptOfConfig(ConfigFile):
    """This will return the QEMU batch script depicting the configuration being used."""
    #ConfigFile = ConfigFile.replace(":-:", ",model=").replace(" - ", " -device ") # Replace a few strings representing the model or device arguments for QEMU.
    BatchString = "" # Create a variable for the final batch string.
    ThingsToLookFor = {"MachineName=" : "-M ", "CPU=" : "-cpu ", "Video=" : "-device ", "Sound=" : "-device ", "Network=" : "-device ", "Accel=" : "-accel ", "Memory=" : "-m ", "hda=" : "-hda ", "hdb=" : "-hdb ", "hdc=" : "-hdc ", "hdd=" : "-hdd ", "odd=" : "-cdrom ", "fda=" : "-fda ", "fdb=" : "-fdb ", "BootOrder=" : "-boot order=", "DisplayType=" : "-display ", "Custom=" : ""} # Create a list of things to look for.
    
    # Before we look at all hardware listings, let's get the exact application that we have to launch...
    Assertion, ThingToAdd = __main__.ConfigurationManager.CheckForStatementInConfigurationFile("Arch=", ConfigFile, False, False, False) # Get the name of the CPU arch.
    assert(Assertion), CreatePopup("Please check the syntax of the configuration file of the VM in the VM directory called " + VMs + ". CC", "Error", 4)
    for CPUArchs in __main__.Machines: # Skim through all CPU architectures listed in the Machines list.
        if CPUArchs[0] == ThingToAdd: # Check if the first value of the CPUArchs sub-list in the Machines list is the same as the ThingToAdd value.
            BatchString = BatchString + '"' + __main__.os.path.normpath(__main__.QEMULocation.Get()) + "\qemu-system-" + CPUArchs[1] + '" -usb -L "' + __main__.os.path.normpath(__main__.QEMULocation.Get()) + '" ' # Append the application name to the BatchString value and then append the -usb argument, should the user specify usb devices.
            # REMINDER - THE -L FLAG IS TEMPORARY. ONCE QEMU CAN SEARCH FOR ROMS WITHOUT -L FLAG, REMOVE -L FLAG.
            break # End the loop, since the CPU architecture has already been discovered.
    
    # Now, let's specify all hardware being used!
    for HardwareUsed in ThingsToLookFor: # Skim through the ThingsToLookFor list.
        Assertion, ExactHardware = __main__.ConfigurationManager.CheckForStatementInConfigurationFile(HardwareUsed, ConfigFile, "Ignore", True, False) # Look for the hardware used in the configuration file.
        assert(Assertion), CreatePopup("Please check the syntax of the configuration file of your machine. CC", "Error", 2)
        if HardwareUsed == "MachineName=": # Check if the hardware being looked for is the machine name.
            MachinesDirectory = __main__.os.path.normpath(__main__.MachinesFolder + "/" + ThingToAdd) # Specify the CPU architecture directory in the Machines folder inside the directory that PeckerMgr is located in.
            assert(__main__.os.path.isdir(MachinesDirectory)), CreatePopup("The CPU architecture directory called " + MachinesDirectory + " is missing from the Machines directory.", "Error", 4)
            for MachineOfCPUArch in ReturnListingOfDirectory(MachinesDirectory, False): # Check for all of the machines for the CPU architecture.
                if MachineOfCPUArch == ExactHardware: # Check if the ExactHardware specification is the exact same as the MachineOfCPUArch value.
                    MachineConfigFile = __main__.os.path.normpath(MachinesDirectory + "/" + MachineOfCPUArch + "/config.cfg") # Specify the machine's configuration file.
                    assert(MachineConfigFile), CreatePopup("The machine " + MachineOfCPUArch + " is missing its config.cfg.", "Error", 3)
                    Assertion2, MachineNameForQEMU = __main__.ConfigurationManager.CheckForStatementInConfigurationFile("Machine=", MachineConfigFile, "Ignore", False, False) # Look for the hardware used in the configuration file.
                    assert(Assertion2), CreatePopup("Please check the syntax of the configuration file. EE", "Error", 2)
                    BatchString = BatchString + " " + ThingsToLookFor[HardwareUsed] + MachineNameForQEMU # Append the machine to use to the BatchString value.
                    break # End the loop.
        else:
            ExactHardware = ExactHardware.replace(":-:", ",model=").replace(" - ", " -device ") # Replace a few strings representing the model or device arguments for QEMU.
            if HardwareUsed == "Memory=": # Check if HardwareUsed depicts memory allocation.
                if ExactHardware[-2:] in AllByteAllocations: ExactHardware = ExactHardware[0:-1] # Check if the last two characters of ExactHardware is present in AllByteAllocations. If so, remove the last character in ExactHardware to use QEMU's storage allocation unit, otherwise QEMU may error.
            if HardwareUsed in ("hda=", "hdb=", "hdc=", "hdd=", "odd=", "fda=", "fdb="): # Check if the HardwareUsed variable is a drive specification.
                ExactHardware = '"' + ExactHardware + '"' # Add quotes, just in the case there are directories with spaces in it.
            elif HardwareUsed == "Network=" and not ExactHardware in ("", "None"): # Check if the HardwareUsed variable specifies the network card and the ExactHardware specification is not empty or is specified as None.
                ExactHardware = ExactHardware + ",netdev=Ethernet -netdev user,id=Ethernet"
            elif HardwareUsed == "CPU=" and not ExactHardware in ("", "None"): # Check if the HardwareUsed variable specifies the CPU and the Exacthardware specification is not empty or is specified as None.
                ExactHardware = '"' + ExactHardware + '"' # Surround the ExactHardware specification by quotes to prevent errors with QEMU if the CPU specification contains spaces in it.
            BatchString = BatchString + " " + ThingsToLookFor[HardwareUsed] + ExactHardware if not ExactHardware in ("None", '"None"', "", '""') else BatchString # Append the specification to the BatchString value if the ExactHardware specification is not None.
    return BatchString # Return the final code that will initiate QEMU with all proper arguments.

def AutomaticWriteToConfigFilesOfAllMachines(CPUArch, WhatToAppend):
    "This wouldn't be used generally - it's just for me to quickly append things to a machine's configuration file."
    MachinePath = __main__.os.path.normpath(__main__.MachinesFolder + "/" + CPUArch) # Bundle the MachinesFolder variable and the CPUArch string together to build the machine path.
    assert(__main__.os.path.isdir(__main__.MachinesFolder) and __main__.os.path.isdir(MachinePath)), CreatePopup("""Application search error. FF
    
""" + MachinePath, "Error", 4) # This will return False if the MachinesFolder or MachinePath aren't existent directories, thus triggering the assert.
    for MachinesFound in ReturnListingOfDirectory(MachinePath, False): # Skim through the machine path.
        __main__.ConfigurationManager.AppendToConfigurationFile(WhatToAppend, __main__.os.path.normpath(MachinePath + "/" + MachinesFound + "/config.cfg")) # Append the necessary information.

def CheckDiskSize(DiskSize):
    """Verify the disk size and see whether it is valid or not.
    The one necessary argument consists of the exact string to verify, depicting the disk size."""
    AllQEMUByteAllocations = {"B"} # Specify storage allocation units that QEMU uses.
    DiskSize = DiskSize.upper() # Make all characters upper-case so case-sensitivity won't be a must.
    StorageUnit = ""

    # Add the first character of all storage units mentioned in AllByteAllocations.
    for Unit in AllByteAllocations:
        AllQEMUByteAllocations.add(Unit[0])

    try:
        # Cut off byte indicators in DiskSize to prevent issues with int conversion, should the disk size be specified correctly
        if DiskSize[-2:] not in AllByteAllocations and DiskSize[-1] in AllQEMUByteAllocations: # Check if the last two characters of DiskSize is not present in AllByteAllocations but the last character is present in AllQEMUByteAllocations.
            StorageUnit = DiskSize[-1]; DiskSize = DiskSize[0:-1]
        elif DiskSize[-2:] in AllByteAllocations: # Check if the last two characters of DiskSize is present in AllByteAllocations, signifying a unit of storage differentiating from normal bytes.
            StorageUnit = DiskSize[-2]; DiskSize = DiskSize[0:-2]
        else: raise ValueError

        # Initiate conversion to see if exception ValueError will be raised, then return DiskSize with QEMU-like storage unit.
        int(DiskSize)
        return ["Success", DiskSize + StorageUnit]
    except ValueError:
        return ["Error", "Please check that your disk size consists of a number and then a suffix defining whether it should be in bytes, kilobytes, megabytes, gigabytes, terabytes, petabytes or exabytes."]

def CreateDiskWizard(DefaultDiskLocation = ""):
    """Launch the create virtual disk wizard.
    The only argument specified, which is optional, will select the default disk location."""
    if __main__.os.path.isfile(__main__.QEMULocation.Get() + "\qemu-img.exe"): # Check if qemu-img.exe exists in QEMU's location.
        DefaultText = "Current desired location: "
        if DefaultDiskLocation == "": DefaultText = DefaultText + "none"
        else: DefaultText = DefaultText + __main__.os.path.normpath(DefaultDiskLocation)
        CVDLayout = [ # Create the layout for the create virtual disk wizard.
                        [framework.Text("Create a new virtual disk", font = ("Segoe UI Light", 20))], # Title of the application
                        [framework.Text("""You can create a virtual disk with the following options listed down below. All supported disk formats will also be listed down below. All disk formats except for raw (.img) support dynamic disks, which are essentially virtual disks that start off as very, very small and eventually take up more space the more that is being written to it. 
                                
Keep in mind that raw virtual disks use the .img file format and VPC (Virtual PC) virtual disks use the legacy .vhd file format.

Although QEMU uses single-letter units for storage allocation, you may use the true abbreviated units while creating a disk image with PeckerMgr. For example, you may type in 25GB as the disk size. If you still feel comfortable using single-lettered units, feel free to do so. All possible storage allocation units: B, KB, GB, TB, PB, EB.""", justification = "center", size = (60, 14))], # Description about the create virtual disk wizard.
                        [framework.Text("Virtual disk format:")], # Sub-title for the virtual disk format.
                        [framework.Listbox(values = ["Raw", "QCOW", "QCOW2", "VDI", "VMDK", "VPC", "VHDX"], size = (60, 7), key = "DiskFormat", background_color = "#ffffff", text_color = "#060e26")], # All available disk formats to choose from.
                        [framework.Text("Disk size:"), framework.Input(key = "DiskSize", background_color = "#ffffff", text_color = "#060e26")], # Allow the user to choose the respective disk size.
                        [framework.Text("Disk name:"), framework.Input(key = "DiskName", background_color = "#ffffff", text_color = "#060e26")], # Allow the user to choose the name for their disk.
                        [framework.Text(DefaultText, size = (75, 2), key = "DiskLocationText", justification = "center", font = ("Segoe UI", 8))], # Notify the user about the current location of their disk drive.
                        [framework.FolderBrowse(button_text = "Browse for location", key = "DiskLocation", enable_events = True)], # Allow the user to choose the location for their virtual disk.
                        [framework.Button("OK", key = "OK"), framework.Button("Cancel", key = "Cancel")] # Finally, create the last few options for the user.
        ]
        CVD = framework.Window("Create virtual disk wizard", layout = CVDLayout, element_justification = "center", debugger_enabled = False) # Finally, create the window!
        while True: # Create a loop since user input may be registered more than once.
            Events2, UserInput2 = CVD.read() # Read the user input and show the window.
            if Events2 in (framework.WIN_CLOSED, "Cancel"):
                break # End the loop.
            elif Events2 == "DiskLocation" and UserInput2["DiskLocation"] != "": # Check if the browse button has been selected and if the user input is not empty.
                CVD["DiskLocationText"].update("Current desired location: " + __main__.os.path.normpath(UserInput2["DiskLocation"])) # Update the current desired location text. This also uses os.path.normpath() because the desired location uses normal slashes for whatever reason.
            elif Events2 == "OK": # Check if the user would like to proceed.
                if UserInput2["DiskLocation"] == "" and DefaultDiskLocation == "": # Check if the disk location is empty.
                    CreatePopup("Please select a location for your disk.", "Error", 1)
                elif UserInput2["DiskSize"] == "": # Check if the disk size is empty.
                    CreatePopup("Please choose a size for your disk.", "Error", 1)
                elif UserInput2["DiskName"] == "": # Check if the disk name is empty.
                    CreatePopup("Please choose a name for your disk.", "Error", 1)
                elif UserInput2["DiskFormat"] == []: # Check if the disk format has not been selected.
                    CreatePopup("Please choose a disk format.", "Error", 1)
                else:
                    StorageUnit = CheckDiskSize(UserInput2["DiskSize"])
                    if StorageUnit[0] == "Error": # Check if the first entry of the StorageUnit array is "Error".
                        CreatePopup(StorageUnit[1], "Error", 3)
                    else:
                        Allowed = True # Reset our Allowed variable, now that we will be looking through the DiskName value.
                        for Char in UserInput2["DiskName"]:
                            Allowed = False if Char in ("\\", "/", ":", "*", "?", '"', "<", ">", "|") else Allowed # Check if the DiskName value contains forbidden characters.
                            if not Allowed:
                                break # Stop the loop so we don't have to continue looking around.
                        if not Allowed:
                            CreatePopup("""The following characters are forbidden for the disk name: \, /, :, *, ?, ", <, >, |""", "Error", 2)
                        else:
                            # Create a few variables to make this look easier on our eyes.
                            DiskLocationToUse = UserInput2["DiskLocation"] if UserInput2["DiskLocation"] != "" else DefaultDiskLocation # Specify the final disk location, containing either the contents of UserInput2["DiskLocation"] if it is not an empty string or the contents of DefaultDiskLocation.
                            FileFormat = UserInput2["DiskFormat"][0] == "VPC" and "vhd" or UserInput2["DiskFormat"][0] == "Raw" and "img" or UserInput2["DiskFormat"][0].lower()
                            FileAndDirectory = __main__.os.path.normpath('"' + DiskLocationToUse + "/" + UserInput2["DiskName"] + "." + FileFormat + '"')

                            if __main__.os.path.isfile(FileAndDirectory[1:-1]): # Check if FileAndDirectory with its enclosing quotes removed does not determine any file on the system.
                                CreatePopup("This file already exists. Please choose another name.", "Error", 2)
                            elif not __main__.os.path.isdir(DiskLocationToUse): # Check if the directory was deleted for some weird reason.
                                CreatePopup("The current selected directory no longer exists.", "Error", 1)
                            else: # If we reach this point, we can safely create our drive!
                                __main__.subprocess.Popen(__main__.QEMULocation.Get() + "\qemu-img.exe create -f " + UserInput2["DiskFormat"][0].lower() + " " + FileAndDirectory + " " + StorageUnit[1]) # Launch qemu-img with the correct parameters!
                                break # End the loop.
        CVD.close() # Close the window just in case it hasn't already.
    else:
        CreatePopup("qemu-img does not exist in your QEMU location.", "Error", 1)

def TellUserToSelectVM():
    __main__.PeckerMgr.hide() # Hide PeckerMgr to prevent inconsistencies from occurring.
    CreatePopup("Please select a virtual machine.", "Error", 1) # Create the necessary popup.
    __main__.PeckerMgr.un_hide() # Show PeckerMgr again.