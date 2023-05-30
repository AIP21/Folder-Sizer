import os
import threading
import sys

canSendNotifications = True

try:
     from plyer import notification
except:
     print("plyer is not installed. This program will still function but will not be able to send notifications when it is finished.")
     canSendNotifications = False

args = sys.argv

verbose = False
shouldNotify = True

for arg in args:
    if "verbose" == arg or "v" == arg:
        verbose = True
        print("Verbose is true")
    
    if "silent" == arg or "s" == arg:
        shouldNotify = False
        print("Silent is true")

# Get input
inputFolder = input("Enter the path of the folder to scan: ")
directorySizes = []
totalSize = 0
errors = 0
dirsLength = 0
curDirInd = 0
dirsScanned = []

def sizeString(size):
    if size == 0:
        return "empty"
    elif size >= 500000000:
        Gb = size / 1000000000
        return str(Gb) + " Gb"
    elif size >= 750000:
        Mb = size / 1000000
        return str(Mb) + " Mb"
    elif size >= 1000:
        Kb = size / 1000
        return str(Kb) + " Kb"
    else:
        return str(size) + " bytes"

# Scan a folder
def scan(rootDir, dir):
    global directorySizes, errors, verbose, dirsLength, curDirInd
    
    print("Starting to calculate size for " + dir)
    
    size = 0
        
    try:
        for root, dirs, files in os.walk(os.path.join(rootDir, dir)):
            try:
                for file in files:
                    pth = os.path.join(root, file)
                    thisSize = os.path.getsize(pth)
                    
                    if verbose:
                        print("<VERBOSE>      Scanning: '" + str(pth) + "'")
                    
                    size += thisSize
            except:
                errors += 1
                pass
    except:
        errors += 1
        pass
    
    directorySizes.append((dir, size))
    
    percentStr = "(" + str(round((curDirInd / dirsLength) * 100, 3)) + "%)"
    
    spaceCount = 10 - len(percentStr)
    
    for s in range(spaceCount):
         percentStr += " "
    
    print(percentStr + "Finished calculating size for '" + str(dir) + "' with size: " + sizeString(size))
    
    curDirInd += 1

# Calcualate sizes for each first-level subfolder of the inputted folder
def scanFolder(folder):
    global directorySizes, totalSize, errors, dirsLength, curDirInd, dirsScanned
    
    if folder not in dirsScanned:
         dirsScanned.append(folder)
    
    totalSize = 0
    errors = 0
    
    curDirInd = 0

    directorySizes = []

    print("")
    print("Calculating directory sizes for " + folder)
    print("")
        
    dirsToScan = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    
    dirsLength = len(dirsToScan)
    
    scanThreads = []
    
    # Create and start scan threads
    for dir in dirsToScan:
        thread = threading.Thread(target = scan, args = [folder, dir])
        thread.start()
        scanThreads.append(thread)
    
    # Join every scan thread
    for thread in scanThreads:
        thread.join()
    
    print("")
    print("Finished calculating directory sizes for the target folder with " + str(errors) + " error(s)")
    print("")
    
    # Sort
    directorySizes.sort(key = lambda x: x[1], reverse = True)
        
    print("----------------------")
    print("")

    # Print out finished list
    index = 0
    totalSize = 0
    printed = ""
    topPrint = ""
    
    for directoryAndSize in directorySizes:
        index += 1
        
        indStr = str(index) + "."
        
        spaceCount = (len(str(dirsLength)) + 1) - len(indStr)
        
        for s in range(spaceCount):
            indStr += " "
        
        toPrint = indStr + " '" + str(directoryAndSize[0]) + "' = " + sizeString(directoryAndSize[1])
        
        totalSize += directoryAndSize[1]
        
        printed += toPrint + "\n"
    
    topPrint += "Total size of all directories in '" + str(folder) + "' = " + sizeString(totalSize) + "\n"
    topPrint += "\n"
    topPrint += "Directories of '" + str(folder) + "' sorted by size:\n"
    
    printed = topPrint + printed

    print(printed)

    # Save to file
    print("----------------------")
    print("")

    print("Saving the list to a file...")
    print("")
    
    thisDir = os.path.dirname(os.path.realpath(__file__))
    
    if "\\" not in folder and "/" not in folder:
        colonInd = folder.index(":")
        folderName = folder[0 : colonInd]
    else:
        newFolder = str(folder)
        
        # Accomodate for having an empty \ at the end of the folder name
        if folder.rfind('\\') == len(folder) - 1:
            newFolder = folder[0 : len(folder) - 1]
        
        split = newFolder .split("\\")
        folderName = split[len(split) - 1]
    
    fileName = os.path.join(folderName, thisDir + "/folderSizes-" + folderName + ".txt")
    
    with open(fileName , "w") as file:
        file.write(printed)
        
        file.close()
    
    # Alert the user that we're done    
    global shouldNotify, canSendNotifications
    
    if shouldNotify:
        if canSendNotifications:
             notificationTitle = "Scanning of directory '" + str(folderName) + "' is complete!"
                 
             # Limit characters to prevent notification error
             notificationTitle = notificationTitle[0 : 64]
            
             notification.notify(app_name = "Folder Sizer", title = notificationTitle, message = "The list of directory sizes is printed to the console and saved to a file. Check the console for the path to the saved file.")
        else:
             print("\a")
    
    print("Finished saving the list to: " + str(fileName))

if inputFolder == None or inputFolder == "" or (not os.path.exists(inputFolder)) or (not os.path.isdir(inputFolder)):
    print("The path you entered is invalid, try again")
else:
    scanFolder(inputFolder)

done = False

while not done:
    print("")

    inStr = input("Type 'Quit', 'quit', or 'q' to close the program, 'Rescan', 'rescan', or 'r' to rescan the current directory, 'Open', 'open', or 'o' to open the current directory in explorer, 'Back', 'back', or 'b' to rescan the last directory, the path of a new directory to scan, or the index of the listed directory you want to scan next: ")
    
    if inStr == "Quit" or inStr == "quit" or inStr == "q":
        done = True
    elif inStr == "Open" or inStr == "open" or inStr == "o":
        os.system("explorer " + inputFolder)
    elif inStr == "Rescan" or inStr == "rescan" or inStr == "r":
        scanFolder(inputFolder)
    elif inStr == "Back" or inStr == "back" or inStr == "b":
        scannedLength = len(dirsScanned)
        if scannedLength > 1:
             lastDir = dirsScanned[scannedLength - 2]
             dirsScanned.pop()
             scanFolder(lastDir)
        else:
             print("There are no prior directories.")
             continue;
    elif inStr.isdigit():
        # Accomodate for having an empty \ at the end of the folder name
        if inputFolder.rfind('\\') == len(inputFolder) - 1:
            inputFolder = inputFolder[0 : len(inputFolder) - 1]
        
        if int(inStr) - 1 >= len(directorySizes):
            print("Given index is out of range, try again.")
            continue
    
        dirName = directorySizes[int(inStr) - 1][0]
        inputFolder += "\\" + dirName
        scanFolder(inputFolder)
    else:
        if inStr == "" or (not os.path.exists(inStr)) or (not os.path.isdir(inStr)):
            print("The path you entered is invalid, try again")
            continue
        else:
            inputFolder = inStr
            scanFolder(inputFolder)