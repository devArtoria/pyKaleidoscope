from enum import Enum


class Token(Enum):
    EOF = -1
    DEF = -2
    EXTERN = -3
    IDENTIFIER = -4
    NUM = -5


class Lexer:
    def __init__(self, code: str):
        self.code: str = code

    @staticmethod
    def token_mapper(s):
        if s == "def":
            return Token.DEF
        elif s == "extern":
            return Token.EXTERN
        elif type(s) == int:
            return Token.NUM
        else:
            return Token.IDENTIFIER

    @staticmethod
    def identifier_check(t: Token, s: str):
        if t == Token.IDENTIFIER:
            if s.strip(".").isdigit():
                raise SyntaxError("LEX: Not a valid number type")

            if type(s[0]) is int:
                raise SyntaxError("LEX: Identifier must be started with character")

        return (t, s)

    def tokenizer(self):
        code = map(lambda x: int(x) if x.isdigit() else x, filter(lambda x: x[0] != "#", self.code.split(" ")))
        tokenized_code = map(self.identifier_check, map(self.token_mapper, code), filter(lambda x: x[0] != "#", self.code.split(" ")))
        tokenized_code = list(tokenized_code)
        tokenized_code.append((Token.EOF, "\n"))

        return tokenized_code


if __name__ == "__main__":
    print(Lexer("def i am #asd code").tokenizer())










