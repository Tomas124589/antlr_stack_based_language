from antlr4 import *

from grammar.PjpGrammarLexer import PjpGrammarLexer as Lexer
from grammar.PjpGrammarParser import PjpGrammarParser as Parser
from visitor import MyVisitor


def main():
    with open('examples/example01.txt', 'r') as file:
        contents = file.read()

    lexer = Lexer(InputStream(contents))
    stream = CommonTokenStream(lexer)
    parser = Parser(stream)

    visitor = MyVisitor()
    visitor.visit(parser.program())


if __name__ == '__main__':
    main()
