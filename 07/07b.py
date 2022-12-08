from enum import Enum

IN_FILE = "07/input.txt"


class EntryType(Enum):
    DIRECTORY = 1
    FILE = 2


class ParserState(Enum):
    INIT = 1
    INPUT = 2
    OUTPUT = 3


class DirEntry:
    def __init__(self, name, parent, type, size=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.type = type
        self.size = size

    def get_size(self):
        if self.type == EntryType.FILE:
            return self.size
        children_size = 0
        for child in self.children:
            children_size += child.get_size()
        return children_size

    def __str__(self) -> str:
        return f"{self.name}: {self.get_size()}"

    def __repr__(self) -> str:
        return f"{self.name}: {self.get_size()}"


if __name__ == "__main__":
    all_dirs = []
    current_dir = None
    state = ParserState.INIT  # first line is gonna be creating root dir

    with open(IN_FILE) as f:
        for line in [line.strip().split(" ") for line in f]:
            if state == ParserState.OUTPUT:
                if line[0] == "$":
                    state = ParserState.INPUT  # reached the last line of the output
                else:
                    new_dir = None
                    if line[0] == "dir":
                        new_dir = DirEntry(line[1], current_dir, EntryType.DIRECTORY)
                        all_dirs.append(new_dir)
                    else:
                        new_dir = DirEntry(
                            line[1], current_dir, EntryType.FILE, int(line[0])
                        )
                    current_dir.children.append(new_dir)

            if state == ParserState.INPUT:
                if line[1] == "ls":
                    state = ParserState.OUTPUT  # getting a listing
                elif line[1] == "cd":
                    target = line[2]
                    if target == "..":
                        current_dir = current_dir.parent
                    else:
                        for entry in current_dir.children:
                            if entry.name == target:
                                current_dir = entry

            if state == ParserState.INIT:
                new_dir = DirEntry(line[2], None, EntryType.DIRECTORY)
                all_dirs.append(new_dir)
                current_dir = new_dir
                state = ParserState.INPUT

    unused_space = 70000000 - all_dirs[0].get_size()
    to_free = 30000000 - unused_space
    candidate_dirs = [x for x in all_dirs if x.get_size() >= to_free]
    candidate_dirs.sort(key=lambda x: x.get_size())
    print(candidate_dirs[0].get_size())
