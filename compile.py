#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on 2022年1月2日

@author: lishangchien
'''

import os
import shutil

def rename(path, oldName, moveForward):
    newName = f'{oldName.split(".")[0]}.{oldName.split(".")[-1]}'
    print(newName)
    os.rename(os.path.join(path, oldName),os.path.join(path, newName))
    shutil.move(os.path.join(path, newName),os.path.join(path, moveForward))

def compile_to_so(dirs):
    
    # remove all .py and .c file
    for dir_ in dirs:
        for file_ in os.listdir(dir_):
            if file_.endswith('.py') or file_.endswith('.c'):
                os.remove(os.path.join(dir_, file_))

        # move and rename all .pyc file in cache to last nest level
        cache = os.path.join(dir_, '__pycache__')
        for file_ in os.listdir(cache):
            if file_.endswith('.pyc'): rename(cache, file_, '../')

        # move .so file to it's original position also rename it
        so_cache = os.path.join(dir_, 'build/lib.linux-x86_64-3.7')
        for file_ in os.listdir(so_cache):
            dir_split = dir_.split('/')
            so_cache2 = so_cache
            for nest_level in range(1,len(dir_.split('/'))-1):
                so_cache2 = os.path.join(so_cache2, dir_.split('/')[nest_level])
            for file_deep in os.listdir(so_cache2):
                if file_deep.endswith('.so'): rename(so_cache2, file_deep, '../' * len(dir_split))

        # remove all unnecessary folder
        for folder in os.listdir(dir_):
            if folder.startswith('__pycache__'):
                os.rmdir(os.path.join(dir_, folder))
            if folder.startswith('build'):
                shutil.rmtree(os.path.join(dir_, folder), ignore_errors=True)

# compile py file to pyc
def compile_to_pyc(dirs):
    for dir_ in dirs:
        for file_ in os.listdir(dir_):
            if file_.endswith('.py'):
                os.remove(os.path.join(dir_, file_))

        # move and rename all .pyc file in cache to last nest level
        cache = os.path.join(dir_, '__pycache__')
        for file_ in os.listdir(cache):
            if file_.endswith('.pyc'): rename(cache, file_, '../')

        for folder in os.listdir(dir_):
            if folder.startswith('__pycache__'):
                os.rmdir(os.path.join(dir_, folder))


if __name__ == '__main__':
    dirs = ["./", "./lang/", "./src/", "./src/doc/", "./src/api/", "./src/ftpd/"]
    compile_to_so(dirs[:-1])
    compile_to_pyc([dirs[-1]])
