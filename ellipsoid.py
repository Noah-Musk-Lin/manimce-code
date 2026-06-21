from manim import *

# Define neon colors
NEON_BLUE = "#00FFFF"
NEON_GREEN = "#39FF14"
NEON_PINK = "#FF10F0"
NEON_YELLOW = "#FFFF00"

class Ellipsoid(ThreeDScene):
    def construct(self):
        #Display title
        title = MathTex("\\mathbb{A}\\text{pplications of the }\\mathbb{J}\\text{acobian }\\mathbb{D}\\text{eterminant}")
        title.scale(1.2).set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(title))
        self.wait(3)
        self.play(FadeOut(title))

        # First example: Ellipse Area Polar Coordinates
        ex1 = MathTex("\\mathbb{E}\\text{llipse }\\mathbb{A}\\text{rea}").shift(UP*3)
        ex1.set_color_by_gradient(RED, MAROON, PINK)
        self.play(Write(ex1))
        self.wait(1)
        axes = Axes(x_range=[-4, 4, 1], y_range=[-2, 2, 1], x_length=8, y_length=4)
        axes.add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")  # Label axes
        self.play(FadeIn(axes), FadeIn(axes_labels), run_time = 2)
        self.wait(1)
        # Create an ellipse
        ellipse = Ellipse(width=4, height=2, color=MAROON)

        # Add the ellipse to the scene
        self.play(Create(ellipse))
        self.wait(2)

        # Highlight a and b
        # Create lines to represent the radii
        major_axis = Line(ORIGIN, ellipse.get_right(), color=TEAL)  # Major axis (width)
        minor_axis = Line(ellipse.get_top(), ORIGIN, color=BLUE)  # Minor axis (height)
        a = MathTex("a").set_color(TEAL).next_to(major_axis, UP)
        b = MathTex("b").set_color(BLUE).next_to(minor_axis, LEFT)
        self.play(Create(major_axis), Create(minor_axis), Write(a), Write(b))
        self.wait(1)

        # Display equation of ellipse
        equ = MathTex("\\frac{x^2}{a^2}+\\frac{y^2}{b^2}=1").shift(LEFT*3, UP*2)
        equ.set_color(RED)
        self.play(Write(equ), run_time = 1.5)
        self.wait(2)

        # Highlight the interior of the ellipse
        self.play(ellipse.animate.set_fill(MAROON, opacity=0.5)) # Set fill color and opacity
        self.wait(1)

        area = MathTex(
            r"&\text{What is the area}\\",
            r"&\text{of an ellipse?}"
        ).shift(LEFT*3, DOWN*2)
        area.set_color(PINK)
        self.play(Write(area))
        self.wait(3)
        self.play(
            FadeOut(equ),
            FadeOut(area),
            FadeOut(axes),
            FadeOut(ellipse),
            FadeOut(major_axis),
            FadeOut(minor_axis),
            FadeOut(a),
            FadeOut(b),
            FadeOut(axes_labels)
        )

        # Integrals
        car_int = MathTex("\\text{Area}=\\int\\int_{\\frac{x^2}{a^2}+\\frac{y^2}{b^2}\\leq 1}dxdy").set_color(MAROON)
        car_int.shift(UP*0.5)
        self.play(Write(car_int))
        self.wait(2)
        txt = MathTex("\\text{But there's an easier method!}").set_color(TEAL)
        txt.shift(DOWN*1.5)
        self.play(Write(txt))
        self.wait(3)
        self.play(FadeOut(car_int), FadeOut(txt))
        let = MathTex("\\text{Let}").shift(LEFT*2.25+UP*2).scale(0.7)
        ch_var = MathTex(
            r"&x=ar\cos\theta\\",
            r"&y=br\sin\theta"
        ).shift(UP*1.5).scale(0.7)
        rn = MathTex("\\text{where }0\\leq r \\leq 1\\text{ and }0\\leq \\theta\\leq 2\\pi.").next_to(ch_var, DOWN)
        rn.scale(0.7)
        tn = MathTex("\\mathbb{J}=").shift(LEFT*3, DOWN*1.5).set_color(TEAL).scale(0.7)
        J = Matrix(
            [["\\frac{\\partial x}{\\partial r}", "\\frac{\\partial x}{\\partial \\theta}"],
             ["\\frac{\\partial y}{\\partial r}", "\\frac{\\partial y}{\\partial \\theta}"]
            ],
            v_buff = 1.5
        ).move_to(DOWN*1).scale(0.7)
        tn.next_to(J, LEFT)
        Jc = Matrix(
            [["a\\cos\\theta", "-ar\\sin\\theta"],
             ["b\\sin\\theta", "br\\cos\\theta"]
             ],
            h_buff=2.2
        ).move_to(DOWN * 1).scale(0.7)
        detJc = MathTex("\\det(\\mathbb{J})=abr\\cos^2\\theta + abr\\sin^2\\theta=abr").shift(DOWN*2.2)
        detJc.set_color_by_gradient(GREEN, YELLOW)
        detJc.scale(0.7)
        self.play(Write(let))
        self.play(Write(ch_var[0]))
        self.play(Write(ch_var[1]))
        self.play(Write(rn))
        self.wait(2)
        self.play(Write(tn), Write(J))
        self.wait(2)
        self.play(Transform(J, Jc), tn.animate.next_to(Jc, LEFT))
        self.wait(2)
        self.play(Write(detJc))
        self.wait(3)
        self.play(FadeOut(let), FadeOut(ch_var), FadeOut(rn), FadeOut(J), FadeOut(tn))
        rounded_rect = SurroundingRectangle(
            detJc,
            corner_radius=0.25,  # Adjust the roundness of the corners
            color=TEAL,  # Border color
            buff=0.25  # Padding around the text
        )
        rounded_rect.set_fill(color=TEAL, opacity=0.2)  # Semi-transparent RED fill
        self.play(Create(rounded_rect))
        self.wait(1)
        self.play(rounded_rect.animate.shift(UP*3.8), detJc.animate.shift(UP*3.8), run_time = 2)
        self.wait(2)
        pol_int = MathTex(
            r"\text{Area}&=\int\int_{\frac{x^2}{a^2}+\frac{y^2}{b^2}\leq 1}dxdy\\",
            r"&=\int_{0}^{2\pi}\int_{0}^{1}abr\ drd\theta\\",
            r"&=ab\int_{0}^{2\pi}\left[\frac{1}{2}r^2\right]_{0}^{1}d\theta\\",
            r"&=\pi ab"
        ).shift(DOWN*1)
        pol_int.scale(0.7)
        self.play(Write(pol_int[0]))
        self.wait(1)
        self.play(Write(pol_int[1]))
        self.wait(1)
        self.play(Write(pol_int[2]))
        self.wait(1)
        self.play(Write(pol_int[3]))
        self.wait(4)

        pi_ab = MathTex("\\text{Area}=\\pi ab")
        box = SurroundingRectangle(
            pi_ab,
            corner_radius=0.25,  # Adjust the roundness of the corners
            color=YELLOW,  # Border color
            buff=0.25  # Padding around the text
        )
        box.set_fill(color=YELLOW, opacity=0.3)  # Semi-transparent RED fill
        self.play(FadeOut(pol_int), FadeOut(detJc), FadeOut(rounded_rect))
        self.play(Create(box), Write(pi_ab))

        #clear screen for next example
        self.wait(3)
        self.play(FadeOut(*self.mobjects))

        # Second example: Ellipsoid Volume Spherical Coordinates

        # Set up the camera orientation
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        ex2 = MathTex("\\mathbb{E}\\text{llipsoid }\\mathbb{V}\\text{olume}")
        ex2.add_updater(lambda m: m.move_to(3 * OUT + UP*3))
        ex2.set_color_by_gradient(RED, MAROON, PINK)
        self.add_fixed_in_frame_mobjects(ex2)  # Ensure text is rendered in 2D
        self.play(Write(ex2))
        self.wait(1)
        
        # Create 3D axes
        axes_3d = ThreeDAxes(
            x_range=[-5, 5, 1],  # x-axis from -5 to 5 with step 1
            y_range=[-5, 5, 1],  # y-axis from -5 to 5 with step 1
            z_range=[-2.5, 2.5, 1],  # z-axis from -5 to 5 with step 1
            x_length=10,
            y_length=10,
            z_length=5,
            axis_config={"color": WHITE},
        )
        self.play(Create(axes_3d))
        self.wait(1)

        # Define the ellipsoid using the Surface class
        ellipsoid = Surface(
            lambda u, v: np.array([
                2.0 * np.cos(u) * np.cos(v),  # x-coordinate
                3.0 * np.cos(u) * np.sin(v),  # y-coordinate
                1.5 * np.sin(u)               # z-coordinate
            ]),
            u_range=[-PI/2, PI/2],  # u range for the ellipsoid
            v_range=[0, TAU],       # v range for the ellipsoid
            resolution=(20, 20),    # Resolution of the surface
            color=MAROON            # Color of the ellipsoid
        )
        ellipsoid.set_fill(MAROON, opacity=0.4)

        # Add the ellipsoid to the scene
        self.play(Create(ellipsoid))
        self.wait(2)

        # Highlight a, b, c
        # Create 3D vectors
        v1_3d = Vector([2, 0, 0], color=NEON_BLUE)
        v2_3d = Vector([0, 3, 0], color=NEON_GREEN)
        v3_3d = Vector([0, 0, 1.5], color=NEON_YELLOW)
        b3 = MathTex("b").set_color(NEON_GREEN)
        b3.add_updater(lambda m: m.move_to(3 * OUT + RIGHT*1.2 + UP*0.15))
        a3 = MathTex("a").set_color(NEON_BLUE)
        a3.add_updater(lambda m: m.move_to(3 * OUT + LEFT*0.5))
        c3 = MathTex("c").set_color(NEON_YELLOW)
        c3.add_updater(lambda m: m.move_to(3 * OUT + UP * 0.8 + LEFT * 0.3))

        self.add_fixed_in_frame_mobjects(a3, b3, c3)
        self.play(Create(v1_3d), Create(v2_3d), Create(v3_3d), Write(a3), Write(b3), Write(c3))
        self.wait(1)

        # Display equation of ellipsoid
        equ2 = MathTex("\\frac{x^2}{a^2}+\\frac{y^2}{b^2}+\\frac{z^2}{c^2}=1").set_color(RED)
        equ2.add_updater(lambda m: m.move_to(3 * OUT + UP*2 + LEFT*4))
        self.add_fixed_in_frame_mobjects(equ2)  # Ensure text is rendered in 2D
        self.play(Write(equ2))
        self.wait(2)

        # Highlight interior of ellipsoid
        self.play(ellipsoid.animate.set_fill(MAROON, opacity=0.7))

        vol = MathTex(
            r"&\text{What is the volume}\\",
            r"&\text{of an ellipsoid?}"
        ).shift(LEFT*3, DOWN*2)
        vol.add_updater(lambda m: m.move_to(3 * OUT + UP*2 + RIGHT*3.5))
        vol.set_color(PINK)
        self.add_fixed_in_frame_mobjects(vol)
        self.play(Write(vol))
        self.wait(3)
        self.play(
            FadeOut(equ2),
            FadeOut(vol),
            FadeOut(axes_3d),
            FadeOut(ellipsoid),
            FadeOut(v1_3d),
            FadeOut(v2_3d),
            FadeOut(v3_3d),
            FadeOut(a3),
            FadeOut(b3),
            FadeOut(c3)
        )

        # Reset camera
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)

        # Integral
        car_int = MathTex(
            "\\text{Volume}=\\int\\int\\int_{\\frac{x^2}{a^2}+\\frac{y^2}{b^2}+\\frac{z^2}{c^2}\\leq 1}dxdydz"
        ).set_color(MAROON)
        car_int.shift(UP*0.5)
        self.play(Write(car_int))
        self.wait(2)
        txt = MathTex("\\text{But there's an easier method!}").set_color(TEAL)
        txt.shift(DOWN*1.5)
        self.play(Write(txt))
        self.wait(3)
        self.play(FadeOut(car_int), FadeOut(txt))
        let = MathTex("\\text{Let}").shift(LEFT*2.8+UP*2.4).scale(0.6)
        ch_var = MathTex(
            r"&x=ar\sin\theta\cos\varphi\\",
            r"&y=br\sin\theta\sin\varphi\\",
            r"&z=cr\cos\theta"
        ).shift(UP*1.65).scale(0.6)
        rn = MathTex(
            "\\text{where }0\\leq r \\leq 1\\text{, }0\\leq \\theta\\leq \\pi\\text{, and }0\\leq \\varphi \\leq 2\\pi."
        ).next_to(ch_var, DOWN)
        rn.scale(0.6)
        tn = MathTex("\\mathbb{J}=").shift(LEFT*3, DOWN*1.5).set_color(TEAL).scale(0.6)
        J = Matrix(
            [["\\frac{\\partial x}{\\partial r}",
              "\\frac{\\partial x}{\\partial \\theta}",
              "\\frac{\\partial x}{\\partial \\varphi}"],
             ["\\frac{\\partial y}{\\partial r}",
              "\\frac{\\partial y}{\\partial \\theta}",
              "\\frac{\\partial y}{\\partial \\varphi}"],
             ["\\frac{\\partial z}{\\partial r}",
              "\\frac{\\partial z}{\\partial \\theta}",
              "\\frac{\\partial z}{\\partial \\varphi}"]
            ],
            v_buff = 1.5
        ).move_to(DOWN*1.2).scale(0.6)
        tn.next_to(J, LEFT)
        Jc = Matrix(
            [["a\\sin\\theta\\cos\\varphi",
              "ar\\cos\\theta\\cos\\varphi",
              "-ar\\sin\\theta\\sin\\varphi"],
             ["b\\sin\\theta\\sin\\varphi",
              "br\\cos\\theta\\sin\\varphi",
              "br\\sin\\theta\\cos\\varphi"],
             ["c\\cos\\theta",
              "-cr\\sin\\theta",
              "0"]
            ],
            h_buff=3.2
        ).move_to(DOWN * 1.2).scale(0.6)
        detJc = MathTex("\\det(\\mathbb{J})=abcr^2\\sin\\theta").shift(DOWN*2.4)
        detJc.set_color_by_gradient(GREEN, YELLOW)
        detJc.scale(0.6)
        self.play(Write(let))
        self.play(Write(ch_var[0]))
        self.play(Write(ch_var[1]))
        self.play(Write(ch_var[2]))
        self.play(Write(rn))
        self.wait(2)
        self.play(Write(tn), Write(J))
        self.wait(2)
        self.play(Transform(J, Jc), tn.animate.next_to(Jc, LEFT))
        self.wait(2)
        self.play(Write(detJc))
        self.wait(3)
        self.play(FadeOut(let), FadeOut(ch_var), FadeOut(rn), FadeOut(J), FadeOut(tn))
        rounded_rect = SurroundingRectangle(
            detJc,
            corner_radius=0.25,  # Adjust the roundness of the corners
            color=TEAL,  # Border color
            buff=0.25  # Padding around the text
        )
        rounded_rect.set_fill(color=TEAL, opacity=0.2)  # Semi-transparent RED fill
        self.play(Create(rounded_rect))
        self.wait(1)
        self.play(rounded_rect.animate.shift(UP*4.3), detJc.animate.shift(UP*4.3), run_time = 2)
        self.wait(2)
        sph_int = MathTex(
            r"\text{Volume}&=\int\int\int_{\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}\leq 1}dxdydz\\",
            r"&=\int_{0}^{2\pi}\int_{0}^{\pi}\int_{0}^{1}abcr^2\sin\theta\ drd\theta d\varphi\\",
            r"&=abc\int_{0}^{2\pi}\int_{0}^{\pi}\sin\theta\left[\frac{1}{3}r^3\right]_{0}^{1}\ d\theta d\varphi\\",
            r"&=\frac{abc}{3}\int_{0}^{2\pi}\left[-\cos\theta\right]_{0}^{\pi}d\varphi\\",
            r"&=\frac{4}{3}\pi abc"
        ).shift(DOWN*1)
        sph_int.scale(0.6)
        self.play(Write(sph_int[0]))
        self.wait(1)
        self.play(Write(sph_int[1]))
        self.wait(1)
        self.play(Write(sph_int[2]))
        self.wait(1)
        self.play(Write(sph_int[3]))
        self.wait(1)
        self.play(Write(sph_int[4]))
        self.wait(4)

        pi_ab = MathTex("\\text{Volume}=\\frac{4}{3}\\pi abc")
        box = SurroundingRectangle(
            pi_ab,
            corner_radius=0.25,  # Adjust the roundness of the corners
            color=YELLOW,  # Border color
            buff=0.25  # Padding around the text
        )
        box.set_fill(color=YELLOW, opacity=0.3)  # Semi-transparent RED fill
        self.play(FadeOut(sph_int), FadeOut(detJc), FadeOut(rounded_rect))
        self.play(Create(box), Write(pi_ab))

        # Clear screen
        self.wait(5)
        self.play(FadeOut(*self.mobjects))