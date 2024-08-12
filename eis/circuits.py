from .shunting_yard import ShuntingYard, TokenType, Component, Token
from math import pi
import numpy as np
from numpy import sqrt
from numpy.typing import NDArray
from collections import OrderedDict


def imp_C(
        f: NDArray[np.float64] | float, C: float
) -> NDArray[np.float64] | float:
    return 1 / (1j * 2 * pi * f * C)


def imp_L(
        f: NDArray[np.float64] | float, L: float
) -> NDArray[np.float64] | float:
    return 1j * 2 * pi * f * L


def imp_Q(
        f: NDArray[np.float64] | float, Q: float, a: float = 1
) -> NDArray[np.float64] | float:
    return Q / (1j * 2 * pi * f) ** a


def imp_W(
        f: NDArray[np.float64] | float, W: float
) -> NDArray[np.float64] | float:
    return (W / sqrt(2 * pi * f)) + (W / (1j * sqrt(2 * pi * f)))


def series(*args):
    return sum(args)


def parallel(*args):
    return 1 / sum(1 / arg for arg in args)


class Circuit:
    def __init__(self, circuit: str):
        self.circuit = " ".join(list(circuit))
        sy = ShuntingYard()  # fix this mess
        self.rpn = sy.run(circuit)  # fix to show the literals not the lexemes
        self.rpn_str = sy.to_str(self.rpn)
        self.components = OrderedDict()
        for token in self.rpn:
            if token.token_type == TokenType.COMPONENT:
                # fix default value in the literals
                setattr(self, token.literal, 1)
                self.components[token.literal] = 1

    def __str__(self):
        output = f"""
        Circuit Representation:    {self.circuit}
        RPN Representation:        {self.rpn_str}
        Components:                {self.components}
        """
        return output

    def __repr__(self):
        return self.__str__()

    def set_component(self, component: str, value: float):
        if component not in self.components:
            raise Exception(f"Component {component} not found in circuit")
        setattr(self, component, value)
        self.components[component] = value

    def set_components(self, **kwargs):
        for component, value in kwargs.items():
            self.set_component(component, value)

    def get_component(self, component: str):
        if component not in self.components:
            raise Exception(f"Component {component} not found in circuit")
        return self.components[component]

    def get_components(self):
        return self.components

    def evaluate_component(
            self, token: Token, frequency: NDArray[np.float64] | float
    ) -> NDArray[np.float64] | float:
        match token.opt:
            case Component.R:
                return self.components[token.literal]
            case Component.C:
                return imp_C(frequency, self.components[token.literal])
            case Component.L:
                return imp_L(frequency, self.components[token.literal])
            case Component.Q:
                return imp_Q(frequency, self.components[token.literal])
            case Component.W:
                return imp_W(frequency, self.components[token.literal])

    def evaluate(
            self, frequency: NDArray[np.float64] | float,
            params: NDArray[np.float64] | float | None = None,
    ) -> NDArray[np.float64] | float:
        stack = []
        for token in self.rpn:
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
        return stack.pop()

    def fit(
            self, frequencies: NDArray[np.float64], Z: NDArray[np.complex64]
    ) -> dict[str, float]:
        pass
