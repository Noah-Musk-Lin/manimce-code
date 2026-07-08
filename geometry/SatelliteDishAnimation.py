from manim import *
import numpy as np

class SatelliteDishAnimation(ThreeDScene):
    """
    展示卫星天线的3D模型及其聚焦原理的动画场景
    包含3D天线旋转和2D截面的光线聚焦演示
    """
    def construct(self):
        # 设置高质量渲染
        config.quality = "high_quality"
        
        # 添加开场介绍
        title = Text("抛物面及其应用", font="SimSun", font_size=48, color=BLUE).to_edge(UP, buff=1)
        
        # 创建副标题
        subtitle = VGroup(
            Text("从几何性质到实际应用的探索", font="SimSun", font_size=36)
        ).next_to(title, DOWN, buff=0.5)
        
        # 创建大纲
        outline = VGroup(
            Text("内容大纲：", font="SimSun", font_size=32, color=YELLOW),
            Text("1. 三维模型展示", font="SimSun", font_size=28),
            Text("2. 几何性质分析", font="SimSun", font_size=28),
            Text("3. 数学原理推导", font="SimSun", font_size=28),
            Text("4. 曲面特性对比", font="SimSun", font_size=28),
            Text("5. 工程应用实例", font="SimSun", font_size=28),
            Text("6. 思考与互动", font="SimSun", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(subtitle, DOWN, buff=0.8)
        
        # 添加作者信息
        author_info = Text(
            "制作：XXX",  # 这里可以替换为实际的作者信息
            font="SimSun",
            font_size=24
        ).to_edge(DOWN, buff=0.5)
        
        # 动画序列
        # 显示标题
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        
        # 显示副标题
        self.play(Write(subtitle), run_time=1)
        self.wait(0.5)
        
        # 逐条显示大纲
        for item in outline:
            self.play(Write(item), run_time=0.5)
            self.wait(0.2)
        
        # 显示作者信息
        self.play(Write(author_info), run_time=1)
        self.wait(1)
        
        # 整体淡出
        self.play(
            *[FadeOut(mob) for mob in [title, subtitle, outline, author_info]],
            run_time=1.5
        )
        self.wait(0.5)
        
        # 添加第一部分过渡
        section_title1 = Text(
            "一、三维模型展示",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(Write(section_title1), run_time=1)
        self.wait(0.5)
        
        # 第一部分：3D卫星天线
        self.show_3d_dish()
        
        # 添加第二部分过渡
        section_title2 = Text(
            "二、几何性质分析",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(
            FadeOut(section_title1),
            FadeIn(section_title2),
            run_time=1
        )
        self.wait(0.5)
        
        # 第二部分：转换到2D截面
        self.transition_to_2d()
        
        # 添加第三部分过渡
        section_title3 = Text(
            "三、光线聚焦原理",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(
            FadeOut(section_title2),
            FadeIn(section_title3),
            run_time=1
        )
        self.wait(0.5)
        
        # 第三部分：光线聚焦演示
        self.show_focus_principle()
        
        # 添加第四部分过渡
        section_title4 = Text(
            "四、数学原理推导",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(
            FadeOut(section_title3),
            FadeIn(section_title4),
            run_time=1
        )
        self.wait(0.5)
        
        # 第四部分：数学推导
        self.show_mathematical_proof()
        
        # 添加第五部分过渡
        section_title5 = Text(
            "五、曲面特性对比",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(
            FadeOut(section_title4),
            FadeIn(section_title5),
            run_time=1
        )
        self.wait(0.5)
        
        # 第五部分：曲面对比
        self.show_surface_comparison()
        
        # 添加第六部分过渡
        section_title6 = Text(
            "六、工程应用实例",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(
            FadeOut(section_title5),
            FadeIn(section_title6),
            run_time=1
        )
        self.wait(0.5)
        
        # 第六部分：实际应用
        self.show_applications()
        
        # 添加第七部分过渡
        section_title7 = Text(
            "七、思考与互动",
            font="SimSun",
            font_size=36,
            color=BLUE
        ).to_edge(UP)
        self.play(
            FadeOut(section_title6),
            FadeIn(section_title7),
            run_time=1
        )
        self.wait(0.5)
        
        # 第七部分：互动结论
        self.show_interactive_conclusion()

    def show_3d_dish(self):
        """创建并展示3D卫星天线"""
        # 创建抛物面天线
        dish = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                0.1 * u**2
            ]),
            u_range=(0, 3),
            v_range=(0, TAU),
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5
        )

        # 设置相机角度
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        self.begin_ambient_camera_rotation(rate=0.2)

        # 添加天线支架
        stand = Cylinder(radius=0.3, height=4, direction=Z_AXIS)
        stand.set_color(GRAY)
        stand.move_to(ORIGIN)

        # 创建和展示天线
        self.play(
            Create(dish),
            Create(stand),
            run_time=2
        )
        self.wait(3)
        self.stop_ambient_camera_rotation()
        self.wait(2)

    def transition_to_2d(self):
        """过渡到2D截面"""
        # 创建2D抛物线
        parabola = ParametricFunction(
            lambda t: np.array([t, 0.25*t**2, 0]),
            t_range=[-4, 4],
            color=BLUE
        )
        
        # 移动相机到正面视角
        self.move_camera(phi=0, theta=-90*DEGREES)
        self.play(
            Create(parabola),
            run_time=2
        )
        self.wait(1)

    def show_focus_principle(self):
        """展示聚焦原理"""
        # 定义焦点
        focus_point = Dot(point=[0, 1, 0], color=RED)
        focus_label = Text("焦点", font="SimSun", font_size=24).next_to(focus_point, RIGHT)

        # 创建入射光线
        incoming_rays = VGroup(*[
            Arrow(
                start=RIGHT*4 + UP*y,
                end=RIGHT*2 + UP*y,
                color=YELLOW,
                buff=0
            ) for y in np.linspace(-2, 2, 5)
        ])

        # 创建反射光线
        reflected_rays = VGroup(*[
            Arrow(
                start=np.array([x, 0.25*x**2, 0]),
                end=np.array([0, 1, 0]),
                color=RED,
                buff=0
            ) for x in np.linspace(-2, 2, 5)
        ])

        # 展示聚焦过程
        self.play(
            Create(focus_point),
            Write(focus_label)
        )
        self.play(LaggedStart(
            *[Create(ray) for ray in incoming_rays],
            lag_ratio=0.2
        ))
        self.wait(1)
        self.play(LaggedStart(
            *[Create(ray) for ray in reflected_rays],
            lag_ratio=0.2
        ))
        self.wait(2)

        # 添加说明文字
        explanation = Text(
            "平行光线经抛物面反射后聚集于焦点",
            font="SimSun",
            font_size=36
        ).to_edge(UP)
        self.play(Write(explanation))
        self.wait(2)

    def show_mathematical_proof(self):
        """展示抛物线的数学性质和推导"""
        # 清除之前的内容
        self.clear()
        
        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY},
            x_length=8,
            y_length=6
        ).add_coordinates()

        # 定义抛物线参数
        p = 1  # 焦距

        # 创建抛物线
        parabola = FunctionGraph(
            lambda x: np.sqrt(4*p*x),
            x_range=[0, 4],
            color=BLUE
        )
        parabola_left = FunctionGraph(
            lambda x: -np.sqrt(4*p*x),
            x_range=[0, 4],
            color=BLUE
        )

        # 创建准线
        directrix = DashedLine(
            start=np.array([-p, -3, 0]),
            end=np.array([-p, 3, 0]),
            color=GREY
        )

        # 创建焦点
        focus = Dot(point=np.array([p, 0, 0]), color=GOLD)
        focus_label = VGroup(
            Text("焦点", font="SimSun", font_size=24),
            MathTex("F(p,0)", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(focus, UP)

        # 创建方程标签
        equation = MathTex(
            "y^2 = 4px",
            font_size=36
        ).to_edge(UP)

        # 动画序列
        self.play(Create(axes), run_time=1)
        self.wait(0.5)

        self.play(
            Create(parabola),
            Create(parabola_left),
            run_time=2
        )
        self.wait(0.5)

        self.play(
            Create(directrix),
            Write(MathTex("x=-p").next_to(directrix, LEFT)),
            run_time=1
        )
        self.wait(0.5)

        self.play(
            FadeIn(focus, scale=1.5),
            Write(focus_label),
            run_time=1
        )
        self.play(
            Flash(focus, color=GOLD, flash_radius=0.5),
            run_time=1
        )

        self.play(Write(equation), run_time=1)
        self.wait(1)

        # 添加焦点性质说明
        focus_property = Text(
            "所有反射光线的交汇点",
            font="SimSun",
            font_size=24
        ).next_to(focus_label, RIGHT)
        self.play(Write(focus_property), run_time=1)
        self.wait(2)

        # 在焦点性质说明之后，添加光线反射证明
        self.wait(1)
        
        # 在抛物线上选取一点P
        t = 0.6  # 参数t决定点P的位置
        point_p = Dot(
            point=np.array([t**2/(4*p), t, 0]),
            color=YELLOW
        )
        point_p_label = MathTex("P(x_1,y_1)", font_size=24).next_to(point_p, UR)
        
        # 创建切线
        tangent_slope = t/(2*p)  # 切线斜率
        tangent = Line(
            start=point_p.get_center() + LEFT*2,
            end=point_p.get_center() + RIGHT*2,
            color=GREEN
        ).set_slope(tangent_slope)
        
        # 创建法线
        normal_slope = -1/tangent_slope if tangent_slope != 0 else np.inf
        normal = DashedLine(
            start=point_p.get_center() + DOWN,
            end=point_p.get_center() + UP,
            color=PURPLE
        ).set_slope(normal_slope)
        
        # 修改入射光线和反射光线的方向
        incident_ray = Arrow(
            start=point_p.get_center() + RIGHT*2 + UP*1,  # 修改起点位置
            end=point_p.get_center(),
            color=YELLOW,
            buff=0
        )
        
        reflected_ray = Arrow(
            start=point_p.get_center(),
            end=focus.get_center(),
            color=RED,
            buff=0
        )
        
        # 修改角度计算方法
        incident_angle = Angle.from_three_points(
            incident_ray.get_start(),
            point_p.get_center(),
            tangent.get_end(),
            radius=0.5,
            color=YELLOW
        )
        
        reflected_angle = Angle.from_three_points(
            reflected_ray.get_end(),
            point_p.get_center(),
            tangent.get_end(),
            radius=0.5,
            color=RED
        )
        
        # 添加角度标注
        angle_label = MathTex("\\theta", font_size=24).next_to(incident_angle, RIGHT)
        angle_label_2 = MathTex("\\theta", font_size=24).next_to(reflected_angle, LEFT)
        
        # 动画序列
        self.play(
            Create(point_p),
            Write(point_p_label),
            run_time=1
        )
        self.wait(0.5)
        
        self.play(Create(tangent), run_time=1)
        self.play(Create(normal), run_time=1)
        self.wait(0.5)
        
        # 显示入射光线和反射光线
        self.play(Create(incident_ray), run_time=1)
        self.play(
            Create(reflected_ray),
            Create(incident_angle),
            Create(reflected_angle),
            run_time=1
        )
        
        self.play(
            Write(angle_label),
            Write(angle_label_2),
            run_time=1
        )
        self.wait(1)
        
        # 添加切线方程
        tangent_eq = MathTex(
            "y-y_1=\\frac{2p}{y_1}(x-x_1)",
            font_size=28
        ).to_edge(DOWN)
        
        self.play(Write(tangent_eq), run_time=1)
        self.wait(2)
        
        # 添加反射定律说明
        reflection_law = Text(
            "入射角等于反射角",
            font="SimSun",
            font_size=28
        ).next_to(tangent_eq, UP)
        
        self.play(Write(reflection_law), run_time=1)
        self.wait(2)

        # 清除之前的内容，包括坐标系和抛物线
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1
        )
        
        # 添加代数证明标题
        title = Text("代数验证：反射光线过焦点", font="SimSun", font_size=36).to_edge(UP)
        self.play(Write(title), run_time=1)
        
        # 创建左侧方程组
        left_equations = VGroup(
            VGroup(
                MathTex("y^2 = 4px"),
                Text("抛物线方程", font="SimSun", font_size=24)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                MathTex("\\frac{dy}{dx} = \\frac{2p}{y}"),
                Text("切线斜率", font="SimSun", font_size=24)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                MathTex("k_r = -\\frac{y_1}{2p}"),
                Text("反射光线斜率", font="SimSun", font_size=24)
            ).arrange(RIGHT, buff=0.3),
            VGroup(
                MathTex("y - y_1 = k_r(x - x_1)"),
                Text("反射光线方程", font="SimSun", font_size=24)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.5).shift(LEFT*3)  # 向左移动
        
        # 创建右侧计算过程
        right_calculations = VGroup(
            Text("代入焦点坐标 F(p,0)：", font="SimSun", font_size=24),
            MathTex("0 - y_1 = -\\frac{y_1}{2p}(p - x_1)"),
            MathTex("0 = -\\frac{y_1}{2p}p + \\frac{y_1^2}{2p}"),
            VGroup(
                MathTex("y_1^2 = 4px_1"),
                Text("与抛物线方程一致！", font="SimSun", font_size=24)
            ).arrange(RIGHT, buff=0.3)
        ).arrange(DOWN, buff=0.3).next_to(title, DOWN, buff=0.5).shift(RIGHT*3)  # 向右移动
        
        # 逐步显示左侧方程组
        for eq in left_equations:
            self.play(Write(eq), run_time=0.8)
            self.wait(0.3)
        
        # 逐步显示右侧计算过程
        for calc in right_calculations:
            self.play(Write(calc), run_time=0.8)
            self.wait(0.3)
        
        # 添加结论，放在底部中间
        conclusion = Text(
            "证明完成：反射光线必过焦点",
            font="SimSun",
            font_size=32,
            color=YELLOW
        ).next_to(VGroup(left_equations, right_calculations), DOWN, buff=0.5)
        
        self.play(Write(conclusion), run_time=1)
        self.wait(2)
        
        # 最终淡出所有内容
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)

    def show_surface_comparison(self):
        """展示不同曲面的反射特性对比"""
        # 设置3D场景
        self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)
        
        # 创建抛物面
        parabolic = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                0.1 * u**2
            ]),
            u_range=(0, 3),
            v_range=(0, TAU),
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5
        )
        
        # 创建球面
        spherical = Surface(
            lambda u, v: np.array([
                3 * np.cos(u) * np.cos(v),
                3 * np.cos(u) * np.sin(v),
                3 * np.sin(u)
            ]),
            u_range=(-PI/2, 0),  # 只显示上半球
            v_range=(0, TAU),
            resolution=(30, 30),
            checkerboard_colors=[RED_D, RED_E],
            stroke_width=0.5
        )
        
        # 创建焦点
        focus_point = Sphere(radius=0.1, color=GOLD)
        focus_point.move_to([0, 0, 0.75])  # 调整焦点位置
        
        # 创建入射光线（抛物面）
        parabolic_rays = VGroup(*[
            Arrow3D(
                start=np.array([x, y, 4]),
                end=np.array([x, y, 2]),
                color=YELLOW
            ) for x, y in [(1,1), (-1,1), (1,-1), (-1,-1), (0,0)]
        ])
        
        # 创建反射光线（抛物面）
        reflected_rays = VGroup(*[
            Arrow3D(
                start=ray.get_end(),
                end=focus_point.get_center(),
                color=RED
            ) for ray in parabolic_rays
        ])
        
        # 创建散射光线（球面）
        scattered_rays = VGroup(*[
            Arrow3D(
                start=np.array([x, y, 2]),
                end=np.array([
                    x + np.random.uniform(-0.5, 0.5),
                    y + np.random.uniform(-0.5, 0.5),
                    1 + np.random.uniform(-0.5, 0.5)
                ]),
                color=RED_A
            ) for x, y in [(1,1), (-1,1), (1,-1), (-1,-1), (0,0)]
        ])
        
        # 动画序列
        # 显示抛物面
        self.play(Create(parabolic), run_time=2)
        self.play(Create(focus_point))
        self.play(
            LaggedStart(*[Create(ray) for ray in parabolic_rays]),
            run_time=2
        )
        self.play(
            LaggedStart(*[Create(ray) for ray in reflected_rays]),
            run_time=2
        )
        self.wait(1)
        
        # 移动相机以更好地观察反射效果
        self.move_camera(phi=60*DEGREES, theta=-60*DEGREES)
        self.wait(1)
        
        # 转换到球面
        self.play(
            Transform(parabolic, spherical),
            FadeOut(reflected_rays),
            run_time=2
        )
        self.play(
            LaggedStart(*[Create(ray) for ray in scattered_rays]),
            run_time=2
        )
        self.wait(1)
        
        # 添加说明文字
        parabolic_text = Text(
            "抛物面：光线聚焦于焦点",
            font="SimSun",
            font_size=24
        ).to_corner(UL)
        
        spherical_text = Text(
            "球面：光线发生散射",
            font="SimSun",
            font_size=24
        ).to_corner(UR)
        
        self.add_fixed_in_frame_mobjects(parabolic_text, spherical_text)
        self.play(
            Write(parabolic_text),
            Write(spherical_text)
        )
        self.wait(2)
        
        # 清除场景
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)

    def show_applications(self):
        """展示抛物面在实际中的应用"""
        # 设置3D场景
        self.set_camera_orientation(phi=60*DEGREES, theta=-45*DEGREES)
        
        # 创建标题
        title = Text("抛物面的实际应用", font="SimSun", font_size=36).to_edge(UP)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title))
        
        # 1. 太阳能灶演示
        # 创建抛物面反射器
        solar_dish = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                0.15 * u**2
            ]),
            u_range=(0, 2),
            v_range=(0, TAU),
            resolution=(30, 30),
            checkerboard_colors=[BLUE_D, BLUE_E],
            stroke_width=0.5
        )
        
        # 创建焦点处的"火焰"效果
        focus_point = Sphere(radius=0.1, color=YELLOW)
        focus_point.move_to([0, 0, 0.6])
        
        # 创建入射光线（代表阳光）
        sun_rays = VGroup(*[
            Arrow3D(
                start=np.array([x, y, 3]),
                end=np.array([x, y, 2]),
                color=YELLOW
            ) for x, y in [(1,1), (-1,1), (1,-1), (-1,-1), (0,0)]
        ])
        
        # 创建反射光线
        reflected_rays = VGroup(*[
            Arrow3D(
                start=ray.get_end(),
                end=focus_point.get_center(),
                color=RED
            ) for ray in sun_rays
        ])
        
        # 添加说明文字
        solar_text = Text(
            "太阳能灶：聚焦阳光产生高温",
            font="SimSun",
            font_size=24
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(solar_text)
        
        # 动画序列
        self.play(
            Create(solar_dish),
            Write(solar_text),
            run_time=2
        )
        self.play(Create(focus_point))
        self.play(
            LaggedStart(*[Create(ray) for ray in sun_rays]),
            run_time=2
        )
        self.play(
            LaggedStart(*[Create(ray) for ray in reflected_rays]),
            run_time=2
        )
        
        # 焦点处的火焰效果动画
        for _ in range(3):
            self.play(
                focus_point.animate.scale(1.2).set_color(RED),
                run_time=0.5
            )
            self.play(
                focus_point.animate.scale(1/1.2).set_color(YELLOW),
                run_time=0.5
            )
        
        # 清除太阳能灶相关内容
        self.play(
            *[FadeOut(mob) for mob in [solar_dish, focus_point, sun_rays, reflected_rays, solar_text]],
            run_time=1
        )
        
        # 2. 激光发射器演示
        # 创建抛物面反射器
        laser_dish = Surface(
            lambda u, v: np.array([
                u * np.cos(v),
                u * np.sin(v),
                0.15 * u**2
            ]),
            u_range=(0, 2),
            v_range=(0, TAU),
            resolution=(30, 30),
            checkerboard_colors=[GREEN_D, GREEN_E],
            stroke_width=0.5
        )
        
        # 创建焦点光源
        laser_source = Sphere(radius=0.1, color=RED)
        laser_source.move_to([0, 0, 0.6])
        
        # 创建平行激光束
        laser_beams = VGroup(*[
            Arrow3D(
                start=laser_source.get_center(),
                end=np.array([x, y, 3]),
                color=RED
            ) for x, y in [(1,1), (-1,1), (1,-1), (-1,-1), (0,0)]
        ])
        
        # 添加说明文字
        laser_text = Text(
            "激光发射器：将点光源转化为平行光束",
            font="SimSun",
            font_size=24
        ).to_corner(UL)
        self.add_fixed_in_frame_mobjects(laser_text)
        
        # 动画序列
        self.play(
            Create(laser_dish),
            Write(laser_text),
            run_time=2
        )
        self.play(Create(laser_source))
        self.play(
            LaggedStart(*[Create(beam) for beam in laser_beams]),
            run_time=2
        )
        
        # 激光源闪烁效果
        for _ in range(3):
            self.play(
                laser_source.animate.scale(1.2),
                run_time=0.3
            )
            self.play(
                laser_source.animate.scale(1/1.2),
                run_time=0.3
            )
        
        self.wait(2)
        
        # 最终淡出所有内容
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)

    def show_interactive_conclusion(self):
        """展示抛物线变换和互动问题"""
        # 创建标题
        title = Text("思考题：抛物线变换", font="SimSun", font_size=36).to_edge(UP)
        
        # 创建坐标系
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 3, 1],
            axis_config={"color": GREY},
            x_length=8,
            y_length=6
        ).add_coordinates()
        
        # 创建原始抛物线 y^2 = 4px
        original_parabola = FunctionGraph(
            lambda x: np.sqrt(4*x),
            x_range=[0, 4],
            color=BLUE
        )
        original_parabola_left = FunctionGraph(
            lambda x: -np.sqrt(4*x),
            x_range=[0, 4],
            color=BLUE
        )
        
        # 创建原始焦点
        original_focus = Dot(point=np.array([1, 0, 0]), color=GOLD)
        original_focus_label = VGroup(
            Text("原焦点", font="SimSun", font_size=24),
            MathTex("F(p,0)", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(original_focus, UR)
        
        # 创建问题文本
        question = VGroup(
            Text("若抛物线方程改为", font="SimSun", font_size=28),
            MathTex("x^2 = 4py", font_size=28),
            Text("，焦点位置会如何变化？", font="SimSun", font_size=28)
        ).arrange(RIGHT, buff=0.2).next_to(title, DOWN)
        
        # 动画序列
        self.play(Write(title), run_time=1)
        self.play(Create(axes), run_time=1)
        self.play(
            Create(original_parabola),
            Create(original_parabola_left),
            run_time=1
        )
        self.play(
            Create(original_focus),
            Write(original_focus_label),
            run_time=1
        )
        self.play(Write(question), run_time=1)
        self.wait(1)
        
        # 创建变换后的抛物线 x^2 = 4py
        transformed_parabola = ParametricFunction(
            lambda t: np.array([t, t**2/4, 0]),
            t_range=[-2, 2],
            color=GREEN
        )
        
        # 创建新焦点
        new_focus = Dot(point=np.array([0, 1, 0]), color=RED)
        new_focus_label = VGroup(
            Text("新焦点", font="SimSun", font_size=24),
            MathTex("F(0,p)", font_size=24)
        ).arrange(RIGHT, buff=0.2).next_to(new_focus, RIGHT)
        
        # 变换动画
        self.play(
            Transform(original_parabola, transformed_parabola),
            FadeOut(original_parabola_left),
            run_time=2
        )
        
        # 焦点移动动画
        self.play(
            Transform(original_focus, new_focus),
            Transform(original_focus_label, new_focus_label),
            run_time=2
        )
        
        # 添加解释
        explanation = VGroup(
            Text("解析：", font="SimSun", font_size=28, color=YELLOW),
            Text("1. 方程变换相当于坐标轴对调", font="SimSun", font_size=24),
            Text("2. 焦点从(p,0)移动到(0,p)", font="SimSun", font_size=24),
            Text("3. 抛物线的开口方向改变", font="SimSun", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT)
        
        self.play(Write(explanation), run_time=2)
        self.wait(2)
        
        # 最终总结
        conclusion = Text(
            "抛物线的形状和焦点位置由方程决定",
            font="SimSun",
            font_size=32,
            color=YELLOW
        ).to_edge(DOWN)
        
        self.play(Write(conclusion), run_time=1)
        self.wait(2)
        
        # 最终淡出
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=2
        )
        self.wait(1)

if __name__ == "__main__":
    with tempconfig({"quality": "high_quality"}):
        scene = SatelliteDishAnimation()
        scene.render()
