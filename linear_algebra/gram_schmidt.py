# -*- coding: utf-8 -*-
r"""施密特正交化 (Gram-Schmidt Orthogonalization) —— Manim 动画

用法：
    manim -qh gram_schmidt.py Scene1Introduction    # 单场景
    python gram_schmidt.py                           # 全场景高清+合并
    python gram_schmidt.py --low                     # 低质量预览
    python gram_schmidt.py --scene 3                 # 只渲染指定场景

场景:
    1. Scene1Introduction       ~10s  概念引入
    2. Scene2InitialSetup       ~15s  初始状态设定
    3. Scene3Step1Foundation    ~10s  第一步：确立地基
    4. Scene4Step2Projection    ~20s  第二步：几何投影
    5. Scene5Step3Subtract      ~20s  第三步：剔除平行分量
    6. Scene6Step4Normalize     ~15s  第四步：标准单位化
    7. Scene7Summary            ~15s  总结与升华
    8. Scene8ThreeDimExample    ~20s  三维推广实例
    总时长:                    ~125s
"""
from manim import *
import numpy as np
import subprocess, sys
from pathlib import Path

config.pixel_height = 1080
config.pixel_width  = 1920
config.frame_rate   = 60

# ═══════════════════════════════════════════
# 风格常量
# ═══════════════════════════════════════════
C_BG     = "#333333"
C_U1     = YELLOW
C_U2     = LIGHT_BROWN
C_V1     = RED_A
C_V2     = GREEN_C
C_V3     = TEAL
C_PROJ   = GRAY
C_AUX    = WHITE
C_CIRCLE = BLUE_B
C_GOLD   = "#F2C14E"
C_HINT   = GREY

CN_FONT = "Microsoft YaHei"


# ═══════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════
def cn(text, size=30, color=WHITE, weight=NORMAL, **kw):
    return Text(text, font=CN_FONT, font_size=size,
                color=color, weight=weight, **kw)


def eqf(tex, size=36, color=WHITE, **kw):
    return MathTex(tex, font_size=size, color=color, **kw)


# ═══════════════════════════════════════════
# 共享几何数据 — 二维
# ═══════════════════════════════════════════
K = 0.85
U1 = np.array([3.0, 1.0, 0.0])
U2 = np.array([1.0, 3.0, 0.0])
V1 = U1.copy()
_D  = float(np.dot(U2, V1)) / float(np.dot(V1, V1))
P1  = _D * V1
V2 = U2 - P1
E1 = V1 / np.linalg.norm(V1)
E2 = V2 / np.linalg.norm(V2)

# 三维数据
U1_3 = np.array([2.0, 1.0, 0.5])
U2_3 = np.array([0.5, 3.0, 1.0])
U3_3 = np.array([1.0, 1.0, 3.0])
V1_3 = U1_3.copy()
_D31 = float(np.dot(U2_3, V1_3)) / float(np.dot(V1_3, V1_3))
V2_3 = U2_3 - _D31 * V1_3
_D32a = float(np.dot(U3_3, V1_3)) / float(np.dot(V1_3, V1_3))
_D32b = float(np.dot(U3_3, V2_3)) / float(np.dot(V2_3, V2_3))
V3_3 = U3_3 - _D32a * V1_3 - _D32b * V2_3
K3 = 0.60


# ═══════════════════════════════════════════
# 公共工具
# ═══════════════════════════════════════════
def make_plane():
    p = NumberPlane(
        x_range=[-2, 5, 1], y_range=[-2, 5, 1],
        x_length=6.5 * K, y_length=6.5 * K,
        background_line_style={
            "stroke_color": GREY, "stroke_opacity": 0.3, "stroke_width": 1},
        axis_config={"stroke_color": "#888888", "stroke_width": 1.5},
    )
    p.shift(-p.c2p(0, 0))
    return p


def vec(data, color, k=K):
    return Vector(data * k, color=color, buff=0,
                  max_tip_length_to_length_ratio=0.12)


def vlab(tex, color, data, direction, buff=0.2, size=40, k=K):
    return MathTex(tex, color=color, font_size=size)\
        .next_to(data * k, direction, buff=buff)


def span_of(v, color, k=K):
    return Line(v * k * (-0.3), v * k * 1.6,
                color=color, stroke_opacity=0.25, stroke_width=3)


def step_title(text):
    t = cn(text, size=38, color=WHITE, weight=BOLD)
    t.to_edge(UP, buff=0.4)
    return t


# ═══════════════════════════════════════════
# Scene 1 — 概念引入  ~10s
# ═══════════════════════════════════════════
class Scene1Introduction(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        title_cn = cn("施密特正交化", size=54, color=WHITE, weight=BOLD)
        title_en = cn("Gram-Schmidt Orthogonalization", size=32, color=C_HINT)
        title = VGroup(title_cn, title_en).arrange(DOWN, buff=0.25).move_to(UP * 0.5)

        self.play(Write(title_cn), run_time=1.0)
        self.play(FadeIn(title_en, shift=0.2 * UP), run_time=0.6)
        self.wait(0.4)

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1],
            x_length=7.0, y_length=7.0,
            background_line_style={
                "stroke_color": GREY, "stroke_opacity": 0.4, "stroke_width": 1},
            axis_config={"stroke_color": "#666666", "stroke_width": 1.5},
        ).move_to(DOWN * 0.3)

        skew_lab = cn("杂乱的非正交网格", size=24, color="#FF9999")
        skew_lab.next_to(plane, DOWN, buff=0.3)

        self.play(Create(plane), FadeIn(skew_lab, shift=0.15 * UP), run_time=1.5)
        self.wait(1.0)

        inv = np.array([[3, -1], [-1, 3]]) / 8.0
        self.play(ApplyMatrix(inv, plane), run_time=2.5)
        self.wait(0.5)

        orth_lab = cn("标准正交网格", size=24, color="#66D19E")
        orth_lab.next_to(plane, DOWN, buff=0.3)
        self.play(Transform(skew_lab, orth_lab), run_time=1.0)
        self.wait(0.5)

        self.play(FadeOut(VGroup(title, plane, skew_lab)), run_time=1.0)


# ═══════════════════════════════════════════
# Scene 2 — 初始状态设定  ~15s
# ═══════════════════════════════════════════
class Scene2InitialSetup(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        plane = make_plane()
        self.play(Create(plane), run_time=1.5)

        vu1 = vec(U1, C_U1); lu1 = vlab(r"\mathbf{u}_1", C_U1, U1, RIGHT)
        vu2 = vec(U2, C_U2); lu2 = vlab(r"\mathbf{u}_2", C_U2, U2, UP)

        self.play(GrowArrow(vu1), Write(lu1), run_time=1.5)
        self.play(GrowArrow(vu2), Write(lu2), run_time=1.5)
        self.wait(1.0)

        a1 = Line(ORIGIN, U1 * K * 0.55)
        a2 = Line(ORIGIN, U2 * K * 0.55)
        angle = Angle(a1, a2, radius=0.9, color=C_AUX)
        ang_lab = MathTex(r"\theta \neq 90^\circ", color=C_AUX, font_size=36)
        ang_lab.next_to(angle, RIGHT, buff=0.25)

        self.play(Create(angle), Write(ang_lab), run_time=2.0)
        self.wait(2.0)

        hint = cn("两个向量线性无关，但夹角不是 90°", size=26, color=C_HINT)
        hint.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(hint, shift=0.15 * UP), run_time=0.6)
        self.wait(3.4)

        self.play(FadeOut(VGroup(plane, vu1, vu2, lu1, lu2,
                                  angle, ang_lab, hint)), run_time=1.0)


# ═══════════════════════════════════════════
# Scene 3 — 第一步：确立地基  ~10s
# ═══════════════════════════════════════════
class Scene3Step1Foundation(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        plane = make_plane(); self.add(plane)

        vu1 = vec(U1, C_U1); lu1 = vlab(r"\mathbf{u}_1", C_U1, U1, RIGHT)
        vu2 = vec(U2, C_U2); lu2 = vlab(r"\mathbf{u}_2", C_U2, U2, UP)
        self.add(vu1, vu2, lu1, lu2)

        self.wait(0.3)

        st = step_title("第一步：确立地基")
        self.play(Write(st), run_time=0.8)
        self.wait(0.4)

        vv1 = vec(V1, C_V1); lv1 = vlab(r"\mathbf{v}_1 = \mathbf{u}_1", C_V1, V1, RIGHT)
        self.play(ReplacementTransform(vu1.copy(), vv1),
                  Transform(lu1.copy(), lv1),
                  vu1.animate.set_opacity(0.3),
                  lu1.animate.set_opacity(0.3),
                  run_time=2.0)
        self.wait(0.5)

        sp  = span_of(V1, C_V1)
        spl = MathTex(r"\mathrm{span}\{\mathbf{v}_1\}",
                      color=C_V1, font_size=30).next_to(sp.get_end(), RIGHT, buff=0.15)
        self.play(Create(sp), Write(spl), run_time=1.2)

        fm = eqf(r"\mathbf{v}_1 = \mathbf{u}_1", size=40, color=C_V1)
        fm.to_corner(UR, buff=0.5)
        self.play(Write(fm), run_time=0.8)
        self.wait(2.5)

        self.play(FadeOut(VGroup(plane, vu1, vu2, vv1, lu1, lu2, lv1,
                                  sp, spl, fm, st)), run_time=1.0)


# ═══════════════════════════════════════════
# Scene 4 — 第二步：几何投影  ~20s
# ═══════════════════════════════════════════
class Scene4Step2Projection(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        plane = make_plane(); self.add(plane)
        vu1 = vec(U1, C_U1).set_opacity(0.3); self.add(vu1)

        vv1 = vec(V1, C_V1); lv1 = vlab(r"\mathbf{v}_1", C_V1, V1, RIGHT)
        self.add(vv1, lv1)
        sp = span_of(V1, C_V1); self.add(sp)

        vu2 = vec(U2, C_U2); lu2 = vlab(r"\mathbf{u}_2", C_U2, U2, UP)
        self.add(vu2, lu2)

        st = step_title("第二步：几何投影")
        self.play(Write(st), run_time=0.8)
        self.wait(0.7)

        pt, ut = P1 * K, U2 * K
        dash = DashedLine(pt, ut, color=C_AUX, dash_length=0.12, stroke_width=2)
        self.play(Create(dash), run_time=1.5)
        ra = RightAngle(Line(pt, ut), Line(pt, ORIGIN),
                        length=0.25, color=C_AUX)
        self.play(Create(ra), run_time=0.5)
        self.wait(0.5)

        vp = vec(P1, C_PROJ)
        pl = MathTex(r"\mathrm{proj}_{\mathbf{v}_1}(\mathbf{u}_2)",
                     color=C_PROJ, font_size=34)
        pl.next_to(P1 * K * 0.5, DOWN, buff=0.3)
        self.play(GrowArrow(vp), Write(pl), run_time=2.0)
        self.wait(0.5)

        fm = eqf(r"\mathrm{proj}_{\mathbf{v}_1}(\mathbf{u}_2)"
                 r"=\frac{\mathbf{u}_2\cdot\mathbf{v}_1}"
                 r"{\mathbf{v}_1\cdot\mathbf{v}_1}\mathbf{v}_1",
                 size=34, color=C_PROJ)
        fm.to_corner(UR, buff=0.4)
        self.play(Write(fm), run_time=1.5)
        self.wait(9.5)

        self.play(FadeOut(VGroup(plane, vu1, vv1, vu2, lv1, lu2,
                                  sp, dash, ra, vp, pl, fm, st)), run_time=1.0)


# ═══════════════════════════════════════════
# Scene 5 — 第三步：剔除平行分量  ~20s
# ═══════════════════════════════════════════
class Scene5Step3Subtract(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        plane = make_plane(); self.add(plane)
        vv1 = vec(V1, C_V1); lv1 = vlab(r"\mathbf{v}_1", C_V1, V1, RIGHT)
        self.add(vv1, lv1)
        sp = span_of(V1, C_V1); self.add(sp)

        vu2 = vec(U2, C_U2); lu2 = vlab(r"\mathbf{u}_2", C_U2, U2, UP)
        self.add(vu2, lu2)

        vp = vec(P1, C_PROJ)
        pl = MathTex(r"\mathrm{proj}", color=C_PROJ, font_size=30)
        pl.next_to(P1 * K * 0.55, DOWN, buff=0.2)
        self.add(vp, pl)

        pt, ut = P1 * K, U2 * K
        dash = DashedLine(pt, ut, color=C_AUX, dash_length=0.12, stroke_width=2)
        self.add(dash)

        self.wait(0.3)

        st = step_title("第三步：剔除平行分量")
        self.play(Write(st), run_time=0.8)
        self.wait(0.4)

        self.play(dash.animate.set_color(C_V2).set_stroke(width=4), run_time=1.5)
        self.wait(0.5)

        vv2 = vec(V2, C_V2); lv2 = vlab(r"\mathbf{v}_2", C_V2, V2, LEFT)
        self.play(dash.animate.scale(0.001, about_point=pt), run_time=0.3)
        self.remove(dash)
        self.play(GrowArrow(vv2), Write(lv2), run_time=1.5)
        self.wait(0.5)

        ra = RightAngle(Line(ORIGIN, V1 * K * 0.45),
                        Line(ORIGIN, V2 * K * 0.45),
                        length=0.35, color=C_AUX)
        self.play(Create(ra), run_time=0.8)
        self.play(Flash(ra, color=C_AUX, line_length=0.4, flash_radius=0.5),
                  run_time=0.7)
        self.wait(0.5)

        fm = eqf(r"\mathbf{v}_2 = \mathbf{u}_2 - "
                 r"\mathrm{proj}_{\mathbf{v}_1}(\mathbf{u}_2)",
                 size=36, color=C_V2)
        fm.to_corner(UR, buff=0.4)
        self.play(Write(fm), run_time=1.5)
        self.wait(7.0)

        b1 = SurroundingRectangle(VGroup(vv1, lv1), color=C_V1, buff=0.15, stroke_width=2)
        b2 = SurroundingRectangle(VGroup(vv2, lv2), color=C_V2, buff=0.15, stroke_width=2)
        self.play(Create(b1), Create(b2), run_time=1.0)
        self.wait(2.5)

        self.play(FadeOut(VGroup(plane, vv1, vv2, vu2, vp,
                                  lv1, lv2, lu2, pl, sp, ra,
                                  fm, st, b1, b2)), run_time=1.0)


# ═══════════════════════════════════════════
# Scene 6 — 第四步：标准单位化  ~15s
# ═══════════════════════════════════════════
class Scene6Step4Normalize(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        plane = make_plane(); self.add(plane)
        vv1 = vec(V1, C_V1); lv1 = vlab(r"\mathbf{v}_1", C_V1, V1, RIGHT)
        vv2 = vec(V2, C_V2); lv2 = vlab(r"\mathbf{v}_2", C_V2, V2, LEFT)
        self.add(vv1, vv2, lv1, lv2)

        ra = RightAngle(Line(ORIGIN, V1 * K * 0.45),
                        Line(ORIGIN, V2 * K * 0.45),
                        length=0.35, color=C_AUX)
        self.add(ra)

        self.wait(0.3)

        st = step_title("第四步：标准单位化")
        self.play(Write(st), run_time=0.8)
        self.wait(0.5)

        circle = Circle(radius=K, color=C_CIRCLE, stroke_width=2, stroke_opacity=0.6)
        self.play(Create(circle), run_time=1.5)
        self.wait(0.5)

        n1, n2 = float(np.linalg.norm(V1)), float(np.linalg.norm(V2))
        le1 = vlab(r"\mathbf{e}_1", C_V1, E1, RIGHT)
        le2 = vlab(r"\mathbf{e}_2", C_V2, E2, LEFT)
        self.play(vv1.animate.scale(1.0 / n1, about_point=ORIGIN),
                  vv2.animate.scale(1.0 / n2, about_point=ORIGIN),
                  Transform(lv1, le1), Transform(lv2, le2),
                  run_time=3.0)
        self.wait(1.0)

        de1 = Dot(E1 * K, color=C_V1, radius=0.06)
        de2 = Dot(E2 * K, color=C_V2, radius=0.06)
        self.play(Create(de1), Create(de2), run_time=1.0)
        self.wait(0.5)

        fm = eqf(r"\mathbf{e}_i = \frac{\mathbf{v}_i}{\|\mathbf{v}_i\|}",
                 size=40, color=WHITE)
        fm.to_corner(UR, buff=0.4)
        self.play(Write(fm), run_time=1.0)
        self.wait(2.0)

        perfect = cn("标准正交基：两两垂直，长度均为 1", size=26, color=C_CIRCLE)
        perfect.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(perfect, shift=0.15 * UP), run_time=0.6)
        self.wait(1.3)

        self.play(FadeOut(VGroup(plane, vv1, vv2, lv1, lv2, ra,
                                  circle, de1, de2, fm, st, perfect)),
                  run_time=1.0)


# ═══════════════════════════════════════════
# Scene 7 — 总结与升华  ~15s
# 分两页：第一页 2D 推导回顾，第二页通用公式
# ═══════════════════════════════════════════
class Scene7Summary(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        r = 2.5
        bg = VGroup(
            Line(LEFT * r, RIGHT * r,
                 color=GREY, stroke_opacity=0.10, stroke_width=1.5),
            Line(DOWN * r, UP * r,
                 color=GREY, stroke_opacity=0.10, stroke_width=1.5),
            Square(side_length=r * 2,
                   color=GREY, stroke_opacity=0.08, stroke_width=1.5),
        )
        bg.move_to(ORIGIN)
        bg.add_updater(lambda m, dt: m.rotate(0.25 * dt, about_point=ORIGIN))
        self.add(bg)

        # ===== 第一页：2D 推导回顾 =====
        title = cn("施密特正交化：几何本质", size=40, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        formulas_2d = VGroup(
            eqf(r"\mathbf{v}_1 = \mathbf{u}_1", size=38),
            eqf(r"\mathbf{v}_2 = \mathbf{u}_2 - "
                r"\mathrm{proj}_{\mathbf{v}_1}(\mathbf{u}_2)", size=38),
            eqf(r"\mathbf{e}_i = \frac{\mathbf{v}_i}{\|\mathbf{v}_i\|}", size=38),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        formulas_2d.move_to(UP * 0.3)

        for f in formulas_2d:
            self.play(Write(f), run_time=1.0)

        note_2d = cn("二维：保留了「投影 → 剥离 → 归一化」三步", size=26, color=C_HINT)
        note_2d.next_to(formulas_2d, DOWN, buff=0.8)
        self.play(FadeIn(note_2d, shift=0.15 * UP), run_time=0.8)
        self.wait(2.5)

        # ---- 翻页 ----
        self.play(FadeOut(VGroup(formulas_2d, note_2d)), run_time=0.6)

        # ===== 第二页：通用公式 - 保持字号 38 =====
        formulas_n = VGroup(
            eqf(r"\mathbf{v}_1 = \mathbf{u}_1", size=38),
            eqf(r"\mathbf{v}_k = \mathbf{u}_k - "
                r"\sum_{i=1}^{k-1}"
                r"\frac{\mathbf{u}_k\cdot\mathbf{v}_i}"
                r"{\mathbf{v}_i\cdot\mathbf{v}_i}\,\mathbf{v}_i",
                size=38),
            eqf(r"\mathbf{e}_i = \frac{\mathbf{v}_i}{\|\mathbf{v}_i\|}", size=38),
        ).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        formulas_n.move_to(UP * 0.3)

        for f in formulas_n:
            self.play(Write(f), run_time=1.0)

        # 核心步骤标注
        steps = VGroup(
            cn("① 选定地基", size=26, color=C_V1),
            cn("② 投影 → 减去平行分量", size=26, color=C_PROJ),
            cn("③ 迭代重复", size=26, color=C_V2),
            cn("④ 归一化", size=26, color=C_CIRCLE),
        ).arrange(RIGHT, buff=0.6)
        steps.next_to(formulas_n, DOWN, buff=0.7)

        note_n = cn("对任意 k ≤ n 迭代，从二维到 n 维完全通用", size=26, color=C_HINT)
        note_n.next_to(steps, DOWN, buff=0.35)

        self.play(FadeIn(steps, shift=0.15 * UP), run_time=1.0)
        self.play(FadeIn(note_n, shift=0.15 * UP), run_time=0.8)
        self.wait(2.0)

        # ---- 结语 ----
        closing = cn("「投影并剥离」—— 适用于任意维空间",
                     size=28, color=C_GOLD, weight=BOLD)
        closing.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(closing, shift=0.15 * UP), run_time=1.0)
        self.wait(1.0)

        # ---- 致谢 ----
        thanks = cn("感谢观看", size=48, color=WHITE, weight=BOLD)
        self.play(FadeOut(VGroup(title, formulas_n, note_n)), run_time=0.6)
        self.play(Write(thanks), run_time=1.0)
        self.wait(0.5)

        bg.clear_updaters()
        self.play(FadeOut(VGroup(thanks, closing, bg)), run_time=0.8)


# ═══════════════════════════════════════════
# Scene 8 — 三维推广实例  ~20s
# ═══════════════════════════════════════════
class Scene8ThreeDimExample(ThreeDScene):
    def construct(self):
        self.camera.background_color = C_BG
        self.set_camera_orientation(phi=70 * DEGREES, theta=-50 * DEGREES)

        # ---- 顶部标题 ----
        title = cn("三维推广：Gram-Schmidt 正交化", size=36, color=WHITE, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title)

        # ---- 底部字幕区 ----
        def show_sub(text, color=WHITE):
            sub = cn(text, size=28, color=color)
            sub.to_edge(DOWN, buff=0.55)
            self.add_fixed_in_frame_mobjects(sub)
            return sub

        def swap_sub(old, text, color=WHITE):
            new = cn(text, size=28, color=color)
            new.to_edge(DOWN, buff=0.55)
            self.add_fixed_in_frame_mobjects(new)
            if old:
                self.remove_fixed_in_frame_mobjects(old)
            return new

        # ---- 三维坐标轴 ----
        axes = ThreeDAxes(
            x_range=[-2, 4], y_range=[-2, 4], z_range=[-2, 4],
            x_length=5.5, y_length=5.5, z_length=5.5,
            axis_config={"stroke_color": "#888888", "stroke_width": 1.5},
        )
        self.play(Create(axes), run_time=1.5)

        # ---- 三个原始向量：Line3D（粗线）+ Dot3D（端点球，替代箭头尖） ----
        T = 0.04  # 线宽——够粗才看得清

        vu1 = Line3D(ORIGIN, U1_3 * K3, color=C_U1, stroke_width=T)
        vu2 = Line3D(ORIGIN, U2_3 * K3, color=C_U2, stroke_width=T)
        vu3 = Line3D(ORIGIN, U3_3 * K3, color=PURPLE, stroke_width=T)
        du1 = Dot3D(point=U1_3 * K3, radius=0.08, color=C_U1)
        du2 = Dot3D(point=U2_3 * K3, radius=0.08, color=C_U2)
        du3 = Dot3D(point=U3_3 * K3, radius=0.08, color=PURPLE)
        ug1 = VGroup(vu1, du1); ug2 = VGroup(vu2, du2); ug3 = VGroup(vu3, du3)

        sub1 = show_sub("给定三个线性无关向量：u₁(黄) · u₂(棕) · u₃(紫)")

        self.play(Create(vu1), Create(vu2), Create(vu3),
                  FadeIn(du1), FadeIn(du2), FadeIn(du3),
                  run_time=3.0)
        self.wait(1.5)

        # ---- 正交化 ----
        vv1 = Line3D(ORIGIN, V1_3 * K3, color=C_V1, stroke_width=T)
        vv2 = Line3D(ORIGIN, V2_3 * K3, color=C_V2, stroke_width=T)
        vv3 = Line3D(ORIGIN, V3_3 * K3, color=C_V3, stroke_width=T)
        dv1 = Dot3D(point=V1_3 * K3, radius=0.08, color=C_V1)
        dv2 = Dot3D(point=V2_3 * K3, radius=0.08, color=C_V2)
        dv3 = Dot3D(point=V3_3 * K3, radius=0.08, color=C_V3)
        vg1 = VGroup(vv1, dv1); vg2 = VGroup(vv2, dv2); vg3 = VGroup(vv3, dv3)

        self.play(
            vu1.animate.set_opacity(0.12), vu2.animate.set_opacity(0.12), vu3.animate.set_opacity(0.12),
            du1.animate.set_opacity(0.12), du2.animate.set_opacity(0.12), du3.animate.set_opacity(0.12),
            Create(vv1), Create(vv2), Create(vv3),
            FadeIn(dv1), FadeIn(dv2), FadeIn(dv3),
            run_time=2.5,
        )

        sub1 = swap_sub(sub1, "减去投影分量 → v₁, v₂, v₃ 两两正交", C_V1)
        self.wait(2.0)

        # 正交向量之间画直角符号似的：端点间连线对比
        # 轻量旋转一下让观众看到夹角
        self.move_camera(phi=55 * DEGREES, theta=-30 * DEGREES, run_time=2.0)
        self.wait(1.0)

        # ---- 归一化 ----
        n1, n2, n3 = [float(np.linalg.norm(v)) for v in [V1_3, V2_3, V3_3]]

        self.play(
            vg1.animate.scale(1.0 / n1, about_point=ORIGIN).set_color(C_CIRCLE),
            vg2.animate.scale(1.0 / n2, about_point=ORIGIN).set_color(C_CIRCLE),
            vg3.animate.scale(1.0 / n3, about_point=ORIGIN).set_color(C_CIRCLE),
            run_time=3.5,
        )

        sub1 = swap_sub(sub1, "归一化 → 标准正交基 e₁, e₂, e₃（长度 = 1）", C_GOLD)
        self.wait(2.0)

        # ---- 缓慢旋转展示三维正交结构 ----
        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(5.0)
        self.stop_ambient_camera_rotation()

        sub1 = swap_sub(sub1, "「投影并剥离」—— 二维到三维完全通用", C_GOLD)
        self.wait(3.5)

        self.play(FadeOut(VGroup(axes, vu1, vu2, vu3, du1, du2, du3,
                                  vv1, vv2, vv3, dv1, dv2, dv3,
                                  title, sub1)),
                  run_time=1.0)


# ═══════════════════════════════════════════════════════════════
# 渲染 & 合并（单文件自包含）
# ═══════════════════════════════════════════════════════════════
SCENES = [
    "Scene1Introduction",
    "Scene2InitialSetup",
    "Scene3Step1Foundation",
    "Scene4Step2Projection",
    "Scene5Step3Subtract",
    "Scene6Step4Normalize",
    "Scene7Summary",
]

QUALITY = {
    "low":  ("-ql", "480p15"),
    "high": ("-qh", "1080p60"),
}


def run_manim(scene, qflag):
    cmd = ["manim", qflag, "--disable_caching", "gram_schmidt.py", scene]
    print(f"\n>> {scene}  [{qflag}]")
    return subprocess.run(cmd, capture_output=False).returncode == 0


def mp4_path(scene, subdir):
    return Path(f"media/videos/gram_schmidt/{subdir}/{scene}.mp4")


def concat(paths, out):
    lst = Path("media/temp/concat_gs.txt")
    lst.parent.mkdir(parents=True, exist_ok=True)
    lst.write_text("\n".join(f"file '{p.resolve()}'" for p in paths),
                   encoding="utf-8")
    r = subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c", "copy", str(out)],
        capture_output=True, text=True)
    if r.returncode != 0:
        print("FFmpeg error:", r.stderr[-400:])
    return r.returncode == 0


if __name__ == "__main__":
    args = sys.argv[1:]
    preset   = "low" if "--low" in args else "high"
    only_idx = None
    if "--scene" in args:
        only_idx = int(args[args.index("--scene") + 1]) - 1

    qflag, subdir = QUALITY[preset]
    print(f"质量: {preset} ({subdir})")

    targets = [SCENES[only_idx]] if only_idx is not None else SCENES
    failed = []
    for s in targets:
        ok = run_manim(s, qflag)
        (lambda: None) if ok else failed.append(s)
        print(f"  {'[OK]' if ok else 'X FAILED'}  {s}")

    if failed:
        print(f"\n失败: {failed}")
    elif only_idx is None:
        paths = [mp4_path(s, subdir) for s in SCENES]
        miss  = [p for p in paths if not p.exists()]
        if miss:
            print(f"缺少: {miss}")
        else:
            out = Path(f"gram_schmidt_{preset}.mp4")
            if concat(paths, out):
                mb = out.stat().st_size / 1_048_576
                print(f"\n[DONE] {out}  ({mb:.1f} MB)")

    print("\n时长:")
    total = 0.0
    for s in SCENES:
        mp4 = mp4_path(s, subdir)
        if mp4.exists():
            r = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(mp4)],
                capture_output=True, text=True)
            d = float(r.stdout.strip() or 0)
            total += d
            print(f"  {s:<30} {d:5.1f}s")
    m, sec = divmod(int(total), 60)
    print(f"  总计: {m}分{sec:02d}s ({total:.0f}s)")
