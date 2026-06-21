from manim import *

class CauchyRiemannEquations(Scene):
    def construct(self):
        # 标题
        title = Title("Cauchy-Riemann Equations", font_size=48).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(title))
        self.wait(2)
        
        # 引入复数函数
        complex_func_text = Tex(r"Consider a complex function: $f(z) = u(x, y) + iv(x, y)$").set_color_by_gradient(RED, MAROON, PINK)
        complex_func_text.to_corner(UL)
        complex_func_text.shift(DOWN * 1)
        self.play(Write(complex_func_text))
        self.wait(2)
        
        # 解释z=x+iy
        z_def = Tex(r"where $z = x + iy$, $x, y \in \mathbb{R}$").set_color_by_gradient(RED, MAROON, PINK)
        z_def.next_to(complex_func_text, DOWN, buff=0.5)
        self.play(Write(z_def))
        self.wait(2)
        
        # 定义导数
        derivative_def = Tex(r"The derivative of $f(z)$ at point $z$ is defined as:").set_color_by_gradient(RED, MAROON, PINK)
        derivative_formula = MathTex(
            r"f'(z) = \lim_{\Delta z \to 0} \frac{f(z + \Delta z) - f(z)}{\Delta z}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        derivative_group = VGroup(derivative_def, derivative_formula).arrange(DOWN, buff=0.5)
        derivative_group.next_to(z_def, DOWN, buff=1.0)
        
        self.play(Write(derivative_def))
        self.play(Write(derivative_formula))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(title, complex_func_text, z_def, derivative_group)))
        self.wait(1)
        
        # 新页面：从不同方向逼近 - 水平方向
        approach_title = Title("Approach from Different Directions", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(approach_title))
        self.wait(1)
        
        horizontal_title = Tex("Horizontal Direction", font_size=36).set_color_by_gradient(RED, MAROON, PINK)
        horizontal_title.to_corner(UL).shift(DOWN * 1)
        self.play(Write(horizontal_title))
        self.wait(1)
        
        horizontal_text = Tex(r"$\Delta z = \Delta x$ (approaching along the real axis):").set_color_by_gradient(RED, MAROON, PINK)
        horizontal_text.next_to(horizontal_title, DOWN, buff=0.7).shift(RIGHT * 3)
        self.play(Write(horizontal_text))
        self.wait(1)
        
        horizontal_derivative = MathTex(
            r"f'(z) = \lim_{\Delta x \to 0} \frac{f(x+\Delta x, y) - f(x, y)}{\Delta x}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        horizontal_derivative.next_to(horizontal_text, DOWN, buff=0.7)
        self.play(Write(horizontal_derivative))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(approach_title, horizontal_title, horizontal_text, horizontal_derivative)))
        self.wait(1)
        
        # 新页面：垂直方向逼近
        vertical_title = Title("Vertical Direction Approach", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(vertical_title))
        self.wait(1)
        
        vertical_text = Tex(r"$\Delta z = i\Delta y$ (approaching along the imaginary axis):").set_color_by_gradient(RED, MAROON, PINK)
        vertical_text.to_corner(UL).shift(DOWN * 1)
        self.play(Write(vertical_text))
        self.wait(1)
        
        vertical_derivative = MathTex(
            r"f'(z) = \lim_{\Delta y \to 0} \frac{f(x, y+\Delta y) - f(x, y)}{i\Delta y}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        vertical_derivative.next_to(vertical_text, DOWN, buff=0.7)
        self.play(Write(vertical_derivative))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(vertical_title, vertical_text, vertical_derivative)))
        self.wait(1)
        
        # 新页面：推导柯西-黎曼方程
        cr_title = Title("Derivation of Cauchy-Riemann Equations", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(cr_title))
        self.wait(1)
        
        # 重新显示水平和垂直方向的导数公式
        horizontal_derivative = MathTex(
            r"f'(z) = \lim_{\Delta x \to 0} \frac{f(x+\Delta x, y) - f(x, y)}{\Delta x} = \frac{\partial u}{\partial x} + i\frac{\partial v}{\partial x}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        horizontal_derivative.to_corner(UL).shift(DOWN * 1)
        self.play(Write(horizontal_derivative))
        self.wait(2)
        
        vertical_derivative = MathTex(
            r"f'(z) = \lim_{\Delta y \to 0} \frac{f(x, y+\Delta y) - f(x, y)}{i\Delta y} = \frac{\partial v}{\partial y} - i\frac{\partial u}{\partial y}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        vertical_derivative.next_to(horizontal_derivative, DOWN, buff=1.0)
        self.play(Write(vertical_derivative))
        self.wait(3)
        
        # 写出完整的等式
        full_equation = MathTex(
            r"\frac{\partial u}{\partial x} + i\frac{\partial v}{\partial x} = \frac{\partial v}{\partial y} - i\frac{\partial u}{\partial y}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        full_equation.next_to(vertical_derivative, DOWN, buff=1.0)
        self.play(Write(full_equation))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(cr_title, horizontal_derivative, vertical_derivative, full_equation)))
        self.wait(1)
        
        # 新页面：实部分析
        real_title = Title("Real Part Analysis", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(real_title))
        self.wait(1)
        
        # 显示完整方程
        full_equation = MathTex(
            r"\frac{\partial u}{\partial x} + i\frac{\partial v}{\partial x} = \frac{\partial v}{\partial y} - i\frac{\partial u}{\partial y}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        full_equation.next_to(real_title, DOWN, buff=1.0)
        self.play(Write(full_equation))
        self.wait(2)
        
        # 分解为实部
        real_part = MathTex(r"\text{Real part: } \frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}").set_color_by_gradient(RED, MAROON, PINK)
        real_part.next_to(full_equation, DOWN, buff=1.0)
        self.play(Write(real_part))
        
        # 添加实部高亮框
        real_box = SurroundingRectangle(real_part, color=BLUE, buff=0.3)
        self.play(Create(real_box))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(real_title, full_equation, real_part, real_box)))
        self.wait(1)
        
        # 新页面：虚部分析
        imag_title = Title("Imaginary Part Analysis", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(imag_title))
        self.wait(1)
        
        # 显示完整方程
        full_equation = MathTex(
            r"\frac{\partial u}{\partial x} + i\frac{\partial v}{\partial x} = \frac{\partial v}{\partial y} - i\frac{\partial u}{\partial y}"
        ).set_color_by_gradient(RED, MAROON, PINK)
        full_equation.next_to(imag_title, DOWN, buff=1.0)
        self.play(Write(full_equation))
        self.wait(2)
        
        # 分解为虚部
        imag_part = MathTex(r"\text{Imaginary part: } \frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y}").set_color_by_gradient(RED, MAROON, PINK)
        imag_part.next_to(full_equation, DOWN, buff=1.0)
        self.play(Write(imag_part))
        
        # 添加虚部高亮框
        imag_box = SurroundingRectangle(imag_part, color=GREEN, buff=0.3)
        self.play(Create(imag_box))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(imag_title, full_equation, imag_part, imag_box)))
        self.wait(1)
        
        # 新页面：柯西-黎曼方程
        cr_title = Title("Cauchy-Riemann Equations", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(cr_title))
        self.wait(1)
        
        # 同时显示实部和虚部方程
        real_part = MathTex(r"\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}").set_color_by_gradient(RED, MAROON, PINK)
        imag_part = MathTex(r"\frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y}").set_color_by_gradient(RED, MAROON, PINK)
        equation_group = VGroup(real_part, imag_part).arrange(DOWN, buff=1.0)
        equation_group.move_to(ORIGIN)
        
        self.play(Write(real_part))
        self.play(Write(imag_part))
        
        # 将方程框起来
        cr_box = SurroundingRectangle(equation_group, color=YELLOW, buff=0.5)
        self.play(Create(cr_box))
        self.wait(3)
        
        # 清除页面
        self.play(FadeOut(VGroup(cr_title, real_part, imag_part, cr_box)))
        self.wait(1)
        
        # 应用示例标题
        app_title = Title("Applications", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(app_title))
        self.wait(1)
        
        # 示例1: f(z) = z^2
        ex1_title = Tex(r"Example 1: $f(z) = z^2$").set_color_by_gradient(RED, MAROON, PINK)
        ex1_title.to_corner(UL).shift(DOWN * 1).shift(RIGHT * 3)
        self.play(Write(ex1_title))
        self.wait(1)
        
        # 分解为实部和虚部
        ex1_uv = VGroup(
            MathTex(r"f(z) = (x+iy)^2 = x^2 - y^2 + i(2xy)"),
            MathTex(r"\Rightarrow u(x,y) = x^2 - y^2, \quad v(x,y) = 2xy")
        ).arrange(DOWN, buff=0.5).set_color_by_gradient(RED, MAROON, PINK)
        ex1_uv.next_to(ex1_title, DOWN, buff=0.7)
        
        self.play(Write(ex1_uv[0]))
        self.play(Write(ex1_uv[1]))
        self.wait(2)
        
        # 计算偏导数
        ex1_derivatives = VGroup(
            MathTex(r"\frac{\partial u}{\partial x} = 2x"),
            MathTex(r"\frac{\partial v}{\partial y} = 2x"),
            MathTex(r"\frac{\partial v}{\partial x} = 2y"),
            MathTex(r"\frac{\partial u}{\partial y} = -2y")
        ).arrange_in_grid(2, 2, buff=0.7).set_color_by_gradient(RED, MAROON, PINK)
        ex1_derivatives.next_to(ex1_uv, DOWN*0.3, buff=1.0).shift(LEFT*2)
        
        for derivative in ex1_derivatives:
            self.play(Write(derivative))
            self.wait(0.5)
        
        # 验证柯西-黎曼方程
        ex1_cr_check = VGroup(
            MathTex(r"\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y} \quad \checkmark"),
            MathTex(r"\frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y} \quad \checkmark")
        ).arrange(DOWN*0.3, buff=0.5).set_color_by_gradient(RED, MAROON, PINK)
        ex1_cr_check.next_to(ex1_uv, DOWN*0.3, buff=1.0).shift(RIGHT*4)
        
        self.play(Write(ex1_cr_check[0]))
        self.play(Write(ex1_cr_check[1]))
        self.wait(3)
        
        # 清除示例1页面
        self.play(FadeOut(VGroup(ex1_title, ex1_uv, ex1_derivatives, ex1_cr_check)))
        self.wait(1)
        
        # 新页面：示例2: f(z) = \overline{z}
        ex2_title = Tex(r"Example 2: $f(z) = \overline{z}$", font_size=42).set_color_by_gradient(RED, MAROON, PINK)
        ex2_title.to_corner(UL).shift(DOWN * 1).shift(RIGHT * 3)
        self.play(Write(ex2_title))
        self.wait(1)
        
        # 分解为实部和虚部
        ex2_uv = VGroup(
            MathTex(r"f(z) = x - iy"),
            MathTex(r"\Rightarrow u(x,y) = x, \quad v(x,y) = -y")
        ).arrange(DOWN, buff=0.5).set_color_by_gradient(RED, MAROON, PINK)
        ex2_uv.next_to(ex2_title, DOWN*0.2, buff=1.0)
        
        self.play(Write(ex2_uv[0]))
        self.play(Write(ex2_uv[1]))
        self.wait(2)
        
        # 计算偏导数
        ex2_derivatives = VGroup(
            MathTex(r"\frac{\partial u}{\partial x} = 1"),
            MathTex(r"\frac{\partial v}{\partial y} = -1"),
            MathTex(r"\frac{\partial v}{\partial x} = 0"),
            MathTex(r"\frac{\partial u}{\partial y} = 0")
        ).arrange_in_grid(2, 2, buff=0.7).set_color_by_gradient(RED, MAROON, PINK)
        ex2_derivatives.next_to(ex2_uv, DOWN*0.3, buff=1.0).shift(LEFT*3)
        
        for derivative in ex2_derivatives:
            self.play(Write(derivative))
            self.wait(0.5)
        
        # 验证柯西-黎曼方程
        ex2_cr_check = VGroup(
            MathTex(r"\frac{\partial u}{\partial x} \neq \frac{\partial v}{\partial y} \quad \times"),
            MathTex(r"\frac{\partial v}{\partial x} = -\frac{\partial u}{\partial y} \quad \checkmark")
        ).arrange(DOWN, buff=0.5).set_color_by_gradient(RED, MAROON, PINK)
        ex2_cr_check.next_to(ex2_uv, DOWN*0.3, buff=1.0).shift(RIGHT*3)
        
        self.play(Write(ex2_cr_check[0]))
        self.play(Write(ex2_cr_check[1]))
        self.wait(3)
        FadeOut(VGroup(ex2_title, ex2_uv, ex2_derivatives, ex2_cr_check))
        self.wait(1)
        # 总结
        conclusion = Tex("The Cauchy-Riemann equations are necessary conditions for a complex function to be analytic", font_size=40).set_color_by_gradient(RED, MAROON, PINK)
        conclusion.next_to(ex2_derivatives,DOWN*0.3).shift(RIGHT*4.5)
        self.play(Write(conclusion))
        self.wait(5)    