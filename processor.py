from memories import AllMemory
from instruct import F1,F2,F3,CD,BR

class CPU:
    def __init__(self, memory=AllMemory()) -> None:
        self.memory = memory
        self.f1 = F1(self.memory)
        self.f2 = F2(self.memory)
        self.f3 = F3(self.memory)
        self.CD = CD(self.memory)
        self.BR = BR(self.memory)
        self.memory = memory

    def clock(self):
        self.memory.reset_flag()
        opt = self.memory.control_memory.read(self.memory.CAR.read_dec(), 'b')[2:]
        if(opt[0:3]=='100' and opt[3:6]=='101'):
            temp = self.memory.AC
            self.memory.AC = self.memory.DR
            self.memory.DR = temp
        else:
            self.f1.instruction(opt[0:3])
            self.f2.instruction(opt[3:6])
        self.f3.instruction(opt[6:9])
        if self.CD.insruction(opt[9:11]):
            self.BR.insruction(opt[11:13])
        else:
            self.memory.CAR.write(self.memory.CAR.read_dec() + 1, "d")
        if self.memory.check_flags():
            raise("Error in CPU, Write in the same space twice in the same clock cycle")
