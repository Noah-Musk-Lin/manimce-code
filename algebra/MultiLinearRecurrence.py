# -*- coding: utf-8 -*-
from manim import *


class MultiLinearRecurrence(Scene):
    def construct(self):
        # ============================================================
        # §1 标题页
        # ============================================================
        title = Text("多元线性递推数列极限求解", font_size=42, color=BLUE, font="SimSun")
        subtitle = Text("八种方法详解", font_size=26, color=GRAY, font="SimSun")
        subtitle.next_to(title, DOWN, buff=0.25)

        self.play(Write(title))
        self.play(Write(subtitle))
        self.wait(2)
        self.play(FadeOut(subtitle))

        # ============================================================
        # §2 问题陈述
        # ============================================================
        sec_title = Text("问题陈述", font_size=34, color=YELLOW, font="SimSun")
        sec_title.to_edge(UP)
        self.play(ReplacementTransform(title, sec_title))

        problem_intro = VGroup(
            Text("给定数列", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"\{x_n\},\{y_n\},\{z_n\}", font_size=28, color=YELLOW),
            Text("满足：", font_size=26, color=WHITE, font="SimSun"),
        ).arrange(RIGHT, buff=0.1)
        problem_intro.next_to(sec_title, DOWN, buff=0.5)

        init_cond = VGroup(
            Text("初始条件：", font_size=24, color=WHITE, font="SimSun"),
            MathTex(r"x_1=-2,\; y_1=1,\; z_1=-1", font_size=26, color=YELLOW),
        ).arrange(RIGHT, buff=0.15)
        init_cond.next_to(problem_intro, DOWN, buff=0.25)

        recurrence = MathTex(
            r"\begin{cases}",
            r"x_{n+1}=3x_n-6y_n-z_n \\[3pt]",
            r"y_{n+1}=-x_n+2y_n+z_n \\[3pt]",
            r"z_{n+1}=x_n+3y_n-z_n",
            r"\end{cases}",
            font_size=30, color=WHITE,
        )
        recurrence.next_to(init_cond, DOWN, buff=0.3)

        goal = VGroup(
            Text("求极限：", font_size=26, color=WHITE, font="SimSun"),
            MathTex(
                r"\lim_{n\to\infty}\frac{x_n+y_n+z_n}{3^n+5^n}",
                font_size=32, color=YELLOW,
            ),
        ).arrange(RIGHT, buff=0.15)
        goal.next_to(recurrence, DOWN, buff=0.3)

        self.play(Write(problem_intro))
        self.wait(0.3)
        self.play(Write(init_cond))
        self.wait(0.3)
        self.play(Write(recurrence))
        self.wait(0.3)
        self.play(Write(goal))
        self.wait(2)
        self.play(FadeOut(VGroup(sec_title, problem_intro, init_cond, recurrence, goal)))

        # ============================================================
        # §3 公共步骤：不变量发现
        # ============================================================
        inv_title = Text("公共基础：发现不变量", font_size=32, color=GREEN, font="SimSun")
        inv_title.to_edge(UP)
        self.play(Write(inv_title))

        inv_idea = VGroup(
            Text("构造", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"T_n = a x_n + b y_n + c z_n", font_size=28, color=YELLOW),
            Text("，使", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"T_{n+1}=T_n", font_size=28, color=GREEN),
        ).arrange(RIGHT, buff=0.1)
        inv_idea.next_to(inv_title, DOWN, buff=0.45)

        self.play(Write(inv_idea))
        self.wait(1.2)

        inv_coeff = MathTex(
            r"\begin{cases}",
            r"2a - b + c = 0 \\",
            r"-6a + b + 3c = 0 \\",
            r"-a + b - 2c = 0",
            r"\end{cases}",
            font_size=28, color=WHITE,
        )
        inv_coeff.next_to(inv_idea, DOWN, buff=0.3)

        inv_solve = VGroup(
            Text("解得", font_size=24, color=WHITE, font="SimSun"),
            MathTex(r"a=1,\; b=3,\; c=1", font_size=26, color=GREEN),
        ).arrange(RIGHT, buff=0.15)
        inv_solve.next_to(inv_coeff, DOWN, buff=0.25)

        self.play(Write(inv_coeff))
        self.wait(0.6)
        self.play(Write(inv_solve))
        self.wait(0.8)

        inv_result = VGroup(
            Text("不变量：", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"T_n = x_n + 3y_n + z_n \equiv 0", font_size=30, color=YELLOW),
        ).arrange(RIGHT, buff=0.15)
        inv_result.next_to(inv_solve, DOWN, buff=0.3)

        inv_verify = VGroup(
            Text("验证", font_size=22, color=WHITE, font="SimSun"),
            MathTex(r"T_1 = -2+3+(-1)=0", font_size=24, color=GREEN),
            Text("，对所有", font_size=22, color=WHITE, font="SimSun"),
            MathTex(r"n", font_size=24, color=YELLOW),
            Text("成立", font_size=22, color=WHITE, font="SimSun"),
        ).arrange(RIGHT, buff=0.1)
        inv_verify.next_to(inv_result, DOWN, buff=0.25)

        self.play(Write(inv_result))
        self.wait(0.4)
        self.play(Write(inv_verify))
        self.wait(1.2)

        inv_reduce = VGroup(
            Text("由此", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"z_n = -x_n - 3y_n", font_size=26, color=ORANGE),
            Text("，令", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"S_n = x_n+y_n+z_n = -2y_n", font_size=26, color=YELLOW),
        ).arrange(RIGHT, buff=0.1)
        inv_reduce.next_to(inv_verify, DOWN, buff=0.3)

        inv_box = SurroundingRectangle(inv_result[1], color=YELLOW, buff=0.12)
        self.play(Write(inv_reduce))
        self.play(Create(inv_box))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            inv_title, inv_idea, inv_coeff, inv_solve,
            inv_result, inv_verify, inv_reduce, inv_box,
        )))

        # ============================================================
        # §4 方法一：数学归纳法
        # ============================================================
        m1_title, m1_sub = self._method_header("方法一：数学归纳法", "猜想通项 + 归纳证明")

        m1_step1 = Text("步骤1：归纳证明不变量", font_size=24, color=YELLOW, font="SimSun")
        m1_step1.next_to(m1_sub, DOWN, buff=0.4)

        m1_base = VGroup(
            Text("基例：", font_size=22, color=GREEN, font="SimSun"),
            MathTex(r"T_1 = x_1+3y_1+z_1 = -2+3+(-1)=0", font_size=22, color=WHITE),
        ).arrange(RIGHT, buff=0.12)
        m1_base.next_to(m1_step1, DOWN, buff=0.25, aligned_edge=LEFT)

        m1_ind = VGroup(
            Text("归纳：假设", font_size=22, color=GREEN, font="SimSun"),
            MathTex(r"T_k=0", font_size=22, color=YELLOW),
            Text("，则", font_size=22, color=WHITE, font="SimSun"),
            MathTex(r"T_{k+1}=x_{k+1}+3y_{k+1}+z_{k+1}=T_k=0", font_size=20, color=WHITE),
        ).arrange(RIGHT, buff=0.08)
        m1_ind.next_to(m1_base, DOWN, buff=0.22, aligned_edge=LEFT)

        self.play(Write(m1_step1))
        self.play(Write(m1_base))
        self.wait(0.3)
        self.play(Write(m1_ind))
        self.wait(1.2)

        self.play(FadeOut(VGroup(m1_step1, m1_base, m1_ind)))

        m1_step2 = Text("步骤2：推导通项并归纳证明", font_size=24, color=YELLOW, font="SimSun")
        m1_step2.next_to(m1_sub, DOWN, buff=0.4)

        m1_recur = MathTex(
            r"y_{n+2} = 3y_{n+1} + 10y_n,\quad y_1=1,\; y_2=3",
            font_size=26, color=WHITE,
        )
        m1_recur.next_to(m1_step2, DOWN, buff=0.3)

        m1_guess = VGroup(
            Text("猜想：", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"y_n = \frac{5^n-(-2)^n}{7}", font_size=26, color=YELLOW),
        ).arrange(RIGHT, buff=0.1)
        m1_guess.next_to(m1_recur, DOWN, buff=0.25)

        m1_prove = VGroup(
            Text("归纳证明：假设", font_size=22, color=WHITE, font="SimSun"),
            MathTex(r"n=k,k+1", font_size=22, color=YELLOW),
            Text("成立，代入递推验证", font_size=22, color=WHITE, font="SimSun"),
            MathTex(r"n=k+2", font_size=22, color=YELLOW),
            Text("亦成立", font_size=22, color=WHITE, font="SimSun"),
        ).arrange(RIGHT, buff=0.08)
        m1_prove.next_to(m1_guess, DOWN, buff=0.25)

        self.play(Write(m1_step2))
        self.play(Write(m1_recur))
        self.wait(0.3)
        self.play(Write(m1_guess))
        self.wait(0.3)
        self.play(Write(m1_prove))
        self.wait(1.2)

        self._show_limit_result(m1_title, m1_sub, m1_step2, m1_recur, m1_guess, m1_prove)

        # ============================================================
        # §5 方法二：特征方程特征根法
        # ============================================================
        m2_title, m2_sub = self._method_header("方法二：特征方程特征根法", "标准代数方法，系统规范")

        m2_recur = MathTex(
            r"y_{n+2} - 3y_{n+1} - 10y_n = 0",
            font_size=30, color=YELLOW,
        )
        m2_recur.next_to(m2_sub, DOWN, buff=0.4)

        self.play(Write(m2_recur))
        self.wait(0.8)

        m2_char = VGroup(
            Text("特征方程：", font_size=28, color=WHITE, font="SimSun"),
            MathTex(r"r^2 - 3r - 10 = 0", font_size=28, color=WHITE),
        ).arrange(RIGHT, buff=0.1)
        m2_char.next_to(m2_recur, DOWN, buff=0.3)

        m2_roots = MathTex(
            r"\implies (r-5)(r+2)=0 \implies r_1=5,\; r_2=-2",
            font_size=26, color=ORANGE,
        )
        m2_roots.next_to(m2_char, DOWN, buff=0.25)

        self.play(Write(m2_char))
        self.wait(0.3)
        self.play(Write(m2_roots))
        self.wait(0.8)

        m2_general = MathTex(
            r"y_n = A\cdot 5^{\,n} + B\cdot (-2)^{\,n}",
            font_size=28, color=GREEN,
        )
        m2_general.next_to(m2_roots, DOWN, buff=0.3)

        m2_solve = MathTex(
            r"\begin{cases}5A-2B=1\\25A+4B=3\end{cases}"
            r"\;\implies\; A=\frac{1}{7},\; B=-\frac{1}{7}",
            font_size=26, color=WHITE,
        )
        m2_solve.next_to(m2_general, DOWN, buff=0.25)

        self.play(Write(m2_general))
        self.wait(0.3)
        self.play(Write(m2_solve))
        self.wait(0.8)

        m2_yn = MathTex(
            r"y_n = \frac{5^{\,n} - (-2)^{\,n}}{7}",
            font_size=30, color=YELLOW,
        )
        m2_yn.next_to(m2_solve, DOWN, buff=0.3)

        self.play(Write(m2_yn))
        self.wait(0.4)

        self._show_limit_result(m2_title, m2_sub, m2_recur, m2_char, m2_roots, m2_general, m2_solve, m2_yn)

        # ============================================================
        # §6 方法三：矩阵递推法
        # ============================================================
        m3_title, m3_sub = self._method_header("方法三：矩阵递推法", "矩阵对角化，理论统一")

        m3_intro = VGroup(
            Text("状态向量", font_size=24, color=WHITE, font="SimSun"),
            MathTex(r"\mathbf{v}_n = \begin{pmatrix}x_n\\y_n\\z_n\end{pmatrix}", font_size=24, color=YELLOW),
        ).arrange(RIGHT, buff=0.12)
        m3_intro.next_to(m3_sub, DOWN, buff=0.4)

        m3_matrix = Matrix([
            ["3", "-6", "-1"],
            ["-1", "2", "1"],
            ["1", "3", "-1"],
        ]).scale(0.6)
        m3_label = MathTex(r"A = ", font_size=24, color=WHITE)
        m3_label.next_to(m3_matrix, LEFT)
        m3_mat_group = VGroup(m3_label, m3_matrix)
        m3_mat_group.next_to(m3_intro, DOWN, buff=0.25)

        m3_power = MathTex(
            r"\mathbf{v}_{n+1}=A\mathbf{v}_n,\; \mathbf{v}_n=A^{\,n-1}\mathbf{v}_1",
            font_size=24, color=WHITE,
        )
        m3_power.next_to(m3_mat_group, DOWN, buff=0.25)

        self.play(Write(m3_intro))
        self.play(Write(m3_mat_group))
        self.play(Write(m3_power))
        self.wait(1.2)

        self.play(FadeOut(VGroup(m3_intro, m3_mat_group, m3_power)))

        m3_eigen_title = Text("特征值与特征向量分解", font_size=24, color=YELLOW, font="SimSun")
        m3_eigen_title.next_to(m3_sub, DOWN, buff=0.45)

        m3_eigen = MathTex(
            r"\lambda_1=1,\;\lambda_2=5,\;\lambda_3=-2",
            font_size=26, color=ORANGE,
        )
        m3_eigen.next_to(m3_eigen_title, DOWN, buff=0.3)

        m3_decomp = MathTex(
            r"\mathbf{v}_1 = 0\cdot\boldsymbol{\xi}_1"
            r"+\frac{5}{7}\boldsymbol{\xi}_2+\frac{1}{7}\boldsymbol{\xi}_3",
            font_size=23, color=WHITE,
        )
        m3_decomp.next_to(m3_eigen, DOWN, buff=0.25)

        m3_vn = MathTex(
            r"\mathbf{v}_n = \frac{5^{\,n}}{7}\boldsymbol{\xi}_2"
            r"+\frac{(-2)^{\,n-1}}{7}\boldsymbol{\xi}_3",
            font_size=23, color=WHITE,
        )
        m3_vn.next_to(m3_decomp, DOWN, buff=0.25)

        self.play(Write(m3_eigen_title))
        self.play(Write(m3_eigen))
        self.wait(0.3)
        self.play(Write(m3_decomp))
        self.play(Write(m3_vn))
        self.wait(0.8)

        m3_sn = MathTex(
            r"S_n = (1,1,1)\mathbf{v}_n"
            r"= -\frac{2}{7}\bigl[5^{\,n}-(-2)^{\,n}\bigr]",
            font_size=25, color=GREEN,
        )
        m3_sn.next_to(m3_vn, DOWN, buff=0.3)

        self.play(Write(m3_sn))
        self.wait(0.4)

        self._show_limit_result(m3_title, m3_sub, m3_eigen_title, m3_eigen, m3_decomp, m3_vn, m3_sn)

        # ============================================================
        # §7 方法四：Stolz 定理
        # ============================================================
        m4_title, m4_sub = self._method_header("方法四：Stolz 定理", "数列极限的洛必达法则")

        m4_intro = VGroup(
            Text("令", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"a_n = \frac{S_n}{5^n}", font_size=28, color=YELLOW),
            Text("，原极限", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"=\lim_{n\to\infty}a_n", font_size=28, color=YELLOW),
        ).arrange(RIGHT, buff=0.1)
        m4_intro.next_to(m4_sub, DOWN, buff=0.4)

        self.play(Write(m4_intro))
        self.wait(0.8)

        m4_stolz1 = MathTex(
            r"\lim_{n\to\infty}\frac{S_n}{5^n}"
            r"=\lim_{n\to\infty}\frac{S_{n+1}-S_n}{5^{\,n+1}-5^{\,n}}",
            font_size=25, color=WHITE,
        )
        m4_stolz1.next_to(m4_intro, DOWN, buff=0.3)

        m4_stolz2 = MathTex(
            r"=\lim_{n\to\infty}\frac{S_{n+1}-S_n}{4\cdot 5^{\,n}}",
            font_size=25, color=WHITE,
        )
        m4_stolz2.next_to(m4_stolz1, DOWN, buff=0.22)

        m4_stolz3 = MathTex(
            r"\xrightarrow{\text{Stolz}}"
            r"\lim_{n\to\infty}\frac{S_{n+2}-2S_{n+1}+S_n}{16\cdot 5^{\,n}}",
            font_size=23, color=WHITE,
        )
        m4_stolz3.next_to(m4_stolz2, DOWN, buff=0.22)

        self.play(Write(m4_stolz1))
        self.wait(0.3)
        self.play(Write(m4_stolz2))
        self.wait(0.3)
        self.play(Write(m4_stolz3))
        self.wait(0.8)

        m4_sub_eq = VGroup(
            MathTex(r"S_{n+2}=3S_{n+1}+10S_n", font_size=22, color=ORANGE),
            Text("代入得", font_size=22, color=WHITE, font="SimSun"),
            MathTex(r"a_{n+2}=\frac{3}{5}a_{n+1}+\frac{2}{5}a_n", font_size=22, color=ORANGE),
        ).arrange(RIGHT, buff=0.08)
        m4_sub_eq.next_to(m4_stolz3, DOWN, buff=0.25)

        m4_char = VGroup(
            Text("特征根：", font_size=24, color=WHITE, font="SimSun"),
            MathTex(r"r=1,-\frac{2}{5}", font_size=24, color=WHITE),
            MathTex(r"\implies a_n = A + B(-\tfrac{2}{5})^n", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.08)
        m4_char.next_to(m4_sub_eq, DOWN, buff=0.25)

        m4_result = MathTex(
            r"\lim_{n\to\infty} a_n = A = -\frac{2}{7}",
            font_size=28, color=YELLOW,
        )
        m4_result.next_to(m4_char, DOWN, buff=0.25)

        self.play(Write(m4_sub_eq))
        self.wait(0.3)
        self.play(Write(m4_char))
        self.wait(0.3)
        self.play(Write(m4_result))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            m4_title, m4_sub, m4_intro, m4_stolz1, m4_stolz2, m4_stolz3,
            m4_sub_eq, m4_char, m4_result,
        )))

        # ============================================================
        # §8 方法五：生成函数法
        # ============================================================
        m5_title, m5_sub = self._method_header("方法五：生成函数法", "幂级数代数运算")

        m5_def = MathTex(
            r"G(x) = \sum_{n=1}^{\infty} S_n x^{\,n}",
            font_size=28, color=YELLOW,
        )
        m5_def.next_to(m5_sub, DOWN, buff=0.4)

        self.play(Write(m5_def))
        self.wait(0.8)

        m5_sub_eq = MathTex(
            r"S_{n+2}=3S_{n+1}+10S_n"
            r"\;\implies\; G(x) = \frac{-2x}{1-3x-10x^2}",
            font_size=24, color=WHITE,
        )
        m5_sub_eq.next_to(m5_def, DOWN, buff=0.3)

        self.play(Write(m5_sub_eq))
        self.wait(0.8)

        m5_partial = MathTex(
            r"\frac{-2x}{(1-5x)(1+2x)}"
            r"= -\frac{2}{7}\cdot\frac{1}{1-5x}"
            r"+ \frac{2}{7}\cdot\frac{1}{1+2x}",
            font_size=24, color=WHITE,
        )
        m5_partial.next_to(m5_sub_eq, DOWN, buff=0.25)

        self.play(Write(m5_partial))
        self.wait(0.8)

        m5_expand = MathTex(
            r"G(x) = \sum_{n=0}^{\infty}"
            r"\Bigl[-\frac{2}{7}\cdot5^{\,n}+\frac{2}{7}\cdot(-2)^{\,n}\Bigr]x^{\,n}",
            font_size=24, color=WHITE,
        )
        m5_expand.next_to(m5_partial, DOWN, buff=0.25)

        m5_sn = MathTex(
            r"\implies S_n = -\frac{2}{7}\bigl[5^{\,n}-(-2)^{\,n}\bigr]",
            font_size=26, color=GREEN,
        )
        m5_sn.next_to(m5_expand, DOWN, buff=0.25)

        self.play(Write(m5_expand))
        self.wait(0.3)
        self.play(Write(m5_sn))
        self.wait(0.4)

        self._show_limit_result(m5_title, m5_sub, m5_def, m5_sub_eq, m5_partial, m5_expand, m5_sn)

        # ============================================================
        # §9 方法六：主导项分析法
        # ============================================================
        m6_title, m6_sub = self._method_header("方法六：主导项分析法", "仅需主导项系数，速度最快")

        m6_intro = VGroup(
            Text("通项", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"S_n = A\cdot5^{\,n} + B\cdot(-2)^{\,n}", font_size=28, color=YELLOW),
        ).arrange(RIGHT, buff=0.1)
        m6_intro.next_to(m6_sub, DOWN, buff=0.4)

        self.play(Write(m6_intro))
        self.wait(0.8)

        m6_compare = VGroup(
            Text("当", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"n\to\infty", font_size=28, color=YELLOW),
            Text("时，", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"|5| > |-2|", font_size=28, color=RED),
        ).arrange(RIGHT, buff=0.1)
        m6_compare.next_to(m6_intro, DOWN, buff=0.3)

        m6_dominant = VGroup(
            Text("故", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"5^{\,n}", font_size=28, color=RED),
            Text("主导，", font_size=26, color=WHITE, font="SimSun"),
            MathTex(r"(-2)^{\,n}", font_size=28, color=ORANGE),
            Text("可忽略", font_size=26, color=WHITE, font="SimSun"),
        ).arrange(RIGHT, buff=0.1)
        m6_dominant.next_to(m6_compare, DOWN, buff=0.25)

        self.play(Write(m6_compare))
        self.wait(0.4)
        self.play(Write(m6_dominant))
        self.wait(1)

        m6_asymp = MathTex(
            r"S_n \sim A\cdot5^{\,n},\qquad 3^{\,n}+5^{\,n} \sim 5^{\,n}",
            font_size=28, color=WHITE,
        )
        m6_asymp.next_to(m6_dominant, DOWN, buff=0.3)

        m6_ratio = MathTex(
            r"\lim_{n\to\infty}\frac{S_n}{3^n+5^n}"
            r"= \lim_{n\to\infty}\frac{A\cdot5^{\,n}}{5^{\,n}} = A",
            font_size=28, color=YELLOW,
        )
        m6_ratio.next_to(m6_asymp, DOWN, buff=0.25)

        self.play(Write(m6_asymp))
        self.wait(0.3)
        self.play(Write(m6_ratio))
        self.wait(0.8)

        m6_solve = MathTex(
            r"\begin{cases}5A-2B=-2\\25A+4B=-6\end{cases}"
            r"\;\implies\; A = -\frac{2}{7}",
            font_size=26, color=GREEN,
        )
        m6_solve.next_to(m6_ratio, DOWN, buff=0.3)

        m6_final = MathTex(
            r"\therefore \lim_{n\to\infty}\frac{S_n}{3^n+5^n}= -\frac{2}{7}",
            font_size=32, color=YELLOW,
        )
        m6_final.next_to(m6_solve, DOWN, buff=0.25)

        self.play(Write(m6_solve))
        self.wait(0.3)
        self.play(Write(m6_final))
        self.wait(1.5)

        self.play(FadeOut(VGroup(
            m6_title, m6_sub, m6_intro, m6_compare, m6_dominant,
            m6_asymp, m6_ratio, m6_solve, m6_final,
        )))

        # ============================================================
        # §10 方法七：谱半径与渐近行为法
        # ============================================================
        m7_title, m7_sub = self._method_header("方法七：谱半径与渐近行为法", "揭示长期行为本质")

        m7_intro = VGroup(
            Text("谱半径：", font_size=26, color=WHITE, font="SimSun"),
            MathTex(
                r"\rho(A)=\max\{|\lambda_1|,|\lambda_2|,|\lambda_3|\}=5",
                font_size=24, color=RED,
            ),
        ).arrange(RIGHT, buff=0.1)
        m7_intro.next_to(m7_sub, DOWN, buff=0.4)

        self.play(Write(m7_intro))
        self.wait(1)

        m7_asy = MathTex(
            r"\mathbf{v}_n \sim C \cdot 5^{\,n} \cdot \boldsymbol{\xi}"
            r"\;\sim\; \frac{5^{\,n}}{7}\begin{pmatrix}-3\\1\\0\end{pmatrix}",
            font_size=24, color=WHITE,
        )
        m7_asy.next_to(m7_intro, DOWN, buff=0.3)

        m7_sn = MathTex(
            r"S_n = (1,1,1)\mathbf{v}_n"
            r"\sim -\frac{2}{7}\cdot5^{\,n}",
            font_size=24, color=WHITE,
        )
        m7_sn.next_to(m7_asy, DOWN, buff=0.25)

        self.play(Write(m7_asy))
        self.wait(0.4)
        self.play(Write(m7_sn))
        self.wait(0.8)

        m7_note = VGroup(
            Text("谱半径", font_size=24, color=RED, font="SimSun"),
            MathTex(r"\rho(A)=5", font_size=24, color=RED),
            Text("决定发散速率，长期行为由对应特征向量主导", font_size=22, color=WHITE, font="SimSun"),
        ).arrange(RIGHT, buff=0.08)
        m7_note.next_to(m7_sn, DOWN, buff=0.3)

        self.play(Write(m7_note))
        self.wait(0.8)

        self._show_limit_result(m7_title, m7_sub, m7_intro, m7_asy, m7_sn, m7_note)

        # ============================================================
        # §11 方法八：哈密顿-凯莱定理法
        # ============================================================
        m8_title, m8_sub = self._method_header("方法八：哈密顿-凯莱定理法", "无需对角化，最优雅")

        m8_poly = MathTex(
            r"f(\lambda)=\det(\lambda E-A)"
            r"= \lambda^3-4\lambda^2-7\lambda+10",
            font_size=24, color=WHITE,
        )
        m8_poly.next_to(m8_sub, DOWN, buff=0.4)

        self.play(Write(m8_poly))
        self.wait(0.8)

        m8_hamilton = MathTex(
            r"\text{Hamilton-Cayley: } f(A)=O"
            r"\;\implies\; A^3-4A^2-7A+10E=O",
            font_size=24, color=YELLOW,
        )
        m8_hamilton.next_to(m8_poly, DOWN, buff=0.3)

        m8_recur = VGroup(
            Text("递推：", font_size=24, color=WHITE, font="SimSun"),
            MathTex(r"S_{n+3}-4S_{n+2}-7S_{n+1}+10S_n=0", font_size=24, color=WHITE),
        ).arrange(RIGHT, buff=0.08)
        m8_recur.next_to(m8_hamilton, DOWN, buff=0.25)

        self.play(Write(m8_hamilton))
        self.wait(0.4)
        self.play(Write(m8_recur))
        self.wait(0.8)

        m8_solve = VGroup(
            Text("特征根：", font_size=24, color=WHITE, font="SimSun"),
            MathTex(r"1,5,-2", font_size=24, color=WHITE),
            MathTex(r"\implies S_n = A + B\cdot5^{\,n} + C\cdot(-2)^{\,n}", font_size=23, color=WHITE),
        ).arrange(RIGHT, buff=0.08)
        m8_solve.next_to(m8_recur, DOWN, buff=0.25)

        m8_final = MathTex(
            r"S_1=-2,S_2=-6,S_3=-38 \implies A=0,B=-\frac{2}{7},C=\frac{2}{7}",
            font_size=22, color=GREEN,
        )
        m8_final.next_to(m8_solve, DOWN, buff=0.25)

        self.play(Write(m8_solve))
        self.wait(0.3)
        self.play(Write(m8_final))
        self.wait(0.8)

        m8_adv = Text("优势：只需特征多项式，无需特征向量与矩阵求逆", font_size=22, color=ORANGE, font="SimSun")
        m8_adv.next_to(m8_final, DOWN, buff=0.3)

        self.play(Write(m8_adv))
        self.wait(0.8)

        self._show_limit_result(m8_title, m8_sub, m8_poly, m8_hamilton, m8_recur, m8_solve, m8_final, m8_adv)

        # ============================================================
        # §12 八种方法对比表
        # ============================================================
        comp_title = Text("八种方法对比总结", font_size=32, color=BLUE, font="SimSun")
        comp_title.to_edge(UP)
        self.play(Write(comp_title))

        table_data = [
            ["方法", "核心思路", "适用场景"],
            ["① 数学归纳法", "猜想通项+归纳证明", "简单递推"],
            ["② 特征方程法", "一元递推+求特征根", "低维线性递推"],
            ["③ 矩阵递推法", "矩阵对角化求幂", "高维递推系统"],
            ["④ Stolz定理", "转化为差商极限", "指数型极限"],
            ["⑤ 生成函数法", "幂级数+代数运算", "任意阶递推"],
            ["⑥ 主导项分析", "仅考虑最大特征根", "快速求极限"],
            ["⑦ 谱半径法", "谱半径主导渐近", "长期行为分析"],
            ["⑧ 哈密顿-凯莱法", "特征多项式推递推", "避免矩阵运算"],
        ]

        table = Table(
            table_data,
            include_outer_lines=True,
            line_config={"color": GRAY},
        ).scale(0.48)
        table.next_to(comp_title, DOWN, buff=0.4)

        table.add_highlighted_cell((7, 1), color=YELLOW)
        table.add_highlighted_cell((7, 2), color=YELLOW)
        table.add_highlighted_cell((7, 3), color=YELLOW)

        self.play(Write(table))
        self.wait(5)

        self.play(FadeOut(VGroup(comp_title, table)))

        # ============================================================
        # §13 最终结果
        # ============================================================
        final_title = Text("最终结果", font_size=34, color=BLUE, font="SimSun")
        final_title.to_edge(UP)
        self.play(Write(final_title))

        final_answer = MathTex(
            r"\lim_{n\to\infty}\frac{x_n+y_n+z_n}{3^{\,n}+5^{\,n}}"
            r"= -\frac{2}{7}",
            font_size=44, color=YELLOW,
        )
        final_answer.next_to(final_title, DOWN, buff=1.2)

        final_box = SurroundingRectangle(
            final_answer, color=YELLOW, buff=0.25, stroke_width=3,
        )

        self.play(Write(final_answer))
        self.play(Create(final_box))
        self.wait(3)

        end_text = Text("感谢观看", font_size=34, color=BLUE, font="SimSun")
        end_text.next_to(final_box, DOWN, buff=0.8)

        self.play(Write(end_text))
        self.wait(3)

        self.play(FadeOut(VGroup(final_title, final_answer, final_box, end_text)))
        self.wait(1)

    # ================================================================
    # 辅助方法
    # ================================================================

    def _method_header(self, title_text, subtitle_text):
        """统一的 method 标题动画。返回 (title, subtitle) 供后续定位。"""
        m_title = Text(title_text, font_size=30, color=BLUE, font="SimSun")
        m_title.to_edge(UP)
        m_sub = Text(subtitle_text, font_size=20, color=GRAY, font="SimSun")
        m_sub.next_to(m_title, DOWN, buff=0.12)

        self.play(Write(m_title), Write(m_sub))
        self.wait(0.6)
        return m_title, m_sub

    def _show_limit_result(self, *mobjects_to_clear):
        """统一展示极限结果 = -2/7 并清除所有传入对象"""
        limit_result = MathTex(
            r"\lim_{n\to\infty}\frac{S_n}{3^n+5^n}"
            r"= -\frac{2}{7}",
            font_size=30, color=YELLOW,
        )
        # 放在最后一个内容元素下方
        if mobjects_to_clear:
            limit_result.next_to(mobjects_to_clear[-1], DOWN, buff=0.4)
        rect = SurroundingRectangle(limit_result, color=YELLOW, buff=0.15)

        self.play(Write(limit_result), Create(rect))
        self.wait(1.5)

        all_mobs = list(mobjects_to_clear) + [limit_result, rect]
        self.play(FadeOut(VGroup(*all_mobs)))
