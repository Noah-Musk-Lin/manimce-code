from manim import *

class LagrangeMeanValueTheorem(Scene):
    def construct(self):
        config.font = "SimHei"
        config.background_color = "#1a1a2e"
        
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{ctex}")
        
        title = Tex(r"拉格朗日中值定理", font_size=48, color=BLUE, tex_template=tex_template)
        title.to_edge(UP)
        self.play(Write(title, run_time=1.5))
        self.wait(0.5)
        
        ax = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[-1, 5, 1],
            axis_config={"stroke_color": WHITE, "stroke_width": 2, "include_tip": True},
            x_length=7.5,
            y_length=5.5
        ).shift(LEFT * 0.5 + DOWN * 0.2)
        
        self.play(Create(ax), run_time=1.5)
        
        graph = ax.plot(lambda x: 0.4 * (x - 1) * (x - 3.5) + 0.5, x_range=[0.2, 4.8], color=YELLOW, stroke_width=3)
        self.play(Create(graph, run_time=2))
        
        a, b = 0.8, 4.2
        f = lambda x: 0.4 * (x - 1) * (x - 3.5) + 0.5
        ya, yb = f(a), f(b)
        
        A = Dot(ax.c2p(a, ya), color=GREEN, radius=0.08)
        B = Dot(ax.c2p(b, yb), color=GREEN, radius=0.08)
        
        label_A = Tex(r"A($a$,$f(a)$)", font_size=22, color=GREEN, tex_template=tex_template).next_to(A, DL, buff=0.15)
        label_B = Tex(r"B($b$,$f(b)$)", font_size=22, color=GREEN, tex_template=tex_template).next_to(B, DR, buff=0.15)
        
        self.play(FadeIn(A), FadeIn(B), run_time=0.8)
        self.play(Write(label_A), Write(label_B), run_time=0.8)
        
        secant = Line(ax.c2p(a, ya), ax.c2p(b, yb), color=BLUE, stroke_width=3)
        secant_label = Tex(r"割线", font_size=22, color=BLUE, tex_template=tex_template).move_to(ax.c2p(2.5, 2.8))
        
        self.play(Create(secant), run_time=1.5)
        self.play(Write(secant_label), run_time=0.8)
        
        c = 2.65
        yc = f(c)
        
        C = Dot(ax.c2p(c, yc), color=RED, radius=0.1)
        label_C = Tex(r"C($\xi$,$f(\xi)$)", font_size=22, color=RED, tex_template=tex_template).next_to(C, UP, buff=0.15)
        
        self.play(FadeIn(C, scale=0.5), Write(label_C, run_time=1), run_time=1.5)
        
        derivative = 0.8 * c - 1.8
        
        tangent = Line(
            ax.c2p(c - 1.2, yc - derivative * 1.2),
            ax.c2p(c + 1.2, yc + derivative * 1.2),
            color=RED,
            stroke_width=3
        )
        tangent_label = Tex(r"切线", font_size=22, color=RED, tex_template=tex_template).move_to(ax.c2p(3.5, 1.5))
        
        self.play(Create(tangent), run_time=1.5)
        self.play(Write(tangent_label), run_time=0.8)
        
        right_info = VGroup()
        
        theorem_title = Tex(r"定理内容", font_size=28, color=BLUE, tex_template=tex_template)
        right_info.add(theorem_title)
        
        theorem = Tex(r"若 $f \in C[a,b]$, $f \in C^1(a,b)$", font_size=22, color=WHITE, tex_template=tex_template)
        theorem.next_to(theorem_title, DOWN, buff=0.4)
        right_info.add(theorem)
        
        theorem2 = Tex(r"则 $\exists \xi \in (a,b)$, 使", font_size=22, color=WHITE, tex_template=tex_template)
        theorem2.next_to(theorem, DOWN, buff=0.3)
        right_info.add(theorem2)
        
        formula = Tex(r"$f'(\xi) = \frac{f(b)-f(a)}{b-a}$", font_size=26, color=YELLOW, tex_template=tex_template)
        formula.next_to(theorem2, DOWN, buff=0.4)
        right_info.add(formula)
        
        divider = Line(LEFT * 3.5, RIGHT * 3.5, color=GRAY, stroke_width=1)
        divider.next_to(formula, DOWN, buff=0.6)
        right_info.add(divider)
        
        calc_title = Tex(r"计算验证", font_size=28, color=GREEN, tex_template=tex_template)
        calc_title.next_to(divider, DOWN, buff=0.5)
        right_info.add(calc_title)
        
        sec_k = (yb - ya) / (b - a)
        sec_eq = Tex(rf"$k_{{割线}} = \frac{{{yb:.1f}-{ya:.1f}}}{{{b}-{a}}} = {sec_k:.2f}$", font_size=22, color=BLUE, tex_template=tex_template)
        sec_eq.next_to(calc_title, DOWN, buff=0.4)
        right_info.add(sec_eq)
        
        tang_k = derivative
        tang_eq = Tex(rf"$k_{{切线}} = f'(\xi) = {tang_k:.2f}$", font_size=22, color=RED, tex_template=tex_template)
        tang_eq.next_to(sec_eq, DOWN, buff=0.3)
        right_info.add(tang_eq)
        
        equal = Tex(r"$k_{割线} = k_{切线}$", font_size=26, color=YELLOW, tex_template=tex_template)
        equal.next_to(tang_eq, DOWN, buff=0.5)
        right_info.add(equal)
        
        geo_title = Tex(r"几何意义", font_size=28, color=BLUE, tex_template=tex_template)
        geo_title.next_to(equal, DOWN, buff=0.8)
        right_info.add(geo_title)
        
        geo_text = Tex(r"曲线上存在一点，其切线与割线平行", font_size=22, color=WHITE, tex_template=tex_template)
        geo_text.next_to(geo_title, DOWN, buff=0.4)
        right_info.add(geo_text)
        
        right_info.to_edge(RIGHT).shift(RIGHT * 0.5 + UP * 0.3)
        
        for item in right_info:
            if isinstance(item, Tex):
                self.play(Write(item, run_time=1))
            else:
                self.play(Create(item), run_time=0.8)
            self.wait(0.3)
        
        self.wait(4)