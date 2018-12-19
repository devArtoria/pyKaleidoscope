from typing import Type, Union, Any, List, Generator
from chapter_1_lexer import Lexer, Token, TokenKind


class ExprAST:
    def __init__(self, val: Any):
        self.val: Any = val

    def dump(self, indent: int):
        print("\t"*indent + "[{0}]: {1}".format(self.__class__.__name__, self.val))


class NumberExprAST(ExprAST):
    val: Union[int, float]


class VariableExprAST(ExprAST):
    val: str


class BinaryExprAST(ExprAST):
    def __init__(self, op, lhs: Type[ExprAST], rhs: Type[ExprAST]):
        self.op: str = op
        self.lhs: Type[ExprAST] = lhs
        self.rhs: Type[ExprAST] = rhs

    def dump(self, indent: int):
        print("\t"*indent + "[{0}]: {1}".format(self.__class__.__name__, self.op))
        self.lhs.dump(indent+1)
        self.rhs.dump(indent+1)


class CallExprAST(ExprAST):
    def __init__(self, callee: str, args: List[Type[ExprAST]]):
        self.calee: str = callee
        self.args: List[Type[ExprAST]] = args

    def dump(self, indent: int):
        print("\t"*indent, "[{0}]: {1} {2}".format(self.__class__.__name__, self.calee, self.args))


class PrototypeAST(ExprAST):
    def __init__(self, name: str, arguments):
        self.name: str = name
        self.arguments: List[str] = arguments

    def dump(self, indent):
        print("\t"*indent, "[{0}]: {1} {2}".format(self.__class__.__name__, self.name, self.arguments))


class FunctionAST(ExprAST):
    def __init__(self, proto, body):
        self.proto: PrototypeAST = proto
        self.body: Type[ExprAST] = body

    def dump(self, indent):
        print("\t"*indent, "[{0}]".format(self.__class__.__name__))
        self.proto.dump(indent+1)
        self.body.dump(indent+2)


class ParseError(Exception):
    pass


class Parser:
    def __init__(self):
        self.token_generator: Generator[Token, None, None] = None
        self.current_token: Token = None
        self.priority_map = {
            "<": 10,
            "+": 20,
            "-": 20,
            "*": 30,
            "/": 30
        }

    def parse_toplevel(self, buf):
        """Given a string, returns an AST node representing it."""
        self.token_generator = Lexer(buf).tokens()
        self.current_token = None
        self.get_next_token()

        if self.current_token.kind == TokenKind.EXTERN:
            return self.parse_extern()
        elif self.current_token.kind == TokenKind.DEF:
            return self.parse_definition()
        elif self.current_token == ';':
            self.get_next_token()
            return None
        else:
            return self.parse_toplevel_expr()

    def get_token_priority(self):
        return self.priority_map.get(self.current_token.value, -1)

    def get_next_token(self):
        self.current_token = next(self.token_generator)

    def parse_number_expr(self):
        result = NumberExprAST(self.current_token.value)
        self.get_next_token()

        return result

    def parse_paren_expr(self):
        self.get_next_token()
        expr = self.parse_expr()

        if self.current_token.value != ")":
            raise ParseError("Expected ')' ")
        self.get_next_token()

        return expr

    def parse_identifier_expr(self):
        id_name = self.current_token.value
        self.get_next_token()

        if self.current_token.value != "(":  # parse variable def expr
            return VariableExprAST(id_name)

        self.get_next_token()
        args = []
        if self.current_token.value != ")":
            while True:
                args.append(self.parse_expr())
                if self.current_token.value == ")":
                    break
                if self.current_token.value != ",":
                    raise ParseError("Expected ',' or ')'")
                self.get_next_token()

        self.get_next_token()

        return CallExprAST(id_name, args)

    def parse_primary(self):
        current_token = self.current_token

        if current_token.kind == TokenKind.IDENTIFIER:
            return self.parse_identifier_expr()
        elif current_token.kind == TokenKind.NUMBER:
            return self.parse_number_expr()
        elif current_token.value == "(":
            return self.parse_paren_expr()
        else:
            raise ParseError('Unknown token when expecting an expression')

    def parse_expr(self):
        lhs = self.parse_primary()
        return self.parse_bin_op_rhs(0, lhs)

    def parse_bin_op_rhs(self, expr_priority, lhs):
        while True:
            current_token_priority = self.get_token_priority()
            if current_token_priority < expr_priority:
                return lhs

            op = self.current_token.value
            self.get_next_token()

            rhs = self.parse_primary()

            next_token_priority = self.get_token_priority()
            if current_token_priority < next_token_priority:
                rhs = self.parse_bin_op_rhs(current_token_priority+1, rhs)

            lhs = BinaryExprAST(op, lhs, rhs)

    def parse_prototype(self):
        if self.current_token.kind != TokenKind.IDENTIFIER:
            raise ParseError("Expected function name in prototype")

        func_name = self.current_token.value
        self.get_next_token()

        if self.current_token.value != '(':
            raise ParseError("Expected ( in prototype")

        self.get_next_token()

        args = []

        while self.current_token.kind == TokenKind.IDENTIFIER:
            args.append(self.current_token.value)
            self.get_next_token()

        if self.current_token.value != ")":
            raise ParseError("Expected ) in prototype")

        self.get_next_token()

        return PrototypeAST(func_name, args)

    def parse_definition(self):
        self.get_next_token()
        prototype = self.parse_prototype()
        expr = self.parse_expr()

        return FunctionAST(prototype, expr)

    def parse_extern(self):
        self.get_next_token()
        return self.parse_prototype()

    def parse_toplevel_expr(self):
        expr = self.parse_expr()
        return FunctionAST(PrototypeAST("", []), expr)


if __name__ == "__main__":
    p = Parser()
    while True:
        code = input("ready>")
        print("result>")
        p.parse_toplevel(code).dump(0)
