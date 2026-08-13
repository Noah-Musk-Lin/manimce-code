"""
Matrix Polar Decomposition geometric - Manim Community Edition v0.21.0.

Render:
    conda run -n manimce manim -pql "manimce code/linear_algebra/polar_decomposition.py" ScenePolarHook
    conda run -n manimce manim -pql "manimce code/linear_algebra/polar_decomposition.py" ScenePolar2D
    conda run -n manimce manim -pql "manimce code/linear_algebra/polar_decomposition.py" ScenePolarLeftRight
    conda run -n manimce manim -pql "manimce code/linear_algebra/polar_decomposition.py" ScenePolar3D
    conda run -n manimce manim -pql "manimce code/linear_algebra/polar_decomposition.py" ScenePolarSVD

Strict math (asserted at import):
    Right polar   A = U P  (P stretches, then U rotates); acts as x -> U(P x)
    Left polar    A = P' U, where P' = U P U^T (symmetric positive definite).
ManimCE Mobject.apply_matrix(M) does points @ M.T, so applying P then U equals one A = UP.
"""
from manim import *
import numpy as np

# Color convention from Plan: P = stretch = ORANGE, U = rotation = BLUE
C_P = ORANGE
CU = BLUE
C_A = GREEN
CN_FONT = "Microsoft YaHei"


def cn(txt, **kw):
    return Text(txt, font=CN_FONT, **kw)


# Core matrices (strictly from the YAML)
P = np.array([[2.0, 0.0], [0.0, 1.0]])
U = np.array([[0.0, -1.0], [1.0, 0.0]])
A = U @ P
PPRIME = U @ P @ U.T  # left polar stretch matrix = [[1,0],[0,2]]

assert np.allclose(A, np.array([[0.0, -1.0], [2.0, 0.0]])), "A != U@P"
assert np.allclose(U @ U.T, np.eye(2)), "U must be orthogonal"
assert np.allclose(P, P.T), "P must be symmetric"
assert np.allclose(PPRIME, PPRIME.T), "P' must be symmetric"
assert np.allclose(A, PPRIME @ U), "left polar A = P' U failed"

# 3D matrices: rotate 60 deg about Z, then diagonal stretch
_th = np.deg2rad(60.0)
P3 = np.diag([1.6, 1.2, 0.6])
U3 = np.array([
    [np.cos(_th), -np.sin(_th), 0.0],
    [np.sin(_th), np.cos(_th), 0.0],
    [0.0, 0.0, 1.0],
])
A3 = U3 @ P3
assert np.allclose(U3 @ U3.T, np.eye(3)), "U3 must be orthogonal"


# ===========================================================================
# Scene 1: The Hook
# ===========================================================================
class ScenePolarHook(LinearTransformationScene):
    """Any complex linear transform = stretch + rotation -> A = U P."""

    def __init__(self, **kwargs):
        super().__init__(show_coordinates=False, leave_ghost_vectors=False, **kwargs)

    def construct(self):
        self.camera.background_color = "#1e1e1e"

        title = cn("ji fen jie A = U P".replace("ji fen jie", "极分解"), color=WHITE, font_size=42)
        title.to_edge(UP, buff=0.4)
        self.add_foreground_mobject(title)
        sub = cn("任何复杂线性变换 = 拉伸 + 旋转", color=GREY_B, font_size=22)
        sub.next_to(title, DOWN, buff=0.25)
        self.add_foreground_mobject(sub)

        circle = Circle(radius=1.0, color=GREEN_E, stroke_width=4)
        circle.set_fill(GREEN_E, opacity=0.25)
        self.add_transformable_mobject(circle)

        # A non-trivial transform: stretch + shear + rotate -> tilted long ellipse
        M = np.array([[2.0, 1.0], [0.0, 1.2]])
        label_A = MathTex("A", color=C_A, font_size=48)
        label_A.to_corner(UL, buff=0.6).shift(DOWN * 1.0)
        self.add_foreground_mobject(label_A)

        self.apply_matrix(M, run_time=4)
        self.wait(0.8)

        eq = MathTex("A", "=", r"U", r"P")
        eq[0].set_color(C_A)
        eq[2].set_color(CU)
        eq[3].set_color(C_P)
        eq.scale(1.6).to_corner(DR, buff=0.7)
        eq.add_background_rectangle()
        self.play(Write(eq), run_time=1.4)
        self.wait(1.5)

        blue_sq = Square(side_length=0.3, color=CU, fill_opacity=1)
        orange_sq = Square(side_length=0.3, color=C_P, fill_opacity=1)
        leg1 = VGroup(blue_sq, cn("U = 旋转", color=CU, font_size=20)).arrange(RIGHT, buff=0.15)
        leg2 = VGroup(orange_sq, cn("P = 拉伸", color=C_P, font_size=20)).arrange(RIGHT, buff=0.15)
        legend = VGroup(leg1, leg2).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        legend.to_corner(DL, buff=0.7).add_background_rectangle()
        self.play(FadeIn(legend, shift=RIGHT), run_time=0.7)
        self.wait(3)


# ===========================================================================
# Scene 2: Core 2D example
# ===========================================================================
class ScenePolar2D(LinearTransformationScene):
    """Right polar decomposition A = U P, step by step, then one-shot A proving coincidence."""

    def __init__(self, **kwargs):
        super().__init__(show_coordinates=True, leave_ghost_vectors=True, **kwargs)

    def construct(self):
        self.camera.background_color = "#1e1e1e"

        title = cn("右极分解 A = U P (先拉伸后旋转)", color=WHITE, font_size=30)
        title.to_edge(UP, buff=0.35)
        self.add_foreground_mobject(title)

        # Matrix numerics top-left
        P_mat = Matrix([["2", "0"], ["0", "1"]], left_bracket="(", right_bracket=")")
        P_mat.scale(0.5).to_corner(UL, buff=0.5).shift(DOWN * 0.15)
        P_lab = MathTex("P=", color=C_P, font_size=28).next_to(P_mat, LEFT, buff=0.1)
        for m in P_mat.get_entries():
            m.set_color(C_P)

        U_mat = Matrix([["0", "-1"], ["1", "0"]], left_bracket="(", right_bracket=")")
        U_mat.scale(0.5).next_to(P_mat, DOWN, buff=0.3, aligned_edge=LEFT)
        U_lab = MathTex("U=", color=CU, font_size=28).next_to(U_mat, LEFT, buff=0.1)
        for m in U_mat.get_entries():
            m.set_color(CU)

        mat_grp = VGroup(P_lab, P_mat, U_lab, U_mat).add_background_rectangle()
        self.add_foreground_mobject(mat_grp)

        # Unit circle as intuitive prop
        circle = Circle(radius=1.0, color=GREEN_E, stroke_width=5)
        circle.set_fill(GREEN_E, opacity=0.3)
        circle.save_state()
        self.plane.save_state()
        self.add_transformable_mobject(circle)

        cap = cn("第一步: P 拉伸 (X 方向 x2)", color=C_P, font_size=24)
        cap.to_edge(DOWN, buff=0.4).add_background_rectangle()
        self.add_foreground_mobject(cap)
        self.wait(0.5)

        # Step 1: P stretch
        self.apply_matrix(P, run_time=3)
        self.wait(1.0)

        cap2 = cn("第二步: U 旋转 (逆时针 90 度)", color=CU, font_size=24)
        cap2.to_edge(DOWN, buff=0.4).add_background_rectangle()
        self.play(Transform(cap, cap2), run_time=0.6)

        # Step 2: U rotation
        self.apply_matrix(U, run_time=3)
        self.wait(1.0)

        # Snapshot of after-two-steps shape (outline only) as the coincidence target
        after_steps = circle.copy().set_stroke(GREEN_B, width=6).set_fill(opacity=0)
        self.add_foreground_mobject(after_steps)

        # Equation verification U P = A
        verify = MathTex(
            r"UP =",
            r"\begin{bmatrix}0&-1\\1&0\end{bmatrix}",
            r"\begin{bmatrix}2&0\\0&1\end{bmatrix}",
            r"=\begin{bmatrix}0&-1\\2&0\end{bmatrix}=A",
        )
        verify.scale(0.7).to_edge(DOWN, buff=0.55).add_background_rectangle()
        self.play(ReplacementTransform(cap, verify), run_time=1.0)
        self.wait(2.2)
        self.remove(verify)

        # Reset the plane and circle to pristine geometry to show "one-shot A"
        self.plane.restore()
        circle.restore()
        for g in list(self.ghost_vectors):
            self.remove(g)
        self.ghost_vectors = VGroup()

        circleB = Circle(radius=1.0, color=YELLOW, stroke_width=5)
        circleB.set_fill(YELLOW, opacity=0.25)
        self.add_transformable_mobject(circleB)

        capB = cn("直接一步: A = U P 作用于原单位圆", color=YELLOW, font_size=22)
        capB.to_edge(DOWN, buff=0.55).add_background_rectangle()
        self.add_foreground_mobject(capB)
        self.wait(0.4)
        self.apply_matrix(A, run_time=3)
        self.wait(1.0)

        ok = cn("两步 (绿轮廓) 与一步 A (黄) 完美重合: U P = A", color=GREEN_B, font_size=22)
        ok.to_edge(DOWN, buff=0.55).add_background_rectangle()
        self.play(ReplacementTransform(capB, ok), run_time=0.8)
        self.wait(3)


# ===========================================================================
# Scene 3: Left vs Right polar decomposition
# ===========================================================================
class ScenePolarLeftRight(LinearTransformationScene):
    """A = U P (right) vs A = P' U (left), illustrating non-commutativity."""

    def __init__(self, **kwargs):
        super().__init__(show_coordinates=True, leave_ghost_vectors=True, **kwargs)

    def construct(self):
        self.camera.background_color = "#1e1e1e"

        title = cn("左极分解 A = P' U  vs  右极分解 A = U P", color=WHITE, font_size=28)
        title.to_edge(UP, buff=0.3)
        self.add_foreground_mobject(title)

        # Two equation rows top-right
        right_eq = MathTex(r"A = U", "P", r"\;\text{(先 }P\text{ 后 }U\text{)}")
        right_eq[1].set_color(C_P)
        left_eq = MathTex(r"A = P'", "U", r"\;\text{(先 }U\text{ 后 }P'\text{)}")
        left_eq[0].set_color(C_P)
        left_eq[1].set_color(C_P)
        eqs = VGroup(right_eq, left_eq).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        eqs.scale(0.7).to_corner(UR, buff=0.35).add_background_rectangle()
        self.add_foreground_mobject(eqs)

        # P' matrix top-left
        pp_mat = Matrix([["1", "0"], ["0", "2"]], left_bracket="(", right_bracket=")")
        pp_mat.scale(0.48).to_corner(UL, buff=0.4).shift(DOWN * 0.15)
        pp_lab = MathTex(r"P'=UPU^{T}=", color=C_P, font_size=28).next_to(pp_mat, LEFT, buff=0.1)
        for m in pp_mat.get_entries():
            m.set_color(C_P)
        pp_grp = VGroup(pp_lab, pp_mat).add_background_rectangle()
        self.add_foreground_mobject(pp_grp)

        circle = Circle(radius=1.0, color=YELLOW_E, stroke_width=5)
        circle.set_fill(YELLOW_E, opacity=0.3)
        circle.save_state()
        self.add_transformable_mobject(circle)

        cap = cn("先 U 旋转 90 度 (形状不变)", color=CU, font_size=24)
        cap.to_edge(DOWN, buff=0.45).add_background_rectangle()
        self.add_foreground_mobject(cap)
        self.wait(0.5)

        # Step 1: U rotation (circle shape unchanged)
        self.apply_matrix(U, run_time=3)
        self.wait(0.8)

        cap2 = cn("后 P' 沿新轴拉伸 (Y 方向 x2)", color=C_P, font_size=24)
        cap2.to_edge(DOWN, buff=0.45).add_background_rectangle()
        self.play(Transform(cap, cap2), run_time=0.6)

        # Step 2: P' stretch
        self.apply_matrix(PPRIME, run_time=3)
        self.wait(1.0)

        verify = MathTex(
            r"P'U =",
            r"\begin{bmatrix}1&0\\0&2\end{bmatrix}",
            r"\begin{bmatrix}0&-1\\1&0\end{bmatrix}",
            r"=\begin{bmatrix}0&-1\\2&0\end{bmatrix}=A",
        )
        verify.scale(0.7).to_edge(DOWN, buff=0.5).add_background_rectangle()
        self.play(ReplacementTransform(cap, verify), run_time=1.0)
        self.wait(2.5)

        concl = cn("矩阵乘法不可交换: P != P'; 但 P' = U P U^T 通过旋转调整拉伸方向达到等价", color=GREEN_B, font_size=20)
        concl.scale(0.85).to_edge(DOWN, buff=0.5).add_background_rectangle()
        self.play(ReplacementTransform(verify, concl), run_time=1.0)
        self.wait(4)


# ===========================================================================
# Scene 4: 3D generalization
# ===========================================================================
class ScenePolar3D(ThreeDScene):
    """3D polar decomposition: sphere -> tilted ellipsoid via U3 P3."""

    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self.set_camera_orientation(phi=70 * DEGREES, theta=-55 * DEGREES)

        title = cn("三维极分解: 球体的拉伸与旋转", color=WHITE, font_size=30)
        title.to_edge(UP, buff=0.3)
        self.add_fixed_in_frame_mobjects(title)

        axes = ThreeDAxes(
            x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[-3, 3, 1],
            x_length=6, y_length=6, z_length=6,
            axis_config={"color": GREY_B, "stroke_width": 2},
        )
        self.add(axes)
        self.wait(0.5)

        sphere = Sphere(radius=1.0, resolution=(24, 16))
        sphere.set_color(GREEN_E, opacity=0.35)
        sphere.set_stroke(GREEN_E, width=1)
        sphere.save_state()
        self.play(FadeIn(sphere, shift=UP * 0.3), run_time=1.0)
        self.wait(0.8)

        cap = cn("整体变换 A3 = U3 P3 一步到位", color=C_A, font_size=22)
        cap.to_edge(DOWN, buff=0.5).add_background_rectangle()
        self.add_fixed_in_frame_mobjects(cap)
        self.wait(0.4)
        self.play(sphere.animate.apply_matrix(A3), run_time=4)
        self.wait(1.5)

        self.begin_ambient_camera_rotation(rate=0.12)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()

        # Decompose and replay: reset, then P3, then U3
        self.remove(cap)
        self.play(sphere.animate.restore(), run_time=0.6)
        self.wait(0.4)

        cap_p = cn("第一步: P3 对称拉伸 -> 正交椭球", color=C_P, font_size=22)
        cap_p.to_edge(DOWN, buff=0.5).add_background_rectangle()
        self.add_fixed_in_frame_mobjects(cap_p)
        self.play(sphere.animate.apply_matrix(P3), run_time=4)
        self.wait(1.2)

        self.remove(cap_p)
        cap_u = cn("第二步: U3 刚体旋转 -> 倾斜椭球", color=CU, font_size=22)
        cap_u.to_edge(DOWN, buff=0.5).add_background_rectangle()
        self.add_fixed_in_frame_mobjects(cap_u)
        self.play(sphere.animate.apply_matrix(U3), run_time=4)
        self.wait(2)

        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(3)
        self.stop_ambient_camera_rotation()


# ===========================================================================
# Scene 5: Conclusion & SVD
# ===========================================================================
class ScenePolarSVD(Scene):
    """Polar decomposition and its link to SVD."""

    def construct(self):
        self.camera.background_color = "#1e1e1e"

        head = cn("总结: 极分解与 SVD", color=WHITE, font_size=40)
        head.to_edge(UP, buff=1.0)
        self.play(Write(head), run_time=1.2)
        self.wait(0.6)

        sq1 = Square(side_length=0.25, color=C_P, fill_opacity=1)
        sq2 = Square(side_length=0.25, color=CU, fill_opacity=1)
        sq3 = Square(side_length=0.25, color=C_A, fill_opacity=1)
        b1 = VGroup(sq1, cn("P = 拉伸前的纯拉伸, 对称正定", color=GREY_A, font_size=24)).arrange(RIGHT, buff=0.2)
        b2 = VGroup(sq2, cn("U = 纯刚体旋转 (可含反射), 保形", color=GREY_A, font_size=24)).arrange(RIGHT, buff=0.2)
        b3 = VGroup(sq3, cn("A = U P : 任何可逆线性变换的唯一拆解", color=GREY_A, font_size=24)).arrange(RIGHT, buff=0.2)
        bullets = VGroup(b1, b2, b3).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        bullets.next_to(head, DOWN, buff=0.9)
        self.play(Write(bullets), run_time=2.5)
        self.wait(1.5)

        # P's own SVD-like decomposition P = V Sigma V^T
        p_decompose = MathTex(r"P = V", r"\Sigma", r"V^{T}")
        p_decompose[1].set_color(C_P)
        p_decompose.scale(1.1).shift(UP * 0.2).add_background_rectangle()
        self.play(FadeOut(bullets), run_time=0.6)
        self.play(Write(p_decompose), run_time=1.5)
        self.wait(1.5)

        # A = U P = (U V) Sigma V^T -> classic SVD
        svd_eq = MathTex(r"A = U", r"(V\Sigma V^{T})", r"= (UV)", r"\Sigma", r"V^{T}")
        svd_eq[0].set_color(CU)
        svd_eq[3].set_color(C_P)
        svd_eq.scale(1.0).next_to(p_decompose, DOWN, buff=0.6).add_background_rectangle()
        self.play(Write(svd_eq), run_time=2.0)
        self.wait(2)

        svd_final = MathTex(r"A = U_{\mathrm{SVD}}\,", r"\Sigma", r"\,V^{T}")
        svd_final[0].set_color(CU)
        svd_final[1].set_color(C_P)
        svd_final.scale(1.4).move_to(ORIGIN + DOWN * 0.3).add_background_rectangle()
        self.play(FadeOut(p_decompose), FadeOut(svd_eq), FadeOut(head), run_time=0.8)
        svd_label = cn("奇异值分解 (SVD)", color=YELLOW_B, font_size=28)
        svd_label.next_to(svd_final, UP, buff=0.4)
        self.play(Write(svd_label), Write(svd_final), run_time=2.0)
        self.wait(3)

        nxt = cn("下期预告: 奇异值分解的完整几何动画", color=GREY_B, font_size=24)
        nxt.next_to(svd_final, DOWN, buff=0.7)
        self.play(FadeIn(nxt, shift=UP), run_time=1.0)
        self.wait(3)
        self.play(FadeOut(VGroup(svd_label, svd_final, nxt)), run_time=1.2)
        self.wait(0.5)
