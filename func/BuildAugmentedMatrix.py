import numpy as np

def BuildAugmentedMatrix(C, L, Q1, T, h, v, m, n, r=8):
    """
    Builds the augmented matrix for the linear system F(v||o) = h after fixing the vinegar variables.

    Args:
        C (np.ndarray): Array of shape (m, 1), dtype=np.uint8
        L (np.ndarray): Array of shape (m, n), dtype=np.uint8
        Q1 (np.ndarray): Array of shape (m, (v * (v + 1)) // 2 + (v * m)), dtype=np.uint8
        T (np.ndarray): Array of shape (v, m), dtype=np.uint8 (bits only)
        h (np.ndarray): Array of shape (m, 1), dtype=np.uint8
        v (np.ndarray): Array of shape (v, 1), dtype=np.uint8
        m (int): Number of rows in the system.
        n (int): Number of columns in L.
        r (int): Bit-length of each field element (default is 8).

    Returns:
        np.ndarray: Augmented matrix of shape (m, m + n + 1), dtype=np.uint8.
    """
    # Initialize RHS and LHS
    RHS = np.zeros((m, 1), dtype=np.uint8)
    LHS = np.zeros((m, m + n + 1), dtype=np.uint8)

    # Step 1: Compute RHS = h - C - L @ (v || 0)^T
    v_padded = np.vstack((v, np.zeros((n, 1), dtype=np.uint8)))  # v || 0
    RHS = (h - C - (L @ v_padded.T) % 256) % 256  # Ensure values fit in 8 bits

    # Step 2: Compute LHS = L @ [-T^T | I_m]
    LHS[:, :v.shape[0]] = (L @ (-T.T % 256)) % 256  # First part: L * -T^T
    LHS[:, v.shape[0]:v.shape[0] + m] = np.eye(m, dtype=np.uint8)  # Identity matrix

    # Loop over rows of the system
    for k in range(m):
        # Step 3: Compute P_k,1 = findPk1(k, Q1) (quadratic terms in v)
        Pk1 = Q1[k, :v.shape[0]]  # Assuming the first v elements are for quadratic terms

        # Step 4: Compute P_k,2 = findPk2(k, Q1) (bilinear terms in v and o)
        Pk2 = Q1[k, v.shape[0]:]  # Remaining terms in Q1 for bilinear terms

        # Step 5: Compute RHS[k] = RHS[k] - v^T P_k,1 v
        vT_Pk1_v = (v.T @ Pk1 @ v) % 256
        RHS[k] = (RHS[k] - vT_Pk1_v) % 256

        # Step 6: Compute F_k,2 = -(P_k,1 @ T.T + P_k,2)
        Fk2 = -(Pk1 @ T.T + Pk2) % 256

        # Step 7: Insert F_k,2 into LHS[k]
        LHS[k, v.shape[0]:v.shape[0] + Fk2.shape[0]] = Fk2

    # Step 8: Insert RHS into LHS
    LHS[:, -1] = RHS.flatten()

    return LHS
