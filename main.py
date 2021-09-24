import random
import os
import sys

a = []
b = []
last = []
flag_count = 0
def gen():
    global a
    global b
    global flag_count
    choose = input("Would you like to load you're safe? y/n ")
    if choose == 'y':
        name = input("What's your name? ")
        try:
            with open(f"{name}1.txt", 'r') as f:
                x = f.readlines()
                for i in x:
                    a.append(list(map(ord, i.split())))
                n = len(a)
            with open(f'{name}2.txt', 'r') as f:
                x = f.readlines()
                for i in x:
                    b.append(i.split())
        except Exception:
            print("Sorry couldn't load it")
            return
    else:
        n, bomb = map(int, input("Type in size and amount of bombs (n bomb) (less than n*n)\n").split())
        even = [i for i in range(1040, 1103, 2)]
        odd = [i for i in range(1041, 1103, 2)]
        a = [[random.choice(even) for i in range(n)] for i in range(n)]
        b = [['[?]' for i in range(n)] for i in range(n)]
        if bomb > n * n: bomb = n*n - 1
        os.system("CLS")
        b2 = []
        for x in range(n):
            for y in range(n):
                b2.append((x,y))
        for i in range(bomb):
            x = random.choice(b2)
            b2.pop(b2.index(x))
            a[x[0]][x[1]] = random.choice(odd)
    for i in b:
        for j in i:
            print(j, end=' ')
        print()
            
    while True:
        if win(b):
            print("You've won")
            break
        elif win(b) == None:
            print("You're cheating!")
            os.remove(f'{name}1.txt')
            os.remove(f'{name}2.txt')
            break
        try:
            com = input("(X Y Action)\nOpen - Open the spot \nFlag- put flag \nSave - save session\n").split()
            y_coord = int(com[0]) - 1 
            x_coord = int(com[1]) - 1
            os.system("CLS")
            if x_coord < 0 or x_coord > n - 1 or y_coord < 0 or y_coord > n - 1:
                print("X and Y should be less than size of grid.")
                for i in b:
                    for j in i:
                        print(j, end=' ')
                    print()
                continue
            com = com[2]
        except Exception:
                os.system("CLS")
                print('Sorry try again')
                for i in b:
                    for j in i:
                        print(j, end=' ')
                    print()
                continue
        if com == "Open":
            if b[x_coord][y_coord] == '[!]':
                print("You've put flag there")
                for i in b:
                    for j in i:
                        print(j, end=' ')
                    print()
                continue
            elif b[x_coord][y_coord] != '[?]':
                print("You've already checked this spot.")
                for i in b:
                    for j in i:
                        print(j, end=' ')
                    print()
                continue
            guessing = guess(x_coord, y_coord)
            if guessing == "You've lost":
                print(guessing)
                break
            else:
                if guessing > 0:
                    b[x_coord][y_coord] = "[" + str(guessing) + ']'
                else:
                    dfs(x_coord, y_coord)
            for i in b:
                for j in i:
                    print(j, end=' ')
                print()
        if com == "Flag":
            if b[x_coord][y_coord] == '[!]':
                ans = input("You sure you want to remove flag? y/n \n")
                if ans == 'y':
                    b[x_coord][y_coord] = '[?]'
                    flag_count -= 1
                    os.system("CLS")
                elif ans == 'n':
                    os.system("CLS")
                else:
                    os.system("CLS")
                    print("Sorry couldn't understand you")
            elif b[x_coord][y_coord] != '[?]':
                print("Cant place flag here")
            elif b[x_coord][y_coord] == '[?]':
                if flag_count == bomb:
                    print("Too many flags! You can replace flags by typing the same command.")
                else:
                    flag_count += 1
                    b[x_coord][y_coord] = '[!]'
            for i in b:
                for j in i:
                    print(j, end=' ')
                print()
        elif com == "Save":
            name = input('Whats your name?: ')
            for i in b:
                for j in i:
                    print(j, end=' ')
                print()
            with open(f'{name}1.txt', 'w') as f:
                for i in a:
                    f.write(' '.join(list(map(chr, i)) ) + '\n')
            with open(f'{name}2.txt', 'w') as f:
                for i in b:
                    f.write(' '.join(list(map(str, i))) + '\n')
        else:
            os.system("CLS")
            for i in b:
                for j in i:
                    print(j, end=' ')
                print()
            continue
    for i in see(a):
        print(' '.join(i))
    print()
    input("Press Enter to proceed.")

def win(vec):
    global a
    
    V = True
    for i in vec:
        if i.count('[?]') != 0:
            V = False
    if V and vec != see(a, 2):
        return None
    if vec != see(a, 2): return False
    return True


def see(a, n=1):
    d = []
    for i in range(len(a)):
        d1 = []
        for j in range(len(a[i])):
            x = 0
            
            for x1 in range(-1, 2):
                for y1 in range(-1, 2):
                    if i + x1 < 0 or j + y1 < 0 or i + x1 >= len(a) or j + y1 >= len(a):
                        continue
                    if x1 == 0 and y1 == 0:
                        continue
                    if (a[i + x1][j + y1]) % 2 == 1:
                        x += 1
            if a[i][j] % 2 == 1:
                if n == 2:
                    x = '!'
                if n == 1:
                    x = 'B'
            d1.append(f"[{x}]")
        d.append(d1)
    return d

def see_one(a, x, y):
        x2 = 0
        if a[x][y] % 2 == 1:
            return 'B'
        for x1 in range(-1, 2):
            for y1 in range(-1, 2):
                if x + x1 < 0 or y + y1 < 0 or x + x1 >= len(a) or y + y1 >= len(a):
                    continue
                if x1 == 0 and y1 == 0:
                    continue
                if (a[x + x1][y + y1]) % 2 == 1:
                    x2 += 1
        return x2
def guess(x, y):
    global a
    x3 = see_one(a, x, y)
    if x3 == 'B':
        return "You've lost"
    else:
        return x3

def dfs(x, y):
    global b
    global a
    global last
    check = see_one(a, x, y)
    last += [(x, y)]
    if check == None:
        return
    if  check == 0:
        b[x][y] = '[0]'
        for x1 in range(-1, 2):
            for y1 in range(-1, 2):
                if x1 != 0 and y1 != 0:
                    continue
                if x + x1 < 0 or y + y1 < 0 or x + x1 >= len(a) or y + y1 >= len(a):
                    continue
                if (x + x1, y + y1) in last:
                    continue
                if x1 == 0 and y1 == 0:
                    continue
                dfs(x + x1, y + y1)
    else:
        if check != 'B':
            b[x][y] = f"[{check}]"
        return
                    
   
gen()