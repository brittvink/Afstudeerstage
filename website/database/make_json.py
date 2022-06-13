import json

class Tree:
    def __init__(self, name, linkje):
        self.children = []
        self.name = name
        self.linkje = linkje

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class jsonmain:
    left = Tree("left" ,"")
    middle = Tree("middle", "")
    right = Tree("right", "")
    root = Tree("root", "")
    root.children = [left, middle, right]

    with open('/Users/brittvink/Desktop/KCBBE/website/media/datamaken.json', 'w') as outfile:
        outfile.write(root.toJSON())


