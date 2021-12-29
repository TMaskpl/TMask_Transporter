#!/usr/bin/python

__author__ = "biuro@tmask.pl"
__copyright__ = "Copyright (C) 2021 TMask.pl"
__license__ = "MIT License"
__version__ = "1.0"


import os
import sys
import string
import platform
import re
import datetime

# --- Zmienne ---

# path = '/home/Python/search_and_del/'
# ext = 'txt'


# Przeszukaj cały system i znajdz konkretny plik
def searchFilesLinuxWindows():
    req_file = input("Enter your file name to search: ")

    if platform.system() == "Windows":
        pd_names = string.ascii_uppercase
        vd_names = []
        for each_drive in pd_names:
            if os.path.exists(each_drive+":\\"):
                #print(each_drive)
                vd_names.append(each_drive+":\\")
        print(vd_names)
        for each_drive in vd_names:
            for r, d, f in os.walk(each_drive):
                for each_f in f:
                    if each_f == req_file:
                        print(os.path.join(r, each_f))
    else:
        for r, d, f in os.walk("/"):
            for each_file in f:
                if each_file == req_file:
                    print(os.path.join(r, each_file))

# Znajdz pliki albp np ext = 'txt'
def searchAllFilesExt(path, ext):
    list = []
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            if fname.endswith(ext):
                list.append(fname)
    return list

# Znajdz wszystkie * pliki 
def searchAllFiles(path):
    list = []
    for dirpath, dirs, files in os.walk(path):
        for filename in files:
            fname = os.path.join(dirpath, filename)
            list.append(fname)
    return list

# Znajdz listę plików pasujących do regex pattern
def searchAllFilesRgex(full_path, pattern):
    req_file = full_path
    list = [] 
    
    if platform.system() == "Windows":
        pd_names = string.ascii_uppercase
        vd_names = []
        for each_drive in pd_names:
            if os.path.exists(each_drive+":\\"):
                #print(each_drive)
                vd_names.append(each_drive+":\\")
        print(vd_names)
        for each_drive in vd_names:
            for r, d, f in os.walk(each_drive):
                for each_f in f:
                    if each_f == req_file:
                        print(os.path.join(r, each_f))
    else:
        for r, d, f in os.walk(full_path):
            for each_file in f:
                # print(each_file)
                result = re.match(pattern, each_file)
                if result:
                    list.append(os.path.join(r, each_file))
    return list

# Usuń pliki starsze niz np days=2
def delFilesOlder(list_files, days):
    today = datetime.datetime.now()
    age = days
    for each_file in list_files:
        file_cre_date = datetime.datetime.fromtimestamp(
            os.path.getctime(each_file))
        
        dif_days=(today-file_cre_date).days
        if dif_days > age:
            print(
                f'Delete --> {each_file} - {file_cre_date}   -->  {dif_days} days old')
            os.remove(each_file)

# Usuń pliki
def delFiles(list_files):
    today = datetime.datetime.now()
    for each_file in list_files:
        file_cre_date = datetime.datetime.fromtimestamp(
            os.path.getctime(each_file))
        print(f'Delete --> {each_file} - {file_cre_date}')
        os.remove(each_file)



# Funkcja główna
def main():
    # searchFilesLinuxWindows()
    # print(searchAllFiles('/home/Pobrane'))
    # print(searchAllFilesExt('/home/Pobrane', 'tar'))
    # list_del_files = searchAllFilesExt('/home/Pobrane', 'pdf')
    # print(list)
    # delFilesOlder(list_del_files, 0)
    # delFiles(list_del_files)
    print(searchAllFilesRgex('/home/dniemczok/Pobrane', '.*KRIS.*'))
    
if __name__ == "__main__":
    main()
