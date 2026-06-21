from manim import *
import numpy as np
class EulerFormulaProof(Scene):
    def construct(self):
        # 复平面与单位圆（放大1.5倍版本）
        plane = ComplexPlane(
            x_range=[-2.25, 2.25, 0.75],  # 原范围×1.5
            y_range=[-2.25, 2.25, 0.75],
            axis_config={
                "include_tip": True,          # 显示箭头
                "tip_width": 0.25 * 1.5,      # 箭头宽度（适配缩放比例）
                "tip_height": 0.35 * 1.5,     # 箭头高度（适配缩放比例）
                "include_numbers": True,      # 保留数字刻度
                "stroke_width": 2.5,          # 轴线条粗细
                "stroke_color": WHITE,        # 坐标轴颜色（与单位圆一致）
            },
            background_line_style={"stroke_color": TEAL, "stroke_width": 0.5, "stroke_opacity": 0.3}
        ).center().scale(1.5)  # 整体缩放

        unit_circle = Circle(radius=1.5, color=WHITE).move_to(plane.get_origin())  # 半径×1.5
        self.play(Create(plane), run_time=1.5)
        self.play(Create(unit_circle), run_time=1)
        self.wait(0.5)

        theta_tracker = ValueTracker(0)

        center_dot = Dot(plane.get_origin(), color=RED, radius=0.075)  # 点半径×1.5

        angle_arc = always_redraw(
            lambda: Arc(
                radius=0.6,  # 原0.4×1.5
                start_angle=0,
                angle=theta_tracker.get_value(),
                arc_center=plane.get_origin(),
                color=GREEN,
                stroke_width=3
            )
        )

        angle_label = always_redraw(
            lambda: MathTex(r"\theta", font_size=36, color=GREEN)  # 字体×1.5
                .next_to(
                    angle_arc.point_from_proportion(0.5), 
                    UR if theta_tracker.get_value() < PI else UL, 
                    buff=0.15
                )
        )

        moving_radius = always_redraw(
            lambda: Line(
                start=plane.get_origin(),
                end=plane.n2p(np.exp(1j * theta_tracker.get_value())),
                color=YELLOW,
                stroke_width=3
            )
        )

        static_radius = Line(plane.get_origin(), plane.n2p(1), color=YELLOW, stroke_width=2)

        euler_vector = always_redraw(lambda: Arrow(
            start=plane.get_origin(),
            end=plane.n2p(np.exp(1j * theta_tracker.get_value())),
            color=YELLOW, buff=0, tip_length=0.225,  # 箭头长度×1.5
            stroke_width=3
        ))

        # 文本信息：可适当放大字体（如从28→42，24→36）
        info_texts = VGroup(
            always_redraw(lambda: MathTex(fr"\theta = {theta_tracker.get_value():.2f}", font_size=42).to_corner(UL, buff=0.5)),
            always_redraw(lambda: MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=42).to_corner(UR, buff=0.5)),
            always_redraw(lambda: MathTex(fr"\cos\theta = {np.cos(theta_tracker.get_value()):.2f}", font_size=36, color=RED).to_corner(DL, buff=0.5)),
            always_redraw(lambda: MathTex(fr"\sin\theta = {np.sin(theta_tracker.get_value()):.2f}", font_size=36, color=BLUE).to_corner(DR, buff=0.5))
        )