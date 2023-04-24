import os

# Get input
inputFolder = input("Enter the path of the folder to scan: ")
directorySizes = []

# Calcualate sizes for 
def scanFolder(folder):
    global directorySizes
    
    directorySizes = []

    print("")
    print("Calculating directory sizes for " + folder)
    print("")

    split = folder.split("\\")
    folderName = split[len(split) - 1]
    
    dirsToScan = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
    
    errors = 0
    for dir in dirsToScan:
        print("Calculating size for: " + dir)
        
        size = 0
        
        try:
            for root, dirs, files in os.walk(os.path.join(folder, dir)):
                try:
                    for file in files:
                        size += os.path.getsize(os.path.join(root, file))
                except:
                    errors += 1
                    pass
        except:
            errors += 1
            pass
        
        directorySizes.append((dir, size))
    
    print("")
    print("Finished calculating directory sizes for the target folder with " + str(errors) + " error(s)")
    print("")
    
    # Sort
    directorySizes.sort(key = lambda x: x[1], reverse = True)
    
    print("")
    print("Sorted the folder by size")
    print("")
    print("")
    
    # Print out finished list
    index = 0
    printed = ""
    for directoryAndSize in directorySizes:
        index += 1
        
        toPrint = ""
        if directoryAndSize[1] == 0:
            toPrint = str(index) + ". '" + directoryAndSize[0] + "' is empty"
        elif directoryAndSize[1] >= 500000000:
            Gb = directoryAndSize[1] / 1000000000
            toPrint = str(index) + ". '" + directoryAndSize[0] + "' = " + str(Gb) + " Gb"
        elif directoryAndSize[1] >= 750000:
            Mb = directoryAndSize[1] / 1000000
            toPrint = str(index) + ". '" + directoryAndSize[0] + "' = " + str(Mb) + " Mb"
        elif directoryAndSize[1] >= 1000:
            Kb = directoryAndSize[1] / 1000
            toPrint = str(index) + ". '" + directoryAndSize[0] + "' = " + str(Kb) + " Kb"
        else:
            toPrint = str(index) + ". '" + directoryAndSize[0] + "' = " + str(directoryAndSize[1]) + " bytes"
        
        print(toPrint)
        printed += "\n" + toPrint

    # Save to file
    print("")
    print("")
    print("Saving the list to a file...")
    print("")
    
    thisDir = os.path.dirname(os.path.realpath(__file__))
    
    with open(os.path.join(folderName, thisDir + "/folderSizes-" + folderName + ".txt"), "w") as file:
        file.write(printed)
        
        file.close()
    
    print("Finished saving the list to a file")

if inputFolder == "" or (not os.path.exists(inputFolder)) or (not os.path.isdir(inputFolder)):
    print("The path you entered is invalid, try again")
else:
    scanFolder(inputFolder)

done = False

while not done:
    inStr = input("Type 'Quit' to finish, 'Open' to open the current directory in explorer, the path of a new directory, or type the index of the listed directory you want to scan next: ")
    
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