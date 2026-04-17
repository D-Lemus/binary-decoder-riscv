import opcodes_and_func as ops

def split_chain(binary_chain: str, as_uncoded= False) -> list:
    opcode = binary_chain[25:32]
    decoded= []
    block_uncoded = []

    if as_uncoded:
        for blocks in ops.opcodes[opcode]:
            start, end = blocks.split(":")
            line_block_uncoded = binary_chain[int(start):int(end)]
            block_uncoded.append(line_block_uncoded)
        return block_uncoded
    else:
        for blocks in ops.opcodes[opcode]:
            start, end = blocks.split(":")
            line_block = int(binary_chain[int(start):int(end)],2)
            decoded.append(line_block)
        return decoded

def shift_logical(funct3: int, imm: int) -> str:
    operation = ""
    shift_logical_ops= {
    (1,0): "slli",
    (5,0): "srli",
    (5,32): "srai"}

    if (funct3, imm) in shift_logical_ops:
        return shift_logical_ops[(funct3, imm)]

    else:
        return f"[shift logical {funct3},{imm} not found]"

def reassemble_imm(type: str, half_1, half_2= None):
    imm = None

    if type == "S":
        imm = half_1 + half_2
        return imm

    elif type == "B":

        msb, bit_11 = list(half_1[0]),list(half_2[4])
        imm_hi= half_1[1:7]
        imm_lo = half_2[0:4]
        imm = msb + bit_11 + imm_hi + imm_lo
        imm = "".join(imm)
        return imm


    # 11111011110111111111
    elif type == "J":
        msb, bit_11 = half_1[0], half_1[9]
        imm_lo= half_1[10:20]
        imm_hi= half_1[1:9]
        #print(f"msb: {msb}, imm_lo: {imm_lo}, imm_hi: {imm_hi}, bit_11: {bit_11}")
        imm = msb + bit_11 + imm_hi + imm_lo
        imm = "".join(imm)
        return imm
    else:
        return False

def r_type_decode(line: str):
    opcode = line[25:32]

    if opcode == "0110011":

        r_decoded = split_chain(line, as_uncoded=False)

        funct7, funct3 = r_decoded[0], r_decoded[3]
        rs1, rs2, rd= r_decoded[2],r_decoded[1],r_decoded[4]
        operation = ops.r_type_valid_ops[(funct3,funct7)]

        print(f"R-type: {operation} x{rd}, x{rs1}, x{rs2}")



    elif opcode == "0101111":
        #todo
        pass

def i_type_decode(line: str):
    opcode = line[25:32]
    i_decoded = split_chain(line, as_uncoded=False)
    imm = i_decoded[0]
    funct3 = i_decoded[2]
    rd, rs1 = i_decoded[3], i_decoded[1]

    #immediate arithmetics
    if opcode == "0010011":

        if funct3 == 5 or funct3 ==1:
            operation = shift_logical(funct3, imm)
        else:
            operation = ops.iType_imm_arithmetic[funct3]

        print(f"I-type: {operation} x{rd}, x{rs1}, {imm}")
    #load
    if opcode == "0000011":
        operation = ops.iType_load[funct3]
        print(f"I-type: {operation} x{rd}, {imm}(x{rs1})")

    #jump
    if opcode == "1110011":
        operation = ops.iType_jump[funct3]
        print(f"I-type (jump): {operation} x{rd}, {imm}(x{rs1})")

def s_type_decode(line: str):
    opcode = line[25:32]
    s_decoded = split_chain(line, as_uncoded=False)
    s_uncoded = split_chain(line, as_uncoded=True)
    rs1, rs2 = s_decoded[2], s_decoded[1]
    funct3 = s_decoded[3]

    imm_hi,imm_lo = s_uncoded[0],s_uncoded[3]
    operation = ops.sType[funct3]

    imm = reassemble_imm("S", imm_hi, imm_lo)
    #print(f"S-type immediate concat: {imm} = {msb} + {lsb}")
    imm = int(imm, 2)
    print(f"S-type: {operation} x{rs2}, {imm}(x{rs1})")

def b_type_decode(line: str):
    opcode = line[25:32]
    b_decoded = split_chain(line, as_uncoded=False)
    b_uncoded = split_chain(line, as_uncoded=True)
    half_1, half_2 = list(b_uncoded[0]), list(b_uncoded[4])
    rs2,rs1,funct3 = b_decoded[1], b_decoded[2], b_decoded[3]
    operation = ops.bType[funct3]
    imm = int(reassemble_imm("B", half_1, half_2), 2)
    #print(f"half_1: {half_1}, half_2: {half_2}")
    #print(f"imm: {imm}")
    print(f"B-type: {operation} x{rs1}, x{rs2}, {imm}")

def u_type_decode(line: str):
    opcode = line[25:32]
    u_decoded = split_chain(line, as_uncoded=False)
    rd = u_decoded[1]
    imm = u_decoded[0]
    if opcode == "0110111":
        operation = "lui"
    elif opcode == "0010111":
        operation = "auipc"
    else:
        operation = "[Unknown operation]"
    print(f"U-type: {operation} x{rd}, {imm}")

def j_type_decode(line: str):
    j_decoded = split_chain(line, as_uncoded=False)
    j_uncoded = split_chain(line, as_uncoded=True)
    rd = j_decoded[1]
    imm = j_uncoded[0]
    imm = int(reassemble_imm("J", imm),2)

    print(f"J-type: jal x{rd}, {imm}")