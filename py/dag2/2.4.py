from random import randint

alder = randint(-100,200)
if alder <= 0 or alder >= 130:
    print("Ugyldig alder")
elif alder < 18:
    print("Du får ungdomsrabat")
elif 18 <= alder <= 65:
    print("Du får ingen rabat")
else:
    print("Du får pensionistrabat")
print(alder)