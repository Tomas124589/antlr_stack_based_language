from antlr4 import *

from grammar.PjpGrammarLexer import PjpGrammarLexer as Lexer
from grammar.PjpGrammarParser import PjpGrammarParser as Parser
from visitors import MyVisitor, ErrorListener


def main():
    with open('examples/example01.txt', 'r') as file:
        contents = file.read()

    lexer = Lexer(InputStream(contents))
    stream = CommonTokenStream(lexer)
    parser = Parser(stream)

    parser.removeErrorListeners()
    parser.addErrorListener(ErrorListener())

    tree = parser.program()
    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = MyVisitor()
        visitor.visit(tree)


if __name__ == '__main__':
    main()
