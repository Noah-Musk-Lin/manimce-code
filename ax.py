from manim import *

class SmoothCoordinateSystem(Scene):
    def construct(self):
        # 提高渲染质量
        config.pixel_height = 1080
        config.pixel_width = 1920
        config.frame_rate = 60
        
        # 创建基础坐标系
        ax = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=8,
            y_length=8,
            axis_config={
                "stroke_color": BLUE,
                "stroke_width": 2,
                "include_tip": True,  # 添加坐标轴箭头
                "tip_width": 0.15,
                "tip_height": 0.25,
            },
            x_axis_config={
                "numbers_to_include": [-4, -2, 0, 2, 4],
                "numbers_with_elongated_ticks": [-5, 5],
            },
            tips=False  # 关闭整体坐标轴箭头，使用上面的单独设置
        )
        
        # 添加坐标刻度
        ax.add_coordinates()
        
        # 绘制函数图像
        graph = ax.plot(
            lambda x: x**2,
            x_range=[-3, 3],
            color=YELLOW,
            stroke_width=3
        )
        
        # 添加函数标签
        func_label = MathTex(r"f(x) = x^2", color=YELLOW).next_to(graph, UP, buff=0.5)
        
        # 使用缓动函数使动画更丝滑
        self.play(Create(ax), run_time=2.5, rate_func=smooth)
        self.play(Create(graph, run_time=3, rate_func=there_and_back), 
                  Write(func_label, run_time=1.5), 
                  run_time=3)
        self.wait(1)    