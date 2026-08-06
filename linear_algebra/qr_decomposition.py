from manim import *
import numpy as np

CN_FONT = "Microsoft YaHei"

def cn(text, **kw):
    """Chinese-capable Text helper."""
    return Text(text, font=CN_FONT, **kw)

class QRDecomposition(Scene):
    """QR 分解的 150 秒（2分30秒）适配版"""

    def construct(self):
        self.camera.background_color = "#1e1e1e"
        self._init_data()
        self._intro()
        self._geometry()
        self._matrix_result()

    def _init_data(self):
        self.a1 = np.array([3.0, 1.0, 0.0])
        self.a2 = np.array([2.0, 3.0, 0.0])
        self.u1 = self.a1.copy()
        d22 = float(np.dot(self.u1, self.u1))
        d12 = float(np.dot(self.a2, self.u1))
        self.proj = (d12 / d22) * self.u1
        self.u2 = self.a2 - self.proj
        self.n_u1 = float(np.linalg.norm(self.u1))
        self.n_u2 = float(np.linalg.norm(self.u2))
        self.q1 = self.u1 / self.n_u1
        self.q2 = self.u2 / self.n_u2

    def _intro(self):
        # 【时间轴：00:00 - 00:20，约 20 秒】
        # 对应配音：“欢迎来到几何的世界... 也就是 A=QR。让我们来看一个具体的例子...”
        title = cn("QR 分解  QR Decomposition").scale(0.9)
        sub = cn("把矩阵 A 拆成正交矩阵 Q 与上三角矩阵 R").scale(0.55).next_to(title, DOWN, buff=0.4)
        eq = MathTex(r"A = QR", font_size=72).next_to(sub, DOWN, buff=0.6)
        props = MathTex(r"Q^\top Q = I,\quad R\ \text{upper-triangular}").scale(0.7).next_to(eq, DOWN, buff=0.5)
        g = VGroup(title, sub, eq, props)
        
        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(sub, shift=0.3 * UP))
        self.play(Write(eq), run_time=1.5)
        self.play(Write(props))
        self.wait(14.0)  # 留足 14 秒给曼波念完开场白
        self.play(FadeOut(g), run_time=1.0)

    def _geometry(self):
        a1, a2, u1, proj, u2 = self.a1, self.a2, self.u1, self.proj, self.u2
        n_u1, n_u2, q1, q2 = self.n_u1, self.n_u2, self.q1, self.q2
        k = 0.7  

        title = cn("Gram-Schmidt 正交化（几何视角）").scale(0.6).to_edge(UP)

        # 【时间轴：00:20 - 00:35，约 15 秒】
        # 对应配音：“矩阵 A 由两个列向量 a1 和 a2 组成。让我们把这两个列向量放到二维坐标系中...”
        A_mat = Matrix([[3, 2], [1, 3]])
        A_lab = MathTex("A=").next_to(A_mat, LEFT)
        Am = VGroup(A_lab, A_mat)
        cols = A_mat.get_columns()
        c_lab1 = MathTex(r"\vec a_1", color=BLUE).next_to(cols[0], UP)
        c_lab2 = MathTex(r"\vec a_2", color=RED).next_to(cols[1], UP)
        A_group = VGroup(Am, c_lab1, c_lab2)
        
        self.play(Write(Am), Write(c_lab1), Write(c_lab2), run_time=1.5)
        self.wait(5.0) 

        plane = NumberPlane(
            x_range=[-2, 4, 1], y_range=[-1, 4, 1],
            x_length=6.0 * k, y_length=5.0 * k,
            background_line_style={"stroke_color": GRAY, "stroke_opacity": 0.3, "stroke_width": 1},
            axis_config={"stroke_color": "#888888", "stroke_width": 1.5},
        )
        plane.shift(-plane.c2p(0, 0))

        v_a1 = Vector(a1 * k, color=BLUE, buff=0)
        v_a2 = Vector(a2 * k, color=RED, buff=0)
        lab_a1 = MathTex(r"\vec a_1", color=BLUE).next_to(a1 * k, RIGHT, buff=0.15)
        lab_a2 = MathTex(r"\vec a_2", color=RED).next_to(a2 * k, UP, buff=0.15)

        self.play(FadeOut(A_group), Create(plane), run_time=1.5)
        self.play(Write(title))
        self.play(GrowArrow(v_a1), Write(lab_a1), run_time=1.0)
        self.play(GrowArrow(v_a2), Write(lab_a2), run_time=1.0)
        self.wait(5.0)

        # 【时间轴：00:35 - 00:45，约 10 秒】
        # 对应配音：“你可以看到... 并不是完美的90度。第一步最简单，把 a1 作为第一根基准标尺，记作 u1。”
        s1 = self._step("第一步：令  u1 = a1", color=YELLOW)
        self.wait(9.0)
        self.play(FadeOut(s1))

        # 【时间轴：00:45 - 01:00，约 15 秒】
        # 对应配音：“接下来是见证奇迹的时刻... 算出这个投影分量，也就是画面中这根黄色的向量。”
        v_proj = Vector(proj * k, color=YELLOW, buff=0)
        err = DashedLine(proj * k, a2 * k, color=YELLOW, dash_length=0.12)
        proj_lab = MathTex(r"\mathrm{proj}", color=YELLOW, font_size=33).next_to(proj * k, DOWN, buff=0.1)
        s2 = self._step_math(
            r"\mathrm{proj}_{\vec u_1}\vec a_2="
            r"\frac{\vec a_2\!\cdot\!\vec u_1}{\vec u_1\!\cdot\!\vec u_1}\vec u_1"
            r"=\frac{9}{10}\begin{bmatrix}3\\1\end{bmatrix}")
        
        self.wait(3.0) 
        self.play(GrowArrow(v_proj), Write(proj_lab), run_time=2.0)
        self.play(Create(err), run_time=1.0)
        self.wait(8.0)
        self.play(FadeOut(s2))

        # 【时间轴：01:00 - 01:20，约 20 秒】
        # 对应配音：“既然我们不需要顺着的方向，那就用向量减法... 剩下的就是垂直的绿色向量 u2。看，直角诞生了！”
        s3 = self._step_math(
            r"\vec u_2=\vec a_2-\mathrm{proj}"
            r"=\begin{bmatrix}2\\3\end{bmatrix}-\begin{bmatrix}2.7\\0.9\end{bmatrix}"
            r"=\begin{bmatrix}-0.7\\2.1\end{bmatrix}")
        
        self.wait(3.0)
        self.play(err.animate.shift(-(proj * k)), run_time=2.5) # 缓慢平移，让观众看清减法
        v_u2 = Vector(u2 * k, color=GREEN, buff=0)
        self.play(ReplacementTransform(err, v_u2), run_time=1.0)
        lab_u2 = MathTex(r"\vec u_2", color=GREEN).next_to(u2 * k, LEFT, buff=0.15)
        self.play(Write(lab_u2))
        
        self.wait(2.0)
        ra = RightAngle(v_a1, v_u2, length=0.3, color=WHITE)
        self.play(Create(ra), run_time=1.0)
        self.wait(9.0)
        self.play(FadeOut(s3))

        # 【时间轴：01:20 - 01:45，约 25 秒】
        # 对应配音：“现在我们有了互相垂直的 u1 和 u2，但长度参差不齐... 长度都是 1，这正是标准正交基！”
        s4 = self._step_math(
            r"\vec q_1=\frac{\vec u_1}{\|\vec u_1\|},"
            r"\quad \vec q_2=\frac{\vec u_2}{\|\vec u_2\|}")
        q1_lab = MathTex(r"\vec q_1", color=WHITE).next_to(q1 * k, RIGHT, buff=0.15)
        q2_lab = MathTex(r"\vec q_2", color=WHITE).next_to(q2 * k, LEFT, buff=0.15)
        ra2 = RightAngle(Line(ORIGIN, q1 * k), Line(ORIGIN, q2 * k), length=0.3, color=WHITE)
        
        self.wait(6.0) 
        self.play(
            v_a1.animate.scale(1.0 / n_u1, about_point=ORIGIN),
            v_u2.animate.scale(1.0 / n_u2, about_point=ORIGIN),
            run_time=2.5)
        self.play(
            v_a1.animate.set_color(WHITE),
            v_u2.animate.set_color(WHITE),
            Transform(lab_a1, q1_lab),
            Transform(lab_u2, q2_lab),
            Transform(ra, ra2),
            FadeOut(v_proj), FadeOut(proj_lab),
            run_time=2.0)
        self.wait(12.0)
        self.play(FadeOut(s4))

        geom = VGroup(plane, title, v_a1, v_a2, v_u2, lab_a1, lab_a2, lab_u2, ra)
        self.play(FadeOut(geom), run_time=1.0)

    def _matrix_result(self):
        title = cn("构造 Q 与 R").scale(0.7).to_edge(UP)

        # 【时间轴：01:45 - 01:55，约 10 秒】
        # 对应配音：“几何变换结束了... 我们把它们并列排在一起，就构成了正交矩阵Q”
        Q_tex = MathTex(
            r"Q=\bigl[\,\vec q_1\ \ \vec q_2\,\bigr]"
            r"=\frac{\sqrt{10}}{10}\begin{bmatrix}3&-1\\1&3\end{bmatrix}",
            font_size=52,
        ).move_to(UP * 1.8)
        q_note = cn("Q 的列：单位正交基").scale(0.5).next_to(Q_tex, DOWN, buff=0.25)

        self.play(Write(title))
        self.wait(2.0)
        self.play(Write(Q_tex), FadeIn(q_note))
        self.wait(6.0) 

        # 【时间轴：01:55 - 02:15，约 20 秒】
        # 对应配音：“那么矩阵 R 是什么呢？它其实是一本历史备忘录... 左下角永远是0，保证是上三角矩阵。”
        R_tex = MathTex(
            r"R=\begin{bmatrix}\|\vec u_1\|&\vec a_2\!\cdot\!\vec q_1\\"
            r"0&\|\vec u_2\|\end{bmatrix}"
            r"=\frac{\sqrt{10}}{10}\begin{bmatrix}10&9\\0&7\end{bmatrix}",
            font_size=52,
        ).move_to(DOWN * 1.8)
        r_note = cn("R 上三角：主对角元 = 各向量长度").scale(0.5).next_to(R_tex, DOWN, buff=0.25)
        
        self.play(Write(R_tex), FadeIn(r_note))
        self.wait(18.0) 
        self.play(FadeOut(VGroup(Q_tex, q_note, R_tex, r_note, title)))

        # 【时间轴：02:15 - 02:30+，约 15 秒及以上结尾】
        # 对应配音：“最后，让我们来验算一下... 在工程中非常强大，数值上比直接求逆要稳定得多。”
        v_title = cn("验证  A = Q R").scale(0.7).to_edge(UP)
        verify = MathTex(
            r"QR=\frac{1}{10}\begin{bmatrix}3&-1\\1&3\end{bmatrix}"
            r"\begin{bmatrix}10&9\\0&7\end{bmatrix}"
            r"=\begin{bmatrix}3&2\\1&3\end{bmatrix}=A",
            font_size=50)
        check = cn("分解正确", color=GREEN).scale(0.7).next_to(verify, DOWN, buff=0.5)
        
        self.play(Write(v_title))
        self.play(Write(verify), run_time=2.0)
        self.wait(3.0)
        self.play(Write(check))
        self.wait(2.0)

        note = cn("应用：最小二乘解  |  QR 算法求特征值  |  数值上比直接求逆更稳定").scale(0.5).to_edge(DOWN)
        self.play(FadeIn(note, shift=0.2 * UP))
        self.wait(12.0) # 留给最后的结尾升华，视频黑屏前多留一点缓冲时间

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