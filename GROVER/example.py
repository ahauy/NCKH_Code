import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt # <--- DÒNG MỚI 1

# --- 1. Thiết lập các tham số ---
n_qubits = 3
winning_state = '101'

# --- 2. Xây dựng Oracle ... (giữ nguyên) ---
def create_oracle(circuit, n):
    circuit.x(1)
    circuit.ccz(0, 2, 1)
    circuit.x(1)

# --- 3. Xây dựng Toán tử Khuếch tán ... (giữ nguyên) ---
def create_diffuser(circuit, n):
    circuit.h(range(n))
    circuit.x(range(n))
    circuit.ccz(0, 1, 2)
    circuit.x(range(n))
    circuit.h(range(n))

# --- 4. Xây dựng mạch Grover hoàn chỉnh ... (giữ nguyên) ---
grover_circuit = QuantumCircuit(n_qubits, n_qubits)
grover_circuit.h(range(n_qubits))
grover_circuit.barrier()
num_iterations = 2
for _ in range(num_iterations):
    create_oracle(grover_circuit, n_qubits)
    grover_circuit.barrier()
    create_diffuser(grover_circuit, n_qubits)
    grover_circuit.barrier()
grover_circuit.measure(range(n_qubits), range(n_qubits))
print("Mạch Lượng tử của Thuật toán Grover:")
print(grover_circuit)

# --- 5. Mô phỏng và hiển thị kết quả ---
simulator = Aer.get_backend('aer_simulator')
compiled_circuit = transpile(grover_circuit, simulator)
result = simulator.run(compiled_circuit, shots=1024).result()
counts = result.get_counts()

print("\nKết quả đo lường:")
plot_histogram(counts, title="Kết quả tìm kiếm trạng thái |101>")

plt.show() # <--- DÒNG MỚI 2 (Ở CUỐI CÙNG)