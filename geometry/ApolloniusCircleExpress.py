from manim import *

class ApolloniusCircleExpress(Scene):
    def construct(self):
        # ===================== 1. 场景初始化：平面坐标系与快递站定点 =====================
        # 创建带网格的平面坐标系，单位长度对应1公里，适配题目数值
        plane = NumberPlane(
            x_range=(-3, 4, 1),
            y_range=(-3, 3, 1),
            x_length=7,
            y_length=6,
            axis_config={"include_numbers": True},
            background_line_style={"stroke_opacity": 0.3}
        )
        # 坐标系标题
        plane_title = Text("平面坐标系（单位：公里）", font_size=24).to_corner(UL)
        self.play(Create(plane), Write(plane_title), run_time=1.5)

        # 定义两个快递站定点A、B，相距2公里，对应坐标A(-1,0)、B(1,0)
        point_A = Dot(plane.coords_to_point(-1, 0), color=BLUE, radius=0.08)
        point_B = Dot(plane.coords_to_point(1, 0), color=RED, radius=0.08)
        label_A = Text("快递站A", font_size=20, color=BLUE).next_to(point_A, UP)
        label_B = Text("快递站B", font_size=20, color=RED).next_to(point_B, UP)
        
        # 标注AB的距离
        line_AB = Line(point_A, point_B, color=GRAY, stroke_width=2)
        label_AB_dist = Text("相距2公里", font_size=20, color=GRAY).next_to(line_AB, DOWN)
        self.play(
            Create(line_AB),
            FadeIn(point_A, label_A),
            FadeIn(point_B, label_B),
            Write(label_AB_dist),
            run_time=2
        )
        self.wait(1)

        # ===================== 2. 展示核心约束条件 =====================
        condition = VGroup(
            Text("自提点P需满足：", font_size=24),
            MathTex(r"|PA| = 2|PB|", font_size=36, color=GREEN)
        ).arrange(DOWN).to_corner(UR)
        self.play(Write(condition), run_time=1.5)
        self.wait(1)

        # ===================== 3. 动点与动态元素初始化 =====================
        # 动点P（初始位置）
        point_P = Dot(plane.coords_to_point(3, 0), color=GREEN, radius=0.08)
        label_P = Text("自提点P", font_size=20, color=GREEN).next_to(point_P, UP)
        
        # PA、PB两条线段
        line_PA = Line(point_A, point_P, color=BLUE, stroke_width=2)
        line_PB = Line(point_B, point_P, color=RED, stroke_width=2)
        
        # 动态更新PA、PB的长度数值（优化：统一用向量范数计算，通用无死角）
        def update_PA(line):
            line.put_start_and_end_on(point_A.get_center(), point_P.get_center())
        def update_PB(line):
            line.put_start_and_end_on(point_B.get_center(), point_P.get_center())
        line_PA.add_updater(update_PA)
        line_PB.add_updater(update_PB)

        # PA长度文本（初始化值+通用计算）
        len_PA = DecimalNumber(
            number=np.linalg.norm(point_P.get_center() - point_A.get_center()),  # 初始值
            num_decimal_places=2, color=BLUE, font_size=20
        )
        len_PA.add_updater(lambda m: m.set_value(
            np.linalg.norm(point_P.get_center() - point_A.get_center())
        ))
        len_PA_label = Text("|PA|=", font_size=20, color=BLUE).next_to(len_PA, LEFT)
        PA_group = VGroup(len_PA_label, len_PA).to_corner(DL).shift(RIGHT*0.5)

        # PB长度文本（初始化值+通用计算）
        len_PB = DecimalNumber(
            number=np.linalg.norm(point_P.get_center() - point_B.get_center()),  # 初始值
            num_decimal_places=2, color=RED, font_size=20
        )
        len_PB.add_updater(lambda m: m.set_value(
            np.linalg.norm(point_P.get_center() - point_B.get_center())
        ))
        len_PB_label = Text("|PB|=", font_size=20, color=RED).next_to(len_PB, LEFT)
        PB_group = VGroup(len_PB_label, len_PB).next_to(PA_group, DOWN, aligned_edge=LEFT)

        # 比值文本（修复核心：增加除零保护，初始化值为2）
        ratio = DecimalNumber(
            number=2.0,  # 初始值设为2，避免初始除零
            num_decimal_places=2, color=GREEN, font_size=20
        )
        # 加除零保护：当PB长度接近0时，比值显示2；否则正常计算
        ratio.add_updater(lambda m: m.set_value(
            len_PA.get_value()/len_PB.get_value() if len_PB.get_value() > 1e-6 else 2.0
        ))
        ratio_label = Text("|PA|/|PB|=", font_size=20, color=GREEN).next_to(ratio, LEFT)
        ratio_group = VGroup(ratio_label, ratio).next_to(PB_group, DOWN, aligned_edge=LEFT)

        # 轨迹追踪：记录P点的移动路径，生成阿波罗尼斯圆
        trace_path = TracedPath(
            point_P.get_center,
            stroke_color=ORANGE,
            stroke_width=3,
            stroke_opacity=0.8
        )

        # 把所有动态元素加入场景
        self.play(
            FadeIn(point_P, label_P),
            Create(line_PA),
            Create(line_PB),
            Write(PA_group),
            Write(PB_group),
            Write(ratio_group),
            Add(trace_path),
            run_time=2
        )
        self.wait(0.5)

        # ===================== 4. 动态生成轨迹：让P点绕圆一周 =====================
        # 圆的参数：圆心(5/3, 0)，半径4/3，和之前解题结果完全一致
        center_x = 5/3
        center_y = 0
        radius = 4/3

        # 用角度控制器控制P点绕圆移动
        angle_tracker = ValueTracker(0)
        def update_P_position(mob):
            angle = angle_tracker.get_value()
            x = center_x + radius * np.cos(angle)
            y = center_y + radius * np.sin(angle)
            mob.move_to(plane.coords_to_point(x, y))
        point_P.add_updater(update_P_position)
        label_P.add_updater(lambda m: m.next_to(point_P, UP))

        # 动画：P点绕圆2周，完整画出轨迹，让学生清晰看到比值始终为2
        self.play(
            angle_tracker.animate.set_value(4 * PI),
            run_time=8,
            rate_func=linear
        )
        # 移除P点的位置更新器，固定轨迹
        point_P.remove_updater(update_P_position)
        label_P.clear_updaters()
        self.wait(1)

        # ===================== 5. 标注圆的核心信息，给出结论 =====================
        # 标注圆心
        center_point = Dot(plane.coords_to_point(center_x, center_y), color=ORANGE, radius=0.06)
        center_label = Text("圆心(5/3, 0)", font_size=20, color=ORANGE).next_to(center_point, DOWN)
        # 标注半径
        radius_line = Line(center_point, plane.coords_to_point(center_x+radius, center_y), color=ORANGE, stroke_width=2)
        radius_label = Text("半径4/3公里", font_size=20, color=ORANGE).next_to(radius_line, UP)
        # 圆的标准方程
        circle_equation = MathTex(
            r"\left(x-\frac{5}{3}\right)^2 + y^2 = \left(\frac{4}{3}\right)^2",
            font_size=32,
            color=ORANGE
        ).to_edge(DOWN*2)
        # 最终结论
        conclusion = Text(
            "自提点P的所有可选地址，连起来是一个圆形（阿波罗尼斯圆）",
            font_size=24,
            color=YELLOW
        ).to_edge(DOWN)

        # 播放最终标注动画
        self.play(
            FadeIn(center_point, center_label),
            Create(radius_line),
            Write(radius_label),
            Write(circle_equation),
            run_time=2
        )
        self.wait(1)
        self.play(Write(conclusion), run_time=1.5)
        self.wait(3)