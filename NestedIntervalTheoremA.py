from manim import *

class NestedIntervalTheoremA(Scene):
    def construct(self):
        # 初始区间 [A1, B1]
        A1 = -4
        B1 = 4
        interval_length = B1 - A1

        # 绘制数轴
        line = NumberLine(x_range=[-5, 5], length=10, include_numbers=False)
        self.play(Create(line))

        # 存储所有点和标签
        dots = []
        labels = []
        brackets = []

        # 绘制初始区间 [A1, B1]
        dot_A1 = Dot(line.n2p(A1), color=BLUE)
        dot_B1 = Dot(line.n2p(B1), color=BLUE)
        label_A1 = Tex("A1", color=BLUE).next_to(dot_A1, DOWN)
        label_B1 = Tex("B1", color=BLUE).next_to(dot_B1, DOWN)

        # 绘制中括号（更粗，中心位于点上）
        bracket_A1 = Tex("[", color=RED, font_size=64).move_to(dot_A1.get_center())
        bracket_B1 = Tex("]", color=RED, font_size=64).move_to(dot_B1.get_center())

        self.play(FadeIn(dot_A1), FadeIn(dot_B1), Write(label_A1), Write(label_B1))
        self.play(Write(bracket_A1), Write(bracket_B1))
        self.wait(0.5)

        # 将点和标签添加到列表中
        dots.extend([dot_A1, dot_B1])
        labels.extend([label_A1, label_B1])
        brackets.extend([bracket_A1, bracket_B1])

        # 逐步绘制闭区间套
        An, Bn = A1, B1
        for n in range(2, 12):
            # 计算新的区间 [An, Bn]
            new_length = interval_length / (2 ** (n - 1))
            An = An + new_length / 2
            Bn = Bn - new_length / 2

            # 绘制新的点
            dot_An = Dot(line.n2p(An), color=BLUE)
            dot_Bn = Dot(line.n2p(Bn), color=BLUE)

            # 只绘制前四个区间的中括号
            if n <= 4:
                # 绘制中括号（更粗，中心位于点上）
                bracket_An = Tex("[", color=RED, font_size=64).move_to(dot_An.get_center())
                bracket_Bn = Tex("]", color=RED, font_size=64).move_to(dot_Bn.get_center())

                # 绘制点和标签
                label_An = Tex(f"A{n}", color=BLUE).next_to(dot_An, DOWN)
                label_Bn = Tex(f"B{n}", color=BLUE).next_to(dot_Bn, DOWN)
                self.play(FadeIn(dot_An), FadeIn(dot_Bn), Write(label_An), Write(label_Bn))
                self.play(Write(bracket_An), Write(bracket_Bn))
            else:
                self.play(FadeIn(dot_An), FadeIn(dot_Bn))

            # 将点和标签添加到列表中
            dots.extend([dot_An, dot_Bn])
            if n <= 4:
                labels.extend([label_An, label_Bn])
                brackets.extend([bracket_An, bracket_Bn])

            # 如果是第五个区间，淡出前四个区间的下标
            if n == 5:
                self.play(
                    *[FadeOut(label) for label in labels],
                    run_time=1
                )

            # 只有前五次描点时拉动镜头
            if n <= 5:
                self.play(
                    line.animate.scale(1.2).shift(LEFT * (An + Bn) / 10),
                    run_time=0.5
                )
            self.wait(0.2)

        # 标出交集点 a
        a = (An + Bn) / 2
        dot_a = Dot(line.n2p(a), color=RED)
        label_a = Tex("a").next_to(dot_a, UP)

        # 镜头拉近到点 a
        self.play(
            line.animate.scale(1.5).shift(LEFT * a / 5),
            run_time=1
        )
        self.play(FadeIn(dot_a), Write(label_a))
        self.wait(1)

        # 用圆圈标出点 a
        circle = Circle(radius=0.2, color=YELLOW).move_to(dot_a)
        self.play(Create(circle))
        self.wait(2)

        # 镜头拉远，展示整体
        self.play(
            line.animate.scale(0.8).shift(RIGHT * a / 5),
            run_time=1
        )
        self.wait(1)

        # 显示文字“闭区间套定理”
        theorem_text = Text("闭区间套定理图解").set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL).to_edge(UP)
        self.play(Write(theorem_text))
        self.wait(2)