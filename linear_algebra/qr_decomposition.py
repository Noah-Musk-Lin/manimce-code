from manim import *
import numpy as np

CN_FONT = "Microsoft YaHei"


def cn(text, **kw):
    """Chinese-capable Text helper."""
    return Text(text, font=CN_FONT, **kw)


class QRDecomposition(Scene):
    """QR 分解的可视化讲解：用 Gram-Schmidt 把 A 拆成正交矩阵 Q 与上三角矩阵 R。"""

    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self._init_data()
        self._intro()
        self._geometry()
        self._matrix_result()

    # ---------------- 数值常量 ----------------
    def _init_data(self):
        self.a1 = np.array([3.0, 1.0, 0.0])
        self.a2 = np.array([2.0, 3.0, 0.0])
        self.u1 = self.a1.copy()
        d22 = float(np.dot(self.u1, self.u1))      # 10
        d12 = float(np.dot(self.a2, self.u1))      # 9
        self.proj = (d12 / d22) * self.u1          # [2.7, 0.9, 0]
        self.u2 = self.a2 - self.proj             # [-0.7, 2.1, 0]
        self.n_u1 = float(np.linalg.norm(self.u1))  # sqrt(10)
        self.n_u2 = float(np.linalg.norm(self.u2))  # sqrt(4.9)
        self.q1 = self.u1 / self.n_u1
        self.q2 = self.u2 / self.n_u2

    # ---------------- 开场 ----------------
    def _intro(self):
        title = cn("QR 分解  QR Decomposition").scale(0.9)
        sub = cn("把矩阵 A 拆成正交矩阵 Q 与上三角矩阵 R").scale(0.55)
        sub.next_to(title, DOWN, buff=0.4)
        eq = MathTex(r"A = QR", font_size=72).next_to(sub, DOWN, buff=0.6)
        props = MathTex(r"Q^\top Q = I,\quad R\ \text{upper-triangular}").scale(0.7)
        props.next_to(eq, DOWN, buff=0.5)
        g = VGroup(title, sub, eq, props)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.play(Write(eq), run_time=1.0)
        self.play(Write(props))
        self.wait(1.5)
        self.play(FadeOut(g), run_time=0.6)

    # ---------------- 几何：Gram-Schmidt ----------------
    def _geometry(self):
        a1, a2, u1, proj, u2 = self.a1, self.a2, self.u1, self.proj, self.u2
        n_u1, n_u2, q1, q2 = self.n_u1, self.n_u2, self.q1, self.q2
        k = 0.7  # 整体缩放坐标系与向量，避免与顶部标题重叠

        title = cn("Gram-Schmidt 正交化（几何视角）").scale(0.6).to_edge(UP)

        # 先短暂展示矩阵 A 与它的两个列向量
        A_mat = Matrix([[3, 2], [1, 3]])
        A_lab = MathTex("A=").next_to(A_mat, LEFT)
        Am = VGroup(A_lab, A_mat)
        cols = A_mat.get_columns()
        c_lab1 = MathTex(r"\vec a_1", color=BLUE).next_to(cols[0], UP)
        c_lab2 = MathTex(r"\vec a_2", color=RED).next_to(cols[1], UP)
        A_group = VGroup(Am, c_lab1, c_lab2)
        self.play(Write(Am), Write(c_lab1), Write(c_lab2))
        self.wait(1.0)

        # 坐标平面 + 原始向量（按 k 同步缩小，保持网格与向量对齐）
        plane = NumberPlane(
            x_range=[-2, 4, 1], y_range=[-1, 4, 1],
            x_length=6.0 * k, y_length=5.0 * k,
            background_line_style={
                "stroke_color": GRAY, "stroke_opacity": 0.3, "stroke_width": 1},
            axis_config={"stroke_color": "#888888", "stroke_width": 1.5},
        )
        plane.shift(-plane.c2p(0, 0))  # 把坐标原点移到屏幕中心

        v_a1 = Vector(a1 * k, color=BLUE, buff=0)
        v_a2 = Vector(a2 * k, color=RED, buff=0)
        lab_a1 = MathTex(r"\vec a_1", color=BLUE).next_to(a1 * k, RIGHT, buff=0.15)
        lab_a2 = MathTex(r"\vec a_2", color=RED).next_to(a2 * k, UP, buff=0.15)

        self.play(FadeOut(A_group), Create(plane), run_time=1.0)
        self.play(Write(title))
        self.play(GrowArrow(v_a1), Write(lab_a1))
        self.play(GrowArrow(v_a2), Write(lab_a2))

        s0 = self._step("列向量：  a1 = (3, 1),   a2 = (2, 3)")
        self.wait(1.0)
        self.play(FadeOut(s0))

        # 第一步：u1 = a1
        s1 = self._step("第一步：令  u1 = a1", color=YELLOW)
        self.wait(1.2)
        self.play(FadeOut(s1))

        # 第二步：投影
        v_proj = Vector(proj * k, color=YELLOW, buff=0)
        err = DashedLine(proj * k, a2 * k, color=YELLOW, dash_length=0.12)
        proj_lab = MathTex(r"\mathrm{proj}", color=YELLOW, font_size=33)
        proj_lab.next_to(proj * k, DOWN, buff=0.1)
        s2 = self._step_math(
            r"\mathrm{proj}_{\vec u_1}\vec a_2="
            r"\frac{\vec a_2\!\cdot\!\vec u_1}{\vec u_1\!\cdot\!\vec u_1}\vec u_1"
            r"=\frac{9}{10}\begin{bmatrix}3\\1\end{bmatrix}")
        self.play(GrowArrow(v_proj), Write(proj_lab))
        self.play(Create(err))
        self.wait(1.5)
        self.play(FadeOut(s2))

        # 第三步：u2 = a2 - proj，把“误差线段”滑到原点变成 u2
        s3 = self._step_math(
            r"\vec u_2=\vec a_2-\mathrm{proj}"
            r"=\begin{bmatrix}2\\3\end{bmatrix}-\begin{bmatrix}2.7\\0.9\end{bmatrix}"
            r"=\begin{bmatrix}-0.7\\2.1\end{bmatrix}")
        self.play(err.animate.shift(-(proj * k)), run_time=1.2)
        v_u2 = Vector(u2 * k, color=GREEN, buff=0)
        self.play(ReplacementTransform(err, v_u2), run_time=1.0)
        lab_u2 = MathTex(r"\vec u_2", color=GREEN).next_to(u2 * k, LEFT, buff=0.15)
        self.play(Write(lab_u2))
        ra = RightAngle(v_a1, v_u2, length=0.3, color=WHITE)
        self.play(Create(ra), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(s3))

        # 第四步：单位化
        s4 = self._step_math(
            r"\vec q_1=\frac{\vec u_1}{\|\vec u_1\|},"
            r"\quad \vec q_2=\frac{\vec u_2}{\|\vec u_2\|}")
        q1_lab = MathTex(r"\vec q_1", color=WHITE).next_to(q1 * k, RIGHT, buff=0.15)
        q2_lab = MathTex(r"\vec q_2", color=WHITE).next_to(q2 * k, LEFT, buff=0.15)
        ra2 = RightAngle(Line(ORIGIN, q1 * k), Line(ORIGIN, q2 * k),
                         length=0.3, color=WHITE)
        self.play(
            v_a1.animate.scale(1.0 / n_u1, about_point=ORIGIN),
            v_u2.animate.scale(1.0 / n_u2, about_point=ORIGIN),
            run_time=1.4)
        self.play(
            v_a1.animate.set_color(WHITE),
            v_u2.animate.set_color(WHITE),
            Transform(lab_a1, q1_lab),
            Transform(lab_u2, q2_lab),
            Transform(ra, ra2),
            FadeOut(v_proj), FadeOut(proj_lab),
            run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(s4))

        geom = VGroup(plane, title, v_a1, v_a2, v_u2,
                      lab_a1, lab_a2, lab_u2, ra)
        self.play(FadeOut(geom), run_time=0.8)

    # ---------------- 构造 Q 与 R 并验证 ----------------
    def _matrix_result(self):
        title = cn("构造 Q 与 R").scale(0.7).to_edge(UP)

        Q_tex = MathTex(
            r"Q=\bigl[\,\vec q_1\ \ \vec q_2\,\bigr]"
            r"=\frac{\sqrt{10}}{10}\begin{bmatrix}3&-1\\1&3\end{bmatrix}",
            font_size=52,
        ).move_to(UP * 1.8)
        q_note = cn("Q 的列：单位正交基").scale(0.5)
        q_note.next_to(Q_tex, DOWN, buff=0.25)

        R_tex = MathTex(
            r"R=\begin{bmatrix}\|\vec u_1\|&\vec a_2\!\cdot\!\vec q_1\\"
            r"0&\|\vec u_2\|\end{bmatrix}"
            r"=\frac{\sqrt{10}}{10}\begin{bmatrix}10&9\\0&7\end{bmatrix}",
            font_size=52,
        ).move_to(DOWN * 1.8)
        r_note = cn("R 上三角：主对角元 = 各向量长度").scale(0.5)
        r_note.next_to(R_tex, DOWN, buff=0.25)

        self.play(Write(title))
        self.play(Write(Q_tex), FadeIn(q_note))
        self.wait(1.2)
        self.play(Write(R_tex), FadeIn(r_note))
        self.wait(2.8)
        self.play(FadeOut(VGroup(Q_tex, q_note, R_tex, r_note, title)))

        # 验证 A = QR
        v_title = cn("验证  A = Q R").scale(0.7).to_edge(UP)
        verify = MathTex(
            r"QR=\frac{1}{10}\begin{bmatrix}3&-1\\1&3\end{bmatrix}"
            r"\begin{bmatrix}10&9\\0&7\end{bmatrix}"
            r"=\begin{bmatrix}3&2\\1&3\end{bmatrix}=A",
            font_size=50)
        check = cn("分解正确", color=GREEN).scale(0.7)
        check.next_to(verify, DOWN, buff=0.5)
        self.play(Write(v_title))
        self.play(Write(verify))
        self.wait(1.5)
        self.play(Write(check))

        note = cn("应用：最小二乘解  |  QR 算法求特征值  |  数值上比直接求逆更稳定").scale(0.5)
        note.to_edge(DOWN)
        self.play(FadeIn(note, shift=0.2 * UP))
        self.wait(3)

    # ---------------- 工具：底部一行说明 ----------------
    def _step(self, text, color=WHITE):
        bar = cn(text, color=color).scale(0.5).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bar, shift=0.2 * UP))
        return bar

    def _step_math(self, tex, color=WHITE):
        bar = MathTex(tex, color=color, font_size=38).to_edge(DOWN, buff=0.4)
        if bar.width > 12:
            bar.scale(12 / bar.width)
        self.play(FadeIn(bar, shift=0.2 * UP))
        return bar
