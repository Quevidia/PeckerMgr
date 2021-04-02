# Import all of our libraries :)
import PySimpleGUI as framework # The framework for all of the app development. This is essentially multiple libraries such as TKinter put all into one library, with more simplicity at the same time.
import os # The OS library will be used for communications between this Python application and the operating system, such as looking for files in a certain directory.
import shutil # An alternative to the OS library for certain tasks.
import subprocess # This can be used to open up applications on the system. Will be necessary for later!

# Now, import custom libraries that I have written myself.
import Miscellaneous.ConfigurationManager as ConfigurationManager # This will be used for interacting with configuration files made specifically for PeckerMgr.
import Miscellaneous.LaunchAspectsOfPeckerMgr as LaunchAspectsOfPeckerMgr # This will be used for launching certain parts of PeckerMgr that may be ran more than once.

# Create a custom method which will be used for a few variables. This can help with updating the ConfigurationManager.DefaultEnclosedVariables list.
class CreateVariable:
    def __init__(self, Name, Variable = None):
        self.Name = Name; self.Value = Variable

    def WhatToDo(self):
        for Options in ConfigurationManager.DefaultEnclosedVariables:
            if Options[0] == "{" + self.Name + "}":
                Options[1] = self.Value

    def Set(self, Variable):
        self.Value = Variable
        self.WhatToDo()

    def Get(self):
        return self.Value

# Set the default icon for all windows.
assert(os.path.isfile(os.path.normpath(os.getcwd() + "/Icons/PeckerMgr1.ico"))), LaunchAspectsOfPeckerMgr.CreatePopup("PeckerMgr icon is not present. Please check your icons folder.", "Error", 2)
framework.SetOptions(icon = os.path.normpath(os.getcwd() + "/Icons/PeckerMgr1.ico"))

# Create a few introductary variables necessary for this application.
Config = os.environ.get("LOCALAPPDATA") + "\PeckerMgr" # Configuration directory
ConfigFile = Config + "\config.cfg" # Configuration file
VMsLocation = CreateVariable("VMsLocation", "")
QEMULocation = CreateVariable("QEMULocation", "")
ThemeColour = "LightGrey6" # Default theme colour
ConfigurationManager.DefaultEnclosedVariables.extend([["{CurrentWorkingDirectory}", os.path.normpath(os.path.normpath(os.getcwd()))], ["{VMsLocation}", QEMULocation.Get()], ["{QEMULocation}", VMsLocation.Get()]]) # Also modify the DefaultEnclosedVariables list.

OldConfigFileLocation = os.getcwd() + "\config\config.cfg"
if os.path.isfile(OldConfigFileLocation): # Check if the config directory and config.cfg is present in PeckerMgr's directory.
    Events = LaunchAspectsOfPeckerMgr.CreatePopup("A configuration file has been found in the directory that PeckerMgr is located at. Would you like to move it over to your local appdata? Upon selecting yes, will both the configuration file and the configuration directory will be deleted.", "Reminder", 4, CustomLayout = [framework.Button("Yes", key = "Yes"), framework.Button("No")]) # Remind the user that there is a configuration file in the old PeckerMgr configuration location.
    if Events == "Yes": # Check if the user selected yes.
        if not os.path.isdir(Config): # Check if the necessary directory for the configuration file does not exist.
            os.mkdir(Config) # Create the necessary directory located at Config.
        Events2 = "" # Specify Events2 to be used in a few lines.
        if os.path.isfile(ConfigFile): # Check if ConfigFile already exists.
            Events2 = LaunchAspectsOfPeckerMgr.CreatePopup("A configuration file already exists in %LOCALAPPDATA%\PeckerMgr. Would you like to continue this operation?", "Warning", 3, CustomLayout = [framework.Button("Yes"), framework.Button("No", key = "No")])
        if Events2 == "" or Events2 != "No": # Check if Events2 is an empty string or if it is no.
            shutil.copyfile(OldConfigFileLocation, ConfigFile) # Copy over OldConfigFileLocation to ConfigFile.
            shutil.rmtree(os.getcwd() + "\config") # Delete the config directory located in PeckerMgr's directory.

# Create a few lists depicting pages for the CreateDocumentary method in LaunchAspectsOfPeckerMgr.
TourInformation = [[ # Define a list that will contain the tour pages.
"""Hello! Welcome to PeckerMgr (made by Quevidia) - a basic application for those using QEMU on the go or just want to get a head start with it! PeckerMgr provides simplicity throughout every bit of it! Create virtual machines, configure them with a user interface and launch them with little research required!

With PeckerMgr, you only have to go through a few simple steps in order to simply set it up. Set up your configuration, locate QEMU if it is not in Program Files, and choose your default virtual machines location, and you are good to go!

Click next if you would like to proceed with this tour (RECOMMENDED IF YOU ARE USING PECKERMGR FOR THE FIRST TIME), otherwise you can simply press exit.""",
"""Setting up a virtual machine for the first time with PeckerMgr? You only need a good few seconds just to get a basic machine up and going!

Before setting up a virtual machine, you will most likely want to get your virtual storage mediums ready. What's that? Well, let's say you want to set up a virtual machine that requires a CD drive or a hard drive. Well, there are virtual files for these coming in different file formats. CDs/DVDs/what-not tend to come in a file format called ISO, which can be easily mounted on Windows 10. Although ISO images cannot be written to in QEMU, you can in fact write to them using third-party applications, such as UltraISO. ISO images are perfect replicas of CDs/DVDs/what-not and contain all features such as the file format and the boot sector - which is necessary for a bootable disc!

You'll also want to prepare your virtual hard drive file. There are so many file formats for these files - such as QCOW2 (QEMU's own file format), VHDX (Microsoft's own file format), VMDK (VMware's own file format), etc. All three of these file formats are actually supported by QEMU, alongside many more. You can create a virtual hard drive by heading to Tools > Create virtual disk, which will allow you to create a virtual hard drive. Good options include QCOW2 and VHDX, where QCOW2 is made by QEMU developers themselves while VHDX is pretty useful and can even be mounted on Windows!""",
"""Okay, let's say that you are ready and you would now like to create your virtual machine. On the home page for PeckerMgr, you should see an option called "New". You could also head to File > New. Clicking on these buttons will take you to the new virtual machine wizard, which contains two important steps - a name and the CPU architecture. 

The name can be whatever you want, however you may be confused with the CPU architecture. Well, for starters - a CPU, or otherwise a central processing unit, is the electronic device responsible for all instructions executed, making up your entire computer - you could otherwise say that it is the brain of your computer. But hold up, what is a CPU architecture? Well, in simple words, a CPU architecture is a set of rules and instructions for a specific CPU model that provide functionality. CPU architectures include x86 (what the majority of our computers use today - used for CPUs made by companies like Intel and AMD), ARM (the architecture used for more mobile devices most of the time such as your phone), PowerPC (an old CPU architecture that Apple used decades ago for their computers) and much more. You'll most likely want to go with x86, since it is pretty widespread and it is what many operating systems stick to.

Hold up, you may also see "32/64" or "_32/_64" on a CPU architecture. What on earth is that? Well, these are in fact just extensions for a CPU architecture. All CPU architectures without the "64" specification are 32-bit, which means that the CPU architecture uses 32-bit registers, which were pretty complex for the past but are now more obsolete compared to 64-bit CPU architectures which computers would primarily use nowadays, which in return use 64-bit registers. Ever see an operating system labeled "64-bit"? Well, you'll most likely want to be going with the 64-bit CPU architecture for said operating system - rather than the 32-bit CPU architecture listed on PeckerMgr.

There are also a few other extensions to CPU architectures such as "el" for the MIPS32/MIPS64 CPU architectures. Although they don't differ a whole lot from the main respective CPU architectures, they can come with additional functionality.""",
"""Okay, let's say that you have finally created a new virtual machine. Then what do you do? Well you'll most certainly not want to stick with the default options - which sometimes won't even work anyway, because some CPU architectures emulated by QEMU don't have a default machine! What you want to do is select your virtual machine, then click on either the Configure button or head to File > Configure. You should be taken to the configure virtual machine wizard afterwards.

You'll see all of these options and tabs, such as your exact machine and the CPU to use. Well, there aren't a whole load of options you'll need to supply. A summary of each tab will be listed on the next page.""",
"""Machine tab
 -Machine: The exact board you would like to emulate. For example - this won't actually be mentioned, but it could be something like the board of a Dell Optiplex.
 -CPU: As described earlier, this is what is responsible for all of the computer instructions being handled out. You'll want to research each CPU for its capabilites and time period for the perfect one to choose.
 -Memory: Basically memory allocation. This is what holds temporary data that your computer will need to read and write to every now and then. You could say that you can use a hard drive instead, but hard drives are slow and memory management must be fast in order for consistency to not be a problem.
 -Acceleration: This is the exact emulation/virtualisation one would use for the CPU. The default option is TCG, which can handle practically every CPU architecture - but it's rather slow and may not be up to user standards. For x86 and x86_64, there are two additional options - HAXM and WHPX. WHPX utilises the Windows Hypervisor Platform, which is pretty quick. For those with the proper BIOS extensions enabled, with HAX tools installed and also use an Intel CPU, you may also use HAXM - which is also pretty fast.
 
Peripherals tab
 -Video card: This is responsible for video output and will also come with certain capabilities. You'll want to research the video cards as well if you'd like to look deeper into them.
 -Sound card: This is basically for sound output - nothing else. Again, you'll want to research these so you can find the right one for your operating system's time period.
 -Network card: If you would like connectivity within the internet and other sorts of networking, you can emulate a network card. Yet again, research this so you can fight the right card.

Non-removable mediums tab
 -This is basically for all of your virtual hard drive files. Make sure to specify a file that QEMU can read and write to.
 -If you didn't create a virtual hard drive image, you may do so with the create virtual disk option, which will launch the create virtual disk manager.
 -Make sure to not specify both the 3rd hard drive and an image for the optical disc drive (or CD/DVD/what-not drive) on the next page as this will cause a conflict and QEMU will not launch properly.

Removable mediums tab
 -You may specify both an ISO image for the optical disc drive and two virtual floppy images for the two floppy drives.
 -Since these were not mentioned before, floppy drives were pretty old drives that are now considered obsolete. However, if you need to use them for an old operating system, feel free to do so. Virtual floppy disk images usually use the .img file format, however there are a few others such as .vfd.
 
Miscellaneous tab
 -Boot order: Specify the drives and peripherals you would like to boot from. The first specification will be the first peripheral to boot from, while the last specification will be the last peripheral to boot from.
 -Display type: This will change how QEMU is represented. The default option is GTK, which represents a GNOME-like user interface (for specification, GNOME is a Linux desktop environment).
 -Custom parameters: This is mostly for advanced users who have used QEMU before and would like to make a few changes to their virtual machine. It is best not to touch this if you are new to QEMU.""",
"""Now, QEMU itself. If you launch your virtual machine, you will notice a new window appearing. This is actually QEMU itself - which will display your operating system and what-not.

Although it is mostly simplistic to get a hang of, there may be a few additional features a new user will need to learn as well. For example, QEMU will usually have multiple display types. There will always be a display type called compat_monitor0, which will be used to send over additional user input to QEMU. We'll get to that to a second. If a display adapter is available, there will be another tab with the name of your display adapter as well. The default option is usually VGA, so the display tab will be called "VGA" in that case.

To switch between tabs, it is mostly common sense - that is if you are using GTK windowing. If you head over to View and then select "Show tabs", you will see all of the available display types. Most of the time you should also notice serial0 and parallel0, but you'll most likely not need that - especially if you're new to QEMU. If you're using SDL, however, it may not be apparent as to how you'd want to open up a new window. What you'll want to do is press CTRL+ALT+X, where X is a number between 1 and 9 on your keyboard. A typical setup will most likely have CTRL+ALT+1 for your primary display, CTRL+ALT+2 for compat-monitor0, CTRL+ALT+3 for serial0 and CTRL+ALT+4 for parallel0, however this is not always the case.

There are a few additional shortcuts on QEMU as well, which could come in handy. For example, CTRL+ALT+F will display QEMU in fullscreen, and initiating CTRL+ALT+F again will display QEMU in a window. You may also press CTRL+ALT+G, which will grab/ungrab user input - or otherwise your cursor.""",
"""On some occasions, you'll find yourself wondering around questions like "How do I screenshot my primary display?" or "How do I eject something in my optical drive and input another disc?" Well, that's where compat-monitor0 comes in! compat-monitor0 has a bunch of a commands which can be very useful. Simply typing "help" will give you a few commands that you can use, however not all of them will be mentioned. Down below, I will mention a few commands used for screen dumping and interacting with removable mediums (optical discs and floppy disks).

For starters, if you would like to screenshot the primary display, you can simply type "screendump Directory\To\FileName.PPM", which will dump a .PPM image to your desired location. Keep in mind that you will need a certain third-party application in order to at least modify these images - such as paint.net with the extension responsible for handling ppm images.

If you would like to interact with removable mediums, here's two commands for it:
 -eject [-f (OPTIONAL)] DRIVETOUSE => Eject the currently disc inside the specified drive. The -f flag is optional, which will force the disc out of the drive. This must go in between eject and DRIVETOUSE.
 -change DRIVETOUSE Location\To\Disk.fileformat => Insert/replace the disc inside the specified drive with the disc you have located.

If you are not sure about the exact disc to use, you may also specify "info block". This will list all available drives and their current statuses, alongside what is currently inserted.""",
"""There are a few other perks with PeckerMgr that you may go through. If you have an unwanted virtual machine laying around, you may remove it and its files by selecting either "Remove" or heading to File > Remove - assuming that you have your virtual machine currently selected. This will prompt you again, and if you selected yes, then kaboom goes your virtual machine!

You can also change a few settings with PeckerMgr, by heading to Edit > Preferences. There are only a few options in there, however they amy come in handy, For example, you may change the theme for PeckerMgr - depending on what you like the most.

Also, if you would like to check QEMU's integrity, you may do so by heading to Tools > Verify QEMU location. This will look through all of the applications you have for QEMU - judging by what is listed in your Machines folder for PeckerMgr (nothing to worry about unless you have customised QEMU pretty heavily). If there is a file missing, you will have to look for a solution.

Feel free to also rename your virtual machine to anything else. Just please double check anything that might interfere with this virtual machine outside of the virtual machine's configuration file, because they may not be able to find your virtual machine after being renamed!

Ever want to redo the tour? Feel free to do so by heading over to Help > Tour!""",
"""Finally, if you ever encounter an error with PeckerMgr, you may get confused at it at first. Fortunately, there is an error booklet for this. Its contents will now be displayed now:

""" + (os.path.isfile(os.getcwd() + "/ErrorBook.txt") and open(os.getcwd() + "/ErrorBook.txt").read() or "ERROR: CANNOT READ ERRORBOOK.TXT OR DOCUMENT DOES NOT EXIST. CONSIDER REDOWNLOADING FILES."), # The brackets are put in place so the comma doesn't then change the string into a tuple.
"""Thank you for picking PeckerMgr. I hope that you enjoy using PeckerMgr :^)

--Quevidia"""
], 73]
HelpForAdvanced = [[ # Create a list of pages for the help with custom parameters documentary.
"""IT IS RECOMMENDED THAT YOU READ ALL PAGES BEFORE SPECIFYING ANY CUSTOM PARAMETERS.

If you are just copying and pasting information that you have retrieved from the internet, for example the code necessary for creating a specific NVRAM file used to store permanent memory such as the boot recorder, make sure that you research what the flags that you are implementing do first!

Otherwise, if you would like to specify your own parameters but are unsure of what exact flags to specify, you may always open up a command prompt, head over to your QEMU directory, and then type the following: qemu-system-ARCHITECTUREOFTHECPU -help. This will return a whole lot of flags that can be appended. For any additional information about each flag, type qemu-system-ARCHITECTUREOFTHECPU -FLAG ?. You can also use -help instead of ?, but this won't work with every flag.""",
"""There are a few shortcuts when specifying custom parameters. Not only will these shortcuts save some typing, but they will also prevent issues from coming up whenever a directory or two is not present. This includes the following:

{CustomWorkingDirectory} - The working directory of PeckerMgr.exe
{VMsLocation} - The default location for all of your virtual machines
{QEMULocation} - QEMU's location

{VMPath} (ONLY USED IN VIRTUAL MACHINES) - The location of the current virtual machine"""
], 23]

# Create our CPU and machine architecture listing. This will be a pretty large list!
Machines = []
MachinesFolder = os.getcwd() + "\Machines"
assert(os.path.isdir(MachinesFolder)), LaunchAspectsOfPeckerMgr.CreatePopup("""Application search error. E1""", "Error", 1)
for MachinesFound in LaunchAspectsOfPeckerMgr.ReturnListingOfDirectory(MachinesFolder, False): # Look for all of the available CPU architectures.
    CPUArchConfigFile = os.path.normpath(MachinesFolder + "/" + MachinesFound + "/config.cfg") # Using normpath because backslashes will be a pain to use. Without backslashes, os.path.isfile will report that the file is not present even if it actually is present.
    assert(os.path.isfile(CPUArchConfigFile)), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. DD", "Error", 2)
    Assertion, ThingToAdd = ConfigurationManager.CheckForStatementInConfigurationFile("Arch=", CPUArchConfigFile, False, False, True) # Get the name of the CPU arch in terms of what the QEMU application is called.
    assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. DD", "Error", 2) # If the input for the assert function is false, the assert will be carried out.
    Machines.append([
        MachinesFound, ThingToAdd, [] # CPU architecture
    ])

for i in range(0, len(Machines)): # Next stage of machines detecting: add all of the available machines and then look for the hardware of the machine!
    for MachinesForCPUArch in LaunchAspectsOfPeckerMgr.ReturnListingOfDirectory(MachinesFolder + "/" + Machines[i][0], False): # Look for all machines and add both the display name and the name used by QEMU into the Machines list.
        MachineToAddForCPUArch = [MachinesForCPUArch] # Create a sub-list that will be added to the CPU arch sub-list in the machines list.
        MachineConfigFile = os.path.normpath(MachinesFolder + "/" + Machines[i][0] + "/" + MachinesForCPUArch + "/config.cfg")
        assert(os.path.isfile(MachineConfigFile)), LaunchAspectsOfPeckerMgr.CreatePopup("The machine " + MachinesForCPUArch + " does not have a configuration file.", "Error", 4)
        Assertion, ThingToAdd = ConfigurationManager.CheckForStatementInConfigurationFile("Machine=", MachineConfigFile, False, False, True) # Check for the statement in the machine's configuration file.
        assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("""Please check the syntax of the configuration file. EE
Machine: """ + MachinesForCPUArch + """
Hardware index missing: Machine=""", "Error", 6) # If the input for the assert function is false, the assert will be carried out.
        MachineToAddForCPUArch.append(ThingToAdd) # Append all data to the MachineToAddForCPUArch sub-list.
        Machines[i][2].append(MachineToAddForCPUArch)
    
    # Now, look for all of the hardware used for this CPU architecture.
    ThingsToLookFor = ["CPU=", "Video=", "Sound=", "Network=", "Accel="] # Just to save a few lines of repetitive code :^)
    HardwareToAddInEnd = []
    for HardwareToAdd in range(len(ThingsToLookFor)): # Start adding all necessary things for the MachineToAddForCPUArch sub-list.
        Assertion, ThingToAdd = ConfigurationManager.CheckForStatementInConfigurationFile(ThingsToLookFor[HardwareToAdd], MachinesFolder + "/" + Machines[i][0] + "/config.cfg", True, False, True) # Check for the statement in the machine's configuration file.
        assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("""Please check the syntax of the configuration file. EE
CPU architecture: """ + Machines[i][0] + """
Hardware index missing: """ + ThingsToLookFor[HardwareToAdd], "Error", 6) # If the input for the assert function is false, the assert will be carried out.
        HardwareToAddInEnd.append(ThingToAdd)
    Machines[i].append(HardwareToAddInEnd) # Append all data to the CPU architecture sub-list.

# Choose the necessary theme for this application.
Assertion, ThemeToSearch = ConfigurationManager.CheckForStatementInConfigurationFile("Theme=", ConfigFile, False, True, True)
if ThemeToSearch != "":
    ThemeColour = ThemeToSearch
assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. E1", "Error", 2) # If ThemingCorrect is false, a popup will appear.
framework.theme(ThemeColour) # Finally, set the theme of the application.

# Check if the configuration file is present.
if not os.path.isdir(Config): # If the configuration directory is not present, then the following comamnds will run.
    LaunchAspectsOfPeckerMgr.CreatePopup("""The configuration directory is not present. This is normal if you are launching this application for the first time.

The configuration directory will now be created, alongside the configuration file.""", "Config not found", 5)
    os.mkdir(Config)
    open(ConfigFile, "w") # Although the function itself is named "open", using the argument "w" will also allow the function to create the necessary file if it does not exist.
elif not os.path.isfile(ConfigFile): # If the configuration directory is present but the configuration file isn't, then the following commands will run.
    LaunchAspectsOfPeckerMgr.CreatePopup("""Although the configuration directory is present, config.cfg is not present. Please double check if it has been renamed to something else or if it has been deleted.
    
A new config.cfg will be created.""", "Config not found", 5)
    open(os.getcwd() + "\config\config.cfg", "w")

# Check if the virtual machines directory is present
if ConfigurationManager.QuickCheck("VMsLocation=", ConfigFile) == -1: # If the configuration file is empty or there is no VMsLocation= statement, the following code in this scope will run.
    LaunchAspectsOfPeckerMgr.CreatePopup("""It seems that the configuration has no record of any virtual machines folder. This is also normal if you are launching this application for the first time""", "Virtual machine folder not recorded", 3)
    Events, UserInput = LaunchAspectsOfPeckerMgr.PromptUserToFindDirectory("Would you like to specify the location of the virtual machines folder? If you choose continue without browsing or click on the window exit button, the virtual machines folder will be placed on the same directory as PeckerMgr.", False, 4) # Get the user input of the directory window.
    FolderChosen = UserInput["Browse"] != "None" and UserInput["Browse"] or ""
    if FolderChosen == "" and (Events == framework.WIN_CLOSED or Events == "Continue"): # If user clicked no or just clicked the X button on the top right
        if not os.path.isdir(os.getcwd() + "\VMsLocation"):
            os.mkdir(os.getcwd() + "\VMsLocation")
        else:
            LaunchAspectsOfPeckerMgr.CreatePopup("It seems that the directory already exists.. Any chance that the configuration file might have been edited?", "Hmm...", 2)
        ConfigurationManager.AppendToConfigurationFile("VMsLocation=" + os.path.normpath(os.getcwd()).replace(";", "\;").replace(",", "\,") + "\VMsLocation", ConfigFile)
    elif FolderChosen != "":
        ConfigurationManager.AppendToConfigurationFile("VMsLocation=" + FolderChosen.replace(";", "\;").replace(",", "\,"), ConfigFile)
else:
    Assertion = ConfigurationManager.CheckForStatementInConfigurationFile("VMsLocation=", ConfigFile, False, True, True)
    assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. E2", "Error", 2)

VMsLocation.Set(ConfigurationManager.CheckForStatementInConfigurationFile("VMsLocation=", ConfigFile, False, False, True)[1]) # Finally, set the VMsLocation variable!

# Initiate the tour if TourDone=True; is not present in the configuration file.
if ConfigurationManager.QuickCheck("TourDone=True;", ConfigFile) == -1: LaunchAspectsOfPeckerMgr.CreateDocumentary(TourInformation[0], "Tour", TourInformation[1]) # If TourDone=True; is present in the configuration file, then the starting point of TourDone=True; will be returned. If it is not present, -1 will be returned instead.

# Check for QEMU location and append it to the configuration file.
if ConfigurationManager.QuickCheck("QEMU=", ConfigFile) == -1: # Check if QEMU= is not already in the configuration file. If -1, that means QEMU= is not present.
    if os.path.isdir("C:/Program Files/QEMU"): # Check if C:\Program Files\QEMU is present
        ConfigurationManager.AppendToConfigurationFile("QEMU=C:\Program Files\QEMU;", ConfigFile)
    elif os.path.isdir("C:/Program Files (x86)/QEMU"): # x86_64 systems only though I don't know why you'd install a 32-bit release of QEMU on a 64-bit operating system - check if C:\Program Files (x86)\QEMU is present
        ConfigurationManager.AppendToConfigurationFile("QEMU=C:\Program Files (x86)\QEMU;", ConfigFile)
    else:
        Events, UserInput = LaunchAspectsOfPeckerMgr.PromptUserToFindDirectory("It seems like that a recording of where QEMU is located at is not present in the configuration file, and it is also not located in your Program Files folder. Please browse for the directory that QEMU is located at.", True, 4)
        ConfigurationManager.AppendToConfigurationFile("QEMU=" + os.path.normpath(UserInput["Browse"]).replace(";", "\;").replace(",", "\,"), ConfigFile)
else:
    Assertion, QEM = ConfigurationManager.CheckForStatementInConfigurationFile("QEMU=", ConfigFile, False, True, True)
    assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. E3", "Error", 2) # If Assertion is false (due to incorrect syntax or whatever) a popup will appear.
    if QEM == "" or not os.path.isdir(QEM): # Check if QEM is not a valid location.
        Events, UserInput = LaunchAspectsOfPeckerMgr.PromptUserToFindDirectory("Either the QEMU recording in the configuration file is empty or the directory does not exist. Please re-locate the QEMU folder.""", True, 2)
        ConfigurationManager.AppendToConfigurationFile("QEMU=" + os.path.normpath(UserInput["Browse"]).replace(";", "\;").replace(",", "\,"), ConfigFile)

QEMULocation.Set(ConfigurationManager.CheckForStatementInConfigurationFile("QEMU=", ConfigFile, False, False, True)[1]) # Finally, set the QEMULocation variable!

# And finally, we can actually open PeckerMgr :^).
# First however, we need to make the layouts for each window.

while True: # Just in case any changes to the application layout are being made.
    Events = "" # This is so we can actually read the application info from the primary loop.
    UserInput = ""
    CurrentlySelectedVM = "none" # The currently selected virtual machine.
    PeckerMgrMenuLayout = [ # This will be the sub-menu of PeckerMgr.
        ["File", [
                    "New",
                    "Remove",
                    "Launch",
                    "---",
                    "Configure",
                    "Clone",
                    "Rename",
                    "---",
                    "Exit"
            ]
        ],
        ["Edit", [
                    "Preferences"
            ]
        ],
        ["Tools", [
                    "Verify QEMU location",
                    "Create virtual disk"
            ]
        ],
        ["Help", [
                    "Tour",
                    "About"
            ]
        ]
    ]

    PeckerMgrVMColumn = [] # This will be the column itself listing all of the virtual machines.
    VMsListing = LaunchAspectsOfPeckerMgr.ReturnListingOfDirectory(VMsLocation.Get(), False) # Simplifying
    
    for VMs in VMsListing: # List all of the directories.
        Assertion, ThingToAdd = ConfigurationManager.CheckForStatementInConfigurationFile("Arch=", os.path.normpath(VMsLocation.Get() + "/" + VMs + "\config.cfg"), False, False, True) # Get the name of the CPU arch.
        assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file in the VM directory called " + VMs + ". CC", "Error", 4)
        PeckerMgrVMColumn.append(# Append the desired column.
            [framework.Text(VMs, size = (54, 1), key = VMs, background_color = "#ebebeb", text_color = "#060e26", font = ("Segoe UI Light", 14), enable_events = True), framework.Image(background_color = "#ffffff", data = open(os.path.normpath(os.getcwd() + "/Icons/Architectures/" + ThingToAdd + ".png"), "rb").read())]
        )

    PeckerMgrLayouts = [
        [ # Create the layout for PeckerMgr itself.
            [framework.Text("Currently selected VM: none", font = ("Segoe UI Light", 14), key = "VMSelected", size = (50, 1), justification = "center")],
            [framework.Menu(PeckerMgrMenuLayout, background_color = "#f4f4f4", text_color = "#060e26", key = "VMsColumn")], # Create the sub-menu
            [framework.Column(PeckerMgrVMColumn, background_color = "#ffffff", size = (600, 300), scrollable = True, vertical_scroll_only = True, key = "VMListing")], # Create the VM listings.
            [framework.Button("New", key = "New"), framework.Button("Remove", key = "Remove"), framework.Button("Rename", key = "Rename"), framework.Button("Configure", key = "Configure"), framework.Button("Clone", key = "Clone"), framework.Button("Launch", key = "Launch")] # Create the necessary buttons all in the same row.
        ]
    ]

    PeckerMgr = framework.Window("PeckerMgr V1.20", PeckerMgrLayouts[0], element_justification = "center", debugger_enabled = False) # Finally, we can actually create the window itself!

    while True: # Create the application loop, since .read() only lasts once.
        Events, UserInput = PeckerMgr.read()
        CurrentlySelectedVM = Events if Events in VMsListing else CurrentlySelectedVM # Change the value of the CurrentlySelectedVM variable if one of the few options in the VMs list has been selected.
        PeckerMgr["VMSelected"].update("Currently selected VM: " + CurrentlySelectedVM) # Update the currently selected text.
        if Events == "About": # About option from the sub-menu.
            AboutLayout = [
                            [framework.Image(data = open(os.getcwd() + "\Icons\PeckerMgr1_64x64.png", "rb").read())],
                            [framework.Text("""PeckerMgr - a simplistic app made for creating and running QEMU virtual machines.

Made by Quevidia!""", justification = "center", size = (45, 4))],
                            [framework.Button("OK", size = (4, 1))]
                          ]
            PeckerMgr.hide() # To prevent mishaps from occurring.
            About = framework.Window("About PeckerMgr", AboutLayout, element_justification = "center", debugger_enabled = False)
            Events2, UserInput2 = About.read()
            if Events2 == "OK":
                About.close()
            PeckerMgr.un_hide() # Show PeckerMgr again.
        elif Events == "Tour": # Go through the tour again upon user request.
            PeckerMgr.hide()
            LaunchAspectsOfPeckerMgr.CreateDocumentary(TourInformation[0], "Tour", TourInformation[1])
            PeckerMgr.un_hide()
        elif Events in (framework.WIN_CLOSED, "Exit"): # Close PeckerMgr upon user request.
            break # End the loop.
        elif Events == "Preferences": # Change certain things with PeckerMgr.
            # Create the function for getting the name for the theme.
            def GetThemeName():
                return CurrentlySelectedTheme == "LightGrey6" and "Light" or CurrentlySelectedTheme == "BrownBlue" and "Navy" or CurrentlySelectedTheme == "DarkGrey2" and "Night"
            PeckerMgr.hide()

            # Create variables that will store information for changes.
            CurrentlySelectedTheme = framework.theme() # Gets the current theme if no parameters are supplied.
            Assertion1, NewQEMULocation = ConfigurationManager.CheckForStatementInConfigurationFile("QEMU=", ConfigFile, False, True, True) # Gets the current location for QEMU.
            Assertion2, NewVMsLocation = ConfigurationManager.CheckForStatementInConfigurationFile("VMsLocation=", ConfigFile, False, True, True)
            assert(Assertion1), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. E2", "Error", 2) # If Assertion is false (due to incorrect syntax or whatever) a popup will appear.
            assert(Assertion2), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. E3", "Error", 2)

            # Create the layout for the preferences window.
            PreferenceLayout = [
                [framework.Text("Themes", font = ("Segoe UI Light", 20))], # Text informing the user about the themes they can choose.
                [framework.Button("Light", key = "LightGrey6"), framework.Button("Navy", key = "BrownBlue"), framework.Button("Night", key = "DarkGrey2")], # All three available themes.
                [framework.Text("Theme currently being used: " + GetThemeName(), key = "ThemeText")], # This displays information about the currently selected theme.
                [framework.Text("Locate QEMU", font = ("Segoe UI Light", 20))], # Text informing the user to change the record of the location for QEMU in the configuration file.
                [framework.Text("If the current location of QEMU is incorrect, you may change it here.")], # More information about QEMU locating.
                [framework.Button("Change", key = "QEMUChange")], # Button for changing the location of QEMU.
                [framework.Text("Locate your VMs folder", font = ("Segoe UI Light", 20))], # Text informing the user to change the record of the location for the VMsLocation folder in the configuration file.
                [framework.Text("If the current location for your VMs folder is incorrect, you may change it here.")], # More information about VMsLocation locating.
                [framework.Button("Change", key = "VMsChange")], # Button for changing the location of VMsLocation.
                [framework.Text("To save all changes, click OK. Otherwise, click cancel.")], # Information about saving changes.
                [framework.Button("OK"), framework.Button("Cancel")], # Create the buttons that carry out certain actions.]
            ]

             # Make the preferences window itself :^)
            Preferences = framework.Window("PeckerMgr Preferences", PreferenceLayout, element_justification = "center", debugger_enabled = False)

            while True: # Create the application loop, since .read() only lasts once.
                Events2, UserInput2 = Preferences.read() # Read the events and user input of the window.
                if not Events2 == framework.WIN_CLOSED and Events2 != CurrentlySelectedTheme and Events2 in ("LightGrey6", "BrownBlue", "DarkGrey2"):
                    CurrentlySelectedTheme = Events2
                    Preferences["ThemeText"].update("Current theme selected: " + GetThemeName())
                elif Events2 == "QEMUChange":
                    Preferences.hide() # Prevent any mishaps.
                    Events3, UserInput3 = LaunchAspectsOfPeckerMgr.PromptUserToFindDirectory("Please locate your QEMU installation. If you chose this option by mistake, simply click Continue without browsing.", False, 2)
                    if Events3 != framework.WIN_CLOSED and UserInput3["Browse"] != "":
                        NewQEMULocation = UserInput3["Browse"]
                    Preferences.un_hide()
                elif Events2 == "VMsChange":
                    Preferences.hide() # Prevent any mishaps.
                    Events3, UserInput3 = LaunchAspectsOfPeckerMgr.PromptUserToFindDirectory("Please locate your VMs folder. If you chose this option by mistake, simply click Continue without browsing.", False, 2)
                    if Events3 != framework.WIN_CLOSED and UserInput3["Browse"] != "":
                        NewVMsLocation = UserInput3["Browse"]
                    Preferences.un_hide()
                elif Events2 in (framework.WIN_CLOSED, "Cancel", "OK"):
                    break # Stop the loop
            if Events2 == "OK":
                framework.theme(CurrentlySelectedTheme) # Finally apply the changes to PeckerMgr!
                ConfigurationManager.AppendToConfigurationFile("Theme=" + os.path.normpath(CurrentlySelectedTheme), ConfigFile) # Append the changes made to the configuration file.
                ConfigurationManager.AppendToConfigurationFile("QEMU=" + os.path.normpath(NewQEMULocation).replace(";", "\;").replace(",", "\,"), ConfigFile)
                ConfigurationManager.AppendToConfigurationFile("VMsLocation=" + os.path.normpath(NewVMsLocation).replace(";", "\;").replace(",", "\,"), ConfigFile)
                QEMULocation.Set(NewQEMULocation)
                VMsLocation.Set(NewVMsLocation)
                Preferences.close() # Make sure that the preferences window actually closes.
                PeckerMgr.close()
                break
            else:
                Preferences.close() # Close the window just in case it hasn't already.
                PeckerMgr.un_hide()
        elif Events == "New": # If the new button has been selected, this will open up the new virtual machine wizard.
            PeckerMgr.hide()
            ListOfCPUArchs = [] # Create a list for each CPU architecture option.
            for i in range(len(Machines)): # Create a for loop to get all values inside of the Machines list.
                ListOfCPUArchs.append(Machines[i][0]) # Append the information to the ListOfCPUArchs list.

            # Create the layout itself.
            NewVMLayout = [
                [framework.Text("Create a new virtual machine", font = ("Segoe UI Light", 18))], # Essentially a title for the application.
                [framework.Text("You will be allowed to create your new virtual machine here and give the virtual machine its own name. You may also choose the CPU architecture. Any additional changes will have to be made after creating the virtual machine.", size = (58, 4), justification = "center")], # A description telling the user what they can do.
                [framework.Text("Virtual machine name:"), framework.Input(key = "VM Name", background_color = "#ffffff", text_color = "#060e26")], # Allow the user to choose the virtual machine name.
                [framework.Listbox(values = ListOfCPUArchs, default_values = ListOfCPUArchs[0], size = (60, 10), background_color = "#ffffff", text_color = "#060e26", key = "CPU Arch")], # Create the listbox, which will list all CPU architectures.
                [framework.Button("OK", key = "OK"), framework.Button("Cancel", key = "Cancel")] # Final user input choices to make.
            ]

            # Create the window.
            NewVMWindow = framework.Window("Create virtual machine wizard", layout = NewVMLayout, element_justification = "center", size = (500, 365), debugger_enabled = False)
            Events2 = None  # Define Events2 outside of the while loop.
            while True: # Create a new loop, since user input may be registered more than once.
                Events2, UserInput2 = NewVMWindow.read()
                if Events2 in ("Cancel", framework.WIN_CLOSED): # Check if the user cancelled this process.
                    break
                elif Events2 == "OK": # Check if the user clicked OK.
                    ContainsIllegalCharacters = False # Create a bool variable that will be used to check if the new virtual machine name contains illegal characters.
                    for Char in UserInput2["VM Name"]: # Go through all of the characters in UserInput2["NewVMName"].
                        if Char in ("\\", "/", ":", "*", "?", '"', "<", ">", "|"): # Check if the character contains any illegal characters.
                            ContainsIllegalCharacters = True # Set ContainsIllegalCharacters to True.
                            break # End the foor loop.
                    if ContainsIllegalCharacters: # Check if ContainsIllegalCharacters is True.
                        LaunchAspectsOfPeckerMgr.CreatePopup("""Please refrain from using unwanted characters. This includes the following: \\, /, :, *, ?, ", ', <, > and |.""", "Error", 2)
                    elif UserInput2["VM Name"] == "": # Check if the user input is empty.
                        LaunchAspectsOfPeckerMgr.CreatePopup("Please input something.", "Error", 1)
                    elif os.path.isdir(os.path.normpath(VMsLocation.Get() + "/" + UserInput2["VM Name"])): # Check if the directory already exists.
                        LaunchAspectsOfPeckerMgr.CreatePopup("This virtual machine already exists.", "Error", 1)
                    else:
                        os.mkdir(os.path.normpath(VMsLocation.Get() + "/" + UserInput2["VM Name"])) # Make a new directory in the VMsLocation directory.
                        open(os.path.normpath(VMsLocation.Get() + "/" + UserInput2["VM Name"] + "/config.cfg"), "w").write("Arch=" + UserInput2["CPU Arch"][0] + ";") # Make a new config file in the created directory.
                        break # End the loop
            NewVMWindow.close() # Ensure that the windows has been closed.
            if Events2 != "OK": # Check if OK has not been selected.
                PeckerMgr.un_hide() # Show PeckerMgr again.
            else:
                break # End the loop so PeckerMgr can be refreshed. This will also go through the virtual machines list check again, thus showing the new virtual machine.
        elif Events == "Remove": # If the remove button has been selected, this will open up the remove virtual machine wizard.
            PeckerMgr.hide()
            if CurrentlySelectedVM == "none": LaunchAspectsOfPeckerMgr.TellUserToSelectVM() # Check if a virtual machine has not been selected.
            else:
                RemoveVMLayout = [
                    [framework.Text("Caution", font = ("Segoe UI Light", 16))], # Warning text
                    [framework.Text("You are about to delete the virtual machine " + CurrentlySelectedVM + ". Are you sure that you would like to proceed?", justification = "center", size = (45, 5))], # Description of what the user is about to do.
                    [framework.Button("Yes", key = "Yes"), framework.Button("No")] # User choice
                ]
                RemoveVMWindow = framework.Window("Remove virtual machine wizard", layout = RemoveVMLayout, element_justification = "center", debugger_enabled = False) # Finally, create the window!
                Events2, UserInput2 = RemoveVMWindow.read() # Since user input will only be recorded once before the application actually closes, a loop is unnecessary.
                RemoveVMWindow.close() # Close the window, should the user have chosen the yes or no button.
                if Events2 == "Yes": # Check if the user selected yes.
                    if os.path.isdir(os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM)): # Check if the directory is present to prevent the code from erroring.
                        shutil.rmtree(os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM)) # Remove the directory.
                    else:
                        LaunchAspectsOfPeckerMgr.CreatePopup("Directory is no longer present.", "Error", 1)
                    break # End the loop so a new instance of PeckerMgr opens up. This also refreshes the virtual machine listing, since the virtual machine folder is checked in the loop outside of the PeckerMgr loop.
                else:
                    PeckerMgr.un_hide()
        elif Events == "Clone":
            PeckerMgr.hide()
            if CurrentlySelectedVM == "none": LaunchAspectsOfPeckerMgr.TellUserToSelectVM() # Check if a virtual machine has not been selected.
            else:
                VMPath = os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM) # Create a variable that will hold the location of the virtual machine being renamed.
                CloneVMLayout = [ # Create the layout for this window!
                    [framework.Text("Clone your virtual machine", font = ("Segoe UI Light", 16))], # Title of the wizard.
                    [framework.Text("Please specify a name for your new cloned virtual machine.", justification = "center", size = (45, 2))], # Description of the wizard.
                    [framework.Text("Virtual machine name:"), framework.Input(key = "VMName", background_color = "#ffffff", text_color = "#060e26")], # Allow the user to choose the virtual machine name.
                    [framework.Button("OK", key = "OK"), framework.Button("Cancel", key = "Cancel")] # Final user input choices to make.
                ]

                CloneVMWindow = framework.Window("Clone virtual machine wizard", layout = CloneVMLayout, element_justification = "center", debugger_enabled = False) # Finally, create the window!
                Events2 = None # Define Events2 outside of the while loop.
                while True: # Create a loop, since user input may be registered more than once.
                    Events2, UserInput2 = CloneVMWindow.read()
                    if Events2 in ("Cancel", framework.WIN_CLOSED): # Check if the user cancelled this process.
                        break
                    elif Events2 == "OK": # Check if the user pressed OK.
                        ContainsIllegalCharacters = False # Create a bool variable that will be used to check if the new virtual machine name contains illegal characters.
                        for Char in UserInput2["VMName"]: # Go through all of the characters in UserInput2["VMName"].
                            if Char in ("\\", "/", ":", "*", "?", '"', "<", ">", "|"): # Check if the character contains any illegal characters.
                                ContainsIllegalCharacters = True # Set ContainsIllegalCharacters to True.
                                break # End the foor loop.
                        if ContainsIllegalCharacters: # Check if ContainsIllegalCharacters is True.
                            LaunchAspectsOfPeckerMgr.CreatePopup("""Please refrain from using unwanted characters. This includes the following: \\, /, :, *, ?, ", ', <, > and |.""", "Error", 2)
                        elif UserInput2["VMName"] == "": # Check if the user input is empty.
                            LaunchAspectsOfPeckerMgr.CreatePopup("Please input something.", "Error", 1)
                        elif os.path.isdir(UserInput2["VMName"]): # Check if the directory already exists.
                            LaunchAspectsOfPeckerMgr.CreatePopup("This virtual machine already exists.", "Error", 1)
                        elif not os.path.isdir(os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM)): # Check if the directory has somehow been removed.
                            LaunchAspectsOfPeckerMgr.CreatePopup("This virtual machine does not exist anymore.", "Error", 1)
                        else:
                            PopupToAppear = LaunchAspectsOfPeckerMgr.CreatePopup("Please wait while your virtual machine is copied over. This will take some time if your virtual machine contains large disk images inside it.", "Please wait...", 3, CreateButtons = False) # Create a popup without any buttons.
                            shutil.copytree(VMPath, os.path.normpath(VMsLocation.Get() + "/" + UserInput2["VMName"]))
                            PopupToAppear.close(); CloneVMWindow.hide() # Close PopupToAppear and hide CloneVMWindow.
                            LaunchAspectsOfPeckerMgr.CreatePopup("Just a reminder that you may want to configure the new virtual machine, should you want to tweak a thing or two.", "Reminder", 2)
                            break
                CloneVMWindow.close() # Ensure that the window has closed.
                if Events2 != "OK":
                    PeckerMgr.un_hide()
                else:
                    break # End the loop so PeckerMgr can be properly refreshed.
        elif Events == "Rename": # If the rename button has been selected, this will open up the rename virtual machine wizard.
            PeckerMgr.hide()
            if CurrentlySelectedVM == "none": LaunchAspectsOfPeckerMgr.TellUserToSelectVM() # Check if a virtual machine has not been selected.
            else:
                VMPath = os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM) # Create a variable that will hold the location of the virtual machine being renamed.
                RenameVMLayout = [ # Create the layout for this window!
                    [framework.Text("Rename your virtual machine", font = ("Segoe UI Light", 16))], # Title of the wizard.
                    [framework.Text("Feel free to change the name of your virtual machine to anything that you want, as long as it does not use unwanted characters.", justification = "center", size = (65, 3))], # Description of the wizard.
                    [framework.Text("New virtual machine name:"), framework.Input(key = "NewVMName", background_color = "#ffffff", text_color = "#060e26")], # Allow the user to choose the virtual machine name.
                    [framework.Button("OK", key = "OK"), framework.Button("Cancel", key = "Cancel")] # Final user input choices to make.
                ]

                RenameVMWindow = framework.Window("Rename virtual machine wizard", layout = RenameVMLayout, element_justification = "center", debugger_enabled = False) # Finally, create the window!
                Events2 = None # Define Events2 outside of the while loop.
                while True: # Create a loop, since user input may be registered more than once.
                    Events2, UserInput2 = RenameVMWindow.read()
                    if Events2 in ("Cancel", framework.WIN_CLOSED): # Check if the user cancelled this process.
                        break
                    elif Events2 == "OK": # Check if the user pressed OK.
                        ContainsIllegalCharacters = False # Create a bool variable that will be used to check if the new virtual machine name contains illegal characters.
                        for Char in UserInput2["NewVMName"]: # Go through all of the characters in UserInput2["NewVMName"].
                            if Char in ("\\", "/", ":", "*", "?", '"', "<", ">", "|"): # Check if the character contains any illegal characters.
                                ContainsIllegalCharacters = True # Set ContainsIllegalCharacters to True.
                                break # End the foor loop.
                        if ContainsIllegalCharacters: # Check if ContainsIllegalCharacters is True.
                            LaunchAspectsOfPeckerMgr.CreatePopup("""Please refrain from using unwanted characters. This includes the following: \\, /, :, *, ?, ", ', <, > and |.""", "Error", 2)
                        elif UserInput2["NewVMName"] == "": # Check if the user input is empty.
                            LaunchAspectsOfPeckerMgr.CreatePopup("Please input something.", "Error", 1)
                        elif os.path.isdir(UserInput2["NewVMName"]): # Check if the directory already exists.
                            LaunchAspectsOfPeckerMgr.CreatePopup("This virtual machine already exists.", "Error", 1)
                        elif not os.path.isdir(os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM)): # Check if the directory has somehow been removed.
                            LaunchAspectsOfPeckerMgr.CreatePopup("This virtual machine does not exist anymore.", "Error", 1)
                        elif LaunchAspectsOfPeckerMgr.CreatePopup("Are you sure? This may cause issues with unresolved configurations outside of the virtual machine's configuration!", "Warning", 2, CustomLayout = [framework.Button("Yes", key = "Yes"), framework.Button("No", key = "No")]) == "Yes": # Check if the user is 100% positive with renaming their virtual machine.
                            os.rename(VMPath, os.path.normpath(VMsLocation.Get() + "/" + UserInput2["NewVMName"]))
                            break
                RenameVMWindow.close() # Ensure that the window has closed.
                if Events2 != "OK":
                    PeckerMgr.un_hide()
                else:
                    break # End the loop so PeckerMgr can be properly refreshed.
        elif Events == "Verify QEMU location": # If the user has selected the verify QEMU location option then the following code will run.
            Message = LaunchAspectsOfPeckerMgr.VerifyQEMULocation() # Run through the verification for QEMU.
            LaunchAspectsOfPeckerMgr.CreatePopup(Message[0], Message[1], 2 if Message[0].find("qemu-system-", 0, len(Message[0])) == -1 else 4)
        elif Events == "Create virtual disk": # If the user has selected the create virtual disk option then the following code will run.
            PeckerMgr.hide() # Hide PeckerMgr to prevent issues from happening.
            LaunchAspectsOfPeckerMgr.CreateDiskWizard() # Launch the create disk wizard.
            PeckerMgr.un_hide() # Show PeckerMgr again.
        elif Events == "Configure": # If the user chose the configure option, the following code will run.
            PeckerMgr.hide()
            VMPath = os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM)
            VMConfigFile = VMPath + "\config.cfg"
            if CurrentlySelectedVM == "none": LaunchAspectsOfPeckerMgr.TellUserToSelectVM() # Check if a virtual machine has not been selected.
            elif not os.path.isdir(VMPath): # Check if the directory has somehow been deleted.
                LaunchAspectsOfPeckerMgr.CreatePopup("The directory for this virtual machine no longer exists.", "Error", 2)
            elif not os.path.isfile(VMConfigFile): # Check if the configuration file does not exist.
                LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. CC", "Error", 2)
            else:
                # Before we do anything, we will need to get the CPU architecture for the virtual machine. This is crucial in order to specify the correct options.
                Assertion, CPUArchForVM = ConfigurationManager.CheckForStatementInConfigurationFile("Arch=", VMConfigFile, False, False, True) # Get the CPU architecture of the virtual machine from the configuration file.
                assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. BB", "Error", 2) # If the input for the assert function is false, the assert will be carried out.

                # We will also need to get a list of all hardware used for this.
                AllHardwareAvailable = [["Do not specify"]] # Specify all available hardware
                MachinesForVM, CPUsForVM = ["Do not specify"], ["Do not specify"] # Specify all available hardware
                for CPUArchFound in range(len(Machines)): # Skim through the machines list.
                    if Machines[CPUArchFound][0] == CPUArchForVM: # Check if the first value of Machines[CPUArchFound] is the same as the CPUArchForVM value.
                        for MachinesFoundInListing in range(len(Machines[CPUArchFound][2])): # Skim through all machines for the CPU architecture.
                            AllHardwareAvailable[0].append(Machines[CPUArchFound][2][MachinesFoundInListing][0]) # Append the machine name to the MachinesForVM list
                        for HardwareType in range(1, len(Machines[CPUArchFound][3]) + 1): # Look for all hardware specifications for the CPU architecture.
                            AllHardwareAvailable.append(["Do not specify"])
                            if Machines[CPUArchFound][3][HardwareType - 1] != ["none"]: # Check if the hardware list being looked at does contain at least one sort of hardware.
                                AllHardwareAvailable[HardwareType] = AllHardwareAvailable[HardwareType] + Machines[CPUArchFound][3][HardwareType - 1]

                # All current information will also need to be acquired.
                CurrentHardware = [] # Store all current hardware.
                AllHardwareToLookFor = {0 : "MachineName=", 1: "CPU=", 2 : "Video=", 3 : "Sound=", 4 : "Network=", 5 : "Accel=", 6 : "Memory=", 7 : "hda=", 8 : "hdb=", 9 : "hdc=", 10 : "hdd=", 11 : "odd=", 12 : "fda=", 13 : "fdb=", 14 : "BootOrder=", 15 : "DisplayType=", 16 : "Custom="} # Specify all hardware that will be looked for to reduce the amount of lines of code :^)
                for HardwareType in range(len(AllHardwareToLookFor)): # Skim through all hardware to look for and see if they have been depicted inside the virtual machine's configuration file.
                    Assertion, HardwareLookingFor = ConfigurationManager.CheckForStatementInConfigurationFile(AllHardwareToLookFor[HardwareType], VMConfigFile, "Ignore", True, False) # Get the hardware being looked for curerntly in the VM's configuration file.
                    assert(Assertion), LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. BB", "Error", 2) # If the input for the assert function is false, the assert will be carried out.
                    if HardwareLookingFor in ("", "None") and not len(AllHardwareAvailable) - 1 <= HardwareType: # Check if the HardwareLookingFor variable is empty or consists of "None". Also check if the hardware being looked for is actually in the HardwareLookingForList.
                        HardwareLookingFor = AllHardwareAvailable[HardwareType][0]
                    elif HardwareLookingFor in ("", "None") and len(AllHardwareAvailable) - 1 <= HardwareType:
                        HardwareLookingFor = "Do not specify"
                    CurrentHardware.append(HardwareLookingFor) # Append the information to the CurrentHardware list so the current hardware can be displayed in the dropdown menus.
                # Now, before creating the window, we will need to make all of the layouts for the window itself.
                MachineTab = [ # Create the machines tab. This will allow the user to choose all baseline hardware and QEMU acceleration choices.
                    [framework.Text("CPU architecture: " + CPUArchForVM, font = ("Segoe UI Light", 16))], # Specify the CPU architecture.
                    [framework.Text("Machine:      "), framework.Combo(AllHardwareAvailable[0], size = (75, 1), default_value = CurrentHardware[0], enable_events = True, key = "MachineName", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdown menu for the machine listing.
                    [framework.Text("CPU:           "), framework.Combo(AllHardwareAvailable[1], size = (75, 1), default_value = CurrentHardware[1], enable_events = True, key = "CPU", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdown menu for the CPU listing.
                    [framework.Text("Memory:      "), framework.Input(key = "Memory", enable_events = True, size = (77, 1), default_text = CurrentHardware[6], background_color = "#ffffff", text_color = "#060e26")], # Create an input box for memory allocation.
                    [framework.Text("Storage allocation units can be either single-lettered (what QEMU uses) or what the true abbreviations are. All available storage allocation units (and their respective single-lettered variants): B, KB, MB, GB, TB, PB, EB.", size = (70, 4), justification = "center")], # Disclaimer about memory allocation.
                    [framework.Text("Acceleration:"), framework.Combo(AllHardwareAvailable[5], size = (75, 1), default_value = CurrentHardware[5], enable_events = True, key = "Accel", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdownm neu for QEMU acceleration options.
                    [framework.Text("Acceleration consists of the usage of third-party software in order to boost the performance of virtual machines used with QEMU, whether it is taking advantage of virtualisation capabilities implemented on computer processors or if it is taking advantage of bare-metal hypervisor platforms installed on Windows.", size = (70, 4), justification = "center")], # Description about QEMU acceleration.
                ]
                PeripheralsTab = [ # Create the peripherals tab. This will allow the user to choose between a selection of additional cards for their system, whether it's a video card or a networking card and such.
                    [framework.Text("Video card:    "), framework.Combo(AllHardwareAvailable[2], size = (75, 1), default_value = CurrentHardware[2], enable_events = True, key = "Video", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdown menu for the video card listing.
                    [framework.Text("Sound card:   "), framework.Combo(AllHardwareAvailable[3], size = (75, 1), default_value = CurrentHardware[3], enable_events = True, key = "Sound", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdown menu for the sound card listing.
                    [framework.Text("Network card:"), framework.Combo(AllHardwareAvailable[4], size = (75, 1), default_value = CurrentHardware[4], enable_events = True, key = "Network", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdown menu for the network card listing.
                    [framework.Text("You won't have to configure any of these cards. Just simply choose a card of your choice and they'll work on the go. Of course, install the drivers for them inside the emulated operating system if necessary - otherwise you won't get the proper experience out of them. Of course, choose a card that perfectly fits the time era as well, otherwise you will not get them to work properly if the card you chose is too new or too old.", size = (70, 6), font = ("Segoe UI Light", 12), justification = "center")]
                ]
                DrivesTab = [ # Create the drives tab. This will allow the user to choose what drive mediums they would like to specify.
                    [framework.Button("Clear", key = "Clearhda"), framework.Text("Hard drive 1: " + CurrentHardware[7], key = "HD1", size = (65, 1))], # Description and a clear option for the first hard drive.
                    [framework.FileBrowse(key = "hda", enable_events = True)], # Create a browse option for hard drive ide 0:0.
                    [framework.Button("Clear", key = "Clearhdb"), framework.Text("Hard drive 2: " + CurrentHardware[8], key = "HD2", size = (65, 1))], # Description and a clear option for the second hard drive.
                    [framework.FileBrowse(key = "hdb", enable_events = True)], # Create a browse option for hard drive ide 0:1.
                    [framework.Button("Clear", key = "Clearhdc"), framework.Text("Hard drive 3: " + CurrentHardware[9], key = "HD3", size = (65, 1))], # Description and a clear option for the third hard drive.
                    [framework.FileBrowse(key = "hdc", enable_events = True)], # Create a browse option for hard drive ide 1:0.
                    [framework.Button("Clear", key = "Clearhdd"), framework.Text("Hard drive 4: " + CurrentHardware[10], key = "HD4", size = (65, 1))], # Description and a clear option for the fourth hard drive.
                    [framework.FileBrowse(key = "hdd", enable_events = True)], # Create a browse option for hard drive ide 1:1.
                    [framework.Button("Create virtual disk", key = "CreateDisk")] # Create an option that allows the user to create a new disk.
                ]
                RemovableDrivesTab = [ # Create the removable drives tab. This will allow the user to choose what CDs/DVDs and floppies they would like to insert.
                    [framework.Button("Clear", key = "Clearodd"), framework.Text("Optical disc drive: " + CurrentHardware[11], key = "ODD", size = (65, 1))], # Description and a clear option for the optical disc drive.
                    [framework.FileBrowse(key = "odd", enable_events = True)], # Create a browse option for the optical disc drive ide 1:0.
                    [framework.Button("Clear", key = "Clearfda"), framework.Text("Floppy drive 1: " + CurrentHardware[12], key = "FD1", size = (65, 1))], # Description and a clear option for the first floppy drive.
                    [framework.FileBrowse(key = "fda", enable_events = True)], # Create a browse option for floppy drive A.
                    [framework.Button("Clear", key = "Clearfdb"), framework.Text("Floppy drive 2: " + CurrentHardware[13], key = "FD2", size = (65, 1))], # Description and a clear option for the second floppy drive.
                    [framework.FileBrowse(key = "fdb", enable_events = True)], # Create a browse option for floppy drive B.
                    [framework.Text("Disclaimer: Be aware that the third hard drive and the optical disc drive both share the same connection - IDE secondary master (IDE 1:0). If both drives are specified, a conflict will occur - thus QEMU will not launch.", justification = "center", size = (62, 3), font = ("Segoe UI light", 13))]
                ]
                MiscellaneousTab = [ # Create a tab for any miscellaneous options, such as the display type.
                    [framework.Text("Boot order:"), framework.Input(key = "BootOrder", enable_events = True, default_text = CurrentHardware[14], size = (77, 1), background_color = "#ffffff", text_color = "#060e26")], # Create an input box for the boot order.
                    [framework.Text("Specify the boot order by using the following letters: A - floppy 1, C - hard drive 1, D - optical disc, N - network. This order is not case-sensitive.", size = (70, 2), justification = "center")], # Disclaimer about the boot order.
                    [framework.Text("Display type:"), framework.Combo(["Do not specify", "gtk", "sdl", "curses"], default_value = CurrentHardware[15], size = (77, 1), enable_events = True, key = "DisplayType", background_color = "#ffffff", text_color = "#060e26")], # Create a dropdown menu for the display type.
                    [framework.Text("Change the interface for QEMU. GTK (the default user interface) will provoke QEMU to use a custom GNOME-like graphical user interface. SDL will provoke QEMU to use Windows' native titlebar. Curses will provoke QEMU to use a text-only user interface.", size = (70, 3), justification = "center")], # Disclaimer about the display type.
                    [framework.Text("Custom parameters:"), framework.Input(key = "Custom", enable_events = True, default_text = CurrentHardware[16], size = (77, 1), background_color = "#ffffff", text_color = "#060e26")], # Create an input box for any additional parameters.
                    [framework.Text("ONLY TOUCH THIS IF YOU KNOW WHAT YOU ARE DOING. Here, you can specify any additional parameters that you would like to use with this QEMU virtual machine.", size = (70, 3), justification = "center")], # Disclaimer about the custom parameters input box.
                    [framework.Button("Need help?", key = "HelpForAdvanced")] # Create a button that will open up a documentary window depicting about the custom parameters if clicked.
                ]

                ConfigureLayout = [ # Create the layout for the window itself.
                    [framework.TabGroup([ # Create a tabgroup.
                        [framework.Tab("Machine", MachineTab, element_justification = "center")], # Specify the machine tab.
                        [framework.Tab("Peripherals", PeripheralsTab, element_justification = "center")], # Specify the peripherals tab.
                        [framework.Tab("Non-removable mediums", DrivesTab, element_justification = "center")], # Specify the drives tab.
                        [framework.Tab("Removable mediums", RemovableDrivesTab, element_justification = "center")], # Specify the removable drives tab.
                        [framework.Tab("Miscellaneous", MiscellaneousTab, element_justification = "center")] # Specify the miscellaneous tab.
                    ])],
                    [framework.Button("OK", key = "OK"), framework.Button("Cancel", key = "Cancel")] # Create the buttons that the user can choose from when they're done.
                ]
                
                # Now, create a few extra variables and functions for this.
                ChangesMade = [] # All changes to be made will be added to this list, and then will be applied to the virtual machine configuration file if the user selected "OK".
                def MakeChange(ChangeToAdd): # This will just make appending to the ChangesMade list a bit more simplistic.
                    Found = False # Check if the change already exists in the ChangesMade list.
                    def GetVariable(String): # Create a sub-function for getting the variable from a string.
                        VariableToUse = ""
                        for Char in String: # Skim through the ChangeToAdd string so we can get the exact variable.
                            VariableToUse = VariableToUse + Char # Append the current character to the Variable string.
                            if Char == "=": # Check if the character is an equal sign.
                                break # End the loop.
                        return VariableToUse
                    Variable = GetVariable(ChangeToAdd) # Get the variable name from the ChangeToAdd string.
                    for Change in range(len(ChangesMade)): # Skim through the ChangesMade list.
                        VariableInChange = GetVariable(ChangesMade[Change]) # Get the variable name for the change being looked at in the ChangesMade list.
                        if VariableInChange == Variable: # Check if the change being looked at has the same variable name as the change we are making.
                            Found = True
                            break # End the loop.
                    if Found: # Check if the Found variable is True, due to the change variable name already existing in the ChangeToAdd list.
                        ChangesMade[Change] = ChangeToAdd # Edit the existing change variable's value.
                    else:
                        ChangesMade.append(ChangeToAdd) # Append the ChangeToAdd information.

                # And finally, make the window itself! Once done, start the main loop since user input will be registered more than once!
                Configure = framework.Window("Configure virtual machine wizard", layout = ConfigureLayout, element_justification = "center", size = (600, 370), debugger_enabled = False)

                while True:
                    Events2, UserInput2 = Configure.read() # Show the window and read all user input.
                    if Events2 in ("Cancel", framework.WIN_CLOSED): # Check if the user has decided to close the window.
                        break # End the loop.
                    elif not Events2 in (framework.WIN_CLOSED, "OK", "Cancel", "Clearhda", "Clearhdb", "Clearhdc", "Clearhdd", "Clearodd", "Clearfda", "Clearfdb", "CreateDisk", "HelpForAdvanced"): # Check if the user has decided to make a change to the specification of any of their drives.
                        DrivesSpecification, ExactChange = ("hda", "hdb", "hdc", "hdd", "odd", "fda", "fdb"), Events2 + "=" + UserInput2[Events2].replace("Do not specify", "None") # Create a variable for each drive specification and the exact change to append.
                        if Events2 in DrivesSpecification and not UserInput2[Events2] == "": # Check if the events was modifying any of the drive specifications and the user input is not empty.
                            MakeChange(ConfigurationManager.OverrideValues(os.path.normpath(ExactChange), AdditionalValues = [["{VMPath}", VMPath]])) # Add the change to the ChangesMade list.
                        elif not Events2 in DrivesSpecification: # Check if the current event is not related to the specification of any of their drives.
                            MakeChange(ExactChange.lower().replace("bootorder", "BootOrder") if Events2 == "BootOrder" else ExactChange) # Add the change to the ChangesMade list, and modify the ExactChange variable to contain lowercase options if the current event is modifying the boot order.
                    elif Events2 == "OK": # Check if the user has selected OK.
                        if not os.path.isfile(VMConfigFile): # Check if the configuration file has somehow disappeared.
                            LaunchAspectsOfPeckerMgr.CreatePopup("The configuration file for your virtual machine no longer exists.", "Error", 2)
                        else:
                            MemoryAllocation, BootOrderAllocation = True, True # This will signify if the memory allocation and the boot order is correct.
                            if len(UserInput2["Memory"]) > 0 and UserInput2["Memory"] != "Do not specify": # Check if the user has decided to allocate some memory for their machine.
                                if LaunchAspectsOfPeckerMgr.CheckDiskSize(UserInput2["Memory"])[0] == "Error": MemoryAllocation = False # Check if the first entry of the returned value of LaunchAspectsOfPeckerMgr.CheckDiskSize() is "Error. If so, set MemoryAllocation to False.
                            if len(UserInput2["BootOrder"]) > 0 and UserInput2["BootOrder"] != "Do not specify": # Check if the user has decided to specify a boot order.
                                Specified = {"a" : False, "c" : False, "d" : False, "n" : False} # Specify all options and see if they have been specified already.
                                for String in UserInput2["BootOrder"]: # Go through all of the specified options in the boot order.
                                    if String.lower() in Specified: # Check if the string is in the specified list.
                                        if Specified[String.lower()] == True: # Check if the boot option has already been specified.
                                            BootOrderAllocation = False
                                        Specified[String.lower()] = True # Set the string specification in the Specified list to true.
                                    else:
                                        BootOrderAllocation = False
                            if not MemoryAllocation: # Check if the MemoryAllocation variable equals False.
                                LaunchAspectsOfPeckerMgr.CreatePopup("Please check your memory allocation.", "Error", 1)
                            elif not BootOrderAllocation:
                                LaunchAspectsOfPeckerMgr.CreatePopup("Please check your boot order.", "Error", 1)
                            else:
                                for Changes in ChangesMade: # Skim through all of the changes that the user has decided to make.
                                    ConfigurationManager.AppendToConfigurationFile(Changes, VMConfigFile) # Append the information to the configuration file.
                                break # End the loop.
                    elif Events2 in ("Clearhda", "Clearhdb", "Clearhdc", "Clearhdd"): # Check if the user wants to clear any of the four hard drive specifications.
                        LetterToNumber = {"a" : 1, "b" : 2, "c" : 3, "d" : 4} # Specify the number variants of the letters.
                        Configure["HD" + str(LetterToNumber[Events2[-1]])].update("Hard drive " + str(LetterToNumber[Events2[-1]]) + ": Do not specify")
                        MakeChange("hd" + Events2[-1] + "=None")
                    elif Events2 == "Clearodd": # Check if the user wants to clear the optical disc drive specification.
                        Configure["ODD"].update("Optical disc drive: Do not specify")
                        MakeChange("odd=None")
                    elif Events2 in ("Clearfda", "Clearfdb"): # Check if the user wants to clear any of the two floppy drive specifications.
                        LetterToNumber = {"a" : 1, "b" : 2, "c" : 3, "d" : 4} # Specify the number variants of the letters.
                        Configure["FD" + str(LetterToNumber[Events2[-1]])].update("Floppy drive " + str(LetterToNumber[Events2[-1]]) + ": Do not specify")
                        MakeChange("fd" + Events2[-1] + "=None")
                    elif Events2 == "CreateDisk": # Check if the user wants to create a new disk.
                        Configure.hide() # Hide the configuration wizard to prevent issues from arising.
                        LaunchAspectsOfPeckerMgr.CreateDiskWizard(DefaultDiskLocation = VMPath) # Launch the create disk wizard.
                        Configure.un_hide() # Show the configuration window again.
                    elif Events2 == "HelpForAdvanced": # Check if the user would like help for the custom parameters option in the miscellaneous tab.
                        Configure.hide() # Hide the configuration wizard to prevent issues from arising.
                        LaunchAspectsOfPeckerMgr.CreateDocumentary(HelpForAdvanced[0], "Help with custom parameters", HelpForAdvanced[1])
                        Configure.un_hide() # Show the configuration window again.
                    if Events2 in ("hda", "hdb", "hdc", "hdd"): # Check if any of the four hard drive specifications were configured.
                        LetterToNumber = {"a" : 1, "b" : 2, "c" : 3, "d" : 4} # Specify the number variants of the letters.
                        if UserInput2[Events2] != "": # Check if the user input is not empty.
                            Configure["HD" + str(LetterToNumber[Events2[-1]])].update("Hard drive " + str(LetterToNumber[Events2[-1]]) + ": " + ConfigurationManager.OverrideValues(os.path.normpath(UserInput2[Events2]), AdditionalValues = [["{VMPath}", VMPath]])) # Update the hard drive information.
                    elif Events2 == "odd": # Check if the optical disc drive specification was configured.
                        if UserInput2[Events2] != "": # Check if the user input is not empty.
                            Configure["ODD"].update("Optical disc drive: " + ConfigurationManager.OverrideValues(os.path.normpath(UserInput2[Events2]), AdditionalValues = [["{VMPath}", VMPath]]))
                    elif Events2 in ("fda", "fdb"): # Check if any of the two floppy drive specifications were configured.
                       LetterToNumber = {"a" : 1, "b" : 2} # Specify the number variants of the letters.
                       if UserInput2[Events2] != "": # Check if the user input is not empty.
                           Configure["FD" + str(LetterToNumber[Events2[-1]])].update("Floppy drive " + str(LetterToNumber[Events2[-1]]) + ": " + ConfigurationManager.OverrideValues(os.path.normpath(UserInput2[Events2]), AdditionalValues = [["{VMPath}", VMPath]]))
                Configure.close() # Close the window, just in case it has not closed already.
            PeckerMgr.un_hide() # Show PeckerMgr again.
        elif Events == "Launch": # If the user has selected the Launch option, the following code will run.
            VMPath = os.path.normpath(VMsLocation.Get() + "/" + CurrentlySelectedVM)
            VMConfigFile = VMPath + "\config.cfg"
            if CurrentlySelectedVM == "none": LaunchAspectsOfPeckerMgr.TellUserToSelectVM() # Check if a virtual machine has not been selected.
            elif not os.path.isdir(VMPath): # Check if the directory has somehow been deleted.
                PeckerMgr.hide() # Hide PeckerMgr.
                LaunchAspectsOfPeckerMgr.CreatePopup("The directory for this virtual machine no longer exists.", "Error", 2)
            elif not os.path.isfile(VMConfigFile): # Check if the configuration file does not exist.
                PeckerMgr.hide() # Hide PeckerMgr.
                LaunchAspectsOfPeckerMgr.CreatePopup("Please check the syntax of the configuration file. CC", "Error", 2)
            else:
                # Before the VM can be ran, let's create the batch file that will be ran whenever the user would like to launch the virtual machine.
                PeckerMgr.un_hide() # Show PeckerMgr again.             
                BatchScriptToRun = """@echo off
echo This is your QEMU configuration: SCRIPTHERE
echo.
echo Reminder - the current release of QEMU has an issue with its ROMs thus the -L flag is temporarily applied onto each QEMU configuration, otherwise QEMU will not launch properly.
echo Now launching QEMU...
echo -------------------------------------------
SCRIPTHERE
echo -------------------------------------------
pause""".replace("SCRIPTHERE", ConfigurationManager.OverrideEnclosedVariables(LaunchAspectsOfPeckerMgr.ReturnBatchScriptOfConfig(VMConfigFile), AdditionalEnclosedVariables = [["{VMPath}", VMPath]])) # Create our batch script and replace the SCRIPTHERE strings with the actual command for launching QEMU with the correct arguments.
                BatchFile = VMPath + "\VMLauncher.bat" # Create a variable for the exact batch file.
                open(BatchFile, "w").write(BatchScriptToRun) # With our script ready, let's create (or modify) the batch file!
                subprocess.Popen(BatchFile) # Finally, launch the batch file!
            PeckerMgr.un_hide() # Show PeckerMgr again.
    PeckerMgr.close() # Close PeckerMgr if it hasn't been closed already.
    if Events in (framework.WIN_CLOSED, "Exit"): # If the user input for PeckerMgr was either closing the window or selecting the exit button, stop this entire loop.
        break

# Written by Quevidia #
# 2021 #
