from enum import Enum


class Token(Enum):
    EOF = -1
    DEF = -2
    EXTERN = -3
    IDENTIFIER = -4
    NUM = -5
    OPERATOR = -6


class Lexer:
    def __init__(self, code: str):
        self.code: str = code

    @staticmethod
    def token_mapper(s):
        if s == "def":
            return (Token.DEF, s)
        elif s == "extern":
            return (Token.EXTERN, s)
        elif s in  ("*", "+", "-", "/", "%", "^", "="):
            return (Token.OPERATOR, s)
        elif s[0].isdigit():
            if not s.replace(".", "").isdigit():
                raise SyntaxError("LEX: Identifier must be started with character")
            if s.count(".") > 1:
                raise SyntaxError("LEX: Not a valid number type")
            s = float(s) if "." in s else int(s)
            return (Token.NUM, s)
        else:
            return (Token.IDENTIFIER, s)

    def tokenizer(self):
        code = [x for x in self.code.split() if x[0] != "#"]
        tokenized_code = [self.token_mapper(x) for x in code]
        tokenized_code.append((Token.EOF, "\n"))

        return tokenized_code


if __name__ == "__main__":
    print(Lexer("def extern 12423.3 + * am #asd code \n adsfasdf").tokenizer())
