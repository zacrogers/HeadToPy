from enum import Enum

class CgbFlag(Enum):
    CGB_SUPPORT = 0x80
    CGB_ONLY =  0xC0


class NewLicenseeCode(Enum):
    NONE = 0x0000
    NINTENDO_RND = 0x0001
    CAPCOM = 0x0008
	# // TODO: more of these


class SgbFlag(Enum):
    SGB_NO = 0x00
    SGB_SUPPORT =  0x03


class CartType(Enum):
    ROM_ONLY = 0x00
    MBC1 =  0x01
    MBC1_RAM =  0x02
    MBC1_RAM_BATT =  0x03
    MBC2 =  0x05
    MBC2_BATT =  0x06
    ROM_RAM =  0x08
    ROM_RAM_BATT =  0x09
    MM01 =  0x0B
    MM01_RAM =  0x0C
    MM01_RAM_BATT =  0x0D
    MBC3_TIM_BATT =  0x0F
    MBC3_TIM_RAM_BATT =  0x10
    MBC3 =  0x11
    MBC3_RAM =  0x12
    MBC3_RAM_BATT =  0x13
    MBC5 =  0x19
    MBC5_RAM =  0x1A
    MBC5_RAM_BATT =  0x1B
    MBC5_RUMBLE =  0x1C
    MBC5_RUM_RAM =  0x1D
    MBC5_RUM_RAM_BATT =  0x1E
    MBC6 =  0x20
    MBC7_SEN_RU_RA_BA =  0x22
    BANDAI_TAMA5 =  0xFD
    HUC3 =  0xFE
    HUC1_RAM_BATT =  0xFF


class RomSize(Enum):
    ROM_32KB = 0x00

class RamSize(Enum):
    RAM_NONE = 0x00
    RAM_2KB =  0x01
    RAM_8KB =  0x02
    RAM_32KB =  0x03

class DestCode(Enum):
    JAP = 0x00
    NO_JAP =  0x01


