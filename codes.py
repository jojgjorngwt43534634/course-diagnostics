num_1 = input("")
if '+' in num_1:
    base_1 = list(num_1.split('+'))
    num2 = float(base_1[0])
    num3 = float(base_1[1])
    add = num2 + num3
    print(add)
elif '-' in num_1:
    base_1 = list(num_1.split('-'))
    num2 = float(base_1[0])
    num3 = float(base_1[1])
    sub = num2 - num3
    print(sub)
elif '*' in num_1:
    base_1 = list(num_1.split('*'))
    num2 = float(base_1[0])
    num3 = float(base_1[1])
    mul = num2 * num3
    print(mul)
elif '/' in num_1:
    base_1 = list(num_1.split('/'))
    num2 = float(base_1[0])
    num3 = float(base_1[1])
    div = num2 / num3
    print(div)