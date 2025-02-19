total = 0
karakterliste = [7, 10, 2, 00, 4]

for x in range(0,len(karakterliste)):
    total = karakterliste[x] + total

gennemsnit = total / len(karakterliste)

print(gennemsnit)


