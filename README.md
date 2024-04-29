# ANTLR Stack Based Language
This project consists of several parts:
1. Type checker
2. Stack instruction generation
3. Interpreting stack instructions using "virtual machine"

Language definition is defined using ANLTR.

## Usage
Generate ANTLR visitor:
```bash
antlr4 -Dlanguage=Python3 grammar/PjpGrammar.g4 -visitor
```

Generate stack instructions:
```bash
python main.py examples/example01.txt
```

Execute stack instructions:
```bash
python virtual_machine.py bytecode.txt
```