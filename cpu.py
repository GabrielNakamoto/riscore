# unix pathname / patterns
import glob
from enum import Enum
# risc-v RV32I base integer instruction set

global PC
global regfile

# instruction formats: R, I, S, U, B, J
# I-type: register / immediate operations
# fixed 32 bit length
# must be aligned in memory
# source and destination registers always in same location
# (rs1, rs2, rd)
# little endian memory storage

# https://www.cs.sfu.ca/~ashriram/Courses/CS295/assets/notebooks/RISCV/RISCV_CARD.pdf
class Opcodes(Enum):
    # register-register op
    ROP = 0b0110011
    # register-immediate op
    IOP = 0b0010011
    # load into rd (from memory)
    LOP = 0b0000011
    # store in main memory
    SOP = 0b0100011
    # branch (increment PC by imm based on rs1 and rs2 comparison)
    BOP = 0b1100011
    # jump...
    JIOP = 0b1101111
    # jump but with a register
    JROP = 0b1100111
    # environment ops (transfer control to OS / Debugger)
    ENVOP = 0b1110011
    # load immediate to rd
    LUOP = 0b0110111
    # load immediate + pc to rd
    LUPCOP = 0b0010111

class Regfile():
    def __init__(self):
        # x0 -> x31
        self.regs = [0] * 32

    def __getitem__(self, key):
        return self.regs[key]

    def __setitem__(self, key, value):
        # zero register, meant to keep constant value of 0
        if key == 0:
            return;
        # 32 bit limit to prevent 'overflow'
        self.regs[key] = value & 0xffffffff

class Instruction():

    def __init__(self, ins):
        self.binary = ins


    def Decode(self):
        def decode_field(start, end):
            return (self.binary >> start) & ((1 << (end + 1)) - 1)

        self.opcode = Opcodes(decode_field(0, 7))
        
        # same location in instruction for each type
        # store register addresses
        self.rs1 = decode_field(15, 19)
        self.rs2 = decode_field(20, 24)
        self.rd = decode_field(7, 11)

        self.funct3 = decode_field(12, 14)
        self.funct7 = decode_field(25, 31)

    def Parse(self):
        print("Parsing...")
        if self.opcode == Opcodes.ROP:
            print("register-register operation")


def step():

    # how do I implement pipelining?
    # https://en.wikipedia.org/wiki/Instruction_pipelining#/media/File:Pipeline,_4_stage.svg

    # https://en.wikipedia.org/wiki/Instruction_cycle

    # fetch
    ins = Instruction(regfile[PC])

    # decode
    ins.Decode()
    ins.Parse()

    # opcode takes up first 7 bits
    # but with little endian thats the last 7?

    # execute

if __name__ == "__main__":
    PC = 31
    regfile = Regfile()

    regfile[0] = 0x00000000
    # open up executable files
    # open them in elf format?
    # extract register data and
    # store it in the core's 'register file'
    regfile[PC] = 0x00000033
    step()
