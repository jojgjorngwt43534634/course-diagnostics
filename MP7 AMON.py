matrix_c = [[0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]]

while True:
    try:
        matrix_a = []
        matrix_b = []

        for i in range(1, 10):
            prompt = f"Enter a{i}: " 
            element = int(input(prompt))
            matrix_a.append(element)
    
        for i in range(1, 10):
            promptS = f"Enter b{i}: " 
            elementS = int(input(promptS))
            matrix_b.append(elementS)
        break
    
    except(ValueError):
        print('Put a real a Number')

for c in range(3):
    for k in range(3):
        for m in range(3):
            index_a = c * 3 + k
            index_b = k * 3 + m
            matrix_c[c][m] += matrix_a[index_a] * matrix_b[index_b]

print('\nMatrix A')
for r in range(3):
    for c in range(3):
        index = r * 3 + c
        print(matrix_a[index], end = "  ")
    print()
    
print('\nMatrix B')
for r in range(3):
    for c in range(3):
        index = r * 3 + c
        print(matrix_b[index] , end = "  ")
    print()
    
print('\nMatrix C')
for r in range(3):
    for c in range(3):
        index = r * 3 + c
        print(matrix_c[r][c] , end = "\t")
    print()
    
