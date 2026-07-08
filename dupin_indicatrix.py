from manim import *
import numpy as np


config.pixel_width = 1080
config.pixel_height = 1920
config.frame_width = 8.0
config.frame_height = 14.22
config.media_dir = "media"


ZH_FONT = "仿宋-GB2312"
BG = "#0F1720"
INK = "#F6F2EA"
MUTED = "#A9B4C2"
BLUE = "#5DADEC"
GREEN = "#66D19E"
YELLOW = "#FFD166"
ORANGE = "#F59E62"
RED = "#FF6B6B"
VIOLET = "#B79CFF"
READ_PAUSE = 1.4


class DupinIndicatrix(ThreeDScene):
    # ===== 文本 helper =====
    def zh(self, content, font_size=30, color=INK, weight=NORMAL):
        return Text(content, font=ZH_FONT, font_size=font_size, color=color, weight=weight)

    def mt(self, content, font_size=40, color=INK):
        return MathTex(content, font_size=font_size, color=color)

    def mixed(self, *items, text_size=28, math_size=32, buff=0.08):
        parts = []
        for kind, content, color in items:
            if kind == "text":
                parts.append(self.zh(content, font_size=text_size, color=color))
            else:
                parts.append(self.mt(content, font_size=math_size, color=color))
        return VGroup(*parts).arrange(RIGHT, buff=buff, aligned_edge=DOWN)

    def fit(self, mob, width=None, height=None):
        target_width = width if width is not None else config.frame_width - 0.72
        target_height = height if height is not None else config.frame_height - 1.2
        if mob.width > target_width:
            mob.scale_to_fit_width(target_width)
        if mob.height > target_height:
            mob.scale_to_fit_height(target_height)
        return mob

    def fix2d(self, mob):
        """把 2D mobject 固定到屏幕坐标系（ThreeDScene 适配）。"""
        self.add_fixed_in_frame_mobjects(mob)
        return mob

    def title_bar(self, text, color=BLUE):
        title = self.zh(text, font_size=43, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        line = Line(
            title.get_left() + DOWN * 0.2,
            title.get_right() + DOWN * 0.2,
            color=color,
            stroke_width=3,
        )
        bar = VGroup(title, line)
        self.fix2d(bar)
        return bar

    def wait_formula(self):
        self.wait(READ_PAUSE)

    def write_formula(self, mob, run_time=0.9):
        self.fix2d(mob)
        self.play(Write(mob), run_time=run_time)
        self.wait_formula()

    def write_text(self, mob, run_time=0.75):
        self.fix2d(mob)
        self.play(Write(mob), run_time=run_time)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.55)

    def _show_3d(self, surface_func, z_range, curves, tag):
        """通用 3D 点缀：曲面 + 切平面 + 切点 + 切平面上指标线 + 缓转 + 收回。
        tag: Mobject（zh/mixed/mt 构建的标签）。
        """
        self.move_camera(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.0, run_time=1.2)
        axes3d = ThreeDAxes(
            x_range=[-1.5, 1.5, 1], y_range=[-1.5, 1.5, 1], z_range=z_range,
            x_length=3, y_length=3, z_length=3,
            axis_config={"stroke_color": MUTED, "stroke_width": 1.5},
        )
        surface = Surface(
            surface_func, u_range=(-1.3, 1.3), v_range=(-1.3, 1.3),
            resolution=(24, 24),
            fill_color=BLUE, fill_opacity=0.55,
            stroke_color=BLUE, stroke_width=0.5,
        )
        tangent = Square(side_length=2.6, fill_color=MUTED, fill_opacity=0.12,
                         stroke_color=MUTED, stroke_width=1, stroke_opacity=0.4)
        pt = Dot3D([0, 0, 0], color=RED, radius=0.06)
        self.play(Create(axes3d), run_time=0.7)
        self.play(Create(surface), run_time=1.6)
        self.play(FadeIn(tangent), FadeIn(pt), run_time=0.7)
        if curves is not None:
            self.play(Create(curves), run_time=1.6)
        tag.to_edge(DOWN, buff=0.6)
        self.fix2d(tag)
        self.play(Write(tag), run_time=0.7)
        self.begin_ambient_camera_rotation(rate=0.08)
        self.wait(4)
        self.stop_ambient_camera_rotation()
        out = VGroup(surface, tangent, pt, axes3d)
        if curves is not None:
            out.add(curves)
        self.play(FadeOut(tag), run_time=0.4)
        self.play(FadeOut(out), run_time=0.6)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=1.0)
        self.clear_scene()

    # ===== 主流程 =====
    def construct(self):
        self.camera.background_color = BG
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1.0)
        self.opening()
        self.prelude()
        self.definition_scene()
        self.elliptic_point()
        self.hyperbolic_point()
        self.parabolic_point()
        self.planar_point()
        self.umbilic_point()
        self.summary_scene()

    # ---------- 1. 封面 ----------
    def opening(self):
        title = self.zh("迪潘指标线", font_size=58, color=INK, weight=BOLD)
        title.to_edge(UP, buff=1.5)

        subtitle = self.zh("曲面在一点处的形状分类", font_size=34, color=MUTED)
        subtitle.next_to(title, DOWN, buff=0.45)

        formula = self.mt(
            r"k_1 x^2 + k_2 y^2 = \pm 1",
            font_size=52,
            color=YELLOW,
        )
        formula.next_to(subtitle, DOWN, buff=0.85)

        hint = self.mixed(
            ("text", "用切平面上的圆锥曲线，", INK),
            ("text", "读懂曲面的弯曲", GREEN),
            text_size=29,
        )
        hint.next_to(formula, DOWN, buff=0.9)
        self.fit(hint)

        self.write_text(title, run_time=0.9)
        self.play(FadeIn(subtitle, shift=UP * 0.2), run_time=0.7)
        self.write_formula(formula)
        self.play(FadeIn(hint, shift=UP * 0.2), run_time=0.8)
        self.wait(1.0)
        self.clear_scene()

    # ---------- 2. 前置铺垫：主曲率与高斯曲率 ----------
    def prelude(self):
        bar = self.title_bar("前置：主曲率与高斯曲率")
        self.play(Write(bar), run_time=0.8)

        k_intro = self.mixed(
            ("text", "曲面在一点 P 沿各方向有法曲率 ", INK),
            ("math", r"k_n", YELLOW),
            ("text", "，其极大、极小值", INK),
            text_size=27,
        )
        k_intro.next_to(bar, DOWN, buff=0.55)
        self.fit(k_intro)
        self.play(Write(k_intro), run_time=0.8)
        self.wait_formula()

        principal = self.mt(
            r"k_1 = \max k_n, \qquad k_2 = \min k_n",
            font_size=42,
            color=GREEN,
        )
        principal.next_to(k_intro, DOWN, buff=0.55)
        self.write_formula(principal)

        gauss = self.mixed(
            ("text", "高斯曲率", INK),
            ("math", r"K = k_1\,k_2", YELLOW),
            ("text", "——衡量曲面弯曲的关键量", INK),
            text_size=29,
        )
        gauss.next_to(principal, DOWN, buff=0.7)
        self.fit(gauss)
        self.play(FadeIn(gauss, shift=UP * 0.2), run_time=0.8)
        self.wait_formula()

        sign = self.mixed(
            ("text", "按 ", INK),
            ("math", r"k_1,k_2", YELLOW),
            ("text", " 的符号，曲面点分为五类：", INK),
            text_size=29,
        )
        sign.next_to(gauss, DOWN, buff=0.7)
        self.fit(sign)
        self.play(Write(sign), run_time=0.7)
        self.wait(1.0)
        self.clear_scene()

    # ---------- 3. 迪潘指标线定义 ----------
    def definition_scene(self):
        bar = self.title_bar("迪潘指标线的定义")
        self.play(Write(bar), run_time=0.8)

        setup = self.mixed(
            ("text", "在切平面（以 P 为原点，主方向为轴）上，取点 ", INK),
            ("math", r"(x,y)", YELLOW),
            ("text", "，令", INK),
            text_size=26,
        )
        setup.next_to(bar, DOWN, buff=0.55)
        self.fit(setup)
        self.play(Write(setup), run_time=0.8)
        self.wait_formula()

        equation = self.mt(
            r"k_1\,x^2 + k_2\,y^2 = \pm 1",
            font_size=54,
            color=YELLOW,
        )
        equation.next_to(setup, DOWN, buff=0.6)
        self.write_formula(equation)

        geom = self.mixed(
            ("text", "其轨迹即", INK),
            ("text", "迪潘指标线", GREEN),
            ("text", "——一条圆锥曲线", INK),
            text_size=29,
        )
        geom.next_to(equation, DOWN, buff=0.7)
        self.fit(geom)
        self.play(FadeIn(geom, shift=UP * 0.2), run_time=0.8)
        self.wait_formula()

        key = self.mixed(
            ("text", "曲线的形状，由 ", INK),
            ("math", r"k_1,k_2", YELLOW),
            ("text", " 的符号决定", INK),
            text_size=29,
        )
        key.next_to(geom, DOWN, buff=0.7)
        self.fit(key)
        self.play(Write(key), run_time=0.7)
        self.wait(1.0)
        self.clear_scene()

    # ---------- 4. 椭圆点 ----------
    def elliptic_point(self):
        bar = self.title_bar("椭圆点", GREEN)
        self.play(Write(bar), run_time=0.8)

        cond = self.mixed(
            ("math", r"k_1=2,\ k_2=1", YELLOW),
            ("text", " 同号，故 ", INK),
            ("math", r"K=k_1k_2=2>0", GREEN),
            text_size=29,
        )
        cond.next_to(bar, DOWN, buff=0.55)
        self.fit(cond)
        self.play(Write(cond), run_time=0.8)
        self.wait_formula()

        eqn = self.mt(r"2x^2+y^2=1", font_size=50, color=YELLOW)
        eqn.next_to(cond, DOWN, buff=0.5)
        self.write_formula(eqn)

        # 2D 指标线俯视
        plane = NumberPlane(
            x_range=[-1.4, 1.4, 1], y_range=[-1.4, 1.4, 1],
            x_length=3.8, y_length=3.8,
            background_line_style={
                "stroke_color": "#1E2A3A", "stroke_width": 1, "stroke_opacity": 0.6
            },
            axis_config={"stroke_color": MUTED, "stroke_width": 2},
        )
        plane.next_to(eqn, DOWN, buff=0.55)
        self.fix2d(plane)

        def ell_2d(t):
            return plane.c2p(np.cos(t) / np.sqrt(2), np.sin(t))

        curve2d = ParametricFunction(ell_2d, t_range=[0, TAU], color=GREEN, stroke_width=4)
        self.fix2d(curve2d)
        self.play(Create(plane), run_time=0.7)
        self.play(Create(curve2d), run_time=1.4)
        self.wait(0.9)

        # 切入 3D
        twod = VGroup(bar, cond, eqn, plane, curve2d)
        self.play(FadeOut(twod), run_time=0.6)
        self._show_3d(
            surface_func=lambda u, v: [u, v, (2 * u ** 2 + v ** 2) / 2],
            z_range=[-0.5, 3, 1],
            curves=ParametricFunction(
                lambda t: [np.cos(t) / np.sqrt(2), np.sin(t), 0.01],
                t_range=[0, TAU], color=YELLOW, stroke_width=5,
            ),
            tag=self.zh("碗形曲面 · 切平面上指标线为椭圆", font_size=27, color=GREEN),
        )

    # ---------- 5. 双曲点 ----------
    def hyperbolic_point(self):
        bar = self.title_bar("双曲点", RED)
        self.play(Write(bar), run_time=0.8)

        cond = self.mixed(
            ("math", r"k_1=1,\ k_2=-1", YELLOW),
            ("text", " 异号，故 ", INK),
            ("math", r"K=k_1k_2=-1<0", RED),
            text_size=29,
        )
        cond.next_to(bar, DOWN, buff=0.55)
        self.fit(cond)
        self.play(Write(cond), run_time=0.8)
        self.wait_formula()

        eqn = self.mt(r"x^2-y^2=\pm 1", font_size=50, color=YELLOW)
        eqn.next_to(cond, DOWN, buff=0.5)
        self.write_formula(eqn)

        plane = NumberPlane(
            x_range=[-1.9, 1.9, 1], y_range=[-1.9, 1.9, 1],
            x_length=3.8, y_length=3.8,
            background_line_style={
                "stroke_color": "#1E2A3A", "stroke_width": 1, "stroke_opacity": 0.6
            },
            axis_config={"stroke_color": MUTED, "stroke_width": 2},
        )
        plane.next_to(eqn, DOWN, buff=0.55)
        self.fix2d(plane)

        tr = [-1.3, 1.3]
        hyp2d = VGroup(
            ParametricFunction(lambda t: plane.c2p(np.cosh(t), np.sinh(t)), t_range=tr, color=RED, stroke_width=4),
            ParametricFunction(lambda t: plane.c2p(-np.cosh(t), np.sinh(t)), t_range=tr, color=RED, stroke_width=4),
            ParametricFunction(lambda t: plane.c2p(np.sinh(t), np.cosh(t)), t_range=tr, color=RED, stroke_width=4),
            ParametricFunction(lambda t: plane.c2p(np.sinh(t), -np.cosh(t)), t_range=tr, color=RED, stroke_width=4),
        )
        self.fix2d(hyp2d)
        self.play(Create(plane), run_time=0.7)
        self.play(Create(hyp2d), run_time=1.8)
        self.wait(0.9)

        twod = VGroup(bar, cond, eqn, plane, hyp2d)
        self.play(FadeOut(twod), run_time=0.6)
        self._show_3d(
            surface_func=lambda u, v: [u, v, (u ** 2 - v ** 2) / 2],
            z_range=[-1, 1.2, 1],
            curves=VGroup(
                ParametricFunction(lambda t: [np.cosh(t), np.sinh(t), 0.01], t_range=tr, color=YELLOW, stroke_width=5),
                ParametricFunction(lambda t: [-np.cosh(t), np.sinh(t), 0.01], t_range=tr, color=YELLOW, stroke_width=5),
                ParametricFunction(lambda t: [np.sinh(t), np.cosh(t), 0.01], t_range=tr, color=YELLOW, stroke_width=5),
                ParametricFunction(lambda t: [np.sinh(t), -np.cosh(t), 0.01], t_range=tr, color=YELLOW, stroke_width=5),
            ),
            tag=self.zh("马鞍面 · 切平面上指标线为共轭双曲线", font_size=27, color=RED),
        )

    # ---------- 6. 抛物点 ----------
    def parabolic_point(self):
        bar = self.title_bar("抛物点", ORANGE)
        self.play(Write(bar), run_time=0.8)

        cond = self.mixed(
            ("math", r"k_1=1,\ k_2=0", YELLOW),
            ("text", "，故 ", INK),
            ("math", r"K=k_1k_2=0", ORANGE),
            text_size=29,
        )
        cond.next_to(bar, DOWN, buff=0.55)
        self.fit(cond)
        self.play(Write(cond), run_time=0.8)
        self.wait_formula()

        eqn = self.mt(r"x^2=1\ \Rightarrow\ x=\pm 1", font_size=46, color=YELLOW)
        eqn.next_to(cond, DOWN, buff=0.5)
        self.write_formula(eqn)

        plane = NumberPlane(
            x_range=[-1.6, 1.6, 1], y_range=[-1.4, 1.4, 1],
            x_length=3.8, y_length=3.4,
            background_line_style={
                "stroke_color": "#1E2A3A", "stroke_width": 1, "stroke_opacity": 0.6
            },
            axis_config={"stroke_color": MUTED, "stroke_width": 2},
        )
        plane.next_to(eqn, DOWN, buff=0.55)
        self.fix2d(plane)

        par2d = VGroup(
            Line(plane.c2p(1, -1.2), plane.c2p(1, 1.2), color=ORANGE, stroke_width=4),
            Line(plane.c2p(-1, -1.2), plane.c2p(-1, 1.2), color=ORANGE, stroke_width=4),
        )
        self.fix2d(par2d)
        self.play(Create(plane), run_time=0.7)
        self.play(Create(par2d), run_time=1.2)
        self.wait(0.9)

        twod = VGroup(bar, cond, eqn, plane, par2d)
        self.play(FadeOut(twod), run_time=0.6)
        self._show_3d(
            surface_func=lambda u, v: [u, v, u ** 2 / 2],
            z_range=[-0.3, 1.6, 1],
            curves=VGroup(
                Line([1, -1.2, 0.01], [1, 1.2, 0.01], color=YELLOW, stroke_width=5),
                Line([-1, -1.2, 0.01], [-1, 1.2, 0.01], color=YELLOW, stroke_width=5),
            ),
            tag=self.zh("抛物柱面 · 指标线退化为平行直线", font_size=27, color=ORANGE),
        )

    # ---------- 7. 平点 ----------
    def planar_point(self):
        bar = self.title_bar("平点", MUTED)
        self.play(Write(bar), run_time=0.8)

        cond = self.mixed(
            ("math", r"k_1=k_2=0", YELLOW),
            ("text", "，故 ", INK),
            ("math", r"K=0", MUTED),
            ("text", "，第二基本形式恒为零", INK),
            text_size=27,
        )
        cond.next_to(bar, DOWN, buff=0.55)
        self.fit(cond)
        self.play(Write(cond), run_time=0.8)
        self.wait_formula()

        eqn = self.mt(r"0\cdot x^2+0\cdot y^2=\pm 1\ \Rightarrow\ 0=\pm 1", font_size=40, color=YELLOW)
        eqn.next_to(cond, DOWN, buff=0.5)
        self.write_formula(eqn)

        note = self.zh("指标线退化，不存在", font_size=31, color=MUTED)
        note.next_to(eqn, DOWN, buff=0.7)
        self.write_text(note)
        self.wait(0.9)

        twod = VGroup(bar, cond, eqn, note)
        self.play(FadeOut(twod), run_time=0.6)
        self._show_3d(
            surface_func=lambda u, v: [u, v, 0],
            z_range=[-0.8, 0.8, 1],
            curves=None,
            tag=self.zh("平面 · 曲面与切平面重合，指标线退化", font_size=27, color=MUTED),
        )

    # ---------- 8. 圆点 ----------
    def umbilic_point(self):
        bar = self.title_bar("圆点（脐点）", VIOLET)
        self.play(Write(bar), run_time=0.8)

        cond = self.mixed(
            ("math", r"k_1=k_2=1", YELLOW),
            ("text", "，故 ", INK),
            ("math", r"K=1>0", VIOLET),
            ("text", "（各方向法曲率相等）", INK),
            text_size=27,
        )
        cond.next_to(bar, DOWN, buff=0.55)
        self.fit(cond)
        self.play(Write(cond), run_time=0.8)
        self.wait_formula()

        eqn = self.mt(r"x^2+y^2=1", font_size=50, color=YELLOW)
        eqn.next_to(cond, DOWN, buff=0.5)
        self.write_formula(eqn)

        plane = NumberPlane(
            x_range=[-1.4, 1.4, 1], y_range=[-1.4, 1.4, 1],
            x_length=3.8, y_length=3.8,
            background_line_style={
                "stroke_color": "#1E2A3A", "stroke_width": 1, "stroke_opacity": 0.6
            },
            axis_config={"stroke_color": MUTED, "stroke_width": 2},
        )
        plane.next_to(eqn, DOWN, buff=0.55)
        self.fix2d(plane)

        circ2d = ParametricFunction(
            lambda t: plane.c2p(np.cos(t), np.sin(t)),
            t_range=[0, TAU], color=VIOLET, stroke_width=4,
        )
        self.fix2d(circ2d)
        self.play(Create(plane), run_time=0.7)
        self.play(Create(circ2d), run_time=1.4)
        self.wait(0.9)

        twod = VGroup(bar, cond, eqn, plane, circ2d)
        self.play(FadeOut(twod), run_time=0.6)
        self._show_3d(
            surface_func=lambda u, v: [u, v, (u ** 2 + v ** 2) / 2],
            z_range=[-0.5, 2.2, 1],
            curves=ParametricFunction(
                lambda t: [np.cos(t), np.sin(t), 0.01],
                t_range=[0, TAU], color=YELLOW, stroke_width=5,
            ),
            tag=self.mixed(
                ("text", "旋转抛物面 · ", VIOLET),
                ("math", r"k_1=k_2", YELLOW),
                ("text", "，指标线为圆", VIOLET),
                text_size=27,
            ),
        )

    # ---------- 9. 总结 ----------
    def summary_scene(self):
        bar = self.title_bar("五类点总结", BLUE)
        self.play(Write(bar), run_time=0.8)

        rows = VGroup(
            self.mixed(("text", "椭圆点", GREEN), ("math", r"\ k_1k_2>0", INK), ("text", "  K>0  椭圆", INK), text_size=28),
            self.mixed(("text", "双曲点", RED), ("math", r"\ k_1k_2<0", INK), ("text", "  K<0  共轭双曲线", INK), text_size=28),
            self.mixed(("text", "抛物点", ORANGE), ("math", r"\ k_1k_2=0", INK), ("text", "  K=0  平行直线", INK), text_size=28),
            self.mixed(("text", "平点", MUTED), ("math", r"\ k_1=k_2=0", INK), ("text", "  K=0  退化", INK), text_size=28),
            self.mixed(("text", "圆点", VIOLET), ("math", r"\ k_1=k_2\neq 0", INK), ("text", "  K>0  圆", INK), text_size=28),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT)
        self.fit(rows, width=config.frame_width - 1.0)
        rows.next_to(bar, DOWN, buff=0.8)
        self.fix2d(rows)
        self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in rows], lag_ratio=0.2))
        self.wait(1.2)

        closing = self.mixed(
            ("text", "指标线的形状", INK),
            ("math", r"=", YELLOW),
            ("text", "曲面在该点的形状", GREEN),
            text_size=32,
        )
        closing.next_to(rows, DOWN, buff=0.9)
        self.fit(closing)
        self.fix2d(closing)
        self.play(Write(closing), run_time=0.9)

        box = SurroundingRectangle(VGroup(rows, closing), color=YELLOW, buff=0.3, stroke_width=3)
        self.fix2d(box)
        self.play(Create(box), run_time=0.7)
        self.wait(READ_PAUSE)
