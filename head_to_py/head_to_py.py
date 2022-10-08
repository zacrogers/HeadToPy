''' 
    Convert enums and structs in a c header to a python equivalent.
    It will only convert typedef'd enums and must be named in snake case. 
'''
import argparse
from enum import Enum
import re
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

class DefineGuard(Enum):
    ENUM_START   = "#define PYTHON_CONVERT_ENUM_START"
    ENUM_END     = "#define PYTHON_CONVERT_ENUM_END"
    STRUCT_START = "#define PYTHON_CONVERT_STRUCT_START"
    STRUCT_END   = "#define PYTHON_CONVERT_STRUCT_END"


''' Exceptions '''
class DefineGuardException(Exception):
    ...

class InvalidTypeException(Exception):
    ...

class DelimiterMatchException(Exception):
    ...


''' Enum processing '''
def _pythonize_enum_name(name: str) -> str:
    if name.count("_e") != 0:
        name = name.split("_e")[0]

    name = name.split("_")
    name = [name.capitalize() for name in name]
    return f"class {''.join(name)}(Enum):\n"


def _remove_enum_val_type(val: str):
    ''' remove things like (uint8_t) from value'''
    val = val.split(")")
    if len(val) > 1:
        val = val[1]
    else:
        val = val[0]
    return val


def _pythonize_enum_values(vals: str, copy_comments: bool) -> str:
    vals   = vals.split(",")
    output = ""

    for v in vals:
        val   = v.split("=")
        label = val[0]
        val   = val[-1]
                
        # get rid of comments for now
        if label.count("//") == 1: 
            label = label.split("\n\t")[0]

        label = label.strip("\n\t").strip(" ")
        val   = _remove_enum_val_type(val)

        if (label.count("//") == 0): 
            output += f"    {label} = {val}\n"

    return output


def _parse_enums(data: str, copy_comments: bool, add_import=True) -> str:
    enums = data.split("typedef enum")
    py_enums = ""

    if add_import:
        py_enums = "from enum import Enum\n\n"

    for e in enums:
        if e.count("{") != 0:
            vals = e.split("{")[1].split("}")
            name = vals[-1].split(";")[0]
            py_name = _pythonize_enum_name(name)

            if py_name == False:
                break
            
            py_vals = _pythonize_enum_values(vals[0], copy_comments)
            py_enums += f"{py_name}{py_vals}\n"

    return py_enums


''' Struct to dataclass processing '''
VALID_C_INT= [
    'char',
    'signed char',
    'unsigned char',
    'short',
    'short int',
    'signed short',
    'signed short int',
    'unsigned short',
    'unsigned short int',
    'int',
    'signed',
    'signed int',
    'unsigned',
    'unsigned int',
    'long',
    'long int'
    # TODO: Fill out the rest.
    'int8_t',
    'int16_t',
    'int32_t',
    'uint8_t',
    'uint16_t',
    'uint32_t'
    # TODO: Fill out the rest.
]

VALID_C_FLOAT = {
    "float",
    'double',
    "long double"
}

VALID_C_STRING = [
    "char*",
    "char *"
]


def _defined_types(data: str):
    ''' Scan the header for all other struct types & enums defined within '''
    semi = data.split(";")
    types = []

    for s in semi:
        if s.count("}") != 0:
            type_name = s.split("}")[-1]

            if type_name.count(" ") > 0:
                type_name = type_name.split(" ")[-1]

            types.append(type_name)

    return types


def _is_array(data: str) -> bool:
    return (data.count("[") > 0) and (data.count("]") > 0)


def _pythonize_struct_name(name: str) -> str:
    name = name.strip("\n").replace("}", "")

    if name.count("_t") != 0:
        name = name.split("_t")[0]
    if name.count(" ") > 0:
        name = name.split(" ")[-1]

    name = name.split("_")
    name = [name.capitalize() for name in name]
    return f"@dataclass\nclass {''.join(name)}:\n"


def _pythonize_type_name(name: str) -> str:
    name = name.strip("\n").replace("}", "")

    if name.count("_t") != 0:
        name = name.split("_t")[0]
    if name.count("_e") != 0:
        name = name.split("_e")[0]
    if name.count(" ") > 0:
        name = name.split(" ")[-1]

    name = name.split("_")
    return ''.join([name.capitalize() for name in name])


def _pythonize_struct_values(data: str, defined_types: list[str]):
    data = data.strip("{").replace("\n", "").replace("\t", "")
    lines = data.split(";")
    lines = [d for d in lines if d != ""]
    output = ""

    for line in lines:
        if line.count(" ") > 0:
            line = line.split(" ")
            _type = line[0]
            var_name = line[-1]

            if _type in VALID_C_INT:
                _type = "int"
            elif _type in VALID_C_FLOAT:
                _type = "float"
            elif _type in VALID_C_STRING:
                _type = "str"
            elif _type in defined_types:
                _type = _pythonize_type_name(_type)
            else:
                raise InvalidTypeException("Type is not a standard c type and cannot be found in the header.")                

            if _is_array(var_name):
                output += f"    {var_name.split('[')[0]}: list[{_type}]\n"
            else:
                output += f"    {var_name}: {_type}\n"

    return f"{output}\n\n" 


def _parse_structs(data: str, copy_comments: bool, defined_types: list[str], add_import=True):
    s_start = [s.start() for s in re.finditer("{", data)] # start of fields
    s_end = [s.start() for s in re.finditer("}", data)]   # end of fields
    s_semi = [s.start() for s in re.finditer(";", data)]  # semicolons

    # get locations of semicolons after typedef names
    s_name = []

    for i in range(len(s_start)):
        if i < len(s_start)-1:
            s_name += list(filter(lambda s: (s > s_end[i]) and (s < s_start[i+1]), s_semi))
        else:
            s_name += list(filter(lambda s: (s > s_end[i]) and (s < len(data)), s_semi))
    
    if (len(s_start) != len(s_name)) and (len(s_end) != len(s_name)):
        raise DelimiterMatchException("The number of each delimiter { } ; must match.")

    output = ""
    if add_import:
        output = "from dataclasses import dataclass"

    for i in range(len(s_start)):
        output += _pythonize_struct_name(data[s_end[i]:s_name[i]])
        output += _pythonize_struct_values(data[s_start[i]:s_end[i]], defined_types)

    return output 


''' General functions '''
def _gather_marked_data(data: str) -> tuple[str, str]:
    ''' Gather all the data inside define guards. Assumes define guards have already been checked. '''
    enums  = ""
    e_section_starts = [s.start() for s in re.finditer(DefineGuard.ENUM_START.value, data)]
    e_section_ends = [s.start() for s in re.finditer(DefineGuard.ENUM_END.value, data)]

    for i, e in enumerate(e_section_starts):
        enums += data[e: e_section_ends[i]].strip(DefineGuard.ENUM_START.value)

    structs = ""
    s_section_starts = [s.start() for s in re.finditer(DefineGuard.STRUCT_START.value, data)]
    s_section_ends = [s.start() for s in re.finditer(DefineGuard.STRUCT_END.value, data)]

    for i, s in enumerate(s_section_starts):
        structs += data[s: s_section_ends[i]].strip(DefineGuard.STRUCT_START.value)

    return enums, structs


def _save_python_file(name: str, data: str) -> None:
    with open(name, "w") as f:        
        f.write(data)


def _check_define_guards(data: str) -> tuple[int, int]:
    n_enum_start   = data.count(DefineGuard.ENUM_START.value)
    n_enum_end     = data.count(DefineGuard.ENUM_END.value)
    n_struct_start = data.count(DefineGuard.STRUCT_START.value)
    n_struct_end   = data.count(DefineGuard.STRUCT_END.value)

    if n_enum_start != n_enum_end:
        raise DefineGuardException(
            f"Start and end guards should be equal. Provided: Enum start={n_enum_start}, Enum end={n_enum_end}."
        )

    if n_struct_start != n_struct_end:
        raise DefineGuardException(
            f"Start and end guards should be equal. Provided: Struct start={n_struct_start}, Struct end={n_struct_end}."
        )

    if (n_enum_start == 0) and (n_struct_start == 0):
        raise DefineGuardException("Zero define guards were found. This isn't going to do anything, silly billy.")

    return n_enum_start, n_struct_start


def _clear_header_flags(header_file: str):
    ''' Clear the header define guard flags '''
    old_head = ""
    with open(header_file, mode="r") as head:
        old_head = head.read()

    print(old_head)

    new_head = old_head.replace(f"\n{DefineGuard.ENUM_START.value}\n", "") 
    new_head = new_head.replace(f"\n{DefineGuard.ENUM_END.value}\n", "") 
    new_head = new_head.replace(f"\n{DefineGuard.STRUCT_START.value}\n", "") 
    new_head = new_head.replace(f"\n{DefineGuard.STRUCT_END.value}\n", "") 

    with open(f"1_{header_file}", mode="w") as head:
        head.write(new_head)


def convert(file_from: str, file_to: str, copy_comments=True, clear_flags=False) -> None:
    with open(file_from, mode="r") as f_from:
        logging.info(f"Loading {file_from}")
        data = f_from.read()
        try:
            n_enum, n_struct = _check_define_guards(data)
        except DefineGuardException as e:
            print(e)
            return

        e_data, s_data = _gather_marked_data(data)
        types = _defined_types(data) 

        logging.info(f"Converting")
        output_data = f"'''\n\tAutomatically generated by c_to_py from {file_from} on {datetime.now()}\n'''\n"

        if (n_enum > 0) and (n_struct == 0):
            output_data  = _parse_enums(e_data, copy_comments, add_import=True)

        elif (n_enum == 0) and (n_struct > 0):
            output_data  = _parse_structs(s_data, copy_comments, add_import=True)

        elif (n_enum > 0) and (n_struct > 0):
            output_data += "from enum import Enum\n"
            output_data += "from dataclasses import dataclass\n\n"
            output_data += _parse_enums(e_data, copy_comments, add_import=False)
            output_data += _parse_structs(s_data, copy_comments, types, add_import=False)
            
        logging.info(f"Saving to {file_to}")
        if output_data != "":
            _save_python_file(file_to, output_data)

    if clear_flags:
        _clear_header_flags(file_from)




def main():
    parser = argparse.ArgumentParser(description="Convert datatypes in c header to the python equivalent.")
    parser.add_argument("-s", "--source", help="Source filename")
    parser.add_argument("-d", "--dest", help="Destination filename")
    parser.add_argument(
        "--clear_flags", 
        action="store_true", 
        help="Clear define startments in source header after copying"
    )
    parser.add_argument(
        "--comments", 
        action="store_true", 
        help="Copy comments to the destination"
    )

    args = parser.parse_args()  

    if args.source and args.dest:
        convert(args.source, args.dest, args.comments, args.clear_flags)


if __name__ == "__main__":
    main()
    convert("test.h", 'testes.py')