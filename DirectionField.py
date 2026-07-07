"""
线素场（方向场）动画 — 基于《常微分方程》教材 §2.1.1

Manim Community v0.20.1
运行: conda activate manimce && manim -pqh manimce\ code/DirectionField.py DirectionField
"""

from manim import *

# 全局字体设置以支持中文
config.font = "SimHei"


class DirectionField(Scene):
    """线素场（方向场）完整动画：

    1. 展示题目：dy/dx = y/x 的线素场
    2. 逐行/逐列绘制线素，直观展示"区域 G 内每一点都有一个线素"
    3. 高亮演示单个线素的构造过程（以某点为中心，斜率为 k 的单位线段）
    4. 叠加积分曲线 y = Cx，展示解曲线处处与线素相切
    """

    def construct(self):
        # ── 1. 标题与坐标系 ──────────────────────────────────
        title = Text("线素场（方向场）", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.4)
        equation = MathTex(
            r"\frac{dy}{dx} = \frac{y}{x}",
            font_size=40,
        ).set_color_by_tex("y", YELLOW)
        equation.next_to(title, DOWN, buff=0.25)

        self.play(Write(title), Write(equation))
        self.wait(0.6)

        # 坐标轴
        axes = Axes(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            x_length=12,
            y_length=12,
            axis_config={
                "color": GREY_B,
                "stroke_width": 2,
                "include_tip": True,
                "tip_shape": StealthTip,
            },
            x_axis_config={"numbers_to_include": range(-8, 9, 2)},
            y_axis_config={"numbers_to_include": range(-8, 9, 2)},
        )
        axes.center()
        labels = axes.get_axis_labels(
            x_label=MathTex("x", font_size=36),
            y_label=MathTex("y", font_size=36),
        )

        self.play(Create(axes), Write(labels), run_time=1.5)
        self.wait(0.3)

        # ── 2. 构造线素场数据 ────────────────────────────────
        lines = VGroup()
        r = 6               # 绘制范围
        spacing = 0.6       # 网格间距
        line_len = 0.45     # 线素半长

        for x in np.arange(-r, r + 1e-9, spacing):
            for y in np.arange(-r, r + 1e-9, spacing):
                # 跳过奇点 x ≈ 0
                if abs(x) < 1e-6:
                    continue

                k = y / x

                # 单位方向向量
                direction = np.array([1, k, 0])
                direction /= np.linalg.norm(direction)

                center = axes.coords_to_point(x, y)
                start = center - line_len * direction
                end = center + line_len * direction

                line = Line(start, end, color=BLUE_D, stroke_width=2.0)
                lines.add(line)

        # ── 3. 动态逐行绘制线素场 ─────────────────────────────
        concept_text = Text(
            "以点 (x, y) 为中点，作斜率为 k = y/x 的线段",
            font_size=28,
            color=GREY_B,
        )
        concept_text.to_edge(DOWN, buff=0.5)
        self.play(Write(concept_text), run_time=0.5)

        # 按行分组以实现逐行动画
        rows = []
        for x_val in np.arange(-r, r + 1e-9, spacing):
            row_lines = VGroup()
            for y_val in np.arange(-r, r + 1e-9, spacing):
                if abs(x_val) < 1e-6:
                    continue
                k = y_val / x_val
                direction = np.array([1, k, 0])
                direction /= np.linalg.norm(direction)
                center = axes.coords_to_point(x_val, y_val)
                start = center - line_len * direction
                end = center + line_len * direction
                row_lines.add(Line(start, end, color=BLUE_D, stroke_width=2.0))
            if len(row_lines) > 0:
                rows.append(row_lines)

        self.play(
            LaggedStart(
                *[Create(row) for row in rows],
                lag_ratio=0.03,
            ),
            run_time=10,
            rate_func=linear,
        )
        self.wait(0.5)

        # 更新说明文字
        explanation = Text(
            "区域 G 内每一点都有一个线素 —— 构成线素场",
            font_size=28,
            color=WHITE,
        )
        self.play(FadeTransform(concept_text, explanation))
        self.wait(1.5)

        # ── 4. 高亮演示单个线素的含义 ─────────────────────────
        demo_point = axes.coords_to_point(3, 2)
        demo_x, demo_y = 3, 2
        demo_k = demo_y / demo_x
        demo_dir = np.array([1, demo_k, 0])
        demo_dir /= np.linalg.norm(demo_dir)

        demo_start = demo_point - line_len * demo_dir
        demo_end = demo_point + line_len * demo_dir
        demo_line = Line(
            demo_start, demo_end,
            color=YELLOW,
            stroke_width=6,
        )

        dot = Dot(demo_point, color=YELLOW, radius=0.1)
        coord_label = MathTex(
            f"({demo_x}, {demo_y})",
            font_size=32,
            color=YELLOW,
        ).next_to(demo_point, UR, buff=0.15)

        slope_label = MathTex(
            f"k = f({demo_x},{demo_y}) = \\frac{{{demo_y}}}{{{demo_x}}}",
            font_size=30,
            color=YELLOW,
        ).next_to(explanation, UP, buff=0.3)

        self.play(FadeOut(explanation))
        self.play(
            Write(slope_label),
            GrowFromCenter(dot),
            Write(coord_label),
            Create(demo_line),
            run_time=1.2,
        )
        self.wait(2)

        # ── 5. 叠加积分曲线 ──────────────────────────────────
        self.play(
            FadeOut(slope_label),
            FadeOut(dot),
            FadeOut(coord_label),
            FadeOut(demo_line),
            run_time=0.6,
        )

        curves_title = Text(
            "积分曲线处处与线素相切",
            font_size=30,
            color=WHITE,
        )
        curves_title.next_to(explanation, UP, buff=0.3).move_to(
            [explanation.get_center()[0], curves_title.get_center()[1], 0]
        )
        # explanation 已 FadeOut，直接 Write
        self.play(Write(curves_title))

        # 绘制通解 y = C*x 的若干积分曲线
        curves = VGroup()
        c_values = [-3, -2, -1, -0.5, -0.2, 0.2, 0.5, 1, 2, 3]
        colors = color_gradient([RED, ORANGE, YELLOW, GREEN, TEAL, BLUE], len(c_values))

        for c, clr in zip(c_values, colors):
            graph = axes.plot(
                lambda x_val, c_val=c: c_val * x_val,
                x_range=[-r, r],
                color=clr,
                stroke_width=3.5,
            )
            # 移除 x=0 附近（因为原方程在 x=0 无定义）
            curves.add(graph)

        self.play(
            LaggedStart(
                *[Create(curve) for curve in curves],
                lag_ratio=0.15,
            ),
            run_time=5,
        )
        self.wait(1)

        # 添加通解公式
        general_solution = MathTex(
            r"y = C x \quad (C \in \mathbb{R})",
            font_size=36,
            color=WHITE,
        )
        general_solution.next_to(title, DOWN, buff=0.25)

        self.play(Write(general_solution))
        self.wait(3)

        # ── 6. 收尾：回到完整线素场视角 ─────────────────────
        self.play(FadeOut(curves), FadeOut(curves_title), run_time=0.8)
        self.play(FadeTransform(general_solution, equation))
        self.wait(1)

        final_text = Text("线素场 — 微分方程的几何灵魂", font_size=30, color=GREY_B)
        final_text.next_to(explanation, UP, buff=0.3).move_to(
            [explanation.get_center()[0], final_text.get_center()[1], 0]
        )
        # explanation was already removed, just write
        self.play(Write(final_text))
        self.wait(3)


class SingleLineElement(Scene):
    """单独展示一个线素的构造过程 —— 适合课堂逐步讲解"""

    def construct(self):
        # 坐标轴
        axes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 5, 1],
            x_length=8,
            y_length=8,
            axis_config={"include_tip": True, "tip_shape": StealthTip},
            x_axis_config={"numbers_to_include": range(0, 6)},
            y_axis_config={"numbers_to_include": range(0, 6)},
        )
        axes.center()
        self.play(Create(axes), Write(axes.get_axis_labels("x", "y")))

        # 取点 (2, 1)，斜率 k = 1/2
        x0, y0 = 2, 1
        k = y0 / x0  # 0.5

        point = axes.coords_to_point(x0, y0)

        # 标记点
        dot = Dot(point, color=YELLOW, radius=0.12)
        coord = MathTex(f"({x0},{y0})", font_size=30, color=YELLOW).next_to(point, UR, buff=0.15)
        self.play(GrowFromCenter(dot), Write(coord))
        self.wait(0.8)

        # 斜率计算
        eq = MathTex(
            r"\frac{dy}{dx} = \frac{y}{x}",
            font_size=36,
        ).to_edge(UP, buff=0.6)
        slope_eq = MathTex(
            f"k = f({x0},{y0}) = \\frac{{{y0}}}{{{x0}}} = {k}",
            font_size=32,
            color=YELLOW,
        ).next_to(eq, DOWN, buff=0.3)

        self.play(Write(eq), Write(slope_eq))
        self.wait(1)

        # 方向向量
        direction = np.array([1, k, 0])
        direction /= np.linalg.norm(direction)
        half_len = 0.6

        start = point - half_len * direction
        end = point + half_len * direction

        # 虚线的方向向量
        dir_line = DashedLine(
            point + np.array([-1.5, -1.5 * k, 0]),
            point + np.array([1.5, 1.5 * k, 0]),
            color=GREY_A,
            stroke_width=1.5,
        )
        self.play(Create(dir_line), run_time=1)

        # 绘制线素
        line_element = Line(start, end, color=BLUE, stroke_width=6)
        self.play(Create(line_element), run_time=0.8)
        self.wait(0.5)

        # 标注
        mid_mark = Text("中点", font_size=24, color=WHITE).next_to(dot, DL, buff=0.2)
        line_label = Text("线素 (单位线段)", font_size=24, color=BLUE).next_to(
            line_element.get_center(), RIGHT, buff=0.3
        )
        slope_indicator = MathTex(
            f"\\text{{斜率 }} k = {k}",
            font_size=28,
            color=YELLOW,
        ).next_to(line_element.get_center(), LEFT, buff=0.4)

        self.play(Write(mid_mark), Write(line_label), Write(slope_indicator))
        self.wait(3)
