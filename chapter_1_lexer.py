from enum import Enum
from collections import namedtuple


class TokenKind(Enum):
    EOF = -1
    DEF = -2
    EXTERN = -3
    IDENTIFIER = -4
    NUMBER = -5
    OPERATOR = -6


Token = namedtuple('Token', 'kind value')


class Lexer:
    def __init__(self, code: str):
        self.code: str = code

        self.pos = 0
        self.last_char = self.code[0]

    def tokens(self):
        while self.last_char:
            # Skip whitespace
            while self.last_char.isspace():
                self.advance()
            # Identifier or keyword
            if self.last_char.isalpha():
                id_str = ''
                while self.last_char.isalnum():
                    id_str += self.last_char
                    self.advance()
                if id_str == 'def':
                    yield Token(kind=TokenKind.DEF, value=id_str)
                elif id_str == 'extern':
                    yield Token(kind=TokenKind.EXTERN, value=id_str)
                else:
                    yield Token(kind=TokenKind.IDENTIFIER, value=id_str)
            # Number
            elif self.last_char.isdigit() or self.last_char == '.':
                num_str = ''
                while self.last_char.isdigit() or self.last_char == '.':
                    num_str += self.last_char
                    self.advance()
                yield Token(kind=TokenKind.NUMBER, value=num_str)
            # Comment
            elif self.last_char == '#':
                self.advance()
                while self.last_char and self.last_char not in '\r\n':
                    self.advance()
            elif self.last_char:
                # Some other char
                yield Token(kind=TokenKind.OPERATOR, value=self.last_char)
                self.advance()
        yield Token(kind=TokenKind.EOF, value='')

    def advance(self):
        try:
            self.pos += 1
            self.last_char = self.code[self.pos]
        except IndexError:
            self.last_char = ''


if __name__ == "__main__":
    a = list(Lexer("def extern 12 + *am+ #asd code adsfasdf").tokens())
    print(a)




