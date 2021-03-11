n = int(input())
spaces = 0
for i in range(n):
    if i == 0:
        print("+", end="")
    print("-+\n" + " "*spaces + "| |\n" + " "*spaces + "+-+", end="")
    spaces += 2
print()
    
