import numpy as np
import matplotlib.pyplot as plt
from itertools import product

class CMAState:
    def __init__(self, label, amplitudes):
        self.label = label
        self.amplitudes = np.array(amplitudes, dtype=complex)
        self.curves = self._init_curves()

    def _init_curves(self):
        curves = {}
        for idx, state in enumerate(self.label):
            t = np.linspace(-1, 1, 100)
            base = np.tanh(3 * t)
            amp = np.abs(self.amplitudes[idx])
            phase = np.angle(self.amplitudes[idx])
            x = t
            y = amp * base * np.cos(phase)
            z = amp * base * np.sin(phase)
            curves[state] = (x, y, z)
        return curves

    def apply_operator(self, operator):
        self.amplitudes = operator @ self.amplitudes
        self.curves = self._init_curves()

    def decohere(self, rate=0.1):
        for i in range(len(self.amplitudes)):
            for j in range(len(self.amplitudes)):
                if i != j:
                    phase_diff = np.angle(self.amplitudes[i]) - np.angle(self.amplitudes[j])
                    decay = np.exp(-rate * np.abs(phase_diff))
                    self.amplitudes[i] *= decay
        self.curves = self._init_curves()

    def apply_correction(self, threshold=0.01):
        norm = np.linalg.norm(self.amplitudes)
        self.amplitudes = self.amplitudes / norm
        self.amplitudes[np.abs(self.amplitudes) < threshold] = 0
        self.curves = self._init_curves()

    def render(self, show_labels=True):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for state, (x, y, z) in self.curves.items():
            label = state if show_labels else ''
            ax.plot(x, y, z, label=label)
        if show_labels:
            ax.legend()
        plt.show()

    def animate_decoherence(self, steps=10, rate=0.1):
        for _ in range(steps):
            self.decohere(rate)
            self.render(show_labels=False)

    def entangle_with(self, other_state):
        combined_label = [a + b for a in self.label for b in other_state.label]
        combined_amp = np.kron(self.amplitudes, other_state.amplitudes)
        return CMAState(combined_label, combined_amp)

    @staticmethod
    def generate_labels(n_qubits):
        return [''.join(bits) for bits in product('01', repeat=n_qubits)]

    @staticmethod
    def ghz_state(n_qubits):
        label0 = '0' * n_qubits
        label1 = '1' * n_qubits
        label = [label0, label1]
        amplitudes = [1/np.sqrt(2), 1/np.sqrt(2)]
        return CMAState(label, amplitudes)

class CMAOperator:
    def __init__(self, matrix, name="Unnamed"):
        self.matrix = np.array(matrix, dtype=complex)
        self.name = name

    def __matmul__(self, state_vector):
        return self.matrix @ state_vector

class CMAAgent:
    def __init__(self, name, state):
        self.name = name
        self.memory = state

    def observe(self, other_agent):
        print(f"{self.name} observes {other_agent.name}'s curves.")
        other_agent.memory.render()

    def interact(self, other_agent):
        print(f"{self.name} interacts with {other_agent.name}, combining memories.")
        combined_amp = (self.memory.amplitudes + other_agent.memory.amplitudes) / 2
        combined_label = list(set(self.memory.label + other_agent.memory.label))
        self.memory = CMAState(combined_label, combined_amp[:len(combined_label)])
        self.memory.render()

    def entangle_with(self, other_agent):
        print(f"{self.name} entangles with {other_agent.name}, forming joint memory.")
        self.memory = self.memory.entangle_with(other_agent.memory)
        self.memory.render()

# Built-in operators
H = CMAOperator((1/np.sqrt(2)) * np.array([[1, 1], [1, -1]]), name="Hadamard")
X = CMAOperator(np.array([[0, 1], [1, 0]]), name="Pauli-X")
Z = CMAOperator(np.array([[1, 0], [0, -1]]), name="Pauli-Z")

# CNOT for 2 qubits (|00>, |01>, |10>, |11>)
CNOT_2Q = CMAOperator(np.array([
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1],
    [0, 0, 1, 0]
]), name="CNOT")

# Create agents with GHZ states
agent_A = CMAAgent("Agent_A", CMAState.ghz_state(3))
agent_B = CMAAgent("Agent_B", CMAState.ghz_state(3))

# Interaction and entanglement demonstration
agent_A.memory.animate_decoherence(steps=3, rate=0.2)
agent_A.memory.apply_correction(threshold=0.05)
agent_A.interact(agent_B)
agent_A.entangle_with(agent_B)
