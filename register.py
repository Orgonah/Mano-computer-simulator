from math import ceil


class Register:
    def __init__(self, number_of_bits: int = 16, initial_value: str = "0b0") -> None:
        initial_value = self.check_bainary_format(initial_value)

        self.number_of_bits = number_of_bits
        self._reg_value = initial_value
        self._flag = 0

    def reset_flag(self):
        self._flag = 0

    def check_flag(self):
        return self._flag > 1

    def test_bits(self, value: str) -> bool:
        for bit in value:
            if bit != '0' and bit != '1':
                return False
        return True

    def check_bainary_format(self, value: str) -> str:
        if value[:2] != '0b':
            raise Exception("The value should be in binary format with '0b' prefix")
        value = value[2:]

        if self.test_bits(value) == False:
            raise Exception("The value should be in binary format consisting of 0s and 1s")
        
        return value

    @property
    def _reg_value(self):
        return self._value
    
    @_reg_value.setter
    def _reg_value(self, value: str):
        self._value = self.normalize(value)

    def assign_bits(self, value: str, start: int, end: int):
        self._flag += 1

        value = self.check_bainary_format(value)

        if end - start + 1 != len(value):
            raise Exception("The length of the value should be equal to end-start+1")
        if end >= self.number_of_bits:
            raise Exception("The end should be less than the number of bits")
        if start < 0:
            raise Exception("The start should be positive")
        if start > end:
            raise Exception("The start should be less than or equal to end")
        end = self.number_of_bits - start - 1
        start = self.number_of_bits - end - 1
        self._reg_value = self._reg_value[:start] + value + self._reg_value[end + 1:]

    def normalize(self, value: str):
        if len(value) <= self.number_of_bits:
            value = "0" * (self.number_of_bits - len(value)) + value
        elif len(value) > self.number_of_bits:
            value = value[-self.number_of_bits:]
        return value

    def write(self, value: str, type: str):
        self._flag += 1
        if type == "b":
            value = self.check_bainary_format(value)
            self._reg_value = value

        elif type == 'd':
            self._reg_value = bin(int(value))[2:]
        elif type == 'h':
            self._reg_value = bin(int(value, 16))[2:]

    def read_binary(self) -> str:
        return '0b' + self._reg_value

    def read_hex(self) -> str:
        output = hex(int(self._reg_value, 2))[2:]
        len_out = ceil(self.number_of_bits / 4)
        if len(output) < len_out:
            output = "0" * (len_out - len(output)) + output
        return '0x' + output 

    def read_dec(self) -> int:
        return int(self._reg_value, 2)
