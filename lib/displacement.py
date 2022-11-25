from .tag import Tag


class Displacement:
    x:bool
    y:bool

    def __init__(self):
        self.x = False
        self.y = False
    
    def set_x(self):
        self.x = True
    
    def clear_x(self):
        self.x = False
    
    def set_y(self):
        self.y = True
    
    def clear_y(self):
        self.y = False

    def get_axis(self):
        return self.x, self.y

    def get_tag(self, selection):
        tag1 = None
        tag2 = None

        if self.x:
            tag1 = Tag("displacement", selection=selection, axis=1)
            
            tag1.append_tree([
                Tag("value").append_tree([0]),
            ])

        if self.y:
            tag2 = Tag("displacement", selection=selection, axis=2)
            
            tag2.append_tree([
                Tag("value").append_tree([0]),
            ])

        return tag1, tag2
