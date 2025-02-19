tal = 20
print("Gæt et tal mellem 1 og 100 ;)")
guess = int(input())

if guess == tal:
    print("Rigtigt!")
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

