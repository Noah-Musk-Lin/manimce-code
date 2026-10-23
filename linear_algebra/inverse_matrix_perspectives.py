# -*- coding: utf-8 -*-
"""
逆矩阵的多维透视 —— 基于《Inverse_Matrix_Advanced_Algebra_Synthesis.md》的系列视频

全片贯穿同一个例子：
    A  = [[1, 3],      A^{-1} = [[ 7, -3],
          [2, 7]]                [-2,  1]]        (det A = 1)

场景结构（每个 Scene 可独立渲染，也可一次性全部渲染）：
    InverseTitle        片头：逆矩阵的四重身份总览
    InverseColView      视角一 · 列视角：解耦与线性表出（含 Cramer 体积比）
    InverseGeoView      视角二 · 映射视角：逆变换还原空间
    InverseDualView     视角三 · 对偶视角：行与列交叉垂直（含病态发散演示）
    InverseGSCompare    正交化对比：Gram-Schmidt vs 双正交化
    InverseBasisChange  视角四 · 基变换视角：坐标解码器（过渡矩阵）
    InverseGaussJordan  消元动力学：[A|I] -> [I|A^{-1}]，一边解方程一边拉直空间
    InverseGlobalMap    全局闭环：逆矩阵串起的高等代数地图 + 片尾总结

渲染示例（先 conda activate manimce）：
    manim -qm inverse_matrix_perspectives.py InverseTitle
    manim -qm inverse_matrix_perspectives.py InverseColView InverseGeoView
    manim -qm inverse_matrix_perspectives.py InverseDualView InverseGSCompare
    manim -qm inverse_matrix_perspectives.py InverseBasisChange InverseGaussJordan InverseGlobalMap
"""

from manim import *
import numpy as np

# ---------------------------------------------------------------- 公共配置
ZH_FONT = "Microsoft YaHei"

A2 = np.array([[1.0, 3.0], [2.0, 7.0]])
A2_INV = np.linalg.inv(A2)          # [[7,-3],[-2,1]]
E1_SHEAR = np.array([[1.0, 0.0], [-2.0, 1.0]])   # Gauss-Jordan 第一步的初等矩阵
E2_SHEAR = np.array([[1.0, -3.0], [0.0, 1.0]])   # 第二步

C_A1, C_A2 = BLUE, TEAL             # A 的两个列/行向量
C_X1, C_X2 = YELLOW, ORANGE         # A^{-1} 的两个列向量


def zh(txt, **kwargs):
    """中文 Text（微软雅黑），其余参数同 Text"""
    kwargs.setdefault("font", ZH_FONT)
    return Text(txt, **kwargs)


def scene_title(txt):
    """左上角标题 + 下划线"""
    t = zh(txt, font_size=32, weight=BOLD)
    line = Underline(t, buff=0.1, color=TEAL)
    return VGroup(t, line).to_corner(UL, buff=0.35)


def vec(v, color, scale=0.5, stroke=7, shift=ORIGIN, **kwargs):
    """原点出发的箭头，v 为 2 维坐标，按 scale 缩放显示"""
    v = np.asarray(v, dtype=float)
    tip = np.array([scale * v[0], scale * v[1], 0.0]) + np.asarray(shift)
    return Arrow(
        np.asarray(shift, dtype=float), tip, buff=0, color=color,
        stroke_width=stroke, max_tip_length_to_length_ratio=0.3, **kwargs,
    )


def p3(v, scale=0.5, shift=ORIGIN):
    """2 维坐标 -> 屏幕三维点（与 vec 一致的缩放/平移）"""
    v = np.asarray(v, dtype=float)
    return np.array([scale * v[0], scale * v[1], 0.0]) + np.asarray(shift)


def fit_plane(x_range, y_range, unit, line_color=BLUE_E, line_opacity=0.45, anchor=ORIGIN):
    """参考 gram_schmidt.py 的 make_plane：显式 x_length/y_length 的有界网格。
    unit 既是网格单位也是向量缩放系数，保证向量端点严格落在网格交点上；
    anchor 为坐标原点(0,0)所在的屏幕位置。"""
    p = NumberPlane(
        x_range=x_range, y_range=y_range,
        x_length=(x_range[1] - x_range[0]) * unit,
        y_length=(y_range[1] - y_range[0]) * unit,
        background_line_style={
            "stroke_color": line_color, "stroke_opacity": line_opacity, "stroke_width": 1.5},
        axis_config={"stroke_color": BLUE_D, "stroke_opacity": 0.35, "stroke_width": 1.5},
    )
    p.shift(np.asarray(anchor, dtype=float) - p.c2p(0, 0))
    return p


def grid_label(m, width=5):
    """ProjectCode 风格：文字加黑色背景描边，压在网格上仍可读"""
    return m.set_stroke(BLACK, width=width, background=True)


def aug(L, R):
    """增广矩阵 [L | R]，返回 (整体, 左阵, 右阵)"""
    lm, rm = Matrix(L), Matrix(R)
    vline = Line(UP, DOWN).set_height(max(lm.height, rm.height) * 0.85)
    group = VGroup(lm, vline, rm).arrange(RIGHT, buff=0.32)
    return group, lm, rm


def light_plane(x_range=None, y_range=None, scale=1.0, shift=ORIGIN, **kwargs):
    bg = {"stroke_color": BLUE_E, "stroke_opacity": 0.45, "stroke_width": 1.5}
    bg.update(kwargs.pop("background_line_style", {}))
    plane = NumberPlane(
        x_range=x_range or [-8, 8, 1],
        y_range=y_range or [-4, 4, 1],
        background_line_style=bg,
        axis_config={"stroke_color": BLUE_D, "stroke_opacity": 0.35, "stroke_width": 1.5},
    )
    return plane.scale(scale).shift(shift)


# ================================================================ 片头
class InverseTitle(Scene):
    def construct(self):
        title = zh("逆矩阵的多维透视", font_size=64, weight=BOLD)
        title.set_color_by_gradient(BLUE_B, TEAL_A, GREEN_B)
        self.play(Write(title))
        self.play(title.animate.to_edge(UP, buff=0.7))

        A_chip = MathTex(
            r"A = \begin{bmatrix} 1 & 3 \\ 2 & 7 \end{bmatrix}", font_size=52,
        ).next_to(title, DOWN, buff=0.5)
        self.play(Write(A_chip))
        self.wait(0.5)

        cards_data = [
            ("列视角", "解耦 · 线性表出", BLUE),
            ("映射视角", "逆变换 · 还原空间", GREEN),
            ("对偶视角", "行列交叉双正交", ORANGE),
            ("基变换视角", "坐标解码 · 过渡矩阵", PURPLE),
        ]
        cards = VGroup()
        for name, desc, col in cards_data:
            box = RoundedRectangle(
                corner_radius=0.15, width=3.0, height=1.5,
                stroke_color=col, fill_color=col, fill_opacity=0.15,
            )
            card = VGroup(
                zh(name, font_size=32, weight=BOLD, color=col),
                zh(desc, font_size=22, color=GREY_A),
            ).arrange(DOWN, buff=0.22)
            cards.add(VGroup(box, card))

        cards.arrange(RIGHT, buff=0.3).next_to(A_chip, DOWN, buff=0.7)
        self.play(AnimationGroup(
            *[FadeIn(b, scale=0.7) for b in cards], lag_ratio=0.18,
        ))
        self.wait(1)

        banner_box = RoundedRectangle(
            corner_radius=0.12, width=10.5, height=0.85,
            stroke_color=TEAL, fill_color=TEAL, fill_opacity=0.15,
        ).to_edge(DOWN, buff=0.6)
        banner = VGroup(
            zh("消元动力学：", font_size=28, color=TEAL_A),
            MathTex(r"[A \mid I] \longrightarrow [I \mid A^{-1}]", font_size=38, color=TEAL_A),
            zh("空间逐步拉直", font_size=28, color=TEAL_A),
        ).arrange(RIGHT, buff=0.25).move_to(banner_box)
        self.play(Create(banner_box), FadeIn(banner, shift=UP * 0.3))
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, A_chip, cards, banner_box, banner)))


# ================================================================ 视角一：列视角
class InverseColView(Scene):
    def construct(self):
        title = scene_title("视角一 · 列视角：解耦与线性表出")
        self.play(Write(title[0]), Create(title[1]))

        # ---------- Part A：按列展开的理论 ----------
        m1 = MathTex(r"A = [\mathbf{a}_1, \mathbf{a}_2, \cdots, \mathbf{a}_n]", font_size=38)
        m2 = MathTex(r"A^{-1} = [\mathbf{x}_1, \mathbf{x}_2, \cdots, \mathbf{x}_n]", font_size=38)
        m3 = MathTex(r"A\,\mathbf{x}_j = \mathbf{e}_j", r",\;\; j = 1, 2, \cdots, n", font_size=38)
        theory = VGroup(m1, m2, m3).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        theory.to_edge(LEFT, buff=0.7).shift(UP * 0.9)
        box = SurroundingRectangle(m3, color=TEAL, buff=0.15)
        cap = zh("逆矩阵的每一列，都是用 A 的列向量\n拼出单位基向量的系数配方",
                 font_size=26, color=TEAL_A, line_spacing=1.1)
        cap.next_to(box, DOWN, aligned_edge=LEFT, buff=0.35)

        self.play(Write(m1))
        self.play(Write(m2))
        self.play(Write(m3), Create(box))
        self.play(FadeIn(cap, shift=UP * 0.2))
        self.wait(1.5)

        # ---------- Part B：实例 —— 完全解耦的两个方程组 ----------
        Am = Matrix([[1, 3], [2, 7]]).scale(0.85)
        Am_label = MathTex(r"A =").next_to(Am, LEFT, buff=0.2)
        sys1 = MathTex(
            r"A\begin{bmatrix} x_{11} \\ x_{21} \end{bmatrix} = \begin{bmatrix} 1 \\ 0 \end{bmatrix}"
            r"\;\Rightarrow\; \mathbf{x}_1 = \begin{bmatrix} 7 \\ -2 \end{bmatrix}", font_size=34,
        )
        sys2 = MathTex(
            r"A\begin{bmatrix} x_{12} \\ x_{22} \end{bmatrix} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}"
            r"\;\Rightarrow\; \mathbf{x}_2 = \begin{bmatrix} -3 \\ 1 \end{bmatrix}", font_size=34,
        )
        decoup = zh("4 个方程完全解耦：系数矩阵相同，仅右端不同",
                    font_size=24, color=GREY_A)
        right_col = VGroup(VGroup(Am_label, Am), sys1, sys2, decoup)
        right_col.arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        right_col.to_edge(RIGHT, buff=0.6).shift(UP * 1.1)

        self.play(Write(VGroup(Am_label, Am)))
        self.play(Write(sys1))
        self.wait(0.5)
        self.play(Write(sys2))
        self.play(FadeIn(decoup, shift=UP * 0.2))

        inv_m = Matrix([[7, -3], [-2, 1]]).scale(0.85)
        inv_eq = MathTex(r"A^{-1} =").next_to(inv_m, LEFT, buff=0.2)
        inv_group = VGroup(inv_eq, inv_m).next_to(decoup, DOWN, buff=0.5).align_to(decoup, LEFT)
        inv_box = SurroundingRectangle(inv_group, color=YELLOW, buff=0.18)
        self.play(FadeTransform(VGroup(sys1, sys2).copy(), inv_group))
        self.play(Create(inv_box))
        self.wait(1.5)

        # ---------- Part C：几何图像 —— 单位基在斜基下的坐标 ----------
        self.play(FadeOut(VGroup(theory, box, cap, right_col, inv_box, title)))

        shift = DOWN * 0.3
        S = 0.55
        # 斜坐标网格：先在原点处做线性变换，再整体平移
        plane = light_plane(x_range=[-3, 10, 1], y_range=[-5, 5, 1], scale=S)
        plane.apply_function(lambda p: np.array([*(A2 @ p[:2]), 0.0]))
        plane.shift(shift)
        a1_arrow = vec((1, 2), C_A1, S, shift=shift)
        a2_arrow = vec((3, 7), C_A2, S, shift=shift)
        lab_a1 = grid_label(MathTex(r"\mathbf{a}_1", color=C_A1, font_size=34)).next_to(p3((1, 2), S, shift), LEFT, buff=0.12)
        lab_a2 = grid_label(MathTex(r"\mathbf{a}_2", color=C_A2, font_size=34)).next_to(p3((3, 7), S, shift), RIGHT, buff=0.12)

        cap_grid = zh("A 的列向量张成的斜坐标系", font_size=26, color=GREY_A)
        cap_grid.to_corner(UR, buff=0.5).shift(DOWN * 0.1)
        self.play(Create(plane), run_time=2)
        self.play(GrowArrow(a1_arrow), GrowArrow(a2_arrow),
                  FadeIn(lab_a1), FadeIn(lab_a2), FadeIn(cap_grid))
        self.wait(0.5)

        e1_dot = Dot(p3((1, 0), S, shift), color=YELLOW, radius=0.1)
        lab_e1 = grid_label(MathTex(r"\mathbf{e}_1", color=YELLOW, font_size=34)).next_to(p3((1, 0), S, shift), DOWN, buff=0.15)
        # 经过 e1 的两条斜网格线：u = 7 与 v = -2（e1 = 7a1 - 2a2）
        line_u = DashedLine(p3(7 * np.array([1, 2]) - 4 * np.array([3, 7]), S, shift),
                            p3(7 * np.array([1, 2]) + 2 * np.array([3, 7]), S, shift),
                            color=YELLOW, stroke_width=3)
        line_v = DashedLine(p3(-2 * np.array([3, 7]) - 1 * np.array([1, 2]), S, shift),
                            p3(-2 * np.array([3, 7]) + 7 * np.array([1, 2]), S, shift),
                            color=ORANGE, stroke_width=3)
        lab_u = grid_label(MathTex(r"u = 7", color=YELLOW, font_size=30))
        lab_v = grid_label(MathTex(r"v = -2", color=ORANGE, font_size=30))
        lab_u.next_to(p3(7 * np.array([1, 2]) - 1.4 * np.array([3, 7]), S, shift), RIGHT, buff=0.1)
        lab_v.next_to(p3(5 * np.array([1, 2]) - 2 * np.array([3, 7]), S, shift), LEFT, buff=0.1)

        self.play(FadeIn(e1_dot), Write(lab_e1))
        self.play(Create(line_u), FadeIn(lab_u))
        self.play(Create(line_v), FadeIn(lab_v))
        self.wait(0.5)

        eq_e1 = grid_label(MathTex(
            r"\mathbf{e}_1 = 7\,\mathbf{a}_1 - 2\,\mathbf{a}_2",
            font_size=42,
        )).to_corner(DL, buff=0.5)
        eq_e2 = grid_label(MathTex(
            r"\mathbf{e}_2 = -3\,\mathbf{a}_1 + 1\,\mathbf{a}_2",
            font_size=42,
        )).next_to(eq_e1, UP, buff=0.35)
        cap_bridge = zh("斜坐标里的读数 (7, -2) 与 (-3, 1)，拼起来正是 A 的逆",
                        font_size=26, color=YELLOW).add_background_rectangle(opacity=0.7, buff=0.1)
        cap_bridge.next_to(eq_e2, UP, buff=0.4).align_to(eq_e1, LEFT)
        self.play(Write(eq_e2))
        self.play(Write(eq_e1))
        self.play(FadeIn(cap_bridge, shift=UP * 0.2))
        self.wait(2)

        # ---------- Part D：Cramer 法则 —— 体积比 ----------
        self.play(FadeOut(VGroup(plane, a1_arrow, a2_arrow, lab_a1, lab_a2, cap_grid,
                                 e1_dot, lab_e1, line_u, line_v, lab_u, lab_v,
                                 eq_e1, eq_e2, cap_bridge, title)))

        cramer_title = zh("Cramer 视角：每个元素都是一个体积比", font_size=34, weight=BOLD)
        cramer_title.to_edge(UP, buff=0.5)
        formula = MathTex(
            r"x_{ij} = \frac{\det[\mathbf{a}_1, \cdots, \mathbf{e}_j, \cdots, \mathbf{a}_n]}"
            r"{\det[\mathbf{a}_1, \cdots, \mathbf{a}_n]}",
            font_size=44,
        ).next_to(cramer_title, DOWN, buff=0.45)
        self.play(Write(cramer_title), Write(formula))
        self.wait(1)

        S2 = 0.38
        poly_A = Polygon(
            ORIGIN, p3((1, 2), S2), p3((4, 9), S2), p3((3, 7), S2),
            fill_color=C_A1, fill_opacity=0.45, stroke_color=C_A1, stroke_width=2,
        ).shift(LEFT * 3.4 + DOWN * 1.6)
        lab_pA = MathTex(r"\det A = 1", font_size=34, color=C_A1).next_to(poly_A, DOWN, buff=0.25)

        poly_E = Polygon(
            ORIGIN, p3((1, 0), S2), p3((4, 7), S2), p3((3, 7), S2),
            fill_color=C_X2, fill_opacity=0.45, stroke_color=C_X2, stroke_width=2,
        ).shift(RIGHT * 1.2 + DOWN * 1.6)
        lab_pE = MathTex(r"\det[\mathbf{e}_1, \mathbf{a}_2] = 7", font_size=34, color=C_X2)
        lab_pE.next_to(poly_E, DOWN, buff=0.25)

        cap_poly = zh("把第 1 根棱 a₁ 换成 e₁，体积从 1 变为 7", font_size=26, color=GREY_A)
        cap_poly.next_to(VGroup(poly_A, poly_E), UP, buff=0.6)
        self.play(DrawBorderThenFill(poly_A), Write(lab_pA))
        self.play(DrawBorderThenFill(poly_E), Write(lab_pE))
        self.play(FadeIn(cap_poly, shift=UP * 0.2))

        ratio = MathTex(r"x_{11} = \frac{7}{1} = 7", font_size=46, color=YELLOW)
        ratio.next_to(poly_E, RIGHT, buff=1.0).shift(DOWN * 0.4)
        ratio_box = SurroundingRectangle(ratio, color=YELLOW, buff=0.15)
        match = zh("恰好是 A⁻¹ 左上角的元素", font_size=24, color=YELLOW)
        match.next_to(ratio_box, DOWN, buff=0.2)
        self.play(Write(ratio), Create(ratio_box), FadeIn(match))
        self.wait(2.5)
        self.play(FadeOut(VGroup(cramer_title, formula, poly_A, lab_pA, poly_E, lab_pE,
                                 cap_poly, ratio, ratio_box, match)))


# ================================================================ 视角二：映射视角
class InverseGeoView(Scene):
    def construct(self):
        title = scene_title("视角二 · 映射视角：逆变换还原空间")
        self.play(Write(title[0]), Create(title[1]))

        # ProjectCode 双网格构图：灰色静止底网格 = “变换前的原位置”参照
        # 网格单位 0.5 = 向量缩放系数，保证端点落在网格交点上
        base = light_plane(x_range=[-15, 15, 1], y_range=[-9, 9, 1], scale=0.5,
                           background_line_style={
                               "stroke_color": GREY_D, "stroke_opacity": 0.35, "stroke_width": 1.5,
                           })
        plane = light_plane(x_range=[-15, 15, 1], y_range=[-9, 9, 1], scale=0.5)
        e1_arrow, e2_arrow = vec((1, 0), BLUE), vec((0, 1), GREEN)
        grid_group = VGroup(plane, e1_arrow, e2_arrow)
        lab_e1 = grid_label(MathTex(r"\mathbf{e}_1", color=BLUE, font_size=34)).next_to(0.5 * RIGHT, UR, buff=0.08)
        lab_e2 = grid_label(MathTex(r"\mathbf{e}_2", color=GREEN, font_size=34)).next_to(0.5 * UP, LEFT, buff=0.08)
        self.play(FadeIn(base, run_time=1.5))
        self.play(Create(plane, run_time=2), GrowArrow(e1_arrow), GrowArrow(e2_arrow))
        self.play(FadeIn(lab_e1), FadeIn(lab_e2))

        A_chip = VGroup(
            MathTex(r"A =", font_size=40, color=ORANGE),
            Matrix([[1, 3], [2, 7]]).scale(0.8).set_color(ORANGE),
        ).arrange(RIGHT, buff=0.15).to_corner(UR, buff=0.5).shift(DOWN * 0.7)
        cap_A = zh("剪切 · 拉伸", font_size=24, color=GREY_A).next_to(A_chip, DOWN, buff=0.15)
        self.play(FadeIn(A_chip, shift=UP * 0.2), FadeIn(cap_A))

        # 逆矩阵的两列（幽灵箭头）：A 会把它们精确送回单位基
        x1_arrow = vec((7, -2), C_X1, stroke=6)
        x2_arrow = vec((-3, 1), C_X2, stroke=6)
        lab_x1 = grid_label(MathTex(r"\mathbf{x}_1", color=C_X1, font_size=34)).next_to(0.5 * np.array([7, -2, 0]), DR, buff=0.1)
        lab_x2 = grid_label(MathTex(r"\mathbf{x}_2", color=C_X2, font_size=34)).next_to(0.5 * np.array([-3, 1, 0]), UL, buff=0.1)
        ghost_group = VGroup(x1_arrow, x2_arrow)
        self.play(GrowArrow(x1_arrow), GrowArrow(x2_arrow), FadeIn(lab_x1), FadeIn(lab_x2))
        self.wait(1)

        # 残影基向量（ProjectCode 模式）：灰色静止，作为“变换前”的对照
        ghost_e1 = vec((1, 0), interpolate_color(BLUE, BLACK, 0.5), stroke=5)
        ghost_e2 = vec((0, 1), interpolate_color(GREEN, BLACK, 0.5), stroke=5)

        # A 作用：网格扭斜；x1, x2 恰好落到 e1, e2 的位置
        self.play(FadeOut(lab_e1), FadeOut(lab_e2), FadeOut(lab_x1), FadeOut(lab_x2))
        self.play(FadeIn(ghost_e1), FadeIn(ghost_e2))
        self.play(ApplyMatrix(A2, grid_group), ApplyMatrix(A2, ghost_group), run_time=3)
        lab_a1 = grid_label(MathTex(r"\mathbf{a}_1", color=BLUE, font_size=34)).next_to(0.5 * np.array([1, 2, 0]), RIGHT, buff=0.12)
        lab_a2 = grid_label(MathTex(r"\mathbf{a}_2", color=GREEN, font_size=34)).next_to(0.5 * np.array([3, 7, 0]), RIGHT, buff=0.12)
        cap1 = zh("标准基被送至 a₁, a₂，网格歪斜（灰网格是原位置）",
                  font_size=26, color=GREY_A).add_background_rectangle(opacity=0.6, buff=0.1)
        cap1.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(lab_a1), FadeIn(lab_a2), FadeIn(cap1, shift=UP * 0.2))

        hit1 = Flash(0.5 * RIGHT, color=C_X1, flash_radius=0.5)
        hit2 = Flash(0.5 * UP, color=C_X2, flash_radius=0.5)
        cap2 = zh("x₁ 与 x₂ 恰好被 A 送到 e₁ 与 e₂ 的位置",
                  font_size=26, color=YELLOW).add_background_rectangle(opacity=0.6, buff=0.1)
        cap2.next_to(cap1, UP, buff=0.15)
        self.play(hit1, run_time=1)
        self.play(hit2, FadeIn(cap2, shift=UP * 0.2))
        self.wait(1.5)

        # A^{-1} 作用：一切还原
        cap3 = zh("再施加 A⁻¹：歪斜的网格被精确拉回标准正交",
                  font_size=26, color=GREEN).add_background_rectangle(opacity=0.6, buff=0.1)
        cap3.to_edge(DOWN, buff=0.5)
        self.play(FadeOut(cap1), FadeOut(cap2), FadeIn(cap3, shift=UP * 0.2))
        self.play(ApplyMatrix(A2_INV, grid_group), ApplyMatrix(A2_INV, ghost_group), run_time=3)
        lab_e1b = lab_e1.copy()
        lab_e2b = lab_e2.copy()
        self.play(FadeIn(lab_e1b), FadeIn(lab_e2b))
        self.wait(1)

        # 两个方向的公式
        self.play(FadeOut(cap3), FadeOut(ghost_e1), FadeOut(ghost_e2))
        f1 = VGroup(
            zh("正向作用", font_size=24, color=GREY_A),
            grid_label(MathTex(r"A\,\mathbf{x}_1 = \mathbf{e}_1, \quad A\,\mathbf{x}_2 = \mathbf{e}_2", font_size=38)),
        ).arrange(DOWN, buff=0.12)
        f2 = VGroup(
            zh("逆向还原", font_size=24, color=GREY_A),
            grid_label(MathTex(r"A^{-1}\mathbf{a}_1 = \mathbf{e}_1, \quad A^{-1}\mathbf{a}_2 = \mathbf{e}_2", font_size=38)),
        ).arrange(DOWN, buff=0.12)
        formulas = VGroup(f1, f2).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.5)
        box_all = SurroundingRectangle(formulas, color=TEAL, buff=0.25)
        self.play(FadeIn(f1, shift=UP * 0.2))
        self.play(FadeIn(f2, shift=UP * 0.2))
        self.play(Create(box_all))
        self.wait(2.5)
        self.play(FadeOut(VGroup(base, plane, grid_group, ghost_group, lab_e1b, lab_e2b,
                                 lab_a1, lab_a2, A_chip, cap_A, formulas, box_all, title)))


# ================================================================ 视角三：对偶视角
class InverseDualView(Scene):
    def construct(self):
        title = scene_title("视角三 · 对偶视角：行与列交叉垂直")
        self.play(Write(title[0]), Create(title[1]))

        S = 0.5
        shift = np.array([-2.0, -0.2, 0.0])
        # 有界网格：单位 = 向量系数 0.5，原点锚定在 (-2.0, -0.2)
        plane = fit_plane([-3.7, 7.7, 1], [-1.8, 7.8, 1], S, anchor=shift)

        d_top = grid_label(MathTex(
            r"A^{-1}A = I \;\Longrightarrow\; \mathbf{r}_i^{T}\mathbf{x}_j = \delta_{ij}"
            r" = \begin{cases} 1, & i = j \\ 0, & i \neq j \end{cases}",
            font_size=36,
        )).to_corner(UR, buff=0.45).shift(DOWN * 0.35)
        cap_top = zh("A 的第 i 行 乘 A⁻¹ 的第 j 列", font_size=24, color=GREY_A)
        cap_top.next_to(d_top, DOWN, buff=0.12).align_to(d_top, RIGHT)

        self.play(Create(plane, run_time=1.5))
        self.play(Write(d_top), FadeIn(cap_top))
        self.wait(0.5)

        # A 的行向量（蓝色系）与 A^{-1} 的列向量（黄橙系）
        r1_arrow = vec((1, 3), C_A1, S, shift=shift)
        r2_arrow = vec((2, 7), C_A2, S, shift=shift)
        lab_r1 = grid_label(MathTex(r"\mathbf{r}_1", color=C_A1, font_size=34))
        lab_r2 = grid_label(MathTex(r"\mathbf{r}_2", color=C_A2, font_size=34))
        lab_r1.next_to(p3((1, 3), S, shift), LEFT, buff=0.1)
        lab_r2.next_to(p3((2, 7), S, shift), RIGHT, buff=0.1)
        self.play(GrowArrow(r1_arrow), GrowArrow(r2_arrow), FadeIn(lab_r1), FadeIn(lab_r2))

        x1_arrow = vec((7, -2), C_X1, S, shift=shift)
        x2_arrow = vec((-3, 1), C_X2, S, shift=shift)
        lab_x1 = grid_label(MathTex(r"\mathbf{x}_1", color=C_X1, font_size=34))
        lab_x2 = grid_label(MathTex(r"\mathbf{x}_2", color=C_X2, font_size=34))
        lab_x1.next_to(p3((7, -2), S, shift), DOWN, buff=0.12)
        lab_x2.next_to(p3((-3, 1), S, shift), UP, buff=0.1)
        self.play(GrowArrow(x1_arrow), GrowArrow(x2_arrow), FadeIn(lab_x1), FadeIn(lab_x2))
        self.wait(0.5)

        # 交叉垂直 1：x2 ⟂ r1（r1 张成的“超平面”就是这条直线）
        span_r1 = DashedLine(
            p3(-1.1 * np.array([1, 3]), S, shift), p3(2.4 * np.array([1, 3]), S, shift),
            color=C_X2, stroke_width=3, stroke_opacity=0.7,
        )
        ra1 = RightAngle(
            Line(ORIGIN + shift, p3((1, 3), S, shift)),
            Line(ORIGIN + shift, p3((-3, 1), S, shift)),
            length=0.22, color=C_X2, stroke_width=3,
        )
        dot1 = MathTex(
            r"\mathbf{r}_1^{T}\mathbf{x}_2 = 1\cdot(-3) + 3\cdot 1 = 0", font_size=32,
        ).to_edge(RIGHT, buff=0.45).shift(UP * 0.8)
        cap1 = zh("x₂ 垂直于其余行张成的超平面", font_size=20, color=C_X2)
        cap1.next_to(dot1, DOWN, buff=0.15).align_to(dot1, LEFT)
        self.play(Create(span_r1), Create(ra1))
        self.play(Write(dot1), FadeIn(cap1, shift=UP * 0.2))
        self.wait(1)

        # 交叉垂直 2：x1 ⟂ r2
        span_r2 = DashedLine(
            ORIGIN + shift, p3(1.3 * np.array([2, 7]), S, shift),
            color=C_X1, stroke_width=3, stroke_opacity=0.7,
        )
        ra2 = RightAngle(
            Line(ORIGIN + shift, p3((2, 7), S, shift)),
            Line(ORIGIN + shift, p3((7, -2), S, shift)),
            length=0.22, color=C_X1, stroke_width=3,
        )
        dot2 = MathTex(
            r"\mathbf{r}_2^{T}\mathbf{x}_1 = 2\cdot 7 + 7\cdot(-2) = 0", font_size=32,
        ).next_to(cap1, DOWN, buff=0.45).align_to(dot1, LEFT)
        cap2 = zh("x₁ 垂直于其余行张成的超平面", font_size=20, color=C_X1)
        cap2.next_to(dot2, DOWN, buff=0.15).align_to(dot2, LEFT)
        self.play(Create(span_r2), Create(ra2))
        self.play(Write(dot2), FadeIn(cap2, shift=UP * 0.2))
        self.wait(1)

        dot3a = MathTex(r"\mathbf{r}_1^{T}\mathbf{x}_1 = 7 - 6 = 1", font_size=32,
                        ).next_to(cap2, DOWN, buff=0.45).align_to(dot1, LEFT)
        dot3b = MathTex(r"\mathbf{r}_2^{T}\mathbf{x}_2 = -6 + 7 = 1", font_size=32,
                        ).next_to(dot3a, DOWN, buff=0.18).align_to(dot1, LEFT)
        cap3 = zh("对角配对全部归一", font_size=20, color=GREY_A)
        cap3.next_to(dot3b, DOWN, buff=0.15).align_to(dot3b, LEFT)
        self.play(Write(dot3a), Write(dot3b), FadeIn(cap3))
        self.wait(1.5)

        # 三维：伴随矩阵 = 外积法向量
        cross_formula = MathTex(
            r"\mathbf{x}_1 = \frac{\mathbf{r}_2 \times \mathbf{r}_3}{\det A}, \quad"
            r"\mathbf{x}_2 = \frac{\mathbf{r}_3 \times \mathbf{r}_1}{\det A}, \quad"
            r"\mathbf{x}_3 = \frac{\mathbf{r}_1 \times \mathbf{r}_2}{\det A}",
            font_size=36,
        ).to_edge(DOWN, buff=0.4)
        cap4 = zh("三维时：代数余子式 = 其余行张成平面的法向量，det A 是归一化因子",
                  font_size=22, color=GREY_A)
        cap4.next_to(cross_formula, UP, buff=0.15).align_to(cross_formula, RIGHT)
        self.play(FadeOut(VGroup(d_top, cap_top, dot1, cap1, dot2, cap2, dot3a, dot3b, cap3)))
        self.play(Write(cross_formula), FadeIn(cap4, shift=UP * 0.2))
        self.wait(2)

        # ---------- 病态演示：基底偏转 2.5°，对偶基爆炸 ----------
        self.play(FadeOut(VGroup(cross_formula, cap4, span_r1, span_r2, ra1, ra2,
                                 r2_arrow, x1_arrow, x2_arrow, lab_r2, lab_x1, lab_x2, title)))

        DTH = np.arctan2(7, 2) - np.arctan2(3, 1)   # r1 与 r2 的夹角 ≈ 0.0435 rad

        def rot2(v, ang):
            c, s = np.cos(ang), np.sin(ang)
            return np.array([c * v[0] - s * v[1], s * v[0] + c * v[1]])

        trk = ValueTracker(0.0)

        def A_now():
            r2 = rot2(np.array([2.0, 7.0]), -trk.get_value() * DTH)
            return np.array([[1.0, 3.0], [r2[0], r2[1]]])

        r2_dyn = always_redraw(
            lambda: vec(rot2([2, 7], -trk.get_value() * DTH), C_A2, S, shift=shift))
        x1_dyn = always_redraw(
            lambda: vec(np.linalg.inv(A_now())[:, 0], C_X1, S, shift=shift))
        x2_dyn = always_redraw(
            lambda: vec(np.linalg.inv(A_now())[:, 1], C_X2, S, shift=shift))

        det_read = always_redraw(lambda: VGroup(
            MathTex(r"\det A =", font_size=34),
            DecimalNumber(np.linalg.det(A_now()), num_decimal_places=2,
                          font_size=34, color=RED),
        ).arrange(RIGHT, buff=0.12).to_corner(UR, buff=0.5).shift(DOWN * 0.6))
        norm_read = always_redraw(lambda: VGroup(
            MathTex(r"\|\mathbf{x}_1\| =", font_size=34),
            DecimalNumber(np.linalg.norm(np.linalg.inv(A_now())[:, 0]),
                          num_decimal_places=1, font_size=34, color=RED),
        ).arrange(RIGHT, buff=0.12).to_corner(UR, buff=0.5).shift(DOWN * 1.25))

        warn = zh("行向量 r₂ 仅向 r₁ 偏转约 2.5°……", font_size=28, color=GREY_A)
        warn.to_edge(DOWN, buff=0.9)
        warn2 = zh("……对偶基却爆炸式发散：det A 越小，逆矩阵越病态；det A = 0 时不存在",
                   font_size=28, color=RED)
        warn2.next_to(warn, DOWN, buff=0.2)

        self.play(FadeIn(r2_dyn), FadeIn(x1_dyn), FadeIn(x2_dyn),
                  FadeIn(det_read), FadeIn(norm_read), FadeIn(warn))
        self.play(trk.animate.set_value(0.9), run_time=7, rate_func=smooth)
        self.play(FadeIn(warn2, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(VGroup(plane, r1_arrow, lab_r1, warn, warn2)),
                  FadeOut(r2_dyn), FadeOut(x1_dyn), FadeOut(x2_dyn),
                  FadeOut(det_read), FadeOut(norm_read))


# ================================================================ 正交化对比
class InverseGSCompare(Scene):
    def construct(self):
        title = scene_title("正交化的两条路：内部拉直 vs 外部对偶")
        self.play(Write(title[0]), Create(title[1]))

        cap_L = zh("Gram–Schmidt：改造基底，在空间内拉直", font_size=24, color=GREEN)
        cap_L.move_to(np.array([-3.4, 3.1, 0]))
        cap_R = zh("双正交化：基底不动，在外部找对偶法向量", font_size=24, color=ORANGE)
        cap_R.move_to(np.array([3.4, 3.1, 0]))

        # ---------- 左：Gram-Schmidt（示例向量取 u1=(3,1), u2=(1,3)，与 gram_schmidt.py 一致）----------
        KL = 0.7
        LSH = np.array([-3.4, -0.6, 0.0])
        plane_L = fit_plane([-2, 4.2, 1], [-2, 4.2, 1], KL, anchor=LSH)
        u1_arrow = vec((3, 1), GREEN, KL, shift=LSH)
        u2_arrow = vec((1, 3), PURPLE, KL, shift=LSH)
        lab_u1 = MathTex(r"\mathbf{u}_1", color=GREEN, font_size=30)
        lab_u2 = MathTex(r"\mathbf{u}_2", color=PURPLE, font_size=30)
        lab_u1.next_to(p3((3, 1), KL, LSH), RIGHT, buff=0.1)
        lab_u2.next_to(p3((1, 3), KL, LSH), UP, buff=0.1)
        self.play(Create(plane_L, run_time=1.2), FadeIn(cap_L),
                  GrowArrow(u1_arrow), GrowArrow(u2_arrow), FadeIn(lab_u1), FadeIn(lab_u2))

        proj_pt = 0.6 * np.array([3, 1])                    # u2 在 u1 上的投影 (1.8, 0.6)
        proj_line = DashedLine(
            p3((0, 0), KL, LSH), p3(proj_pt, KL, LSH),
            color=GREY_B, stroke_width=3,
        )
        perp_line = DashedLine(
            p3(proj_pt, KL, LSH), p3((1, 3), KL, LSH),
            color=WHITE, stroke_width=3,
        )
        q1_dir = np.array([3, 1]) / np.sqrt(10)
        ra = RightAngle(
            Line(p3(proj_pt, KL, LSH), p3(proj_pt + q1_dir, KL, LSH)),
            Line(p3(proj_pt, KL, LSH), p3((1, 3), KL, LSH)),
            length=0.2, color=WHITE, stroke_width=2.5,
        )
        self.play(Create(proj_line), Create(perp_line), Create(ra))
        step1_cap = zh("减去投影分量：u₂ → 垂直残差", font_size=22, color=GREY_A)
        step1_cap.next_to(plane_L, DOWN, buff=0.25)
        residual = (1, 3) - proj_pt                          # (-0.8, 2.4)
        u2_res = vec(residual, PURPLE, KL, shift=LSH)
        self.play(Transform(u2_arrow, u2_res), FadeIn(step1_cap, shift=UP * 0.2))
        q2_dir = residual / np.linalg.norm(residual)
        u2_q = vec(q2_dir, PURPLE, KL, shift=LSH)
        u1_q = vec(q1_dir, GREEN, KL, shift=LSH)
        step2_cap = zh("再归一化：得到内正交基 q₁, q₂", font_size=22, color=GREEN)
        step2_cap.next_to(step1_cap, DOWN, buff=0.12)
        self.play(Transform(u2_arrow, u2_q), Transform(u1_arrow, u1_q),
                  FadeIn(step2_cap, shift=UP * 0.2))
        lab_q1 = MathTex(r"\mathbf{q}_1", color=GREEN, font_size=30).next_to(
            p3(q1_dir, KL, LSH), UR, buff=0.05)
        lab_q2 = MathTex(r"\mathbf{q}_2", color=PURPLE, font_size=30).next_to(
            p3(q2_dir, KL, LSH), LEFT, buff=0.05)
        self.play(FadeOut(lab_u1), FadeOut(lab_u2), FadeIn(lab_q1), FadeIn(lab_q2))
        self.wait(1)

        # ---------- 右：双正交（仍用 A 的行向量与 A⁻¹ 的列向量）----------
        KR = 0.45
        RSH = np.array([2.5, -1.0, 0.0])
        plane_R = fit_plane([-3.5, 7.5, 1], [-1.8, 7.8, 1], KR, anchor=RSH)
        self.play(Create(plane_R, run_time=1.2), FadeIn(cap_R))
        r1_arrow = vec((1, 3), C_A1, KR, shift=RSH)
        r2_arrow = vec((2, 7), C_A2, KR, shift=RSH)
        lab_r1 = MathTex(r"\mathbf{r}_1", color=C_A1, font_size=30)
        lab_r2 = MathTex(r"\mathbf{r}_2", color=C_A2, font_size=30)
        lab_r1.next_to(p3((1, 3), KR, RSH), LEFT, buff=0.08)
        lab_r2.next_to(p3((2, 7), KR, RSH), RIGHT, buff=0.08)
        self.play(GrowArrow(r1_arrow), GrowArrow(r2_arrow), FadeIn(lab_r1), FadeIn(lab_r2))

        span_r1 = DashedLine(p3(-1.0 * np.array([1, 3]), KR, RSH),
                             p3(2.2 * np.array([1, 3]), KR, RSH),
                             color=C_X2, stroke_width=3, stroke_opacity=0.7)
        x2_arrow = vec((-3, 1), C_X2, KR, shift=RSH)
        ra2 = RightAngle(
            Line(ORIGIN + RSH, p3((1, 3), KR, RSH)),
            Line(ORIGIN + RSH, p3((-3, 1), KR, RSH)),
            length=0.2, color=C_X2, stroke_width=2.5,
        )
        cap_d1 = zh("x₂ 垂直 r₁，且 r₂·x₂ = 1：方向与长度被唯一锁定",
                    font_size=20, color=C_X2)
        cap_d1.next_to(plane_R, DOWN, buff=0.25)
        self.play(Create(span_r1), GrowArrow(x2_arrow), Create(ra2))
        self.play(FadeIn(cap_d1, shift=UP * 0.2))
        x1_arrow = vec((7, -2), C_X1, KR, shift=RSH)
        ra3 = RightAngle(
            Line(ORIGIN + RSH, p3((2, 7), KR, RSH)),
            Line(ORIGIN + RSH, p3((7, -2), KR, RSH)),
            length=0.2, color=C_X1, stroke_width=2.5,
        )
        cap_d2 = zh("原基底保持倾斜不变", font_size=20, color=GREY_A)
        cap_d2.next_to(cap_d1, DOWN, buff=0.12)
        self.play(GrowArrow(x1_arrow), Create(ra3), FadeIn(cap_d2, shift=UP * 0.2))
        self.wait(2)

        # ---------- 对比表 ----------
        self.play(FadeOut(VGroup(plane_L, plane_R, cap_L, cap_R,
                                 u1_arrow, u2_arrow, proj_line, perp_line, ra,
                                 step1_cap, step2_cap, lab_q1, lab_q2,
                                 r1_arrow, r2_arrow, lab_r1, lab_r2,
                                 span_r1, x2_arrow, ra2, cap_d1,
                                 x1_arrow, ra3, cap_d2, title)))

        def cell(txt, **kw):
            return zh(txt, font_size=26, **kw)

        def cell_mix(cn, tex, color=None):
            g = VGroup(zh(cn, font_size=26),
                       MathTex(tex, font_size=30, color=color or WHITE))
            return g.arrange(RIGHT, buff=0.12)

        header = [cell("维度", weight=BOLD),
                  cell("Gram–Schmidt（A = QR）", weight=BOLD),
                  cell("双正交化（A⁻¹A = I）", weight=BOLD)]
        rows = [
            [cell("几何策略"), cell("空间内拉直：改造基底"), cell("跨空间对偶：基底不动")],
            [cell("正交性质"), cell_mix("内正交：", r"q_i^T q_j = \delta_{ij}"),
             cell_mix("互正交：", r"r_i^T x_j = \delta_{ij}")],
            [cell("度量保真"), cell("保距：属于正交群 O(n)"), cell("不保距：病态时发散")],
            [cell("代数联系"), cell_mix("桥梁：", r"A^{-1} = R^{-1}Q^T")],
        ]

        table_x = [frame_left_edge() + 0.55, -4.35, 0.8]
        row_ys = [2.6, 1.75, 0.9, 0.05, -0.8]

        all_cells = VGroup()
        for ri, row in enumerate([header] + rows):
            for ci, c in enumerate(row):
                c.align_to(np.array([table_x[ci], row_ys[ri], 0.0]), LEFT)
                c.set_y(row_ys[ri])
                all_cells.add(c)
        h_lines = VGroup(*[
            Line(np.array([table_x[0] - 0.2, y, 0]), np.array([6.5, y, 0]),
                 stroke_opacity=0.3, stroke_width=1.5)
            for y in (row_ys[0] - 0.42, row_ys[1] - 0.42, row_ys[2] - 0.42, row_ys[3] - 0.42)
        ])
        v_lines = VGroup(*[
            Line(np.array([x, row_ys[0] + 0.45, 0]), np.array([x, row_ys[-1] - 0.4, 0]),
                 stroke_opacity=0.2, stroke_width=1.5)
            for x in (-4.7, 0.45)
        ])
        self.play(FadeIn(all_cells, lag_ratio=0.06), Create(h_lines), Create(v_lines))
        self.wait(1)

        link_cap = zh("先由 Qᵀ 做正交投影，再由 R⁻¹ 解开三角耦合", font_size=26, color=TEAL_A)
        link_cap.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(link_cap, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(VGroup(all_cells, h_lines, v_lines, link_cap)))


def frame_left_edge():
    return -config.frame_x_radius


# ================================================================ 视角四：基变换
class InverseBasisChange(Scene):
    def construct(self):
        title = scene_title("视角四 · 基变换：坐标解码器")
        self.play(Write(title[0]), Create(title[1]))

        # ---------- 左：理论 ----------
        l0 = MathTex(r"\mathcal{E} = (\mathbf{e}_1, \mathbf{e}_2)", font_size=36)
        l0b = MathTex(r"\mathcal{A} = (\mathbf{a}_1, \mathbf{a}_2)", font_size=36)
        l1 = MathTex(r"\mathcal{A} = \mathcal{E}\,A", font_size=40, color=C_A1)
        l1_cap = zh("标准基 → 斜基：过渡矩阵就是 A", font_size=24, color=GREY_A)
        l2 = MathTex(r"\mathcal{E} = \mathcal{A}\,A^{-1}", font_size=40, color=C_X1)
        l2_cap = zh("斜基 → 标准基：过渡矩阵就是 A⁻¹", font_size=24, color=GREY_A)
        concl = zh("求逆矩阵 = 求回到标准基的过渡矩阵", font_size=28, color=TEAL_A, weight=BOLD)
        concl_box = SurroundingRectangle(concl, color=TEAL, buff=0.2)

        left = VGroup(
            VGroup(l0, l0b).arrange(RIGHT, buff=0.5),
            l1, l1_cap, l2, l2_cap,
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        left.to_edge(LEFT, buff=0.7).shift(UP * 1.3)
        concl.next_to(left, DOWN, buff=0.45).align_to(left, LEFT)

        self.play(Write(l0), Write(l0b))
        self.play(Write(l1), FadeIn(l1_cap, shift=UP * 0.15))
        self.play(Write(l2), FadeIn(l2_cap, shift=UP * 0.15))
        self.play(Write(concl), Create(concl_box))
        self.wait(1)

        # ---------- 右：坐标解码的几何 ----------
        S = 0.45
        shift = RIGHT * 3.3 + DOWN * 0.35
        std_plane = light_plane(x_range=[-6, 8, 1], y_range=[-6, 6, 1], scale=S, shift=shift)
        std_plane.set_stroke(opacity=0.35)
        # 斜基网格：先在原点处做线性变换，再平移
        ob_plane = light_plane(x_range=[-4, 13, 1], y_range=[-7, 7, 1], scale=S)
        ob_plane.apply_function(lambda p: np.array([*(A2 @ p[:2]), 0.0]))
        ob_plane.shift(shift)

        a1_arrow = vec((1, 2), C_A1, S, shift=shift)
        a2_arrow = vec((3, 7), C_A2, S, shift=shift)
        lab_a1 = grid_label(MathTex(r"\mathbf{a}_1", color=C_A1, font_size=32))
        lab_a2 = grid_label(MathTex(r"\mathbf{a}_2", color=C_A2, font_size=32))
        lab_a1.next_to(p3((1, 2), S, shift), LEFT, buff=0.08)
        lab_a2.next_to(p3((3, 7), S, shift), RIGHT, buff=0.08)

        v_pt = np.array([2, 1])
        v_dot = Dot(p3(v_pt, S, shift), color=RED, radius=0.09)
        lab_v = grid_label(MathTex(r"\mathbf{v} = (2, 1)", color=RED, font_size=32))
        lab_v.next_to(p3(v_pt, S, shift), DOWN, buff=0.15)

        self.play(Create(std_plane, run_time=1.2))
        self.play(FadeIn(ob_plane, run_time=1.5))
        self.play(GrowArrow(a1_arrow), GrowArrow(a2_arrow),
                  FadeIn(lab_a1), FadeIn(lab_a2))
        self.play(FadeIn(v_dot), Write(lab_v))
        cap_r = zh("同一个向量 v，两套坐标系给出两份读数",
                   font_size=24, color=GREY_A).add_background_rectangle(opacity=0.6, buff=0.1)
        cap_r.move_to(np.array([3.3, 3.35, 0]))
        self.play(FadeIn(cap_r))

        # 斜基下的分解线：v = 11 a1 - 3 a2
        deco1 = DashedLine(
            p3(v_pt - 4 * np.array([3, 7]), S, shift),
            p3(v_pt + 2 * np.array([3, 7]), S, shift),
            color=YELLOW, stroke_width=3)
        deco2 = DashedLine(
            p3(v_pt - 2 * np.array([1, 2]), S, shift),
            p3(v_pt + 12 * np.array([1, 2]), S, shift),
            color=ORANGE, stroke_width=3)
        self.play(Create(deco1), Create(deco2))
        self.wait(0.5)

        eq_v = MathTex(
            r"\mathbf{v} = 11\,\mathbf{a}_1 - 3\,\mathbf{a}_2", font_size=38,
        ).next_to(concl, DOWN, buff=0.5).align_to(left, LEFT)
        read_E = VGroup(
            zh("标准基读数", font_size=24, color=GREY_A),
            MathTex(r"[\mathbf{v}]_{\mathcal{E}} = \begin{bmatrix} 2 \\ 1 \end{bmatrix}",
                    font_size=34),
        ).arrange(RIGHT, buff=0.2)
        read_A = VGroup(
            zh("斜基读数", font_size=24, color=GREY_A),
            MathTex(r"[\mathbf{v}]_{\mathcal{A}} = \begin{bmatrix} 11 \\ -3 \end{bmatrix}",
                    font_size=34, color=YELLOW),
        ).arrange(RIGHT, buff=0.2)
        reads = VGroup(read_E, read_A).arrange(RIGHT, buff=0.8)
        reads.next_to(eq_v, DOWN, buff=0.35).align_to(eq_v, LEFT)
        self.play(Write(eq_v))
        self.play(FadeIn(read_E, shift=UP * 0.2))
        self.play(FadeIn(read_A, shift=UP * 0.2))
        self.wait(1)

        conv = MathTex(
            r"[\mathbf{v}]_{\mathcal{E}} = A\,[\mathbf{v}]_{\mathcal{A}}"
            r" \quad\Longleftrightarrow\quad"
            r"[\mathbf{v}]_{\mathcal{A}} = A^{-1}[\mathbf{v}]_{\mathcal{E}}",
            font_size=36,
        ).to_edge(DOWN, buff=0.3)
        conv_box = SurroundingRectangle(conv, color=YELLOW, buff=0.15)
        self.play(Write(conv), Create(conv_box))
        self.wait(1.5)

        # 推广：任意两组基
        gen = MathTex(
            r"B_2 = B_1 P \;\Longrightarrow\; P = B_1^{-1}B_2", font_size=36,
        ).next_to(concl, DOWN, buff=0.55).align_to(left, LEFT)
        gen_cap = zh("求逆只是 B₁ = I（标准基）时的特例", font_size=24, color=GREY_A)
        gen_cap.next_to(gen, RIGHT, buff=0.3)
        self.play(FadeOut(eq_v), FadeOut(reads))
        self.play(Write(gen), FadeIn(gen_cap))
        self.wait(2.5)
        self.play(FadeOut(VGroup(std_plane, ob_plane, a1_arrow, a2_arrow, lab_a1, lab_a2,
                                 v_dot, lab_v, cap_r, deco1, deco2,
                                 conv, conv_box, gen, gen_cap, left,
                                 concl, concl_box, title)))


# ================================================================ 消元动力学
class InverseGaussJordan(Scene):
    def construct(self):
        title = scene_title("消元动力学：一边解方程，一边拉直空间")
        self.play(Write(title[0]), Create(title[1]))

        # ---------- 左：增广矩阵的演化 ----------
        g0, l0, r0 = aug([[1, 3], [2, 7]], [[1, 0], [0, 1]])
        g0.move_to(np.array([-3.9, 1.9, 0]))
        g0_label = MathTex(r"[A \mid I]", font_size=34).next_to(g0, UP, buff=0.25)
        self.play(Write(g0), Write(g0_label))

        # ---------- 右：网格的同步演化（ProjectCode 双网格：灰底 = 拉直目标参照）----------
        # 网格单位 0.5 = 向量系数，a1 落到 e1 时与网格线严格对齐
        s = np.array([3.2, -0.3, 0.0])
        base = fit_plane([-14, 14, 1], [-8, 8, 1], 0.5,
                         line_color=GREY_D, line_opacity=0.35, anchor=s)
        plane = fit_plane([-14, 14, 1], [-8, 8, 1], 0.5, anchor=s)
        v1_arrow = vec((1, 0), BLUE, 0.5, shift=s)
        v2_arrow = vec((0, 1), GREEN, 0.5, shift=s)
        grid_group = VGroup(plane, v1_arrow, v2_arrow)
        cap_grid0 = zh("先让 A 把空间扭斜", font_size=24, color=GREY_A)
        cap_grid0.to_corner(UR, buff=0.4).shift(DOWN * 0.75 + LEFT * 0.6)
        self.play(FadeIn(base, run_time=1),
                  Create(plane, run_time=1.2),
                  GrowArrow(v1_arrow), GrowArrow(v2_arrow), FadeIn(cap_grid0))
        self.play(ApplyMatrix(A2, grid_group, about_point=s), run_time=2)
        lab_w1 = grid_label(MathTex(r"\mathbf{a}_1", color=BLUE, font_size=30)).next_to(
            s + p3((1, 2), 0.5), RIGHT, buff=0.08)
        lab_w2 = grid_label(MathTex(r"\mathbf{a}_2", color=GREEN, font_size=30)).next_to(
            s + p3((3, 7), 0.5), RIGHT, buff=0.08)
        self.play(FadeIn(lab_w1), FadeIn(lab_w2), FadeOut(cap_grid0))
        self.wait(0.5)

        # ---- 第一步：R2 <- R2 - 2 R1 ----
        op1 = MathTex(r"R_2 \leftarrow R_2 - 2\,R_1", font_size=34, color=BLUE)
        E1m = MathTex(r"E_1 = \begin{bmatrix} 1 & 0 \\ -2 & 1 \end{bmatrix}", font_size=30)
        op1_row = VGroup(op1, E1m).arrange(RIGHT, buff=0.4)
        op1_row.move_to(np.array([-3.9, 0.45, 0]))
        hl1 = SurroundingRectangle(
            VGroup(l0.get_rows()[1], r0.get_rows()[1]), color=BLUE, buff=0.08)

        g1, l1, r1 = aug([[1, 3], [0, 1]], [[1, 0], [-2, 1]])
        g1.move_to(g0)

        step1_cap = zh("第一步剪切：a₁ 恰好落到 e₁", font_size=24, color=BLUE)
        step1_cap.to_corner(UR, buff=0.4).shift(DOWN * 0.75 + LEFT * 0.6)
        self.play(Create(hl1), Write(op1), Write(E1m))
        self.play(FadeOut(hl1), FadeTransform(g0, g1),
                  ApplyMatrix(E1_SHEAR, grid_group, about_point=s), run_time=2.5)
        lab_after1 = grid_label(MathTex(r"\mathbf{e}_1\,\checkmark", color=BLUE, font_size=30)).next_to(
            s + 0.5 * RIGHT, UR, buff=0.05)
        self.play(FadeOut(lab_w1), FadeIn(lab_after1), FadeIn(step1_cap))
        self.wait(1)

        # ---- 第二步：R1 <- R1 - 3 R2 ----
        op2 = MathTex(r"R_1 \leftarrow R_1 - 3\,R_2", font_size=34, color=PURPLE)
        E2m = MathTex(r"E_2 = \begin{bmatrix} 1 & -3 \\ 0 & 1 \end{bmatrix}", font_size=30)
        op2_row = VGroup(op2, E2m).arrange(RIGHT, buff=0.4)
        op2_row.move_to(np.array([-3.9, -0.85, 0]))
        hl2 = SurroundingRectangle(
            VGroup(l1.get_rows()[0], r1.get_rows()[0]), color=PURPLE, buff=0.08)

        g2, l2, r2 = aug([[1, 0], [0, 1]], [[7, -3], [-2, 1]])
        g2.move_to(g0)

        step2_cap = zh("第二步剪切：a₂ 也落到 e₂，网格拉直", font_size=24, color=GREEN)
        step2_cap.to_corner(UR, buff=0.4).shift(DOWN * 0.75 + LEFT * 0.6)
        self.play(Create(hl2), Write(op2), Write(E2m))
        self.play(FadeOut(hl2), FadeTransform(g1, g2),
                  ApplyMatrix(E2_SHEAR, grid_group, about_point=s), run_time=2.5)
        lab_after2 = grid_label(MathTex(r"\mathbf{e}_2\,\checkmark", color=GREEN, font_size=30)).next_to(
            s + 0.5 * UP, LEFT, buff=0.05)
        self.play(FadeOut(lab_w2), FadeIn(lab_after2),
                  FadeOut(step1_cap), FadeIn(step2_cap))
        self.wait(1)

        # ---- 收官 ----
        final_box = SurroundingRectangle(r2, color=YELLOW, buff=0.12)
        fin1 = MathTex(
            r"E_2 E_1 = \begin{bmatrix} 7 & -3 \\ -2 & 1 \end{bmatrix} = A^{-1}",
            font_size=36, color=YELLOW,
        ).move_to(np.array([-3.9, -2.2, 0]))
        fin2 = zh("右侧同步经历相同剪切，累积记录 = A⁻¹", font_size=24, color=GREY_A)
        fin2.next_to(fin1, DOWN, buff=0.2)
        self.play(Create(final_box), Write(fin1), FadeIn(fin2, shift=UP * 0.2))
        self.play(Indicate(l2, color=GREEN), Indicate(plane, scale_factor=1.01))
        self.wait(1)

        ess = zh("初等行变换 = 左乘剪切算子：把斜网格连续同胚地形变回正交网格",
                 font_size=26, color=TEAL_A)
        ess.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(ess, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(VGroup(g2, g0_label, op1_row, op2_row, final_box, fin1, fin2,
                                 base, grid_group, lab_after1, lab_after2, step2_cap,
                                 ess, title)))


# ================================================================ 全局闭环
class InverseGlobalMap(Scene):
    def construct(self):
        title = scene_title("全局闭环：逆矩阵串起的高等代数地图")
        self.play(Write(title[0]), Create(title[1]))

        def node(text_mobj, w, h, color):
            box = RoundedRectangle(corner_radius=0.12, width=w, height=h,
                                   stroke_color=color, fill_color=color, fill_opacity=0.18)
            return VGroup(box, text_mobj)

        n1 = node(zh("线性方程组  Ax = b", font_size=28, weight=BOLD), 4.6, 0.7, BLUE)
        n1.move_to(np.array([0, 3.0, 0]))
        n2 = node(zh("矩阵代数 · 初等行变换", font_size=28, weight=BOLD), 4.6, 0.7, BLUE)
        n2.move_to(np.array([0, 1.85, 0]))
        n3 = node(zh("逆矩阵 A⁻¹", font_size=32, weight=BOLD), 4.0, 0.8, GOLD)
        n3.move_to(np.array([0, 0.6, 0]))
        n4 = node(zh("向量空间 · 基 · 过渡矩阵 P", font_size=28, weight=BOLD), 5.2, 0.7, TEAL)
        n4.move_to(np.array([0, -0.6, 0]))

        n5l_box = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.7,
                                   stroke_color=PURPLE, fill_color=PURPLE, fill_opacity=0.18)
        n5l_text = MathTex(r"[\mathbf{v}]_{\mathcal{A}} = A^{-1}[\mathbf{v}]_{\mathcal{E}}",
                           font_size=30)
        n5l_text_pre = zh("坐标反变：", font_size=24, color=GREY_A)
        n5l_in = VGroup(n5l_text_pre, n5l_text).arrange(RIGHT, buff=0.15)
        n5l = VGroup(n5l_box, n5l_in).move_to(np.array([-3.6, -1.8, 0]))

        n5r_box = RoundedRectangle(corner_radius=0.12, width=4.4, height=0.7,
                                   stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.18)
        n5r_text = MathTex(r"B = P^{-1}AP", font_size=30)
        n5r_text_pre = zh("相似变换：", font_size=24, color=GREY_A)
        n5r_in = VGroup(n5r_text_pre, n5r_text).arrange(RIGHT, buff=0.15)
        n5r = VGroup(n5r_box, n5r_in).move_to(np.array([3.6, -1.8, 0]))

        n6l_box = RoundedRectangle(corner_radius=0.12, width=5.0, height=0.7,
                                   stroke_color=ORANGE, fill_color=ORANGE, fill_opacity=0.18)
        n6l_text = MathTex(r"\langle \mathbf{r}_i, \mathbf{x}_j \rangle = \delta_{ij}",
                           font_size=30)
        n6l_text_pre = zh("对偶空间：", font_size=24, color=GREY_A)
        n6l_in = VGroup(n6l_text_pre, n6l_text).arrange(RIGHT, buff=0.15)
        n6l = VGroup(n6l_box, n6l_in).move_to(np.array([-3.6, -3.0, 0]))

        n6r_box = RoundedRectangle(corner_radius=0.12, width=4.4, height=0.7,
                                   stroke_color=GREEN, fill_color=GREEN, fill_opacity=0.18)
        n6r = VGroup(n6r_box, zh("特征值 · 谱分解 · SVD", font_size=24)).move_to(
            np.array([3.6, -3.0, 0]))

        arrows = VGroup(
            Arrow(n1.get_bottom(), n2.get_top(), buff=0.08, stroke_width=4),
            Arrow(n2.get_bottom(), n3.get_top(), buff=0.08, stroke_width=4),
            Arrow(n3.get_bottom(), n4.get_top(), buff=0.08, stroke_width=4),
            Arrow(n4.get_bottom() + LEFT * 1.6, n5l.get_top(), buff=0.08, stroke_width=4),
            Arrow(n4.get_bottom() + RIGHT * 1.6, n5r.get_top(), buff=0.08, stroke_width=4),
            Arrow(n5l.get_bottom(), n6l.get_top(), buff=0.08, stroke_width=4),
            Arrow(n5r.get_bottom(), n6r.get_top(), buff=0.08, stroke_width=4),
        )
        # 反馈弧：对偶配对回到逆矩阵
        back = CurvedArrow(
            n6l.get_left() + LEFT * 0.1, n3.get_left() + LEFT * 0.1,
            angle=-TAU / 6, color=ORANGE, stroke_width=3, tip_length=0.18,
        )
        back_lab = zh("双正交配对", font_size=20, color=ORANGE)
        back_lab.move_to(np.array([-5.9, -1.2, 0]))

        self.play(AnimationGroup(*[FadeIn(n, scale=0.8) for n in (n1, n2, n3, n4)],
                                 lag_ratio=0.25))
        self.play(AnimationGroup(*[FadeIn(n, scale=0.8) for n in (n5l, n5r, n6l, n6r)],
                                 lag_ratio=0.2))
        self.play(AnimationGroup(*[GrowArrow(a) for a in arrows], lag_ratio=0.15))
        self.play(Create(back), FadeIn(back_lab))
        self.wait(2)

        # ---------- 片尾总结 ----------
        self.play(FadeOut(VGroup(n1, n2, n3, n4, n5l, n5r, n6l, n6r,
                                 arrows, back, back_lab, title)))

        finale_title = zh("A⁻¹ 的四重身份", font_size=46, weight=BOLD)
        finale_title.set_color_by_gradient(BLUE_B, TEAL_A, GREEN_B)
        finale_title.move_to(np.array([0, 2.6, 0]))
        self.play(Write(finale_title))

        chips_data = [
            ("解耦器", "n 个方程各自独立求解", BLUE),
            ("还原器", "把扭曲的空间拉回正交", GREEN),
            ("解码器", "直角坐标 → 斜坐标读数", ORANGE),
            ("拉直器", "消元 = 空间的连续校正", PURPLE),
        ]
        chips = VGroup()
        for name, desc, col in chips_data:
            box = RoundedRectangle(corner_radius=0.14, width=3.2, height=1.5,
                                   stroke_color=col, fill_color=col, fill_opacity=0.15)
            chip = VGroup(zh(name, font_size=30, weight=BOLD, color=col),
                          zh(desc, font_size=19, color=GREY_A)).arrange(DOWN, buff=0.2)
            chips.add(VGroup(box, chip))
        chips.arrange(RIGHT, buff=0.35).move_to(np.array([0, 0.4, 0]))
        self.play(AnimationGroup(*[FadeIn(c, scale=0.7) for c in chips], lag_ratio=0.15))
        self.wait(1)

        final_formula = MathTex(r"AX = XA = I", font_size=56)
        final_formula.move_to(np.array([0, -1.7, 0]))
        final_word = zh("逆矩阵不是除法，而是空间语言之间的翻译",
                        font_size=28, color=TEAL_A)
        final_word.move_to(np.array([0, -2.9, 0]))
        self.play(Write(final_formula))
        self.play(FadeIn(final_word, shift=UP * 0.2))
        self.wait(3)
        self.play(FadeOut(VGroup(finale_title, chips, final_formula, final_word)))
