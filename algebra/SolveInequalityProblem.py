from manim import *

class SolveInequalityProblem(Scene):
    def construct(self):
        # 创建问题文本，使用更大的字体
        line1_parts = [
            Text("已知函数", font_size=40),
            MathTex(r"f(x)=\frac{1 + \ln x}{x}", font_size=40),
            Text("，若对任意", font_size=40),
            MathTex(r"x_1,x_2 \in (1,+\infty) (x_1 \neq x_2)", font_size=40),
            Text("，", font_size=40)
        ]
        line2_parts = [
            Text("都有", font_size=40),
            MathTex(r"|f(x_1) - f(x_2)| \leq k|\ln x_1 - \ln x_2|", font_size=40),
            Text("，求实数", font_size=40),
            MathTex(r"k", font_size=40),
            Text("的取值范围。", font_size=40)
        ]
        
        # 排列第一行
        line1 = VGroup(*line1_parts).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        # 排列第二行
        line2 = VGroup(*line2_parts).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        # 将两行组合在一起
        problem = VGroup(line1, line2).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        
        # 显示问题
        self.play(Write(problem))
        self.wait(3)
        
        # 将问题移动到左上角
        # 由于字体变大，需要更小的缩放比例
        problem_scale = 0.8  # 缩小比例
        problem.move_to(ORIGIN)  # 确保从中心开始移动
        
        # 计算左上角位置，留出适当边距
        top_left = np.array([-config.frame_width/2 + 0.7, config.frame_height/2 - 0.7, 0])
        
        # 执行移动和缩小动画
        self.play(
            problem.animate.scale(problem_scale).move_to(top_left).align_to(top_left, LEFT).align_to(top_left, UP),
            run_time=2
        )
        
        self.wait(2)
        
        # 解法1的步骤展示
        solution_title = Text("解法1：", font_size=36, color=YELLOW).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(solution_title))
        self.wait(3)
        
        # 第一部分：导数结果和单调性分析
        part1_title = Text("第一步：求导和单调性分析", font_size=36, color=BLUE)
        part1_title.next_to(solution_title, DOWN, aligned_edge=LEFT, buff=0.5)
        
        f_prime_result = MathTex(r"f'(x) = -\frac{\ln x}{x^2}", font_size=36)
        f_prime_result.next_to(part1_title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        monotonicity = VGroup(
            MathTex("f(x)", font_size=36),
            Text("在", font_size=36),
            MathTex("(0,1)", font_size=36),
            Text("上递增，在", font_size=36),
            MathTex("(1,+\infty)", font_size=36),
            Text("上递减", font_size=36)).arrange(RIGHT, buff=0.1)
        monotonicity.next_to(f_prime_result, DOWN, aligned_edge=LEFT, buff=0.3)
        
        part1 = VGroup(part1_title, f_prime_result, monotonicity)
        self.play(Write(part1))
        self.wait(3)
        
        # 淡出第一部分，准备显示第二部分
        self.play(FadeOut(part1))
        
        # 第二部分：假设和符号分析
        part2_title = Text("第二步：假设和符号分析", font_size=36, color=BLUE)
        part2_title.next_to(solution_title, DOWN, aligned_edge=LEFT, buff=0.5)
        
        assumption_part = VGroup(
            MathTex("x_1, x_2 \in (1, +\infty),", font_size=36),  # x₁对应x_1，∈对应\in，+∞对应+\infty
            Text("不妨设", font_size=36)
        ).arrange(RIGHT, buff=0.1)
        assumption_math = MathTex(r"1<x_1<x_2", font_size=36)
        assumption = VGroup(assumption_part, assumption_math).arrange(RIGHT, buff=0.1)
        assumption.next_to(part2_title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        sign_text = Text("则", font_size=36)
        sign_math1 = MathTex(r"f(x_1)-f(x_2)>0,", font_size=36)
        sign_math2 = MathTex(r"\ln x_1 - \ln x_2<0", font_size=36)
        sign_analysis = VGroup(sign_text, sign_math1, sign_math2).arrange(RIGHT, buff=0.1)
        sign_analysis.next_to(assumption, DOWN, aligned_edge=LEFT, buff=0.3)
        
        part2 = VGroup(part2_title, assumption, sign_analysis)
        self.play(Write(part2))
        self.wait(3)
        
        # 淡出第二部分，准备显示第三部分
        self.play(FadeOut(part2))
        
        # 第三部分：去绝对值和构造函数
        part3_title = Text("第三步：去绝对值和构造函数", font_size=36, color=BLUE)
        part3_title.next_to(solution_title, DOWN, aligned_edge=LEFT, buff=0.5)
        
        abs_text = Text("去绝对值有:", font_size=36)
        abs_math = MathTex(r"f(x_1)+k\ln x_1\leq f(x_2)+k\ln x_2", font_size=36)
        abs_removal = VGroup(abs_text, abs_math).arrange(RIGHT, buff=0.1)
        abs_removal.next_to(part3_title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        construct_text = Text("构造", font_size=36)
        construct_math = MathTex(r"g(x)=f(x)+k\ln x,", font_size=36)
        construct_domain = Text("x>1", font_size=36)
        function_construction = VGroup(construct_text, construct_math, construct_domain).arrange(RIGHT, buff=0.1)
        function_construction.next_to(abs_removal, DOWN, aligned_edge=LEFT, buff=0.3)
        
        monotonicity_text1 = Text("由题意:", font_size=36)
        monotonicity_math1 = MathTex(r"g(x_1)\leq g(x_2),", font_size=36)
        monotonicity_text2 = Text("即有", font_size=36)
        monotonicity_math2 = MathTex(r"g'(x)\geq 0", font_size=36)
        g_monotonicity = VGroup(monotonicity_text1, monotonicity_math1, monotonicity_text2, monotonicity_math2).arrange(RIGHT, buff=0.1)
        g_monotonicity.next_to(function_construction, DOWN, aligned_edge=LEFT, buff=0.3)
        
        part3 = VGroup(part3_title, abs_removal, function_construction, g_monotonicity)
        self.play(Write(part3))
        self.wait(3)
        
        # 淡出第三部分，准备显示第四部分
        self.play(FadeOut(part3))
        
        # 第四部分：计算导数和得到k的条件
        part4_title = Text("第四步：计算导数和得到k的条件", font_size=36, color=BLUE)
        part4_title.next_to(solution_title, DOWN, aligned_edge=LEFT, buff=0.5)
        
        derivative_text = Text("计算", font_size=36)
        derivative_math = MathTex(r"g'(x)=f'(x)+\frac{k}{x}=-\frac{\ln x}{x^2}+\frac{k}{x}", font_size=36)
        derivative_calc = VGroup(derivative_text, derivative_math).arrange(RIGHT, buff=0.1)
        derivative_calc.next_to(part4_title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        condition_text = Text("则", font_size=36)
        condition_math = MathTex(r"k\geq\frac{\ln x}{x}", font_size=36)
        condition_domain = Text("在(1,+∞)上恒成立", font_size=36)
        k_condition = VGroup(condition_text, condition_math, condition_domain).arrange(RIGHT, buff=0.1)
        k_condition.next_to(derivative_calc, DOWN, aligned_edge=LEFT, buff=0.3)
        
        part4 = VGroup(part4_title, derivative_calc, k_condition)
        self.play(Write(part4))
        self.wait(3)
        
        # 淡出第四部分，准备显示第五部分
        self.play(FadeOut(part4))
        
        # 第五部分：求最大值和最终答案
        part5_title = Text("第五步：求最大值和最终答案", font_size=36, color=BLUE)
        part5_title.next_to(solution_title, DOWN, aligned_edge=LEFT, buff=0.5)
        
        max_text = Text("即", font_size=36)
        max_math = MathTex(r"k\geq\left[\frac{\ln x}{x}\right]_{\max}=\frac{1}{e}", font_size=36)
        max_value = VGroup(max_text, max_math).arrange(RIGHT, buff=0.1)
        max_value.next_to(part5_title, DOWN, aligned_edge=LEFT, buff=0.3)
        
        answer_text = Text("所以", font_size=40, color=GREEN)
        answer_math = MathTex(r"k\in\left[\frac{1}{e},+\infty\right)", font_size=40, color=GREEN)
        answer = VGroup(answer_text, answer_math).arrange(RIGHT, buff=0.1)
        answer.next_to(max_value, DOWN, aligned_edge=LEFT, buff=0.5)
        
        part5 = VGroup(part5_title, max_value, answer)
        self.play(Write(part5))
        self.wait(3)