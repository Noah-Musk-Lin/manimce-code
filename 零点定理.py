from manim import *

class A1(ZoomedScene):  # 替换原Scene
    def construct(self):
        # 设置中文字体
        config.font = "SimHei"
        
        # 创建支持中文的TexTemplate
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{ctex}")
        
        # 标题动画优化
        title1 = Tex(
            r"\text{证明}$x^2-4=0$\text{在区间}$(0,3)$\text{至少存在一个实根}",
            font_size=28,
            color=BLUE,
            tex_template=tex_template,
            substrings_to_isolate=["$x^2-4=0$"]
        )
        title1.set_color_by_tex("$x^2-4=0$", YELLOW)
        
        # 添加标题出现动画
        self.play(Write(title1, run_time=2))
        self.wait(1)
        
        # 使用更平滑的移动动画
        self.play(title1.animate.shift(UL * 3 ), rate_func=smooth)
        self.wait(0.5)
        
        # 创建坐标系
        ax = Axes(
            x_range=[-5, 5, 1], y_range=[-5, 5, 1],
            axis_config={"stroke_color": BLUE, "stroke_width": 1,"include_tip": True, "tip_width": 0.15, "tip_height": 0.25},
            x_length=8,
            y_length=8
        )
        ax.move_to(RIGHT * 2.5)  # 移动到坐标点
        ax.add_coordinates()
        
        # 添加坐标系出现动画
        self.play(Create(ax, run_time=1.5))
        
        # 绘制函数图像 - 使用更流畅的绘制动画
        graph1 = ax.plot(lambda x: x**2 - 4, x_range=[-5, 5], color=YELLOW)
        self.play(Create(graph1, run_time=2))
        self.wait(0.5)
        
        # 添加函数标签
        func_label = MathTex(r"f(x)=x^2-4", font_size=24, color=YELLOW, tex_template=tex_template)
        func_label.move_to(ax.c2p(-5, 1.5))
        self.play(FadeIn(func_label, shift=UP))
        self.wait(1)
        
        # 标记根的位置 - 添加强调动画
        dot = Dot(ax.c2p(2, 0), color=RED)
        root_label = MathTex(r"x=2", font_size=24, color=RED, tex_template=tex_template)
        root_label.next_to(dot, DOWN)
        
        self.play(
            FadeIn(dot, scale=0.5),
            Create(root_label, run_time=1)
        )
        self.wait(1)
        
        # 显示解方程步骤
        eq_step1 = MathTex(r"x^2-4", r"=(x+2)(x-2)=0", font_size=24, tex_template=tex_template)
        eq_step1.next_to(title1, DOWN, buff=0.5)
        eq_step1[0].set_color(YELLOW)
        self.play(FadeIn(eq_step1))
        self.wait(2)
        
        eq_step2 = MathTex(r"x_1=2, x_2=-2", font_size=24, tex_template=tex_template)
        eq_step2.next_to(eq_step1, DOWN, buff=0.5)
        self.play(TransformFromCopy(eq_step1, eq_step2))
        self.wait(2)

        
        # 第一部分结束后仅淡出函数相关元素
        self.play(
            FadeOut(title1,ax,graph1, dot, root_label, func_label, eq_step1, eq_step2),
            run_time=1.5
        )

        # 淡出原坐标系
        #self.play(FadeOut(ax), run_time=1)
        # 第二部分：证明 2x⁵-8x²+1=0 在区间(0,1)至少存在一个实根
        title2 = MathTex(
            r"\text{证明} \ 2x^5-8x^2+1=0 \ \text{在区间}(0,1)\text{至少存在一个实根}",
            font_size=28,
            color=BLUE,
            tex_template=tex_template
        )
        title2.set_color_by_tex("2x^5-8x^2+1=0", YELLOW)
        title2.move_to(ax.c2p(-3, -4))
        #title2.move_to(ORIGIN+DOWN * 2)  # 上移第二部分标题位置
        self.play(Write(title2, run_time=2))
        self.wait(1.5)
        
        # 切换场景 - 保留原坐标系，调整标题位置
        self.play(
            title1.animate.shift(UP * 4),
            title2.animate.shift(UP * 6.5),
            run_time=2,
            rate_func=smooth
        )
        self.wait(0.5)
        
        # 引入零点定理 - 添加标题强调效果
        theorem_title = MathTex(r"\text{零点定理（零值定理）}", font_size=30, color=RED, tex_template=tex_template)
        theorem_title.next_to(title2, DOWN, buff=0.7)
        
        self.play(
            Write(theorem_title, run_time=1.5),
            theorem_title.animate.scale(1.1),
            run_time=1.5
        )
        self.play(theorem_title.animate.scale(1/1.1))
        self.wait(1)
        
        theorem_content = MathTex(
            r"\text{设函数}f(x)\text{在闭区间}[a,b]\text{上连续，且}f(a)\cdot f(b)<0,",
            r"\text{则}f(x)\text{在}(a,b)\text{内至少存在一点}\xi,\text{使得}f(\xi)=0",
            font_size=24, tex_template=tex_template
        )
        theorem_content.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        theorem_content.next_to(theorem_title, DOWN, buff=0.5)
        
        # 逐行显示定理内容
        for line in theorem_content:
            self.play(Write(line, run_time=1.5))
            self.wait(0.3)
        self.wait(2)
        
        # 高亮定理 - 添加动态高亮效果
        sr = SurroundingRectangle(theorem_content, buff=0.15, color=GREEN, stroke_width=1.5)
        self.play(Create(sr, run_time=1))
        
        # 添加闪烁效果
        self.play(sr.animate.set_color(YELLOW), run_time=0.5)
        self.play(sr.animate.set_color(GREEN), run_time=0.5)
        self.wait(1)
        
        # 应用零点定理证明 - 添加步骤间的连接动画
        proof_step1 = MathTex(r"\text{设}f(x)=2x^5-8x^2+1", font_size=24, color=YELLOW, tex_template=tex_template)
        proof_step1.next_to(theorem_content, DOWN, buff=1.0)
        
        self.play(Write(proof_step1, run_time=1.5))
        self.wait(1)
        
        proof_step2 = MathTex(
            r"\text{将}0\text{和}1\text{分别代入可得：}f(0)=1,\ f(1)=-5",
            font_size=24, color=BLUE, tex_template=tex_template
        )
        proof_step2.next_to(proof_step1, DOWN, buff=0.5)
        
        self.play(Write(proof_step2, run_time=1.5))
        self.wait(1)
        
        proof_step3 = MathTex(r"f(0) \cdot f(1) = -5 < 0", font_size=24, color=YELLOW, tex_template=tex_template)
        proof_step3.next_to(proof_step2, DOWN, buff=0.5)
        
        # 添加箭头指示逻辑关系
        arrow = Arrow(proof_step2.get_corner(DR), proof_step3.get_corner(UR), color=GREEN)
        self.play(Create(arrow, run_time=0.8))
        self.play(Write(proof_step3, run_time=1.5))
        self.wait(1)
        
        proof_conclusion = MathTex(
            r"\text{所以方程在区间}(0,1)\text{至少存在一个实根}",
            font_size=24, color=BLUE, tex_template=tex_template
        )
        proof_conclusion.next_to(proof_step3, DOWN, buff=0.5)
        
        self.play(Write(proof_conclusion, run_time=1.5))
        self.wait(1)
        
        
        self.play(
            FadeOut(theorem_title, theorem_content, proof_step1, proof_step2, proof_step3, proof_conclusion,sr,arrow),
            run_time=1.5
        )
        
        
        # 创建全新的坐标系，而不是变换原坐标系
        ax2 = Axes(
            x_range=[-0.5, 1.5], y_range=[-6, 2],
            axis_config={"stroke_color": BLUE, "stroke_width": 1},
            x_axis_config={"include_ticks": True, "include_numbers": True},
            y_axis_config={"include_ticks": True},
            x_length=8,
            y_length=5
        ).shift(DOWN * 1.5)
        

        
        # 再显示新坐标系
        self.play(Create(ax2), run_time=1.5)
        
        # 绘制函数在区间[0,1]的图像 - 添加动态绘制效果
        graph2 = ax2.plot(lambda x: 2*x**5 - 8*x**2 + 1, x_range=[0, 1], color=YELLOW)
        self.play(Create(graph2, run_time=2.5))
        
        # 标记区间端点 - 添加端点出现动画
        dot_a = Dot(ax2.c2p(0, 1), color=GREEN)
        dot_b = Dot(ax2.c2p(1, -5), color=GREEN)
        label_a = MathTex(r"(0,1)", font_size=20, color=GREEN, tex_template=tex_template).next_to(dot_a, UP+LEFT)
        label_b = MathTex(r"(1,-5)", font_size=20, color=GREEN, tex_template=tex_template).next_to(dot_b, DOWN+RIGHT)
        
        self.play(
            FadeIn(dot_a, scale=0.5),
            FadeIn(dot_b, scale=0.5),
            run_time=1
        )
        self.play(
            Write(label_a, run_time=0.8),
            Write(label_b, run_time=0.8)
        )
        
        # 标记根的位置（近似值）- 添加根的发现动画
        root_x = 0.36
        dot2 = Dot(ax2.c2p(root_x, 0), color=RED)
        root_label2 = MathTex(r"\xi", font_size=24, color=RED, tex_template=tex_template).next_to(dot2, DOWN)
        
        # 添加水平和垂直参考线
        h_line = DashedLine(
            start=ax2.c2p(-0.5, 0),
            end=ax2.c2p(1.5, 0),
            color=GRAY,
            dash_length=0.1
        )
        v_line = DashedLine(
            start=ax2.c2p(root_x, -6),
            end=ax2.c2p(root_x, 2),
            color=GRAY,
            dash_length=0.1
        )
        
        self.play(Create(h_line, run_time=1))
        self.play(Create(v_line, run_time=1))
        self.play(
            FadeIn(dot2, scale=0.5),
            Write(root_label2, run_time=1)
        )
        
        # 添加函数在零点附近的缩放动画
        self.play(
            self.camera.frame.animate.scale(0.7).move_to(ax2.c2p(root_x, 0)),
            run_time=2
        )
        self.wait(1)
        self.play(
            self.camera.frame.animate.scale(1/0.7).move_to(ORIGIN),
            run_time=2
        )
        
        self.wait(3)    