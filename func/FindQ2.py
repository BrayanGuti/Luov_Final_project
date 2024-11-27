from func.findPK import findPk1, findPk2
import numpy as np

def findQ2(Q1, T, m, v):
  Q2_length = (m * (m + 1)) // 2
  Q2 = np.zeros((m, Q2_length))

  for k in range(m):
    matrix_Pk1 = findPk1(k, Q1, v, m)
    matrix_Pk2 = findPk2(k, Q1, v, m)

    # Asegurarse de que las matrices sean binarias antes de operar
    matrix_Pk1 = matrix_Pk1 % 2
    matrix_Pk2 = matrix_Pk2 % 2
    T = T % 2
    
    # Calcular Pk3 con operaciones módulo 2
    matrix_Pk3 = (-np.matmul(np.matmul(T.T, matrix_Pk1), T) + np.matmul(T.T, matrix_Pk2)) % 2
    
    column = 0
    for i in range(m):
      Q2[k, column] = matrix_Pk3[i, i]  # Diagonal principal
      column += 1
      
      for j in range(i + 1, m):
        Q2[k, column] = (matrix_Pk3[i, j] + matrix_Pk3[j, i]) % 2  # Reducir suma módulo 2
        column += 1
        
  return Q2