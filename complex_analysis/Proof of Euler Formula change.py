from manim import *
import numpy as np

class EulerFormulaProof(Scene):
    def construct(self):
        # 全局配置：统一缓冲距离和动画时间
        DEFAULT_BUFF = 0.4
        DEFAULT_ANIM_TIME = 1.0

        # --------------------------
        # 1. 标题与核心公式展示
        # --------------------------
        title = Title("Proof of Euler's Formula by Taylor Series", font_size=44)
        euler_formula = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=48)
        
        # 初始展示核心公式，再添加标题
        self.play(Write(euler_formula))
        self.wait(1)
        self.play(
            Write(title),
            euler_formula.animate.next_to(title, DOWN, buff=DEFAULT_BUFF)
        )
        self.wait(1.5)

        # --------------------------
        # 2. 泰勒级数与麦克劳林级数
        # --------------------------
        # 用VGroup组织级数相关内容，便于统一管理位置
        taylor_group = VGroup()
        taylor_title = Text("Taylor Series Definition", font_size=32)
        taylor_series = MathTex(
            r"f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \cdots",
            font_size=32
        )
        maclaurin = MathTex(
            r"f(x) = f(0) + f'(0)x + \frac{f''(0)}{2!}x^2 + \cdots",
            font_size=32
        )
        # 组内元素排版
        taylor_group.add(taylor_title, taylor_series, maclaurin)
        taylor_group.arrange(DOWN, buff=DEFAULT_BUFF)
        taylor_group.next_to(euler_formula, DOWN, buff=DEFAULT_BUFF*1.5)

        # 分步显示级数内容
        self.play(Write(taylor_title))
        self.wait(0.5)
        self.play(Write(taylor_series))
        self.wait(1)
        self.play(Write(maclaurin))
        self.wait(1.5)

        # 清除泰勒部分，保留麦克劳林公式
        self.play(
            FadeOut(taylor_title),
            FadeOut(taylor_series),
            maclaurin.animate.next_to(euler_formula, DOWN, buff=DEFAULT_BUFF*1.5)
        )

        # --------------------------
        # 3. 指数函数展开与替换
        # --------------------------
        # 指数级数组
        exp_title = Text("Exponential Function Series", font_size=32)
        exp_series = MathTex(
            r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots",
            font_size=36
        )
        
        # 将指数级数放置在麦克劳林公式下方
        exp_series.next_to(maclaurin, DOWN*2.5, buff=DEFAULT_BUFF)
        exp_title.next_to(exp_series, UP, buff=DEFAULT_BUFF/2)
        
        self.play(
            Write(exp_title),
            Write(exp_series)
        )
        self.wait(1.5)

        # 替换x为iθ
        replace_step = MathTex(
            r"e^{i\theta} = 1 + i\theta + \frac{(i\theta)^2}{2!} + \frac{(i\theta)^3}{3!} + \cdots",
            font_size=36
        ).move_to(exp_series.get_center())
        
        self.play(
            FadeOut(maclaurin),
            FadeOut(exp_title),
            Transform(exp_series, replace_step)
        )
        self.wait(1.5)

        # i的幂次说明
        i_powers = MathTex(
            r"i^0 = 1,\ i^1 = i,\ i^2 = -1,\ i^3 = -i,\ i^4 = 1,\ \cdots",
            font_size=32
        )
        i_powers.next_to(exp_series, DOWN, buff=DEFAULT_BUFF).to_corner(RIGHT, buff=1.0)
        self.play(Write(i_powers))
        self.wait(1.5)

        # 简化展开式
        simplified = MathTex(
            r"e^{i\theta} = 1 + i\theta - \frac{\theta^2}{2!} - i\frac{\theta^3}{3!} + \frac{\theta^4}{4!} + \cdots",
            font_size=36
        ).next_to(euler_formula, DOWN, buff=DEFAULT_BUFF * 1.5)
        
        self.play(
            Transform(exp_series, simplified),
            i_powers.animate.next_to(simplified, DOWN, buff=DEFAULT_BUFF).to_corner(RIGHT, buff=1.0)
        )
        self.wait(1.5)

        # --------------------------
        # 4. 分离实部虚部与三角函数展开
        # --------------------------
        self.play(
            FadeOut(i_powers),
            exp_series.animate.next_to(euler_formula, DOWN ,buff=1.0)
        )

        # 实部虚部分离
        real_imaginary = MathTex(
            r"e^{i\theta} = \left(1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots \right) + i\left(\theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots \right)",
            font_size=36
        )
        real_imaginary.next_to(exp_series, DOWN, buff=DEFAULT_BUFF*1.2)
        self.play(Write(real_imaginary))
        self.wait(1.5)

        # 三角函数展开式
        cos_group = VGroup(
            Text("Cosine Series (Real)", font_size=28, color=RED),
            MathTex(
                r"\cos\theta = 1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots",
                font_size=36, color=RED
            )
        ).arrange(DOWN, buff=DEFAULT_BUFF)

        sin_group = VGroup(
            Text("Sine Series (Imaginary)", font_size=28, color=BLUE),
            MathTex(
                r"\sin\theta = \theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots",
                font_size=36, color=BLUE
            )
        ).arrange(DOWN, buff=DEFAULT_BUFF)

        # 左右对称放置
        trig_group = VGroup(cos_group, sin_group).arrange(RIGHT, buff=2.5)
        trig_group.next_to(real_imaginary, DOWN, buff=DEFAULT_BUFF*1.2)
        self.play(FadeIn(cos_group, shift=UP), FadeIn(sin_group, shift=UP))
        self.wait(1.5)

        # 高亮对应部分
        self.play(
            Create(SurroundingRectangle(real_imaginary[0][4:23], color=RED, buff=0.1)),
            Create(SurroundingRectangle(cos_group[1], color=RED, buff=0.1))
        )
        self.wait(1)
        self.play(
            Create(SurroundingRectangle(real_imaginary[0][25:50], color=BLUE, buff=0.1)),
            Create(SurroundingRectangle(sin_group[1], color=BLUE, buff=0.1))
        )
        self.wait(1.5)

        # --------------------------
        # 5. 结论与可视化部分
        # --------------------------
        # 最终公式展示
        result = MathTex(r"e^{i\theta} = \cos\theta + i\sin\theta", font_size=48)
        self.play(
            FadeOut(Group(exp_series, real_imaginary, trig_group, *self.mobjects)),
        )
        self.wait(0.5)
        self.play(Write(result))
        self.wait(1)

        # --------------------------
        # 6. 使用画圆思路优化的角度标记
        # --------------------------
        self.play(FadeOut(result))

        # 复平面与单位圆
        plane = ComplexPlane(
            x_range=[-1.5, 1.5, 0.5],
            y_range=[-1.5, 1.5, 0.5],
            background_line_style={"stroke_color": TEAL, "stroke_width": 0.5, "stroke_opacity": 0.3}
        ).center()

        unit_circle = Circle(radius=1, color=WHITE).move_to(plane.get_origin())
        self.play(Create(plane), run_time=1.5)
        self.play(Create(unit_circle), run_time=1)
        self.wait(0.5)

        # 角度追踪器
        theta_tracker = ValueTracker(0)

        # 圆心点
        center_dot = Dot(plane.get_origin(), color=RED, radius=0.05)
        
        # 优化的角度弧：使用画圆思路
        angle_arc = always_redraw(
            lambda: Arc(
                radius=0.4,  # 圆弧半径
                start_angle=0,
                angle=theta_tracker.get_value(),
                arc_center=plane.get_origin(),
                color=GREEN,
                stroke_width=3
            )
        )
        
        # 角度标签
        angle_label = always_redraw(
            lambda: MathTex(r"\theta", font_size=24, color=GREEN)
                .next_to(
                    angle_arc.point_from_proportion(0.5), 
                    UR if theta_tracker.get_value() < PI else UL, 
                    buff=0.1
                )
        )
        
        # 动态半径线段
        moving_radius = always_redraw(
            lambda: Line(
                start=plane.get_origin(),
                end=plane.n2p(np.exp(1j * theta_tracker.get_value())),
                color=YELLOW,
                stroke_width=3
            )
        )

        # 固定半径线段（参考）
        static_radius = Line(plane.get_origin(), plane.n2p(1), color=YELLOW, stroke_width=2)
        
        # 欧拉向量
        euler_vector = always_redraw(lambda: Arrow(
            start=plane.get_origin(),
            end=plane.n2p(np.exp(1j * theta_tracker.get_value())),
            color=YELLOW, buff=0, tip_length=0.15, stroke_width=3
        ))

        # 文本信息
        info_texts = VGroup(
            always_redraw(lambda: MathTex(
                fr"\theta = {theta_tracker.get_value():.2f}",
                font_size=28
            ).to_corner(UL, buff=0.5)),
            always_redraw(lambda: MathTex(
                r"e^{i\theta} = \cos\theta + i\sin\theta",
                font_size=28
            ).to_corner(UR, buff=0.5)),
            always_redraw(lambda: MathTex(
                fr"\cos\theta = {np.cos(theta_tracker.get_value()):.2f}",
                font_size=24, color=RED
            ).to_corner(DL, buff=0.5)),
            always_redraw(lambda: MathTex(
                fr"\sin\theta = {np.sin(theta_tracker.get_value()):.2f}",
                font_size=24, color=BLUE
            ).to_corner(DR, buff=0.5)),
            always_redraw(lambda: MathTex(
             fr"e^{{i\theta}} = {np.cos(theta_tracker.get_value()):.2f} {'+' if np.sin(theta_tracker.get_value()) >= 0 else '-'} i{abs(np.sin(theta_tracker.get_value())):.2f}",
            font_size=28, color=YELLOW  # 黄色与欧拉向量颜色呼应
            ).move_to(plane.get_center() + UP * 2))  # 位置：复平面中心上方
        )

        # 添加所有元素
        self.add(center_dot, static_radius, moving_radius, angle_arc, angle_label, euler_vector, info_texts)
        self.play(Write(info_texts))
        
        # 动画：角度从0到2π
        self.play(
            theta_tracker.animate.set_value(2 * PI),
            run_time=8,
            rate_func=linear
        )
        self.wait(1)

        # 结束语
        conclusion = Text(
            "Euler's formula connects exponential\nand trigonometric functions", 
            font_size=32
        ).center()

        self.play(
            FadeOut(VGroup(plane, unit_circle, center_dot, static_radius, moving_radius, 
                           angle_arc, angle_label, euler_vector, info_texts)),
            FadeIn(conclusion)
        )
        self.wait(2)

        # 最终淡出
        self.play(FadeOut(conclusion), FadeOut(title))
        self.wait(1)