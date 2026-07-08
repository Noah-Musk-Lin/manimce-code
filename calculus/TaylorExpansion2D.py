from manim import *
import numpy as np

class TaylorExpansion2D(Scene):
    def construct(self):
        # 标题
        title = Text("泰勒展开: f(x,y) = x² + 2y²", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 显示原函数
        func_tex = MathTex("f(x,y)", "=", "x^2", "+", "2y^2")
        func_tex.scale(1.2)
        self.play(Write(func_tex))
        self.wait(2)
        
        # 移动到顶部
        self.play(
            func_tex.animate.scale(0.8).to_edge(UP).shift(DOWN * 0.5)
        )
        
        # 计算偏导数
        derivatives_text = Text("在点 (0,0) 处的偏导数:", font_size=36)
        derivatives_text.next_to(func_tex, DOWN, buff=0.5)
        self.play(Write(derivatives_text))
        
        # 偏导数列表
        derivatives = VGroup(
            MathTex("f(0,0) = 0"),
            MathTex("f_x = 2x \\Rightarrow f_x(0,0) = 0"),
            MathTex("f_y = 4y \\Rightarrow f_y(0,0) = 0"),
            MathTex("f_{xx} = 2 \\Rightarrow f_{xx}(0,0) = 2"),
            MathTex("f_{yy} = 4 \\Rightarrow f_{yy}(0,0) = 4"),
            MathTex("f_{xy} = f_{yx} = 0")
        )
        
        derivatives.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        derivatives.scale(0.7)
        derivatives.next_to(derivatives_text, DOWN, buff=0.3)
        
        for deriv in derivatives:
            self.play(Write(deriv))
            self.wait(0.5)
        
        self.wait(2)
        
        # 清除偏导数显示
        self.play(
            FadeOut(derivatives_text),
            FadeOut(derivatives)
        )
        
        # 泰勒展开公式
        taylor_title = Text("泰勒展开公式:", font_size=36)
        taylor_title.next_to(func_tex, DOWN, buff=0.5)
        
        taylor_general = MathTex(
            "T(x,y) = f(0,0) + f_x(0,0)x + f_y(0,0)y + ",
            "\\frac{1}{2}[f_{xx}(0,0)x^2 + 2f_{xy}(0,0)xy + f_{yy}(0,0)y^2] + \\cdots"
        )
        taylor_general.scale(0.8)
        taylor_general.next_to(taylor_title, DOWN, buff=0.3)
        
        self.play(Write(taylor_title))
        self.play(Write(taylor_general))
        self.wait(2)
        
        # 代入数值
        taylor_substituted = MathTex(
            "T(x,y) = 0 + 0\\cdot x + 0\\cdot y + ",
            "\\frac{1}{2}[2x^2 + 2\\cdot 0\\cdot xy + 4y^2]"
        )
        taylor_substituted.scale(0.9)
        taylor_substituted.next_to(taylor_general, DOWN, buff=0.5)
        
        self.play(Write(taylor_substituted))
        self.wait(2)
        
        # 简化结果
        taylor_simplified = MathTex(
            "T(x,y) = x^2 + 2y^2"
        )
        taylor_simplified.scale(1.1)
        taylor_simplified.next_to(taylor_substituted, DOWN, buff=0.8)
        taylor_simplified.set_color(YELLOW)
        
        self.play(Write(taylor_simplified))
        self.wait(2)
        
        # 结论
        conclusion = Text("结论: 对于这个二次函数，二阶泰勒展开就是原函数本身!", 
                         font_size=32, color=GREEN)
        conclusion.next_to(taylor_simplified, DOWN, buff=0.8)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        # 创建函数图像（可选）
        self.show_function_surface()
    
    def show_function_surface(self):
        """显示函数曲面（可选部分）"""
        # 清除之前的文本
        self.clear()
        
        # 重新显示标题
        title = Text("函数 f(x,y) = x² + 2y² 的图像", font_size=36)
        title.to_edge(UP)
        self.play(Write(title))
        
        # 创建坐标系
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[0, 20, 5],
            x_length=6,
            y_length=6,
            z_length=4,
        )
        
        # 定义函数
        def func(x, y):
            return x**2 + 2*y**2
        
        # 创建曲面
        surface = Surface(
            lambda u, v: axes.c2p(u, v, func(u, v)),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            fill_opacity=0.7
        )
        surface.set_color(BLUE)
        
        # 设置3D相机
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        
        # 添加坐标系和曲面
        self.add(axes, surface)
        
        # 旋转展示
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(8)
        self.stop_ambient_camera_rotation()
