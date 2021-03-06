from typing import List
from .utility.utility.functions import read1, setcurpos, getcurpos, iswhitespace, get_filename_from_path, isalnum

def get_includes(filepath:str) -> List[str]:
    print('get_includes:', filepath)
    includes = []
    with open(filepath) as fin:
        while True:
            c = read1(fin)
            if not c:
                break

            elif c == '/':
                curpos = getcurpos(fin)
                c = read1(fin)
                if c == '/':    # ignoring single line comment
                    while c != '\n' and not not c:
                        c = read1(fin)

                elif c == '*':  # ignoring multi line comment
                    while True:
                        c = read1(fin)
                        curpos = getcurpos(fin)
                        if c == '*':
                            c = read1(fin)
                            if c == '/':
                                break
                            else:
                                setcurpos(fin, curpos)
                        elif not c:
                            break
                else:
                    setcurpos(fin, curpos)

            elif c == '"':  # ignoring string
                while True:
                    c = read1(fin)
                    if c == '\\':
                        c = read1(fin)
                    elif c == '"':
                        break
                    elif not c:
                        break

            elif c == '#':
                word = ''
                c = read1(fin)
                while iswhitespace(c):
                    c = read1(fin)
                while isalnum(c):
                    word += c
                    c = read1(fin)
                if word == 'include':
                    word = ''
                    while c != '"' and c != '<':
                        c = read1(fin)
                    c = read1(fin)
                    while c != '"' and c != '>':
                        word += c
                        c = read1(fin)
                    includes.append(get_filename_from_path(word))
    return includes


# -------------------------------------------------------
# ----- functions to get filepaths from a folder(s) -----
# -------------------------------------------------------

from os import listdir as os_listdir
from os.path import isfile as os_path_isfile, join as os_path_join, normpath as os_path_normpath

def myjoin(a:str, b:str):
    return os_path_normpath(os_path_join(a, b))

def get_filepaths_in_folder(folderpath:str, ignore:List[str], recursive:bool=False) -> List[str]:
    folderpath = os_path_normpath(folderpath)
    print('get_filepaths_in_folder:', folderpath)
    list_filepaths = []
    for f in os_listdir(folderpath):
        if f not in ignore:
            f_path = myjoin(folderpath, f)
            if os_path_isfile(f_path):
                list_filepaths.append(myjoin(folderpath, f))
            elif recursive:
                list_filepaths += get_filepaths_in_folder(f_path, ignore, recursive)

    return list_filepaths


def get_filepaths_in_folders(folderpaths:List[str], ignore:List[str], recursive:bool=False) -> List[str]:
    print('get_filepaths_in_folders')
    list_filepaths = []
    for folderpath in folderpaths:
        list_filepaths += get_filepaths_in_folder(folderpath, ignore, recursive)
    return list_filepaths


# -----------------------------------------------------------
# ----- function to get dependent-dependency tuple list -----
# -----------------------------------------------------------

from typing import Tuple

def get_dependent_dependeny_tuple_list(folderpaths:List[str], ignore:List[str] = [], ignore_outside_files:bool = False, recursive:bool = False) -> List[Tuple[str, str]]:
    print('get_dependent_dependeny_tuple_list')
    dependent_dependency_tuple_list = []
    filepaths = []
    inside_files = []

    for filepath in get_filepaths_in_folders(folderpaths, ignore, recursive):
        filepaths.append(filepath)
        inside_files.append(get_filename_from_path(filepath))

    for filepath in filepaths:
        includes = get_includes(filepath)
        for include in includes:
            if include not in ignore and (not ignore_outside_files or include in inside_files):
                dependent_dependency_tuple_list.append((get_filename_from_path(filepath), include))
    
    print('Returning dependent_dependency_tuple_list')
    return dependent_dependency_tuple_list