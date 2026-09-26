%{
#include <stdio.h>
#include <string.h>

int linea = 1;
FILE *salida;

void escribir_token(const char *tipo, const char *lexema) {
    fprintf(salida, "TOKEN|%s|%s|%d\n", lexema, tipo, linea);
}

void escribir_error(const char *lexema) {
    fprintf(salida, "ERROR|%s|ERROR_LEXICO|%d\n", lexema, linea);
}

%}

%option noyywrap

DIGITO      [0-9]
LETRA       [a-zA-Z_]
ALFANUM     [a-zA-Z0-9_]

%%

"//"[^\n]*              { }
"/*"([^*]|\*+[^*/])*\*+"/"  {
    char *p = yytext;
    while (*p) { if (*p == '\n') linea++; p++; }
}

"int"       { escribir_token("PALABRA_RESERVADA", yytext); }
"float"     { escribir_token("PALABRA_RESERVADA", yytext); }
"string"    { escribir_token("PALABRA_RESERVADA", yytext); }
"bool"      { escribir_token("PALABRA_RESERVADA", yytext); }
"if"        { escribir_token("PALABRA_RESERVADA", yytext); }
"else"      { escribir_token("PALABRA_RESERVADA", yytext); }
"while"     { escribir_token("PALABRA_RESERVADA", yytext); }
"return"    { escribir_token("PALABRA_RESERVADA", yytext); }
"true"      { escribir_token("PALABRA_RESERVADA", yytext); }
"false"     { escribir_token("PALABRA_RESERVADA", yytext); }

{LETRA}{ALFANUM}*   { escribir_token("IDENTIFICADOR", yytext); }

{DIGITO}+"."{DIGITO}+   { escribir_token("NUMERO_DECIMAL", yytext); }
{DIGITO}+               { escribir_token("NUMERO_ENTERO", yytext); }

\"([^\"\\]|\\.)*\"      { escribir_token("CADENA", yytext); }

"=="    { escribir_token("OP_IGUAL", yytext); }
"!="    { escribir_token("OP_DIFERENTE", yytext); }
">="    { escribir_token("OP_MAYOR_IGUAL", yytext); }
"<="    { escribir_token("OP_MENOR_IGUAL", yytext); }
"&&"    { escribir_token("OP_AND", yytext); }
"||"    { escribir_token("OP_OR", yytext); }

"+"     { escribir_token("OP_SUMA", yytext); }
"-"     { escribir_token("OP_RESTA", yytext); }
"*"     { escribir_token("OP_MULTIPLICACION", yytext); }
"/"     { escribir_token("OP_DIVISION", yytext); }
"="     { escribir_token("OP_ASIGNACION", yytext); }
">"     { escribir_token("OP_MAYOR", yytext); }
"<"     { escribir_token("OP_MENOR", yytext); }
"!"     { escribir_token("OP_NOT", yytext); }

"("     { escribir_token("PARENTESIS_ABRE", yytext); }
")"     { escribir_token("PARENTESIS_CIERRA", yytext); }
"{"     { escribir_token("LLAVE_ABRE", yytext); }
"}"     { escribir_token("LLAVE_CIERRA", yytext); }
"["     { escribir_token("CORCHETE_ABRE", yytext); }
"]"     { escribir_token("CORCHETE_CIERRA", yytext); }
";"     { escribir_token("PUNTO_COMA", yytext); }
","     { escribir_token("COMA", yytext); }

" "|\t      { }
\n          { linea++; }
\r\n        { linea++; }
\r          { linea++; }

.           { escribir_error(yytext); }

%%

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Uso: lexer <archivo_entrada> <archivo_salida>\n");
        return 1;
    }

    FILE *entrada = fopen(argv[1], "r");
    if (!entrada) {
        fprintf(stderr, "Error: No se puede abrir el archivo de entrada: %s\n", argv[1]);
        return 1;
    }

    salida = fopen(argv[2], "w");
    if (!salida) {
        fprintf(stderr, "Error: No se puede crear el archivo de salida: %s\n", argv[2]);
        fclose(entrada);
        return 1;
    }

    yyin = entrada;
    yylex();

    fclose(entrada);
    fclose(salida);

    return 0;
}
