from manim import *
class ODE(Scene):
    def construct(self):
        Text1 = Text("解常微分方程之换元法", font="SimHei", font_size=45).to_edge(UP)
        self.play(Write(Text1))
        self.wait(1)
        Text2 = Text("引入变换:", font="SimHei", font_size=30).to_edge(LEFT).shift(UP*2)
        self.play(Write(Text2))
        self.wait(1)
        formula0 = MathTex("t = h(x,y)", font_size=35).arrange(RIGHT,buff = 0.3).next_to(Text2, buff=0.5)
        self.play(Write(formula0))
        self.wait(1)
        Text3 = Text("两种理解方式:", font="SimHei", font_size=30).to_edge(LEFT).shift(UP)
        self.play(Write(Text3))
        self.wait(1)
        text5 = Text("1.将t视为x与y的二元函数,利用全微分的方法", font="SimHei", font_size=30,t2c={"全微分": BLUE})
        formula1 = MathTex("dt = \\frac{\\partial t}{\\partial x} dx + \\frac{\\partial t}{\\partial y} dy",font_size=30)
        group1 = VGroup(text5, formula1).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*0.2)
        self.play(Write(group1))
        self.wait(1)
        text6 = Text("2.将t视为x的复合函数,利用复合函数求导的方法", font="SimHei", font_size=30,t2c={"复合函数求导": BLUE})
        formula2 = MathTex("\\frac{dt}{dx} = \\frac{\\partial h}{\\partial x} + \\frac{\\partial h}{\\partial y}\\frac{dy}{dx}", font_size=30)
        group2 = VGroup(text6, formula2).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(DOWN*0.5)
        self.play(Write(group2))
        self.wait(1)
        
        
        
        formula3 = MathTex("dt = \\frac{\\partial t}{\\partial x} dx + \\frac{\\partial t}{\\partial y} dy", font_size=30)
        formula3.to_edge(LEFT).shift(DOWN*1.5)
        self.play(Write(formula3))
        self.wait(1)
        formula4 = MathTex("\\frac{dt}{dx} = \\frac{\\partial t}{\\partial x} \\cdot \\frac{dx}{dx} + \\frac{\\partial t}{\\partial y} \\cdot \\frac{dy}{dx}", font_size=30)
        formula4.move_to(formula3.get_center())
        self.play(Transform(formula3, formula4))
        self.wait(1.5)
        formula5 = MathTex("\\frac{dt}{dx} = \\frac{\\partial t}{\\partial x} + \\frac{\\partial t}{\\partial y}\\frac{dy}{dx}", font_size=30)
        formula5.move_to(formula4.get_center())
        self.play(Transform(formula3, formula5))
        self.wait(2)
        arrow = Arrow(start=(-3, 0, 0), end=(3, 0, 0), color=WHITE, stroke_width=3)
        arrow_top_text = Text("t是x,y的二元函数", font="SimHei", font_size=20, color=WHITE, t2c={"二元函数": YELLOW}).next_to(arrow, UP, buff=0.1)
        arrow_bottom_text = MathTex("\\frac{\\partial t}{\\partial x} = \\frac{\\partial h}{\\partial x}, \\quad \\frac{\\partial t}{\\partial y} = \\frac{\\partial h}{\\partial y}", font_size=20, color=YELLOW_B).next_to(arrow, DOWN, buff=0.1)
        arrow_group = VGroup(arrow, arrow_top_text, arrow_bottom_text)
        center_y = formula3.get_center()[1]
        arrow_group.next_to(formula3, RIGHT, buff=0.5)
        arrow_group.move_to([arrow_group.get_center()[0], center_y, 0])
        self.play(Write(arrow_group))
        self.wait(2)
        formula2_right = MathTex("\\frac{dt}{dx} = \\frac{\\partial h}{\\partial x} + \\frac{\\partial h}{\\partial y}\\frac{dy}{dx}", font_size=30)
        formula2_right.next_to(arrow_group, RIGHT, buff=0.3)
        formula2_right.move_to([formula2_right.get_center()[0], center_y, 0])
        self.play(Write(formula2_right))
        self.wait(2)
        
        
        
        text7 = Text("显然,两种理解方式推出的结果是完全一致的", font="SimHei", font_size=30,t2c={"完全一致": BLUE}).to_edge(LEFT).shift(DOWN*3)
        self.play(Write(text7))
        self.wait(2)
        
        self.play(
            FadeOut(Text2), 
            FadeOut(formula0),
            FadeOut(Text3), 
            FadeOut(group1), 
            FadeOut(group2), 
            FadeOut(formula3), 
            FadeOut(arrow_group), 
            FadeOut(formula2_right), 
            FadeOut(text7)
        )
        self.wait(1)

        text8 = Text("下面来运用换元解决常见的6种常微分方程", font="SimHei", font_size=35,color = YELLOW_A).to_edge(UP*2.5)
        self.play(Write(text8))
        self.wait(1)
        self.play(FadeOut(text8))
        self.wait(0.5)
        
        text9 = Text("1.一阶齐次方程", font="SimHei", font_size=30,color = WHITE).to_edge(LEFT).shift(UP*2)
        self.play(Write(text9))
        self.wait(0.5)
        formula6 = MathTex("\\frac{dy}{dx} = f(\\frac{y}{x})", font_size=40).arrange(RIGHT,buff = 0.3).next_to(text9, buff=0.5)
        self.play(Write(formula6))
        self.wait(1)
        text10 = Text("换元:令", font="SimHei", font_size=30, color=WHITE).next_to(formula6, buff=0.5)
        formula7 = MathTex("t = \\frac{y}{x}", font_size=35, color=BLUE).next_to(text10, buff=0.1)
        group4 = VGroup(text10,formula7).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*1)
        self.play(Write(group4))
        self.wait(1)
        text11 = Text("使用全微分的方法:", font="SimHei", font_size=30, color=WHITE)
        text11.next_to(group4, RIGHT, buff=0.3).align_to(group4, UP)
        formula8 = MathTex("dt = -\\frac{y}{x^2} \\, dx + \\frac{1}{x} \\, dy", font_size=35)
        formula8.next_to(text11, RIGHT, buff=0.3).align_to(text11, UP)
        group5 = VGroup(text11, formula8).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*0.2)
        self.play(Write(group5))
        self.wait(0.5)
        formula9 = MathTex("\\frac{dy}{dx} = \\frac{dy}{dt} \\cdot \\frac{dt}{dx} = f(t) \\cdot \\frac{1}{x}", font_size=40)
        text12 = Text("最后得到了一个关于x与t的变量可分离方程:", font="SimHei", font_size=30, color=WHITE)
        vertical_group = VGroup(formula9,text12).arrange(DOWN, buff=0.5)
        vertical_group.next_to(group5, DOWN, buff=0.5).align_to(group5, LEFT)
        self.play(Write(vertical_group[0]))  
        self.wait(0.5)
        self.play(Write(vertical_group[1])) 
        self.wait(0.5)
        formula10 = MathTex("t + x \\cdot \\frac{dt}{dx} = f(t)",font_size = 35)
        formula10.next_to(text12,RIGHT,buff = 0.3).set_y(text12.get_y())
        self.play(Write(formula10))
        self.wait(0.5)
        single_arrow = Arrow(start=vertical_group.get_left(),end=vertical_group.get_left()+RIGHT*2,stroke_width=3,color=WHITE)
        single_arrow.set_y(vertical_group.get_bottom()[1]-1)
        self.play(Create(single_arrow))
        self.wait(0.5)
        formula11 = MathTex("\\frac{dx}{x} = \\frac{dt}{f(t) - t}", font_size=35)
        formula11.next_to(single_arrow, RIGHT, buff=0.3)
        self.play(Write(formula11))
        self.wait(0.5)
        general_solution_xy = MathTex("y = C \\cdot \\frac{y}{x} \\cdot e^{\\int \\frac{1}{f\\left(\\frac{y}{x}\\right) - \\frac{y}{x}} d\\left(\\frac{y}{x}\\right)}",font_size=22,color = BLUE)
        text13 = Text("通积分为:", font="SimHei", font_size=30, color=WHITE)
        group6 = VGroup(text13, general_solution_xy)
        group6.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        formula11_center_y = formula11.get_center()[1]
        group6.next_to(formula11, RIGHT, buff=0.5)
        group6.move_to([group6.get_center()[0], formula11_center_y, 0])
        self.play(Write(group6))
        self.wait(2)
        self.play(
            FadeOut(text9), 
            FadeOut(formula6),
            FadeOut(group4), 
            FadeOut(group5), 
            FadeOut(vertical_group), 
            FadeOut(single_arrow), 
            FadeOut(formula10), 
            FadeOut(formula11),
            FadeOut(group6)
        )
        
        text14 = Text("2.伯努利(Bernoulli)方程", font="SimHei", font_size=30, color=WHITE).to_edge(LEFT).shift(UP*2)
        self.play(Write(text14))
        self.wait(0.5)

        formula12 = MathTex("\\frac{dy}{dx} + P(x)y = Q(x)y^n", font_size=40).arrange(RIGHT, buff=0.3).next_to(text14, buff=0.5)
        self.play(Write(formula12))
        self.wait(1)

        text15 = Text("换元:令", font="SimHei", font_size=30, color=WHITE).next_to(formula12, buff=0.5)
        formula13 = MathTex("v = y^{1 - n}", font_size=35, color=BLUE).next_to(text15, buff=0.1)
        group7 = VGroup(text15, formula13).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*1)
        self.play(Write(group7))
        self.wait(1)

        text16 = Text("求导:", font="SimHei", font_size=30, color=WHITE)
        text16.next_to(group7, RIGHT, buff=0.3).align_to(group7, UP)
        formula14 = MathTex("\\frac{dv}{dx} = (1 - n)y^{-n} \\cdot \\frac{dy}{dx}", font_size=35)
        formula14.next_to(text16, RIGHT, buff=0.3).align_to(text16, UP)
        group8 = VGroup(text16, formula14).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*0.2)
        self.play(Write(group8))
        self.wait(0.5)

        formula15 = MathTex("\\frac{dy}{dx} = \\frac{1}{1 - n}y^{n} \\cdot \\frac{dv}{dx}", font_size=35)
        formula15.next_to(group8, DOWN, buff=0.3).align_to(group8, LEFT)
        self.play(Write(formula15))
        self.wait(0.5)

        text17 = Text("代入原方程得到线性方程:", font="SimHei", font_size=30, color=WHITE)
        text17.next_to(formula15, DOWN, buff=0.5).align_to(formula15, LEFT)
        self.play(Write(text17))
        self.wait(0.5)

        formula16 = MathTex("\\frac{dv}{dx} + (1 - n)P(x)v = (1 - n)Q(x)", font_size=35)
        formula16.next_to(text17, RIGHT, buff=0.3).set_y(text17.get_y())
        self.play(Write(formula16))
        self.wait(0.5)

        single_arrow2 = Arrow(start=text17.get_left(), end=text17.get_left()+RIGHT*2, stroke_width=3, color=WHITE)
        single_arrow2.set_y(text17.get_bottom()[1]-0.5)
        self.play(Create(single_arrow2))
        self.wait(0.5)

        text18 = Text("利用一阶线性方程通解公式求解v，再回代", font="SimHei", font_size=30, color=WHITE)
        text18.next_to(single_arrow2, RIGHT, buff=0.3)
        self.play(Write(text18))
        self.wait(0.5)

        general_solution_bern = MathTex("y^{1-n} = e^{-\\int (1-n)P(x)dx} \\left[ \\int (1-n)Q(x)e^{\\int (1-n)P(x)dx}dx + C \\right]", font_size=28, color=BLUE)
        text19 = Text("通积分为:", font="SimHei", font_size=30, color=WHITE)
        group9 = VGroup(text19, general_solution_bern)
        group9.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        text18_center_y = text18.get_center()[1]
        group9.next_to(text18, DOWN, buff=0.5)
        group9.move_to([group9.get_center()[0], text18_center_y-0.7, 0])
        self.play(Write(group9))
        self.wait(2)

        self.play(
            FadeOut(text14),
            FadeOut(formula12),
            FadeOut(group7),
            FadeOut(group8),
            FadeOut(formula15),
            FadeOut(text17),
            FadeOut(formula16),
            FadeOut(single_arrow2),
            FadeOut(text18),
            FadeOut(group9)
        )
        
        text20 = Text("3.可化为齐次的方程（含常数项的线性分式型）", font="SimHei", font_size=30, color=WHITE).to_edge(LEFT).shift(UP*2)
        self.play(Write(text20))
        self.wait(0.5)

        formula17 = MathTex("\\frac{dy}{dx} = f\\left( \\frac{a_1 x + b_1 y + c_1}{a_2 x + b_2 y + c_2} \\right)", font_size=35).arrange(RIGHT, buff=0.3).next_to(text20, buff=0.5)
        self.play(Write(formula17))
        self.wait(1)

        text21 = Text("换元方法:", font="SimHei", font_size=30, color=WHITE).next_to(formula17, buff=0.5)
        group10 = VGroup(text21).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*1)
        self.play(Write(group10))
        self.wait(0.5)

        # 情况1:行列式非零
        text22 = Text("情况1:行列式非零", font="SimHei", font_size=28, color=YELLOW)
        text22.next_to(group10, DOWN, buff=0.3).align_to(group10, LEFT)
        self.play(Write(text22))
        self.wait(0.5)

        determinant_formula = MathTex("\\begin{vmatrix} a_1 & b_1 \\\\ a_2 & b_2 \\end{vmatrix} \\neq 0", font_size=35)
        determinant_formula.next_to(text22, RIGHT, buff=0.3).set_y(text22.get_y())
        self.play(Write(determinant_formula))
        self.wait(0.5)

        text23 = Text("平移变换消去常数项:", font="SimHei", font_size=28, color=WHITE)
        text23.next_to(text22, DOWN, buff=0.5).align_to(text22, LEFT)
        self.play(Write(text23))
        self.wait(0.5)

        transform_formula = MathTex("x = X + h,\\quad y = Y + k", font_size=30,color=BLUE)
        transform_formula.next_to(text23, RIGHT, buff=0.3).set_y(text23.get_y())
        self.play(Write(transform_formula))
        self.wait(0.5)

        system_text = Text("其中h,k满足:", font="SimHei", font_size=28, color=WHITE)
        system_text.next_to(text23, DOWN, buff=0.5).align_to(text23, LEFT)
        self.play(Write(system_text))
        self.wait(0.5)

        system_eq = MathTex("\\begin{cases} a_1 h + b_1 k + c_1 = 0 \\\\ a_2 h + b_2 k + c_2 = 0 \\end{cases}", font_size=30)
        system_eq.next_to(system_text, RIGHT, buff=0.3).set_y(system_text.get_y())
        self.play(Write(system_eq))
        self.wait(0.5)

        text24 = Text("转化为齐次方程:", font="SimHei", font_size=28, color=WHITE)
        text24.next_to(system_text, DOWN, buff=0.5).align_to(system_text, LEFT)
        self.play(Write(text24))
        self.wait(0.5)

        homogeneous_eq = MathTex("\\frac{dY}{dX} = f\\left( \\frac{a_1 X + b_1 Y}{a_2 X + b_2 Y} \\right)", font_size=30,color=RED)
        homogeneous_eq.next_to(text24, RIGHT, buff=0.3).set_y(text24.get_y())
        self.play(Write(homogeneous_eq))
        self.wait(2)

        # 淡出情况1的内容，保留大标题和方程形式
        self.play(
            FadeOut(text22),
            FadeOut(determinant_formula),
            FadeOut(text23),
            FadeOut(transform_formula),
            FadeOut(system_text),
            FadeOut(system_eq),
            FadeOut(text24),
            FadeOut(homogeneous_eq)
        )
        self.wait(0.5)

        # 情况2:行列式为零
        text25 = Text("情况2:行列式为零", font="SimHei", font_size=28, color=YELLOW)
        text25.next_to(group10, DOWN, buff=0.3).align_to(group10, LEFT)
        self.play(Write(text25))
        self.wait(0.5)

        zero_determinant = MathTex("a_1 b_2 = a_2 b_1", font_size=30)
        zero_determinant.next_to(text25, RIGHT, buff=0.3).set_y(text25.get_y())
        self.play(Write(zero_determinant))
        self.wait(0.5)

        text26 = Text("令", font="SimHei", font_size=28, color=WHITE)
        substitution_formula = MathTex("u = a_1 x + b_1 y", font_size=30,color=BLUE)
        group11 = VGroup(text26, substitution_formula).arrange(RIGHT, buff=0.1)
        group11.next_to(text25, DOWN, buff=0.5).align_to(text25, LEFT)
        self.play(Write(group11))
        self.wait(0.5)

        text27 = Text("方程转化为可分离变量方程:", font="SimHei", font_size=28, color=WHITE)
        text27.next_to(group11, DOWN, buff=0.5).align_to(group11, LEFT)
        self.play(Write(text27))
        self.wait(0.5)

        separable_eq = MathTex("\\frac{du}{dx} = a_1 + b_1 \\cdot f\\left( \\frac{u + c_1}{k u + c_2} \\right)", font_size=30,color=RED)
        separable_eq.next_to(text27, RIGHT, buff=0.3).set_y(text27.get_y())
        self.play(Write(separable_eq))
        self.wait(2)

        self.play(
            FadeOut(text20),
            FadeOut(formula17),
            FadeOut(group10),
            FadeOut(text25),
            FadeOut(zero_determinant),
            FadeOut(group11),
            FadeOut(text27),
            FadeOut(separable_eq)
        )
        
        text28 = Text("4.形如", font="SimHei", font_size=30, color=WHITE).to_edge(LEFT).shift(UP*2)
        formula18 = MathTex("\\frac{dy}{dx} = f(ax + by + c)", font_size=35).next_to(text28, RIGHT, buff=0.1)
        text28_end = Text("的方程", font="SimHei", font_size=30, color=WHITE).next_to(formula18, RIGHT, buff=0.1)
        title_group = VGroup(text28, formula18, text28_end)
        self.play(Write(title_group))
        self.wait(1)

        text29 = Text("换元方法:", font="SimHei", font_size=28, color=WHITE)
        group12 = VGroup(text29).to_edge(LEFT).shift(UP*1.2)
        self.play(Write(group12))
        self.wait(0.5)

        text30 = Text("令", font="SimHei", font_size=28, color=WHITE)
        formula19 = MathTex("u = ax + by + c", font_size=32, color=BLUE)
        group13 = VGroup(text30, formula19).arrange(RIGHT, buff=0.1).next_to(group12, DOWN, buff=0.2).align_to(group12, LEFT)
        self.play(Write(group13))
        self.wait(0.5)

        text31 = Text("求导:", font="SimHei", font_size=28, color=WHITE)
        formula20 = MathTex("\\frac{du}{dx} = a + b\\frac{dy}{dx}", font_size=32)
        group14 = VGroup(text31, formula20).arrange(RIGHT, buff=0.3).next_to(group13, DOWN, buff=0.2).align_to(group13, LEFT)
        self.play(Write(group14))
        self.wait(0.5)

        formula21 = MathTex("\\frac{dy}{dx} = \\frac{1}{b}\\left( \\frac{du}{dx} - a \\right)", font_size=32)
        formula21.next_to(group14, RIGHT, buff=0.5)
        self.play(Write(formula21))
        self.wait(0.5)

        text32 = Text("代入原方程:", font="SimHei", font_size=28, color=WHITE)
        text32.next_to(group14, DOWN, buff=0.25).align_to(group14, LEFT)
        self.play(Write(text32))
        self.wait(0.5)

        formula22 = MathTex("\\frac{1}{b}\\left( \\frac{du}{dx} - a \\right) = f(u)", font_size=32)
        formula22.next_to(text32, RIGHT, buff=0.3).set_y(text32.get_y())
        self.play(Write(formula22))
        self.wait(0.5)

        single_arrow3 = Arrow(start=text32.get_left(), end=text32.get_left()+RIGHT*2, stroke_width=3, color=WHITE)
        single_arrow3.set_y(text32.get_bottom()[1]-0.4)
        self.play(Create(single_arrow3))
        self.wait(0.5)

        formula23 = MathTex("\\frac{du}{dx} = b f(u) + a", font_size=32)
        formula23.next_to(single_arrow3, RIGHT, buff=0.3)
        self.play(Write(formula23))
        self.wait(0.5)

        text33 = Text("转化为可分离变量方程:", font="SimHei", font_size=26, color=WHITE)
        text33.next_to(single_arrow3, DOWN, buff=0.2).align_to(single_arrow3, LEFT)
        self.play(Write(text33))
        self.wait(0.5)

        formula24 = MathTex("\\frac{du}{b f(u) + a} = dx", font_size=28)
        formula24.next_to(text33, RIGHT, buff=0.3).set_y(text33.get_y())
        self.play(Write(formula24))
        self.wait(0.5)

        text34 = Text("通积分为:", font="SimHei", font_size=28, color=WHITE)
        general_solution = MathTex("\\int \\frac{du}{b f(u) + a} = x + C", font_size=32, color=BLUE)
        group15 = VGroup(text34, general_solution)
        group15.arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        group15.next_to(text33, DOWN, buff=0.25).align_to(text33, LEFT)
        self.play(Write(group15))
        self.wait(2)

        self.play(
            FadeOut(title_group),
            FadeOut(group12),
            FadeOut(group13),
            FadeOut(group14),
            FadeOut(formula21),
            FadeOut(text32),
            FadeOut(formula22),
            FadeOut(single_arrow3),
            FadeOut(formula23),
            FadeOut(text33),
            FadeOut(formula24),
            FadeOut(group15),
        )
        
        
        
        text35 = Text("5.高阶方程的降阶（通过换元降阶）", font="SimHei", font_size=30, color=WHITE).to_edge(LEFT).shift(UP*2)
        self.play(Write(text35))
        self.wait(0.5)

        text36 = Text("换元方法:", font="SimHei", font_size=30, color=WHITE).next_to(text35, buff=0.5)
        group16 = VGroup(text36).arrange(RIGHT, buff=0.3).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(group16))
        self.wait(0.5)

        # 情况1:不显含未知函数y的二阶方程
        text37 = Text("情况1:不显含未知函数y的二阶方程", font="SimHei", font_size=28, color=YELLOW)
        text37.next_to(group16, DOWN, buff=0.3).align_to(group16, LEFT)
        self.play(Write(text37))
        self.wait(0.5)

        formula25 = MathTex("y'' = f(x, y')", font_size=35)
        formula25.next_to(text37, RIGHT, buff=0.3).set_y(text37.get_y())
        self.play(Write(formula25))
        self.wait(0.5)

        text38 = Text("换元:", font="SimHei", font_size=28, color=WHITE)
        formula26 = MathTex("p = y'", font_size=30, color=BLUE)
        text39 = Text("则", font="SimHei", font_size=28, color=WHITE)
        formula27 = MathTex("y'' = \\frac{dp}{dx}", font_size=30)
        group17 = VGroup(text38, formula26, text39, formula27).arrange(RIGHT, buff=0.1)
        group17.next_to(text37, DOWN*0.5, buff=0.5).align_to(text37, LEFT)
        self.play(Write(group17))
        self.wait(0.5)

        text40 = Text("方程转化为一阶方程:", font="SimHei", font_size=28, color=WHITE)
        formula28 = MathTex("\\frac{dp}{dx} = f(x, p)", font_size=30, color=RED)
        group18 = VGroup(text40, formula28).arrange(RIGHT, buff=0.3)
        group18.next_to(group17, DOWN*0.5, buff=0.3).align_to(group17, LEFT)
        self.play(Write(group18))
        self.wait(0.5)

        text41 = Text("求解", font="SimHei", font_size=28, color=WHITE)
        formula29 = MathTex("p = \\varphi(x, C_1)", font_size=30)
        text42 = Text("后，再积分", font="SimHei", font_size=28, color=WHITE)
        formula30 = MathTex("y' = \\varphi(x, C_1)", font_size=30)
        group19 = VGroup(text41, formula29, text42, formula30).arrange(RIGHT, buff=0.1)
        group19.next_to(group18, DOWN*0.5, buff=0.5).align_to(group18, LEFT)
        self.play(Write(group19))
        self.wait(0.5)

        text43 = Text("得通解:", font="SimHei", font_size=28, color=WHITE)
        formula31 = MathTex("y = \\int \\varphi(x, C_1) dx + C_2", font_size=30, color=BLUE)
        group20 = VGroup(text43, formula31).arrange(RIGHT, buff=0.3)
        group20.next_to(group19, DOWN*0.5, buff=0.3).align_to(group19, LEFT)
        self.play(Write(group20))
        self.wait(2)

        # 淡出情况1的内容，保留大标题和换元方法
        self.play(
            FadeOut(text37),
            FadeOut(formula25),
            FadeOut(group17),
            FadeOut(group18),
            FadeOut(group19),
            FadeOut(group20)
        )
        self.wait(0.5)

        # 情况2:不显含自变量x的二阶方程
        text44 = Text("情况2:不显含自变量x的二阶方程", font="SimHei", font_size=28, color=YELLOW)
        text44.next_to(group16, DOWN, buff=0.3).align_to(group16, LEFT)
        self.play(Write(text44))
        self.wait(0.5)

        formula32 = MathTex("y'' = f(y, y')", font_size=35)
        formula32.next_to(text44, RIGHT, buff=0.3).set_y(text44.get_y())
        self.play(Write(formula32))
        self.wait(0.5)

        text45 = Text("换元:", font="SimHei", font_size=28, color=WHITE)
        formula33 = MathTex("p = y'", font_size=30, color=BLUE)
        text46 = Text("则", font="SimHei", font_size=28, color=WHITE)
        formula34 = MathTex("y'' = \\frac{dp}{dx} = \\frac{dp}{dy} \\cdot \\frac{dy}{dx} = p\\frac{dp}{dy}", font_size=30)
        group21 = VGroup(text45, formula33, text46, formula34).arrange(RIGHT, buff=0.1)
        group21.next_to(text44, DOWN, buff=0.5).align_to(text44, LEFT)
        self.play(Write(group21))
        self.wait(0.5)

        text47 = Text("方程转化为一阶方程:", font="SimHei", font_size=28, color=WHITE)
        formula35 = MathTex("p\\frac{dp}{dy} = f(y, p)", font_size=30, color=BLUE)
        group22 = VGroup(text47, formula35).arrange(RIGHT, buff=0.3)
        group22.next_to(group21, DOWN, buff=0.3).align_to(group21, LEFT)
        self.play(Write(group22))
        self.wait(0.5)

        text48 = Text("求解", font="SimHei", font_size=28, color=WHITE)
        formula36 = MathTex("p = \\psi(y, C_1)", font_size=30)
        text49 = Text("后，分离变量", font="SimHei", font_size=28, color=WHITE)
        formula37 = MathTex("\\frac{dy}{\\psi(y, C_1)} = dx", font_size=30)
        group23 = VGroup(text48, formula36, text49, formula37).arrange(RIGHT, buff=0.1)
        group23.next_to(group22, DOWN, buff=0.5).align_to(group22, LEFT)
        self.play(Write(group23))
        self.wait(0.5)

        text50 = Text("积分得通解:", font="SimHei", font_size=28, color=WHITE)
        formula38 = MathTex("\\int \\frac{dy}{\\psi(y, C_1)} = x + C_2", font_size=30, color=RED)
        group24 = VGroup(text50, formula38).arrange(RIGHT, buff=0.3)
        group24.next_to(group23, DOWN, buff=0.3).align_to(group23, LEFT)
        self.play(Write(group24))
        self.wait(2)

        self.play(
            FadeOut(text35),
            FadeOut(group16),
            FadeOut(text44),
            FadeOut(formula32),
            FadeOut(group21),
            FadeOut(group22),
            FadeOut(group23),
            FadeOut(group24)
        )
        # ===== 6. 黎卡提方程 — 第一页：推导 =====
        text51 = Text("6.黎卡提(Riccati)方程", font="SimHei", font_size=30, color=WHITE).to_edge(LEFT).shift(UP*2)
        self.play(Write(text51))
        self.wait(0.5)

        formula39 = MathTex("\\frac{dy}{dx} = P(x)y^2 + Q(x)y + R(x)", font_size=35)
        formula39.next_to(text51, RIGHT, buff=0.3)
        self.play(Write(formula39))
        self.wait(1)

        text52 = Text("换元方法:", font="SimHei", font_size=28, color=WHITE)
        group25 = VGroup(text52).to_edge(LEFT).shift(UP*1.2)
        self.play(Write(group25))
        self.wait(0.5)

        text53 = Text("设已知一个特解", font="SimHei", font_size=26, color=YELLOW)
        formula40 = MathTex("y_1(x)", font_size=28, color=YELLOW)
        group26 = VGroup(text53, formula40).arrange(RIGHT, buff=0.1)
        group26.next_to(group25, DOWN, buff=0.2).align_to(group25, LEFT)
        self.play(Write(group26))
        self.wait(0.5)

        text54 = Text("作变换:", font="SimHei", font_size=26, color=WHITE)
        formula41 = MathTex("y = y_1 + \\frac{1}{v}", font_size=30, color=BLUE)
        group27 = VGroup(text54, formula41).arrange(RIGHT, buff=0.1)
        group27.next_to(group26, DOWN, buff=0.2).align_to(group26, LEFT)
        self.play(Write(group27))
        self.wait(0.5)

        text55 = Text("求导:", font="SimHei", font_size=26, color=WHITE)
        formula42 = MathTex("\\frac{dy}{dx} = \\frac{dy_1}{dx} - \\frac{1}{v^2} \\frac{dv}{dx}", font_size=30)
        group28 = VGroup(text55, formula42).arrange(RIGHT, buff=0.3)
        group28.next_to(group27, DOWN, buff=0.2).align_to(group27, LEFT)
        self.play(Write(group28))
        self.wait(0.5)

        text56 = Text("代入原方程，利用特解满足方程化简:", font="SimHei", font_size=26, color=WHITE)
        text56.next_to(group28, DOWN, buff=0.25).align_to(group28, LEFT)
        self.play(Write(text56))
        self.wait(0.5)

        formula43 = MathTex("P(x)y_1^2 + Q(x)y_1 + R(x) = 0", font_size=28)
        formula43.next_to(text56, RIGHT, buff=0.3).set_y(text56.get_y())
        self.play(Write(formula43))
        self.wait(0.5)

        text57 = Text("得到关于v的线性方程:", font="SimHei", font_size=26, color=WHITE)
        text57.next_to(text56, DOWN, buff=0.25).align_to(text56, LEFT)
        self.play(Write(text57))
        self.wait(0.5)

        formula44 = MathTex("\\frac{dv}{dx} + [2P(x)y_1 + Q(x)] v = -P(x)", font_size=30)
        formula44.next_to(text57, RIGHT, buff=0.3).set_y(text57.get_y())
        self.play(Write(formula44))
        self.wait(2)

        # 翻页：淡出推导细节，保留标题
        self.play(
            FadeOut(group25),
            FadeOut(group26),
            FadeOut(group27),
            FadeOut(group28),
            FadeOut(text56),
            FadeOut(formula43),
            FadeOut(text57),
            FadeOut(formula44),
        )
        self.wait(0.5)

        # ===== 6. 黎卡提方程 — 第二页：求解 =====
        text60 = Text("求解:", font="SimHei", font_size=28, color=WHITE).to_edge(LEFT).shift(UP*1)
        self.play(Write(text60))
        self.wait(0.5)

        single_arrow4 = Arrow(start=text60.get_left(), end=text60.get_left()+RIGHT*2, stroke_width=3, color=WHITE)
        single_arrow4.set_y(text60.get_bottom()[1]-0.4)
        self.play(Create(single_arrow4))
        self.wait(0.5)

        text58 = Text("利用一阶线性方程通解公式求解v，再回代", font="SimHei", font_size=28, color=WHITE)
        text58.next_to(single_arrow4, RIGHT, buff=0.3)
        self.play(Write(text58))
        self.wait(0.5)

        text59 = Text("通解为:", font="SimHei", font_size=30, color=WHITE)
        formula45 = MathTex("y = y_1 + \\frac{1}{v(x)}", font_size=35, color=BLUE)
        group29 = VGroup(text59, formula45).arrange(RIGHT, buff=0.5, aligned_edge=DOWN)
        group29.next_to(text58, DOWN, buff=0.5).align_to(text58, LEFT)
        self.play(Write(group29))
        self.wait(2)

        self.play(
            FadeOut(text51),
            FadeOut(formula39),
            FadeOut(text60),
            FadeOut(single_arrow4),
            FadeOut(text58),
            FadeOut(group29),
            FadeOut(Text1)
        )
