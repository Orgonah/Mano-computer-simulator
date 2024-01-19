from memories import AllMemory

class F1:
    def __init__(self, memory: AllMemory) -> None:
        self.memory = memory
        self.opt = ['000', '001', '010', '011', '100', '101', '110', '111']
        self.func = [self.isz_000, self.isz_001, self.isz_010, self.isz_011, self.isz_100, self.isz_101, self.isz_110, self.isz_111]
    
    def instruction(self, inst: str):
        for i in range(len(self.opt)):
            if inst == self.opt[i]:
                self.func[i]()
                break
    
    def isz_000(self):
        pass

    def isz_001(self):
        self.memory.AC.write(self.memory.AC.read_dec()+ self.memory.DR.read_dec(), "d")

    def isz_010(self):
        self.memory.AC.write("0b0", "b")

    def isz_011(self):
        self.memory.AC.write(self.memory.AC.read_dec()+1, "d")

    def isz_100(self):
        self.memory.AC.write(self.memory.DR.read_dec(), "d")

    def isz_101(self):
        self.memory.AR.write('0b'+self.memory.DR.read_binary()[-11:], "b")

    def isz_110(self):
        self.memory.AR.write(self.memory.PC.read_binary(), "b")

    def isz_111(self):
        self.memory.main_memory.write(self.memory.AR.read_dec(), self.memory.DR.read_binary(), "b")

class F2:
    def __init__(self, memory: AllMemory) -> None:
        self.memory = memory
        self.opt = ['000', '001', '010', '011', '100', '101', '110', '111']
        self.func = [self.isz_000, self.isz_001, self.isz_010, self.isz_011, self.isz_100, self.isz_101, self.isz_110, self.isz_111]
    
    def instruction(self, inst):
        for i in range(len(self.opt)):
            if inst == self.opt[i]:
                self.func[i]()
                break

    def isz_000(self):
        pass

    def isz_001(self):
        self.memory.AC.write(self.memory.AC.read_dec() - self.memory.DR.read_dec(), "d")

    def isz_010(self):
        self.memory.AC.write(self.memory.AC.read_dec() | self.memory.DR.read_dec(), "d")

    def isz_011(self):
        self.memory.AC.write(self.memory.AC.read_dec() & self.memory.DR.read_dec(), "d")

    def isz_100(self):
        self.memory.DR.write(self.memory.main_memory.read(self.memory.AR.read_dec(), 'd'), "d")

    def isz_101(self):
        self.memory.DR.write(self.memory.AC.read_dec(), "d")

    def isz_110(self):
        self.memory.DR.write(self.memory.DR.read_dec() + 1, "d")

    def isz_111(self):
        self.memory.DR.assign_bits(self.memory.PC.read_binary(), 0, 10)

class F3:
    def __init__(self, memory: AllMemory) -> None:
        self.memory = memory
        self.opt = ['000', '001', '010', '011', '100', '101', '110', '111']
        self.func = [self.isz_000, self.isz_001, self.isz_010, self.isz_011, self.isz_100, self.isz_101, self.isz_110, self.isz_111]
    
    def instruction(self, inst):
        for i in range(len(self.opt)):
            if inst == self.opt[i]:
                self.func[i]()
                break

    def isz_000(self):
        pass

    def isz_001(self):
        self.memory.AC.write(self.memory.AC.read_dec() ^ self.memory.DR.read_dec(), "d")

    def isz_010(self):
        ans = '0b'
        for i in self.memory.AC.read_binary()[2:]:
            ans += '0' if i == '1' else '1'
        self.memory.AC.write(ans, "b")

    def isz_011(self):
        self.memory.AC.write(self.memory.AC.read_dec() << 1, "d")

    def isz_100(self):
        self.memory.AC.write(self.memory.AC.read_dec() >> 1, "d")

    def isz_101(self):
        self.memory.PC.write(self.memory.PC.read_dec()+1, "d")

    def isz_110(self):
        self.memory.PC.write(self.memory.AR.read_dec(), "d")

    def isz_111(self):
        exit()

class CD:
    def __init__(self, mem: AllMemory) -> None:
        self.mem = mem
        self.CD_opt = ['00', '01', '10', '11']
        self.CD_func = [self.U, self.I, self.S, self.Z]

    def insruction(self, CD: str):
        for i in range(len(self.CD_opt)):
            if CD == self.CD_opt[i]:
                return self.CD_func[i]()


    def U(self):
        return True

    def I(self):
        return self.mem.DR.read_binary()[2] == '1'

    def S(self):
        return self.mem.AC.read_binary()[2] == '1'

    def Z(self):
        return self.mem.AC.read_dec() == 0
    
class BR:
    def __init__(self, mem: AllMemory) -> None:
        self.mem = mem
        self.opt = ['00', '01', '10', '11']
        self.func = [self.JMP, self.CALL, self.RET, self.MAP]

    def insruction(self, BR: str):
        for i in range(len(self.opt)):
            if BR == self.opt[i]:
                return self.func[i]()
    
    def AD(self):
        return self.mem.control_memory.read(self.mem.CAR.read_dec(), 'b')[-7:]

    def JMP(self):
        self.mem.CAR.write('0b'+self.AD(), "b")
    
    def CALL(self):
        self.mem.SBR.write(self.mem.CAR.read_dec() + 1, "d")
        self.mem.CAR.write('0b'+self.AD(), "b")

    def RET(self):
        self.mem.CAR.write(self.mem.SBR.read_dec(), "d")
    
    def MAP(self):
        opt = '0b0' + self.mem.DR.read_binary()[2:][1:5]+'00'
        self.mem.CAR.write(opt, "b")


