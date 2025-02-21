import random

while True:
    tal = random.randint(1, 100)
    print(tal)
    forsøg = 0
    print("Gæt et tal mellem 1 og 100 ;)")

    while True:
        guess = int(input())
        forsøg += 1
        print("Det er dit forsøg nr, ", forsøg)
        if guess == tal:
            print(f"Rigtigt! Du gættede det på {forsøg} forsøg.")
            break
        elif guess < 1 or guess > 100:
            print("Uden for den angivne interval på 1-100")
        else:
            difference = abs(guess - tal)
            if difference > 50:
                print("Meget langt forbi")
            elif 19 < difference <= 49:
                print("Du er ikke helt ved siden af")
            else:
                print("Tampen brænder!")
        if forsøg == 10:
            print("Du har ikke flere forsøg")
            break

    igen = input("Vil du prøve igen? (y/n): ").lower()
    if igen != "y":
        print("Farvel!")
        break