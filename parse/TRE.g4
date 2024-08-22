grammar TRE;

file : expr EOF ;

expr : EPS																				#EpsExpr
	 | IDENTIFIER																		#AtomicExpr
	 | '(' expr ')'																		#ParenExpr
     | expr '*'																			#KleeneExpr
     | expr '.' expr																	#ConcatExpr
     | expr '+'																			#PlusExpr
     | expr '+' expr																	#UnionExpr
     | expr '&' expr																	#IntersectionExpr
     | '<' expr '>' '_' interval														#TimedExpr
     | '{' (rename_token ',')* rename_token '}' expr									#RenameExpr
     ;

interval : '[' INT ',' (INT | INF) ']';

//LETTER : [a-zA-Z] ;

EPS : 'EPS';
INF : 'INF' | 'oo' | 'inf';

rename_token : IDENTIFIER ':' IDENTIFIER;

IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]* ;


INT : [0-9]+ ;
WS : [ \t\r\n]+ -> skip ;

// Rule to handle Python-style comments
COMMENT : '#' ~[\r\n]* -> skip ;