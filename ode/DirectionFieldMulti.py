"""
线素场多例子动画 — 综合 manim-3b1b-skill + manim-transform-skill + manim:animate

运行: conda activate manimce && manim -pqh "manimce code/DirectionFieldMulti.py" DirectionFieldGallery
"""

from manim import *

config.font = "SimHei"

# ═══════════════════ 配色 ═══════════════════
C_TITLE = BLUE
C_EMPHASIS = YELLOW
C_RESULT = GREEN
C_DEFAULT = WHITE
C_DIM = GREY
C_LINE = BLUE_D
C_HIGHLIGHT = YELLOW
C_CURVE_START = TEAL
C_CURVE_END = RED


# ═══════════════════ 辅助函数 ═══════════════════

def make_axes():
    return Axes(
        x_range=[-8, 8, 1],
        y_range=[-8, 8, 1],
        x_length=12.5,
        y_length=12.5,
        axis_config={
            "color": GREY_B, "stroke_width": 2,
            "include_tip": True, "tip_shape": StealthTip,
        },
        x_axis_config={"numbers_to_include": range(-8, 9, 2)},
        y_axis_config={"numbers_to_include": range(-8, 9, 2)},
    ).center()


def build_field_rows(axes, slope_func, spacing=0.6, half_len=0.45,
                     color=C_LINE, stroke_w=2.0):
    """构造按 x 行分组的线素场。slope_func(x,y) → k | None"""
    rows = []
    for x in np.arange(-6, 6 + 1e-9, spacing):
        row = VGroup()
        for y in np.arange(-6, 6 + 1e-9, spacing):
            k = slope_func(x, y)
            if k is None:
                continue
            d = np.array([1, k, 0])
            n = np.linalg.norm(d)
            if n < 1e-9:
                continue
            d /= n
            c = axes.coords_to_point(x, y)
            row.add(Line(c - half_len * d, c + half_len * d,
                         color=color, stroke_width=stroke_w))
        if len(row) > 0:
            rows.append(row)
    return rows


def draw_field(rows, run_time=9, lag_ratio=0.025):
    return LaggedStart(
        *[Create(row) for row in rows],
        lag_ratio=lag_ratio, run_time=run_time, rate_func=linear,
    )


# ═══════════════════ 主场景 ═══════════════════

class DirectionFieldGallery(Scene):
    """三个一阶微分方程的线素场 + 积分曲线。

    例1: dy/dx = y/x   → 径向场    y = Cx
    例2: dy/dx = -x/y  → 旋转场    x² + y² = C
    例3: dy/dx = x     → 抛物场    y = x²/2 + C
    """

    def construct(self):
        # ── 共享轴 ──
        axes = make_axes()
        ax_labels = axes.get_axis_labels("x", "y")
        self.axes = axes

        # ── 开场 ──
        title = Text("线素场", font_size=44, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.add(title)  # 始终保留

        sub = Text(
            "一阶微分方程 dy/dx = f(x,y) 的几何解释",
            font_size=24, color=C_DIM,
        ).next_to(title, DOWN, buff=0.15)

        self.play(Write(title), Write(sub))
        self.wait(0.6)

        # 定义块
        def_group = self._definition()
        self.wait(1.2)
        self.play(FadeOut(VGroup(sub, def_group)), run_time=0.6)

        # 坐标轴
        self.play(Create(axes), Write(ax_labels), run_time=1.5)
        self.ax_labels = ax_labels

        # ── 三个例子 ──
        self._radial(title)
        self._circular(title)
        self._parabolic(title)

        # ── 总结 ──
        self._summary(title)
        self.wait(3)

    # ═══════════════════ 定义 ═══════════════════
    def _definition(self):
        eq = MathTex(r"\frac{dy}{dx} = f(x, y)", font_size=40, color=C_EMPHASIS)
        eq.to_edge(DOWN, buff=4.5)

        lines = VGroup(
            Text("对区域 G 内每一点，以该点为中点，作单位线段", font_size=24, color=C_DEFAULT),
            Text("使其斜率恰为 k = f(x,y)，称为线素", font_size=24, color=C_DEFAULT,
                 t2c={"线素": C_EMPHASIS}),
            Text("区域 G 内全体线素构成该方程的线素场", font_size=24, color=C_DEFAULT,
                 t2c={"线素场": C_EMPHASIS}),
        ).arrange(DOWN, buff=0.12)
        lines.next_to(eq, DOWN, buff=0.5)

        self.play(Write(eq), run_time=1)
        self.play(Write(lines), run_time=2)
        return VGroup(eq, lines)

    # ═══════════════════ 例1: 径向场 ═══════════════════
    def _radial(self, title):
        eg = VGroup()

        # 左对齐的标题行
        tag = Text("例1", font_size=30, color=C_EMPHASIS)
        eq = MathTex(r"\frac{dy}{dx} = \frac{y}{x}", font_size=36, color=C_EMPHASIS)
        header = VGroup(tag, eq).arrange(RIGHT, buff=0.35)
        header.next_to(title, DOWN, buff=0.25).to_edge(LEFT, buff=1.2)
        eg.add(header)
        self.play(Write(header))

        # 场
        rows = build_field_rows(self.axes, lambda x, y: None if abs(x) < 1e-6 else y / x)
        field = VGroup(*[l for r in rows for l in r])
        eg.add(field)
        self.play(draw_field(rows))
        self.wait(0.4)

        # 高亮
        h = self._highlight(2, 1, 0.5, r"\tfrac{1}{2}")
        eg.add(h)
        self.wait(1.5)
        self.play(FadeOut(h), run_time=0.4)
        eg.remove(h)

        # 积分曲线
        curve_label = Text("积分曲线  y = Cx", font_size=26, color=C_RESULT)
        curve_label.next_to(header, DOWN, buff=3.8).align_to(header, LEFT)
        eg.add(curve_label)
        self.play(Write(curve_label))

        c_vals = [-3, -2, -1, -0.5, -0.2, 0.2, 0.5, 1, 2, 3]
        colors = color_gradient([C_CURVE_START, C_CURVE_END], len(c_vals))
        curves = VGroup()
        for c, clr in zip(c_vals, colors):
            curves.add(self.axes.plot(lambda x, c=c: c * x,
                                      x_range=[-6, 6], color=clr, stroke_width=3))
        eg.add(curves)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.1, run_time=4))
        self.wait(1.2)

        self.play(FadeOut(eg), run_time=0.7)

    # ═══════════════════ 例2: 旋转场 ═══════════════════
    def _circular(self, title):
        eg = VGroup()

        tag = Text("例2", font_size=30, color=C_EMPHASIS)
        eq = MathTex(r"\frac{dy}{dx} = -\frac{x}{y}", font_size=36, color=C_EMPHASIS)
        header = VGroup(tag, eq).arrange(RIGHT, buff=0.35)
        header.next_to(title, DOWN, buff=0.25).to_edge(LEFT, buff=1.2)
        eg.add(header)
        self.play(Write(header))

        rows = build_field_rows(self.axes, lambda x, y: None if abs(y) < 1e-6 else -x / y)
        field = VGroup(*[l for r in rows for l in r])
        eg.add(field)
        self.play(draw_field(rows))
        self.wait(0.4)

        h = self._highlight(2, 2, -1.0, "-1")
        eg.add(h)
        self.wait(1.5)
        self.play(FadeOut(h), run_time=0.4)
        eg.remove(h)

        curve_label = Text("积分曲线  x² + y² = C  同心圆", font_size=26, color=C_RESULT)
        curve_label.next_to(header, DOWN, buff=3.8).align_to(header, LEFT)
        eg.add(curve_label)
        self.play(Write(curve_label))

        radii = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0]
        colors = color_gradient([C_CURVE_START, C_CURVE_END], len(radii))
        curves = VGroup()
        for r, clr in zip(radii, colors):
            curves.add(self.axes.plot_parametric_curve(
                lambda t, r=r: (r * np.cos(t), r * np.sin(t)),
                t_range=[0, 2 * PI], color=clr, stroke_width=3,
            ))
        eg.add(curves)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.1, run_time=4))
        self.wait(1.2)

        self.play(FadeOut(eg), run_time=0.7)

    # ═══════════════════ 例3: 抛物场 ═══════════════════
    def _parabolic(self, title):
        eg = VGroup()

        tag = Text("例3", font_size=30, color=C_EMPHASIS)
        eq = MathTex(r"\frac{dy}{dx} = x", font_size=36, color=C_EMPHASIS)
        header = VGroup(tag, eq).arrange(RIGHT, buff=0.35)
        header.next_to(title, DOWN, buff=0.25).to_edge(LEFT, buff=1.2)
        eg.add(header)
        self.play(Write(header))

        rows = build_field_rows(self.axes, lambda x, y: x)
        field = VGroup(*[l for r in rows for l in r])
        eg.add(field)
        self.play(draw_field(rows))
        self.wait(0.4)

        h = self._highlight(3, 1, 3.0, "3")
        eg.add(h)
        self.wait(1.5)
        self.play(FadeOut(h), run_time=0.4)
        eg.remove(h)

        curve_label = Text("积分曲线  y = x²/2 + C", font_size=26, color=C_RESULT)
        curve_label.next_to(header, DOWN, buff=3.8).align_to(header, LEFT)
        eg.add(curve_label)
        self.play(Write(curve_label))

        c_vals = [-3, -2, -1, 0, 1, 2, 3]
        colors = color_gradient([C_CURVE_START, C_CURVE_END], len(c_vals))
        curves = VGroup()
        for c, clr in zip(c_vals, colors):
            curves.add(self.axes.plot(lambda x, c=c: x**2 / 2 + c,
                                      x_range=[-6, 6], color=clr, stroke_width=3))
        eg.add(curves)
        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.1, run_time=4))
        self.wait(1.2)

        self.play(FadeOut(eg), run_time=0.7)

    # ═══════════════════ 高亮 ═══════════════════
    def _highlight(self, x0, y0, k_val, k_label_str):
        """在 (x0, y0) 处高亮展示线素。k_val 是数值, k_label_str 是显示用的 LaTeX 字符串。"""
        group = VGroup()
        point = self.axes.coords_to_point(x0, y0)

        direction = np.array([1, k_val, 0])
        direction /= np.linalg.norm(direction)
        half = 0.45

        dot = Dot(point, color=C_HIGHLIGHT, radius=0.1)
        coord = MathTex(f"({x0},{y0})", font_size=26, color=C_HIGHLIGHT)
        coord.next_to(point, UR, buff=0.1)
        k_label = MathTex(f"k={k_label_str}", font_size=26, color=C_HIGHLIGHT)
        k_label.next_to(coord, RIGHT, buff=0.15)
        line = Line(point - half * direction, point + half * direction,
                    color=C_HIGHLIGHT, stroke_width=6)

        group.add(dot, coord, k_label, line)
        self.play(GrowFromCenter(dot), Write(coord), Write(k_label),
                  Create(line), run_time=1)
        return group

    # ═══════════════════ 总结 ═══════════════════
    def _summary(self, title):
        sum_title = Text("三种线素场对比", font_size=34, color=C_TITLE)
        sum_title.next_to(title, DOWN, buff=0.3)
        self.play(Write(sum_title))

        examples = VGroup()
        for eq_str, name in [
            (r"\frac{dy}{dx} = \frac{y}{x}", "径向场"),
            (r"\frac{dy}{dx} = -\frac{x}{y}", "旋转场"),
            (r"\frac{dy}{dx} = x", "抛物场"),
        ]:
            box = VGroup(
                MathTex(eq_str, font_size=26, color=C_EMPHASIS),
                Text(name, font_size=22, color=C_DEFAULT),
            ).arrange(DOWN, buff=0.1)
            examples.add(box)
        examples.arrange(RIGHT, buff=1.0)
        examples.next_to(sum_title, DOWN, buff=0.8)

        self.play(LaggedStart(*[Write(b) for b in examples], lag_ratio=0.3))

        insight = Text("线素场是微分方程的几何指纹", font_size=28, color=C_RESULT)
        insight.next_to(examples, DOWN, buff=0.8)
        insight2 = Text("它能预言积分曲线的形状，无需真正求解方程", font_size=22, color=C_DIM)
        insight2.next_to(insight, DOWN, buff=0.15)

        self.play(Write(insight), Write(insight2))
        self.wait(2)

        self.play(FadeOut(VGroup(
            self.axes, self.ax_labels,
            sum_title, examples, insight, insight2,
        )), run_time=1.2)


# ═══════════════════ 场景2: 深度讲解 ═══════════════════
class DirectionFieldDeepDive(Scene):
    """以 dy/dx = -x/y 为例，逐步展示线素场构造全过程。"""

    def construct(self):
        title = Text("线素场的构造过程", font_size=40, color=C_TITLE)
        title.to_edge(UP, buff=0.35)
        self.add(title)

        eq = MathTex(r"\frac{dy}{dx} = -\frac{x}{y}", font_size=38, color=C_EMPHASIS)
        eq.next_to(title, DOWN, buff=0.25)
        self.play(Write(title), Write(eq))
        self.wait(0.6)

        axes = make_axes()
        ax_labels = axes.get_axis_labels("x", "y")
        self.axes = axes
        self.play(Create(axes), Write(ax_labels), run_time=1.5)

        # 单点示范
        guide = Text("以点 (3, 2) 为例", font_size=24, color=C_DEFAULT)
        guide.to_edge(DOWN, buff=1.0)
        self.play(Write(guide))

        x0, y0 = 3, 2
        k0 = -x0 / y0
        point = axes.coords_to_point(x0, y0)
        d = np.array([1, k0, 0])
        d /= np.linalg.norm(d)
        h = 0.5

        dot = Dot(point, color=C_HIGHLIGHT, radius=0.12)
        coord = MathTex(f"({x0},{y0})", font_size=28, color=C_HIGHLIGHT)
        coord.next_to(point, UR, buff=0.1)
        self.play(GrowFromCenter(dot), Write(coord))

        calc = MathTex(
            f"k = f({x0},{y0}) = -\\frac{{{x0}}}{{{y0}}} = -1.5",
            font_size=26, color=C_HIGHLIGHT,
        )
        calc.next_to(guide, UP, buff=0.15)
        self.play(Write(calc))
        self.wait(0.6)

        ghost = DashedLine(point - 1.5 * d, point + 1.5 * d,
                           color=GREY_A, stroke_width=1.5)
        self.play(Create(ghost))

        elem = Line(point - h * d, point + h * d,
                    color=C_HIGHLIGHT, stroke_width=6)
        self.play(Create(elem))
        self.wait(1.5)

        self.play(FadeOut(VGroup(guide, calc, dot, coord, ghost, elem)),
                  run_time=0.6)

        # 全场
        field_text = Text("对区域内每一点重复此操作 → 得到线素场", font_size=24, color=C_DEFAULT)
        field_text.to_edge(DOWN, buff=0.7)
        self.play(Write(field_text))

        rows = build_field_rows(
            axes, lambda x, y: None if abs(y) < 1e-6 else -x / y, spacing=0.55,
        )
        self.play(draw_field(rows, run_time=10, lag_ratio=0.02))
        self.play(FadeOut(field_text), run_time=0.4)
        self.wait(0.4)

        # 积分曲线
        info = VGroup(
            Text("微分方程的解曲线 — 积分曲线", font_size=26, color=C_RESULT),
            Text("处处与线素相切", font_size=22, color=C_DIM),
        ).arrange(DOWN, buff=0.08)
        info.to_edge(DOWN, buff=0.8)
        self.play(Write(info))

        radii = [1.0, 2.0, 3.0, 4.0, 5.0]
        colors = color_gradient([C_CURVE_START, C_CURVE_END], len(radii))
        curves = VGroup()
        for r, clr in zip(radii, colors):
            curves.add(axes.plot_parametric_curve(
                lambda t, r=r: (r * np.cos(t), r * np.sin(t)),
                t_range=[0, 2 * PI], color=clr, stroke_width=3.5,
            ))

        self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.12, run_time=4))
        self.wait(0.6)

        general = MathTex(r"x^2 + y^2 = C \quad (C > 0)", font_size=34, color=C_RESULT)
        general.next_to(eq, DOWN, buff=0.2)
        self.play(Write(general))
        self.wait(2)

        final = Text("线素场 — 微分方程的几何指纹", font_size=30, color=C_TITLE)
        final.to_edge(DOWN, buff=0.7)
        self.play(FadeOut(info), Write(final))
        self.wait(3)
