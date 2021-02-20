# Token Types
from typing import Tuple, List

TOKEN_INT = "INT"
TOKEN_FLOAT = "FLOAT"
TOKEN_PLUS = "PLUS"
TOKEN_MINUS = "MINUS"
TOKEN_MULTIPLY = "MULTIPLY"
TOKEN_DIVISION = "DIVISION"
TOKEN_LBRACKET = "LBRACKET"
TOKEN_RBRACKET = "RBRACKET"

SPACES = " \t"
DIGITS = "0123456789"
CHAR_TO_TOKEN = {
    "+": TOKEN_PLUS,
    "-": TOKEN_MINUS,
    "*": TOKEN_MULTIPLY,
    "/": TOKEN_DIVISION,
    "(": TOKEN_LBRACKET,
    ")": TOKEN_RBRACKET
}


class Token:
    def __init__(self, t_type: str, value: any = None) -> None:
        self.type = t_type
        self.value = value

    def __repr__(self) -> str:
        return f"{self.type}: {self.value}" if self.value else f"{self.type}"


class Error:
    def __init__(self, name: str, msg: str) -> None:
        self.name = name
        self.msg = msg

    def __str__(self):
        return f"{self.name}: \n\t{self.msg}"


class UnexpectedTokenError(Error):
    def __init__(self, msg, name: str):
        super().__init__("Unexpected Token", msg)


class Lexer:
    def __init__(self, expr: str) -> None:
        self.expr = expr
        self.pos = 0
        self.curr = expr[0] if len(expr) > 0 else None

    def next(self) -> None:
        self.pos += 1
        if self.pos < len(self.expr):
            self.curr = self.expr[self.pos]
        else:
            self.curr = None

    def get_tokens(self) -> Tuple[List[str], Error or None]:
        tokens = []

        while self.curr is not None:
            if self.curr in SPACES:
                self.next()
            elif self.curr in DIGITS:
                tokens.append(self.get_number())
            elif self.curr in CHAR_TO_TOKEN:
                tokens.append(CHAR_TO_TOKEN[self.curr])
                self.next()
            else:
                token = self.curr
                pos = self.pos
                self.next()
                return [], UnexpectedTokenError(
                    f"Unexpected token '{token}' at position {pos}."
                )

        return tokens, None

    def get_number(self) -> Token:
        parsed_str = ""
        num_dots = 0

        while self.curr is not None and self.curr in DIGITS + ".":
            if self.curr == ".":
                if num_dots > 0:
                    break
                num_dots += 1
            parsed_str += self.curr
            self.next()

        if num_dots == 0:
            return Token(TOKEN_INT, int(parsed_str))
        else:
            return Token(TOKEN_FLOAT, float(parsed_str))


def evaluate(expr: str) -> Tuple[List[str], Error or None]:
    lexer = Lexer(expr)
    return lexer.get_tokens()