from antlr4 import *

from grammar.PjpGrammarLexer import PjpGrammarLexer as Lexer
from grammar.PjpGrammarParser import PjpGrammarParser as Parser
from visitors import ErrorListener, TypeChecker, MyVisitor


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
        type_checker = TypeChecker()
        type_checker.visit(tree)

        if len(type_checker.type_errors) > 0:
            print('Type errors:')
            for e in type_checker.type_errors:
                print(e)
            exit(1)

        visitor = MyVisitor()
        visitor.visit(tree)


if __name__ == '__main__':
    main()
