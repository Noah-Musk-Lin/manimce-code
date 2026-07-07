# -*- coding: utf-8 -*-
r"""复仿射线性变换存在性与唯一性证明
运行: manim -qh "affine_proof.py" AffineProof
"""
from manim import *
import numpy as np

config.pixel_height = 1080
config.pixel_width = 1920
config.frame_rate = 60

# ═══════════════════════════════════
# 颜色方案
# ═══════════════════════════════════
C_SOURCE   = BLUE
C_TARGET   = ORANGE
C_STEP     = GREEN
C_DET      = YELLOW
C_KEY      = GOLD
C_CHECK    = GREEN
C_LINK     = TEAL

G7 = [BLUE, TEAL, GREEN, YELLOW, GOLD, RED, PURPLE]

# ═══════════════════════════════════
# 布局常量（平面几何 skill）
# ═══════════════════════════════════
PROOF_X       = 2.5
FIG_POS       = [-4.8, -0.2, 0]
FIG_SCALE     = 0.75
FIG_RETURN    = 1.333
PROOF_Y_START = 1.2
LINE_GAP      = 0.80

CN_FONT = "SimSun"


# ═══════════════════════════════════
# 模块级辅助函数
# ═══════════════════════════════════
def make_proof_line(y_offset, elements, scale_factor=0.9):
    """创建证明行，居中于右侧 PROOF_X"""
    parts = []
    for typ, content, clr in elements:
        if typ == 'T':
            parts.append(Text(content, font=CN_FONT, font_size=38, color=clr))
        elif typ == 'M':
            parts.append(MathTex(content, font_size=44, color=clr))
    line = VGroup(*parts).arrange(RIGHT, buff=0.18)
    line.scale(scale_factor)
    line.move_to([PROOF_X, PROOF_Y_START - y_offset * LINE_GAP, 0])
    return line


def make_problem_line(y_idx, elements, scale_factor=0.9):
    """抄题区域的行（居中于屏幕）"""
    parts = []
    for typ, content, clr in elements:
        if typ == 'T':
            parts.append(Text(content, font=CN_FONT, font_size=34, color=clr))
        elif typ == 'M':
            parts.append(MathTex(content, font_size=40, color=clr))
    line = VGroup(*parts).arrange(RIGHT, buff=0.18)
    line.scale(scale_factor)
    line.move_to([0, 1.2 - y_idx * 1.0, 0])
    return line


# ═══════════════════════════════════
# 主场景
# ═══════════════════════════════════
class AffineProof(Scene):
    def construct(self):
        # ===== PART 0: 标题 =====
        title_main = Text("复仿射线性变换", font=CN_FONT, font_size=68)
        title_sub  = Text("存在性与唯一性证明", font=CN_FONT, font_size=84, color=YELLOW)
        title = VGroup(title_main, title_sub).arrange(DOWN, buff=0.2)
        title.set_color_by_gradient(*G7)
        self.play(Write(title[0]), Write(title[1]))
        self.wait(1.5)
        self.play(FadeOut(title), run_time=0.5)

        # ===== PART 1: 抄题（全屏居中）=====
        prob = self.show_problem()
        self.wait(2.5)
        self.play(FadeOut(prob), run_time=0.7)

        # ===== PART 2: 绘图（全屏居中）=====
        fig = self.draw_figure()
        self.wait(1.0)

        # ===== PART 3: 图形去左侧 =====
        self.play(fig['all'].animate.scale(FIG_SCALE).move_to(FIG_POS), run_time=1.5)
        self.wait(0.45)

        # ===== PART 4: 分页证明 =====
        kept = self.proof_scene1_equations()         # 场景一前半：方程组
        kept = self.proof_scene1_determinant(kept)    # 场景一后半：行列式
        self.proof_scene2_properties(fig)             # 场景二：重心性质 + 图动
        self.proof_scene3_linearity(fig)              # 场景三：线性验证 + 图动

        # ===== END: 结论 =====
        self.show_conclusion(fig)

    # ═════════════════════════════════════════
    # PART 1: 抄题
    # ═════════════════════════════════════════
    def show_problem(self):
        box = RoundedRectangle(
            width=11.5, height=5.2, corner_radius=0.15,
            stroke_color=TEAL, stroke_width=2.5,
            fill_color="#0D1117", fill_opacity=0.95,
        )
        box.move_to(ORIGIN)

        prob_title = Text("已知与求证", font=CN_FONT, font_size=40)
        prob_title.set_color_by_gradient(*G7[:5])
        prob_title.next_to(box, UP, buff=0.2)

        L1 = make_problem_line(0, [
            ('T', '已知：源点 ', WHITE),
            ('M', r'1,\ \omega,\ \omega^2', C_SOURCE),
            ('T', ' 在复平面上构成以原点为重心的正三角形', WHITE),
        ])
        L2 = make_problem_line(1, [
            ('M', r'\omega = e^{\frac{2\pi i}{3}},\quad 1+\omega+\omega^2=0', TEAL),
        ])
        L3 = make_problem_line(2, [
            ('T', '目标点 ', WHITE),
            ('M', r'z_1,\ z_2,\ z_3', C_TARGET),
            ('T', ' 满足 ', WHITE),
            ('M', r'z_1+z_2+z_3=0', C_TARGET),
            ('T', '，且三点不共线', WHITE),
        ])
        L4 = make_problem_line(3, [
            ('T', '求证：', WHITE),
            ('M', r'\exists! \ T(w)=uw+v\overline{w},\ \ u,v\in\mathbb{C}', YELLOW),
        ], scale_factor=0.82)

        for ln in [L1, L2, L3, L4]:
            ln.move_to([0, ln.get_y(), 0])

        lines = VGroup(L1, L2, L3, L4)

        self.play(FadeIn(box), Write(prob_title), run_time=1.0)
        self.play(Write(L1), run_time=1.5)
        self.play(Write(L2), run_time=1.5)
        self.play(Write(L3), run_time=1.5)
        self.play(Write(L4), run_time=2.0)

        return VGroup(box, prob_title, lines)

    # ═════════════════════════════════════════
    # PART 2: 绘图
    # ═════════════════════════════════════════
    def draw_figure(self):
        R = 1.5  # 单位圆半径

        # ----- 坐标轴 -----
        ax_len = 3.2
        x_axis = Arrow([-ax_len, 0, 0], [ax_len, 0, 0], buff=0,
                       stroke_width=1.8, color=WHITE)
        y_axis = Arrow([0, -ax_len, 0], [0, ax_len, 0], buff=0,
                       stroke_width=1.8, color=WHITE)
        re_label = MathTex(r"\operatorname{Re}", font_size=32, color=WHITE)
        re_label.next_to(x_axis.get_end(), RIGHT, buff=0.15)
        im_label = MathTex(r"\operatorname{Im}", font_size=32, color=WHITE)
        im_label.next_to(y_axis.get_end(), UP, buff=0.15)
        origin = Dot(ORIGIN, radius=0.06, color=WHITE)
        o_label = MathTex("O", font_size=30, color=WHITE).next_to(origin, DL, buff=0.10)

        # ----- 单位圆 -----
        unit_circle = Circle(radius=R, color="#555566", stroke_width=1.2)
        unit_circle.set_opacity(0.45)

        # ----- 源点: 1, ω, ω² -----
        p1  = np.array([R, 0, 0])
        pw  = np.array([R * np.cos(2*PI/3),  R * np.sin(2*PI/3),  0])
        pw2 = np.array([R * np.cos(4*PI/3),  R * np.sin(4*PI/3),  0])

        d1  = Dot(p1,  radius=0.12, color=C_SOURCE)
        dw  = Dot(pw,  radius=0.12, color=C_SOURCE)
        dw2 = Dot(pw2, radius=0.12, color=C_SOURCE)

        lb1  = MathTex("1",        font_size=40, color=C_SOURCE).next_to(d1,  RIGHT, buff=0.15)
        lbw  = MathTex(r"\omega",  font_size=40, color=C_SOURCE).next_to(dw,  UL,    buff=0.12)
        lbw2 = MathTex(r"\omega^2",font_size=40, color=C_SOURCE).next_to(dw2, DL,    buff=0.12)

        src_tri = Polygon(p1, pw, pw2,
                          stroke_color=C_SOURCE, stroke_width=2.8,
                          fill_color=C_SOURCE, fill_opacity=0.12)

        # ----- 目标点: z₁, z₂, z₃ -----
        z1 = np.array([ 2.0,  0.5, 0])
        z2 = np.array([-1.0,  1.5, 0])
        z3 = np.array([-1.0, -2.0, 0])

        dz1 = Dot(z1, radius=0.12, color=C_TARGET)
        dz2 = Dot(z2, radius=0.12, color=C_TARGET)
        dz3 = Dot(z3, radius=0.12, color=C_TARGET)

        lz1 = MathTex("z_1", font_size=40, color=C_TARGET).next_to(dz1, RIGHT, buff=0.15)
        lz2 = MathTex("z_2", font_size=40, color=C_TARGET).next_to(dz2, UL,    buff=0.12)
        lz3 = MathTex("z_3", font_size=40, color=C_TARGET).next_to(dz3, DOWN,  buff=0.12)

        _raw_tri = Polygon(z1, z2, z3,
                           stroke_color=C_TARGET, stroke_width=2.8,
                           fill_color=C_TARGET, fill_opacity=0.10)
        tgt_tri = DashedVMobject(_raw_tri, num_dashes=28)

        # ----- 重心标记 -----
        c_size = 0.18
        c1 = Line([-c_size, -c_size, 0], [c_size, c_size, 0],
                  stroke_color="#888899", stroke_width=1.5)
        c2 = Line([-c_size,  c_size, 0], [c_size, -c_size, 0],
                  stroke_color="#888899", stroke_width=1.5)
        centroid_mark = VGroup(c1, c2)
        centroid_note = Text("重心", font=CN_FONT, font_size=22, color="#888899")
        centroid_note.next_to(origin, RIGHT, buff=0.35)

        # ----- 图例 -----
        leg_src = VGroup(
            Dot(ORIGIN, radius=0.07, color=C_SOURCE),
            MathTex(r"1,\omega,\omega^2", font_size=28, color=C_SOURCE),
        ).arrange(RIGHT, buff=0.12)
        leg_tgt = VGroup(
            Dot(ORIGIN, radius=0.07, color=C_TARGET),
            MathTex(r"z_1,z_2,z_3", font_size=28, color=C_TARGET),
        ).arrange(RIGHT, buff=0.12)
        legend = VGroup(leg_src, leg_tgt).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to([0, -2.8, 0])

        # ----- 收集全部元素 -----
        all_elements = VGroup(
            x_axis, y_axis, re_label, im_label,
            origin, o_label, centroid_mark, centroid_note,
            unit_circle,
            src_tri, d1, dw, dw2, lb1, lbw, lbw2,
            tgt_tri, dz1, dz2, dz3, lz1, lz2, lz3,
            legend,
        )

        # ----- 逐步绘制 -----
        self.play(Create(x_axis), Create(y_axis), run_time=1.0)
        self.play(Write(re_label), Write(im_label), run_time=0.6)
        self.play(FadeIn(origin), Write(o_label), run_time=0.5)
        self.play(Create(unit_circle), run_time=1.5)

        self.play(Create(src_tri), run_time=1.0)
        self.play(
            FadeIn(d1), FadeIn(dw), FadeIn(dw2),
            Write(lb1), Write(lbw), Write(lbw2),
            run_time=1.2,
        )

        self.play(Create(tgt_tri), run_time=1.0)
        self.play(
            FadeIn(dz1), FadeIn(dz2), FadeIn(dz3),
            Write(lz1), Write(lz2), Write(lz3),
            run_time=1.2,
        )
        self.play(FadeIn(centroid_mark), Write(centroid_note), run_time=0.6)
        self.play(FadeIn(legend), run_time=0.8)

        return {
            'all':     all_elements,
            'axes':    VGroup(x_axis, y_axis, re_label, im_label),
            'origin':  VGroup(origin, o_label, centroid_mark, centroid_note),
            'uc':      unit_circle,
            'src_pts': [d1, dw, dw2],
            'src_lbl': [lb1, lbw, lbw2],
            'src_tri': src_tri,
            'tgt_pts': [dz1, dz2, dz3],
            'tgt_lbl': [lz1, lz2, lz3],
            'tgt_tri': tgt_tri,
            'legend':  legend,
        }

    # ═════════════════════════════════════════
    # PART 4a: 场景一（前半）— 建立方程组
    # ═════════════════════════════════════════
    def proof_scene1_equations(self):
        """返回最后一行供下页衔接"""
        step = make_proof_line(0, [
            ('T', '▎第一步：建立线性方程组', C_STEP),
        ])
        eq1 = make_proof_line(1, [
            ('M', r'u+v = z_1', WHITE),
        ])
        num1 = MathTex(r"\cdots (1)", font_size=44, color=C_KEY)
        num1.next_to(eq1, RIGHT, buff=0.45)
        eq1_grp = VGroup(eq1, num1)
        eq1_grp.move_to([PROOF_X, PROOF_Y_START - 1 * LINE_GAP, 0])

        eq2 = make_proof_line(2, [
            ('M', r'u\omega+v\omega^2 = z_2', WHITE),
        ])
        num2 = MathTex(r"\cdots (2)", font_size=44, color=C_KEY)
        num2.next_to(eq2, RIGHT, buff=0.45)
        eq2_grp = VGroup(eq2, num2)
        eq2_grp.move_to([PROOF_X, PROOF_Y_START - 2 * LINE_GAP, 0])

        note = make_proof_line(3, [
            ('T', '代入前两个对应点 ', WHITE),
            ('M', r'1\mapsto z_1,\ \ \omega\mapsto z_2', WHITE),
        ])

        self.play(Write(step), run_time=1.2)
        self.wait(0.3)
        self.play(Write(eq1), Write(num1), run_time=1.5)
        self.wait(0.5)
        self.play(Write(eq2), Write(num2), run_time=1.5)
        self.wait(0.5)
        self.play(Write(note), run_time=1.0)
        self.wait(3.0)

        # 淡出前 3 行，保留 eq2_grp 上移
        self.play(
            FadeOut(step), FadeOut(eq1_grp), FadeOut(note),
            eq2_grp.animate.move_to([PROOF_X, PROOF_Y_START - 0 * LINE_GAP, 0]),
            run_time=0.8,
        )
        return eq2_grp

    # ═════════════════════════════════════════
    # PART 4b: 场景一（后半）— 行列式判唯一解
    # ═════════════════════════════════════════
    def proof_scene1_determinant(self, kept_line):
        """kept_line 来自上一页的 eq2_grp"""
        if kept_line:
            self.play(FadeOut(kept_line), run_time=0.35)

        step = make_proof_line(0, [
            ('T', '▎第二步：系数行列式判唯一解', C_STEP),
        ])

        matrix_line = make_proof_line(1, [
            ('T', '系数矩阵 ', WHITE),
            ('M', r'A=\begin{pmatrix}1&1\\ \omega&\omega^2\end{pmatrix}', C_DET),
        ])

        det_line = make_proof_line(2, [
            ('M', r'\det A = 1\cdot\omega^2-1\cdot\omega = \omega^2-\omega', C_DET),
        ])

        neq = make_proof_line(3, [
            ('M', r'\omega\neq 1\ \Rightarrow\ \omega^2\neq\omega\ \Rightarrow\ \det A\neq 0', WHITE),
        ])

        check = MathTex(r"\checkmark", font_size=56, color=C_CHECK)
        check.next_to(neq, RIGHT, buff=0.45)

        self.play(Write(step), run_time=1.2)
        self.wait(0.3)
        self.play(Write(matrix_line), run_time=1.5)
        self.wait(0.6)
        self.play(Write(det_line), run_time=1.5)
        self.wait(0.5)
        self.play(Write(neq), run_time=1.5)
        self.wait(0.3)
        self.play(Write(check), run_time=0.7)
        self.wait(0.5)

        # 画框 + 结论
        box = SurroundingRectangle(
            VGroup(det_line, neq, check),
            color=C_CHECK, stroke_width=3, buff=0.2, corner_radius=0.1,
        )
        conclusion = make_proof_line(4.5, [
            ('T', 'u, v 由前两个条件唯一确定！', C_CHECK),
        ], scale_factor=0.9)
        conclusion.move_to([PROOF_X, PROOF_Y_START - 4.5 * LINE_GAP, 0])

        self.play(Create(box), run_time=0.8)
        self.play(Write(conclusion), run_time=1.2)
        self.wait(3.5)

        # 清理
        self.play(
            FadeOut(step), FadeOut(matrix_line), FadeOut(det_line),
            FadeOut(neq), FadeOut(check), FadeOut(box), FadeOut(conclusion),
            run_time=0.7,
        )
        return None

    # ═════════════════════════════════════════
    # PART 4c: 场景二 — 重心性质（左侧图跟着动）
    # ═════════════════════════════════════════
    def proof_scene2_properties(self, fig):
        step = make_proof_line(0, [
            ('T', '▎第三步：利用重心性质', C_STEP),
        ])

        src_prop = make_proof_line(1, [
            ('T', '源点：', WHITE),
            ('M', r'1+\omega+\omega^2=0\ \Rightarrow\ \omega^2=-1-\omega', C_SOURCE),
        ])

        tgt_prop = make_proof_line(2, [
            ('T', '目标：', WHITE),
            ('M', r'z_1+z_2+z_3=0\ \Rightarrow\ z_3=-z_1-z_2', C_TARGET),
        ])

        self.play(Write(step), run_time=1.2)
        self.wait(0.3)

        # ★ 左侧图：高亮 ω² 点
        self.play(
            fig['src_pts'][2].animate.scale(1.5).set_color(YELLOW),
            fig['src_lbl'][2].animate.set_color(YELLOW),
            run_time=0.6,
        )
        self.play(Write(src_prop), run_time=1.5)
        self.wait(0.8)

        w2_annot = MathTex(r"=-1-\omega", font_size=30, color=YELLOW)
        w2_annot.next_to(fig['src_pts'][2], LEFT, buff=0.25)
        self.play(Write(w2_annot), run_time=0.8)
        self.wait(0.8)

        # ★ 左侧图：高亮 z₃ 点
        self.play(
            fig['tgt_pts'][2].animate.scale(1.5).set_color(YELLOW),
            fig['tgt_lbl'][2].animate.set_color(YELLOW),
            run_time=0.6,
        )
        self.play(Write(tgt_prop), run_time=1.5)
        self.wait(0.8)

        z3_annot = MathTex(r"=-z_1-z_2", font_size=30, color=YELLOW)
        z3_annot.next_to(fig['tgt_pts'][2], DOWN, buff=0.3)
        self.play(Write(z3_annot), run_time=0.8)
        self.wait(2.5)

        # 恢复颜色
        self.play(
            fig['src_pts'][2].animate.scale(1/1.5).set_color(C_SOURCE),
            fig['src_lbl'][2].animate.set_color(C_SOURCE),
            fig['tgt_pts'][2].animate.scale(1/1.5).set_color(C_TARGET),
            fig['tgt_lbl'][2].animate.set_color(C_TARGET),
            FadeOut(w2_annot), FadeOut(z3_annot),
            run_time=0.7,
        )

        # 淡出证明行
        self.play(FadeOut(step), FadeOut(src_prop), FadeOut(tgt_prop), run_time=0.6)

    # ═════════════════════════════════════════
    # PART 4d: 场景三 — 线性性质验证（左侧图跟着动）
    # ═════════════════════════════════════════
    def proof_scene3_linearity(self, fig):
        step = make_proof_line(0, [
            ('T', '▎第四步：线性性质自动验证', C_STEP),
        ])

        L1 = make_proof_line(1, [
            ('M', r'T(\omega^2)', WHITE),
            ('M', r'= T(-1-\omega)', WHITE),
        ])

        L2 = make_proof_line(2, [
            ('M', r'= -T(1)-T(\omega)', WHITE),
        ])

        L3 = make_proof_line(3, [
            ('M', r'= -z_1-z_2', WHITE),
        ])

        L4 = make_proof_line(4, [
            ('M', r'= z_3', YELLOW),
        ])

        check3 = MathTex(r"\checkmark", font_size=52, color=C_CHECK)
        check3.next_to(L4, RIGHT, buff=0.4)

        self.play(Write(step), run_time=1.2)
        self.wait(0.3)

        # ★ 左侧图：高亮 ω²
        self.play(
            Indicate(fig['src_pts'][2], scale_factor=1.4, color=YELLOW),
            run_time=0.8,
        )
        self.play(Write(L1), run_time=1.5)
        self.wait(0.5)

        self.play(Write(L2), run_time=1.5)
        self.wait(0.5)
        self.play(Write(L3), run_time=1.5)
        self.wait(0.5)

        # ★ 左侧图：高亮 z₃
        self.play(
            Indicate(fig['tgt_pts'][2], scale_factor=1.4, color=YELLOW),
            run_time=0.8,
        )
        self.play(Write(L4), run_time=1.2)
        self.play(Write(check3), run_time=0.7)
        self.wait(0.5)

        # ★ 左侧图：从 ω² 到 z₃ 画虚线箭头（用当前屏幕坐标）
        link = DashedLine(
            fig['src_pts'][2].get_center(),
            fig['tgt_pts'][2].get_center(),
            color=C_LINK, stroke_width=3, dash_length=0.15,
        )
        link_label = MathTex("T", font_size=36, color=C_LINK)
        link_label.move_to(link.get_center() + UP * 0.2 + RIGHT * 0.15)
        self.play(Create(link), Write(link_label), run_time=1.2)

        # 结论框
        box = SurroundingRectangle(
            VGroup(L4, check3),
            color=C_CHECK, stroke_width=3, buff=0.25, corner_radius=0.1,
        )
        final_note = make_proof_line(5.2, [
            ('T', '第三个条件自动满足！证毕。', C_CHECK),
        ], scale_factor=0.9)
        final_note.move_to([PROOF_X, PROOF_Y_START - 5.2 * LINE_GAP, 0])

        self.play(Create(box), run_time=0.7)
        self.play(Write(final_note), run_time=1.0)
        self.wait(4.0)

        # 存储引用供后续清理
        self._link_arrow = VGroup(link, link_label)
        self._final_box   = VGroup(box, final_note)
        self._scene3_lines = VGroup(step, L1, L2, L3, L4, check3)

    # ═════════════════════════════════════════
    # END: 结论 — 图形回中央
    # ═════════════════════════════════════════
    def show_conclusion(self, fig):
        # 清理右侧证明
        to_clear = [self._scene3_lines, self._final_box]
        if hasattr(self, '_link_arrow'):
            to_clear.append(self._link_arrow)
        self.play(*[FadeOut(g, run_time=0.5) for g in to_clear])

        # ★ 图形缩小并上移，避免与底部定理重叠
        self.play(
            fig['all'].animate.scale(0.88).move_to(ORIGIN + UP * 1.8),
            run_time=2.25,
        )
        self.wait(0.6)

        # 底部定理
        final_theorem = VGroup(
            MathTex(
                r"\exists! \ T(w)=uw+v\overline{w},\quad "
                r"T(1)=z_1,\ T(\omega)=z_2,\ T(\omega^2)=z_3",
                font_size=46, color=YELLOW,
            ),
            Text("复仿射线性变换 · 存在唯一 · 得证", font=CN_FONT, font_size=36, color=GREEN),
        ).arrange(DOWN, buff=0.35)
        final_theorem.to_edge(DOWN, buff=0.55)

        self.play(Write(final_theorem[0]), run_time=2.5)
        self.play(Write(final_theorem[1]), run_time=1.2)
        self.wait(4.0)

        # 优雅退场
        self.play(FadeOut(fig['all']), FadeOut(final_theorem), run_time=1.2)
