from manim import *

class HeartCurve(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-20, 20, 2],
            y_range=[-20, 20, 2],
            axis_config={"color": BLUE},
            x_length=8,
            y_length=8
        )
        
        # 定义心形曲线的参数方程
        def heart_function(t):
            x = 16 * (np.sin(t))**3 - 5 * np.sin(t)
            y = 13 * np.cos(t) - 5 * np.sin(2*t) - 5 * np.sin(t)
            return axes.c2p(x, y)
        
        # 创建心形曲线
        heart = ParametricFunction(
            heart_function,
            t_range=[0, 2*PI],
            color=RED,
            stroke_width=4
        )
        
        # 添加标题
        title = Text("Heart Curve", font_size=40).to_corner(UL)
        
        # 添加坐标轴标签
        x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=RIGHT, buff=0.2)
        y_label = axes.get_y_axis_label("y", edge=UP, direction=UP, buff=0.2)
        
        # 动画显示
        self.play(Create(axes))
        self.play(Write(title))
        self.play(Create(heart))
        self.wait(2)
