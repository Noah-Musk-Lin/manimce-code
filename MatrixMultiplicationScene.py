from manim import *

class MatrixMultiplicationScene(Scene):
    def construct(self):
        ab_title = Text("Matrix Multiplication: AB", font_size=36).move_to(UP)
        self.play(Write(ab_title))
        
        # 使用 Matrix 类创建矩阵
        # 矩阵 A
        matrix_A = Matrix([["a", "b", "c"], ["d", "e", "f"]])
        label_A = Tex("A = ").next_to(matrix_A, LEFT)
        matrix_a_group = VGroup(label_A, matrix_A).next_to(ab_title, DOWN*1.2, buff=0.7).shift(LEFT*3.5)
        
        # 矩阵 B
        matrix_B = Matrix([["g", "h"], ["i", "j"], ["k", "l"]])
        label_B = Tex("B = ").next_to(matrix_B, LEFT)
        matrix_b_group = VGroup(label_B, matrix_B).next_to(ab_title, DOWN*0.8, buff=0.7).shift(RIGHT*3.5)
        
        self.play(Write(matrix_a_group))
        self.play(Write(matrix_b_group))
        self.wait(1)
        
        # 创建所有步骤的Tex对象
        step1 = MathTex(
            r"\text{Step 1:} \ \begin{bmatrix} a & b & c \end{bmatrix} \begin{bmatrix} g \\ i \\ k \end{bmatrix} = ag + bi + ck",
            font_size=32
        ).next_to(matrix_a_group, DOWN, buff=1.5).center()

        step2 = MathTex(
            r"\text{Step 2:} \ \begin{bmatrix} a & b & c \end{bmatrix} \begin{bmatrix} h \\ j \\ l \end{bmatrix} = ah + bj + cl",
            font_size=32
        ).next_to(matrix_a_group, DOWN, buff=1.5).center()

        step3 = MathTex(
            r"\text{Step 3:} \ \begin{bmatrix} d & e & f \end{bmatrix} \begin{bmatrix} g \\ i \\ k \end{bmatrix} = dg + ei + fk",
            font_size=32
        ).next_to(matrix_a_group, DOWN, buff=1.5).center()

        step4 = MathTex(
            r"\text{Step 4:} \ \begin{bmatrix} d & e & f \end{bmatrix} \begin{bmatrix} h \\ j \\ l \end{bmatrix} = dh + ej + fl",
            font_size=32
        ).next_to(matrix_a_group, DOWN, buff=1.5).center()
        
        # 使用 Matrix 类可以直接获取行和列
        # 矩阵 A 的行
        row0_A = matrix_A.get_rows()[0]
        row1_A = matrix_A.get_rows()[1]
        
        # 矩阵 B 的列
        col0_B = matrix_B.get_columns()[0]
        col1_B = matrix_B.get_columns()[1]
        
        # 创建高亮矩形
        row1_a = SurroundingRectangle(row0_A, color=YELLOW, buff=0.1)
        col1_b = SurroundingRectangle(col0_B, color=YELLOW, buff=0.1)
        col2_b = SurroundingRectangle(col1_B, color=YELLOW, buff=0.1)
        row2_a = SurroundingRectangle(row1_A, color=YELLOW, buff=0.1)

        # 使用 Succession 按顺序播放动画
        # 步骤1: 第一行 x 第一列
        self.play(Create(row1_a), Create(col1_b), Write(step1))
        self.wait(2)

        # 步骤2: 第一行 x 第二列
        self.play(
            FadeOut(col1_b),                # 只淡出列1
            Transform(step1, step2),        # 转换步骤文本
            Create(col2_b)                  # 创建列2高亮
        )
        self.wait(2)

        # 步骤3: 第二行 x 第一列
        self.play(
            FadeOut(row1_a), FadeOut(col2_b),  # 淡出第一行和列2
            Transform(step1, step3),           # 转换步骤文本
            Create(row2_a), Create(col1_b)     # 创建第二行和列1高亮
        )
        self.wait(2)

        # 步骤4: 第二行 x 第二列
        self.play(
            FadeOut(col1_b),                  # 只淡出列1
            Transform(step1, step4),           # 转换步骤文本
            Create(col2_b)                     # 创建列2高亮
        )
        self.wait(2)

        # 清理场景
        self.play(FadeOut(row2_a), FadeOut(col2_b), FadeOut(step1))