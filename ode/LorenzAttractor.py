from manim import *
import numpy as np

# ---------------------------------------------------------------------------
# Lorenz (1963) atmospheric convection model:
#   dx/dt = sigma (y - x)
#   dy/dt = x (rho - z) - y
#   dz/dt = x y - beta z
# Classical chaotic parameters: sigma=10, rho=28, beta=8/3.
# A deterministic, low-dimensional ODE system whose solutions settle onto a
# strange attractor and exhibit sensitive dependence on initial conditions.
# ---------------------------------------------------------------------------

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0


def lorenz_deriv(state):
    x, y, z = state
    return np.array(
        [SIGMA * (y - x), x * (RHO - z) - y, x * y - BETA * z]
    )


def integrate_lorenz(x0, dt, n_steps):
    """Classic 4th-order Runge-Kutta integration. Returns array (n_steps+1, 3)."""
    traj = np.empty((n_steps + 1, 3))
    traj[0] = np.array(x0, dtype=float)
    s = traj[0].copy()
    half = dt / 2.0
    for i in range(n_steps):
        k1 = lorenz_deriv(s)
        k2 = lorenz_deriv(s + k1 * half)
        k3 = lorenz_deriv(s + k2 * half)
        k4 = lorenz_deriv(s + k3 * dt)
        s = s + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)
        traj[i + 1] = s
    return traj


def to_scene_points(traj, scale, z_center):
    """Center the attractor (shift z so the wings sit near z=0) and rescale."""
    pts = traj.astype(float).copy()
    pts[:, 2] -= z_center
    return pts * scale


def make_curve(points, color, stroke_width=2.0):
    """Build a piecewise-linear 3D curve from sampled points."""
    curve = VMobject(stroke_color=color, stroke_width=stroke_width)
    curve.set_points_as_corners(points)
    return curve


class LorenzAttractor(ThreeDScene):
    SCALE = 0.11          # Lorenz coords -> scene-space scale
    Z_CENTER = 25.0       # vertical offset so the attractor is centered
    FRAME_RATE = 0.10     # ambient camera rotation speed (rad/s)

    def construct(self):
        self.show_theory()
        self.show_attractor()
        self.show_butterfly_effect()
        self.show_conclusion()

    # ------------------------------------------------------------------ theory
    def show_theory(self):
        title = Text(
            "洛伦兹吸引子 Lorenz Attractor",
            font="SimHei", font_size=44, color=BLUE,
        )
        eqs = VGroup(
            MathTex(r"\frac{dx}{dt} = \sigma\,(y - x)", color=YELLOW),
            MathTex(r"\frac{dy}{dt} = x\,(\rho - z) - y", color=YELLOW),
            MathTex(r"\frac{dz}{dt} = x\,y - \beta\,z", color=YELLOW),
        ).arrange(DOWN, buff=0.4)

        params = MathTex(
            r"\sigma = 10,\quad \rho = 28,\quad \beta = \tfrac{8}{3}",
            color=BLUE_B,
        )
        note = Text(
            "确定性非线性系统中的混沌行为",
            font="SimHei", font_size=30, color=WHITE,
        )

        content = VGroup(title, eqs, params, note).arrange(DOWN, buff=0.6)
        content.scale(0.9)
        self.add_fixed_in_frame_mobjects(content)

        self.play(Write(title))
        for eq in eqs:
            self.play(Write(eq), run_time=0.8)
        self.play(Write(params))
        self.play(FadeIn(note, shift=UP))
        self.wait(1.5)

        self.play(FadeOut(content))
        self.wait(0.5)

    # ---------------------------------------------------------------- attractor
    def show_attractor(self):
        self.set_camera_orientation(
            phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.3
        )

        # Faint reference axes to convey 3D orientation.
        axes = ThreeDAxes(
            x_range=[-25, 25, 10],
            y_range=[-30, 30, 10],
            z_range=[0, 50, 10],
            x_length=9,
            y_length=9,
            z_length=6,
        )
        axes.set_opacity(0.22)
        self.add(axes)

        # Persistent top-left caption during the 3D sections.
        caption = Text(
            "洛伦兹吸引子", font="SimHei", font_size=28, color=BLUE,
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(caption)
        self.play(FadeIn(caption))
        self.caption = caption

        # Numerically integrate one trajectory and draw it progressively.
        traj = integrate_lorenz((1.0, 1.0, 1.0), dt=0.01, n_steps=5000)
        points = to_scene_points(traj, self.SCALE, self.Z_CENTER)
        curve = make_curve(points, YELLOW, stroke_width=2)
        head = Dot3D(points[0], color=RED, radius=0.06)

        self.add(head)
        self.begin_ambient_camera_rotation(rate=self.FRAME_RATE, about="theta")
        self.play(
            Create(curve),
            MoveAlongPath(head, curve),
            run_time=18, rate_func=linear,
        )
        self.wait(3)
        self.stop_ambient_camera_rotation()

        self.attractor_objs = [axes, curve, head]

    # ------------------------------------------------------------ butterfly fx
    def show_butterfly_effect(self):
        # Clear the single-trajectory attractor; keep the persistent caption.
        for m in self.attractor_objs:
            self.remove(m)
        self.attractor_objs = []

        delta = 1e-5
        ic1_text = Text("初值 1: (1.00000, 1, 1)", font="SimHei", font_size=20, color=WHITE)
        ic2_text = Text("初值 2: (1.00001, 1, 1)", font="SimHei", font_size=20, color=WHITE)
        legend = VGroup(
            VGroup(Dot(color=YELLOW, radius=0.05), ic1_text).arrange(RIGHT, buff=0.15),
            VGroup(Dot(color=BLUE, radius=0.05), ic2_text).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(UL).shift(DOWN * 0.6)
        self.add_fixed_in_frame_mobjects(legend)
        self.play(FadeIn(legend, shift=RIGHT))

        traj1 = integrate_lorenz((1.0, 1.0, 1.0), dt=0.01, n_steps=4500)
        traj2 = integrate_lorenz((1.0 + delta, 1.0, 1.0), dt=0.01, n_steps=4500)
        pts1 = to_scene_points(traj1, self.SCALE, self.Z_CENTER)
        pts2 = to_scene_points(traj2, self.SCALE, self.Z_CENTER)

        curve1 = make_curve(pts1, YELLOW, stroke_width=2)
        curve2 = make_curve(pts2, BLUE, stroke_width=2)
        head1 = Dot3D(pts1[0], color=YELLOW, radius=0.05)
        head2 = Dot3D(pts2[0], color=BLUE, radius=0.05)

        self.add(head1, head2)
        self.begin_ambient_camera_rotation(rate=self.FRAME_RATE, about="theta")
        self.play(
            Create(curve1), Create(curve2),
            MoveAlongPath(head1, curve1), MoveAlongPath(head2, curve2),
            run_time=20, rate_func=linear,
        )
        self.wait(2)
        self.stop_ambient_camera_rotation()

        self.butterfly_objs = [curve1, curve2, head1, head2]
        self.legend = legend

    # --------------------------------------------------------------- conclusion
    def show_conclusion(self):
        self.play(
            FadeOut(VGroup(*self.butterfly_objs)),
            FadeOut(self.legend),
        )

        title = Text("蝴蝶效应", font="SimHei", font_size=54, color=BLUE)
        subtitle = Text(
            "初值敏感性:微小的初始差异导致指数级发散",
            font="SimHei", font_size=30, color=YELLOW,
        )
        note = Text(
            "确定性系统中的不可预测性",
            font="SimHei", font_size=26, color=WHITE,
        )

        grp = VGroup(title, subtitle, note).arrange(DOWN, buff=0.6)
        self.add_fixed_in_frame_mobjects(grp)
        self.play(Write(title))
        self.play(Write(subtitle))
        self.play(FadeIn(note, shift=UP))
        self.wait(3)
        self.play(FadeOut(VGroup(grp, self.caption)))
        self.wait(0.5)
