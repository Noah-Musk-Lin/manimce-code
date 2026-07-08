from manim import *

class CauchyBinetFormula(Scene):
    def construct(self):
        # Define title
        title = Title("Cauchy-Binet Formula", color=BLUE)
        self.play(Write(title))
        self.wait(1)
        
        # Definition section
        definition_text = Text("Definition:", font_size=36).set_color_by_gradient(RED, MAROON, PINK).next_to(title, DOWN*0.5, buff=1).align_to(title, LEFT)
        self.play(Write(definition_text))
        self.wait(0.5)
        
        # Formula
        formula = MathTex(
            r"\text{If} \ A \in \mathbb{R}^{m \times n}, \ B \in \mathbb{R}^{n \times m} \ (m \leq n), \ \text{then}",
            font_size=32
        ).next_to(definition_text, DOWN, buff=0.9).align_to(definition_text, LEFT)
        self.play(Write(formula))
        self.wait(0.5)
        
        formula_main = MathTex(
            r"\det(AB) = \sum_{S \in \binom{[n]}{m}} \det(A_S) \det(B_S)",
            font_size=40,
            color=YELLOW
        ).next_to(formula, DOWN, buff=0.7)
        self.play(Write(formula_main))
        self.wait(1)
        
        # Explanation (split into three separate lines)
        explanation1 = Text(
            "1. S is the set of all possible subsets of size m from {1,2,...,n}",
            font_size=28,
            t2c={"subsets": GREEN}
        ).next_to(formula_main, DOWN*0.5, buff=0.7).align_to(formula_main, LEFT)
        
        explanation2 = Text(
            "2. A_S is the submatrix of A formed by columns indexed by S",
            font_size=28,
            t2c={"submatrix": GREEN}
        ).next_to(explanation1, DOWN, buff=0.5).align_to(formula_main, LEFT)
        
        explanation3 = Text(
            "3. B_S is the submatrix of B formed by rows indexed by S",
            font_size=28,
            t2c={"submatrix": GREEN}
        ).next_to(explanation2, DOWN, buff=0.5).align_to(formula_main, LEFT)
        
        self.play(Write(explanation1))
        self.wait(0.5)
        self.play(Write(explanation2))
        self.wait(0.5)
        self.play(Write(explanation3))
        self.wait(2)
        
        # Clear definition part, keep title
        self.play(
            FadeOut(definition_text),
            FadeOut(formula),
            FadeOut(formula_main),
            FadeOut(explanation1),
            FadeOut(explanation2),
            FadeOut(explanation3)
        )
        self.wait(0.5)
        
        # Application part - shifted to the right
        application_text = Text("Application Example:", font_size=36).set_color_by_gradient(RED, MAROON, PINK).next_to(title, DOWN*0.5, buff=1)
        self.play(Write(application_text))
        self.wait(0.5)
        
        # 2x2 Matrix example - Page 1: Matrices and Multiplication
        matrix_text = Text("Let m=2, n=3, consider matrices:", font_size=32).set_color_by_gradient(RED, MAROON, PINK).next_to(application_text, DOWN*0.5, buff=0.5)
        self.play(Write(matrix_text))
        self.wait(0.5)
        
        # Matrix A
        matrix_a = MathTex(
            r"A = \begin{bmatrix} a & b & c \\ d & e & f \end{bmatrix}",
            font_size=36
        ).next_to(matrix_text, DOWN, buff=0.7).shift(LEFT*2.5)
        self.play(Write(matrix_a))
        self.wait(0.5)
        
        # Matrix B
        matrix_b = MathTex(
            r"B = \begin{bmatrix} g & h \\ i & j \\ k & l \end{bmatrix}",
            font_size=36
        ).next_to(matrix_text, DOWN*0.6, buff=0.7).shift(RIGHT*2.5)
        self.play(Write(matrix_b))
        self.wait(1)
        
        # Calculate AB - Page 2: Matrix Multiplication Setup
        self.play(
            FadeOut(matrix_text),
            FadeOut(matrix_a),
            FadeOut(matrix_b)
        )
        
        ab_title = Text("Matrix Multiplication: AB", font_size=36).set_color_by_gradient(RED, MAROON, PINK).next_to(application_text, DOWN, buff=0.5)
        self.play(Write(ab_title))
        self.wait(0.5)
        
        # 使用 Matrix 类创建矩阵
        # 矩阵 A
        matrix_A = Matrix([["a", "b", "c"], ["d", "e", "f"]])
        label_A = Tex("A = ").next_to(matrix_A, LEFT)
        matrix_a_group = VGroup(label_A, matrix_A).next_to(ab_title, DOWN*1.9, buff=0.9).shift(LEFT*4.3)
        
        # 矩阵 B
        matrix_B = Matrix([["g", "h"], ["i", "j"], ["k", "l"]])
        label_B = Tex("B = ").next_to(matrix_B, LEFT)
        matrix_b_group = VGroup(label_B, matrix_B).next_to(ab_title, DOWN*1.3, buff=0.9).shift(RIGHT*4.3)
        
        self.play(Write(matrix_a_group))
        self.play(Write(matrix_b_group))
        self.wait(1)

        # 创建所有步骤的Tex对象
        step1 = MathTex(
            r"\text{Step 1:} \ \begin{bmatrix} a & b & c \end{bmatrix} \begin{bmatrix} g \\ i \\ k \end{bmatrix} = ag + bi + ck",
            font_size=32
        ).set_color_by_gradient(BLUE, PURPLE).next_to(matrix_a_group, DOWN, buff=1.5).center()

        step2 = MathTex(
            r"\text{Step 2:} \ \begin{bmatrix} a & b & c \end{bmatrix} \begin{bmatrix} h \\ j \\ l \end{bmatrix} = ah + bj + cl",
            font_size=32
        ).set_color_by_gradient(BLUE, PURPLE).next_to(matrix_a_group, DOWN, buff=1.5).center()

        step3 = MathTex(
            r"\text{Step 3:} \ \begin{bmatrix} d & e & f \end{bmatrix} \begin{bmatrix} g \\ i \\ k \end{bmatrix} = dg + ei + fk",
            font_size=32
        ).set_color_by_gradient(BLUE, PURPLE).next_to(matrix_a_group, DOWN, buff=1.5).center()

        step4 = MathTex(
            r"\text{Step 4:} \ \begin{bmatrix} d & e & f \end{bmatrix} \begin{bmatrix} h \\ j \\ l \end{bmatrix} = dh + ej + fl",
            font_size=32
        ).set_color_by_gradient(BLUE, PURPLE).next_to(matrix_a_group, DOWN, buff=1.5).center()
        
        # 使用 Matrix 类可以直接获取行和列
        # 矩阵 A 的行
        row0_A = matrix_A.get_rows()[0]
        row1_A = matrix_A.get_rows()[1]
        
        # 矩阵 B 的列
        col0_B = matrix_B.get_columns()[0]
        col1_B = matrix_B.get_columns()[1]
        
        # 创建高亮矩形
        row1_a = SurroundingRectangle(row0_A, color=YELLOW, buff=0.1)
        col1_b = SurroundingRectangle(col0_B, color=BLUE, buff=0.1)
        col2_b = SurroundingRectangle(col1_B, color=BLUE, buff=0.1)
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
        
        
        # Page 7: Result matrix
        
        ab_result = MathTex(
            r"AB = \begin{bmatrix} ag+bi+ck & ah+bj+cl \\ dg+ei+fk & dh+ej+fl \end{bmatrix}",
            font_size=36
        ).set_color_by_gradient(RED, MAROON, PINK).next_to(ab_title, DOWN*2.5, buff=1.5)
        
        self.play(Write(ab_result))
        self.wait(2)
        
        # Clear multiplication steps - Page 8: Determinant Calculation
        self.play(
            FadeOut(ab_title),
            FadeOut(matrix_a_group),
            FadeOut(matrix_b_group),
            FadeOut(ab_result)
        )
        
        # Determinant calculation
        det_title = Text("Determinant Calculation", font_size=36).set_color_by_gradient(RED, MAROON, PINK).next_to(application_text, DOWN, buff=0.5)
        self.play(Write(det_title))
        self.wait(0.5)
        
        ab_matrix = MathTex(
            r"AB = \begin{bmatrix} ag+bi+ck & ah+bj+cl \\ dg+ei+fk & dh+ej+fl \end{bmatrix}",
            font_size= 40
        ).set_color_by_gradient(RED, MAROON, PINK).next_to(det_title, DOWN*0.8, buff=0.7)
        self.play(Write(ab_matrix))
        self.wait(0.5)
        
        det_text = Text("Determinant of AB:", font_size=32).set_color_by_gradient(RED, MAROON, PINK).next_to(ab_matrix, DOWN, buff=1).align_to(application_text, LEFT)
        self.play(Write(det_text))
        self.wait(0.5)
        
        # Step-by-step determinant calculation
        det_step1 = MathTex(
            r"\det(AB) = (ag+bi+ck)(ej+fl) - (ah+bj+cl)(ei+fk)",
            font_size=36
        ).set_color_by_gradient(RED, MAROON, PINK).next_to(det_text, DOWN*0.5, buff=0.7)
        
        self.play(Write(det_step1))
        self.wait(2)
        
        # Using Cauchy-Binet formula - Page 9: Formula Application
        self.play(
            FadeOut(det_title),
            FadeOut(ab_matrix),
            FadeOut(det_text),
            FadeOut(det_step1)
        )
        
        formula_text = Text("Using Cauchy-Binet Formula:", font_size=32).set_color_by_gradient(RED, MAROON, PINK).next_to(application_text, DOWN, buff=0.5).shift(RIGHT*0.5)
        self.play(Write(formula_text))
        self.wait(0.5)
        
        subsets = MathTex(
            r"S \in \binom{\{1,2,3\}}{2} = \{\{1,2\}, \{1,3\}, \{2,3\}\}",
            font_size=32
        ).set_color_by_gradient(RED, MAROON, PINK).next_to(formula_text, DOWN*0.5, buff=0.7)
        self.play(Write(subsets))
        self.wait(1)
        
        # Expanded formula with highlighting
        expanded_formula = MathTex(
            r"\det(AB) = \underbrace{\det\begin{bmatrix}a&b\\d&e\end{bmatrix}\det\begin{bmatrix}g&h\\i&j\end{bmatrix}}_{S=\{1,2\}} +",
            r"\underbrace{\det\begin{bmatrix}a&c\\d&f\end{bmatrix}\det\begin{bmatrix}g&h\\k&l\end{bmatrix}}_{S=\{1,3\}} +",
            r"\underbrace{\det\begin{bmatrix}b&c\\e&f\end{bmatrix}\det\begin{bmatrix}i&j\\k&l\end{bmatrix}}_{S=\{2,3\}}",
            font_size=30
        ).set_color_by_gradient(YELLOW,LIGHT_BROWN).next_to(subsets, DOWN*0.5, buff=0.7)
        
        self.play(Write(expanded_formula[0]))
        self.wait(1)
        self.play(Write(expanded_formula[1]))
        self.wait(1)
        self.play(Write(expanded_formula[2]))
        self.wait(2)
        
        # Final conclusion
        conclusion = Text("Both methods yield the same result, verifying the Cauchy-Binet formula!", font_size=32, color=GREEN).next_to(expanded_formula, DOWN*0.4, buff=1).shift(LEFT*0.5)
        self.play(Write(conclusion))
        self.wait(2)
        
        # End scene
        self.play(FadeOut(title), *[FadeOut(mob) for mob in self.mobjects if mob != title])
        self.wait()    