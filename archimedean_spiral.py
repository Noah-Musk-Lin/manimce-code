from manim import *
# 在construct方法开头添加，指定中文字体
  # 或 "Microsoft YaHei"、"WenQuanYi Micro Hei" 等
class ArchimedeanSpiral(Scene):
    def construct(self):
        config.font = "SimHei"
        # 设置螺线参数：r = a + b·θ
        a = 0
        b = 0.55
        max_theta = 10 * PI  # 最大角度（10圈）

        # 创建参数方程：x = r·cos(θ), y = r·sin(θ)
        spiral = ParametricFunction(
            lambda t: np.array([
                (a + b * t) * np.cos(t),  # x 坐标
                (a + b * t) * np.sin(t),  # y 坐标
                0                          # z 坐标
            ]),
            t_range=[0, max_theta],
            color=BLUE
        ).set_stroke(width=4)

        # 添加坐标系
        axes = Axes(
            x_range=[-20, 20, 5],
            y_range=[-20, 20, 5],
            axis_config={"color": GREY}
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")

        # 添加标题
        title = Text("阿基米德螺线：")
        formula = Tex(r"$r = a + b\theta$")
        title_and_formula = VGroup(title, formula).arrange(DOWN, buff=0.5)
        title_and_formula.to_edge(UP)

        # 动画展示
        self.play(Create(axes), Write(axes_labels))
        self.play(Write(title_and_formula))
        self.wait(0.5)
        self.play(Create(spiral, run_time=6))  # 缓慢绘制螺线
        self.wait(2)

# 运行指令（在命令行中使用）：
# manim -pql archimedean_spiral.py ArchimedeanSpiral