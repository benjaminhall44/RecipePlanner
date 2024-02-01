import json
import os
import sys


class CraftPlanner:
    EXT = ".crp"
    filename: str = None
    project: str = None
    recipe = {}

    def save(self):
        if self.filename is not None:
            json.dump(self.recipe, open(self.filename, "w"), indent=4)

    def find_raw(self, name: str, found: dict, count: float):
        if len(self.recipe[name]["ingredients"]) > 0:
            for i in self.recipe[name]["ingredients"].items():
                self.find_raw(i[0], found, count * i[1])
        else:
            if name not in found:
                found[name] = 0.0
            found[name] += count

    def count(self, name: str, found: dict, count: float):
        if name not in found:
            found[name] = 0.0
        found[name] += count
        if len(self.recipe[name]["ingredients"]) > 0:
            for i in self.recipe[name]["ingredients"].items():
                self.count(i[0], found, count * i[1])

    def tree(self, name: str, count = 1.0, accumulated = 1.0, indent = 0):
        print(" " * indent + f"{name} {count} -> {count * accumulated}", end="")
        if len(self.recipe[name]["ingredients"]) > 0:
            print(":")
            for i in self.recipe[name]["ingredients"].items():
                self.tree(i[0], i[1], count * accumulated, indent + 4)
        else:
            print()

    def open(self, filename: str):
        if self.filename is not None:
            self.save()
        self.filename = filename
        self.project = os.path.splitext(os.path.basename(filename))[0]
        if os.path.exists(self.filename) and os.path.isfile(self.filename):
            file = open(self.filename, "r")
            self.recipe = json.load(file)
            file.close()
            self.save()
        else:
            print("cannot find file")

    def newfile(self, filename: str):
        if self.filename is not None:
            self.save()
        self.filename = filename
        self.project = os.path.splitext(os.path.basename(filename))[0]
        if os.path.exists(self.filename) and os.path.isfile(self.filename):
            print("already exists")
        else:
            file = open(self.filename, "w")
            self.recipe = {self.project: {"ingredients": {}}}
            file.close()
            self.save()

    def add(self, makes, item, count=1.0):
        if makes in self.recipe:
            self.recipe[makes]["ingredients"][item] = count
            if self.recipe[makes]["ingredients"][item] == 0:
                del self.recipe[makes]["ingredients"][item]
            if item not in self.recipe:
                self.recipe[item] = {"ingredients": {}}
                print(f"created entry {item}")
            print(f"{makes} now requires {count} {item}")
        else:
            print("entry does not exist: " + makes)
    def intro(self):
        print(f"Project: {self.project}")

    def run(self):
        running: bool = True
        while running:
            command = input().split()
            if len(command) == 0:
                continue
            if command[0] == "exit":
                self.save()
                running = False
                continue

            elif command[0] == "open":
                if len(command) != 2:
                    print("bad command")
                self.open(command[1] + self.EXT)
                self.intro()

            elif command[0] == "newfile":
                if len(command) != 2:
                    print("bad command")
                self.newfile(command[1] + self.EXT)
                self.intro()

            elif command[0] == "save":
                self.save()

            elif "add" in command:
                if len(command) == 4:
                    count = float(command[3])
                elif len(command) == 3:
                    count = 1.0
                else:
                    print("bad format")
                    continue

                if command[0] == "add":
                    makes = command[1]
                elif command[1] == "add":
                    makes = command[0]
                else:
                    print("bad format")
                    continue

                self.add(makes, command[2], count)

            elif command[0] == "list":
                found = {}
                if len(command) == 2:
                    search = command[1]
                else:
                    search = self.project
                if search not in self.recipe:
                    print("entry does not exist: " + search)
                    continue

                self.find_raw(search, found, 1.0)
                for k in found.items():
                    print(f"{k[0]}: {k[1]}")

            elif command[0] == "count":
                found = {}
                self.count(self.project, found, 1.0)
                if len(command) == 2:
                    if command[1] in found:
                        print(f"{command[1]}: {found[command[1]]}")
                    else:
                        print("entry does not exist: " + command[1])
                else:
                    for k in found.items():
                        print(f"{k[0]}: {k[1]}")

            elif command[0] == "recipe":
                if len(command) == 2:
                    search = command[1]
                else:
                    search = self.project
                if search in self.recipe:
                    for k in self.recipe[search]["ingredients"].items():
                        print(f"{k[0]}: {k[1]}")
                else:
                    print("entry does not exist: " + search)

            elif command[0] == "tree":
                if len(command) == 2:
                    search = command[1]
                else:
                    search = self.project
                if search not in self.recipe:
                    print("entry does not exist: " + search)
                    continue
                self.tree(search)
            elif command[0] == "print":
                print(json.dumps(self.recipe, indent=4))

        if self.filename is not None:
            self.save()


if __name__ == "__main__":
    plan = CraftPlanner()
    if len(sys.argv) == 2:
        plan.open(sys.argv[1])
        plan.intro()
    plan.run()
