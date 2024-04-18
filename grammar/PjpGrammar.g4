grammar PjpGrammar;

program: statement+ ;

statement   : SEMICOL
            | write SEMICOL
            | variableDeclaration SEMICOL
            | variableAssignment SEMICOL
            ;

write : 'write' valueList ;
valueList : value (',' value)* ;
value : STRING | INT | FLOAT | BOOL | ID ;

variableDeclaration : TYPE ID ;
variableAssignment : ID '=' value ;

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

fragment EscapeSequence:
    '\\' 'u005c'? [btnfr"'\\]
    | '\\' 'u005c'? ([0-3]? [0-7])? [0-7]
    | '\\' 'u'+ HexDigit HexDigit HexDigit HexDigit
;

fragment Digits: [0-9] ([0-9_]* [0-9])?;

fragment ExponentPart: [eE] [+-]? Digits;

fragment HexDigit: [0-9a-fA-F];