# -*- coding: utf-8 -*-
"""
矩阵的极分解 (Polar Decomposition) —— ManimCE 动画脚本

数学背景：任何实矩阵 A 都可分解为 A = U P，
其中 P 为对称半正定矩阵（拉伸/缩放部分），U 为正交矩阵（旋转/翻转部分）。

本脚本严格遵循约定：
    P = (AᵀA)^{1/2}   对称半正定，负责"先拉伸"
    U = A P^{-1}      正交，负责"后旋转"
满足  A = U P  （列向量右乘约定，顺序不可交换！）

用法：
    manim -pql polar_decomposition.py Scene01_Intro
    manim -pql polar_decomposition.py Scene02_RightPolar
    manim -pql polar_decomposition.py Scene03_LeftVsRight
    manim -pql polar_decomposition.py Scene04_ThreeD
    manim -pql polar_decomposition.py Scene05_SVD_Teaser

场景顺序 (对应 Plan/polar_decomposition_manim_plan.yaml):
    1.  Scene01_Intro        引入与直觉 (The Hook)
    2.  Scene02_RightPolar   核心 2D 演示：A = U P，分步变形 + 精确重合
    3.  Scene03_LeftVsRight  左极分解 vs 右极分解
    4.  Scene04_ThreeD       升维拓展：三维球面 → 椭球 → 旋转
    5.  Scene05_SVD_Teaser   总结与延伸：极分解与 SVD 的联系

色彩约定（全局严格一致）：
    P  拉伸相关  →  ORANGE
    U  旋转相关  →  BLUE
    A  复合矩阵  →  WHITE
"""

from manim import *
from manim.utils.tex import TexTemplate
import numpy as np

config.background_color = "#0B0E14"
config.frame_width = 14.22
config.frame_height = 8.0


class CJKTexTemplate(TexTemplate):
    """支持中文标注的 LaTeX 模板（公式内 \text{旋转} 等）。"""

    def __init__(self):
        super().__init__()
        self.add_to_preamble(r"\usepackage[UTF8]{ctex}")


config.tex_template = CJKTexTemplate()

# ---- 颜色 ----
CN_FONT = "Microsoft YaHei"
C_P = ORANGE        # 拉伸（P 相关）
C_U = BLUE          # 旋转（U 相关）
C_A = WHITE         # 复合矩阵 A
C_ACCENT = YELLOW   # 强调

# ============================================================
# 数学常数（极分解）
# ============================================================
# 右极分解：A = U · P
# P = (AᵀA)^{1/2}，U = A·P^{-1}
A_MAT = np.array([[0.0, -1.0], [2.0, 0.0]])          # 逆时针旋转90° ∘ X轴拉伸2倍
P_MAT = np.array([[2.0, 0.0], [0.0, 1.0]])           # 半正定：X 轴拉伸 2 倍
U_MAT = np.array([[0.0, -1.0], [1.0, 0.0]])          # 正交：逆时针旋转 90°
UP_MAT = U_MAT @ P_MAT                                # 精确等于 A_MAT

# 左极分解：A = P' · U'
# P' = (A Aᵀ)^{1/2}，U' = A^{-1}·P'（沿旋转后的新坐标轴拉伸）
PL_MAT = np.array([[1.0, 0.0], [0.0, 2.0]])          # 半正定：Y 轴拉伸 2 倍
UL_MAT = np.array([[0.0, -1.0], [1.0, 0.0]])          # 正交：逆时针旋转 90°

# ---- 数学恒等式断言（代码级保证，绝不依赖视觉微调）----
assert np.allclose(U_MAT @ P_MAT, A_MAT), "右极分解 A = U·P 必须严格成立"
assert np.allclose(PL_MAT @ UL_MAT, A_MAT), "左极分解 A = P'·U' 必须严格成立"
assert np.allclose(P_MAT, P_MAT.T), "P 必须对称半正定"
assert np.allclose(PL_MAT, PL_MAT.T), "P' 必须对称半正定"
assert np.allclose(U_MAT @ U_MAT.T, np.eye(2)), "U 必须正交"
assert np.allclose(UL_MAT @ UL_MAT.T, np.eye(2)), "U' 必须正交"

# ---- 辅助函数 ----
def cn(text, size=28, color=C_A, weight=NORMAL, **kw):
    """中文字体文本（绝不用 MathTex 放中文）。"""
    return Text(text, font=CN_FONT, font_size=size, color=color, weight=weight, **kw)


def eq(tex, size=36, color=C_A, **kw):
    """LaTeX 公式。"""
    kw.pop("weight", None)
    return MathTex(tex, font_size=size, color=color, **kw)


def banner(text, color, size=24):
    """彩色圆角矩形标签。"""
    tag = cn(text, size=size, color="#0B0E14", weight=BOLD)
    box = RoundedRectangle(
        corner_radius=0.09,
        fill_color=color,
        fill_opacity=1,
        stroke_width=0,
        width=tag.width + 0.6,
        height=tag.height + 0.30,
    )
    tag.move_to(box)
    return VGroup(box, tag)


# 单位圆（用于显示拉伸 / 旋转的几何效果）
UNIT_CIRCLE = Circle(
    radius=1.0,
    color=C_ACCENT,
    stroke_width=3.5,
    fill_color=C_ACCENT,
    fill_opacity=0.10,
)


def lin2(mat):
    """二维线性变换（列向量右乘约定，与 apply_matrix 一致）。"""
    m = np.array(mat, dtype=float)

    def func(p):
        return np.array([m[0, 0] * p[0] + m[0, 1] * p[1],
                         m[1, 0] * p[0] + m[1, 1] * p[1], 0.0])

    return func


def lin3(mat):
    """三维线性变换（列向量右乘约定）。"""
    m = np.array(mat, dtype=float)

    def func(p):
        return np.array([m[0, 0] * p[0] + m[0, 1] * p[1] + m[0, 2] * p[2],
                         m[1, 0] * p[0] + m[1, 1] * p[1] + m[1, 2] * p[2],
                         m[2, 0] * p[0] + m[2, 1] * p[1] + m[2, 2] * p[2]])

    return func


# ============================================================
# Scene 1  引入与直觉 (The Hook)
# ============================================================
class Scene01_Intro(Scene):
    """The Hook：复杂变换 = 拉伸 + 旋转"""

    def construct(self):
        title = cn("矩阵的极分解", size=56, color=GOLD, weight=BOLD)
        sub = cn("任何线性变换，都只包含两步动作：拉伸 与 旋转",
                 size=30, color=GREY_A)
        title_group = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.wait(1.0)
        self.play(VGroup(title_group).animate.to_edge(UP, buff=0.4),
                  run_time=1.0)

        # 左侧：复杂变换 A 的几何效果（单步）
        left_panel = self._left_complex_transform()
        self.wait(2.0)

        # 右侧：A = U P 公式
        a_eq = eq("A", size=72, color=WHITE)
        up_eq = MathTex(
            "A=", r"\underbrace{U}_{\text{旋转}}",
            r"\cdot", r"\underbrace{P}_{\text{拉伸}}",
            font_size=72,
            substrings_to_isolate=["U", "P"],
        )
        # 给 U / P 上色
        for sub in up_eq.submobjects:
            if sub.get_tex_string() == "U":
                sub.set_color(C_U)
            elif sub.get_tex_string() == "P":
                sub.set_color(C_P)
        # underbrace 块也会上色（整体继承内部颜色）
        formula = VGroup(a_eq, up_eq).arrange(RIGHT, buff=0.6)
        formula.move_to(RIGHT * 3.5 + UP * 0.8)
        self.play(Write(formula), run_time=2.0)
        self.wait(1.5)

        # 底部结论
        note = cn("左图 = 一次复合；右图 = 把它拆成两小步",
                  size=28, color=GREY_A).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(note, shift=0.2 * UP))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)

    def _left_complex_transform(self):
        """左侧：A 作用于网格与单位圆。"""
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=6, y_length=6,
            background_line_style={"stroke_color": GREY_A,
                                   "stroke_opacity": 0.4,
                                   "stroke_width": 1},
            axis_config={"stroke_color": "#888888", "stroke_width": 1.5},
        ).shift(LEFT * 3.5)
        # 把原点对齐到屏幕坐标 (0,0) 处
        origin = plane.c2p(0, 0)
        plane.shift(LEFT * 3.5 - origin)
        label = cn("A 的一次作用", size=24, color=WHITE)
        label.next_to(plane, DOWN, buff=0.3)

        circle = UNIT_CIRCLE.copy().move_to(plane.get_center())
        self.play(FadeIn(plane, shift=DOWN * 0.5), run_time=1.2)
        self.play(Create(circle), run_time=1.2)
        self.play(FadeIn(label, shift=0.2 * UP))
        self.wait(0.8)

        # A 的矩阵作用（列向量右乘约定，精确计算）
        self.play(
            plane.animate.apply_function(lin2(A_MAT)),
            circle.animate.apply_function(lin2(A_MAT)),
            run_time=2.5,
        )
        self.wait(1.5)
        return VGroup(plane, circle, label)


# ============================================================
# Scene 2  核心 2D 演示：A = U P（右极分解）
# ============================================================
class Scene02_RightPolar(LinearTransformationScene):
    """核心 2D 演示：A = U P，分步变形 + 精确重合"""

    def __init__(self, **kwargs):
        super().__init__(
            include_foreground_plane=True,
            show_basis_vectors=True,
            background_plane_kwargs={
                "x_range": [-4, 4, 1],
                "y_range": [-4, 4, 1],
                "color": GREY_A,
                "axis_config": {"stroke_color": "#888888", "stroke_width": 1.5},
                "background_line_style": {
                    "stroke_color": GREY_A,
                    "stroke_opacity": 0.4,
                    "stroke_width": 1,
                },
            },
            foreground_plane_kwargs={
                "x_range": [-4, 4, 1],
                "y_range": [-4, 4, 1],
                "faded_line_ratio": 1,
                "background_line_style": {
                    "stroke_color": GREY_A,
                    "stroke_opacity": 0.35,
                    "stroke_width": 1,
                },
                "axis_config": {"stroke_color": "#888888", "stroke_width": 1.5},
            },
            i_hat_color=C_U,
            j_hat_color=C_P,
            leave_ghost_vectors=False,
            **kwargs,
        )

    def construct(self):
        self.camera.background_color = "#0B0E14"
        # 添加单位圆（直接入场景，随每一步矩阵精确变换）
        self.circle = UNIT_CIRCLE.copy()
        self.add(self.circle)

        # ---- 阶段 0：标题 ----
        title = cn("极分解  A = U P", size=36, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        sub = cn("拉伸 · 旋转 与矩阵乘法的不可交换性",
                 size=24, color=GREY_A).next_to(title, DOWN, buff=0.2)
        self.play(Write(title))
        self.play(FadeIn(sub, shift=0.2 * UP))
        self.wait(0.8)
        self.play(FadeOut(sub), run_time=0.5)

        # ---- 阶段 1：A 的直接效果 ----
        self._apply_step(A_MAT, "A 的直接效果", C_A)
        self.wait(1.0)

        # ---- 阶段 2：重置（A 的逆变换精确倒放回原状）----
        self._apply_step(np.linalg.inv(A_MAT), "时间倒流：重置", GREY)
        self.wait(1.0)

        # ---- 阶段 3：第一步 P（拉伸）----
        self._apply_step(P_MAT, "第一步：拉伸  P", C_P)
        self.wait(1.0)

        # ---- 阶段 4：第二步 U（旋转）----
        self._apply_step(U_MAT, "第二步：旋转  U", C_U)
        self.wait(1.0)

        # ---- 阶段 5：对比重合 ----
        self._stage_overlap()

        self.wait(2.0)

    def _apply_step(self, matrix, label_text, label_color):
        """对 plane / 单位圆 / 基向量精确施加线性变换（列向量右乘）。

        用 ApplyPointwiseFunction 逐点变换，拓扑结构不变，
        保证数学精确且无动画插值结构错配。
        """
        func = lin2(matrix)
        label = banner(label_text, label_color, size=22).to_edge(UP, buff=0.4)
        self.play(FadeIn(label, shift=0.2 * UP), run_time=0.6)
        self.wait(0.5)
        self.play(
            ApplyPointwiseFunction(func, self.plane),
            ApplyPointwiseFunction(func, self.circle),
            ApplyPointwiseFunction(func, self.i_hat),
            ApplyPointwiseFunction(func, self.j_hat),
            run_time=3.0,
        )
        self.wait(1.2)
        self.play(FadeOut(label), run_time=0.4)

    def _stage_overlap(self):
        """分屏对比：一步到位 vs 分步执行，精确重合。

        当前画面 = 分步执行 U·P 后的网格、单位圆与基向量。
        叠加层 = 对原始单位圆独立施加 A 的精确计算结果（lin2(A_MAT)）。
        由于 A = U·P 数值严格相等，两步像完全重合——绝无视觉手动微调。
        """
        caption = cn("分步执行  U·P   与   一步到位  A\n结果完全重合",
                     size=28, color=GOLD, weight=BOLD).to_edge(UP, buff=0.4)
        self.play(FadeIn(caption, shift=0.2 * UP), run_time=0.8)

        # 一步到位 A 的精确像（基于矩阵运算）
        a_plane = NumberPlane(
            x_range=[-4, 4, 1], y_range=[-4, 4, 1],
            background_line_style={
                "stroke_color": WHITE, "stroke_opacity": 0.35, "stroke_width": 1,
            },
            axis_config={"stroke_color": WHITE, "stroke_width": 1.5},
        )
        a_plane.apply_function(lin2(A_MAT))
        a_circle = UNIT_CIRCLE.copy()
        a_circle.apply_function(lin2(A_MAT))
        a_circle.set_style(stroke_color=WHITE, stroke_width=4.0,
                           fill_color=WHITE, fill_opacity=0.18)
        overlay = VGroup(a_plane, a_circle)

        self.play(FadeIn(overlay, run_time=1.2))
        self.wait(2.0)
        self.play(FadeOut(overlay), run_time=0.5)
        self.play(FadeOut(caption), run_time=0.4)


# ============================================================
# Scene 3  左极分解 vs 右极分解
# ============================================================
class Scene03_LeftVsRight(Scene):
    """左极分解 A = P'U'  与  右极分解 A = U P 的对比"""

    def construct(self):
        self._add_compare_header()

        # ---- 左半屏：右极分解  A = U P（先拉伸后旋转）----
        left_title = cn("右极分解  A = U P", size=28, color=WHITE, weight=BOLD)
        left_title.to_corner(UL, buff=0.6)
        self.play(Write(left_title))
        self.wait(0.6)

        # 右极分解的两步：拉伸（橙）→ 旋转（蓝）
        self._play_step(
            "先拉伸", "后旋转",
            C_P, C_U, P_MAT, U_MAT,
            shift=LEFT * 3.6,
        )
        self.wait(1.0)

        # ---- 右半屏：左极分解  A = P' U'（先旋转后拉伸）----
        right_title = cn("左极分解  A = P' U'", size=28, color=WHITE, weight=BOLD)
        right_title.to_corner(UR, buff=0.6)
        self.play(Write(right_title))
        self.wait(0.6)

        # 左极分解的两步：旋转（蓝）→ 沿旋转后方向拉伸（橙）
        self._play_step(
            "先旋转", "后拉伸",
            C_U, C_P, U_MAT, PL_MAT,
            shift=RIGHT * 3.6,
        )
        self.wait(1.5)

        # ---- 结论 ----
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        note = cn("矩阵乘法不可交换，但通过调整拉伸方向可达到等价效果",
                  size=30, color=GOLD, weight=BOLD).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(note, shift=0.2 * UP), run_time=0.8)
        self.wait(3.0)

    def _add_compare_header(self):
        header = cn("左极分解 vs 右极分解", size=36, color=GOLD, weight=BOLD)
        header.to_edge(UP, buff=0.3)
        self.play(Write(header))
        self.wait(0.8)
        return header

    def _play_step(self, step1, step2, c1, c2, m1, m2, shift=ORIGIN):
        """在 (标题, shift) 位置画网格 + 单位圆，依次播放两步变换。"""
        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=5, y_length=5,
            background_line_style={"stroke_color": GREY_A,
                                   "stroke_opacity": 0.4,
                                   "stroke_width": 1},
            axis_config={"stroke_color": "#888888", "stroke_width": 1.5},
        ).shift(shift + UP * 1.2)
        origin = plane.c2p(0, 0)
        plane.shift(shift + UP * 1.2 - origin)
        circle = UNIT_CIRCLE.copy().move_to(plane.get_center())

        self.play(FadeIn(plane), Create(circle), run_time=0.8)

        # 第一步
        s1 = banner(step1, c1, size=20).next_to(plane, DOWN, buff=0.3)
        self.play(FadeIn(s1, shift=0.2 * UP), run_time=0.5)
        self.play(
            plane.animate.apply_function(lin2(m1)),
            circle.animate.apply_function(lin2(m1)),
            run_time=2.0,
        )
        self.wait(0.5)
        self.play(FadeOut(s1), run_time=0.3)

        # 第二步
        s2 = banner(step2, c2, size=20).next_to(plane, DOWN, buff=0.3)
        self.play(FadeIn(s2, shift=0.2 * UP), run_time=0.5)
        self.play(
            plane.animate.apply_function(lin2(m2)),
            circle.animate.apply_function(lin2(m2)),
            run_time=2.0,
        )
        self.wait(0.5)
        self.play(FadeOut(s2), run_time=0.3)
        # 保留当前画面，供左右对比
        self.wait(1.2)


# ============================================================
# Scene 4  3D 演示
# ============================================================
class Scene04_ThreeD(ThreeDScene):
    """三维空间中的极分解"""

    def construct(self):
        self.camera.background_color = "#0B0E14"
        self.set_camera_orientation(phi=70 * DEGREES, theta=-60 * DEGREES)

        # ---- 3D 矩阵（沿 x 轴拉伸2倍，y 轴 0.5 倍）----
        P3 = np.diag([2.0, 0.5, 1.0])
        # 绕 z 轴旋转 45°
        th = np.pi / 4
        R3 = np.array([[np.cos(th), -np.sin(th), 0.0],
                       [np.sin(th), np.cos(th), 0.0],
                       [0.0, 0.0, 1.0]])
        A3 = R3 @ P3

        title = cn("三维空间中的极分解", size=36, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(title)
        self.play(FadeIn(title, shift=0.2 * UP))
        self.wait(0.8)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=6,
            axis_config={"stroke_color": GREY_A, "stroke_width": 1.5,
                         "color": GREY_A},
        )
        self.play(Create(axes), run_time=1.5)

        sphere = Sphere(
            radius=1.0, resolution=(16, 16),
            fill_opacity=0.25, fill_color=C_ACCENT,
            stroke_color=C_ACCENT, stroke_width=1.0,
        )
        self.play(Create(sphere), run_time=1.5)
        self.wait(1.0)

        # ---- 阶段 1：A 的一次作用（球 → 倾斜椭球）----
        label_a = cn("A 的一次作用", size=26, color=WHITE, weight=BOLD)
        label_a.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(label_a)
        self.play(FadeIn(label_a, shift=0.2 * UP))
        self.play(sphere.animate.apply_function(lin3(A3)), run_time=2.5)
        self.wait(1.5)
        self.remove_fixed_in_frame_mobjects(label_a)
        self.play(FadeOut(label_a), run_time=0.4)

        # ---- 阶段 2：重置（逆变换精确倒放回球）----
        label_reset = cn("重置（时间倒流）", size=26, color=GREY, weight=BOLD)
        label_reset.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(label_reset)
        self.play(FadeIn(label_reset, shift=0.2 * UP))
        self.play(sphere.animate.apply_function(lin3(np.linalg.inv(A3))), run_time=2.0)
        self.wait(1.0)
        self.remove_fixed_in_frame_mobjects(label_reset)
        self.play(FadeOut(label_reset), run_time=0.4)

        # ---- 阶段 3：分步拆解回放：先 P（拉伸成正交椭球）----
        label_p = cn("先 P：拉伸成椭球", size=26, color=C_P, weight=BOLD)
        label_p.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(label_p)
        self.play(FadeIn(label_p, shift=0.2 * UP))
        self.play(sphere.animate.apply_function(lin3(P3)), run_time=2.5)
        self.wait(1.2)
        self.remove_fixed_in_frame_mobjects(label_p)
        self.play(FadeOut(label_p), run_time=0.4)

        # ---- 阶段 4：再 U（刚体旋转至目标位形）----
        label_u = cn("再 U：刚体旋转", size=26, color=C_U, weight=BOLD)
        label_u.to_edge(UP, buff=0.4)
        self.add_fixed_in_frame_mobjects(label_u)
        self.play(FadeIn(label_u, shift=0.2 * UP))
        self.play(sphere.animate.apply_function(lin3(R3)), run_time=2.5)
        self.wait(1.2)
        self.remove_fixed_in_frame_mobjects(label_u)
        self.play(FadeOut(label_u), run_time=0.4)
        self.wait(1.5)

        note = cn("A = U · P   拉伸成椭球 → 刚体旋转至目标位形",
                  size=26, color=GREY_A).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(note)
        self.play(FadeIn(note, shift=0.2 * UP))
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


# ============================================================
# Scene 5  总结与延伸：SVD
# ============================================================
class Scene05_SVD_Teaser(Scene):
    """总结 + 引出 SVD 公式"""

    def construct(self):
        # ---- 总结 ----
        title = cn("极分解的意义", size=40, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.4)
        self.play(Write(title))
        self.wait(1.0)

        points = VGroup(
            cn("图形学：旋转 + 缩放 = 刚体运动 × 形变", size=28),
            cn("连续介质力学：形变梯度的极分解", size=28),
            cn("任意可逆矩阵都能写成  U·P", size=28),
        ).arrange(DOWN, buff=0.5)
        points.next_to(title, DOWN, buff=1.0)
        for p in points:
            self.play(FadeIn(p, shift=0.2 * UP))
            self.wait(0.6)
        self.wait(1.0)

        # ---- P 自身的分解：P = V Σ Vᵀ ----
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        p_formula = MathTex(
            r"P = V \Sigma V^\top",
            font_size=56, color=C_P,
            substrings_to_isolate=[r"V", r"\Sigma", r"V^\top"],
        )
        # 给 V 与 Σ 上色
        for sub in p_formula.submobjects:
            if sub.get_tex_string() == "V" or sub.get_tex_string() == r"V^\top":
                sub.set_color(C_U)
            elif sub.get_tex_string() == r"\Sigma":
                sub.set_color(C_ACCENT)
        p_formula.to_edge(UP, buff=1.0)
        self.play(Write(p_formula), run_time=2.0)
        p_note = cn("P 是对称半正定矩阵：可对角化", size=28, color=GREY_A)
        p_note.next_to(p_formula, DOWN, buff=0.5)
        self.play(FadeIn(p_note, shift=0.2 * UP))
        self.wait(1.5)

        # ---- SVD 彩蛋 ----
        svd = MathTex(
            r"A = U \Sigma V^\top",
            font_size=64, color=C_A,
            substrings_to_isolate=["U", r"\Sigma", r"V^\top"],
        )
        for sub in svd.submobjects:
            if sub.get_tex_string() == "U":
                sub.set_color(C_U)
            elif sub.get_tex_string() == r"V^\top":
                sub.set_color(C_U)
            elif sub.get_tex_string() == r"\Sigma":
                sub.set_color(C_ACCENT)
        svd.to_edge(DOWN, buff=1.0)
        self.play(Write(svd), run_time=2.0)
        svd_note = cn("SVD：极分解的推广（下期预告）", size=28, color=GREY_A)
        svd_note.next_to(svd, DOWN, buff=0.4)
        self.play(FadeIn(svd_note, shift=0.2 * UP))
        self.wait(3.0)
