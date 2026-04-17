# RISC-V Instruction Decoder

A Python-based decoder for RISC-V 32-bit machine code. Reads binary instruction files and prints human-readable assembly for each instruction.

---

## Project Structure

```
.
├── main.py                 # Entry point — reads binary file and dispatches decoding
├── decodification.py       # Decoding logic for each instruction type
├── opcodes_and_func.py     # Opcode tables, funct3/funct7 mappings
└── Codigo_Maquina.txt      # Sample binary machine code input
```

---

## Supported Instruction Types

| Type | Opcode | Examples |
|------|--------|---------|
| R-type | `0110011` | `add`, `sub`, `xor`, `or`, `and`, `sll`, `srl`, `sra`, `slt`, `sltu` |
| I-type (arithmetic) | `0010011` | `addi`, `xori`, `ori`, `andi`, `slti`, `sltiu`, `slli`, `srli`, `srai` |
| I-type (load) | `0000011` | `lb`, `lh`, `lw`, `lbu`, `lhu` |
| I-type (env) | `1110011` | `jalr` |
| S-type | `0100011` | `sb`, `sh`, `sw` |
| B-type | `1100011` | `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu` |
| U-type | `0110111`, `0010111` | `lui`, `auipc` |
| J-type | `1101111` | `jal` |

---

## Requirements

- Python 3.7+
- No external dependencies

---

## Usage

1. Place your binary machine code in a text file (one 32-bit instruction per line).

2. Update the filename in `main.py` if needed:
```python
with open("Codigo_Maquina.txt", "r") as f:
```

3. Run the decoder:
```bash
python main.py
```

### Example Input (`Codigo_Maquina.txt`)
```
00001111110000010000101000010111
00000000010010100000101000010011
```

### Example Output
```
U-type: auipc x20, 261121
I-type: addi x20, x20, 2
```

---

## How It Works

### 1. Dispatch (`main.py`)
Each 32-bit binary string is read line by line. The last 7 bits (positions `25:32`) identify the opcode, which maps to a specific decoder function via a handler dictionary.

### 2. Bit Splitting (`decodification.py` → `split_chain`)
The instruction is sliced into fields (funct7, rs1, rs2, rd, funct3, imm) based on the bit ranges defined in `opcodes_and_func.py`. Fields are returned either as integers or as raw binary strings.

### 3. Immediate Reassembly (`reassemble_imm`)
S, B, and J-type instructions encode their immediates in non-contiguous bit fields. `reassemble_imm` reconstructs the full immediate value from its scattered parts.

### 4. Operation Lookup
Decoded funct3/funct7 values are looked up in dictionaries (`r_type_valid_ops`, `iType_imm_arithmetic`, etc.) to resolve the final instruction mnemonic.

---

## Known Limitations

- Immediate values are not sign-extended (negative immediates will print as large positive numbers)
- Atomic extension (`0101111`) is not yet implemented
- Filename is hardcoded in `main.py`
- Decode functions print directly instead of returning values, limiting testability

---

## Potential Improvements

- Add sign extension for I, S, B, and J-type immediates
- Implement atomic (AMO) instruction decoding
- Refactor decode functions to return strings instead of printing
- Accept input file as a command-line argument via `argparse`
- Add unit tests with known binary/assembly pairs
