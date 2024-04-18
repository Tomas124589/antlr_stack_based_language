grammar PjpGrammar;

program: statement+ ;

statement : SEMICOL | write SEMICOL ;

write : 'write' argumentList ;

argumentList : argument (',' argument)* ;
argument : STRING | INT | FLOAT ;

ID : [a-z]+ ;
STRING: '"' (~["\\\r\n] | EscapeSequence)* '"';
INT : [0-9]+ ;
FLOAT:
    (Digits '.' Digits? | '.' Digits) ExponentPart? [fFdD]?
    | Digits (ExponentPart [fFdD]? | [fFdD])
;
BOOL: 'true' | 'false' ;
SEMICOL: ';' ;
WS : [ \t\r\n]+ -> skip;

fragment EscapeSequence:
    '\\' 'u005c'? [btnfr"'\\]
    | '\\' 'u005c'? ([0-3]? [0-7])? [0-7]
    | '\\' 'u'+ HexDigit HexDigit HexDigit HexDigit
;

fragment Digits: [0-9] ([0-9_]* [0-9])?;

fragment ExponentPart: [eE] [+-]? Digits;

fragment HexDigit: [0-9a-fA-F];