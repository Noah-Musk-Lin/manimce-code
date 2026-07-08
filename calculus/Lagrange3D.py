from manim import *
import numpy as np

class Lagrange3D(ThreeDScene):
    def construct(self):
        # 设置相机位置
        self.set_camera_orientation(phi=60 * DEGREES, theta=-45 * DEGREES)
        
        # 定义函数 f(x,y) = x^2 + y^2
        def f(x, y):
            return x**2 + y**2
        
        # 定义函数 f 的偏导数
        def fx(x, y):
            return 2*x
        
        def fy(x, y):
            return 2*y
        
        # 定义两个点 P 和 Q
        P = np.array([-1, -1, f(-1, -1)])
        Q = np.array([1, 2, f(1, 2)])
        
        # 计算线段 PQ 的参数方程
        # r(t) = P + t(Q-P), t ∈ [0,1]
        def line_segment(t):
            x = P[0] + t * (Q[0] - P[0])
            y = P[1] + t * (Q[1] - P[1])
            return np.array([x, y, f(x, y)])
        
        # 创建函数曲面
        surface = Surface(
            lambda u, v: np.array([u, v, f(u, v)]),
            u_range=[-2, 2],
            v_range=[-2, 2],
            resolution=(20, 20),
            fill_opacity=0.7,
            stroke_width=0.5,
            fill_color=BLUE
        )
        
        # 创建坐标系 - 进一步向下移动以显示Q点
        axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-2, 6, 2],
            x_length=6,
            y_length=6,
            z_length=4
        ).shift(DOWN * 4.5)  # 增加下移距离到2.5个单位
        
        # 添加标签
        axes_labels = axes.get_axis_labels(
            x_label="x", y_label="y", z_label="z"
        )
        
        # 添加点 P 和 Q
        point_P = Dot3D(point=P, color=RED, radius=0.08)
        point_Q = Dot3D(point=Q, color=RED, radius=0.08)
        
        # 添加点 P 和 Q 的标签
        label_P = Text("P", font_size=24).next_to(point_P, OUT+LEFT, buff=0.1)
        label_Q = Text("Q", font_size=24).next_to(point_Q, OUT+RIGHT, buff=0.1)
        
        # 创建线段 PQ 在曲面上的投影
        curve_points = [line_segment(t) for t in np.linspace(0, 1, 50)]
        curve = VMobject()
        curve.set_points_smoothly([point for point in curve_points])
        curve.set_color(YELLOW).set_stroke(width=4)
        
        # 创建线段 PQ 在 xy 平面上的投影
        line_xy = Line(
            start=[P[0], P[1], 0],
            end=[Q[0], Q[1], 0],
            color=GREEN,
            stroke_width=3
        )
        
        # 创建垂直线段连接曲线和 xy 平面
        vertical_lines = VGroup()
        for t in np.linspace(0, 1, 10):
            point_on_curve = line_segment(t)
            point_on_xy = [point_on_curve[0], point_on_curve[1], 0]
            vertical_line = DashedLine(
                start=point_on_xy,
                end=point_on_curve,
                color=GRAY,
                stroke_width=2
            )
            vertical_lines.add(vertical_line)
        
        # 找到满足拉格朗日中值定理的点 M
        # 计算 f(Q) - f(P)
        f_diff = f(Q[0], Q[1]) - f(P[0], P[1])
        
        # 求解参数 t 找到点 M
        numerator = f_diff - 2*P[0]*(Q[0]-P[0]) - 2*P[1]*(Q[1]-P[1])
        denominator = 2*(Q[0]-P[0])**2 + 2*(Q[1]-P[1])** 2
        t_M = numerator / denominator
        
        # 计算点 M 的坐标
        M = line_segment(t_M)
        point_M = Dot3D(point=M, color=ORANGE, radius=0.1)
        label_M = Text("M", font_size=24).next_to(point_M, OUT+UP, buff=0.1)
        
        # 在点 M 处创建切平面
        def tangent_plane(x, y):
            return f(M[0], M[1]) + fx(M[0], M[1])*(x - M[0]) + fy(M[0], M[1])*(y - M[1])
        
        tangent_surface = Surface(
            lambda u, v: np.array([u, v, tangent_plane(u, v)]),
            u_range=[M[0]-1, M[0]+1],
            v_range=[M[1]-1, M[1]+1],
            resolution=(10, 10),
            fill_opacity=0.5,
            stroke_width=0.5,
            fill_color=RED
        )
        
        # 创建梯度向量
        grad_vector = Arrow3D(
            start=M,
            end=M + np.array([fx(M[0], M[1])/5, fy(M[0], M[1])/5, 0]),
            color=PURPLE,
            thickness=0.02
        )
        
        # 创建 PQ 向量在 xy 平面上的投影
        pq_vector = Arrow3D(
            start=[P[0], P[1], 0],
            end=[Q[0], Q[1], 0],
            color=GREEN,
            thickness=0.02
        )
        
        # 添加标题
        title = Text("二元函数拉格朗日中值定理", font_size=36).to_edge(UP)
        
        # 添加定理陈述
        theorem_text = MathTex(
            r"f(Q) - f(P) = \nabla f(M) \cdot (Q-P)",
            font_size=30
        ).next_to(title, DOWN)
        
        # 将所有图形元素向下移动，与坐标系保持一致
        all_objects = VGroup(
            surface, point_P, point_Q, label_P, label_Q,
            curve, line_xy, vertical_lines,
            point_M, label_M, tangent_surface,
            grad_vector, pq_vector
        ).shift(DOWN * 4.5)  # 同样增加下移距离到2.5个单位
        
        # 动画序列
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # 展示坐标系和曲面
        self.play(Create(axes), Write(axes_labels))
        self.play(Create(surface))
        self.wait(1)
        
        # 展示点 P 和 Q
        self.play(
            Create(point_P), Write(label_P),
            Create(point_Q), Write(label_Q)
        )
        
        # 展示线段 PQ 在 xy 平面上的投影
        self.play(Create(line_xy))
        
        # 展示垂直线段
        self.play(Create(vertical_lines))
        
        # 展示曲线 PQ 在曲面上的投影
        self.play(Create(curve))
        self.wait(1)
        
        # 展示点 M
        self.play(Create(point_M), Write(label_M))
        
        # 展示切平面
        self.play(Create(tangent_surface))
        
        # 展示梯度向量和 PQ 向量
        self.play(Create(grad_vector), Create(pq_vector))
        
        # 展示定理文本
        self.add_fixed_in_frame_mobjects(theorem_text)
        self.play(Write(theorem_text))
        
        # 旋转相机以展示3D效果
        self.begin_ambient_camera_rotation(rate=0.1)
        self.wait(5)
        self.stop_ambient_camera_rotation()
        
        # 最后强调定理
        self.play(
            Flash(point_M, color=ORANGE, line_length=0.3, num_lines=12),
            theorem_text.animate.set_color(YELLOW)
        )
        self.wait(2)

# 运行此场景的命令行指令:
# manim -pql lagrange_3d.py Lagrange3D
