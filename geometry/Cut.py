from manim import *


class Ultimate_Version_Circle_Area(Scene):
    def construct(self):
        # 添加文字
        text1 = Text("首先，我们先画一个圆。", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL)
        text1.move_to(UP * 3)  # 将文字移动到圆的上方，可根据需要调整
        self.play(Write(text1))
        self.wait(1)

        # 定义圆心
        center = ORIGIN
        # 定义圆的半径
        radius = 2
        # 创建圆心点
        center_dot = Dot(center, color=RED)
        # 创建一个动态的角度追踪器，初始角度为 0
        angle_tracker = ValueTracker(0)
        # 始终重绘圆弧，根据角度追踪器的值动态更新圆弧
        arc = always_redraw(
            lambda: Arc(
                start_angle=0,
                angle=angle_tracker.get_value(),
                radius=radius,
                arc_center=center,
                color=BLUE
            )
        )
        # 始终重绘移动的半径线段，根据角度追踪器的值动态更新线段的终点
        moving_radius = always_redraw(
            lambda: Line(
                start=center,
                end=center + radius * rotate_vector(RIGHT, angle_tracker.get_value()),
                color=GREEN
            )
        )
        # 初始半径线段，保持静止
        static_radius = Line(center, center + radius * RIGHT, color=YELLOW)
        # 将圆心点、初始半径线段、移动的半径线段和圆弧添加到场景中
        self.add(center_dot, static_radius, moving_radius, arc)
        # 播放动画，让角度追踪器的值从 0 变化到 2π，模拟画圆过程
        self.play(angle_tracker.animate.set_value(2 * PI), run_time=5)
        # 等待一段时间
        self.wait(0.5)
        # 移除动态更新的元素和圆心、半径相关元素，使用渐隐动画
        self.play(FadeOut(moving_radius, center_dot, static_radius))
        self.remove(arc)
        # 创建橙色的圆并移动到正中间
        C = Circle(radius=radius, fill_color=RED, fill_opacity=0.8,
                   stroke_color=BLUE, stroke_width=4).move_to(center)
        # 获取橙色圆的圆心位置
        new_center = C.get_center()
        # 创建新的圆心点
        new_center_dot = Dot(new_center, color=RED)
        # 创建竖直半径线段，从圆心到圆底部
        vertical_radius = Line(center, center + radius * DOWN, color=PURPLE)
        # 设置竖直半径的 z_index 为一个较大的值
        vertical_radius.set_z_index(10)
        # 创建半径长度的标注
        radius_label = Tex(r"$r$").next_to(vertical_radius, RIGHT, buff=0.2)
        # 设置标注的 z_index 为一个较大的值
        radius_label.set_z_index(10)
        # 添加橙色圆、新的圆心点、竖直半径和标注到场景中
        self.play(FadeIn(C, new_center_dot, vertical_radius, radius_label, run_time=0.5))
        # 等待一段时间
        self.play(FadeOut(text1))
        self.wait(0.5)

        # 添加文字
        text2 = Text("然后，我们对圆进行分割。", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL)
        text2.move_to(UP * 3)  # 将文字移动到圆的上方，可根据需要调整
        self.play(Write(text2))
        self.wait(1)
        self.play(FadeOut(text2))
        self.wait(1)

        # 逐渐增加同心圆的个数
        max_divisions = 110
        prev_concentric_circles = []
        prev_stacked_rectangles = None
        prev_brace = None
        prev_brace_text = None
        prev_division_text = None

        # 定义每个分割步骤的动画运行时间，可根据需要调整
        animation_run_time = 2

        # 修改循环，让分割次数间隔为 30
        for division in range(10, max_divisions + 1, 30):
            num_rectangles = division

            # 生成同心圆
            concentric_circles = []
            for i in range(num_rectangles):
                current_radius = radius * (i + 1) / num_rectangles
                circle = Circle(radius=current_radius, color=GREEN_A,
                                stroke_width=2).move_to(new_center)
                concentric_circles.append(circle)

            # 移除之前的同心圆
            if division > 1:
                self.remove(*prev_concentric_circles)

            # 将同心圆转换为矩形条并堆叠
            rectangles = []
            rectangle_height = radius / num_rectangles
            for i in range(num_rectangles):
                outer_radius = radius * (i + 1) / num_rectangles
                rectangle_width = 2 * PI * outer_radius
                rectangle = Rectangle(width=rectangle_width, height=rectangle_height, color=BLUE,
                                      stroke_width=2, fill_color=YELLOW, fill_opacity=0.8)
                # 设置矩形的 z_index 为一个较小的值
                rectangle.set_z_index(5)
                rectangles.append(rectangle)

            # 堆叠矩形条
            stacked_rectangles = VGroup(*rectangles).arrange(DOWN, buff=0)
            # 调整堆叠矩形的位置，使其最高中心点与圆心重合
            stacked_rectangles.move_to(center).align_to(center, UP)

            # 移除之前的堆叠矩形、大括号和标注文字并添加消失动画
            if prev_stacked_rectangles is not None:
                self.play(
                    FadeOut(prev_stacked_rectangles, prev_brace, prev_brace_text, prev_division_text),
                    run_time=animation_run_time
                )

            # 播放新的同心圆创建动画
            self.play(*[Create(circle) for circle in concentric_circles],
                      run_time=animation_run_time)

            # 获取最下面矩形的左右端点
            bottom_rect = stacked_rectangles[-1]
            left_point = bottom_rect.get_left()
            right_point = bottom_rect.get_right()

            # 创建大括号
            brace = BraceBetweenPoints(left_point, right_point, direction=DOWN)
            # 设置大括号的 z_index 为一个较小的值
            brace.set_z_index(5)
            # 创建标注文字
            brace_text = Tex(r"$2\pi r$")
            # 设置标注文字的 z_index 为一个较小的值
            brace_text.set_z_index(5)
            # 调整标注文字的位置，使其与矩形保持一定的间距
            brace_text.next_to(brace, DOWN, buff=0.2)

            # 创建分割次数文本
            division_text = Text(f"分割次数 n = {division}", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL)
            division_text.move_to(DOWN * 3.5)  # 将文字移动到圆的下方

            # 播放新的堆叠矩形、大括号和标注文字出现动画
            self.play(
                Create(stacked_rectangles),
                Create(brace),
                Write(brace_text),
                Write(division_text),
                run_time=animation_run_time
            )

            # 存储当前的同心圆、堆叠矩形、大括号和标注文字，用于下一次移除
            prev_concentric_circles = concentric_circles
            prev_stacked_rectangles = stacked_rectangles
            prev_brace = brace
            prev_brace_text = brace_text
            prev_division_text = division_text

            # 等待一段时间
            self.wait(0.1)

        text3 = VGroup(
            Text("分割次数逐渐增加。", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL),
            Text("圆的面积近似等于这个由矩形堆叠成的类等腰三角形的面积。", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL),
        )
        text3.arrange(DOWN, buff=SMALL_BUFF)
        text3.move_to(UP * 3)  # 将文字移动到圆的上方，可根据需要调整
        self.play(Write(text3), run_time=3)  # 显示文字动画
        self.wait(3)
        self.play(FadeOut(text3), run_time=3)
        self.wait(1)

        text5 = VGroup(
            Text("这个类等腰三角形的面积为：", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL),
            Tex(r"S = $\frac{1}{2} \times 2\pi r \times r $").set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL),
        )
        text6 = VGroup(
            Text("即圆的面积为：", font_size=36).set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL),
            Tex(r"S = $\pi r^2 $").set_color_by_gradient(GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL),
        )
        text5.arrange(RIGHT, buff=SMALL_BUFF)
        text5.move_to(UP * 3)
        text6.arrange(RIGHT, buff=SMALL_BUFF)
        text6.move_to(UP * 2.5)  # 调整 text6 的位置，避免与 text5 重叠
        self.play(Write(text5), run_time=1)
        self.wait(1)
        self.play(Write(text6), run_time=1)
        self.wait(2)
        # 最终等待
        self.wait(2)