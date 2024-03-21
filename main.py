from antlr4 import *

from grammar.PjpGrammarLexer import PjpGrammarLexer as Lexer
from grammar.PjpGrammarParser import PjpGrammarParser as Parser

lexer = Lexer(InputStream('hello world'))
stream = CommonTokenStream(lexer)
parser = Parser(stream)

tree = parser.r()

print((tree.toStringTree(recog=parser)))
