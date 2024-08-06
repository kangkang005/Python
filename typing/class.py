class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def get_radius(self) -> float:
        return self.radius

    def set_radius(self, radius: float) -> 'Circle':
        self.radius = radius
        return self

    def __str__(self) -> str:
        return str(self.radius)

# 链式调用
circle = Circle(5.0)
circle.set_radius(10.0).set_radius(15.0).set_radius(20.0)
print(circle)