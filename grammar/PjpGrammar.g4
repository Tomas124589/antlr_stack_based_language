grammar PjpGrammar;

program: statement+ ;

statement   : SEMICOL
            | write SEMICOL
            | read SEMICOL
            | variableDeclaration SEMICOL
            | variableAssignment SEMICOL
            ;

write : 'write' expression (',' expression)* ;
value : STRING | INT | FLOAT | BOOL | ID | expression ;

read : 'read' ID (',' ID)* ;

variableDeclaration : TYPE ID (',' ID)* ;
variableAssignment : (ID '=')+ value ;

expression : expression op=( MUL | DIV | MOD ) expression   # MulDivModExpression
           | expression op=( '+' | '-' ) expression         # AddSubExpression
           | expression op=(AND | OR) expression            # LogicalExpression
           | expression op=(LT | GT) expression             # LesserGreaterExpression
           | expression op=(EQ | NEQ) expression            # EqualNotEqualExpression
           | '(' expression ')'                             # ParenExpression
           | ID                                             # IdExpression
           | (INT | FLOAT)                                  # NumberExpression
           | STRING '.' STRING                              # ConcatExpression
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