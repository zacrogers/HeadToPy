''' 
    Convert enums and constant defines in a c header to a python equivalent.
    It will only convert typedef'd enums and in snake case. 
    Use #define CONVERT_TO_PYTHON_START and #define CONVERT_TO_PYTHON_END to only 
    convert selected sections.
'''
from ast import parse
from pprint import pprint
import argparse
from enum import Enum, auto
import logging

logging.basicConfig(level=logging.INFO)

class CDataType(Enum):
    ENUM = auto()
    STRUCT = auto()


def _pythonize_enum_name(name: str) -> str:
    if name.count("_e") != 0:
        name = name.split("_e")[0]

    name = name.split("_")
    name = [name.capitalize() for name in name]
    return f"class {''.join(name)}(Enum):\n"


def _remove_type(val: str):
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
        val   = _remove_type(val)

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


def _save_python_file(name: str, data: str) -> None:
    with open(name, "w") as f:        
        f.write(data)


def convert(file_from: str, file_to: str, copy_comments=True) -> None:
    with open(file_from, mode="r") as f_from:
        logging.info(f"Loading {file_from}")
        data = f_from.read()
        logging.info(f"Converting")
        py_enums = _parse_enums(data, copy_comments)
        logging.info(f"Saving to {file_to}")
        _save_python_file(file_to, py_enums)


def main():
    parser = argparse.ArgumentParser(description="Convert datatypes in c header to the python equivalent.")
    parser.add_argument("-s", "--source", help="Source filename")
    parser.add_argument("-d", "--dest", help="Destination filename")

    args = parser.parse_args()  

    if args.source and args.dest:
        convert(args.source, args.dest)


if __name__ == "__main__":
    main()