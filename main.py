import opcodes_and_func as ops
import decodification as d

handler = {
    "0110011": d.r_type_decode,
    "0101111": d.r_type_decode,
    "0010011": d.i_type_decode,
    "0000011": d.i_type_decode,
    "1110011": d.i_type_decode,
    "0100011": d.s_type_decode,
    "1100011": d.b_type_decode,
    "0110111": d.u_type_decode,
    "0010111": d.u_type_decode,
    "1101111": d.j_type_decode,
}


with open("Codigo_Maquina.txt", "r") as f:
    f.seek(0)
    acum = 0
    for line in f:

        op = line[25:32]
        if op in ops.opcodes:
            if op in handler:
                handler[op](line)
            else:
                acum += 1
                #print(f"no opcode {op} in handler yet")
        else:
            print(False)

    print(f"Operation Failures : [{acum}]")




