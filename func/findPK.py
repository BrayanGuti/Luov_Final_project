import numpy as np

def findPk1(k, Q1, v, m):
  matrix_Pk1 = np.zeros((v, v))
  column = 0

  for i in range(v):
    for j in range(i, v):
      matrix_Pk1[i][j] = Q1[k, column]
      column += 1
    column += m
  
  return(matrix_Pk1)

def findPk2(k, Q1, v, m):
  matrix_Pk2 = np.zeros((v, m))
  column = 1

  for i in range(1, v + 1):
    column += v - i + 1  # Salto en columnas debido al término cuadrático
    for j in range(1, m + 1):
      matrix_Pk2[i - 1][j - 1] = Q1[k, column - 1]
      column += 1
  return(matrix_Pk2)

