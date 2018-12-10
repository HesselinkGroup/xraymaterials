import os
import pandas
import glob

pwd = os.path.dirname(os.path.abspath(__file__))
icru44_dir = os.path.join(pwd, "icru44")
elements_dir = os.path.join(pwd, "elements")

def _list_files(dir):
    files = glob.glob(os.path.join(dir, "*.txt"))
    return [os.path.splitext(os.path.basename(file))[0] for file in files]

def _load_file(dir, file_name):
    ext = os.path.splitext(file_name)
    if len(ext[1]) == 0:
        fname = file_name + ".txt"
    else:
        fname = file_name
    
    df = pandas.read_csv(os.path.join(dir, fname))
    return df


def list_icru44():
    return _list_files(icru44_dir)

def list_elements():
    return _list_files(elements_dir)

def load_element(element_name):
    return _load_file(elements_dir, element_name)

def load_icru44(material_name):
    return _load_file(icru44_dir, material_name)
