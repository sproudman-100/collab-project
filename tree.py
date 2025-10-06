# Create a tree entity
class Tree(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.scale_y = 4
        self.scale_x = 4
        self.collider = 'box'
        self.texture = 'assets/tree.png'
        for key, value in kwargs.items():
            setattr(self, key, value)

                # Insert Tree entities at random positions
    tree_count = 10
    for i in range(tree_count):
        Tree(position=(random.uniform(-20, 20), random.uniform(-20, 20), 0), collider='box')