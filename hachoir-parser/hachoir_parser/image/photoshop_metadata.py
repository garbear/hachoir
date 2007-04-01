from hachoir_core.field import (FieldSet, ParserError,
    UInt16,
    String, CString, PascalString8,
    NullBytes, RawBytes)
from hachoir_core.text_handler import hexadecimal
from hachoir_core.tools import alignValue, createDict
from hachoir_parser.image.iptc import IPTC

class Photoshop8BIM(FieldSet):
    TAG_INFO = {
        0x03ed: ("res_info", None, "Resolution information"),
        0x03f3: ("print_flg", None, "Print flags: labels, crop marks, colour bars, etc."),
        0x03f5: ("col_half_info", None, "Colour half-toning information"),
        0x03f8: ("color_trans_func", None, "Colour transfer function"),
        0x0404: ("iptc", IPTC, "IPTC/NAA"),
        0x0406: ("jpeg_qual", None, "JPEG quality"),
        0x0408: ("grid_guide", None, "Grid guides informations"),
        0x040a: ("copyright_flg", None, "Copyright flag"),
        0x040c: ("thumb_res2", None, "Thumbnail resource (2)"),
        0x040d: ("glob_angle", None, "Global lighting angle for effects"),
        0x0411: ("icc_tagged", None, "ICC untagged (1 means intentionally untagged)"),
        0x0414: ("base_layer_id", None, "Base value for new layers ID's"),
        0x0419: ("glob_altitude", None, "Global altitude"),
        0x041a: ("slices", None, "Slices"),
        0x041e: ("url_list", None, "Unicode URL's"),
        0x0421: ("version", None, "Version information"),
        0x2710: ("print_flg2", None, "Print flags (2)"),
    }
    TAG_NAME = createDict(TAG_INFO, 0)
    CONTENT_HANDLER = createDict(TAG_INFO, 1)
    TAG_DESC = createDict(TAG_INFO, 2)

    def __init__(self, *args, **kw):
        FieldSet.__init__(self, *args, **kw)
        tag = self["tag"].value
        if tag in self.TAG_NAME:
            self._name = self.TAG_NAME[tag]
        if tag in self.TAG_DESC:
            self._description = self.TAG_DESC[tag]
        size = self["size"]
        self._size = size.address + size.size + alignValue(size.value, 2) * 8

    def createFields(self):
        yield String(self, "signature", 4, "8BIM signature", charset="ASCII")
        if self["signature"].value != "8BIM":
            raise ParserError("Stream doesn't look like 8BIM item (wrong signature)!")
        yield UInt16(self, "tag", text_handler=hexadecimal)
        if self.stream.readBytes(self.absolute_address + self.current_size, 4) != "\0\0\0\0":
            yield PascalString8(self, "name")
            size = 2 + (self["name"].size // 8) % 2
            yield NullBytes(self, "name_padding", size)
        else:
            yield String(self, "name", 4, strip="\0")
        yield UInt16(self, "size")
        size = alignValue(self["size"].value, 2)
        if 0 < size:
            tag = self["tag"].value
            if tag in self.CONTENT_HANDLER:
                cls = self.CONTENT_HANDLER[tag]
                yield cls(self, "content", size=size*8)
            else:
                yield RawBytes(self, "content", size)

class PhotoshopMetadata(FieldSet):
    def createFields(self):
        yield CString(self, "signature", "Photoshop version")
        if self["signature"].value == "Photoshop 3.0":
            while not self.eof:
                yield Photoshop8BIM(self, "item[]")
        else:
            size = (self._size - self.current_size) / 8
            yield RawBytes(self, "rawdata", size)

