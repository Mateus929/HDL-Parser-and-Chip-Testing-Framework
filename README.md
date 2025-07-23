# HDL Parser and Chip Testing Framework

## Overview

This framework provides a complete solution for parsing HDL (Hardware Description Language) files, building internal chip representations, simulating chip behavior, and running automated tests against test vectors.

## Features

- **HDL Parsing**: Parses syntactically correct HDL files with `IN`, `OUT`, and `PARTS` sections
- **Built-in Gates**: Supports primitive gates (`Nand`, `Not`, `And`, `Or`)
- **Hierarchical Simulation**: Handles composed chips that instantiate other chips
- **Automated Testing**: Reads test vectors and verifies chip behavior
- **Detailed Reporting**: Provides pass/fail results with detailed output comparisons

## Architecture

### Core Components

1. **HDLParser**: Parses HDL files and builds chip definitions
2. **ChipSimulator**: Simulates chip behavior for given inputs
3. **TestRunner**: Runs test vectors and generates reports
4. **BuiltinChips**: Implements logic for primitive gates

### Data Structures

- **Pin**: Represents input/output pins with name and width
- **ChipInstance**: Represents a chip instance within another chip
- **ChipDefinition**: Complete chip definition with inputs, outputs, and parts
- **TestVector**: Single test case with inputs and expected outputs

## Built-in Gates

The framework supports these primitive gates:

| Gate | Description | Inputs | Outputs | Logic |
|------|-------------|--------|---------|-------|
| `Nand` | NAND gate | a, b | out | `out = NOT(a AND b)` |
| `Not` | NOT gate | in | out | `out = NOT(in)` |
| `And` | AND gate | a, b | out | `out = a AND b` |
| `Or` | OR gate | a, b | out | `out = a OR b` |

## Implementation Details

### Parsing Strategy

1. **Preprocessing**: Remove comments and normalize whitespace
2. **Section Extraction**: Use regex to extract `IN`, `OUT`, and `PARTS` sections
3. **Pin Parsing**: Handle single pins 
4. **Parts Parsing**: Extract chip instantiations and their connections

### Simulation Strategy

1. **Signal Propagation**: Maintain a dictionary of signal values
2. **Part Execution**: Execute each part in order, updating signals
3. **Built-in Logic**: Use hardcoded logic functions for primitive gates
4. **Recursive Resolution**: Parse and simulate composed chips recursively


## Limitations and Assumptions

- Assumes syntactically correct HDL files
- No error checking for circular dependencies
- Single-bit signals only 
- Sequential execution of parts
- No walking in directory. Assume working directory contains the HDL file and test vectors only and not any subdirectories.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Mateus929/HDL-Parser-and-Chip-Testing-Framework.git
cd HDL-Parser-and-Chip-Testing-Framework
```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv env
source env/bin/activate 
```

3. Install dependencies:

```bash
make install
```

## Example Usage

Run the CLI tool on a file or directory:

```bash
poetry run python -m src.main [--files hdl&tv]|[--directory path_to_your_directory]
```

Example of running on a single HDL file and test vector:

```bash
poetry run python -m src.main --files tests/test_files/And.hdl tests/test_files/And.tv
```

Example of running on a directory containing HDL files and test vectors:

```bash
poetry run python -m src.main --directory tests/test_files
```

To run the full test suite:

```bash
poetry run pytest
```
---

## File Formats

### HDL File Format

```hdl
CHIP ChipName {
    IN input1, input2, input3;
    OUT output1, output2;
    
    PARTS:
    ChipType1(pin1=signal1, pin2=signal2, out=internal1);
    ChipType2(a=internal1, b=input3, out=output1);
    Not(in=output1, out=output2);
}
```

**Key Points:**
- Chip name follows `CHIP` keyword
- `IN` section lists input pins (comma-separated)
- `OUT` section lists output pins (comma-separated)
- `PARTS` section contains chip instantiations
- Connections are specified as `pin=signal`
- Statements end with semicolons

### Test Vector Format

```
input1,input2,input3;output1,output2
0,0,0;0,1
0,0,1;1,0
0,1,0;0,1
0,1,1;1,0
1,0,0;1,0
1,0,1;0,1
1,1,0;1,0
1,1,1;0,1
```

**Key Points:**
- First line is header: `inputs;outputs`
- Subsequent lines are test cases: `input_values;expected_output_values`
- Values are comma-separated
- Semicolon separates inputs from outputs