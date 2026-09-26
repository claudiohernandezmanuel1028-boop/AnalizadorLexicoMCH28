@echo off
SET FLEX="C:\Users\manue\Downloads\win_flex_bison-2.5.25\win_flex.exe"
SET GCC="C:\Users\manue\Downloads\i686-16.2.0-release-mcf-dwarf-ucrt-rt_v14-rev1\mingw32\bin\gcc.exe"
SET SRC=src\lex.yy.c
SET LEX=src\lexer.l
SET OUT=build\lexer.exe

echo [1/3] Generando lex.yy.c con FLEX...
%FLEX% --wincompat -o %SRC% %LEX%
if %errorlevel% neq 0 (
    echo ERROR: FLEX no pudo procesar lexer.l
    pause
    exit /b 1
)
echo       OK

echo [2/3] Compilando lexer.exe con GCC...
%GCC% %SRC% -o %OUT% -static -static-libgcc
if %errorlevel% neq 0 (
    echo ERROR: GCC no pudo compilar lex.yy.c
    pause
    exit /b 1
)
echo       OK

echo [3/3] Listo. Ejecuta: python main.py
pause
