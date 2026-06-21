# -*- coding: utf-8 -*-
from manim import *

"""
拉普拉斯行列式展开 (Laplace Expansion of Determinants)
基于高等代数学第四版（谢启鸿绿皮书）内容
使用 manimce (0.20.1) 制作
"""


class LaplaceExpansion(Scene):
    def construct(self):
        self.next_section("Title", skip_animations=False)
        self.show_title()
        self.next_section("MinorsAndCofactors", skip_animations=False)
        self.show_minors_and_cofactors()
        self.next_section("RowExpansion", skip_animations=False)
        self.show_row_expansion_theorem()
        self.next_section("ColumnExpansion", skip_animations=False)
        self.show_column_expansion()
        self.next_section("KeyProperties", skip_animations=False)
        self.show_key_properties()
        self.next_section("LaplaceTheorem", skip_animations=False)
        self.show_laplace_theorem()
        self.next_section("ComputationExample", skip_animations=False)
        self.show_computation_example()
        self.next_section("Summary", skip_animations=False)
        self.show_summary()

    # ============================================================
    # Section 1: 标题
    # ============================================================
    def show_title(self):
        title = Text("拉普拉斯行列式展开", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.6)
        subtitle = Text("—— 高等代数学（第四版）", font_size=28, color=GRAY)
        subtitle.next_to(title, DOWN, buff=0.3)
        author = Text("Laplace Expansion of Determinants", font_size=24, color=GRAY)
        author.next_to(subtitle, DOWN, buff=0.2)

        self.play(Write(title))
        self.play(Write(subtitle), Write(author))
        self.wait(1.5)
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(author))

    # ============================================================
    # Section 2: 余子式与代数余子式
    # ============================================================
    def show_minors_and_cofactors(self):
        sec_title = Text("一、余子式与代数余子式", font_size=36, color=BLUE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title))

        # 使用 Matrix 类精确控制每个元素
        det3 = Matrix(
            [["a_{11}", "a_{12}", "a_{13}"],
             ["a_{21}", "a_{22}", "a_{23}"],
             ["a_{31}", "a_{32}", "a_{33}"]],
            h_buff=1.35, v_buff=0.95,
            element_alignment_corner=ORIGIN,
        )
        det3.move_to(UP * 0.8)
        self.play(Write(det3))
        self.wait(0.5)

        # 精确定位 a_{23}：get_entries() 按先行后列排列，[5] 是第2行第3列
        entries = det3.get_entries()
        a23_el = entries[5]  # 0-indexed: row1*3+col2 = 5
        a21_el = entries[3]
        a13_el = entries[2]
        a33_el = entries[8]

        highlight = SurroundingRectangle(
            a23_el, color=YELLOW, buff=0.15, stroke_width=3
        )
        self.play(Create(highlight))
        self.wait(0.8)

        # 精确划线：第2行和第3列
        h_line = Line(
            a21_el.get_left() + LEFT * 0.2,
            a23_el.get_right() + RIGHT * 0.2,
            color=RED, stroke_width=3,
        )
        v_line = Line(
            a13_el.get_top() + UP * 0.2,
            a33_el.get_bottom() + DOWN * 0.2,
            color=RED, stroke_width=3,
        )
        self.play(Create(h_line), Create(v_line))
        self.wait(0.8)

        # 显示余子式
        minor_label = Text("余子式", font_size=28, color=GREEN)
        minor_label.next_to(det3, DOWN, buff=0.8).shift(LEFT * 2.5)
        minor_eq = MathTex(
            r"M_{23} = \begin{vmatrix}",
            r"a_{11} & a_{12} \\",
            r"a_{31} & a_{32}",
            r"\end{vmatrix}",
            font_size=36,
        )
        minor_eq.next_to(minor_label, RIGHT, buff=0.15).align_to(minor_label, DOWN)

        self.play(Write(minor_label), Write(minor_eq))
        self.wait(0.5)

        # 显示代数余子式
        cof_label = Text("代数余子式", font_size=28, color=ORANGE)
        cof_label.next_to(minor_label, DOWN, buff=0.6).align_to(minor_label, LEFT)
        cof_eq = MathTex(
            r"A_{23} = (-1)^{2+3} M_{23} = -M_{23}",
            font_size=36,
        )
        cof_eq.next_to(cof_label, RIGHT, buff=0.15).align_to(cof_label, DOWN)

        self.play(Write(cof_label), Write(cof_eq))
        self.wait(1.5)

        # 一般定义
        general_def = MathTex(
            r"A_{ij} = (-1)^{i+j} \, M_{ij}",
            font_size=38, color=YELLOW,
        )
        general_def.next_to(cof_eq, DOWN, buff=0.5)
        box = SurroundingRectangle(general_def, color=YELLOW, buff=0.25, stroke_width=2)
        self.play(Write(general_def), Create(box))
        self.wait(1.5)

        self.play(
            FadeOut(sec_title), FadeOut(det3), FadeOut(highlight),
            FadeOut(h_line), FadeOut(v_line),
            FadeOut(minor_label), FadeOut(minor_eq),
            FadeOut(cof_label), FadeOut(cof_eq),
            FadeOut(general_def), FadeOut(box),
        )

    # ============================================================
    # Section 3: 按一行展开定理
    # ============================================================
    def show_row_expansion_theorem(self):
        sec_title = Text("二、按一行（列）展开定理", font_size=36, color=BLUE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title))

        # 定理陈述
        theorem = MathTex(
            r"|A| = \sum_{j=1}^{n} a_{ij} A_{ij}",
            r"\qquad (i = 1, 2, \ldots, n)",
            font_size=38,
            color=YELLOW,
        )
        theorem.next_to(sec_title, DOWN, buff=0.6)
        self.play(Write(theorem))
        self.wait(0.5)

        row_label = Text("按第 i 行展开", font_size=26, color=GRAY)
        row_label.next_to(theorem, DOWN, buff=0.2)
        self.play(Write(row_label))
        self.wait(1.5)

        self.play(FadeOut(row_label))

        # 以 3x3 行列式为例
        example_label = Text("以 3 阶行列式按第一行展开为例：", font_size=28)
        example_label.next_to(theorem, DOWN, buff=0.6).align_to(theorem, LEFT)
        self.play(Write(example_label))
        self.wait(0.3)

        det3 = MathTex(
            r"\begin{vmatrix}",
            r"a_{11} & a_{12} & a_{13} \\",
            r"a_{21} & a_{22} & a_{23} \\",
            r"a_{31} & a_{32} & a_{33}",
            r"\end{vmatrix}",
            font_size=38,
        )
        det3.next_to(example_label, DOWN, buff=0.4).shift(LEFT * 2.5)
        self.play(Write(det3))

        eq_sign = MathTex(r"=", font_size=42)
        eq_sign.next_to(det3, RIGHT, buff=0.3).align_to(det3, DOWN)
        self.play(Write(eq_sign))

        # 展开式（分项逐步展示）
        expansion = MathTex(
            r"a_{11}A_{11} + a_{12}A_{12} + a_{13}A_{13}",
            font_size=36,
        )
        expansion.next_to(eq_sign, RIGHT, buff=0.25).align_to(eq_sign, DOWN)
        self.play(Write(expansion))
        self.wait(1)

        # 展开每项为二阶
        detail1 = MathTex(
            r"= a_{11} \cdot (-1)^{1+1}",
            r"\begin{vmatrix} a_{22} & a_{23} \\ a_{32} & a_{33} \end{vmatrix}",
            font_size=30,
        )
        detail1.next_to(det3, DOWN, buff=0.45).align_to(det3, LEFT)
        detail2 = MathTex(
            r"+ a_{12} \cdot (-1)^{1+2}",
            r"\begin{vmatrix} a_{21} & a_{23} \\ a_{31} & a_{33} \end{vmatrix}",
            font_size=30,
        )
        detail2.next_to(detail1, DOWN, buff=0.2).align_to(detail1, LEFT)
        detail3 = MathTex(
            r"+ a_{13} \cdot (-1)^{1+3}",
            r"\begin{vmatrix} a_{21} & a_{22} \\ a_{31} & a_{32} \end{vmatrix}",
            font_size=30,
        )
        detail3.next_to(detail2, DOWN, buff=0.2).align_to(detail1, LEFT)

        self.play(Write(detail1))
        self.wait(0.3)
        self.play(Write(detail2))
        self.wait(0.3)
        self.play(Write(detail3))
        self.wait(1.2)

        # 符号规律说明（横向排列以节省纵向空间）
        sign_note = Text("符号规律：(-1)^{i+j}，棋盘格正负交替", font_size=22, color=ORANGE)
        sign_pattern = MathTex(
            r"\begin{vmatrix} + & - & + \\ - & + & - \\ + & - & + \end{vmatrix}",
            font_size=26,
            color=ORANGE,
        )
        sign_group = VGroup(sign_note, sign_pattern).arrange(RIGHT, buff=0.3)
        sign_group.next_to(detail3, DOWN, buff=0.35)
        self.play(Write(sign_group))
        self.wait(2)

        self.play(
            FadeOut(sec_title), FadeOut(theorem), FadeOut(example_label),
            FadeOut(det3), FadeOut(eq_sign), FadeOut(expansion),
            FadeOut(detail1), FadeOut(detail2), FadeOut(detail3),
            FadeOut(sign_group),
        )

    # ============================================================
    # Section 4: 按一列展开
    # ============================================================
    def show_column_expansion(self):
        sec_title = Text("三、按一列展开", font_size=36, color=BLUE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title))

        col_theorem = MathTex(
            r"|A| = \sum_{i=1}^{n} a_{ij} A_{ij}",
            r"\qquad (j = 1, 2, \ldots, n)",
            font_size=38,
            color=YELLOW,
        )
        col_theorem.next_to(sec_title, DOWN, buff=0.6)
        self.play(Write(col_theorem))

        col_label = Text("按第 j 列展开", font_size=26, color=GRAY)
        col_label.next_to(col_theorem, DOWN, buff=0.2)
        self.play(Write(col_label))
        self.wait(1.5)

        self.play(FadeOut(col_label))

        # 简例
        note = Text("原理与按行展开完全类似，仅展开方向不同", font_size=26)
        note.next_to(col_theorem, DOWN, buff=0.7)
        self.play(Write(note))
        self.wait(0.5)

        det3 = MathTex(
            r"\begin{vmatrix}",
            r"a_{11} & a_{12} & a_{13} \\",
            r"a_{21} & a_{22} & a_{23} \\",
            r"a_{31} & a_{32} & a_{33}",
            r"\end{vmatrix}",
            font_size=38,
        )
        det3.next_to(note, DOWN, buff=0.6).shift(LEFT * 2.5)
        eq_sign = MathTex(r"=", font_size=42)
        eq_sign.next_to(det3, RIGHT, buff=0.3).align_to(det3, DOWN)
        col_exp = MathTex(
            r"a_{12}A_{12} + a_{22}A_{22} + a_{32}A_{32}",
            font_size=34,
        )
        col_exp.next_to(eq_sign, RIGHT, buff=0.25).align_to(eq_sign, DOWN)

        self.play(Write(det3), Write(eq_sign), Write(col_exp))
        self.wait(1.5)

        # 标注"按第二列展开"
        col_note = Text("← 按第 2 列展开", font_size=24, color=GREEN)
        col_note.next_to(det3, DOWN, buff=0.7)
        self.play(Write(col_note))
        self.wait(1.5)

        self.play(
            FadeOut(sec_title), FadeOut(col_theorem), FadeOut(note),
            FadeOut(det3), FadeOut(eq_sign), FadeOut(col_exp),
            FadeOut(col_note),
        )

    # ============================================================
    # Section 5: 重要性质
    # ============================================================
    def show_key_properties(self):
        sec_title = Text("四、重要推论与性质", font_size=36, color=BLUE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title))

        # 性质1: 异行异列展开为0
        prop1_title = Text("性质 1（异行异列展开为零）", font_size=28, color=GREEN)
        prop1_title.next_to(sec_title, DOWN, buff=0.6).align_to(sec_title, LEFT).shift(RIGHT * 0.3)
        self.play(Write(prop1_title))

        prop1_formula = MathTex(
            r"\sum_{k=1}^{n} a_{ik} A_{jk} = 0 \qquad (i \neq j)",
            font_size=36,
            color=YELLOW,
        )
        prop1_formula.next_to(prop1_title, DOWN, buff=0.3).align_to(prop1_title, LEFT)
        self.play(Write(prop1_formula))

        prop1_explain = Text(
            "直观理解：用第 j 行的代数余子式去乘第 i 行的元素再求和，",
            font_size=22, color=GRAY,
        )
        prop1_explain2 = Text(
            "相当于求一个有两行相同的行列式的展开，故结果为零。",
            font_size=22, color=GRAY,
        )
        prop1_explain.next_to(prop1_formula, DOWN, buff=0.3).align_to(prop1_formula, LEFT)
        prop1_explain2.next_to(prop1_explain, DOWN, buff=0.15).align_to(prop1_explain, LEFT)
        self.play(Write(prop1_explain), Write(prop1_explain2))
        self.wait(2)

        self.play(
            FadeOut(prop1_title), FadeOut(prop1_formula),
            FadeOut(prop1_explain), FadeOut(prop1_explain2),
        )

        # 性质2: 伴随矩阵
        prop2_title = Text("性质 2（伴随矩阵）", font_size=28, color=GREEN)
        prop2_title.next_to(sec_title, DOWN, buff=0.6).align_to(sec_title, LEFT).shift(RIGHT * 0.3)
        self.play(Write(prop2_title))

        adj_def = MathTex(
            r"A^* = \begin{bmatrix}",
            r"A_{11} & A_{21} & \cdots & A_{n1} \\",
            r"A_{12} & A_{22} & \cdots & A_{n2} \\",
            r"\vdots & \vdots & \ddots & \vdots \\",
            r"A_{1n} & A_{2n} & \cdots & A_{nn}",
            r"\end{bmatrix}",
            font_size=32,
        )
        adj_def.next_to(prop2_title, DOWN, buff=0.4).shift(LEFT * 2)
        self.play(Write(adj_def))

        adj_label = Text("伴随矩阵\n（注意转置！）", font_size=22, color=ORANGE)
        adj_label.next_to(adj_def, RIGHT, buff=0.6)

        adj_prop = MathTex(
            r"A \cdot A^* = A^* \cdot A = |A| \cdot I_n",
            font_size=32,
            color=YELLOW,
        )
        adj_prop.next_to(prop2_title, DOWN, buff=0.4).shift(RIGHT * 2.5)

        self.play(Write(adj_label), Write(adj_prop))
        self.wait(2.5)

        self.play(
            FadeOut(sec_title), FadeOut(prop2_title),
            FadeOut(adj_def), FadeOut(adj_label), FadeOut(adj_prop),
        )

    # ============================================================
    # Section 6: 拉普拉斯定理（一般形式）
    # ============================================================
    def show_laplace_theorem(self):
        sec_title = Text("五、拉普拉斯定理（一般形式）", font_size=36, color=BLUE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title))

        # 定理陈述
        thm_text1 = Text("在 n 阶行列式中，任意选定 k 行", font_size=28)
        thm_text2 = Text("则这 k 行中一切 k 阶子式与其代数余子式的乘积之和等于原行列式。", font_size=28)
        thm_group = VGroup(thm_text1, thm_text2).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        thm_group.next_to(sec_title, DOWN, buff=0.6).align_to(sec_title, LEFT)
        self.play(Write(thm_group))
        self.wait(1.5)

        # 一般公式
        laplace_formula = MathTex(
            r"|A| = \sum_{1 \le j_1 < \cdots < j_k \le n}",
            r"A\begin{pmatrix} i_1 & \cdots & i_k \\",
            r"j_1 & \cdots & j_k \end{pmatrix}",
            r"\cdot \widehat{A}\begin{pmatrix} i_1 & \cdots & i_k \\",
            r"j_1 & \cdots & j_k \end{pmatrix}",
            font_size=28,
        )
        laplace_formula.next_to(thm_group, DOWN, buff=0.4)
        self.play(Write(laplace_formula))
        self.wait(1.5)
        self.play(FadeOut(thm_group), FadeOut(laplace_formula))

        # 4x4 例子：按前两行展开
        ex_label = Text("例：4 阶行列式按前两行展开（共 C_4^2 = 6 项）", font_size=28)
        ex_label.next_to(sec_title, DOWN, buff=0.7)
        self.play(Write(ex_label))
        self.wait(0.3)

        det4 = MathTex(
            r"\begin{vmatrix}",
            r"a_{11} & a_{12} & a_{13} & a_{14} \\",
            r"a_{21} & a_{22} & a_{23} & a_{24} \\",
            r"a_{31} & a_{32} & a_{33} & a_{34} \\",
            r"a_{41} & a_{42} & a_{43} & a_{44}",
            r"\end{vmatrix}",
            font_size=36,
        )
        det4.next_to(ex_label, DOWN, buff=0.4).shift(LEFT * 2.8)
        self.play(Write(det4))

        # 展示前两行
        row_rect = SurroundingRectangle(
            VGroup(
                MathTex(r"a_{11}\;a_{12}\;a_{13}\;a_{14}", font_size=1).move_to(det4.get_center() + UP * 0.55),
                MathTex(r"a_{21}\;a_{22}\;a_{23}\;a_{24}", font_size=1).move_to(det4.get_center() + UP * 0.0),
            ),
            color=YELLOW, buff=0.15, stroke_width=3,
        )
        # 实际上需要正确位置——用线标注
        top_y = det4.get_center()[1] + 0.60
        bot_y = det4.get_center()[1] + 0.05
        row_indicator = Line(
            det4.get_left() + LEFT * 0.3 + UP * (top_y - det4.get_center()[1]),
            det4.get_right() + RIGHT * 0.3 + UP * (top_y - det4.get_center()[1]),
            color=YELLOW, stroke_width=4,
        )
        row_indicator2 = Line(
            det4.get_left() + LEFT * 0.3 + UP * (bot_y - det4.get_center()[1]),
            det4.get_right() + RIGHT * 0.3 + UP * (bot_y - det4.get_center()[1]),
            color=YELLOW, stroke_width=4,
        )
        self.play(Create(row_indicator), Create(row_indicator2))
        self.wait(0.5)

        # 选列 {1,2} 的第一个子式
        term1 = MathTex(
            r"\begin{vmatrix} a_{11} & a_{12} \\ a_{21} & a_{22} \end{vmatrix}",
            r"\cdot \begin{vmatrix} a_{33} & a_{34} \\ a_{43} & a_{44} \end{vmatrix}",
            font_size=28,
        )
        term1.next_to(det4, RIGHT, buff=0.5).align_to(det4, UP).shift(UP * 0.3)
        term1_label = MathTex(r"(j_1,j_2)=(1,2)", font_size=22, color=GRAY)
        term1_label.next_to(term1, DOWN, buff=0.15)

        self.play(Write(term1), Write(term1_label))
        self.wait(0.5)

        # 省略号 + 其余5项
        dots = Text("⋮  共 6 项求代数和", font_size=26, color=GRAY)
        dots.next_to(term1_label, DOWN, buff=0.4)
        self.play(Write(dots))
        self.wait(0.5)

        # 符号说明
        sign_text = Text("代数余子式：", font_size=24, color=ORANGE)
        sign_formula = MathTex(
            r"\widehat{A} = (-1)^{i_1+\cdots+i_k+j_1+\cdots+j_k}"
            r"\times \text{(complementary minor)}",
            font_size=24,
            color=ORANGE,
        )
        sign_group = VGroup(sign_text, sign_formula).arrange(RIGHT, buff=0.15)
        sign_group.next_to(dots, DOWN, buff=0.4)
        self.play(Write(sign_group))
        self.wait(2)

        self.play(
            FadeOut(sec_title), FadeOut(ex_label), FadeOut(det4),
            FadeOut(row_indicator), FadeOut(row_indicator2),
            FadeOut(term1), FadeOut(term1_label), FadeOut(dots),
            FadeOut(sign_group),
        )

    # ============================================================
    # Section 7: 例题计算
    # ============================================================
    def show_computation_example(self):
        sec_title = Text("六、例题演示", font_size=36, color=BLUE)
        sec_title.to_edge(UP, buff=0.5)
        self.play(Write(sec_title))

        # 例题 — 左侧行列式
        ex_text = Text("计算行列式：", font_size=28)
        ex_text.next_to(sec_title, DOWN, buff=0.5).align_to(sec_title, LEFT)

        det_ex = MathTex(
            r"D = \begin{vmatrix}",
            r"3 & 1 & -1 & 2 \\",
            r"-5 & 1 & 3 & -4 \\",
            r"2 & 0 & 1 & -1 \\",
            r"1 & -5 & 3 & -3",
            r"\end{vmatrix}",
            font_size=34,
        )
        det_ex.next_to(ex_text, DOWN, buff=0.35).shift(LEFT * 2.5)
        self.play(Write(ex_text), Write(det_ex))
        self.wait(1.5)

        # 策略说明 — 右侧
        strategy = Text(
            "策略：选含 0 较多的\n行或列展开以减量",
            font_size=24, color=GREEN,
        )
        strategy.next_to(det_ex, RIGHT, buff=0.8).align_to(det_ex, UP)
        self.play(Write(strategy))
        self.wait(1)

        # 按第3行展开
        step_formula = MathTex(
            r"D = 2A_{31} + 0A_{32} + 1A_{33} - 1A_{34}",
            font_size=32, color=YELLOW,
        )
        step_formula.next_to(strategy, DOWN, buff=0.5)
        row_note = Text("按第3行展开", font_size=22, color=GRAY)
        row_note.next_to(step_formula, UP, buff=0.1).align_to(step_formula, LEFT)

        self.play(Write(row_note), Write(step_formula))
        self.wait(1.5)

        # 展示余子式 A_{31}（只展示一个示例）
        calc_label = Text("例如：", font_size=24, color=GRAY)
        calc_label.next_to(det_ex, DOWN, buff=0.4).align_to(det_ex, LEFT)

        a31 = MathTex(
            r"A_{31} = (-1)^{3+1}",
            r"\begin{vmatrix}",
            r"1 & -1 & 2 \\ 1 & 3 & -4 \\ -5 & 3 & -3",
            r"\end{vmatrix}",
            font_size=28,
        )
        a31.next_to(calc_label, RIGHT, buff=0.15).align_to(calc_label, DOWN)
        self.play(Write(calc_label), Write(a31))
        self.wait(0.8)

        # 简短的后续说明
        final_note = Text(
            "类似得 A_{33}, A_{34}，各 3 阶行列式继续展开降阶至 2 阶求值",
            font_size=22, color=GRAY,
        )
        final_note.next_to(a31, DOWN, buff=0.4).align_to(a31, LEFT)
        self.play(Write(final_note))
        self.wait(2)

        self.play(
            FadeOut(sec_title), FadeOut(ex_text), FadeOut(det_ex),
            FadeOut(strategy), FadeOut(row_note), FadeOut(step_formula),
            FadeOut(calc_label), FadeOut(a31), FadeOut(final_note),
        )

    # ============================================================
    # Section 8: 总结
    # ============================================================
    def show_summary(self):
        title = Text("总  结", font_size=40, color=BLUE)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title))

        items = [
            "余子式 M_{ij}：划去第 i 行第 j 列后的 n-1 阶行列式",
            "代数余子式 A_{ij} = (-1)^{i+j} M_{ij}",
            "按行展开：|A| = Sum_j a_{ij} A_{ij}",
            "按列展开：|A| = Sum_i a_{ij} A_{ij}",
            "异行异列展开为零：Sum a_{ik} A_{jk} = 0 (i != j)",
            "拉普拉斯定理：按 k 行展开的一般形式",
            "核心思想：降阶——高阶化低阶",
        ]
        bullet_group = VGroup()
        for item_text in items:
            dot = Text("•", font_size=22, color=YELLOW)
            content = Text(item_text, font_size=22)
            row = VGroup(dot, content).arrange(RIGHT, buff=0.15)
            bullet_group.add(row)
        bullet_group.arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        bullet_group.next_to(title, DOWN, buff=0.5).align_to(title, LEFT).shift(RIGHT * 0.1)

        for bullet in bullet_group:
            self.play(Write(bullet))
            self.wait(0.2)

        # 核心公式框
        core_formula = MathTex(
            r"|A| = \sum_{j=1}^{n} a_{ij} A_{ij}",
            font_size=34,
            color=YELLOW,
        )
        core_label = Text("(按第 i 行展开)", font_size=24, color=GRAY)
        core_group = VGroup(core_formula, core_label).arrange(RIGHT, buff=0.2)
        core_group.next_to(bullet_group, DOWN, buff=0.5)
        box = SurroundingRectangle(core_group, color=YELLOW, buff=0.3, stroke_width=2)
        self.play(Write(core_group), Create(box))
        self.wait(2)

        # 最终黑屏
        self.play(FadeOut(title), FadeOut(bullet_group),
                  FadeOut(core_group), FadeOut(box))
        self.wait(0.5)
