# -*- coding: utf-8 -*-
from manim import *


class Wronskian(Scene):
    def construct(self):
        # ============================================================
        # Part 1: 朗斯基行列式定义
        # ============================================================
        title1 = Text("朗斯基行列式", font_size=44, color=BLUE)
        self.play(Write(title1))
        self.wait(1.5)
        self.play(title1.animate.to_edge(UP))

        # 介绍文字 + 公式
        def_text = Text("对于一组函数", font_size=32)
        def_formula = MathTex(
            r"f_1(x),\; f_2(x),\; \cdots,\; f_n(x)",
            font_size=36,
        )
        def_group = VGroup(def_text, def_formula).arrange(RIGHT, buff=0.3)
        def_group.next_to(title1, DOWN, buff=0.8)

        # 朗斯基行列式定义
        wronskian_def = MathTex(
            r"W(f_1, \dots, f_n)(x) = \det",
            r"\begin{pmatrix}",
            r"f_1(x) & f_2(x) & \cdots & f_n(x) \\",
            r"f_1'(x) & f_2'(x) & \cdots & f_n'(x) \\",
            r"\vdots & \vdots & \ddots & \vdots \\",
            r"f_1^{(n-1)}(x) & f_2^{(n-1)}(x) & \cdots & f_n^{(n-1)}(x)",
            r"\end{pmatrix}",
            font_size=36,
        )
        wronskian_def.next_to(def_group, DOWN, buff=0.6)

        self.play(Write(def_group), run_time=1.5)
        self.wait(0.5)
        self.play(Write(wronskian_def), run_time=2)
        self.wait(3)

        # ============================================================
        # Part 2: 应用 —— 判断线性无关
        # ============================================================
        title2 = Text("应用：判断线性无关", font_size=44, color=YELLOW)
        title2.to_edge(UP)

        # 定理陈述
        theorem_line1 = Text("若存在点 ", font_size=30)
        theorem_math1 = MathTex(r"x_0", font_size=32)
        theorem_line2 = Text(" 使得 ", font_size=30)
        theorem_math2 = MathTex(r"W(f_1,\dots,f_n)(x_0) \neq 0", font_size=32)
        theorem_line3 = Text("，则", font_size=30)
        theorem_math3 = MathTex(r"\{f_1,\dots,f_n\}", font_size=32)
        theorem_line4 = Text("在区间上线性无关", font_size=30)

        theorem_row1 = VGroup(theorem_line1, theorem_math1, theorem_line2,
                              theorem_math2, theorem_line3).arrange(RIGHT, buff=0.1)
        theorem_row2 = VGroup(theorem_math3, theorem_line4).arrange(RIGHT, buff=0.1)
        theorem_group = VGroup(theorem_row1, theorem_row2).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        theorem_group.next_to(title2, DOWN, buff=0.5)

        # 证明标题
        proof_title = Text("证明思路：", font_size=30, color=GREEN)
        proof_title.next_to(theorem_group, DOWN, buff=0.4, aligned_edge=LEFT)

        # 证明步骤1
        ps1 = Text("假设存在不全为零的常数 ", font_size=26)
        ps1_math = MathTex(r"c_1, c_2, \cdots, c_n", font_size=28)
        ps1_end = Text("，使得：", font_size=26)
        ps1_group = VGroup(ps1, ps1_math, ps1_end).arrange(RIGHT, buff=0.1)
        ps1_group.next_to(proof_title, DOWN, buff=0.3, aligned_edge=LEFT)

        # 方程
        equation1 = MathTex(
            r"c_1 f_1(x) + c_2 f_2(x) + \cdots + c_n f_n(x) = 0",
            font_size=30,
        )
        equation1.next_to(ps1_group, DOWN, buff=0.3)

        # 证明步骤2
        ps2 = Text("对方程连续求导 ", font_size=26)
        ps2_math = MathTex(r"n-1", font_size=28)
        ps2_end = Text(" 次，得到线性方程组：", font_size=26)
        ps2_group = VGroup(ps2, ps2_math, ps2_end).arrange(RIGHT, buff=0.1)
        ps2_group.next_to(equation1, DOWN, buff=0.3, aligned_edge=LEFT)

        # 方程组
        equation2 = MathTex(
            r"\begin{cases}",
            r"c_1 f_1(x) + c_2 f_2(x) + \cdots + c_n f_n(x) = 0 \\",
            r"c_1 f_1'(x) + c_2 f_2'(x) + \cdots + c_n f_n'(x) = 0 \\",
            r"\qquad\vdots \\",
            r"c_1 f_1^{(n-1)}(x) + \cdots + c_n f_n^{(n-1)}(x) = 0",
            r"\end{cases}",
            font_size=26,
        )
        equation2.next_to(ps2_group, DOWN, buff=0.25)

        # 证明步骤3
        ps3 = Text("系数矩阵的行列式 ", font_size=26)
        ps3_math = MathTex(r"W(x_0) \neq 0", font_size=28)
        ps3_end = Text("，方程组只有零解 ", font_size=26)
        ps3_math2 = MathTex(r"c_1 = c_2 = \cdots = c_n = 0", font_size=28)
        ps3_group = VGroup(ps3, ps3_math, ps3_end, ps3_math2).arrange(RIGHT, buff=0.1)
        ps3_group.next_to(equation2, DOWN, buff=0.3)

        # 动画 Part 2
        self.play(
            ReplacementTransform(title1, title2),
            FadeOut(def_group),
            FadeOut(wronskian_def),
        )
        self.play(Write(theorem_group), run_time=2)
        self.wait(2)
        self.play(Write(proof_title))
        self.play(Write(ps1_group))
        self.play(Write(equation1))
        self.play(Write(ps2_group))
        self.play(Write(equation2))
        self.play(Write(ps3_group))
        self.wait(3)

        # ============================================================
        # Part 3: 示例
        # ============================================================
        title3 = Text("示例：检验线性无关", font_size=44, color=ORANGE)
        title3.to_edge(UP)

        # 函数及导数并排
        func_part = MathTex(r"f_1(x)=e^x,\; f_2(x)=e^{2x},\; x\in\mathbb{R}", font_size=28)
        deriv_part = MathTex(r"f_1'(x)=e^x,\; f_2'(x)=2e^{2x}", font_size=28)
        func_and_deriv = VGroup(func_part, deriv_part).arrange(RIGHT, buff=0.5)
        func_and_deriv.next_to(title3, DOWN, buff=0.4)

        # 朗斯基矩阵
        wronskian_matrix = MathTex(
            r"W(f_1, f_2)(x) = \det \begin{pmatrix} e^x & e^{2x} \\ e^x & 2e^{2x} \end{pmatrix}",
            font_size=32,
        )
        wronskian_matrix.next_to(func_and_deriv, DOWN, buff=0.3)

        # 计算过程（从第二步开始，矩阵已在上面展示）
        result = MathTex(
            r"\begin{aligned}"
            r"&= e^x \cdot 2e^{2x} - e^{2x} \cdot e^x \\"
            r"&= 2e^{3x} - e^{3x} \\"
            r"&= e^{3x}"
            r"\end{aligned}",
            font_size=30,
        )
        result.next_to(wronskian_matrix, DOWN, buff=0.25)

        # 非零判定 + 结论合并为一行
        summary = VGroup(
            MathTex(r"e^{3x} \neq 0 \;(\forall x\in\mathbb{R})", font_size=28, color=GREEN),
            Text("  →  ", font_size=28),
            Text("因此 ", font_size=28),
            MathTex(r"e^x", font_size=30),
            Text(" 和 ", font_size=28),
            MathTex(r"e^{2x}", font_size=30),
            Text("线性无关", font_size=28, color=YELLOW),
        ).arrange(RIGHT, buff=0.08)
        summary.next_to(result, DOWN, buff=0.3)

        # 动画 Part 3
        self.play(
            ReplacementTransform(title2, title3),
            FadeOut(VGroup(theorem_group, proof_title, ps1_group, equation1,
                          ps2_group, equation2, ps3_group)),
        )
        self.play(Write(func_and_deriv))
        self.play(Write(wronskian_matrix))
        self.play(Write(result), run_time=2)
        self.play(Write(summary))
        self.wait(3)

        # ============================================================
        # 结尾
        # ============================================================
        final_text = Text(
            "朗斯基行列式是判断函数线性无关的有力工具",
            font_size=38,
            color=BLUE,
        )
        self.play(FadeOut(VGroup(
            title3, func_and_deriv,
            wronskian_matrix, result, summary,
        )))
        self.play(Write(final_text))
        self.wait(3)
        self.play(FadeOut(final_text))
