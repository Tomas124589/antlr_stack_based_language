import sys
from pathlib import Path

from antlr4 import *

from grammar.PjpGrammarLexer import PjpGrammarLexer as Lexer
from grammar.PjpGrammarParser import PjpGrammarParser as Parser
from visitors import ErrorListener, TypeChecker, MyVisitor


def main(path):
    with open(path, 'r') as file:
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
        instructions = visitor.visit(tree)

        with open(Path(__file__).parent / 'bytecode.txt', 'w') as file:
            file.writelines("\n".join(instructions))


if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print('No source code specified')
