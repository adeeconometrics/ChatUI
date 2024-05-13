def multiply_matrices(A, B):
    # Get the dimensions of the matrices
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Check if the matrices can be multiplied
    if cols_A != rows_B:
        raise ValueError("Matrices cannot be multiplied")

    # Create a result matrix with dimensions (rows_A x cols_B)
    C = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Perform the multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):  # or len(A[0])
                C[i][j] += A[i][k] * B[k][j]

    return C


if __name__ == "__main__":
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print(multiply_matrices(A, B))  # Output: [[19, 22], [43, 50]]