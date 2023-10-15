import math
from typing import Any

types_env = {}

class BoolType:
    pass

class NumberType:
    def add(self, other):
        if other.__lt__(self) or self.__eq__(other):
            return self
        elif self.__lt__(other):
            return other
        else:
            raise BaseException("Cannot " + repr(self) + " with " + repr(other))
    
    def minus(self, other):
        return self.add(other)
    
    def mul(self, other):
        return self.add(other)
    
    def div(self, other):
        return self.add(other)
    
    def conj(self):
        return self
    
    def re(self):
        return types_env['float']
    
    def im(self):
        return types_env['float']
    
    def dsp_conj(self, v):
        return v.conjugate()
    
    def dsp_re(self, v):
        return v.real
    
    def dsp_im(self, v):
        return v.imag
    
    def __lt__(self, other):
        return False
    
    def __repr__(self):
        return "NumberType()"
    
    def __eq__(self, other: object) -> bool:
        return other.__class__ == self.__class__
    
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    
    def __gt__(self, other):
        return other.__lt__(self)
    
    def __ge__(self, other):
        return self.__eq__(other) or other.__lt__(self)

class ComplexType(NumberType):
    def __init__(self, nb_bits=None):
        self.nb_bits = nb_bits

    def __lt__(self, other):
        return other.__class__ == NumberType
    
    def __repr__(self):
        return "ComplexType(" +str(self.nb_bits) + ")"
    
    def __eq__(self, other: object) -> bool:
        return other.__class__ == self.__class__ and self.nb_bits == other.nb_bits

class FloatType(ComplexType):
    def __init__(self, nb_bits=None):
        self.nb_bits = nb_bits

    def __repr__(self):
        return "FloatType(" +str(self.nb_bits) + ")"

    def __lt__(self, other):
        if other.__class__ in [ComplexType, NumberType]:
            return True
        elif other.__class__ == FloatType:
            if self.nb_bits is None:
                return False
            if other.nb_bits is None:
                return True
            return self.nb_bits < other.nb_bits
        elif other.__class__ == IntegerType:
            return False
        raise NotImplementedError
    
    def __eq__(self, other: object) -> bool:
        return other.__class__ == self.__class__ and self.nb_bits == other.nb_bits

class IntegerType(FloatType):
    def __init__(self, is_signed=True, nb_bits=None):
        self.is_signed = is_signed
        self.nb_bits = nb_bits

    def __repr__(self):
        return "IntegerType("+ str(self.is_signed) + ", " + str(self.nb_bits) + ")"

    def __lt__(self, other: object) -> bool:
        if other.__class__ in [FloatType, ComplexType, NumberType]:
            return True
        elif other.__class__ == IntegerType:
            if self.is_signed == other.is_signed:
                if other.nb_bits is None:
                    return self.nb_bits != None
                else:
                    if self.nb_bits is None:
                        return other.nb_bits != None
                    else:
                        return self.nb_bits < other.nb_bits
            else:
                return other.nb_bits is None
        raise BaseException("aie")
    
    def __eq__(self, other: object) -> bool:
        return other.__class__ == self.__class__ \
                and self.nb_bits == other.nb_bits \
                and self.is_signed == other.is_signed

class MatrixType:
    def transpose(self):
        return self
    
    def __eq__(self, other: object) -> bool:
        return other.__class__ == MatrixType
    
    def __lt__(self, other):
        return False
    
    def __le__(self, other):
        return self.__eq__(other) or self.__lt__(other)
    
    def __gt__(self, other):
        return not self.__le__(other)
    
    def __ge__(self, other):
        return not self.__lt__(other)

class StreamType:
    def __init__(self, innerType) -> None:
        self.innerType = innerType

    def __getattr__(self, __name: str) -> Any:
        innerMthd = getattr(self.innerType, __name, None)
        if innerMthd:
            return lambda *x: StreamType(innerMthd(*x))
        raise AttributeError
    
    def __lt__(self, other):
        if other.__class__ == StreamType:
            return self.innerType < other.innerType
        return NotImplementedError
    
    def __eq__(self, other: object) -> bool:
        return other.__class__ == self.__class__ and self.innerType == other.innerType

types_env['u8'] = IntegerType(False, 8)
types_env['u16'] = IntegerType(False, 16)
types_env['u32'] = IntegerType(False, 32)

types_env['i8'] = IntegerType(True, 8)
types_env['i16'] = IntegerType(True, 16)
types_env['i32'] = IntegerType(True, 32)

types_env['natural'] = IntegerType(False)
types_env['integer'] = IntegerType(True)

types_env['f32'] = FloatType(32)
types_env['f64'] = FloatType(64)
types_env['float'] = FloatType()

types_env['c32'] = ComplexType(32)
types_env['c64'] = ComplexType(64)
types_env['complex'] = ComplexType()

types_env['number'] = NumberType()

for k, t in types_env.copy().items():
    types_env['stream<' + k + '>'] = StreamType(t)

types_env['matrix'] = MatrixType()
