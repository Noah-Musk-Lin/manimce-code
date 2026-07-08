"""
三维矢量场中心漩涡动画
========================
方案 C：中心吸引 + 切向旋转
引擎：Manim Community Edition
运行：manim -pql vortex_animation.py ThreeDVortex  (预览)
      manim -pqh vortex_animation.py ThreeDVortex  (高清)
"""

from manim import *
import numpy as np

# ============================================================
# 矢量场函数：方案 C — 中心吸引 + 切向旋转 + 垂向上升
# ============================================================

def vortex_field(pos):
    """
    三维漩涡矢量场 (笛卡尔坐标)
    - 径向分量：指向中心，r/(1+r²) 型，在 r≈1 处最强
    - 切向分量：绕 Z 轴旋转，(1+r)⁻¹ 衰减
    - 垂直分量：近中心轻微上升，Gaussian 衰减
    """
    x, y, z = pos[0], pos[1], pos[2]
    r_xy = np.sqrt(x ** 2 + y ** 2)

    if r_xy < 1e-8:
        return np.array([0.0, 0.0, 1.5])

    # 径向向内 (中心吸引)
    k_r = 2.0
    v_r = -k_r * r_xy / (1.0 + r_xy ** 2)

    # 切向旋转 (绕 Z 轴逆时针)
    k_theta = 3.0
    v_theta = k_theta / (1.0 + 0.5 * r_xy)

    # 垂直上升 (近中心)
    k_z = 1.5
    v_z = k_z * np.exp(-r_xy ** 2 / 2.0)

    # 笛卡尔分量
    v_x = v_r * x / r_xy - v_theta * y / r_xy
    v_y = v_r * y / r_xy + v_theta * x / r_xy

    return np.array([v_x, v_y, v_z])


# ============================================================
# 主场景
# ============================================================

class ThreeDVortex(ThreeDScene):
    """三维矢量场中心漩涡可视化"""

    def construct(self):
        # ---- 摄像机初始化 ----
        self.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.0)

        # ================================================
        # 阶段一：标题 (0-2s)
        # ================================================
        title = Text("三维矢量场：中心漩涡", font_size=40, color=WHITE)
        title.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.0)
        self.wait(0.5)

        # ================================================
        # 阶段二：三维坐标轴 (2-4s)
        # ================================================
        axes = ThreeDAxes(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            z_range=(-3, 3, 1),
            x_length=10,
            y_length=10,
            z_length=6,
        )
        axes.set_stroke(GREY, 0.6)
        axes_labels = axes.get_axis_labels(
            x_label="x",
            y_label="y",
            z_label="z",
        )

        self.play(Create(axes), Write(axes_labels), run_time=1.8)
        self.wait(0.3)

        # ================================================
        # 阶段三：中心涡核标记 (4-5s)
        # ================================================
        core_dot = Dot3D(point=ORIGIN, color=RED, radius=0.12)
        core_glow = Dot3D(point=ORIGIN, color=YELLOW, radius=0.20)
        core_glow.set_opacity(0.4)

        self.play(
            FadeIn(core_glow),
            FadeIn(core_dot),
            run_time=1.0,
        )

        # ================================================
        # 阶段四：矢量箭头阵列 (5-7s)
        # ================================================
        arrows = self.make_arrow_field()
        self.play(FadeIn(arrows), run_time=2.0)
        self.wait(0.3)

        # 隐藏标题，让画面更干净
        self.play(FadeOut(title), run_time=0.5)

        # ================================================
        # 阶段五：摄像机 360° 轨道旋转 (7-19s)
        # ================================================
        orbit_label = Text("360° 轨道视角", font_size=22, color=GREY)
        orbit_label.to_corner(UL, buff=0.5)
        self.add_fixed_in_frame_mobjects(orbit_label)
        self.play(FadeIn(orbit_label), run_time=0.5)

        # 平滑环绕旋转
        self.begin_ambient_camera_rotation(rate=0.10)
        self.wait(10)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(orbit_label), run_time=0.5)
        self.wait(0.5)

        # ================================================
        # 阶段六：收尾 (25-30s)
        # ================================================
        end_text = Text("漩涡场可视化", font_size=36, color=WHITE)
        end_text.to_edge(DOWN, buff=0.8)
        self.add_fixed_in_frame_mobjects(end_text)
        self.play(Write(end_text), run_time=1.0)
        self.wait(2)

        # 全场淡出
        self.play(
            FadeOut(end_text),
            FadeOut(arrows),
            FadeOut(core_dot),
            FadeOut(core_glow),
            FadeOut(axes),
            FadeOut(axes_labels),
            run_time=1.5,
        )
        self.wait(0.5)

    # ========================================================
    # 构建箭头阵列
    # ========================================================

    def make_arrow_field(self):
        """
        三维网格采样 → 计算矢量 → 生成 Arrow3D
        颜色：蓝(外围低速) → 红(核心高速)
        长度：非线性压缩以提升外围可见性
        """
        all_arrows = VGroup()

        # 精简采样网格: 5×5×3 = 75 点
        xs = np.linspace(-4, 4, 5)
        ys = np.linspace(-4, 4, 5)
        zs = np.linspace(-2, 2, 3)

        # 收集数据
        samples = []
        max_speed = 0.0
        for x in xs:
            for y in ys:
                for z in zs:
                    r = np.sqrt(x ** 2 + y ** 2)
                    if r < 0.25:  # 跳过核心奇点
                        continue
                    vel = vortex_field(np.array([x, y, z]))
                    speed = float(np.linalg.norm(vel))
                    if speed > max_speed:
                        max_speed = speed
                    samples.append((np.array([x, y, z]), vel, speed))

        max_speed = max(max_speed, 1e-6)

        # 批量生成箭头
        for pos, vel, speed in samples:
            t = np.clip(speed / max_speed, 0.0, 1.0)
            color = interpolate_color(BLUE, RED, t)

            direction = vel / np.linalg.norm(vel)

            # 非线性长度映射
            length = 0.35 + 0.65 * np.sqrt(t)

            arrow = Arrow3D(
                start=pos - direction * length / 2,
                end=pos + direction * length / 2,
                color=color,
                thickness=0.025,
                resolution=8,
            )
            all_arrows.add(arrow)

        return all_arrows
