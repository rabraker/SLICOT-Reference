from pathlib import Path

from numpy.f2py import crackfortran

f2c_type_map = {
    'integer': 'int',
    'character': 'char',
    'double precision': 'double',
    'logical': 'bool',
    'complex': 'complex',
}

def make_const(in_type):
    return f"const {in_type} const*"

def arg_to_c_arg(name, arg_spec):
    c_type = f2c_type_map[arg_spec['typespec']]
    intent = arg_spec.get('intent', None)
    if intent is None:
        c_type += "*"
    elif intent == "input":
        c_type = make_const(c_type)
        assert None
    else:
        raise ValueError("Unknown intent: %s" % intent)

    notes = f'{name}: '
    for note in ['=', 'check', 'depend', 'attrspec']:
        if note in arg_spec:
            notes += f'{note}: {arg_spec[note]}, '

    return f"{c_type} {name}", notes.strip()

def parse_one_method(method_spec):
    name = method_spec['name']
    result = 'void'
    if 'result' in method_spec:
        result = f2c_type_map[method_spec['result']]

    signature = f"{result} {name}("
    doc_comment = "///"
    docstring = doc_comment
    num_args = len(method_spec['args'])

    for idx in range(num_args):
        arg_name = method_spec['args'][idx]
        c_arg, doc = arg_to_c_arg(arg_name, method_spec['vars'][arg_name])
        suffix = ", "
        doc_suffix = ""
        if idx == num_args-1:
            suffix = ");"
            doc_suffix = f"\n{doc_comment}"
        signature += c_arg + suffix
        docstring += "\n" + f"{doc_comment} {doc}{doc_suffix}"

    return signature, docstring


# def main(args):

# f = "slycot/src/SLICOT-Reference/src/AB01MD.f"
root = Path("slycot/src/SLICOT-Reference/src/")
files = root.glob("A*.f")
files = [str(f) for f in files][0:2]
output = Path("analysis.h")
output.unlink()
all_methods = crackfortran.crackfortran(files)
for method_spec in all_methods:
    with output.open("a+") as fid:
        signature, docstring = parse_one_method(method_spec)
        fid.write(docstring)
        fid.write("\n")
        fid.write(signature)
        fid.write("\n\n")

    print(docstring)
    print(signature)
    print()

# signature = ''.join(signature)
