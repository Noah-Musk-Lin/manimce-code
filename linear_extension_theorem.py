#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
线性扩张定理 — Manim 动画（3b1b 风格）
手动 ApplyMatrix 实现网格平滑变形，避免 LinearTransformationScene bug。
"""

from manim import *
import numpy as np

# ═══════════════════════════════════════════════
# 颜色常量
# ═══════════════════════════════════════════════
C_TITLE = BLUE
C_KEY = YELLOW
C_RESULT = GREEN
C_AUX = GRAY
C_VEC = YELLOW
C_I = RED
C_J = BLUE
C_BG = "#1e1e1e"

# 变换矩阵: β₁=(1, 0.6), β₂=(0.4, 1)
MATRIX = np.array([[1.0, 0.4], [0.6, 1.0]])
V_SAMPLE = np.array([2.0, 1.5])          # 示例向量
PHI_V = MATRIX @ V_SAMPLE                 # (2.6, 2.7)


def to_3d(v):
    """2D → 3D 坐标"""
    return np.array([v[0], v[1], 0.0])


# ═══════════════════════════════════════════════
# Scene 1: ℝ²→ℝ² 线性变换 — 核心可视化
# ═══════════════════════════════════════════════
class LinearExtensionScene1(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        # ── 标题 ──
        title = Text("线性扩张定理：由基决定的线性映射", font_size=38, color=C_TITLE)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=0.8)
        self.wait(0.3)

        # ── 映射规则 ──
        rule = VGroup(
            Text("选定基的像：", font_size=24, color=WHITE),
            Tex(r"$\varphi(\hat{\imath})=\beta_1=\begin{pmatrix}1\\0.6\end{pmatrix}$",
                color=C_I, font_size=30),
            Tex(r"$\varphi(\hat{\jmath})=\beta_2=\begin{pmatrix}0.4\\1\end{pmatrix}$",
                color=C_J, font_size=30),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rule.to_corner(UL, buff=0.4)
        rule.next_to(title, DOWN, buff=0.6, aligned_edge=LEFT)
        self.play(Write(rule[0]), run_time=0.4)
        self.play(Write(rule[1]))
        self.play(Write(rule[2]))
        self.wait(0.8)

        # ── 平面 + 网格 ──
        plane = NumberPlane(
            x_range=(-5, 5, 1),
            y_range=(-5, 5, 1),
            x_length=11,
            y_length=7.5,
            background_line_style={
                "stroke_color": GRAY,
                "stroke_opacity": 0.28,
                "stroke_width": 0.5,
            },
            axis_config={
                "stroke_color": WHITE,
                "stroke_width": 2.5,
                "stroke_opacity": 0.85,
            },
            faded_line_ratio=0,  # 让所有网格线相同
        )
        plane.move_to(ORIGIN)

        # 基向量箭头（使用 plane.c2p 确保与网格对齐）
        a1 = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), color=C_I, buff=0,
                   stroke_width=5, max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), color=C_J, buff=0,
                   stroke_width=5, max_tip_length_to_length_ratio=0.15)
        la1 = MathTex(r"\alpha_1", color=C_I, font_size=32)
        la1.next_to(a1.get_end(), DR, buff=0.1)
        la2 = MathTex(r"\alpha_2", color=C_J, font_size=32)
        la2.next_to(a2.get_end(), UL, buff=0.1)

        # 示例向量 v
        v_arrow = Arrow(plane.c2p(0, 0), plane.c2p(V_SAMPLE[0], V_SAMPLE[1]),
                        color=C_VEC, buff=0,
                        stroke_width=5, max_tip_length_to_length_ratio=0.12)
        lv = MathTex(r"\mathbf{v} = (2,\,1.5)", color=C_VEC, font_size=30)
        lv.next_to(v_arrow.get_end(), UR, buff=0.12)

        self.play(
            FadeIn(plane, shift=DOWN * 0.3),
            GrowArrow(a1), GrowArrow(a2), GrowArrow(v_arrow),
            Write(la1), Write(la2), Write(lv),
            run_time=1.2,
        )
        self.wait(0.6)

        # ── 清文字，准备变换 ──
        self.play(
            FadeOut(VGroup(rule, la1, la2, lv)),
            run_time=0.5,
        )

        # ── ★ 核心动画：矩阵施加，网格 + 向量同步变形 ★ ──
        self.play(
            ApplyMatrix(MATRIX, plane),
            ApplyMatrix(MATRIX, a1),
            ApplyMatrix(MATRIX, a2),
            ApplyMatrix(MATRIX, v_arrow),
            run_time=3.5,
            rate_func=smooth,
        )
        self.wait(0.5)

        # ── 变换后标注 ──
        # 直接用变换后箭头的实际位置
        b1_label = MathTex(r"\beta_1", color=C_I, font_size=36)
        b1_label.next_to(a1.get_end(), DR, buff=0.12)
        b2_label = MathTex(r"\beta_2", color=C_J, font_size=36)
        b2_label.next_to(a2.get_end(), UL, buff=0.12)

        # φ(v) 标签
        phi_label = MathTex(
            r"\varphi(\mathbf{v}) = (2.6,\,2.7)",
            color=C_VEC, font_size=30,
        )
        phi_label.next_to(v_arrow.get_end(), UR, buff=0.12)

        self.play(
            Write(b1_label), Write(b2_label), Write(phi_label),
            run_time=1.0,
        )
        self.wait(0.6)

        # ── 关键洞察 ──
        insight1 = Text("关键发现：坐标 (2, 1.5) 保持不变！", font_size=34, color=C_KEY)
        insight1.to_edge(DOWN, buff=0.3)

        insight2 = Text("基从 α₁,α₂ 变成 β₁,β₂ → 向量位置改变，但坐标系数不变", font_size=22, color=C_AUX)
        insight2.next_to(insight1, DOWN, buff=0.08)

        rect_insight = SurroundingRectangle(
            VGroup(insight1, insight2), color=C_KEY, buff=0.18
        )

        self.play(
            Write(insight1), Write(insight2), Create(rect_insight),
            run_time=1.5,
        )
        self.wait(3.0)

        # ── 清理 + 总结 ──
        self.play(
            FadeOut(VGroup(
                plane, a1, a2, v_arrow, title,
                b1_label, b2_label, phi_label,
                insight1, insight2, rect_insight,
            )),
            run_time=0.6,
        )

        summary = VGroup(
            Text("核心思想", font_size=42, color=C_TITLE),
            Text("基的像一旦确定，整个线性映射就完全固定", font_size=30, color=WHITE),
            Text("坐标不变，基变 → 空间随之变形", font_size=24, color=C_AUX),
        ).arrange(DOWN, buff=0.35)
        summary.move_to(ORIGIN)

        for s in summary:
            self.play(Write(s), run_time=0.5)
        self.wait(2.5)
        self.play(FadeOut(summary), run_time=0.5)


# ═══════════════════════════════════════════════
# Scene 2: 证明概要 + ℝ²→ℝ³ 示例 + 矩阵联系
# ═══════════════════════════════════════════════
class LinearExtensionScene2(Scene):
    def construct(self):
        self.camera.background_color = C_BG

        # ===== Part A: 证明概要 =====
        ta = Text("证明概要：存在性 + 唯一性", font_size=40, color=C_TITLE)
        ta.to_edge(UP, buff=0.4)
        self.play(Write(ta))

        s1 = VGroup(
            MathTex(
                r"x = x_1\alpha_1 + x_2\alpha_2 + \cdots + x_n\alpha_n",
                color=C_KEY, font_size=32,
            ),
            Text("基表示 → 坐标唯一确定", font_size=22, color=C_AUX),
        ).arrange(DOWN, buff=0.18)
        s1.next_to(ta, DOWN, buff=0.7)
        self.play(Write(s1[0]), Write(s1[1]))
        self.wait(0.5)

        s2 = VGroup(
            MathTex(
                r"\varphi(x) = x_1\beta_1 + x_2\beta_2 + \cdots + x_n\beta_n",
                color=C_RESULT, font_size=32,
            ),
            Text("← 系数 xᵢ 完全相同！", font_size=24, color=C_KEY),
        ).arrange(DOWN, buff=0.18)
        s2.next_to(s1, DOWN, buff=0.45)
        self.play(Write(s2[0]), Write(s2[1]))
        self.wait(0.5)

        s3 = MathTex(
            r"\psi(x) = \sum_{i} x_i\psi(\alpha_i)"
            r" = \sum_{i} x_i\beta_i = \varphi(x)",
            color=C_RESULT, font_size=30,
        )
        s3.next_to(s2, DOWN, buff=0.4)
        s3n = Text("→ 线性性强制决定唯一性", font_size=24, color=C_AUX)
        s3n.next_to(s3, DOWN, buff=0.15)
        self.play(Write(s3), Write(s3n))
        self.wait(1.5)

        self.play(FadeOut(VGroup(ta, s1, s2, s3, s3n)), run_time=0.5)

        # ===== Part B: ℝ² → ℝ³ 高维示例 =====
        tb = Text("高维示例：ℝ² → ℝ³", font_size=38, color=C_TITLE)
        tb.to_edge(UP, buff=0.4)
        self.play(Write(tb))

        # 左侧 ℝ² 平面
        p2d = NumberPlane(
            x_range=(-3, 3, 1), y_range=(-3, 3, 1),
            x_length=4.2, y_length=4.2,
            background_line_style={
                "stroke_color": GRAY, "stroke_opacity": 0.22, "stroke_width": 0.4,
            },
            axis_config={
                "stroke_color": WHITE, "stroke_width": 1.6, "stroke_opacity": 0.7,
            },
        )
        p2d.to_edge(LEFT, buff=0.6)
        dl = Text("ℝ² 定义域", font_size=20, color=C_AUX)
        dl.next_to(p2d, DOWN, buff=0.12)
        self.play(FadeIn(p2d), Write(dl))

        a1 = Arrow(p2d.c2p(0, 0), p2d.c2p(1, 0),
                   color=C_I, buff=0, stroke_width=4,
                   max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(p2d.c2p(0, 0), p2d.c2p(0, 1),
                   color=C_J, buff=0, stroke_width=4,
                   max_tip_length_to_length_ratio=0.15)
        la1 = MathTex(r"\alpha_1", color=C_I, font_size=26)
        la1.next_to(p2d.c2p(1, 0), DOWN, buff=0.06)
        la2 = MathTex(r"\alpha_2", color=C_J, font_size=26)
        la2.next_to(p2d.c2p(0, 1), LEFT, buff=0.06)
        self.play(GrowArrow(a1), GrowArrow(a2), Write(la1), Write(la2))

        v2 = np.array([2.0, -3.0])
        av = Arrow(p2d.c2p(0, 0), p2d.c2p(v2[0], v2[1]),
                   color=C_VEC, buff=0, stroke_width=4,
                   max_tip_length_to_length_ratio=0.12)
        lv = MathTex(r"\mathbf{v}=(2,-3)", color=C_VEC, font_size=24)
        lv.next_to(p2d.c2p(v2[0], v2[1]), DR, buff=0.06)
        self.play(GrowArrow(av), Write(lv))
        self.wait(0.4)

        # 右侧面板
        rp = VGroup(
            Text("ℝ³ 值域", font_size=22, color=C_AUX),
            Tex(r"$\beta_1=\begin{pmatrix}1\\2\\3\end{pmatrix},\;"
                r"\beta_2=\begin{pmatrix}4\\5\\6\end{pmatrix}$",
                color=C_KEY, font_size=28),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rp.to_edge(RIGHT, buff=0.6)
        rp.shift(UP * 1.0)
        self.play(Write(rp[0]), Write(rp[1]))
        self.wait(0.4)

        arrow_m = MathTex(r"\xrightarrow{\quad\varphi\quad}", color=C_KEY, font_size=38)
        arrow_m.move_to(RIGHT * 0.25)

        calc = VGroup(
            MathTex(
                r"\varphi(\mathbf{v}) = 2\beta_1 + (-3)\beta_2",
                color=WHITE, font_size=26,
            ),
            MathTex(
                r"= \begin{pmatrix}-10\\-11\\-12\end{pmatrix}",
                color=C_RESULT, font_size=30,
            ),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        calc.next_to(rp, DOWN, buff=0.5)

        self.play(Write(arrow_m))
        self.play(Write(calc[0]))
        self.wait(0.3)
        self.play(Write(calc[1]))
        self.wait(1.5)

        cn = VGroup(
            Text("坐标 ", font_size=22, color=C_AUX),
            MathTex(r"(2,\,-3)", color=C_KEY, font_size=26),
            Text(" 从 ℝ² 传递到 ℝ³", font_size=22, color=C_AUX),
        ).arrange(RIGHT, buff=0.08)
        cn.next_to(calc, DOWN, buff=0.35)
        cn_rect = SurroundingRectangle(cn, color=C_KEY, buff=0.15)
        self.play(Write(cn), Create(cn_rect))
        self.wait(2.0)

        self.play(FadeOut(VGroup(
            tb, p2d, dl, a1, a2, la1, la2, av, lv,
            rp, calc, arrow_m, cn, cn_rect,
        )), run_time=0.5)

        # ===== Part C: 总结 + 矩阵联系 =====
        tc = Text("总结：线性扩张定理的意义", font_size=38, color=C_TITLE)
        tc.to_edge(UP, buff=0.4)
        self.play(Write(tc))

        left = VGroup(
            Text("🆓  自由度", font_size=34, color=C_RESULT),
            Text("基上可任意指定像", font_size=24, color=WHITE),
            Text("构造出线性映射", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        right = VGroup(
            Text("🔒  约束", font_size=34, color=C_KEY),
            Text("基的像一旦确定", font_size=24, color=WHITE),
            Text("全空间映射锁定", font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)

        cols = VGroup(left, right).arrange(RIGHT, buff=2.0)
        cols.next_to(tc, DOWN, buff=0.7)
        self.play(Write(left))
        self.play(Write(right))
        self.wait(0.8)

        mt = Text("矩阵表示线性变换的本质", font_size=28, color=C_TITLE)
        mt.next_to(cols, DOWN, buff=0.7)
        meq = MathTex(
            r"\varphi \longleftrightarrow "
            r"M = \bigl(\beta_1\;\beta_2\;\cdots\;\beta_n\bigr)",
            color=WHITE, font_size=30,
        )
        meq.next_to(mt, DOWN, buff=0.25)
        mn = Text("矩阵的列 = 基向量的像", font_size=26, color=C_KEY)
        mn.next_to(meq, DOWN, buff=0.2)
        mrect = SurroundingRectangle(VGroup(meq, mn), color=C_RESULT, buff=0.3)

        self.play(Write(mt))
        self.play(Write(meq), Write(mn))
        self.play(Create(mrect))
        self.wait(2.5)

        self.play(FadeOut(VGroup(tc, cols, mt, meq, mn, mrect)), run_time=0.5)

        end = VGroup(
            Text("感谢观看", font_size=44, color=C_TITLE),
            Text("线性是由基决定的", font_size=24, color=C_AUX),
        ).arrange(DOWN, buff=0.3)
        end.move_to(ORIGIN)
        self.play(Write(end[0]), Write(end[1]))
        self.wait(2.5)
        self.play(FadeOut(end), run_time=0.5)
