from manim import *

class BlockMatrixScene(Scene):
    def construct(self):
        self.next_section("Title", skip_animations=False)
        title = Text("分块矩阵", font_size=48, color=BLUE).to_edge(UP)
        subtitle = Text("定义 · 性质 · 证明", font_size=26, color=GRAY).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Write(subtitle))
        self.wait(0.8)
        self.play(FadeOut(subtitle))

        # ---------- 一、分块矩阵的定义 ----------
        self.next_section("Definition", skip_animations=False)
        sec1 = Text("一、分块矩阵的定义", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Transform(title, sec1))

        mat = Matrix(
            [["1", "2", "3", "4"],
             ["5", "6", "7", "8"],
             ["9", "10", "11", "12"],
             ["13", "14", "15", "16"]],
            h_buff=1.3, v_buff=0.85,
        ).shift(LEFT * 2.0 + UP * 0.3)
        self.play(Write(mat))

        entries = mat.get_entries()
        e00, e01, e02, e03 = entries[0], entries[1], entries[2], entries[3]
        e10, e11, e12, e13 = entries[4], entries[5], entries[6], entries[7]
        e20, e21, e22, e23 = entries[8], entries[9], entries[10], entries[11]
        e30, e31, e32, e33 = entries[12], entries[13], entries[14], entries[15]

        mid_y = (e11.get_center()[1] + e21.get_center()[1]) / 2
        mid_x = (e11.get_center()[0] + e12.get_center()[0]) / 2

        h_line = Line(
            mat.get_left() + LEFT * 0.15,
            mat.get_right() + RIGHT * 0.15,
            color=YELLOW, stroke_width=4
        ).shift(DOWN * (mat.get_center()[1] - mid_y))
        v_line = Line(
            mat.get_top() + UP * 0.15,
            mat.get_bottom() + DOWN * 0.15,
            color=YELLOW, stroke_width=4
        ).shift(RIGHT * (mid_x - mat.get_center()[0]))
        self.play(Create(h_line), Create(v_line))

        def_text = Text("用横线和纵线将矩阵划分为若干子块", font_size=24)\
            .next_to(mat, DOWN, buff=0.35)
        self.play(Write(def_text))
        self.wait(0.8)
        self.play(FadeOut(def_text))

        tl = VGroup(e00, e01, e10, e11)
        tr = VGroup(e02, e03, e12, e13)
        bl = VGroup(e20, e21, e30, e31)
        br = VGroup(e22, e23, e32, e33)

        rect_tl = SurroundingRectangle(tl, color=RED, buff=0.2, stroke_width=3)
        rect_tr = SurroundingRectangle(tr, color=GREEN, buff=0.2, stroke_width=3)
        rect_bl = SurroundingRectangle(bl, color=BLUE, buff=0.2, stroke_width=3)
        rect_br = SurroundingRectangle(br, color=PURPLE, buff=0.2, stroke_width=3)

        self.play(Create(rect_tl))
        label = MathTex(r"A_{11}", font_size=30, color=RED).move_to(rect_tl)
        self.play(Write(label))
        self.wait(0.2)
        self.play(Transform(rect_tl, rect_tr),
                  Transform(label, MathTex(r"A_{12}", font_size=30, color=GREEN).move_to(rect_tr)))
        self.wait(0.2)
        self.play(Transform(rect_tl, rect_bl),
                  Transform(label, MathTex(r"A_{21}", font_size=30, color=BLUE).move_to(rect_bl)))
        self.wait(0.2)
        self.play(Transform(rect_tl, rect_br),
                  Transform(label, MathTex(r"A_{22}", font_size=30, color=PURPLE).move_to(rect_br)))
        self.wait(0.4)

        notation = MathTex(
            r"A = \begin{bmatrix}",
            r"A_{11} & A_{12} \\",
            r"A_{21} & A_{22}",
            r"\end{bmatrix}",
            font_size=34
        ).next_to(mat, RIGHT, buff=0.8)
        self.play(FadeOut(rect_tl), FadeOut(label))
        self.play(Write(notation))
        self.wait(0.5)

        gen_mat = MathTex(
            r"A = \begin{bmatrix}",
            r"A_{11} & A_{12} & A_{13} \\",
            r"A_{21} & A_{22} & A_{23} \\",
            r"A_{31} & A_{32} & A_{33}",
            r"\end{bmatrix}",
            font_size=28, color=DARK_BLUE
        ).next_to(notation, DOWN, buff=0.4).align_to(notation, LEFT)
        gen_label = Text("更一般的分块", font_size=20, color=GRAY).next_to(gen_mat, DOWN, buff=0.15)
        self.play(Write(gen_mat), Write(gen_label))
        self.wait(1.2)

        self.play(FadeOut(mat, h_line, v_line, notation, gen_mat, gen_label))

        # ---------- 二、按行 / 按列分块 ----------
        sec2 = Text("二、按行 / 按列分块", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Transform(title, sec2))

        row_mat = MathTex(
            r"A = \begin{bmatrix}",
            r"\boldsymbol{\alpha}_1 \\[4pt] \boldsymbol{\alpha}_2 \\[4pt] \vdots \\[4pt] \boldsymbol{\alpha}_m",
            r"\end{bmatrix}",
            font_size=34
        ).shift(LEFT * 2.5 + DOWN * 0.5)
        col_mat = MathTex(
            r"A = \begin{bmatrix}",
            r"\boldsymbol{\beta}_1 & \boldsymbol{\beta}_2 & \cdots & \boldsymbol{\beta}_n",
            r"\end{bmatrix}",
            font_size=34
        ).shift(RIGHT * 2.5 + DOWN * 0.5)

        row_label = Text("按行分块（行向量）", font_size=20, color=ORANGE)\
            .next_to(row_mat, DOWN, buff=0.2)
        col_label = Text("按列分块（列向量）", font_size=20, color=ORANGE)\
            .next_to(col_mat, DOWN, buff=0.2)

        block2 = MathTex(
            r"A = \begin{bmatrix}",
            r"A_{11} & A_{12} \\",
            r"A_{21} & A_{22}",
            r"\end{bmatrix}",
            font_size=38
        ).shift(DOWN * 2.2)
        block2_label = Text("四分块矩阵", font_size=20, color=ORANGE).next_to(block2, DOWN, buff=0.15)

        self.play(Write(row_mat), Write(row_label),
                  Write(col_mat), Write(col_label),
                  Write(block2), Write(block2_label))
        self.wait(1.5)
        self.play(FadeOut(row_mat, row_label, col_mat, col_label, block2, block2_label))

        # ---------- 三、分块矩阵的性质 ----------
        self.next_section("Properties - Addition", skip_animations=False)
        sec3 = Text("三、分块矩阵的性质", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Transform(title, sec3))

        p1 = Text("1. 分块加法", font_size=24, color=GREEN).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(p1))

        A_mat = MathTex(
            r"A = \begin{bmatrix}",
            r"A_{11} & A_{12} \\",
            r"A_{21} & A_{22}",
            r"\end{bmatrix}",
            font_size=30
        ).next_to(p1, DOWN, buff=0.35, aligned_edge=LEFT)
        B_mat = MathTex(
            r"B = \begin{bmatrix}",
            r"B_{11} & B_{12} \\",
            r"B_{21} & B_{22}",
            r"\end{bmatrix}",
            font_size=30
        ).next_to(A_mat, RIGHT, buff=0.4).align_to(A_mat, DOWN)
        plus = MathTex(r"+", font_size=38).next_to(A_mat, RIGHT, buff=0.2).align_to(A_mat, DOWN)
        eq = MathTex(r"=", font_size=38).next_to(B_mat, RIGHT, buff=0.3).align_to(A_mat, DOWN)
        sum_mat = MathTex(
            r"\begin{bmatrix}",
            r"A_{11}+B_{11} & A_{12}+B_{12} \\",
            r"A_{21}+B_{21} & A_{22}+B_{22}",
            r"\end{bmatrix}",
            font_size=30
        ).next_to(eq, RIGHT, buff=0.2).align_to(A_mat, DOWN)
        self.play(Write(A_mat), Write(plus), Write(B_mat), Write(eq), Write(sum_mat))
        self.wait(1.5)
        self.play(FadeOut(p1, A_mat, plus, B_mat, eq, sum_mat))

        # ---------- 分块乘法 ----------
        self.next_section("Properties - Multiplication", skip_animations=False)
        p2 = Text("2. 分块乘法", font_size=24, color=GREEN).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(p2))

        mul_rule = MathTex(
            r"C_{ij} = \sum_{k=1}^{t} A_{ik} B_{kj}",
            font_size=34, color=YELLOW
        ).next_to(p2, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(mul_rule))

        mul_a = MathTex(
            r"A = \begin{bmatrix}",
            r"A_{11} & A_{12} \\",
            r"A_{21} & A_{22}",
            r"\end{bmatrix}",
            font_size=26
        ).next_to(mul_rule, DOWN, buff=0.35, aligned_edge=LEFT)
        mul_b = MathTex(
            r"B = \begin{bmatrix}",
            r"B_{11} & B_{12} \\",
            r"B_{21} & B_{22}",
            r"\end{bmatrix}",
            font_size=26
        ).next_to(mul_a, RIGHT, buff=0.3).align_to(mul_a, DOWN)
        mul_c = MathTex(
            r"AB = \begin{bmatrix}",
            r"A_{11}B_{11}+A_{12}B_{21} & A_{11}B_{12}+A_{12}B_{22} \\[6pt]",
            r"A_{21}B_{11}+A_{22}B_{21} & A_{21}B_{12}+A_{22}B_{22}",
            r"\end{bmatrix}",
            font_size=24
        ).next_to(mul_b, RIGHT, buff=0.3).align_to(mul_a, DOWN)

        self.play(Write(mul_a), Write(mul_b))
        self.wait(0.3)
        self.play(Write(mul_c))
        self.wait(0.5)

        note = Text("前提：A的列分法与B的行分法一致", font_size=21, color=RED)\
            .next_to(mul_c, DOWN, buff=0.2).align_to(mul_c, LEFT)
        self.play(Write(note))
        self.wait(1.5)
        self.play(FadeOut(p2, mul_rule, mul_a, mul_b, mul_c, note))

        # ---------- 分块转置 ----------
        self.next_section("Properties - Transpose", skip_animations=False)
        p3 = Text("3. 分块转置", font_size=24, color=GREEN).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(p3))

        orig = MathTex(
            r"A = \begin{bmatrix}",
            r"A_{11} & A_{12} \\",
            r"A_{21} & A_{22}",
            r"\end{bmatrix}",
            font_size=34
        ).next_to(p3, DOWN, buff=0.35, aligned_edge=LEFT)
        arrow = MathTex(r"\Longrightarrow", font_size=34).next_to(orig, RIGHT, buff=0.3).align_to(orig, DOWN)
        trans = MathTex(
            r"A^{\mathrm{T}} = \begin{bmatrix}",
            r"A_{11}^{\mathrm{T}} & A_{21}^{\mathrm{T}} \\",
            r"A_{12}^{\mathrm{T}} & A_{22}^{\mathrm{T}}",
            r"\end{bmatrix}",
            font_size=34
        ).next_to(arrow, RIGHT, buff=0.3).align_to(orig, DOWN)
        rule = Text("先转置再交换", font_size=22, color=ORANGE).next_to(trans, DOWN, buff=0.25).align_to(trans, LEFT)

        self.play(Write(orig), Write(arrow))
        self.play(Write(trans), Write(rule))
        self.wait(1.5)
        self.play(FadeOut(p3, orig, arrow, trans, rule))

        # ---------- 分块行列式 ----------
        self.next_section("Properties - Determinant", skip_animations=False)
        p4 = Text("4. 分块行列式（上三角型）", font_size=24, color=GREEN).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(p4))

        up_mat = MathTex(
            r"M = \begin{bmatrix}",
            r"A & B \\",
            r"0 & C",
            r"\end{bmatrix}",
            font_size=38
        ).next_to(p4, DOWN, buff=0.35, aligned_edge=LEFT)
        det_f = MathTex(
            r"\det(M) = \det(A) \cdot \det(C)",
            font_size=34, color=YELLOW
        ).next_to(up_mat, RIGHT, buff=0.5).align_to(up_mat, DOWN)
        condition = Text("（其中 A, B, C 为方阵）", font_size=22, color=GRAY)\
            .next_to(det_f, DOWN, buff=0.2).align_to(det_f, LEFT)
        self.play(Write(up_mat))
        self.play(Write(det_f), Write(condition))
        self.wait(1.5)
        self.play(FadeOut(p4, up_mat, det_f, condition))

        # ---------- 四、证明题 ----------
        self.next_section("Proof 1", skip_animations=False)
        sec4 = Text("四、证明题", font_size=32, color=YELLOW).to_edge(UP)
        self.play(Transform(title, sec4))

        q1 = Text("证明1：分块对角阵的秩", font_size=24, color=GREEN).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(q1))

        st1 = MathTex(
            r"\mathrm{rank}\begin{bmatrix} A & 0 \\ 0 & B \end{bmatrix}"
            r"= \mathrm{rank}(A) + \mathrm{rank}(B)",
            font_size=30
        ).next_to(q1, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(Write(st1))
        self.wait(0.3)

        pf1a = Text("设 r(A) = r₁, r(B) = r₂, 则", font_size=23)\
            .next_to(st1, DOWN, buff=0.35, aligned_edge=LEFT)
        pf1b = Text("A中有 r₁ 列线性无关，B中有 r₂ 列线性无关", font_size=23)\
            .next_to(pf1a, DOWN, buff=0.2, aligned_edge=LEFT)
        pf1c = Text("这些列扩充到原矩阵中仍线性无关，故", font_size=23)\
            .next_to(pf1b, DOWN, buff=0.2, aligned_edge=LEFT)
        pf1d = MathTex(
            r"\mathrm{rank}\begin{bmatrix} A & 0 \\ 0 & B \end{bmatrix}"
            r"= r_1 + r_2",
            font_size=26, color=YELLOW
        ).next_to(pf1c, DOWN, buff=0.3, aligned_edge=LEFT)
        self.play(Write(pf1a), Write(pf1b), Write(pf1c), Write(pf1d))
        self.wait(1.5)
        self.play(FadeOut(q1, st1, pf1a, pf1b, pf1c, pf1d))

        # ---------- 证明2 ----------
        self.next_section("Proof 2", skip_animations=False)
        q2 = Text("证明2：上三角分块矩阵的逆", font_size=24, color=GREEN).to_edge(LEFT).shift(UP * 1.5)
        self.play(Write(q2))

        st2 = MathTex(
            r"\begin{bmatrix} A & B \\ 0 & C \end{bmatrix}^{-1}"
            r"= \begin{bmatrix}",
            r"A^{-1} & -A^{-1}BC^{-1} \\",
            r"0 & C^{-1}",
            r"\end{bmatrix}",
            font_size=30
        ).next_to(q2, DOWN, buff=0.35, aligned_edge=LEFT)
        cond2 = Text("(A, C 可逆)", font_size=21, color=GRAY).next_to(st2, RIGHT, buff=0.4).align_to(st2, DOWN)
        self.play(Write(st2), Write(cond2))
        self.wait(0.5)

        pf2a_label = Text("证：设 ", font_size=24).next_to(st2, DOWN, buff=0.4, aligned_edge=LEFT)
        pf2a = MathTex(
            r"\begin{bmatrix} A & B \\ 0 & C \end{bmatrix}"
            r"\begin{bmatrix} X & Y \\ Z & W \end{bmatrix}"
            r"= \begin{bmatrix} I & 0 \\ 0 & I \end{bmatrix}",
            font_size=26
        ).next_to(pf2a_label, RIGHT, buff=0.1).align_to(pf2a_label, DOWN)
        self.play(Write(pf2a_label), Write(pf2a))
        self.wait(0.3)

        eq_group = MathTex(
            r"\left.\begin{aligned}",
            r"AX + BZ &= I & (1) \\",
            r"CZ &= 0 & (2) \\",
            r"AY + BW &= 0 & (3) \\",
            r"CW &= I & (4)",
            r"\end{aligned}\right\}",
            font_size=26
        ).next_to(pf2a, DOWN, buff=0.35, aligned_edge=LEFT).shift(LEFT * 0.1)
        self.play(Write(eq_group))
        self.wait(1)

        solve = MathTex(
            r"(2)\Rightarrow Z = 0,\; (4)\Rightarrow W = C^{-1},\; (1)\Rightarrow X = A^{-1},\; (3)\Rightarrow Y = -A^{-1}BC^{-1}",
            font_size=22, color=YELLOW
        ).next_to(eq_group, DOWN, buff=0.35, aligned_edge=LEFT)
        self.play(Write(solve))
        self.wait(2)

        self.play(FadeOut(q2, st2, cond2, pf2a_label, pf2a, eq_group, solve))

        # ---------- 五、总结 ----------
        self.next_section("Summary", skip_animations=False)
        sec5 = Text("五、总结", font_size=32, color=BLUE).to_edge(UP)
        self.play(Transform(title, sec5))

        bullet_items = [
            "分块矩阵：用横线和纵线将矩阵划分为子块",
            "常见分块：按行、按列、四分块、对角分块",
            "分块运算：加法须同型、乘法须分法一致、转置后交换",
            "分块行列式：上三角型 = 对角块行列式之积",
            "利用分块可简化矩阵运算和证明",
        ]
        bullets = VGroup(*[
            Text(f"• {s}", font_size=22).align_to(title, LEFT).shift(RIGHT * 0.5)
            for s in bullet_items
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(title, DOWN, buff=0.5)
        for item in bullets:
            self.play(Write(item))
            self.wait(0.15)
        self.wait(1.5)
