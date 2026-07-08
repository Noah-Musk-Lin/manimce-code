from manim import*
class Circle_Area(Scene):
    def construct(self):
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
