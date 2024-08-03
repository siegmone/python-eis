from enum import Enum


class ComponentType(Enum):
    R = 1
    C = 2
    L = 3
    Q = 4
    W = 5


class TokenType(Enum):
    PIPE = 1
    DASH = 2
    LEFT_PAREN = 3
    RIGHT_PAREN = 4
    EOF = 5
    COMPONENT = 6


class Token:
    def __init__(self, token_type, lexeme, literal):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.opt = None

    def set_opt(self, opt):
        self.opt = opt

    def __str__(self):
        return f"{self.token_type} {self.lexeme} {self.literal} {self.opt}"

    def __repr__(self):
        return self.__str__()


def precedence(token):
    if token == TokenType.DASH:
        return 1
    if token == TokenType.PIPE:
        return 2
    return 0


class ShuntingYard:
    def __init__(self):
        self.tokens = []
        self.start = 0
        self.current = 0
        self.output_queue = []
        self.operator_stack = []
        self.components_counter = {}

    def run_prompt(self):
        while True:
            src = input("> ")
            if src == "exit":
                break
            try:
                print(self.run_str(src))
            except Exception as e:
                raise e

    def run(self, src):
        self.src = src
        self.scan_tokens()
        self.parse_tokens()
        return self.output_queue

    def run_str(self, src):
        self.run(src)
        lexemes = [token.lexeme for token in self.output_queue]
        return " ".join(lexemes)

    def parse_tokens(self):
        for token in self.tokens:
            self.parse_token(token)
        while self.operator_stack:
            if self.operator_stack[-1] == "(":  # )
                raise Exception("Mismatched parenthesis")
            self.output_queue.append(self.handle_pop())

    def parse_token(self, token):
        match token.token_type:
            case TokenType.COMPONENT:
                self.handle_component(token)
            case TokenType.PIPE:
                self.parse_operator(token)
            case TokenType.DASH:
                self.parse_operator(token)
            case TokenType.LEFT_PAREN:
                self.operator_stack.append(token)
            case TokenType.RIGHT_PAREN:
                while self.operator_stack[-1].token_type != TokenType.LEFT_PAREN:
                    self.output_queue.append(self.handle_pop())
                    if not self.operator_stack:
                        raise Exception("Parenthesis mismatch")
                self.handle_pop()

    def handle_component(self, token):
        match token.lexeme:
            case "R":
                token.set_opt(ComponentType.R)
                self.output_queue.append(token)
            case "C":
                token.set_opt(ComponentType.C)
                self.output_queue.append(token)
            case "L":
                token.set_opt(ComponentType.L)
                self.output_queue.append(token)
            case "Q":
                token.set_opt(ComponentType.Q)
                self.output_queue.append(token)
            case "W":
                token.set_opt(ComponentType.W)
                self.output_queue.append(token)
            case _:
                self.output_queue.append(token)

    def parse_operator(self, token):
        flag = True
        if len(self.operator_stack) == 0:
            self.operator_stack.append(token)
            flag = False
        while (flag and self.operator_stack and
               self.operator_stack[-1].token_type != TokenType.LEFT_PAREN) and (
                precedence(self.operator_stack[-1]) > precedence(token)
        ):
            self.output_queue.append(self.handle_pop())
        if flag:
            self.operator_stack.append(token)

    def handle_pop(self):
        return self.operator_stack.pop()

    def at_end(self):
        return self.current > len(self.src) - 1

    def add_token(self, token_type, *args):
        if len(args) > 1:
            raise TypeError("Too many arguments!")
        elif len(args) == 0:
            self.add_token(token_type, None)
        elif len(args) == 1:
            literal = args[0]
            text = self.src[self.start:self.current]
            self.tokens.append(Token(token_type, text, literal))

    def scan_tokens(self):
        while not self.at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None))
        return self.tokens

    def scan_token(self):
        char: str = self.advance()
        match char:
            case "(":  # )
                self.add_token(TokenType.LEFT_PAREN)
            case ")":  # )
                self.add_token(TokenType.RIGHT_PAREN)
            case '-':
                self.add_token(TokenType.DASH)
            case '|':
                self.add_token(TokenType.PIPE)
            case ' ':
                pass
            case _:
                if char.isalpha():
                    self.scan_component()
                else:
                    raise Exception("Unknown Token!")

    def scan_component(self):
        while self.peek().isalpha():
            self.advance()
        text = self.src[self.start:self.current]
        self.components_counter[text] = self.components_counter.get(
            text, 0) + 1
        self.add_token(
            TokenType.COMPONENT,
            f"{text}{self.components_counter[text]}"
        )

    def advance(self):
        next_char = self.src[self.current]
        self.current += 1
        return next_char

    def matchNext(self, expected):
        if self.at_end():
            return False
        if self.src[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.at_end():
            return '\0'
        else:
            return self.src[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.src):
            return '\0'
        return self.src[self.current + 1]
