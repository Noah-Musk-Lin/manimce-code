"""
矩阵LU分解的几何直观 —— Manim 动画脚本

按照 Plan/gemini-code-1786128246647.yaml 的 5 个场景实现。
采用 ProjectCode 风格：手动网格 + animate.apply_matrix + save_state/restore。
参考 project_linear/main.py 的视觉实践。

用法：
    manim -pql linear_algebra/LU_decomposition_geometric.py LUDecompositionGeometric
    manim -pqh linear_algebra/LU_decomposition_geometric.py LUDecompositionGeometric
"""

from manim import *
import numpy as np

# ═══════════════════════════════════════════════
# 颜色常量（plan 指定）
# ═══════════════════════════════════════════════
C_I   = GREEN
C_J   = RED
C_A   = PURPLE
C_U   = BLUE
C_L   = YELLOW
C_KEY = YELLOW
C_BG  = "#1e1e1e"
CN_FONT = "Microsoft YaHei"


def cn(txt, **kw):
    return Text(txt, font=CN_FONT, **kw)


# 矩阵数据
MAT_A = np.array([[2.0, 1.0], [4.0, 5.0]], dtype=np.float64)
MAT_U = np.array([[2.0, 1.0], [0.0, 3.0]], dtype=np.float64)
MAT_L = np.array([[1.0, 0.0], [2.0, 1.0]], dtype=np.float64)
MAT_A_3D = np.array([[2.0, 1.0, 0.0], [4.0, 5.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.float64)
MAT_U_3D = np.array([[2.0, 1.0, 0.0], [0.0, 3.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.float64)
MAT_L_3D = np.array([[1.0, 0.0, 0.0], [2.0, 1.0, 0.0], [0.0, 0.0, 0.0]], dtype=np.float64)


class LUDecompositionGeometric(Scene):
    """LU 分解几何直观 — 5场景 约160s"""

    def construct(self):
        self.camera.background_color = C_BG
        self._scene_1_intro()       # 25s
        self._scene_2_U()           # 35s
        self._scene_3_L()           # 35s
        self._scene_4_compose()     # 45s
        self._scene_5_summary()     # 20s

    # ═══════════════════════════════════════════════
    # 内部工具：手动网格（ProjectCode 风格）
    # ═══════════════════════════════════════════════
    def _build_grid(self):
        """返回 (grid, arrows, points, background)。ProjectCode 风格的网格+基向量+点阵。"""
        ratio = 0.4
        left, right = 70 * ratio * LEFT, 70 * ratio * RIGHT
        up, down = 40 * ratio * DOWN, 40 * ratio * UP
        axis_x = Line(up, down)
        axis_y = Line(left, right)

        lines_h = VGroup(*[
            Line(left + i * ratio * UP, right + i * ratio * UP,
                 stroke_width=2, color=BLUE_E)
            for i in range(-40, 41)
        ])
        lines_v = VGroup(*[
            Line(up + i * ratio * RIGHT, down + i * ratio * RIGHT,
                 stroke_width=2, color=BLUE_E)
            for i in range(-70, 71)
        ])
        grid = VGroup(lines_h, lines_v)

        # 离散点阵（变换后自动变成拉伸后的点阵）
        points = VGroup(*[
            Dot(i * ratio * UP + j * ratio * RIGHT, radius=0.06, color=GREY)
            for i in range(16) for j in range(40)
        ])

        arrows = VGroup(
            Arrow(ORIGIN, ratio * RIGHT, color=C_I, buff=0),
            Arrow(ORIGIN, ratio * UP, color=C_J, buff=0),
        )

        background = VGroup(
            lines_h.copy().set_stroke(GREY, width=1),
            lines_v.copy().set_stroke(GREY, width=1),
            axis_x.copy(),
            axis_y.copy(),
        )

        return grid, arrows, points, background

    def _apply_matrix(self, mat_2d, grid, arrows, points, run_time=3):
        """对网格、箭头、点阵施加矩阵变换（ProjectCode 风格）"""
        mat_3d = np.array([[mat_2d[0, 0], mat_2d[0, 1], 0],
                           [mat_2d[1, 0], mat_2d[1, 1], 0],
                           [0, 0, 0]], dtype=np.float64)
        self.play(
            *[mob.save_state().animate.apply_matrix(mat_2d)
              for mob in [grid, *arrows]],
            *[mob.save_state().animate.move_to(
                np.dot(mat_3d, mob.get_center()))
              for mob in points],
            run_time=run_time,
            rate_func=smooth,
        )

    def _restore_grid(self, grid, arrows, points, run_time=3):
        """恢复网格到标准状态"""
        self.play(
            *[mob.animate.restore() for mob in [grid, *arrows] + list(points)],
            run_time=run_time,
            rate_func=smooth,
        )

    def _fade_all(self, *extras):
        all_mobs = list(self.mobjects)
        if extras:
            all_mobs.extend(extras)
        if all_mobs:
            self.play(*[FadeOut(m) for m in all_mobs], run_time=0.6)

    # ═══════════════════════════════════════════════
    # Scene 1: 引入线性变换与矩阵拆分 (25s)
    # ═══════════════════════════════════════════════
    def _scene_1_intro(self):
        # ── 标题（居中） ──
        title = cn("矩阵 LU 分解", color=C_A, font_size=48)
        sub = cn("把复杂变换拆成两次单轴方向不变的变换", font_size=28, color=WHITE)
        heading = VGroup(title, sub).arrange(DOWN, buff=0.2)
        heading.move_to(ORIGIN)
        self.play(Write(heading), run_time=1.5)
        self.wait(2)

        # ── 矩阵 A ──
        A_mat = Matrix([["2", "1"], ["4", "5"]],
                       left_bracket="(", right_bracket=")",
                       element_to_mobject_config={"color": C_A, "font_size": 40})
        A_lab = MathTex("A=", color=C_A, font_size=40).next_to(A_mat, LEFT)
        Am = VGroup(A_lab, A_mat).move_to(ORIGIN)
        self.play(FadeOut(heading), Write(Am), run_time=1.5)
        self.wait(1.5)

        # ── 网格 ──
        grid, arrows, points, bg = self._build_grid()
        self.play(FadeOut(Am))
        self.bring_to_back(bg)
        self.play(FadeIn(grid), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  *[GrowFromCenter(p) for p in points], run_time=1.5)
        self.add(*points, *arrows)
        self.wait(0.5)

        # ── A 变换 ──
        self._apply_matrix(MAT_A, grid, arrows, points, run_time=3)
        self.wait(3)

        # ── 淡出 → 分解公式 ──
        self._fade_all()

        eq = MathTex(r"A = L \cdot U", font_size=72, color=WHITE)
        L_note = cn("L: 下三角 (Lower triangular)", font_size=28, color=C_L)
        U_note = cn("U: 上三角 (Upper triangular)", font_size=28, color=C_U)
        notes = VGroup(L_note, U_note).arrange(DOWN, buff=0.2)
        g = VGroup(eq, notes).arrange(DOWN, buff=0.5)
        self.play(Write(eq), Write(notes))
        self.wait(5)
        self._fade_all()

    # ═══════════════════════════════════════════════
    # Scene 2: 上三角矩阵 U 的几何意义 (35s)
    # ═══════════════════════════════════════════════
    def _scene_2_U(self):
        title = cn("上三角矩阵 U 的几何意义", color=C_U, font_size=38).to_edge(UP, buff=0.35)

        # U 矩阵
        U_mat = Matrix([["2", "1"], ["0", "3"]],
                       left_bracket="(", right_bracket=")",
                       element_to_mobject_config={"color": C_U, "font_size": 40})
        U_lab = MathTex("U=", color=C_U, font_size=40).next_to(U_mat, LEFT)
        Um = VGroup(U_lab, U_mat).next_to(title, DOWN, buff=0.5)

        # 高亮左下角 0
        zero_cell = U_mat.get_rows()[1][0]
        zero_rect = SurroundingRectangle(zero_cell, color=C_KEY, buff=0.1, stroke_width=3)

        self.play(Write(title), run_time=0.8)
        self.play(Write(Um), run_time=1.2)
        self.play(Create(zero_rect))
        self.wait(1.5)

        note = cn("左下角为 0 → x 轴方向不变", color=C_KEY, font_size=28)
        note.next_to(Um, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(1.5)

        # ── 网格 + U 变换 ──
        self.play(FadeOut(VGroup(Um, zero_rect, note)))
        grid, arrows, points, bg = self._build_grid()
        self.bring_to_back(bg)
        self.play(FadeIn(grid), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  *[GrowFromCenter(p) for p in points], run_time=1.2)
        self.add(*points, *arrows)

        hint = cn("U 变换：i-hat 只被拉伸，x轴不变", color=C_KEY, font_size=26)
        hint.to_edge(DOWN, buff=0.35)
        self.play(Write(hint))

        self._apply_matrix(MAT_U, grid, arrows, points, run_time=2.5)
        self.wait(3)
        self.play(FadeOut(hint))

        emphasis = cn("i-hat 只被水平拉伸，没有离开 x 轴！", color=C_KEY, font_size=30)
        emphasis.to_edge(DOWN, buff=0.35)
        self.play(Write(emphasis))
        self.wait(5)

        self._fade_all(title)

    # ═══════════════════════════════════════════════
    # Scene 3: 下三角矩阵 L 的几何意义 (35s)
    # ═══════════════════════════════════════════════
    def _scene_3_L(self):
        title = cn("下三角矩阵 L 的几何意义", color=C_L, font_size=38).to_edge(UP, buff=0.35)

        # L 矩阵
        L_mat = Matrix([["1", "0"], ["2", "1"]],
                       left_bracket="(", right_bracket=")",
                       element_to_mobject_config={"color": C_L, "font_size": 40})
        L_lab = MathTex("L=", color=C_L, font_size=40).next_to(L_mat, LEFT)
        Lm = VGroup(L_lab, L_mat).next_to(title, DOWN, buff=0.5)

        # 高亮右上角 0 + 对角线 1
        L_rows = L_mat.get_rows()
        zero_rect = SurroundingRectangle(L_rows[0][1], color=C_J, buff=0.1, stroke_width=3)
        diag_rects = VGroup(
            SurroundingRectangle(L_rows[0][0], color=C_KEY, buff=0.08, stroke_width=2),
            SurroundingRectangle(L_rows[1][1], color=C_KEY, buff=0.08, stroke_width=2),
        )

        self.play(Write(title), run_time=0.8)
        self.play(Write(Lm), run_time=1.2)
        self.play(Create(zero_rect), Create(diag_rects))
        self.wait(1.5)

        note = cn("右上角为 0, 对角线全为 1 → y 轴不变", color=C_J, font_size=28)
        note.next_to(Lm, DOWN, buff=0.4)
        self.play(Write(note))
        self.wait(1.5)

        # ── 网格 + L 变换 ──
        self.play(FadeOut(VGroup(Lm, zero_rect, diag_rects, note)))
        grid, arrows, points, bg = self._build_grid()
        self.bring_to_back(bg)
        self.play(FadeIn(grid), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  *[GrowFromCenter(p) for p in points], run_time=1.2)
        self.add(*points, *arrows)

        hint = cn("L 变换：j-hat 完全不改变 (垂直剪切)", color=C_J, font_size=26)
        hint.to_edge(DOWN, buff=0.35)
        self.play(Write(hint))

        self._apply_matrix(MAT_L, grid, arrows, points, run_time=2.5)
        self.wait(3)
        self.play(FadeOut(hint))

        emphasis = cn("j-hat 完全没有改变！i-hat 向上倾斜", color=C_J, font_size=30)
        emphasis.to_edge(DOWN, buff=0.35)
        self.play(Write(emphasis))
        self.wait(5)

        self._fade_all(title)

    # ═══════════════════════════════════════════════
    # Scene 4: 拼图游戏——从 U 到 L (45s)
    # ═══════════════════════════════════════════════
    def _scene_4_compose(self):
        title = cn("拼图：先 U 后 L = A", color=C_KEY, font_size=38).to_edge(UP, buff=0.35)

        flow = MathTex(
            r"\mathbf{x} \;\xrightarrow{\;U\;}\; U\mathbf{x}"
            r"\;\xrightarrow{\;L\;}\; A\mathbf{x}",
            font_size=36, color=WHITE,
        ).next_to(title, DOWN, buff=0.4)

        self.play(Write(title), run_time=0.8)
        self.play(Write(flow), run_time=1)
        self.wait(1)

        # ── 网格 ──
        grid, arrows, points, bg = self._build_grid()
        self.bring_to_back(bg)
        self.play(FadeIn(grid), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  *[GrowFromCenter(p) for p in points], run_time=1.2)
        self.add(*points, *arrows)

        # ── 第一步：U ──
        s1 = cn("第一步：U 变换 (保持 x 轴方向不变)", color=C_U, font_size=26)
        s1.to_edge(DOWN, buff=0.35)
        self.play(Write(s1))
        self._apply_matrix(MAT_U, grid, arrows, points, run_time=2.5)
        self.wait(2)

        # ── 第二步：直接在变形基础上叠加 L ──
        self.play(FadeOut(s1))
        s2 = cn("第二步：L 变换 (保持 y 轴方向不变)", color=C_L, font_size=26)
        s2.to_edge(DOWN, buff=0.35)
        self.play(Write(s2))
        self._apply_matrix(MAT_L, grid, arrows, points, run_time=2.5)
        self.wait(2)

        # ── 完美重合 ──
        self.play(FadeOut(s2))
        coincide = cn("两次变换组合 = 直接应用 A —— 完美重合", color=C_KEY, font_size=30)
        coincide.to_edge(DOWN, buff=0.35)
        self.play(Write(coincide))
        self.wait(6)

        self._fade_all(title, flow)

    # ═══════════════════════════════════════════════
    # Scene 5: 总结与高斯消元 (20s)
    # ═══════════════════════════════════════════════
    def _scene_5_summary(self):
        title = cn("总结：高斯消元的矩阵表达", color=C_A, font_size=38).to_edge(UP, buff=0.35)
        self.play(Write(title), run_time=0.8)

        # ── A 变换后的网格 ──
        grid, arrows, points, bg = self._build_grid()
        self.bring_to_back(bg)
        self.play(FadeIn(grid), GrowArrow(arrows[0]), GrowArrow(arrows[1]),
                  *[GrowFromCenter(p) for p in points], run_time=1.0)
        self.add(*points, *arrows)

        self._apply_matrix(MAT_A, grid, arrows, points, run_time=1.8)
        self.wait(0.5)

        # ── Ax = b → L(Ux) = b ──
        eq1 = MathTex(r"A\mathbf{x} = \mathbf{b}", font_size=56, color=WHITE)
        eq1.next_to(title, DOWN, buff=0.8)
        self.play(Write(eq1))
        self.wait(2)

        eq2 = MathTex(r"L\,(U\mathbf{x}) = \mathbf{b}", font_size=56, color=WHITE)
        eq2.move_to(eq1)
        self.play(TransformMatchingTex(eq1, eq2, run_time=2))
        self.wait(2)

        gaussian = cn("高斯消元法 (Gaussian Elimination) 的矩阵表达",
                      color=C_KEY, font_size=30)
        gaussian.next_to(eq2, DOWN, buff=0.7)
        self.play(Write(gaussian))
        self.wait(4)

        self._fade_all()

        # ── 结束语 ──
        thanks = VGroup(
            cn("懂了几何直观，线性代数就不再是死记硬背", font_size=34, color=WHITE),
            cn("感谢观看！点赞 + 关注", font_size=38, color=C_KEY),
        ).arrange(DOWN, buff=0.4)
        self.play(Write(thanks))
        self.wait(5)
        self.play(FadeOut(thanks), run_time=0.6)
