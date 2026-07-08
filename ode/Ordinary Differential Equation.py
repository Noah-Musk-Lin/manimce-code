from manim import *
class OrdinaryDifferentialEquation(Scene):
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
        formula7 = MathTex("t = \\frac{y}{x}", font_size=35, color=WHITE).next_to(text10, buff=0.1)
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
        general_solution_xy = MathTex("y = C \\cdot \\frac{y}{x} \\cdot e^{\\int \\frac{1}{f\\left(\\frac{y}{x}\\right) - \\frac{y}{x}} d\\left(\\frac{y}{x}\\right)}",font_size=32,color = BLUE)
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        