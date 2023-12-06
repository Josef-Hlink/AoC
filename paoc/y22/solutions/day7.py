#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" AoC 22 Day 7 - No Space Left On Device """

from paoc.helper import get_input, print_summary
import os


def p1() -> any:
    
    lines = get_input(7)

    # make a root directory
    root = '/'.join(__file__.split('/')[:-1] + ['root'])
    if not os.path.exists(root):
        os.mkdir(root)
    os.chdir(root)

    for line in lines[1:]:
        if line.startswith('$ cd'):
            directory = line.split(' ')[2]
            if not os.path.exists(directory) and not directory in ['..', '/']:
                os.mkdir(directory)
            if directory == '/':
                directory = root
            os.chdir(directory)
        elif line.startswith('$ ls'):
            pass
        else:
            size, filename = line.split(' ')
            if line.startswith('dir'):
                if not os.path.exists(filename):
                    os.mkdir(filename)
            else:
                with open(filename, 'w') as f:
                    f.write(size)
    
    # we have a directory structure with files and directories
    # we can now calculate the size of each directory
    dirs = {}
    for dirname, _, filenames in os.walk(root):
        size = 0
        for filename in filenames:
            with open(os.path.join(dirname, filename), 'r') as f:
                size += int(f.read())
        dirs[dirname] = size
    
    # remove everything inside the root directory
    for rt, ds, fs in os.walk(root, topdown=False):
        for f in fs:
            os.remove(os.path.join(rt, f))
        for d in ds:
            os.rmdir(os.path.join(rt, d))

    # remove the root directory itself
    os.rmdir(root)
    
    # to get the actual sizes (recursive), we need to add
    # the size of the child directory to the size of the parent directory
    for dirname in sorted(dirs, reverse=True):
        if dirname == root:
            continue
        parent = '/'.join(dirname.split('/')[:-1])
        dirs[parent] += dirs[dirname]
    
    # now we can filter the directories that have a size of 100000
    total = 0
    for dirname, size in dirs.items():
        if size <= 100000:
            total += size

    return total

def p2() -> any:

    lines = get_input(7)

    # make a root directory
    root = '/'.join(__file__.split('/')[:-1] + ['root'])
    if not os.path.exists(root):
        os.mkdir(root)
    os.chdir(root)

    for line in lines[1:]:
        if line.startswith('$ cd'):
            directory = line.split(' ')[2]
            if not os.path.exists(directory) and not directory in ['..', '/']:
                os.mkdir(directory)
            if directory == '/':
                directory = root
            os.chdir(directory)
        elif line.startswith('$ ls'):
            pass
        else:
            size, filename = line.split(' ')
            if line.startswith('dir'):
                if not os.path.exists(filename):
                    os.mkdir(filename)
            else:
                with open(filename, 'w') as f:
                    f.write(size)
    
    # we have a directory structure with files and directories
    # we can now calculate the size of each directory
    dirs = {}
    for dirname, _, filenames in os.walk(root):
        size = 0
        for filename in filenames:
            with open(os.path.join(dirname, filename), 'r') as f:
                size += int(f.read())
        dirs[dirname] = size
    
    # remove everything inside the root directory
    for rt, ds, fs in os.walk(root, topdown=False):
        for f in fs:
            os.remove(os.path.join(rt, f))
        for d in ds:
            os.rmdir(os.path.join(rt, d))
    
    # remove the root directory itself
    os.rmdir(root)
    
    # to get the actual sizes (recursive), we need to add
    # the size of the child directory to the size of the parent directory
    for dirname in sorted(dirs, reverse=True):
        if dirname == root:
            continue
        parent = '/'.join(dirname.split('/')[:-1])
        dirs[parent] += dirs[dirname]
    
    # find the smallest directory that would free up at least 30000000 disk space
    dirs = {k: v for k, v in sorted(dirs.items(), key=lambda item: item[1])}
    space_available = int(7e7) - dirs[root]
    space_needed = int(3e7) - space_available
    for dirname, size in dirs.items():
        if size > space_needed:
            break

    return size


if __name__ == '__main__':
    print_summary(__file__, p1, p2, n=10)
