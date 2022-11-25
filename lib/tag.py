class Tag:
    def __init__(self, name_, **kwargs):
        self.name = name_
        self.attr = kwargs
        self.child = []

    def append_child(self, child):
        self.child.append(child)

        return self

    def append_tree(self, tree):
        self.child.extend(tree)

        return self

    def to_string(self, _pad=0):
        pad = " " * _pad
        aux = []

        aux.append(pad)
        aux.append(f"<{self.name}")

        for attr, value in self.attr.items():
            aux.append(f' {attr}="{str(value)}"')

        if len(self.child) > 0:
            aux.append(">\n")

            for child in self.child:
                aux.append(child.to_string(_pad=_pad + 4))
                aux.append("\n")

            aux.append(pad)
            aux.append(f"</{self.name}")
        else:
            aux.append("/")

        aux.append(">")

        return "".join(aux)

