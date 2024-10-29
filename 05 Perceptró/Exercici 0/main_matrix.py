#!/usr/bin/env python3

from perceptron import initialize_weights, train, test_accuracy

def generate_all_matrices():
    matrices = []
    for i in range(512):
        binary = format(i, '09b')
        matrix = [int(bit) for bit in binary]
        matrices.append(matrix)
    return matrices

def is_diagonal(matrix):
    diagonals = [
        [1, 0, 0, 0, 1, 0, 0, 0, 1],  
        [0, 0, 1, 0, 1, 0, 1, 0, 0]   
    ]
    return 1 if matrix in diagonals else 0

def is_vertical(matrix):
    for col in range(3):
        if matrix[col] == 1 and matrix[col + 3] == 1 and matrix[col + 6] == 1:
            return 1  
    return 0  

def is_horizontal(matrix):
    for row in range(0, 9, 3):
        if matrix[row] == 1 and matrix[row + 1] == 1 and matrix[row + 2] == 1:
            return 1  
    return 0  

# trys
EPOCHS = 10
LEARNING_RATE = 0.1
INPUT_SIZE = 9

matrices = generate_all_matrices()
labels_diagonal = [is_diagonal(matrix) for matrix in matrices]
labels_vertical = [is_vertical(matrix) for matrix in matrices]
labels_horizontal = [is_horizontal(matrix) for matrix in matrices]

weights_diagonal = initialize_weights(INPUT_SIZE)
bias_diagonal = 0.0
weights_vertical = initialize_weights(INPUT_SIZE)
bias_vertical = 0.0
weights_horizontal = initialize_weights(INPUT_SIZE)
bias_horizontal = 0.0

for epoch in range(EPOCHS + 1):
    print(f"\nEpoch {epoch}")

    weights_diagonal, bias_diagonal = train(weights_diagonal, bias_diagonal, matrices, labels_diagonal, LEARNING_RATE, epoch)
    weights_vertical, bias_vertical = train(weights_vertical, bias_vertical, matrices, labels_vertical, LEARNING_RATE, epoch)
    weights_horizontal, bias_horizontal = train(weights_horizontal, bias_horizontal, matrices, labels_horizontal, LEARNING_RATE, epoch)
    accuracy_diagonal = test_accuracy(weights_diagonal, bias_diagonal, matrices, labels_diagonal)
    accuracy_vertical = test_accuracy(weights_vertical, bias_vertical, matrices, labels_vertical)
    accuracy_horizontal = test_accuracy(weights_horizontal, bias_horizontal, matrices, labels_horizontal)
    
    print(f"Accuracy (Diagonal): {accuracy_diagonal:.2f}%")
    print(f"Accuracy (Vertical): {accuracy_vertical:.2f}%")
    print(f"Accuracy (Horizontal): {accuracy_horizontal:.2f}%")

    if accuracy_diagonal > 80 and accuracy_vertical > 80 and accuracy_horizontal > 80:
        print(f"Todos los perceptrones alcanzaron más del 80% de precisión en la época {epoch}.")
        break
    elif accuracy_diagonal > 50 and accuracy_vertical > 50 and accuracy_horizontal > 50:
        print(f"Todos los perceptrones alcanzaron más del 50% de precisión en la época {epoch}.")
