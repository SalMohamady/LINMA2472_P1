file1 = open('JurassicPark.txt', 'r')
Lines = file1.readlines()

listOfScenes = []

for line in Lines:
    if (line[0].isnumeric()):
        listOfScenes.append(line)

print(listOfScenes)
print("\n")
print(len(listOfScenes))
