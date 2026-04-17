opcodes = {
    # REGISTER TYPES | R-type

    #          func7 | rs2 |  rs1  | func3 |  rd   | opcode
    "0110011":["0:7","7:12","12:17","17:20","20:25","25:32"],
    # Atomic Extension
    "0101111": ["0:7","7:12","12:17","17:20","20:25","25:32"],

    # IMMEDIATE TYPES | I- type

    #          imm  |  rs1  | func3 |  rd   | opcode
    "0010011":["0:12","12:17","17:20","20:25","25:32"],
    # Loading
    "0000011":["0:12","12:17","17:20","20:25","25:32"],
    # env call & break
    "1110011":["0:12","12:17","17:20","20:25","25:32"],


    #STORE TYPE | S-type
    #           imm | rs2 |  rs1  | func3 |  imm   | opcode
    "0100011":["0:7","7:12","12:17","17:20","20:25","25:32"],
            #  11:5                          4:0

    #BRANCH TYPE | B-type
    #           imm | rs2 |  rs1  | func3 |   imm  | opcode
    "1100011":["0:7","7:12","12:17","17:20","20:25","25:32"],
    #         12|10:5                       4:1|11

    #UPPER IMMEDIATE | U-type
#                imm  |   rd  | opcode
    "0110111": ["0:20","20:25","25:32"],

    "0010111": ["0:20","20:25","25:32"],

    #JUMP TYPE | J-type
#                imm  |   rd  | opcode
    "1101111": ["0:20","20:25","25:32"],
}

r_type_valid_ops = {
        (0, 0): "add",
        (0, 32): "sub",
        (4, 0): "xor",
        (6, 0): "or",
        (7, 0): "and",
        (1, 0): "sll",
        (5, 0): "srl",
        (5,20): "sra",
        (2,0): "slt",
        (3,0): "sltu"
    }


iType_imm_arithmetic = {
    0: "addi",
    4: "xori",
    6: "ori",
    7: "andi",
    2: "slti",
    3: "sltiu"
}

iType_load = {
    0: "lb",
    1: "lh",
    2: "lw",
    4: "lbu",
    5: "lhu",
}

iType_jump = {
    0: "jalr"
}

sType = {
    0:"sb",
    1:"sh",
    2:"sw"
}


bType = {
    0: "beq",
    1: "bne",
    4: "blt",
    5: "bge",
    6: "bltu",
    7: "bgeu"
}

