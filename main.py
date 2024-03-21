from antlr4 import *

from grammar.pjpGrammarLexer import pjpGrammarLexer
from grammar.pjpGrammarParser import pjpGrammarParser

lexer = pjpGrammarLexer(InputStream('hello world'))
stream = CommonTokenStream(lexer)
parser = pjpGrammarParser(stream)

tree = parser.r()

print((tree.toStringTree(recog=parser)))
