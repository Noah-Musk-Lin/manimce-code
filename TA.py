from manim import *

class Test(Scene):
    def construct(self):
        # 创建坐标系
        axes = Axes(
            x_range=[-3, 3], 
            y_range=[-3, 3],
            axis_config={"color": GREY, "include_numbers": True, "stroke_width": 2}
        )
        zerolabel = Text("0", font="SimSun", font_size=26).move_to(axes.c2p(-0.1, -0.2))
        self.play(FadeIn(axes), FadeIn(zerolabel))
        
        # 显示旋转矩阵信息（中文用Text，公式用MathTex）
        info3_text = Text("旋转矩阵:", font="SimSun", font_size=30).move_to(axes.c2p(-4.5, 2.3))
        info3_math = MathTex(
            r"A=\begin{bmatrix} \cos\alpha & -\sin\alpha \\ \sin\alpha & \cos\alpha \end{bmatrix}",
            font_size=30
        ).next_to(info3_text, DOWN, aligned_edge=LEFT)
        info3 = VGroup(info3_text, info3_math)
        self.play(FadeIn(info3))
        
        # 显示作用向量信息（中文用Text，公式用MathTex）
        info4_text = Text("作用于向量:", font="SimSun", font_size=30, color=RED).next_to(info3, DOWN, aligned_edge=LEFT)
        info4_math = MathTex(
            r"x=\begin{bmatrix} 2 \\ 1 \end{bmatrix}",
            font_size=30, 
            color=RED
        ).next_to(info4_text, RIGHT, buff=0.2)
        info4 = VGroup(info4_text, info4_math)
        self.play(FadeIn(info4))
        
        # 创建向量x
        x = Arrow(
            start=axes.c2p(0, 0), 
            end=axes.c2p(2, 1), 
            buff=0, 
            color=RED,
            tip_length=0.2,
            max_stroke_width_to_length_ratio=999,
            max_tip_length_to_length_ratio=0.2
        )
        self.play(Create(x))
        
        x_label = MathTex(r"x", font_size=30, color=RED).move_to(axes.c2p(2.1, 1.1))
        self.play(FadeIn(x_label))
        
        # 显示矩阵乘法信息（保留公式，中文部分如需可拆分）
        info5 = MathTex(r"A", font_size=40, color=WHITE).next_to(info4, DOWN*2).shift(LEFT*0.5)
        info5_1 = MathTex(r"x", font_size=40, color=RED).next_to(info5, RIGHT, buff=0.1).shift(DOWN*0.05)
        info5_2 = MathTex(r"=b", font_size=40, color=BLUE).next_to(info5_1, RIGHT, buff=0.1).shift(UP*0.05)
        self.play(FadeIn(info5), FadeIn(info5_1), FadeIn(info5_2))
        
        sr1 = SurroundingRectangle(VGroup(info5, info5_1, info5_2), buff=0.2, color=BLUE, stroke_width=1)
        self.play(Create(sr1))
        
        # 显示轨迹说明（中文用Text，公式用MathTex）
        info6_text = Text("当α从0到2π时，b的轨迹", font="SimSun", font_size=30, color=BLUE).next_to(info5, DOWN*2).shift(RIGHT*0.8)
        info6 = VGroup(info6_text)  # 无公式部分可直接用Text
        self.play(FadeIn(info6))
        
        # 创建向量b
        b = Arrow(
            start=axes.c2p(0, 0), 
            end=axes.c2p(2, 1), 
            buff=0, 
            color=BLUE,
            tip_length=0.2,
            max_stroke_width_to_length_ratio=999,
            max_tip_length_to_length_ratio=0.2
        )
        self.play(Create(b))
        
        b_label = MathTex(r"b", font_size=30, color=BLUE).move_to(b.get_end() + 0.2)
        self.play(FadeIn(b_label))
        
        # 创建轨迹
        trace = TracedPath(b.get_end, stroke_width=2, stroke_color=BLUE)
        self.add(trace)
        
        # 标签随向量旋转
        b_label.add_updater(lambda m: m.move_to(b.get_end() + 0.2 * b.get_unit_vector()))
        
        # 向量旋转动画
        self.play(Rotate(b, TAU, about_point=axes.c2p(0, 0), run_time=5))
        
        # 显示特定角度信息（中文用Text，公式用MathTex）
        info7_text = Text("比如当α=120°时", font="SimSun", font_size=30, color=YELLOW).next_to(info6, DOWN*2, aligned_edge=LEFT)
        info7 = VGroup(info7_text)
        self.play(FadeIn(info7))
        
        self.play(Rotate(b, 2*PI/3, about_point=axes.c2p(0, 0), run_time=2))
        
        # 创建角度圆弧
        arc = Arc(
            arc_center=axes.c2p(0, 0),
            radius=0.8,
            start_angle=26.57/180*PI,
            angle=2*PI/3,
            color=YELLOW
        )
        self.bring_to_back(arc)
        self.play(Create(arc))
        
        arc_label = MathTex(r"\alpha=120^\circ", font_size=30, color=YELLOW).move_to(axes.c2p(0, 1.2))
        self.play(FadeIn(arc_label))
        self.wait(1)
        
        # 显示问题（中文用Text）
        info8 = Text("旋转矩阵A是如何来的呢？", font="SimSun", font_size=30).to_edge(UP)
        self.play(Write(info8))
        self.wait(2)
        
        # 淡出当前场景元素
        self.play(FadeOut(VGroup(
            axes, info3, info4, info5, info5_1, info5_2, 
            info6, info7, sr1, arc, arc_label, x, x_label, 
            b, b_label, trace, zerolabel
        )))
        
        # 第二部分：旋转矩阵推导
        
        # 创建新坐标系
        axes2 = Axes(
            x_range=[-2, 2], 
            y_range=[0, 1],
            axis_config={"color": GREY, "include_numbers": True, "stroke_width": 2}
        ).shift(UP*1.5)
        
        zerolabel2 = Text("0", font="SimSun", font_size=26).move_to(axes2.c2p(-0.1, -0.2))
        self.play(FadeIn(axes2), FadeIn(zerolabel2))
        
        # 旋转θ角度的动画
        dot1 = Dot(axes2.c2p(1, 0), color=YELLOW)
        self.play(FadeIn(dot1))
        self.wait(1)
        
        dot1_arrow = Arrow(
            start=axes2.c2p(0, 0),
            end=axes2.c2p(1, 0),
            buff=0,
            color=YELLOW,
            tip_length=0.2,
            max_stroke_width_to_length_ratio=999,
            max_tip_length_to_length_ratio=0.2
        )
        
        trace1 = TracedPath(dot1_arrow.get_end, stroke_width=2, stroke_color=YELLOW)
        self.add(trace1)
        
        self.play(Rotate(dot1_arrow, PI/6, about_point=axes2.c2p(0, 0), run_time=2))
        
        # 创建角度圆弧
        arc2 = Arc(
            arc_center=axes2.c2p(0, 0),
            radius=0.4,
            start_angle=0,
            angle=PI/6,
            color=YELLOW
        )
        self.bring_to_back(arc2)
        self.play(Create(arc2))
        
        arc2_label = MathTex(r"\theta", font_size=30, color=YELLOW).move_to(axes2.c2p(0.3, 0.06))
        self.play(FadeIn(arc2_label))
        self.wait(1)
        
        # 显示坐标信息（公式用MathTex）
        coord1 = MathTex(
            r"\begin{pmatrix} \cos\theta \\ \sin\theta \end{pmatrix}",
            font_size=30, 
            color=YELLOW
        ).move_to(axes2.c2p(1.2, 0.6))
        self.play(FadeIn(coord1))
        self.wait(1)
        
        # 显示矩阵作用信息（公式用MathTex）
        tip1 = MathTex(
            r"A\begin{pmatrix} 1 \\ 0 \end{pmatrix}=\begin{pmatrix} \cos\theta \\ \sin\theta \end{pmatrix}",
            font_size=30, 
            color=YELLOW
        ).move_to(axes2.c2p(1, -0.5))
        self.play(FadeIn(tip1))
        self.wait(1)
        
        # 再旋转90度
        dot2_arrow = Arrow(
            start=axes2.c2p(0, 0),
            end=axes2.c2p(np.cos(PI/6), np.sin(PI/6)),
            buff=0,
            color=BLUE,
            tip_length=0.2,
            max_stroke_width_to_length_ratio=999,
            max_tip_length_to_length_ratio=0.2
        )
        
        trace2 = TracedPath(dot2_arrow.get_end, stroke_width=2, stroke_color=BLUE)
        self.add(trace2)
        
        self.play(Rotate(dot2_arrow, PI/2, about_point=axes2.c2p(0, 0), run_time=2))
        
        # 创建直角符号
        rect = Polygon(
            axes2.c2p(0, 0), 
            axes2.c2p(0, 0.1), 
            axes2.c2p(0.1, 0.1), 
            axes2.c2p(0.1, 0), 
            color=GREY
        ).rotate(PI/6, about_point=axes2.c2p(0, 0))
        self.bring_to_back(rect)
        self.play(FadeIn(rect))
        self.wait(1)
        
        # 显示旋转后的坐标信息（公式用MathTex）
        tip2 = MathTex(
            r"\begin{pmatrix} \cos(\frac{\pi}{2}+\theta) \\ \sin(\frac{\pi}{2}+\theta) \end{pmatrix}=\begin{pmatrix} -\sin\theta \\ \cos\theta \end{pmatrix}",
            font_size=30, 
            color=BLUE
        ).move_to(axes2.c2p(-1.45, 0.9))
        self.play(FadeIn(tip2))
        self.wait(1)
        
        # 创建另一个点
        dot2 = Dot(axes2.c2p(0, 1), color=RED)
        self.play(FadeIn(dot2))
        self.wait(1)
        
        # 创建角度圆弧
        arc3 = Arc(
            arc_center=axes2.c2p(0, 0),
            radius=0.4,
            start_angle=PI/2,
            angle=PI/6,
            color=RED
        )
        self.bring_to_back(arc3)
        self.play(Create(arc3))
        
        arc3_label = MathTex(r"\theta", font_size=30, color=RED).move_to(axes2.c2p(-0.05, 0.3))
        self.play(FadeIn(arc3_label))
        self.wait(1)
        
        # 显示矩阵作用信息（公式用MathTex）
        tip3 = MathTex(
            r"A\begin{pmatrix} 0 \\ 1 \end{pmatrix}=\begin{pmatrix} -\sin\theta \\ \cos\theta \end{pmatrix}",
            font_size=30, 
            color=RED
        ).move_to(axes2.c2p(-1, -0.5))
        self.play(FadeIn(tip3))
        self.wait(1)
        
        # 综合推导结果（公式用MathTex）
        tip4 = MathTex(
            r"A\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}=\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}",
            font_size=30, 
            color=GREEN
        ).move_to(axes2.c2p(0, -1.2))
        self.play(FadeIn(tip4))
        self.wait(1)
        
        tip5 = MathTex(
            r"A=\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}",
            font_size=30, 
            color=GREEN
        ).move_to(axes2.c2p(0, -1.8))
        self.play(TransformFromCopy(tip4, tip5))
        self.wait(1)
        
        # 高亮最终结果
        sr = SurroundingRectangle(tip5, color=GREEN, buff=0.2, stroke_width=1)
        self.play(Create(sr))
        self.wait(3)