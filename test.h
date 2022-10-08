#include <stdint.h>
#define PYTHON_CONVERT_ENUM_START


typedef enum
{
	CGB_SUPPORT       = (uint8_t)0x80,
	CGB_ONLY          = 0xC0

}cgb_flag_e;


typedef enum
{
	NONE              = (uint16_t)0x0000,
	NINTENDO_RND      = (uint16_t)0x0001,
	CAPCOM            = (uint16_t)0x0008
}new_licensee_code_e;

#define PYTHON_CONVERT_ENUM_END

#define PYTHON_CONVERT_ENUM_START

typedef enum
{
	SGB_NO            = (uint8_t)0x00,
	SGB_SUPPORT       = 0x03
}sgb_flag_e;


typedef enum
{
	ROM_ONLY          = (uint8_t)0x00,
	MBC1              = 0x01,
	MBC1_RAM          = 0x02,
	MBC1_RAM_BATT     = 0x03,
	MBC2              = 0x05,
	MBC2_BATT         = 0x06,
	ROM_RAM           = 0x08,
	ROM_RAM_BATT      = 0x09,
	MM01              = 0x0B,
	MM01_RAM          = 0x0C,
	MM01_RAM_BATT     = 0x0D,
	MBC3_TIM_BATT     = 0x0F,
	MBC3_TIM_RAM_BATT = 0x10,
	MBC3              = 0x11,
	MBC3_RAM          = 0x12,
	MBC3_RAM_BATT     = 0x13,
	MBC5              = 0x19,
	MBC5_RAM          = 0x1A,
	MBC5_RAM_BATT     = 0x1B,
	MBC5_RUMBLE       = 0x1C,
	MBC5_RUM_RAM      = 0x1D,
	MBC5_RUM_RAM_BATT = 0x1E,
	MBC6              = 0x20,
	MBC7_SEN_RU_RA_BA = 0x22,   // MBC7+SENSOR+RUMBLE+RAM+BATTERY
	POCKET_CAMERA     = 0xFC,
	BANDAI_TAMA5      = 0xFD,
	HUC3              = 0xFE,
	HUC1_RAM_BATT     = 0xFF
}cart_type_e;


typedef enum
{
	ROM_32KB          = (uint8_t)0x00,  // no rom banks
	ROM_64KB          = 0x01,  // 4 banks
	ROM_128KB         = 0x02,  // 8 banks
	ROM_256KB         = 0x03,  // 16 banks
	ROM_512KB         = 0x04,  // 32 banks
	ROM_1MB           = 0x05,  // 64 banks - only 63 banks used by MBC1
	ROM_2MB           = 0x06,  // 128 banks - only 125 banks used by MBC1
	ROM_4MB           = 0x07,  // 256 banks
	ROM_8MB           = 0x08,  // 512 banks
	ROM_1_1MB         = 0x52,  // 72 banks
	ROM_1_2MB         = 0x53,  // 80 banks
	ROM_1_5MB         = 0x54   // 96 banks
}rom_size_e;


typedef enum
{
	RAM_NONE          = (uint8_t)0x00,
	RAM_2KB           = 0x01,
	RAM_8KB           = 0x02,
	RAM_32KB          = 0x03,  // 4 banks of 8kB
	RAM_128KB         = 0x04,  // 16 banks of 8kB
	RAM_64KB          = 0x05   // 8 banks of 8kB
}ram_size_e;


typedef enum
{
	JAP    = (uint8_t)0x00,
	NO_JAP = 0x01
}dest_code_e;

#define PYTHON_CONVERT_ENUM_END

#define PYTHON_CONVERT_STRUCT_START

typedef struct
{
	int cats;
	uint8_t hats;
}another_struct_t;


typedef struct
{
	uint8_t             entry_point[ENTRY_POINT_LEN];
	char                rom_title[ROM_TITLE_LEN];
	new_licensee_code_e new_licensee_code;
	sgb_flag_e          sgb_flag;
	cart_type_e         cart_type;
	rom_size_e          rom_size;
	ram_size_e          ram_size;
	dest_code_e         dest_code;
	uint8_t             old_licensee_code;
	uint8_t             mask_rom_ver_num;
	uint8_t             checksum;
}__attribute__((packed, aligned(1))) gb_metadata_t;

#define PYTHON_CONVERT_STRUCT_END
