import matplotlib.pyplot as plt


class Diagram:
    def __init__(self, points, pt1=None, pt2=None, pt3=None):
        self.points = points
        self.pt1 = pt1
        self.pt2 = pt2
        self.pt3 = pt3

    def plot(self):
        x_points = [point[0] for point in self.points]
        y_points = [point[1] for point in self.points]

        plt.figure(figsize=(8, 8))
        plt.scatter(x_points, y_points, color='blue')
        if self.pt1:
            plt.scatter(self.pt1.x, self.pt1.y, color='purple')
        if self.pt2:
            plt.scatter(self.pt2.x, self.pt2.y, color='yellow')
        if self.pt3:
            plt.scatter(self.pt3.x, self.pt3.y, color='black')

        plt.axhline(0, color='gray', linestyle='--')
        plt.axvline(0, color='gray', linestyle='--')
        plt.grid(True, linestyle='--', linewidth=0.5)

        plt.show()
