class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def clone(self) -> 'Point':
        point = Point(self.x, self.y)
        return point

    def __repr__(self) -> str:
        return f"Point({int(self.x)}, {int(self.y)})"
