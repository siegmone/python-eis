from shunting_yard import ShuntingYard, TokenType, ComponentType, Token
from math import pi
from numpy import sqrt

def imp_C(f, C):
    return 1 / (1j * 2 * pi * f * C)


def imp_L(f, L):
    return 1j * 2 * pi * f * L


def imp_Q(f, Q, a):
    return Q / (1j * 2 * pi * f) ** a


def imp_W(f, W):
    return (W / sqrt(2 * pi * f)) + (W / (1j * sqrt(2 * pi * f)))


def series(*args):
    return sum(args)


def parallel(*args):
    return 1 / sum(1 / arg for arg in args)


class Circuit:
    def __init__(self, circuit: str):
        self.circuit = circuit
        self.circuit_rpn = ShuntingYard().run(circuit)
        self.components = []
        for token in self.circuit_rpn:
            if token.token_type == TokenType.COMPONENT:
                setattr(self, token.literal, 1)
                self.components.append(token.literal)
        self.impedance = 0

    def set_component(self, component: str, value: float):
        if component not in self.components:
            raise Exception(f"Component {component} not found in circuit")
        setattr(self, component, value)

    def set_components(self, **kwargs):
        for component, value in kwargs.items():
            self.set_component(component, value)

    def evaluate_component(self, token: Token, frequency: float):
        match token.opt:
            case ComponentType.R:
                # return imp_R(frequency, getattr(self, token.literal))
                return getattr(self, token.literal)
            case ComponentType.C:
                return imp_C(frequency, getattr(self, token.literal))
            case ComponentType.L:
                return imp_L(frequency, getattr(self, token.literal))
            case ComponentType.Q:
                return imp_Q(frequency, getattr(self, token.literal))
            case ComponentType.W:
                return imp_W(frequency, getattr(self, token.literal))

    def evaluate(self, frequency: float = 1):
        stack = []
        for token in self.circuit_rpn:
            if token.token_type == TokenType.COMPONENT:
                stack.append(self.evaluate_component(token, frequency))
            elif token.token_type == TokenType.DASH:
                left = stack.pop()
                right = stack.pop()
                stack.append(series(left, right))
            elif token.token_type == TokenType.PIPE:
                left = stack.pop()
                right = stack.pop()
                stack.append(parallel(left, right))
        self.impedance = stack.pop()
        return self.impedance


if __name__ == "__main__":
    circuit = Circuit("R | R")
    print(circuit.circuit_rpn)
    # circuit.evaluate()
    # print(circuit.get_components())
    print(circuit.evaluate())
