from manim import *

class RightTriangle(Scene):
    def construct(self):
        # 创建直角三角形的三个顶点
        A = np.array([-3, -1.5, 0])
        B = np.array([3, 3, 0])
        C = np.array([-3, 3, 0])
        D = np.array([0, 3, 0])
        E = np.array([0, 0.75, 0])
        # 创建三角形
        triangle1 = Polygon(A, B, C, color=WHITE, fill_opacity=0.5, fill_color=BLUE)
        triangle2 = Polygon(B, D, E, color=WHITE, fill_opacity=0.5, fill_color=YELLOW)
        # 更精确地创建直角标记 - 现在直角在C点
        right_angle = RightAngle(
            Line(C, A), Line(C, B), 
            length=0.3, 
            color=YELLOW, 
            stroke_width=8
        )
        

        
        # 添加顶点标签 - 调整位置
        a_label = MathTex("A", color=WHITE).next_to(A, DOWN+LEFT, buff=0.1)
        b_label = MathTex("B", color=WHITE).next_to(B, UP+RIGHT, buff=0.1)
        c_label = MathTex("C", color=WHITE).next_to(C, UP+LEFT, buff=0.1)
        d_label = MathTex("D", color=WHITE).next_to(D, UP, buff=0.1)
        e_label = MathTex("E", color=WHITE).next_to(E, DOWN, buff=0.1)

        # 动画展示
        self.play(Create(triangle1))
        self.wait(0.5)
        self.play(Create(triangle2))
        self.wait(0.5)
        self.play(Create(right_angle))
        self.wait(0.5)
        self.play(Write(a_label), Write(b_label), Write(c_label), Write(d_label), Write(e_label))
        self.wait(0.5)
        
