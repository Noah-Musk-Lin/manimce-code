from manim import *
import numpy as np


class EllipsePerpendicularSegments(Scene):
    def construct(self):
        # ===================== 1. 椭圆参数 =====================
        a, b = 4, 2
        const_val = 1 / a**2 + 1 / b**2  # 理论常数 1/a² + 1/b² = 0.3125

        ellipse = Ellipse(width=2 * a, height=2 * b, color=BLUE, stroke_width=2)
        center_O = Dot(ORIGIN, color=WHITE)
        label_O = MathTex("O", font_size=30, color=WHITE).next_to(
            ORIGIN, DOWN + LEFT, buff=0.15
        )

        # ===================== 2. 椭圆方程（先显示后消失）=====================
        eq = MathTex(
            r"\frac{x^2}{%d}" % (a**2),
            r"+ \frac{y^2}{%d}" % (b**2),
            r"= 1",
            font_size=36,
            color=YELLOW,
        ).to_edge(UP)

        self.play(Create(ellipse), FadeIn(center_O, label_O))
        self.wait(0.5)
        self.play(Write(eq))
        self.wait(1.5)
        self.play(FadeOut(eq))

        # ===================== 3. 线段 OA、OB（始���垂直）=====================
        theta_tracker = ValueTracker(0)

        def get_ellipse_point(theta: float) -> np.ndarray:
            cos_t = np.cos(theta)
            sin_t = np.sin(theta)
            denom = np.sqrt((cos_t / a) ** 2 + (sin_t / b) ** 2)
            r = 1 / denom
            return np.array([r * cos_t, r * sin_t, 0])

        def get_A(theta: float) -> np.ndarray:
            return get_ellipse_point(theta)

        def get_B(theta: float) -> np.ndarray:
            return get_ellipse_point(theta + PI / 2)

        # 动态点和线段
        dot_A = always_redraw(
            lambda: Dot(get_A(theta_tracker.get_value()), color=RED)
        )
        dot_B = always_redraw(
            lambda: Dot(get_B(theta_tracker.get_value()), color=GREEN)
        )
        line_OA = always_redraw(
            lambda: Line(
                ORIGIN, get_A(theta_tracker.get_value()), color=RED, stroke_width=3
            )
        )
        line_OB = always_redraw(
            lambda: Line(
                ORIGIN, get_B(theta_tracker.get_value()), color=GREEN, stroke_width=3
            )
        )
        label_A = always_redraw(
            lambda: MathTex("A", font_size=28, color=RED).next_to(
                get_A(theta_tracker.get_value()), UR, buff=0.1
            )
        )
        label_B = always_redraw(
            lambda: MathTex("B", font_size=28, color=GREEN).next_to(
                get_B(theta_tracker.get_value()), UR, buff=0.1
            )
        )
        right_angle = always_redraw(
            lambda: RightAngle(
                Line(ORIGIN, get_A(theta_tracker.get_value())),
                Line(ORIGIN, get_B(theta_tracker.get_value())),
                length=0.3,
                color=YELLOW,
            )
        )

        # ===================== 4. 右侧信息面板 =====================
        # 将信息放在画面右侧偏上的位置
        panel_x = 4.5  # 右侧 x 坐标
        panel_top = 2.5  # 顶部 y 坐标
        line_spacing = 0.6  # 行间距

        def panel_y(row: int) -> float:
            """第 row 行（从0开始）的 y 坐标"""
            return panel_top - row * line_spacing

        # 标题
        title = Text("实时计算面板", font_size=22, color=GRAY).move_to(
            np.array([panel_x, panel_top + 0.5, 0])
        )

        # 第1行：|OA| 长度（实时）
        len_OA_label = always_redraw(
            lambda: MathTex(
                r"|OA| = %.4f" % np.linalg.norm(get_A(theta_tracker.get_value())),
                font_size=26,
                color=RED,
            ).move_to(np.array([panel_x, panel_y(0), 0]))
        )

        # 第2行：|OB| 长度（实时）
        len_OB_label = always_redraw(
            lambda: MathTex(
                r"|OB| = %.4f" % np.linalg.norm(get_B(theta_tracker.get_value())),
                font_size=26,
                color=GREEN,
            ).move_to(np.array([panel_x, panel_y(1), 0]))
        )

        # 分隔线
        sep_line = Line(
            np.array([panel_x - 2.5, panel_y(1.5), 0]),
            np.array([panel_x + 2.5, panel_y(1.5), 0]),
            color=DARK_GRAY,
            stroke_width=1,
        )

        # 第3行：1/OA²（实时）
        inv_OA_label = always_redraw(
            lambda: MathTex(
                r"\frac{1}{|OA|^2} = %.4f"
                % (1 / np.linalg.norm(get_A(theta_tracker.get_value())) ** 2),
                font_size=26,
                color=RED,
            ).move_to(np.array([panel_x, panel_y(2), 0]))
        )

        # 第4行：1/OB²（实时）
        inv_OB_label = always_redraw(
            lambda: MathTex(
                r"\frac{1}{|OB|^2} = %.4f"
                % (1 / np.linalg.norm(get_B(theta_tracker.get_value())) ** 2),
                font_size=26,
                color=GREEN,
            ).move_to(np.array([panel_x, panel_y(3), 0]))
        )

        # 分隔线2
        sep_line2 = Line(
            np.array([panel_x - 2.5, panel_y(3.5), 0]),
            np.array([panel_x + 2.5, panel_y(3.5), 0]),
            color=DARK_GRAY,
            stroke_width=1,
        )

        # 第5行：1/OA² + 1/OB²（实时求和）
        sum_label = always_redraw(
            lambda: MathTex(
                r"\frac{1}{|OA|^2} + \frac{1}{|OB|^2} = %.4f"
                % (
                    1 / np.linalg.norm(get_A(theta_tracker.get_value())) ** 2
                    + 1 / np.linalg.norm(get_B(theta_tracker.get_value())) ** 2
                ),
                font_size=28,
                color=YELLOW,
            ).move_to(np.array([panel_x, panel_y(4), 0]))
        )

        # 第6行：理论常数 1/a² + 1/b²（不变）
        const_label = MathTex(
            r"\frac{1}{a^2} + \frac{1}{b^2} = \frac{1}{%d} + \frac{1}{%d} = %.4f"
            % (a**2, b**2, const_val),
            font_size=26,
            color=TEAL,
        ).move_to(np.array([panel_x, panel_y(5), 0]))

        # ===================== 5. 底部公式 =====================
        formula = VGroup(
            MathTex(r"\frac{1}{OA^2}", color=RED),
            MathTex("+", color=WHITE),
            MathTex(r"\frac{1}{OB^2}", color=GREEN),
            MathTex("=", color=WHITE),
            MathTex(r"\frac{1}{a^2}", color=PURPLE),
            MathTex("+", color=WHITE),
            MathTex(r"\frac{1}{b^2}", color=ORANGE),
        ).arrange(RIGHT, buff=0.15).scale(0.85).next_to(ellipse, DOWN, buff=0.5)

        # ===================== 6. 动画序列 =====================
        self.play(
            Create(line_OA),
            Create(line_OB),
            FadeIn(dot_A, dot_B),
            FadeIn(label_A, label_B),
            FadeIn(right_angle),
        )
        self.wait(0.3)

        # 显示右侧面板（逐行出现）
        self.play(FadeIn(title))
        self.wait(0.2)

        self.play(Write(len_OA_label), Write(len_OB_label))
        self.wait(0.3)

        self.play(Create(sep_line))
        self.play(Write(inv_OA_label), Write(inv_OB_label))
        self.wait(0.3)

        self.play(Create(sep_line2))
        self.play(Write(sum_label), Write(const_label))
        self.wait(0.5)

        # 显示底部恒等式
        self.play(FadeIn(formula))
        self.wait(1)

        # 线段旋转 2 圈，所有数值实时跳动
        self.play(
            theta_tracker.animate.set_value(4 * PI),
            run_time=8,
            rate_func=linear,
        )
        self.wait(1)
