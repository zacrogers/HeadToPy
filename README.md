# C Header to Python

Convert the data structures in a c header to their python equivalent

## How to use:
* Anything to be converted must be typedef'd
* Use #defines in the target header to select what should be converted
    ```c
    #define PYTHON_CONVERT_ENUM_START
    #define PYTHON_CONVERT_ENUM_END
    #define PYTHON_CONVERT_STRUCT_START
    #define PYTHON_CONVERT_STRUCT_END
    ```

## Note:
    * Any type casting applied to c enum values will be stripped from the python version

## Examples:
* Enum
    ``` c
    #define PYTHON_CONVERT_ENUM_START

    typedef enum
    {
        OK = 0x00,
        ERROR = 0x01
    } enum_name_e;

    #define PYTHON_CONVERT_ENUM_END
    ```
    ```python
    from enum import Enum

    class EnumName(Enum):
        OK = 0x00
        ERROR = 0x01
    ```