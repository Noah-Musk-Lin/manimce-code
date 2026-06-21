from manim import *

# 修正：逻辑坐标 → Manim 坐标的映射（完全对齐Manim原生3D坐标系）
# 逻辑坐标：X右、Y里（深度）、Z上 → 直接对应Manim原生坐标，无需翻转
def l2m(pos):
    x, y, z = pos
    return np.array([x, y, z])  # 核心修正：移除原有的轴翻转

class TrigCircle3D(ThreeDScene):
    def construct(self):
        # 角度追踪器（0 → 2π）
        theta_tracker = ValueTracker(0)

        # ------------------------------------------------------------
        # 1. 自定义三维坐标轴（严格对齐：X右、Y里、Z上，XOY平面平行地面）
        # ------------------------------------------------------------
        axes_group = VGroup()
        origin = l2m((0, 0, 0))

        # X轴（红）：向右（地面水平方向）
        x_axis = Arrow3D(origin, l2m((5, 0, 0)), color=RED, thickness=0.02)
        x_label = Tex("X", color=RED).move_to(l2m((5.3, 0, 0.3)))
        axes_group.add(x_axis, x_label)

        # Y轴（绿）：向屏幕内（地面深度方向，XOY平面内）
        y_axis = Arrow3D(origin, l2m((0, 4, 0)), color=GREEN, thickness=0.02)
        y_label = Tex("Y", color=GREEN).move_to(l2m((0.3, 4.3, 0.3)))
        axes_group.add(y_axis, y_label)

        # Z轴（蓝）：竖直向上（垂直XOY平面）
        z_axis = Arrow3D(origin, l2m((0, 0, 4)), color=BLUE, thickness=0.02)
        z_label = Tex("Z", color=BLUE).move_to(l2m((0.3, 0.3, 4.3)))
        axes_group.add(z_axis, z_label)

        self.add(axes_group)

        # ------------------------------------------------------------
        # 2. 单位圆（XOZ平面，Y=0）→ 垂直地面的平面，圆心(2,0,2)
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
        # 3. 余弦曲线：沿Y轴（深度方向）延伸，X轴分量为cosθ
        #    逻辑坐标 (2+cos t, t, 0) → 地面（Z=0）上沿Y轴延伸
        # ------------------------------------------------------------
        cos_curve = always_redraw(lambda: ParametricFunction(
            lambda t: l2m((2 + np.cos(t), t, 0)),
            t_range=[0, theta_tracker.get_value()],
            color=RED,
            stroke_width=3
        ))
        cos_dot = always_redraw(lambda: Dot3D(
            l2m((2 + np.cos(theta_tracker.get_value()), theta_tracker.get_value(), 0)),
            color=RED, radius=0.08
        ))
        # 余弦曲线起点（θ=0）
        x_start_point = l2m((3, 0, 0))
        x_start_dot = Dot3D(x_start_point, color=RED, radius=0.06)
        x_start_label = Tex("cos", color=RED).move_to(l2m((3.5, 0, 0.5)))
        self.add(cos_curve, cos_dot, x_start_dot, x_start_label)

        # ------------------------------------------------------------
        # 4. 正弦曲线：沿Y轴（深度方向）延伸，Z轴分量为sinθ
        #    逻辑坐标 (0, t, 2+sin t) → 沿Y轴延伸，Z轴方向波动
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
        # 正弦曲线起点（θ=0）
        z_start_point = l2m((0, 0, 2))
        z_start_dot = Dot3D(z_start_point, color=BLUE, radius=0.06)
        z_start_label = Tex("sin", color=BLUE).move_to(l2m((0.5, 0, 2.5)))
        self.add(sin_curve, sin_dot, z_start_dot, z_start_label)

        # ------------------------------------------------------------
        # 5. 辅助平面（核心修正：对齐XOY地面、XOZ垂直面）
        # ------------------------------------------------------------
        # 水平面 XOY (Z=0) → 完全平行地面，覆盖核心区域
        plane_xoy = Surface(
            lambda u, v: l2m((u, v, 0)),  # Z=0 固定，u=X, v=Y
            u_range=[0, 5],
            v_range=[-2, 4],
            fill_opacity=0.1,
            fill_color=GRAY,
            stroke_width=0.1,
            stroke_color=WHITE,
            resolution=(8, 8)
        )
        # 垂直面 XOZ (Y=0) → 垂直地面，沿X-Z轴
        plane_xoz = Surface(
            lambda u, v: l2m((u, 0, v)),  # Y=0 固定，u=X, v=Z
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
        # 6. 动画设置（优化视角，更清晰观察XOY地面）
        # ------------------------------------------------------------
        # 调整相机视角：俯仰45°（更贴近地面视角），方位-45°
        self.set_camera_orientation(phi=45 * DEGREES, theta=-45 * DEGREES)
        self.wait(1)

        # 角度从0到2π的动画
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=12,
            rate_func=linear
        )
        self.wait(2)

        # 旋转相机展示全貌
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        self.wait(1)