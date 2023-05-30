import os
import threading
import sys

args = sys.argv

verbose = False

if "verbose" in args:
    verbose = True

for arg in args:
    if "verbose" in arg or "v" in arg:
        verbose = True

# Get input
inputFolder = input("Enter the path of the folder to scan: ")
directorySizes = []
totalSize = 0
errors = 0

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
    global directorySizes, errors, verbose
    
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
    
    print("Finished calculating size for '" + str(dir) + "' with size: " + sizeString(size))

# Calcualate sizes for each first-level subfolder of the inputted folder
def scanFolder(folder):
    global directorySizes, totalSize, errors
    
    totalSize = 0
    errors = 0

    directorySizes = []

    print("")
    print("Calculating directory sizes for " + folder)
    print("")
        
    dirsToScan = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    
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
        
        toPrint = str(index) + ". '" + str(directoryAndSize[0]) + "' = " + sizeString(directoryAndSize[1])
        
        totalSize += directoryAndSize[1]
        
        printed += toPrint + "\n"
    
    topPrint += "Total size of '" + str(folder) + "' = " + sizeString(totalSize) + "\n"
    topPrint += "\n"
    topPrint += "Directories of ' " + str(folder) + "' sorted by size:\n"
    
    printed = topPrint + printed

    print(printed)

    # Save to file
    print("----------------------")
    print("")

    print("Saving the list to a file...")
    print("")
    
    thisDir = os.path.dirname(os.path.realpath(__file__))
    
    if ":" in folder:
        colonInd = folder.index(":")
        folderName = folder[0 : colonInd]
    else:
        split = folder.split("\\")
        folderName = split[len(split) - 1]
    
    with open(os.path.join(folderName, thisDir + "/folderSizes-" + folderName + ".txt"), "w") as file:
        file.write(printed)
        
        file.close()
    
    print("Finished saving the list to a file")

if inputFolder == None or inputFolder == "" or (not os.path.exists(inputFolder)) or (not os.path.isdir(inputFolder)):
    print("The path you entered is invalid, try again")
else:
    scanFolder(inputFolder)

done = False

while not done:
    print("")

    inStr = input("Type 'Quit', 'quit', or 'q' to close the program, 'Open', 'open', or 'o' to open the current directory in explorer, the path of a new directory to scan, or the index of the listed directory you want to scan next: ")
    
    if inStr == "Quit" or inStr == "quit" or inStr == "q":
        done = True
    elif inStr == "Open" or inStr == "open" or inStr == "o":
        os.system("explorer " + inputFolder)
    elif inStr.isdigit():
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