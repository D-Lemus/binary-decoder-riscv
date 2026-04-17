
from decoder import split_chain, shift_logical, reassemble_imm, u_type_decode


   # --- split_chain ---
def test_split_chain_decoded():
    # opcode 0110011 (R-type) con todos los campos en cero
    line = "0" * 25 + "0110011"
    result = split_chain(line, as_uncoded=False)
    assert result == [0, 0, 0, 0, 0, 51]


# --- shift_logical ---
def test_shift_logical_slli():
    assert shift_logical(1, 0) == "slli"

def test_shift_logical_srli():
    assert shift_logical(5, 0) == "srli"


# --- reassemble_imm ---
def test_reassemble_imm_s_type():
    result = reassemble_imm("S", "0000000", "00000")
    assert result == "000000000000"


# --- u_type_decode ---
def test_u_type_lui():
    # opcode 0110111 (lui), rd=1, imm=0
    line = "0" * 20 + "00001" + "0110111"
    assert "lui" in u_type_decode(line)

    # --- split_chain (rama faltante: as_uncoded=True) ---
def test_split_chain_uncoded():
    # Mismo opcode R-type, pero pedimos los bloques sin decodificar
    line = "0" * 25 + "0110011"
    result = split_chain(line, as_uncoded=True)
    # Debe devolver strings, no enteros
    assert all(isinstance(b, str) for b in result)
    assert result[-1] == "0110011"


# --- shift_logical (rama faltante: else) ---
def test_shift_logical_not_found():
    result = shift_logical(2, 99)
    assert "not found" in result


# --- reassemble_imm (ramas faltantes: B, J, else) ---
def test_reassemble_imm_b_type():
    # half_1 de 7 chars, half_2 de 5 chars (imm de B-type)
    half_1 = list("1010101")
    half_2 = list("11010")
    result = reassemble_imm("B", half_1, half_2)
    # Debe ser un string binario de 12 bits
    assert len(result) == 12
    assert all(c in "01" for c in result)


def test_reassemble_imm_j_type():
    # half_1 de 20 chars (imm completo de J-type)
    half_1 = "10101010101010101010"
    result = reassemble_imm("J", half_1)
    assert len(result) == 20
    assert all(c in "01" for c in result)


def test_reassemble_imm_invalid_type():
    # Cualquier tipo no reconocido devuelve False
    assert reassemble_imm("X", "0000") is False


# --- u_type_decode (ramas faltantes: auipc y Unknown) ---
def test_u_type_auipc():
    # opcode 0010111 (auipc), rd=1, imm=0
    line = "0" * 20 + "00001" + "0010111"
    assert "auipc" in u_type_decode(line)


def test_u_type_unknown_opcode():
    # Un opcode válido en el diccionario pero que no sea lui ni auipc
    # Usamos 0110111 modificado... en realidad necesitamos uno que esté en ops.opcodes
    # pero no sea 0110111 ni 0010111. Por ejemplo 1101111 (J-type) tiene la misma
    # estructura U en opcodes (20,25,32), así que podemos forzar ese caso.
    line = "0" * 20 + "00001" + "1101111"
    result = u_type_decode(line)
    assert "Unknown" in result