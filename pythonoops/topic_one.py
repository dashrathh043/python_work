# 2 Methods

class Vector2D:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def Set(self, x, y):
        self.x = x
        self.y = y

    def Compare(self, other):
        if self.x > other.x:
            return self.x
        return other.x


def Main():
    vec1 = Vector2D(9, 4)
    vec2 = Vector2D(5, 6)
    Bigger = vec1.Compare(vec2)
    print(Bigger)
    print("X : " + str(vec1.x) + ", Y : " + str(vec1.y))


if __name__ == '__main__':
    Main()
