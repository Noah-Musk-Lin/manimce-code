"""
微分方程最大存在区间教学动画
课题: dy/dx = 1/y, y(1) = 1 的解及其最大存在区间

运行: manim -pqh ode_max_interval.py ODEMaxIntervalScene
"""
from manim import *
import numpy as np

# ── 颜色 ──────────────────────────────────────────────────
RD = RED
YL = YELLOW
GN = GREEN
BL = BLUE
GR = GREY
BG = BLACK

# ── 字体 / 字号 ───────────────────────────────────────────
FONT = "SimHei"
TS = 36          # 标题
BS = 26          # 正文 (从 28 缩至 26，留白更好)
NS = 20          # 注释 (从 22 缩至 20)
SS = 17          # 小字 (从 18 缩至 17)

# ── 坐标轴 ────────────────────────────────────────────────
AX_W = 6.0
AX_H = 3.8


# ═══════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════
def T(text: str, font_size: int = BS, color=WHITE, **kw) -> Text:
    return Text(text, font=FONT, font_size=font_size, color=color, **kw)


def title_t(text: str, font_size: int = TS, **kw) -> Text:
    return T(text, font_size=font_size, color=BL, **kw)


def note_t(text: str) -> Text:
    return T(text, font_size=NS, color=GR)


# ═══════════════════════════════════════════════════════════
class ODEMaxIntervalScene(Scene):

    def construct(self):
        self.s01_title()
        self.s02_domain()
        self.s03_separate()
        self.s04_integrate()
        self.s05_initial()
        self.s06_branch()
        self.s07_graph()
        self.s08_boundary()
        self.s09_slope()
        self.s10_summary()

    def _clear(self):
        # Group 接受所有 Mobject 类型（VGroup 仅限 VMobject）
        all_mobs = Group(*self.mobjects)
        self.play(FadeOut(all_mobs, shift=UP * 0.25), run_time=0.7)

    # ═══════════════════════════════════════════════════════
    # S01  标题与问题引入
    # ═══════════════════════════════════════════════════════
    def s01_title(self):
        ti = title_t("一阶微分方程初值问题").to_edge(UP, buff=0.3)

        eq = MathTex(
            r"\frac{dy}{dx}", "=", r"\frac{1}{y}",
            r",\qquad", r"y(1)=1",
        ).scale(1.3)

        qs = T("求解并判断最大存在区间", color=YL)

        body = VGroup(eq, qs).arrange(DOWN, buff=0.45)
        body.next_to(ti, DOWN, buff=0.55)

        self.play(Write(ti, run_time=0.7))
        self.play(Write(eq, run_time=1))
        self.play(FadeIn(qs, shift=UP * 0.3))
        self.wait(0.3)

        # 高亮 1/y — 放到 body 下方，加大间距避免重叠
        box = SurroundingRectangle(eq[2], color=RD, buff=0.1, corner_radius=0.06)
        warn = T("注意：当 y=0 时右端无定义", font_size=NS, color=RD)
        warn.next_to(body, DOWN, buff=0.55)

        self.play(Create(box), Write(warn))
        self.wait(2.5)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S02  右端函数定义域 — 标题→公式行→大轴→注释 四层清晰布局
    # ═══════════════════════════════════════════════════════
    def s02_domain(self):
        ti = title_t("先看右端函数的定义域").to_edge(UP, buff=0.3)

        # ── 第 1 行：公式 + 警告 横向排列，放在标题和轴之间 ──
        f_tex = MathTex(r"f(x,y)=\frac{1}{y}").scale(1.2)
        w_tex = T("当 y=0 时无定义", font_size=NS + 2, color=RD)
        header_row = VGroup(f_tex, w_tex).arrange(RIGHT, buff=0.5)
        header_row.next_to(ti, DOWN, buff=0.45)

        # ── 第 2 层：坐标轴，画面主体 ──
        axes = Axes(
            x_range=[-2.5, 2.5, 1],
            y_range=[-1.5, 1.5, 0.5],
            x_length=AX_W * 0.88,
            y_length=AX_H * 0.78,
            tips=True,
            axis_config={"include_numbers": True, "font_size": 16},
            x_axis_config={"stroke_opacity": 0},
        )
        axes.next_to(header_row, DOWN, buff=0.4)

        xl = axes.get_x_axis_label(MathTex("x").scale(0.8), edge=RIGHT, buff=0.04)
        yl = axes.get_y_axis_label(MathTex("y").scale(0.8), edge=UP, buff=0.04)

        # ── y=0 红色虚线 ──
        L_pt = axes.c2p(axes.x_range[0], 0)
        R_pt = axes.c2p(axes.x_range[1], 0)
        red_line = DashedLine(L_pt, R_pt, color=RD, stroke_width=4)

        y0_lbl = MathTex("y=0", color=RD).scale(0.7)
        y0_lbl.next_to(L_pt, UL, buff=0.1)

        # ── 原点叉号 ──
        ox, oy, _ = axes.c2p(0, 0)
        sz = 0.42
        cr1 = Line([ox - sz, oy - sz, 0], [ox + sz, oy + sz, 0],
                   color=RD, stroke_width=5)
        cr2 = Line([ox - sz, oy + sz, 0], [ox + sz, oy - sz, 0],
                   color=RD, stroke_width=5)

        # ── 第 3 层：底部注释 ──
        note = T("解曲线不能碰到这里", font_size=NS + 2, color=RD)
        note.next_to(axes, DOWN, buff=0.3)

        # ── 动画 ──
        self.play(Write(ti))
        self.play(Write(header_row))
        self.wait(0.2)
        self.play(Create(axes), Write(xl), Write(yl))
        self.play(Create(red_line), Write(y0_lbl))
        self.play(Create(cr1), Create(cr2))
        self.play(Write(note))
        self.wait(2.5)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S03  分离变量 — TransformMatchingShapes 展示代数变形
    # ═══════════════════════════════════════════════════════
    def s03_separate(self):
        ti = title_t("第一步：分离变量").to_edge(UP, buff=0.3)

        e1 = MathTex(r"\frac{dy}{dx} = \frac{1}{y}").scale(1.4)
        e2 = MathTex(r"y\,dy = dx").scale(1.4)
        nt = note_t("将含 y 的部分和含 x 的部分分开（y ≠ 0）")

        body = VGroup(e1, e2, nt).arrange(DOWN, buff=0.5)
        body.next_to(ti, DOWN, buff=0.65)

        self.play(Write(ti))
        self.play(Write(e1))
        self.wait(0.4)

        # TransformMatchingShapes：形态感知的符号过渡
        self.play(
            TransformMatchingShapes(e1, e2),
            run_time=1.5,
        )
        self.play(FadeIn(nt, shift=UP * 0.3))
        self.wait(2.5)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S04  两边积分 — 用 TransformFromCopy 避免残影
    # ═══════════════════════════════════════════════════════
    def s04_integrate(self):
        ti = title_t("第二步：两边积分").to_edge(UP, buff=0.3)

        a = MathTex(r"y\,dy=dx").scale(1.25)
        b = MathTex(r"\int y\,dy=\int dx").scale(1.25)
        # 拆开才能用索引定位 C
        c = MathTex(r"\frac{1}{2}y^2", "=", "x", "+", "C").scale(1.25)

        body = VGroup(a, b, c).arrange(DOWN, buff=0.45)
        body.next_to(ti, DOWN, buff=0.55)

        # C 高亮 — 索引 4
        c_box = SurroundingRectangle(c[4], color=YL, buff=0.1, corner_radius=0.06)
        c_note = T("积分常数", font_size=NS, color=YL)
        c_note.next_to(c[4], DOWN, buff=0.55)

        self.play(Write(ti))
        self.play(Write(a))
        self.wait(0.25)
        self.play(TransformFromCopy(a, b), run_time=1.1)
        self.wait(0.25)
        self.play(TransformFromCopy(b, c), run_time=1.3)
        self.play(Create(c_box), Write(c_note))
        self.wait(2.5)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S05  代入初值 — 左对齐推导链，数学书写习惯
    # ═══════════════════════════════════════════════════════
    def s05_initial(self):
        ti = title_t("第三步：代入初值").to_edge(UP, buff=0.3)

        sc = 0.85
        eqs = VGroup(
            MathTex(r"\tfrac{1}{2}y^2 = x + C").scale(sc),
            MathTex(
                r"\xrightarrow{\;y(1)=1\;}",
                r"\tfrac{1}{2}(1)^2 = 1 + C",
            ).scale(sc),
            MathTex(r"\tfrac{1}{2} = 1 + C").scale(sc),
            MathTex(r"C = -\tfrac{1}{2}").scale(sc),
            MathTex(r"y^2 = 2x - 1", color=GN).scale(sc),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)

        eqs.next_to(ti, DOWN, buff=0.65)

        fin_box = SurroundingRectangle(eqs[-1], color=GN, buff=0.15, corner_radius=0.06)

        self.play(Write(ti))
        for line in eqs:
            self.play(Write(line), run_time=0.35)
            self.wait(0.15)
        self.play(Create(fin_box))
        self.wait(2.5)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S06  选择正确分支 — 负分支用灰色，避免歧义
    # ═══════════════════════════════════════════════════════
    def s06_branch(self):
        ti = title_t("第四步：选择正确分支").to_edge(UP, buff=0.3)

        sq = MathTex(r"y^2 = 2x - 1").scale(1.1)
        ar = MathTex(r"\Downarrow").scale(1.1)
        bp = MathTex(r"y", "=", r"\sqrt{2x-1}", color=GN).scale(1.05)
        bn = MathTex(r"y", "=", r"-\sqrt{2x-1}", color=GR).scale(1.05)
        br = VGroup(bp, bn).arrange(DOWN, buff=0.3)

        rs = VGroup(
            MathTex(r"y(1)=1>0", color=GN),
            MathTex(r"\;\Rightarrow\;"),
            T("取正分支", font_size=BS - 2, color=GN),
        ).arrange(RIGHT, buff=0.15)

        body = VGroup(sq, ar, br, rs).arrange(DOWN, buff=0.2)
        body.next_to(ti, DOWN, buff=0.5)

        self.play(Write(ti))
        self.play(Write(sq), Write(ar))
        self.play(Write(bp), Write(bn))
        self.wait(0.3)

        # Indicate 脉冲强调正分支，Circumscribe 画圈确认
        self.play(
            Indicate(bp, color=GN, scale_factor=1.08, run_time=0.8),
            Circumscribe(bp, color=GN, fade_out=True, run_time=1.0),
        )
        self.play(Write(rs))
        # 负分支缩小淡出，视觉上"被淘汰"
        self.play(
            bn.animate.scale(0.7).set_opacity(0),
            run_time=0.8,
        )
        self.remove(bn)
        self.wait(2)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S07  解曲线图像 — 空心圆加大 + 底部边界提示
    # ═══════════════════════════════════════════════════════
    def s07_graph(self):
        ti = title_t("解曲线图像").to_edge(UP, buff=0.3)

        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=AX_W,
            y_length=AX_H,
            tips=True,
        )
        axes.move_to(DOWN * 0.15)
        xl = axes.get_x_axis_label(MathTex("x").scale(0.8), edge=RIGHT, buff=0.06)
        yl = axes.get_y_axis_label(MathTex("y").scale(0.8), edge=UP, buff=0.06)

        # 解曲线
        g = axes.plot(lambda x: np.sqrt(2 * x - 1),
                      x_range=[0.5001, 5], color=GN, stroke_width=5)
        gl = MathTex(r"y=\sqrt{2x-1}", color=GN).scale(0.7)
        gl.next_to(axes.c2p(3.5, np.sqrt(2 * 3.5 - 1)), UP, buff=0.2)

        # 初值点
        dot = Dot(axes.c2p(1, 1), color=YL, radius=0.06)
        dt = MathTex("(1,1)").scale(0.6).next_to(dot, UR, buff=0.08)

        # 边界虚线
        bd = DashedLine(axes.c2p(0.5, 0.08), axes.c2p(0.5, 2.7),
                        color=RD, stroke_width=3)
        bl = MathTex(r"x=\tfrac{1}{2}", color=RD).scale(0.68)
        bl.next_to(axes.c2p(0.5, 2.7), UP, buff=0.15)

        # 空心圆 — 稍大，更醒目
        oc = Circle(radius=0.10, color=RD, stroke_width=4)
        oc.set_fill(BG, opacity=1).move_to(axes.c2p(0.5, 0))
        ot = MathTex(r"(\frac{1}{2},0)", color=RD).scale(0.55)
        ot.next_to(oc, DOWN, buff=0.12)

        # 底部边界提示
        edge_note = T("边界点不能包含在解区间内", font_size=SS + 1, color=RD)
        edge_note.to_edge(DOWN, buff=0.25)

        self.play(Write(ti))
        self.play(Create(axes), Write(xl), Write(yl))
        self.play(Create(g), run_time=1.8, rate_func=linear)
        self.play(Write(gl))
        self.play(FadeIn(dot, scale=1.5), Write(dt))
        self.wait(0.25)
        self.play(Create(bd), Write(bl))
        self.play(Create(oc), Write(ot))
        # Flash 闪烁强调边界不可触碰
        self.play(Flash(oc, color=RD, line_length=0.3, flash_radius=0.25, time_width=0.3),
                  run_time=1.2)
        self.play(FadeIn(edge_note, shift=UP * 0.2))
        self.wait(2.5)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S08  为什么不能包含边界点 — 拆成两层
    # ═══════════════════════════════════════════════════════
    def s08_boundary(self):
        ti = title_t("为什么不能包含边界点？").to_edge(UP, buff=0.3)

        s1 = MathTex(r"x=\frac{1}{2}\Rightarrow y=0").scale(1.0)
        s2 = MathTex(r"\frac{1}{y}=\frac{1}{0}").scale(1.15)
        c1 = T("原微分方程右端无定义！", font_size=BS, color=RD)
        c2 = T("函数可以取值 ≠ 微分方程有意义", font_size=BS - 4, color=YL)

        top = VGroup(s1, s2).arrange(DOWN, buff=0.4)
        bottom = VGroup(c1, c2).arrange(DOWN, buff=0.25)
        body = VGroup(top, bottom).arrange(DOWN, buff=0.5)
        body.next_to(ti, DOWN, buff=0.55)

        self.play(Write(ti))
        self.play(Write(s1))
        self.wait(0.2)
        self.play(Write(s2))
        self.wait(0.3)
        # Flash + Circumscribe 双重强调 1/0 无定义
        self.play(
            Flash(s2, color=RD, flash_radius=0.4, line_length=0.3, time_width=0.3),
            Circumscribe(s2, color=RD, fade_out=True, run_time=1.2),
        )
        self.play(Write(c1))
        self.play(FadeIn(c2, shift=UP * 0.25))
        self.wait(3)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S09  斜率场 — 降低密度 (6×5=30 条线段)
    # ═══════════════════════════════════════════════════════
    def s09_slope(self):
        ti = title_t("斜率场直观理解").to_edge(UP, buff=0.3)

        # 隐藏黑色 x 轴线，用红色禁区虚线替代
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 3, 1],
            x_length=AX_W,
            y_length=AX_H,
            tips=True,
            x_axis_config={"stroke_opacity": 0},
        )
        axes.move_to(DOWN * 0.1)
        xl = axes.get_x_axis_label(MathTex("x").scale(0.8), edge=RIGHT, buff=0.06)
        yl = axes.get_y_axis_label(MathTex("y").scale(0.8), edge=UP, buff=0.06)

        # 斜率场 — 颜色映射：斜率越大越红（接近 y=0）
        segs = VGroup()
        for x in np.linspace(0.8, 4.4, 6):
            for y in np.linspace(0.5, 2.7, 5):
                slope = 1.0 / y
                ang = np.arctan(slope)
                L = 0.18
                dx = L * np.cos(ang)
                dy = L * np.sin(ang)
                p1 = axes.c2p(x - dx / 2, y - dy / 2)
                p2 = axes.c2p(x + dx / 2, y + dy / 2)
                # 颜色渐变：y 大时偏蓝，y 小时偏红
                t = np.clip(1.0 / (y * 2.8), 0, 1)
                seg_color = interpolate_color(BLUE_C, RD, t)
                segs.add(Line(p1, p2, color=seg_color,
                             stroke_width=2.2, stroke_opacity=0.65))

        # 解曲线
        g = axes.plot(lambda x: np.sqrt(2 * x - 1),
                      x_range=[0.5005, 5], color=GN, stroke_width=5)

        # y=0 禁区线 — 用 c2p 精确画出
        left_point = axes.c2p(axes.x_range[0], 0)
        right_point = axes.c2p(axes.x_range[1], 0)
        rz = DashedLine(left_point, right_point, color=RD, stroke_width=4)

        # 底部注释
        fn1 = T("y=0 处无斜率（奇点）", font_size=NS, color=RD)
        fn2 = T("当 y → 0⁺ 时,  y' = 1/y → +∞ ,  曲线越来越陡",
                font_size=SS + 1, color=GR)
        fn = VGroup(fn1, fn2).arrange(DOWN, buff=0.35)
        fn.next_to(axes, DOWN, buff=0.5)

        self.play(Write(ti))
        self.play(Create(axes), Write(xl), Write(yl))
        self.play(LaggedStart(
            *[Create(s) for s in segs], lag_ratio=0.008,
        ), run_time=2)
        self.play(Create(g), run_time=1.5)
        self.play(Create(rz))
        self.play(Write(fn))
        self.wait(3)
        self._clear()

    # ═══════════════════════════════════════════════════════
    # S10  最终结论
    # ═══════════════════════════════════════════════════════
    def s10_summary(self):
        ti = title_t("最终结论", font_size=40).to_edge(UP, buff=0.3)

        sr = VGroup(
            T("解：", font_size=BS),
            MathTex(r"y=\sqrt{2x-1}").scale(1.15),
        ).arrange(RIGHT, buff=0.25)

        ir = VGroup(
            T("最大存在区间：", font_size=BS),
            MathTex(r"\left(\frac{1}{2},+\infty\right)", color=GN).scale(1.25),
        ).arrange(RIGHT, buff=0.25)

        main = VGroup(sr, ir).arrange(DOWN, buff=0.6, aligned_edge=LEFT)

        wr = VGroup(
            MathTex(r"(0,+\infty)", color=RD).scale(1.05),
            T("← 不是最大存在区间", font_size=NS + 2, color=RD),
        ).arrange(RIGHT, buff=0.25)

        sm = T("最大存在区间必须避开原方程的奇点",
               font_size=BS - 2, color=YL)
        sm.to_edge(DOWN, buff=0.4)

        body = VGroup(main, wr).arrange(DOWN, buff=0.55)
        body.next_to(ti, DOWN, buff=0.6)

        self.play(Write(ti))
        self.play(Write(sr))
        self.wait(0.25)
        self.play(Write(ir))
        self.wait(0.3)
        self.play(Write(wr))
        cm = Cross(wr[0], color=RD, stroke_width=6)
        self.play(Create(cm))
        self.wait(0.25)
        self.play(FadeIn(sm, shift=UP * 0.25))
        self.wait(4)
        self._clear()
