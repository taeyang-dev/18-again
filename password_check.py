password = input("Enter password: ")

Ucase = 0
Lcase = 0
digit = 0
other = 0

for char in password:
    if char.isupper():
        Ucase += 1
    elif char.islower():
        Lcase += 1
    elif char.isdigit():
        digit += 1
    else:
        other += 1

if Ucase > 0 and Lcase > 0 and digit > 0 and Ucase + Lcase + digit + other > 7:
    print("Strong password")
else:
    print("Weak password")