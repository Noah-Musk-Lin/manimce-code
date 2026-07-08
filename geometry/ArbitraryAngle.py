from manim import *

class ArbitraryAngle(Scene):
    def construct(self):
        title = Text("任意角的可视化", font_size=48).to_edge(UP)
        self.add(title)
        self.wait(0.5)

        center = ORIGIN
        radius = 2
        center_dot = Dot(center, color=RED)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            axis_config={"include_tip": True}
        ).add_coordinates()
        self.play(Create(axes))
        self.play(Write(title))
        self.play(FadeIn(center_dot))
        self.wait(0.5)

        angle_tracker = ValueTracker(0)
        
        positive_arc = Arc(start_angle=0, angle=PI/3, radius=radius, arc_center=center, color=YELLOW, stroke_width=4)
        positive_line = Line(center, center + radius * rotate_vector(RIGHT, PI/3), color=GREEN)
        positive_label = MathTex(r"60^\circ", font_size=36).move_to(center + 1.5 * rotate_vector(RIGHT, PI/6) + 0.3 * UP)
        
        self.play(Create(positive_arc), Create(positive_line), Write(positive_label))
        self.wait(0.5)
        
        positive_text = Text("正角：逆时针旋转", font_size=28).to_corner(UL)
        self.play(Write(positive_text))
        self.wait(1)
        self.play(FadeOut(positive_arc, positive_line, positive_label, positive_text))

        negative_arc = Arc(start_angle=0, angle=-2*PI/3, radius=radius, arc_center=center, color=ORANGE, stroke_width=4)
        negative_line = Line(center, center + radius * rotate_vector(RIGHT, -2*PI/3), color=PINK)
        negative_label = MathTex(r"-120^\circ", font_size=36).move_to(center + 1.5 * rotate_vector(RIGHT, -PI/3) + 0.3 * DOWN)
        
        self.play(Create(negative_arc), Create(negative_line), Write(negative_label))
        
        negative_text = Text("负角：顺时针旋转", font_size=28).to_corner(UL)
        self.play(Write(negative_text))
        self.wait(1)
        self.play(FadeOut(negative_arc, negative_line, negative_label, negative_text))

        base_arc = Arc(start_angle=0, angle=PI/3, radius=radius, arc_center=center, color=BLUE, stroke_width=3)
        base_line = Line(center, center + radius * rotate_vector(RIGHT, PI/3), color=GREEN)
        
        equivalent_arc1 = Arc(start_angle=0, angle=PI/3 + 2*PI, radius=radius, arc_center=center, color=BLUE, stroke_width=2, stroke_opacity=0.5)
        equivalent_line1 = Line(center, center + radius * rotate_vector(RIGHT, PI/3 + 2*PI), color=GREEN, stroke_opacity=0.5)
        
        equivalent_label = MathTex(r"60^\circ + 360^\circ = 420^\circ", font_size=32).to_corner(UL)
        
        self.play(Create(base_arc), Create(base_line))
        self.play(Write(equivalent_label))
        self.play(Create(equivalent_arc1), Create(equivalent_line1))
        
        same_text = Text("终边相同的角", font_size=28).to_corner(DL)
        self.play(Write(same_text))
        self.wait(1.5)
        self.play(FadeOut(base_arc, base_line, equivalent_arc1, equivalent_line1, equivalent_label, same_text))

        radians_title = Text("弧度制", font_size=36).to_edge(UP)
        self.play(Transform(title, radians_title))
        
        circle_arc = Circle(radius=radius, arc_center=center, color=GRAY, stroke_width=2)
        self.play(Create(circle_arc))
        
        rad_label = MathTex(r"1\text{ rad} = \frac{180^\circ}{\pi}", font_size=40).to_edge(DOWN)
        self.play(Write(rad_label))
        self.wait(1.5)
        
        self.play(FadeOut(circle_arc, rad_label))

        trig_title = Text("任意角的三角函数", font_size=36).to_edge(UP)
        self.play(Transform(title, trig_title))
        
        angle = ValueTracker(PI/6)
        
        radius_line = always_redraw(
            lambda: Line(ORIGIN, radius * rotate_vector(RIGHT, angle.get_value()), color=GREEN, stroke_width=3)
        )
        x_projection = always_redraw(
            lambda: DashedLine(
                radius * rotate_vector(RIGHT, angle.get_value()),
                radius * rotate_vector(RIGHT, angle.get_value())[0] * RIGHT,
                color=BLUE, stroke_width=2, stroke_opacity=0.6
            )
        )
        y_projection = always_redraw(
            lambda: DashedLine(
                radius * rotate_vector(RIGHT, angle.get_value()),
                radius * rotate_vector(RIGHT, angle.get_value())[1] * UP,
                color=RED, stroke_width=2, stroke_opacity=0.6
            )
        )
        
        x_brace = always_redraw(
            lambda: BraceBetweenPoints(
                ORIGIN,
                radius * rotate_vector(RIGHT, angle.get_value())[0] * RIGHT,
                direction=DOWN,
                color=BLUE
            )
        )
        y_brace = always_redraw(
            lambda: BraceBetweenPoints(
                ORIGIN,
                radius * rotate_vector(RIGHT, angle.get_value())[1] * UP,
                direction=RIGHT,
                color=RED
            )
        )
        
        cos_label = always_redraw(
            lambda: MathTex(r"\cos\theta", font_size=24, color=BLUE).next_to(x_brace, DOWN, buff=0.1)
        )
        sin_label = always_redraw(
            lambda: MathTex(r"\sin\theta", font_size=24, color=RED).next_to(y_brace, RIGHT, buff=0.1)
        )
        
        self.add(radius_line, x_projection, y_projection, x_brace, y_brace, cos_label, sin_label)
        self.play(angle.animate.set_value(PI/2), run_time=2)
        self.play(angle.animate.set_value(PI), run_time=2)
        self.play(angle.animate.set_value(3*PI/2), run_time=2)
        self.play(angle.animate.set_value(2*PI), run_time=2)
        
        self.wait(0.5)
        
        final_text = Text("任意角概念完毕", font_size=32, color=YELLOW).center()
        self.play(Write(final_text))
        self.wait(1)