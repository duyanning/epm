%{
#include <stdio.h>
//int yylex(void);
void yyerror(const char*);
#include "scaner.h"
%}

%token NUM

%%
/*
1
1 3 5 7
1-20
1-20+2

1*3
(1 3 5 7)*3
1-20*3
1-20+2*3

((1 3 5 7) (2 4 6))*3
((1 3 5 7) 1-20*3)*3
((1 3 5 7)*2 1-20*3)*3
*/

seq_list:	  seq
			| seq_list seq
			;

seq:	  NUM
		| range
		| compound_seq
		| times_seq
		;

compound_seq:	  '(' seq_list ')'
				;


times_seq:	  seq '*' NUM
			;

range:	  NUM '-' NUM
		| NUM '-' NUM '+' NUM
		| NUM '-' NUM '-' NUM
		;


%%

