from manim import *

class RightTriangleWithMidsegment(Scene):
    def construct(self):
        # 标题
        title = Text("直角三角形与中位线", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 创建大直角三角形
        # 顶点坐标
        A = LEFT * 3 + DOWN * 2
        B = RIGHT * 4 + DOWN * 2  
        C = LEFT * 3 + UP * 3
        
        # 绘制三角形
        triangle = Polygon(A, B, C, color=BLUE, stroke_width=4)
        
        # 标记直角
        right_angle = RightAngle(
            Line(A, C), Line(A, B), 
            length=0.4, color=YELLOW, stroke_width=4
        )
        
        # 顶点标签
        label_A = Text("A", font_size=24).next_to(A, DL * 0.5)
        label_B = Text("B", font_size=24).next_to(B, DR * 0.5)
        label_C = Text("C", font_size=24).next_to(C, UL * 0.5)
        
        # 显示三角形
        self.play(Create(triangle), run_time=2)
        self.play(Create(right_angle))
        self.play(Write(label_A), Write(label_B), Write(label_C))
        self.wait(1)
        
        # 找到中点
        mid_AB = (A + B) / 2
        mid_AC = (A + C) / 2
        
        # 绘制中点
        dot_AB = Dot(mid_AB, color=RED, radius=0.06)
        dot_AC = Dot(mid_AC, color=RED, radius=0.06)
        
        # 中点标签
        label_D = Text("D", font_size=20).next_to(mid_AB, DOWN * 0.3)
        label_E = Text("E", font_size=20).next_to(mid_AC, LEFT * 0.3)
        
        # 显示中点
        self.play(
            Create(dot_AB),
            Create(dot_AC),
            Write(label_D),
            Write(label_E)
        )
        self.wait(1)
        
        # 绘制中位线
        midsegment = Line(mid_AB, mid_AC, color=GREEN, stroke_width=4)
        
        # 中位线标签
        midsegment_label = Text("中位线 DE", font_size=20, color=GREEN)
        midsegment_label.next_to(midsegment, RIGHT * 0.5)
        
        # 显示中位线
        self.play(Create(midsegment), run_time=1.5)
        self.play(Write(midsegment_label))
        self.wait(1)
        
        # 添加中位线性质说明
        properties = VGroup(
            Text("中位线性质:", font_size=28, color=YELLOW),
            Text("1. DE ∥ BC", font_size=24),
            Text("2. DE = ½ BC", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT)
        properties.to_edge(RIGHT).shift(UP)
        
        self.play(Write(properties))
        self.wait(2)
        
        # 高亮显示平行关系
        line_BC = Line(B, C, color=ORANGE, stroke_width=3)
        parallel_arrow1 = Arrow(
            midsegment.get_center() + UP * 0.3 + LEFT * 0.3,
            midsegment.get_center() + UP * 0.3 + RIGHT * 0.3,
            color=ORANGE, stroke_width=3
        )
        parallel_arrow2 = Arrow(
            line_BC.get_center() + DOWN * 0.3 + LEFT * 0.3,
            line_BC.get_center() + DOWN * 0.3 + RIGHT * 0.3,
            color=ORANGE, stroke_width=3
        )
        
        self.play(
            Create(line_BC),
            Create(parallel_arrow1),
            Create(parallel_arrow2)
        )
        self.wait(2)
        
        # 最终展示
        self.play(
            triangle.animate.set_stroke(opacity=0.7),
            midsegment.animate.set_stroke(opacity=1),
            FadeOut(parallel_arrow1),
            FadeOut(parallel_arrow2),
            line_BC.animate.set_stroke(opacity=0.5)
        )
        self.wait(2)

class AnimatedMidsegment(Scene):
    def construct(self):
        # 更生动的版本，展示中位线的构造过程
        
        # 创建直角三角形
        A = LEFT * 4 + DOWN * 2
        B = RIGHT * 5 + DOWN * 2  
        C = LEFT * 4 + UP * 4
        
        triangle = Polygon(A, B, C, color=BLUE, stroke_width=5)
        
        # 顶点标签
        labels = VGroup(
            Text("A", font_size=28).next_to(A, DL * 0.5),
            Text("B", font_size=28).next_to(B, DR * 0.5),
            Text("C", font_size=28).next_to(C, UL * 0.5)
        )
        
        self.play(Create(triangle), Write(labels), run_time=2)
        self.wait(1)
        
        # 动画显示找中点过程
        mid_AB = (A + B) / 2
        mid_AC = (A + C) / 2
        
        # 从A到B的移动点
        moving_dot_AB = Dot(A, color=RED)
        trace_line_AB = DashedLine(A, B, color=RED, stroke_width=2)
        
        # 从A到C的移动点
        moving_dot_AC = Dot(A, color=RED)
        trace_line_AC = DashedLine(A, C, color=RED, stroke_width=2)
        
        self.play(Create(trace_line_AB), Create(trace_line_AC))
        
        # 动画：点移动到中点位置
        self.play(
            moving_dot_AB.animate.move_to(mid_AB),
            moving_dot_AC.animate.move_to(mid_AC),
            run_time=2
        )
        
        # 固定中点
        dot_D = Dot(mid_AB, color=RED, radius=0.07)
        dot_E = Dot(mid_AC, color=RED, radius=0.07)
        label_D = Text("D", font_size=24).next_to(mid_AB, DOWN * 0.3)
        label_E = Text("E", font_size=24).next_to(mid_AC, LEFT * 0.3)
        
        self.play(
            ReplacementTransform(moving_dot_AB, dot_D),
            ReplacementTransform(moving_dot_AC, dot_E),
            Write(label_D),
            Write(label_E),
            FadeOut(trace_line_AB),
            FadeOut(trace_line_AC)
        )
        self.wait(1)
        
        # 动画绘制中位线
        midsegment = Line(mid_AB, mid_AC, color=GREEN, stroke_width=6)
        
        self.play(Create(midsegment), run_time=1.5)
        
        # 中位线标签
        midsegment_label = Text("中位线 DE", font_size=24, color=GREEN)
        midsegment_label.next_to(midsegment.get_center(), RIGHT)
        
        self.play(Write(midsegment_label))
        self.wait(2)
        
        # 强调中位线性质
        explanation = Text(
            "DE 平行于 BC 且等于 BC 的一半",
            font_size=30,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(explanation))
        self.wait(3)