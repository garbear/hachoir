"""
Integer field classes:
- UInt8, UInt16, UInt24, UInt32, UInt64: unsigned integer of 8, 16, 32, 64 bits ;
- UInt16BE, UInt16LE, UInt24BE, UInt24LE, UInt32BE, UInt32LE, UInt64BE, UInt64LE:
        interpreted in the specified byte order regardless of the parent FieldSet's endianness.
- Int8, Int16, Int24, Int32, Int64: signed integer of 8, 16, 32, 64 bits.
- Int16BE, Int16LE, Int24BE, Int24LE, Int32BE, Int32LE, Int64BE, Int64LE:
        big- and little-endian signed integer counterparts.
"""

from hachoir_core.endian import BIG_ENDIAN, MIDDLE_ENDIAN, LITTLE_ENDIAN
from hachoir_core.field import Bits, FieldError

class GenericInteger(Bits):
    """
    Generic integer class used to generate other classes.
    """
    def __init__(self, parent, name, signed, endian, size, description=None):
        if not (8 <= size <= 16384):
            raise FieldError("Invalid integer size (%s): have to be in 8..16384" % size)
        Bits.__init__(self, parent, name, size, description)
        self.signed = signed
        self.endian = endian or self._parent.endian

    def createValue(self):
        return self._parent.stream.readInteger(
            self.absolute_address, self.signed, self._size, self.endian)

def integerFactory(name, is_signed, endian_override, size, doc):
    assert endian_override in (None, BIG_ENDIAN, MIDDLE_ENDIAN, LITTLE_ENDIAN)
    class Integer(GenericInteger):
        __doc__ = doc
        static_size = size
        def __init__(self, parent, name, description=None):
            GenericInteger.__init__(self, parent, name, is_signed, endian_override, size, description)
    cls = Integer
    cls.__name__ = name
    return cls

UInt8 = integerFactory("UInt8", False, None, 8, "Unsigned integer of 8 bits")
UInt16 = integerFactory("UInt16", False, None, 16, "Unsigned integer of 16 bits")
UInt24 = integerFactory("UInt24", False, None, 24, "Unsigned integer of 24 bits")
UInt32 = integerFactory("UInt32", False, None, 32, "Unsigned integer of 32 bits")
UInt64 = integerFactory("UInt64", False, None, 64, "Unsigned integer of 64 bits")

UInt16BE = integerFactory("UInt16", False, BIG_ENDIAN, 16, "Unsigned integer of 16 bits (big-endian)")
UInt24BE = integerFactory("UInt24", False, BIG_ENDIAN, 24, "Unsigned integer of 24 bits (big-endian)")
UInt32BE = integerFactory("UInt32", False, BIG_ENDIAN, 32, "Unsigned integer of 32 bits (big-endian)")
UInt64BE = integerFactory("UInt64", False, BIG_ENDIAN, 64, "Unsigned integer of 64 bits (big-endian)")

UInt16LE = integerFactory("UInt16", False, LITTLE_ENDIAN, 16, "Unsigned integer of 16 bits (little-endian)")
UInt24LE = integerFactory("UInt24", False, LITTLE_ENDIAN, 24, "Unsigned integer of 24 bits (little-endian)")
UInt32LE = integerFactory("UInt32", False, LITTLE_ENDIAN, 32, "Unsigned integer of 32 bits (little-endian)")
UInt64LE = integerFactory("UInt64", False, LITTLE_ENDIAN, 64, "Unsigned integer of 64 bits (little-endian)")

Int8 = integerFactory("Int8", True, None, 8, "Signed integer of 8 bits")
Int16 = integerFactory("Int16", True, None, 16, "Signed integer of 16 bits")
Int24 = integerFactory("Int24", True, None, 24, "Signed integer of 24 bits")
Int32 = integerFactory("Int32", True, None, 32, "Signed integer of 32 bits")
Int64 = integerFactory("Int64", True, None, 64, "Signed integer of 64 bits")

Int16BE = integerFactory("Int16", True, BIG_ENDIAN, 16, "Signed integer of 16 bits (big-endian)")
Int24BE = integerFactory("Int24", True, BIG_ENDIAN, 24, "Signed integer of 24 bits (big-endian)")
Int32BE = integerFactory("Int32", True, BIG_ENDIAN, 32, "Signed integer of 32 bits (big-endian)")
Int64BE = integerFactory("Int64", True, BIG_ENDIAN, 64, "Signed integer of 64 bits (big-endian)")

Int16LE = integerFactory("Int16", True, LITTLE_ENDIAN, 16, "Signed integer of 16 bits (little-endian)")
Int24LE = integerFactory("Int24", True, LITTLE_ENDIAN, 24, "Signed integer of 24 bits (little-endian)")
Int32LE = integerFactory("Int32", True, LITTLE_ENDIAN, 32, "Signed integer of 32 bits (little-endian)")
Int64LE = integerFactory("Int64", True, LITTLE_ENDIAN, 64, "Signed integer of 64 bits (little-endian)")

