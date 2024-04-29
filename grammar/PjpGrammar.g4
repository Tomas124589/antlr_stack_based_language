grammar PjpGrammar;

program: statement+ ;

statement   : SEMICOL
            | write SEMICOL
            | read SEMICOL
            | variableDeclaration SEMICOL
            | variableAssignment SEMICOL
            | ifStatement
            | ifStatementBody
            | whileStatement
            ;

write : 'write' expression (',' expression)* ;

read : 'read' ID (',' ID)* ;

variableDeclaration : TYPE ID (',' ID)* ;
variableAssignment : (ID '=')+ expression ;
ifStatement: IF '(' expression ')' statement ELSE statement;
ifStatementBody: IF '(' expression ')' '{' statement+ '}';
whileStatement: WHILE '(' expression ')' '{' statement+ '}' ;

expression : expression op=( MUL | DIV | MOD ) expression   # MulDivModExpression
           | expression op=( '+' | '-' ) expression         # AddSubExpression
           | expression op=AND expression                   # LogicalExpression
           | expression op=OR expression                    # LogicalExpression
           | expression op=(LT | GT) expression             # LesserGreaterExpression
           | expression op=(EQ | NEQ) expression            # EqualNotEqualExpression
           | '(' expression ')'                             # ParenExpression
           | ID                                             # IdExpression
           | (INT | FLOAT)                                  # NumberExpression
           | expression '.' expression                      # ConcatExpression
           | STRING                                         # StringExpression
           | BOOL                                           # BoolExpression
           | NOT expression                                 # NotExpression
           ;

NOT: '!' ;
AND: '&&' ;
OR: '||' ;
LT: '<' ;
GT: '>' ;
EQ: '==';
NEQ: '!=';

MUL : '*' ;
DIV : '/' ;
MOD : '%' ;
ADD : '+' ;
SUB : '-' ;

IF : 'if' ;
ELSE : 'else' ;
WHILE : 'while' ;

TYPE : 'string' | 'int' | 'float' | 'bool' ;
BOOL: 'true' | 'false' ;
SEMICOL: ';' ;
STRING: '"' (~["\\\r\n] | EscapeSequence)* '"';
ID : [a-z]+ ;
INT : '-'?[0-9]+ ;
FLOAT:
    (Digits '.' Digits? | '.' Digits) ExponentPart? [fFdD]?
    | Digits (ExponentPart [fFdD]? | [fFdD])
;
WS : [ \t\r\n]+ -> skip;
LINE_COMMENT : '//' ~[\r\n]* -> skip;

fragment EscapeSequence:
    '\\' 'u005c'? [btnfr"'\\]
    | '\\' 'u005c'? ([0-3]? [0-7])? [0-7]
    | '\\' 'u'+ HexDigit HexDigit HexDigit HexDigit
;

fragment Digits: [0-9] ([0-9_]* [0-9])?;

fragment ExponentPart: [eE] [+-]? Digits;

fragment HexDigit: [0-9a-fA-F];