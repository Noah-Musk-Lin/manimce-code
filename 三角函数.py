from manim import *

# 逻辑坐标 → Manim 坐标的映射（右手系，Z轴向上，Y轴向屏幕里）
def l2m(pos):
    x, y, z = pos
    return np.array([x, z, -y])

class TrigCircle3D(ThreeDScene):
    def construct(self):
        # 角度追踪器（0 → 2π）
        theta_tracker = ValueTracker(0)

        # ------------------------------------------------------------
        # 1. 自定义三维坐标轴（右手系：X右，Y里，Z上）
        # ------------------------------------------------------------
        axes_group = VGroup()
        origin = l2m((0, 0, 0))

        # X轴（红）
        x_axis = Arrow3D(origin, l2m((5, 0, 0)), color=RED, thickness=0.02)
        x_label = Tex("X", color=RED).move_to(l2m((5.3, -0.3, 0.3)))
        axes_group.add(x_axis, x_label)

        # Y轴（绿）– 指向屏幕里（Manim 的 -Z 方向）
        y_axis = Arrow3D(origin, l2m((0, 4, 0)), color=GREEN, thickness=0.02)
        y_label = Tex("Y", color=GREEN).move_to(l2m((0.3, 4.3, 0.3)))
        axes_group.add(y_axis, y_label)

        # Z轴（蓝）– 指向上方（Manim 的 +Y 方向）
        z_axis = Arrow3D(origin, l2m((0, 0, 4)), color=BLUE, thickness=0.02)
        z_label = Tex("Z", color=BLUE).move_to(l2m((0.3, 0.3, 4.3)))
        axes_group.add(z_axis, z_label)

        self.add(axes_group)

        # ------------------------------------------------------------
        # 2. 单位圆（XOZ平面，Y=0）
        #    圆心 (2,0,2)  →  Manim (2,2,0)
        #    半径 1，逆时针参数： (2+cosθ, 0, 2+sinθ)
        # ------------------------------------------------------------
        circle_center = l2m((2, 0, 2))
        circle = ParametricFunction(
            lambda t: l2m((2 + np.cos(t), 0, 2 + np.sin(t))),
            t_range=[0, 2 * PI],
            color=YELLOW,
            stroke_width=4
        )
        center_dot = Dot3D(circle_center, color=YELLOW, radius=0.08)
        self.add(circle, center_dot)

        # 动点（半径终点）和半径线段（始终跟随 theta）
        moving_dot = always_redraw(lambda: Dot3D(
            l2m((2 + np.cos(theta_tracker.get_value()), 0, 2 + np.sin(theta_tracker.get_value()))),
            color=ORANGE, radius=0.1
        ))
        radius_line = always_redraw(lambda: Line3D(
            circle_center,
            l2m((2 + np.cos(theta_tracker.get_value()), 0, 2 + np.sin(theta_tracker.get_value()))),
            color=ORANGE, stroke_width=3
        ))
        self.add(moving_dot, radius_line)

        # ------------------------------------------------------------
        # 3. 余弦曲线：从 X 轴上的点 (3,0,0) 沿 Y 轴延伸
        #    逻辑坐标 (2+cos y, y, 0), y ∈ [0, θ] → Manim (2+cos y, 0, -y)
        # ------------------------------------------------------------
        cos_curve = always_redraw(lambda: ParametricFunction(
            lambda t: l2m((2 + np.cos(t), t, 0)),
            t_range=[0, theta_tracker.get_value()],
            color=RED,
            stroke_width=3
        ))
        # 余弦曲线上的动点（对应当前角度）
        cos_dot = always_redraw(lambda: Dot3D(
            l2m((2 + np.cos(theta_tracker.get_value()), theta_tracker.get_value(), 0)),
            color=RED, radius=0.08
        ))
        # 从 X 轴起点到曲线起点的指示线（静态）
        x_start_point = l2m((3, 0, 0))  # θ=0 时曲线起点
        x_start_dot = Dot3D(x_start_point, color=RED, radius=0.06)
        x_start_label = Tex("cos", color=RED).move_to(l2m((3.5, 0, 0.5)))
        self.add(cos_curve, cos_dot, x_start_dot, x_start_label)

        # ------------------------------------------------------------
        # 4. 正弦曲线：从 Z 轴上的点 (0,0,2) 沿 Y 轴延伸
        #    逻辑坐标 (0, y, 2+sin y), y ∈ [0, θ] → Manim (0, 2+sin y, -y)
        # ------------------------------------------------------------
        sin_curve = always_redraw(lambda: ParametricFunction(
            lambda t: l2m((0, t, 2 + np.sin(t))),
            t_range=[0, theta_tracker.get_value()],
            color=BLUE,
            stroke_width=3
        ))
        sin_dot = always_redraw(lambda: Dot3D(
            l2m((0, theta_tracker.get_value(), 2 + np.sin(theta_tracker.get_value()))),
            color=BLUE, radius=0.08
        ))
        z_start_point = l2m((0, 0, 2))  # θ=0 时曲线起点
        z_start_dot = Dot3D(z_start_point, color=BLUE, radius=0.06)
        z_start_label = Tex("sin", color=BLUE).move_to(l2m((0.5, 2.5, 0.3)))
        self.add(sin_curve, sin_dot, z_start_dot, z_start_label)

        # ------------------------------------------------------------
        # 5. 辅助元素：水平面（XOY）和垂直面（XOZ）的半透明网格（可选）
        # ------------------------------------------------------------
        # 水平面 XOY (Z=0) → Manim Y=0 平面
        plane_xoy = Surface(
            lambda u, v: np.array([u, 0, v]),
            u_range=[0, 5],
            v_range=[-2, 3],
            fill_opacity=0.1,
            fill_color=GRAY,
            stroke_width=0.1,
            stroke_color=WHITE,
            resolution=(8, 8)
        )
        # 垂直面 XOZ (Y=0) → Manim Z=0 平面
        plane_xoz = Surface(
            lambda u, v: np.array([u, v, 0]),
            u_range=[0, 5],
            v_range=[0, 4],
            fill_opacity=0.1,
            fill_color=GRAY,
            stroke_width=0.1,
            stroke_color=WHITE,
            resolution=(8, 8)
        )
        self.add(plane_xoy, plane_xoz)

        # ------------------------------------------------------------
        # 6. 动画设置
        # ------------------------------------------------------------
        # 调整相机视角（俯仰60°，方位-45°，便于观察三维关系）
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        self.wait(1)

        # 播放角度从 0 到 2π 的动画，同时更新所有依赖 theta_tracker 的对象
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=12,
            rate_func=linear
        )
        self.wait(2)

        # 额外：旋转相机展示全貌（可选）
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(1)