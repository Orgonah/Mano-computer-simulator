from register import Register

class Memory:
    def __init__(self, block_size: int, address_size: int) -> None:
        self.memory = []
        for i in range(2**address_size):
            self.memory.append(Register(block_size))

    def read(self, address: int, type: str):
        self._check_address(address)

        if type == "b":
            return self.memory[address].read_binary()
        elif type == 'd':
            return self.memory[address].read_dec()
        elif type == 'h':
            return self.memory[address].read_hex()

    def write(self, address: int, value: str, type: str):
        self._check_address(address)
        self.memory[address].write(value, type)

    def _check_address(self, address: int):
        if address < 0 or address >= len(self.memory):
            raise IndexError("Address out of bounds")
    
    def reset_flags(self):
        for i in self.memory:
            i.reset_flag()
    
    def check_flags(self):
        for i in self.memory:
            if i.check_flag():
                return True
        return False
