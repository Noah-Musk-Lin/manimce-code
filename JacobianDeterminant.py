from manim import *
import numpy as np


class JacobianDeterminant(Scene):
    def construct(self):
        self.setup_colors()
        self.introduction()
        self.jacobian_definition()
        self.geometric_meaning()
        self.grid_transformation()
        self.example_polar_coordinates()
        self.conclusion()

    def setup_colors(self):
        self.colors = {
            'title': RED,
            'highlight': YELLOW,
            'grid': BLUE,
            'transformed': GREEN,
            'derivative': PINK,
            'text': WHITE
        }

    def introduction(self):
        title = Title(
            r"Jacobi Determinant Visualization",
            font_size=48,
            color=self.colors['title']
        )
        self.play(Write(title))
        self.wait(1.5)

        subtitle = Tex(
            r"Geometric Meaning of the Jacobian",
            font_size=36,
            color=BLUE
        )
        subtitle.next_to(title, DOWN, buff=0.5)
        self.play(Write(subtitle))
        self.wait(2)

        self.play(FadeOut(VGroup(title, subtitle)))
        self.wait(0.5)

    def jacobian_definition(self):
        title = Title(r"Jacobi Matrix", font_size=44, color=self.colors['title'])
        self.play(Write(title))
        self.wait(1)

        intro_text = Tex(
            r"Consider a differentiable map from $\mathbb{R}^n$ to $\mathbb{R}^n$:",
            font_size=32
        )
        intro_text.next_to(title, DOWN, buff=1)
        self.play(Write(intro_text))
        self.wait(2)

        transform_text = MathTex(
            r"\mathbf{f}: \mathbb{R}^n \to \mathbb{R}^n, \quad "
            r"(x_1, x_2, \dots, x_n) \mapsto (y_1, y_2, \dots, y_n)",
            font_size=36
        )
        transform_text.next_to(intro_text, DOWN, buff=0.8)
        self.play(Write(transform_text))
        self.wait(2)

        jacobian_def = MathTex(
            r"J = \frac{\partial(y_1, y_2, \dots, y_n)}{\partial(x_1, x_2, \dots, x_n)} "
            r"= \begin{pmatrix}"
            r"\frac{\partial y_1}{\partial x_1} & \cdots & \frac{\partial y_1}{\partial x_n} \\"
            r"\vdots & \ddots & \vdots \\"
            r"\frac{\partial y_n}{\partial x_1} & \cdots & \frac{\partial y_n}{\partial x_n}"
            r"\end{pmatrix}",
            font_size=32
        )
        jacobian_def.next_to(transform_text, DOWN, buff=1)
        self.play(Write(jacobian_def))
        self.wait(3)

        det_text = Tex(
            r"Jacobi Determinant = determinant of the above matrix",
            font_size=32,
            color=YELLOW
        )
        det_text.next_to(jacobian_def, DOWN, buff=1)
        self.play(Write(det_text))
        self.wait(3)

        self.play(FadeOut(VGroup(title, intro_text, transform_text, jacobian_def, det_text)))
        self.wait(0.5)

    def geometric_meaning(self):
        title = Title(r"Geometric Meaning", font_size=44, color=self.colors['title'])
        self.play(Write(title))
        self.wait(1)

        meaning = MathTex(
            r"\text{det}(J) = \frac{\text{area after transform}}{\text{area before transform}}",
            font_size=40
        )
        meaning.move_to(ORIGIN)
        self.play(Write(meaning))
        self.wait(2)

        explanation = Tex(
            r"The Jacobian determinant represents the area scaling factor",
            font_size=32,
            color=BLUE
        )
        explanation.next_to(meaning, DOWN, buff=1)
        self.play(Write(explanation))
        self.wait(2)

        note = MathTex(
            r"\text{det}(J) > 0: \text{orientation preserved} \quad "
            r"\text{det}(J) < 0: \text{orientation reversed}",
            font_size=28
        )
        note.next_to(explanation, DOWN, buff=0.8)
        self.play(Write(note))
        self.wait(3)

        self.play(FadeOut(VGroup(title, meaning, explanation, note)))
        self.wait(0.5)

    def grid_transformation(self):
        title = Title(r"2D Coordinate Transformation", font_size=44, color=self.colors['title'])
        self.play(Write(title))
        self.wait(1)

        self.transform_intro_2d()
        self.wait(1)
        self.play(FadeOut(title))

    def transform_intro_2d(self):
        transform_eq = MathTex(
            r"\begin{cases}"
            r"u = x - y \\"
            r"v = x + y"
            r"\end{cases}",
            font_size=40
        )
        transform_eq.to_corner(UR).shift(LEFT * 2)
        self.play(Write(transform_eq))
        self.wait(1)

        jacobian_calc = MathTex(
            r"J = \begin{vmatrix}"
            r"\frac{\partial u}{\partial x} & \frac{\partial u}{\partial y} \\"
            r"\frac{\partial v}{\partial x} & \frac{\partial v}{\partial y}"
            r"\end{vmatrix}"
            r"= \begin{vmatrix} 1 & -1 \\ 1 & 1 \end{vmatrix} = 2",
            font_size=36
        )
        jacobian_calc.next_to(transform_eq, DOWN, buff=0.5)
        self.play(Write(jacobian_calc))
        self.wait(2)

        grid_label = Tex(r"Original Grid (x, y)", font_size=28, color=BLUE)
        grid_label.to_corner(UL)
        self.play(Write(grid_label))

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True}
        )
        axes.to_corner(DL).shift(RIGHT * 1.5, UP * 0.5)

        original_grid = VGroup()
        for i in range(-3, 4):
            h_line = Line(
                axes.c2p(-3, i),
                axes.c2p(3, i),
                color=BLUE,
                stroke_opacity=0.5
            )
            v_line = Line(
                axes.c2p(i, -3),
                axes.c2p(i, 3),
                color=BLUE,
                stroke_opacity=0.5
            )
            original_grid.add(h_line, v_line)

        self.play(Create(original_grid), run_time=2)
        self.wait(1)

        axes2 = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_tip": True}
        )
        axes2.to_corner(DR).shift(LEFT * 1.5, UP * 0.5)

        transformed_label = Tex(r"Transformed Grid (u, v)", font_size=28, color=GREEN)
        transformed_label.next_to(axes2, UP, buff=0.3)
        self.play(Write(transformed_label))

        def transform_point(x, y):
            return (x - y, x + y)

        transformed_grid = VGroup()
        for i in range(-3, 4):
            points_h = [axes.c2p(*transform_point(x, i)) for x in np.linspace(-3, 3, 50)]
            points_v = [axes.c2p(*transform_point(i, y)) for y in np.linspace(-3, 3, 50)]

            h_line = VMobject()
            h_line.set_points_smoothly([axes.c2p(*transform_point(x, i)) for x in np.linspace(-3, 3, 100)])
            h_line.set_color(GREEN)
            h_line.set_opacity(0.5)

            v_line = VMobject()
            v_line.set_points_smoothly([axes.c2p(*transform_point(i, y)) for y in np.linspace(-3, 3, 100)])
            v_line.set_color(GREEN)
            v_line.set_opacity(0.5)

            transformed_grid.add(h_line, v_line)

        self.play(Create(transformed_grid), run_time=2)
        self.wait(2)

        area_text = Tex(
            r"Area scaling factor = |det(J)| = 2",
            font_size=32,
            color=YELLOW
        )
        area_text.to_corner(UP).shift(DOWN * 3.5)
        self.play(Write(area_text))
        self.wait(3)

        self.play(FadeOut(VGroup(
            transform_eq, jacobian_calc, grid_label, axes, original_grid,
            axes2, transformed_label, transformed_grid, area_text
        )))
        self.wait(0.5)

    def example_polar_coordinates(self):
        title = Title(r"Polar Coordinates Example", font_size=44, color=self.colors['title'])
        self.play(Write(title))
        self.wait(1)

        transform = MathTex(
            r"\begin{cases}"
            r"x = r\cos\theta \\"
            r"y = r\sin\theta"
            r"\end{cases}",
            font_size=38
        )
        transform.to_corner(UR).shift(LEFT * 2)
        self.play(Write(transform))
        self.wait(1)

        jacobian = MathTex(
            r"J = \begin{vmatrix}"
            r"\frac{\partial x}{\partial r} & \frac{\partial x}{\partial \theta} \\"
            r"\frac{\partial y}{\partial r} & \frac{\partial y}{\partial \theta}"
            r"\end{vmatrix}"
            r"= \begin{vmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{vmatrix}",
            font_size=32
        )
        jacobian.next_to(transform, DOWN, buff=0.5)
        self.play(Write(jacobian))
        self.wait(1)

        det_result = MathTex(
            r"\text{det}(J) = r(\cos^2\theta + \sin^2\theta) = r",
            font_size=36,
            color=YELLOW
        )
        det_result.next_to(jacobian, DOWN, buff=0.8)
        self.play(Write(det_result))
        self.wait(2)

        area_meaning = Tex(
            r"In polar coordinates: $dA = r\,dr\,d\theta$",
            font_size=32,
            color=BLUE
        )
        area_meaning.next_to(det_result, DOWN, buff=1)
        self.play(Write(area_meaning))
        self.wait(2)

        self.play(FadeOut(VGroup(title, transform, jacobian, det_result, area_meaning)))
        self.wait(0.5)

        self.show_rectangle_transformation()
        self.wait(1)

    def show_rectangle_transformation(self):
        title = Tex(r"Rectangle Transformation in Polar Coordinates", font_size=36, color=BLUE)
        title.to_corner(UP)
        self.play(Write(title))

        r_range = MathTex(r"r \in [1, 2]", font_size=28)
        theta_range = MathTex(r"\theta \in [0, \frac{\pi}{2}]", font_size=28)
        ranges = VGroup(r_range, theta_range).arrange(RIGHT, buff=1).to_corner(UL).shift(DOWN * 0.5)
        self.play(Write(ranges))
        self.wait(1)

        cartesian_axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-0.5, 2.5, 0.5],
            x_length=4,
            y_length=4
        )
        cartesian_axes.to_corner(DL).shift(RIGHT * 2)

        x_label = MathTex("x", font_size=24)
        y_label = MathTex("y", font_size=24)
        x_label.next_to(cartesian_axes.x_axis, RIGHT, buff=0.1)
        y_label.next_to(cartesian_axes.y_axis, UP, buff=0.1)
        self.play(Write(cartesian_axes), Write(x_label), Write(y_label))

        original_rect = Polygon(
            cartesian_axes.c2p(1, 0),
            cartesian_axes.c2p(2, 0),
            cartesian_axes.c2p(2, 1),
            cartesian_axes.c2p(1, 1),
            color=BLUE,
            fill_opacity=0.3
        )
        self.play(Create(original_rect))
        self.wait(1)

        polar_axes = Axes(
            x_range=[-0.5, 2.5, 0.5],
            y_range=[-0.5, 2.5, 0.5],
            x_length=4,
            y_length=4
        )
        polar_axes.to_corner(DR).shift(LEFT * 2)

        polar_label = Tex("Polar", font_size=24)
        polar_label.next_to(polar_axes, UP, buff=0.3)
        self.play(Write(polar_axes), Write(polar_label))

        def polar_to_cartesian(r, theta):
            return r * np.cos(theta), r * np.sin(theta)

        curved_region = VMobject()
        points = []
        for r_val in np.linspace(1, 2, 20):
            for theta_val in np.linspace(0, np.pi/2, 30):
                x, y = polar_to_cartesian(r_val, theta_val)
                points.append(polar_axes.c2p(x, y))
        curved_region.set_points_smoothly(points)
        curved_region.set_color(GREEN)
        curved_region.set_fill(GREEN, 0.3)

        arc1 = Arc(radius=1, start_angle=0, angle=PI/2, color=GREEN)
        arc1.move_to(polar_axes.get_origin())

        arc2 = Arc(radius=2, start_angle=0, angle=PI/2, color=GREEN)
        arc2.move_to(polar_axes.get_origin())

        line1 = Line(
            polar_axes.c2p(0, 0),
            polar_axes.c2p(2, 0),
            color=GREEN
        )

        line2 = Line(
            polar_axes.c2p(0, 0),
            polar_axes.c2p(0, 2),
            color=GREEN
        )

        self.play(Create(arc1), Create(arc2), Create(line1), Create(line2), run_time=2)
        self.wait(1)

        area_comparison = MathTex(
            r"\text{Original area} = 1 \times \frac{\pi}{2} = \frac{\pi}{2}",
            font_size=28
        )
        area_comparison.to_corner(UR).shift(DOWN * 0.5)
        self.play(Write(area_comparison))
        self.wait(1)

        avg_jacobian = MathTex(
            r"\text{Average scaling} \approx \bar{r} = 1.5",
            font_size=28
        )
        avg_jacobian.next_to(area_comparison, DOWN, buff=0.5)
        self.play(Write(avg_jacobian))
        self.wait(2)

        self.play(FadeOut(VGroup(
            title, ranges, cartesian_axes, x_label, y_label, original_rect,
            polar_axes, polar_label, arc1, arc2, line1, line2,
            area_comparison, avg_jacobian
        )))
        self.wait(0.5)

    def conclusion(self):
        title = Title(r"Summary", font_size=44, color=self.colors['title'])
        self.play(Write(title))
        self.wait(1)

        points = [
            Tex(r"1. Jacobian = area scaling factor of the transformation", font_size=32),
            Tex(r"2. $\text{det}(J) = 0$ means the map is not invertible", font_size=32),
            Tex(r"3. Key role in multiple integral change of variables", font_size=32),
            Tex(r"4. In polar coordinates: $dA = r\,dr\,d\theta$", font_size=32)
        ]

        conclusion_group = VGroup(*points).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        conclusion_group.move_to(ORIGIN)

        for point in points:
            self.play(Write(point))
            self.wait(1)

        self.wait(2)

        final_message = Tex(
            r"Jacobi Determinant: Bridge between linear approximation and geometric transformation",
            font_size=36,
            color=YELLOW
        )
        final_message.next_to(conclusion_group, DOWN, buff=1.5)
        self.play(Write(final_message))
        self.wait(3)


class JacobianInteractive(Scene):
    def construct(self):
        self.show_interactive_transformation()

    def show_interactive_transformation(self):
        title = Title(r"Interactive Transformation Demo", font_size=44, color=BLUE)
        self.play(Write(title))
        self.wait(1)

        transform_eq = MathTex(
            r"\begin{cases}"
            r"u = ax \\"
            r"v = by"
            r"\end{cases}",
            font_size=40
        )
        transform_eq.to_corner(UR).shift(LEFT * 3)
        self.play(Write(transform_eq))
        self.wait(1)

        jacobian = MathTex(
            r"\text{det}(J) = ab",
            font_size=36,
            color=YELLOW
        )
        jacobian.next_to(transform_eq, DOWN, buff=0.5)
        self.play(Write(jacobian))
        self.wait(1)

        axes1 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        )
        axes1.to_corner(DL).shift(RIGHT * 1.5, UP * 0.5)

        unit_square = Polygon(
            axes1.c2p(0, 0),
            axes1.c2p(1, 0),
            axes1.c2p(1, 1),
            axes1.c2p(0, 1),
            color=BLUE,
            fill_opacity=0.5
        )

        self.play(Create(axes1), Create(unit_square))
        self.wait(1)

        axes2 = Axes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            x_length=4,
            y_length=4
        )
        axes2.to_corner(DR).shift(LEFT * 1.5, UP * 0.5)

        self.play(Write(axes2))

        a, b = 2, 1.5

        transformed_square = Polygon(
            axes2.c2p(0, 0),
            axes2.c2p(a, 0),
            axes2.c2p(a, b),
            axes2.c2p(0, b),
            color=GREEN,
            fill_opacity=0.5
        )

        area_text = MathTex(
            r"\text{Area ratio} = |ab| = " + f"{a*b:.1f}",
            font_size=32,
            color=YELLOW
        )
        area_text.next_to(jacobian, DOWN, buff=1)
        self.play(Write(area_text))
        self.wait(1)

        self.play(TransformFromCopy(unit_square, transformed_square))
        self.wait(2)

        flip_eq = MathTex(
            r"\begin{cases}"
            r"u = -x \\"
            r"v = y"
            r"\end{cases}",
            font_size=36
        )
        flip_eq.next_to(area_text, DOWN, buff=1)
        self.play(Write(flip_eq))
        self.wait(1)

        det_text = MathTex(
            r"\text{det}(J) = -1 \quad (\text{orientation reversed})",
            font_size=28,
            color=RED
        )
        det_text.next_to(flip_eq, DOWN, buff=0.5)
        self.play(Write(det_text))
        self.wait(3)