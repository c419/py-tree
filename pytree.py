#!/bin/env python3
from pathlib import Path
from sys import argv, exit

VERT_RIGHT = chr(0x2523)
UP_RIGHT = chr(0x2517)
VERT = chr(0x2503)
HORIZ = chr(0x2501)
SPACE = " "
COLOR_BLUE = '\033[94m'
COLOR_END = '\033[0m'

def get_path_content_dirs(p):
    if not p.is_dir():
        return []
    return sorted([d for d in p.iterdir() if d.is_dir()], key=lambda p: p.name)

def get_path_content_files(p):
    if not p.is_dir():
        return []
    return sorted([f for f in p.iterdir() if f.is_file()], key=lambda p: p.name)

def draw_pg_line(name, intendation, verts, is_last):
    """
    name - 
    intendation - current intendation
    vert - list of intendation levels where we should draw verts
    is_last - if the item is last to draw on layer
    """
    prefix = ""
    for level in range(intendation):
        if level in verts:
            prefix += VERT
        else:
            prefix += SPACE
        prefix += SPACE * 3
    prefix = prefix + UP_RIGHT + HORIZ*2 if is_last else prefix + VERT_RIGHT + HORIZ*2
    print(prefix + name)

#draw directory contents on specific intendation level. levels are from 0. previous_verts is a list of layers where we should draw vertical lines

def draw_dir(path, intendation, previous_verts):
    items = get_path_content_dirs(path) + get_path_content_files(path)
    while items:
        item = items.pop(0)
        is_last = False if items else True
        if item.is_dir():
            draw_pg_line(COLOR_BLUE + item.name + COLOR_END, intendation, previous_verts, is_last)
        else:
            draw_pg_line(item.name, intendation, previous_verts, is_last)

        if item.is_dir():
            verts = previous_verts[:]
            if not is_last:
                verts.append(intendation)
            draw_dir(item, intendation + 1, verts)


if __name__ == "__main__":
    print(".")
    if len(argv) > 1:
        if not Path(argv[1]).is_dir():
            exit(f"Not a directory: {argv[1]}")
        draw_dir(Path(argv[1]), 0, [])
    else:
        draw_dir(Path.cwd(), 0, [])
