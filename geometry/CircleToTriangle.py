from manim import *


class CircleToTriangle(Scene):
    def construct(self):
        # 定义大圆的半径
        big_radius = 2
        # 定义同心圆的数量
        num_circles = 10
        # 创建一个大圆
        big_circle = Circle(radius=2, fill_color=BLUE, fill_opacity=1, stroke_color=WHITE, stroke_width=2)
        self.add(big_circle)
        self.wait(1)

        # 创建同心圆列表
        circles = []
        for i in range(num_circles):
            radius = big_radius * (i + 1) / num_circles
            circle = Circle(radius=radius, color=BLUE)
            circles.append(circle)

        # 移除大圆，添加同心圆
        self.remove(big_circle)
        self.add(*circles)
        self.wait(1)

        # 剪开同心圆
        arcs = []
        for circle in circles:
            arc = Arc(
                start_angle=0,
                angle=2 * PI,
                radius=circle.radius,
                color=circle.color
            )
            arcs.append(arc)
            self.remove(circle)
            self.add(arc)
        self.wait(1)

        # 平铺并累叠成近似三角形
        for i, arc in enumerate(arcs):
            length = 2 * PI * arc.radius
            new_arc = Line(LEFT * length / 2, RIGHT * length / 2, color=arc.color)
            new_arc.move_to(UP * (num_circles - i - 1) * big_radius / num_circles)
            self.play(Transform(arc, new_arc))
        self.wait(2)
