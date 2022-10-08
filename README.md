# C Header to Python

Convert the data structures in a c header to their python equivalent

## How to use:
* Anything to be converted must be typedef'd
* The typedef'd name must be on a line starting with a }
* Define guards should have a clear line below and above
* Use #defines in the target header to select what should be converted
    ```c
    #define PYTHON_CONVERT_ENUM_START
    #define PYTHON_CONVERT_ENUM_END
    #define PYTHON_CONVERT_STRUCT_START
    #define PYTHON_CONVERT_STRUCT_END
    ```

### Command line args:
```
    -h, --help            show this help message and exit
    -s, --source          Source filename
    -d, --dest            Destination filename
    --clear_flags         Clear define startments in source header after copying
    --comments            Copy comments to the destination
```
## Note:
* Any type casting applied to c enum values will be stripped from the python version

## Examples:
### Enum

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