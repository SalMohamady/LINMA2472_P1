file1 = open('JurassicPark.txt', 'r')
Lines = file1.readlines()

listOfScenes = []
ListOfcharacters = []
ListOfcharactersInScene = []

acceptedCh = ["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]


for line in Lines:
    isAname=1
    if line == " \n" or line == "\n" or line == "  \n" :
        continue
    for ch in line:
        if ch == "\n" or ch == " ":
            continue
        elif not(ch in (acceptedCh)):
            isAname=0
            break
    if (isAname == 1):
        if not (line.strip() in ListOfcharacters):
            ListOfcharacters.append(line.strip())
    


print(ListOfcharacters)
print("\n")
print(len(ListOfcharacters))
