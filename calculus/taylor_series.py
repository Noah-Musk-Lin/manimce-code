from manim import *

# 创建支持中文的 TexTemplate
tex_template = TexTemplate()
tex_template.add_to_preamble(r"\usepackage{ctex}")


class Test(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        # 修改这里，将数学表达式用 $ 包裹
        info1 = Tex(r"$P_n(x)=\sum_{i=0}^n\frac{f^{(i)}x_0}{i!}(x - x_0)^i$", font_size=40, color=YELLOW, tex_template=tex_template).shift(UP)
        info1.set_font("SimSun")
        self.play(FadeIn(info1))
        self.wait(3)
        # 修改这里，将数学表达式用 $ 包裹
        info2 = Tex(r"$P_n(x)=\sum_{i=0}^n\frac{f^{(i)}(0)}{i!}x^i$", font_size=40, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(3)
        self.play(FadeOut(info1))
        sr = SurroundingRectangle(info2, color=BLUE, buff=0.2, stroke_width=1)
        self.play(Create(sr))
        self.wait(3)
        info3 = Tex(r"\text{麦克劳林公式(是泰勒公式}$x_0$ = 0\text{的一种特殊形式)}", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, UP * 2)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(3)
        info4 = Text("常用函数的推导", font="SimSun", font_size=30).set_color_by_gradient(RED, GREEN, BLUE).shift(UP * 2).shift(LEFT * 0.5)
        self.play(FadeIn(info4))
        self.wait(1)
        self.play(info4.animate.scale(1.5))
        self.wait(3)


class A1(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        info1 = Tex(r"$\sin x,x \in \mathbb{R}$", font_size=50, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)
        sr1 = SurroundingRectangle(info1, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr1))
        self.wait(3)
        info2 = Tex(r"$f(0)=\sin 0 = 0$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(1)
        info3 = Tex(r"$f'(0)x=\cos 0\cdot x = x$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN, aligned_edge=LEFT)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(1)
        info4 = Tex(r"$\frac{f''(0)x^2}{2!}=\frac{-\sin 0\cdot x^2}{2!}=0$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN, aligned_edge=LEFT)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        info5 = Tex(r"$\frac{f^{(3)}(0)x^3}{3!}=\frac{-\cos 0\cdot x^3}{3!}=-\frac{x^3}{3!}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info4, DOWN, aligned_edge=LEFT)
        info5.set_font("SimSun")
        self.play(FadeIn(info5))
        self.wait(1)
        info6 = Tex(r"$\frac{f^{(4)}(0)x^4}{4!}=\frac{\sin 0\cdot x^4}{4!}=0$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info5, DOWN, aligned_edge=LEFT)
        info6.set_font("SimSun")
        self.play(FadeIn(info6))
        self.wait(1)
        info7 = Tex(r"$\frac{f^{(5)}(0)x^5}{5!}=\frac{\cos 0\cdot x^5}{5!}=\frac{x^5}{5!}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info6, DOWN, aligned_edge=LEFT)
        info7.set_font("SimSun")
        self.play(FadeIn(info7))
        self.wait(1)
        t2 = Tex(r"$\sin x$", font_size=30, color=RED, tex_template=tex_template).next_to(info2, LEFT * 4)
        t2.set_font("SimSun")
        self.play(FadeIn(t2))
        t3 = Tex(r"$\sin' x=\cos x$", font_size=30, color=RED, tex_template=tex_template).next_to(info3, LEFT * 4)
        t3.set_font("SimSun")
        self.play(FadeIn(t3))
        t4 = Tex(r"$\sin'' x=-\sin x$", font_size=30, color=RED, tex_template=tex_template).next_to(info4, LEFT * 4)
        t4.set_font("SimSun")
        self.play(FadeIn(t4))
        t5 = Tex(r"$\sin''' x=-\cos x$", font_size=30, color=RED, tex_template=tex_template).next_to(info5, LEFT * 4)
        t5.set_font("SimSun")
        self.play(FadeIn(t5))
        t6 = Tex(r"$\sin^{(4)} x=\sin x$", font_size=30, color=RED, tex_template=tex_template).next_to(info6, LEFT * 4)
        t6.set_font("SimSun")
        self.play(FadeIn(t6))
        t7 = Tex(r"$\sin^{(5)} x=\cos x$", font_size=30, color=RED, tex_template=tex_template).next_to(info7, LEFT * 4)
        t7.set_font("SimSun")
        self.play(FadeIn(t7))
        self.wait(1)
        result = Tex(r"$\sin x \approx x-\frac{x^3}{3!}+\frac{x^5}{5!}$", font_size=40, color=YELLOW, tex_template=tex_template).next_to(info7, DOWN * 2).shift(LEFT * 0.3)
        result.set_font("SimSun")
        self.play(Write(result))
        self.wait(3)


class A2(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        info1 = Tex(r"$\cos x,x \in \mathbb{R}$", font_size=50, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)
        sr1 = SurroundingRectangle(info1, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr1))
        self.wait(3)
        info2 = Tex(r"$f(0)=\cos 0 = 1$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(1)
        info3 = Tex(r"$f'(0)x=-\sin 0\cdot x = 0$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN, aligned_edge=LEFT)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(1)
        info4 = Tex(r"$\frac{f''(0)x^2}{2!}=\frac{-\cos 0\cdot x^2}{2!}=-\frac{x^2}{2!}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN, aligned_edge=LEFT)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        info5 = Tex(r"$\frac{f^{(3)}(0)x^3}{3!}=\frac{\sin 0\cdot x^3}{3!}=0$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info4, DOWN, aligned_edge=LEFT)
        info5.set_font("SimSun")
        self.play(FadeIn(info5))
        self.wait(1)
        info6 = Tex(r"$\frac{f^{(4)}(0)x^4}{4!}=\frac{\cos 0\cdot x^4}{4!}=\frac{x^4}{4!}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info5, DOWN, aligned_edge=LEFT)
        info6.set_font("SimSun")
        self.play(FadeIn(info6))
        self.wait(1)
        t2 = Tex(r"$\cos x$", font_size=30, color=RED, tex_template=tex_template).next_to(info2, LEFT * 4)
        t2.set_font("SimSun")
        self.play(FadeIn(t2))
        t3 = Tex(r"$\cos' x=-\sin x$", font_size=30, color=RED, tex_template=tex_template).next_to(info3, LEFT * 4)
        t3.set_font("SimSun")
        self.play(FadeIn(t3))
        t4 = Tex(r"$\cos'' x=-\cos x$", font_size=30, color=RED, tex_template=tex_template).next_to(info4, LEFT * 4)
        t4.set_font("SimSun")
        self.play(FadeIn(t4))
        t5 = Tex(r"$\cos''' x=\sin x$", font_size=30, color=RED, tex_template=tex_template).next_to(info5, LEFT * 4)
        t5.set_font("SimSun")
        self.play(FadeIn(t5))
        t6 = Tex(r"$\cos^{(4)} x=\cos x$", font_size=30, color=RED, tex_template=tex_template).next_to(info6, LEFT * 4)
        t6.set_font("SimSun")
        self.play(FadeIn(t6))
        self.wait(1)
        result = Tex(r"$\cos x \approx 1-\frac{x^2}{2!}+\frac{x^4}{4!}$", font_size=40, color=YELLOW, tex_template=tex_template).next_to(info6, DOWN * 2).shift(LEFT * 0.5)
        result.set_font("SimSun")
        self.play(Write(result))
        self.wait(3)


class A3(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        info1 = Tex(r"$e^x,x \in \mathbb{R}$", font_size=50, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)
        sr1 = SurroundingRectangle(info1, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr1))
        self.wait(3)
        info2 = Tex(r"$f(0)=e^0 = 1$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(1)
        info3 = Tex(r"$f'(0)x=e^0\cdot x = x$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN, aligned_edge=LEFT)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(1)
        info4 = Tex(r"$\frac{f''(0)x^2}{2!}=\frac{e^0\cdot x^2}{2!}=\frac{x^2}{2!}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN, aligned_edge=LEFT)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        info5 = Tex(r"$\frac{f^{(3)}(0)x^3}{3!}=\frac{e^0\cdot x^3}{3!}=\frac{x^3}{3!}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info4, DOWN, aligned_edge=LEFT)
        info5.set_font("SimSun")
        self.play(FadeIn(info5))
        self.wait(1)
        t2 = Tex(r"$(e^x)'=e^x$", font_size=50, color=RED, tex_template=tex_template).next_to(info4, LEFT * 4)
        t2.set_font("SimSun")
        self.play(FadeIn(t2))
        self.wait(1)
        result = Tex(r"$e^x \approx 1 + x+\frac{x^2}{2!}+\frac{x^3}{3!}$", font_size=40, color=YELLOW, tex_template=tex_template).next_to(info5, DOWN * 2).shift(LEFT * 0.5)
        result.set_font("SimSun")
        self.play(Write(result))
        self.wait(3)
        result2 = Tex(r"$\text{欧拉公式：}e^{ix} = \cos x + i\sin x$", font_size=40, color=GREEN, tex_template=tex_template).next_to(result, DOWN * 2)
        result2.set_font("SimSun")
        self.play(Write(result2))
        sr2 = SurroundingRectangle(result2, color=GREEN, buff=0.2, stroke_width=1)
        self.play(Create(sr2))
        self.wait(3)


class A4(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        info1 = Tex(r"$\frac{1}{1 + x},x \in (-1,1)$", font_size=40, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)
        sr1 = SurroundingRectangle(info1, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr1))
        self.wait(3)
        info2 = Tex(r"$f(0)=\frac{1}{1 + 0}=1$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(1)
        info3 = Tex(r"$f'(0)x=-(1 + 0)^{-2}\cdot x=-x$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN * 1.5, aligned_edge=LEFT)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(1)
        info4 = Tex(r"$\frac{f''(0)x^2}{2!}=\frac{2(1 + 0)^{-3}\cdot x^2}{2!}=x^2$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN * 1.5, aligned_edge=LEFT)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        info5 = Tex(r"$\frac{f^{(3)}(0)x^3}{3!}=\frac{-6(1 + 0)^{-4}\cdot x^3}{3!}=-x^3$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info4, DOWN * 1.5, aligned_edge=LEFT)
        info5.set_font("SimSun")
        self.play(FadeIn(info5))
        self.wait(1)
        t2 = Tex(r"$\frac{1}{1 + x}$", font_size=30, color=RED, tex_template=tex_template).next_to(info2, LEFT * 4)
        t2.set_font("SimSun")
        self.play(FadeIn(t2))
        t3 = Tex(r"$\bigg(\frac{1}{1 + x}\bigg)'=-(1 + x)^{-2}$", font_size=30, color=RED, tex_template=tex_template).next_to(info3, LEFT * 4)
        t3.set_font("SimSun")
        self.play(FadeIn(t3))
        t4 = Tex(r"$\bigg(\frac{1}{1 + x}\bigg)''=2(1 + x)^{-3}$", font_size=30, color=RED, tex_template=tex_template).next_to(info4, LEFT * 4)
        t4.set_font("SimSun")
        self.play(FadeIn(t4))
        t5 = Tex(r"$\bigg(\frac{1}{1 + x}\bigg)'''=-6(1 + x)^{-4}$", font_size=30, color=RED, tex_template=tex_template).next_to(info5, LEFT * 4)
        t5.set_font("SimSun")
        self.play(FadeIn(t5))
        self.wait(1)
        t6 = Tex(r"\text{注意复合函数求导:}\thinspace (1 + x)'=1", font_size=22, color=YELLOW, tex_template=tex_template).move_to(axes.c2p(-5, 3))
        t6.set_font("SimSun")
        self.play(FadeIn(t6))
        sr2 = SurroundingRectangle(t6, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr2))
        self.wait(1)
        result = Tex(r"$\frac{1}{1 + x} \approx 1 - x + x^2 - x^3$", font_size=40, color=YELLOW, tex_template=tex_template).next_to(info5, DOWN * 2).shift(LEFT * 0.5)
        result.set_font("SimSun")
        self.play(Write(result))
        self.wait(3)


class A5(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        info1 = Tex(r"$\frac{1}{1 - x},x \in (-1,1)$", font_size=40, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)
        sr1 = SurroundingRectangle(info1, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr1))
        self.wait(3)
        info2 = Tex(r"$f(0)=\frac{1}{1 - 0}=1$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(1)
        info3 = Tex(r"$f'(0)x=(1 - 0)^{-2}\cdot x=x$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN * 1.5, aligned_edge=LEFT)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(1)
        info4 = Tex(r"$\frac{f''(0)x^2}{2!}=\frac{2(1 - 0)^{-3}\cdot x^2}{2!}=x^2$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN * 1.5, aligned_edge=LEFT)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        info5 = Tex(r"$\frac{f^{(3)}(0)x^3}{3!}=\frac{6(1 - 0)^{-4}\cdot x^3}{3!}=x^3$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info4, DOWN * 1.5, aligned_edge=LEFT)
        info5.set_font("SimSun")
        self.play(FadeIn(info5))
        self.wait(1)
        t2 = Tex(r"$\frac{1}{1 - x}$", font_size=30, color=RED, tex_template=tex_template).next_to(info2, LEFT * 4)
        t2.set_font("SimSun")
        self.play(FadeIn(t2))
        t3 = Tex(r"$\bigg(\frac{1}{1 - x}\bigg)'=(1 - x)^{-2}$", font_size=30, color=RED, tex_template=tex_template).next_to(info3, LEFT * 4)
        t3.set_font("SimSun")
        self.play(FadeIn(t3))
        t4 = Tex(r"$\bigg(\frac{1}{1 - x}\bigg)''=2(1 - x)^{-3}$", font_size=30, color=RED, tex_template=tex_template).next_to(info4, LEFT * 4)
        t4.set_font("SimSun")
        self.play(FadeIn(t4))
        t5 = Tex(r"$\bigg(\frac{1}{1 - x}\bigg)'''=6(1 - x)^{-4}$", font_size=30, color=RED, tex_template=tex_template).next_to(info5, LEFT * 4)
        t5.set_font("SimSun")
        self.play(FadeIn(t5))
        t6 = Tex(r"\text{注意复合函数求导:}\thinspace (1 - x)'=-1", font_size=22, color=YELLOW, tex_template=tex_template).move_to(axes.c2p(-5, 3))
        t6.set_font("SimSun")
        self.play(FadeIn(t6))
        sr2 = SurroundingRectangle(t6, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr2))
        self.wait(1)
        result = Tex(r"$\frac{1}{1 - x} \approx 1 + x + x^2 + x^3$", font_size=40, color=YELLOW, tex_template=tex_template).next_to(info5, DOWN * 2).shift(LEFT * 0.5)
        result.set_font("SimSun")
        self.play(Write(result))
        self.wait(3)


class A6(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))
        info1 = Tex(r"$\ln(1 + x),x \in (-1,1]$", font_size=40, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)
        sr1 = SurroundingRectangle(info1, color=YELLOW, buff=0.2, stroke_width=1)
        self.play(Create(sr1))
        self.wait(3)
        info2 = Tex(r"$f(0)=\ln(1 + 0)=0$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info1, DOWN * 2, aligned_edge=LEFT)
        info2.set_font("SimSun")
        self.play(FadeIn(info2))
        self.wait(1)
        info3 = Tex(r"$f'(0)x=\frac{1}{1 + 0}\cdot x=x$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN * 1.5, aligned_edge=LEFT)
        info3.set_font("SimSun")
        self.play(FadeIn(info3))
        self.wait(1)
        info4 = Tex(r"$\frac{f''(0)x^2}{2!}=\frac{-(1 + 0)^{-2}\cdot x^2}{2!}=-\frac{x^2}{2}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN * 1.5, aligned_edge=LEFT)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        info5 = Tex(r"$\frac{f^{(3)}(0)x^3}{3!}=\frac{2(1 + 0)^{-3}\cdot x^3}{3!}=\frac{x^3}{3}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info4, DOWN * 1.5, aligned_edge=LEFT)
        info5.set_font("SimSun")
        self.play(FadeIn(info5))
        self.wait(1)
        info6 = Tex(r"$\frac{f^{(4)}(0)x^4}{4!}=\frac{-6(1 + 0)^{-4}\cdot x^4}{4!}=-\frac{x^4}{4}$", font_size=30, color=BLUE, tex_template=tex_template).next_to(info5, DOWN * 1.5, aligned_edge=LEFT)
        info6.set_font("SimSun")
        self.play(FadeIn(info6))
        self.wait(1)
        t2 = Tex(r"$\ln(1 + x)$", font_size=30, color=RED, tex_template=tex_template).next_to(info2, LEFT * 4)
        t2.set_font("SimSun")
        self.play(FadeIn(t2))
        t3 = Tex(r"$\bigg(\ln(1 + x)\bigg)'=\frac{1}{1 + x}$", font_size=30, color=RED, tex_template=tex_template).next_to(info3, LEFT * 4)
        t3.set_font("SimSun")
        self.play(FadeIn(t3))
        t4 = Tex(r"$\bigg(\ln(1 + x)\bigg)''=-(1 + x)^{-2}$", font_size=30, color=RED, tex_template=tex_template).next_to(info4, LEFT * 4)
        t4.set_font("SimSun")
        self.play(FadeIn(t4))
        t5 = Tex(r"$\bigg(\ln(1 + x)\bigg)'''=2(1 + x)^{-3}$", font_size=30, color=RED, tex_template=tex_template).next_to(info5, LEFT * 4)
        t5.set_font("SimSun")
        self.play(FadeIn(t5))
        t6 = Tex(r"$\bigg(\ln(1 + x)\bigg)^{(4)}=-6(1 + x)^{-4}$", font_size=30, color=RED, tex_template=tex_template).next_to(info6, LEFT * 4)
        t6.set_font("SimSun")
        self.play(FadeIn(t6))
        self.wait(1)
        t7 = Tex(r"$\ln(1 + x) \approx x-\frac{x^2}{2}+\frac{x^3}{3}-\frac{x^4}{4}$", font_size=40, color=YELLOW, tex_template=tex_template).next_to(info6, DOWN * 2).shift(LEFT * 0.5)
        t7.set_font("SimSun")
        self.play(Write(t7))
        self.wait(3)


class A7(Scene):
    def construct(self):
        axes = NumberPlane(x_range=[-6, 6], y_range=[-6, 6], axis_config={"stroke_color": GREY,
                                                                          "include_numbers": True,
                                                                          "stroke_width": 1},
                           background_line_style={"stroke_color": GREY, "stroke_width": 0.5})
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        # self.play(FadeIn(axes), FadeIn(zerolabel))  # 按需显示坐标系

        # 标题：泰勒公式可以延伸很多公式
        info1 = Tex(r"\text{泰勒公式可以延伸很多公式}", font_size=30, color=YELLOW, tex_template=tex_template).to_edge(UP)
        info1.set_font("SimSun")
        self.play(Write(info1))
        self.wait(1)

        # 泰勒公式带余项的一般形式
        m1 = Tex(r"$f(x)=\sum_{i=0}^n\frac{f^{(i)}(x_0)}{i!}(x - x_0)^i + R_n(x)$", 
                 font_size=30, color=RED, tex_template=tex_template).next_to(info1, DOWN * 1.5)
        m1.set_font("SimSun")
        self.play(FadeIn(m1))

        # 拉格朗日型余项
        m2 = Tex(r"$\text{拉格朗日型余项：}R_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}(x - x_0)^{n+1}$", 
                 font_size=30, color=RED, tex_template=tex_template).next_to(m1, DOWN * 2)
        m2.set_font("SimSun")
        self.play(FadeIn(m2))
        self.wait(3)

        # 麦克劳林公式与泰勒公式的关系
        info2 = Tex(r"\text{当}$x_0$ = 0\text{时,就是我们介绍的麦克劳林公式}", 
                    font_size=30, color=PINK, tex_template=tex_template).next_to(m2, DOWN * 2)
        info2.set_font("SimSun")
        self.play(Write(info2))
        self.wait(1)

        # 拉格朗日中值定理（n=0 时的泰勒公式）
        info3 = Tex(r"\text{当}n = 0\text{时,就是大名鼎鼎的拉格朗日中值定理}", 
                    font_size=30, color=BLUE, tex_template=tex_template).next_to(info2, DOWN * 1.5)
        info3.set_font("SimSun")
        self.play(Write(info3))
        self.wait(1)

        # 拉格朗日中值定理公式
        info4 = Tex(r"$f'(\xi)=\frac{f(b)-f(a)}{b-a}, \text{其中 } [a,b]\text{连续}, (a,b)\text{可导}$", 
                    font_size=30, color=BLUE, tex_template=tex_template).next_to(info3, DOWN * 2)
        info4.set_font("SimSun")
        self.play(FadeIn(info4))
        self.wait(1)
        # 包围公式
        sr = SurroundingRectangle(info4, color=BLUE, buff=0.2, stroke_width=1)
        self.play(Create(sr))
        self.wait(3)

        # 罗尔中值定理（拉格朗日中值定理的特例）
        info5 = Tex(r"\text{当}$f(a)=f(b)$\text{时,就是罗尔中值定理：}$f'(\xi)=0$", 
                    font_size=30, color=ORANGE, tex_template=tex_template).next_to(info4, DOWN * 2)
        info5.set_font("SimSun")
        self.play(Write(info5))  # 注意：这里原代码可能有笔误，修正了 LaTeX 转义
        self.wait(3)

        # 柯西中值定理
        info6 = Tex(r"$\text{柯西中值定理：}\frac{f'(\xi)}{g'(\xi)}=\frac{f(b)-f(a)}{g(b)-g(a)}, \text{其中 } g'(\xi) \neq 0$", 
                    font_size=30, color=GREEN, tex_template=tex_template).next_to(info5, DOWN * 1.5)
        info6.set_font("SimSun")
        self.play(Write(info6))
        self.wait(5)  # 最后一个动画，等待结束