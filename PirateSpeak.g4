grammar PirateSpeak;

program: classDeclaration* ;

classDeclaration: 'ship' IDENTIFIER '{' memberDeclaration* '}' ;

memberDeclaration: variableDeclaration | methodDeclaration ;

variableDeclaration: accessModifier 'treasure' type IDENTIFIER ';' ;

methodDeclaration: accessModifier 'adventure' IDENTIFIER '(' parameterList? ')' block ;

parameterList: parameter (',' parameter)* ;

parameter: type IDENTIFIER ;

block: '{' statement* '}' ;

statement: variableDeclaration
         | expressionStatement
         | ifStatement
         | forStatement
         | whileStatement
         | returnStatement
         | block
         ;

expressionStatement: expression ';' ;

ifStatement: 'explore' '(' expression ')' statement ('deviate' statement)? ;

forStatement: 'sail' '(' expression? ';' expression? ';' expression? ')' statement ;

whileStatement: 'while' '(' expression ')' statement ;

returnStatement: 'return' expression? ';' ;

expression: assignment | logicalOr ;

assignment: IDENTIFIER '=' expression ;

logicalOr: logicalAnd ('||' logicalAnd)* ;

logicalAnd: equality ('&&' equality)* ;

equality: comparison (('==' | '!=') comparison)* ;

comparison: term (('>' | '>=' | '<' | '<=') term)* ;

term: factor (('+' | '-') factor)* ;

factor: unary (('*' | '/') unary)* ;

unary: ('!' | '-')? primary ;

primary: literal | IDENTIFIER | '(' expression ')' ;

literal: INTEGER_LITERAL | STRING_LITERAL | BOOLEAN_LITERAL | CHARACTER_LITERAL | FLOAT_LITERAL ;

accessModifier: 'allHands' | 'officerOnly' ;

type: 'coin' | 'scroll' | 'loot' | 'beacon' | 'mark' ;

IDENTIFIER: [a-zA-Z_][a-zA-Z0-9_]* ;
INTEGER_LITERAL: [0-9]+ ;
STRING_LITERAL: '"' .*? '"' ;
BOOLEAN_LITERAL: 'aye' | 'nay' ;
CHARACTER_LITERAL: '\'' . '\'' ;
FLOAT_LITERAL: [0-9]+ '.' [0-9]+ ;

WS: [ \t\r\n]+ -> skip ;