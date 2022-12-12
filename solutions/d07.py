from io import TextIOWrapper
from dataclasses import dataclass, field
from typing import Self


@dataclass
class File:
    name: str
    size: int

    def __str__(self) -> str:
        return f'- {self.name} (file, size={self.size})'

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Directory:
    name: str
    parent: Self = None
    size: int = 0
    subdirs: list[Self] = field(default_factory=list)
    files: list[File] = field(default_factory=list)

    def set_total_size(self):
        self.size = sum([f.size for f in self.files])
        for d in self.subdirs:
            d.set_total_size()
            self.size += d.size

    def print_tree(self, level=0):
        print(f'{" "*level}- {self.name} (dir)')
        for d in self.subdirs:
            d.print_tree(level+2)
        for f in self.files:
            print(f'{" "*level}{f}')

    def get_small_sizes(self, limit: int) -> int:
        size = 0
        for d in self.subdirs:
            if d.size < limit:
                size += d.size
            size += d.get_small_sizes(limit)
        return size

    def get_delete_candidate(self, space_needed: int) -> int:
        space = self.size
        for d in self.subdirs:
            if d.size >= space_needed:
                space = min(space, d.get_delete_candidate(space_needed))
        return space


def get_path_name(path: list[str]) -> str:
    return '/'.join(path)


def main(file: TextIOWrapper):
    path: list[str] = []
    dirs: dict[str, Directory] = dict()
    currdir: Directory = Directory('')
    for cmdline in file.readlines():
        cmd = cmdline.strip().split()
        match cmd:
            case ['$', 'cd', '..']:
                currdir = currdir.parent
                path.pop()
            case ['$', 'cd', dirname]:
                path_name = get_path_name(path + [dirname])
                if path_name not in dirs:
                    dirs[path_name] = Directory(dirname)
                currdir = dirs[path_name]
                path.append(dirname)
            case ['$', 'ls']:
                pass
            case ['dir', dirname]:
                path_name = get_path_name(path + [dirname])
                if path_name not in dirs:
                    dirs[path_name] = Directory(dirname)
                currdir.subdirs.append(dirs[path_name])
                dirs[path_name].parent = currdir
            case [size, filename]:
                currdir.files.append(File(filename, int(size)))

    dirs['/'].set_total_size()
    FS_SIZE_LIMIT = 70000000
    FS_MIN_SIZE = 30000000
    unused = FS_SIZE_LIMIT - dirs['/'].size
    needed = FS_MIN_SIZE - unused

    print(dirs['/'].get_small_sizes(100000))
    print(dirs['/'].get_delete_candidate(needed))
