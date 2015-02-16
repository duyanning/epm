%{
#include <math.h>
#include "parser.h"
%}

%%

[0-9]+					yylval = atoi( yytext ); return NUM;
[ \t\n]+				/* eat up whitespace */
"("|")"|"-"|"+"|"*"		return *yytext;
.						printf("XXX");
