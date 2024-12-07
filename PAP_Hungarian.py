import numpy as np

def subtract_row_min(matrix):
    """Langkah 1: Kurangi nilai minimum dari setiap baris."""
    for i in range(len(matrix)):
        min_val = min(matrix[i])
        matrix[i] -= min_val
def subtract_col_min(matrix):
    """Langkah 2: Kurangi nilai minimum dari setiap kolom."""
    for j in range(len(matrix[0])):
        min_val = min(matrix[:, j])
        matrix[:, j] -= min_val

def cover_zeros(matrix):
    """Menentukan jumlah garis minimum yang diperlukan untuk menutupi semua nol."""
    covered_rows = [False] * len(matrix)
    covered_cols = [False] * len(matrix[0])
    lines = 0

    # Menutup baris dan kolom yang memiliki nol
    while True:
        row = col = -1
        for i in range(len(matrix)):
            if not covered_rows[i]:
                for j in range(len(matrix[0])):
                    if matrix[i][j] == 0 and not covered_cols[j]:
                        row = i
                        col = j
                        break
                if row != -1:
                    break
        if row == -1:
            break
        covered_rows[row] = True
        covered_cols[col] = True
        lines += 1
    return lines, covered_rows, covered_cols

def create_zeros(matrix):
    """Langkah 4: Buat lebih banyak nol dengan mengubah matriks."""
    # Menemukan nilai terkecil yang tidak tertutup
    min_val = np.inf
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                min_val = min(min_val, matrix[i][j])

    # Mengurangi nilai terkecil dari elemen yang tidak tertutup dan menambahkannya ke elemen yang tertutup dua kali
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > 0:
                matrix[i][j] -= min_val
            elif matrix[i][j] == 0:
                matrix[i][j] += min_val

def hungarian_algorithm(cost_matrix):
    """Implementasi algoritma Hungarian untuk mendapatkan penugasan optimal."""
    matrix = np.array(cost_matrix, dtype=int)
    n = len(matrix)

    # Langkah 1: Kurangi nilai minimum setiap baris
    subtract_row_min(matrix)

    # Langkah 2: Kurangi nilai minimum setiap kolom
    subtract_col_min(matrix)

    # Langkah 3: Tutup semua nol dengan garis minimal
    lines, covered_rows, covered_cols = cover_zeros(matrix)

    # Langkah 4: Buat nol tambahan jika jumlah garis kurang dari n
    while lines < n:
        create_zeros(matrix)
        lines, covered_rows, covered_cols = cover_zeros(matrix)

    # Langkah 5: Cari penugasan optimal
    assigned_jobs = [-1] * n
    assigned_workers = [-1] * n

    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 0 and assigned_workers[j] == -1:
                assigned_jobs[i] = j
                assigned_workers[j] = i
                break

    return assigned_jobs, matrix

# Matriks biaya
cost_matrix = [
    [89, 94, 28, 78],
    [30, 25, 83, 74],
    [67, 75, 59, 61],
    [29, 41, 76, 44]
]

# Menjalankan algoritma Hungarian
assigned_jobs, final_matrix = hungarian_algorithm(cost_matrix)

# Menampilkan hasil penugasan optimal dan total biaya
print("Penugasan Optimal:")
total_cost = 0
for worker, job in enumerate(assigned_jobs):
    cost = cost_matrix[worker][job]
    print(f"Worker {worker + 1} -> Job {job + 1} (Cost: {cost})")
    total_cost += cost

print(f"Total Cost: {total_cost}")
