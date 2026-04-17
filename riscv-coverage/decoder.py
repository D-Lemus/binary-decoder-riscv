import opcodes_and_func as ops


def split_chain(binary_chain: str, as_uncoded=False) -> list:
    opcode = binary_chain[25:32]
    decoded = []
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
            line_block = int(binary_chain[int(start):int(end)], 2)
            decoded.append(line_block)
        return decoded


def shift_logical(funct3: int, imm: int) -> str:
    shift_logical_ops = {
        (1, 0): "slli",
        (5, 0): "srli",
        (5, 32): "srai"
    }

    if (funct3, imm) in shift_logical_ops:
        return shift_logical_ops[(funct3, imm)]
    else:
        return f"[shift logical {funct3},{imm} not found]"


def reassemble_imm(type: str, half_1, half_2=None):
    if type == "S":
        return half_1 + half_2

    elif type == "B":
        msb, bit_11 = list(half_1[0]), list(half_2[4])
        imm_hi = half_1[1:7]
        imm_lo = half_2[0:4]
        imm = msb + bit_11 + imm_hi + imm_lo
        return "".join(imm)

    elif type == "J":
        msb, bit_11 = half_1[0], half_1[9]
        imm_lo = half_1[10:20]
        imm_hi = half_1[1:9]
        imm = msb + bit_11 + imm_hi + imm_lo
        return "".join(imm)

    else:
        return False


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
    return f"U-type: {operation} x{rd}, {imm}"