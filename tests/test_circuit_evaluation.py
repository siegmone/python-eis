from eis.circuits import Circuit, imp_C


def test_basic_circuit():
    circuit = Circuit("R | R")  # component default value parameter is 1
    circuit_imp = circuit.evaluate(1)  # evaluate is at a default frequency of 1
    assert circuit_imp == 0.5


def test_rc_cell():
    circuit = Circuit("R - C | R")
    circuit.set_component("R1", 10)
    circuit.set_component("C1", 5)
    circuit.set_component("R2", 2)
    circuit_imp = circuit.evaluate(1)
    cmp_imp = 10 + (1 / (1 / imp_C(1, 5) + 1 / 2))
    assert circuit_imp == cmp_imp
