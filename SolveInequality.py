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
        # 解法2的步骤展示
        solution2_title = Text("解法2：", font_size=32, color=YELLOW).to_edge(LEFT).shift(UP*1.5)
        self.play(Write(solution2_title))
        self.wait(3)
        
        # 第一部分：构造辅助函数
        part1_title = Text("第一步：构造辅助函数", font_size=32, color=BLUE)
        part1_title.next_to(solution2_title, DOWN*0.5, aligned_edge=LEFT, buff=0.5)
        
        func_text1 = Text("已知", font_size=32)
        func_math1 = MathTex(r"f(x) = \frac{1 + \ln x}{x}", font_size=32)
        func_line1 = VGroup(func_text1, func_math1).arrange(RIGHT, buff=0.1)
        func_line1.next_to(part1_title, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        substitution_text = Text("令", font_size=32)
        substitution_math = MathTex(r"t = \ln x", font_size=32)
        substitution_text2 = Text("（则", font_size=32)
        substitution_math2 = MathTex(r"t \in \mathbb{R}", font_size=32)
        substitution_text3 = Text("，因为", font_size=32)
        substitution_math3 = MathTex(r"x > 0", font_size=32)
        substitution_text4 = Text("）", font_size=32)
        substitution_line = VGroup(
            substitution_text, substitution_math, substitution_text2, 
            substitution_math2, substitution_text3, substitution_math3, substitution_text4
        ).arrange(RIGHT, buff=0.1)
        substitution_line.next_to(func_line1, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        transform_text = Text("函数可转化为", font_size=32)
        transform_math = MathTex(r"g(t) = \frac{1 + t}{e^t}", font_size=32)
        transform_line = VGroup(transform_text, transform_math).arrange(RIGHT, buff=0.1)
        transform_line.next_to(substitution_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        condition_text = Text("题目条件", font_size=32)
        condition_math = MathTex(r"|f(x_1) - f(x_2)| \leq k|\ln x_1 - \ln x_2|", font_size=32)
        condition_text2 = Text("（", font_size=32)
        condition_math2 = MathTex(r"x_1 \neq x_2", font_size=32)
        condition_text3 = Text("）", font_size=32)
        condition_line1 = VGroup(condition_text, condition_math, condition_text2, condition_math2, condition_text3).arrange(RIGHT, buff=0.1)
        condition_line1.next_to(transform_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        equivalent_text = Text("代入", font_size=32)
        equivalent_math1 = MathTex(r"t = \ln x", font_size=32)
        equivalent_text2 = Text("后，等价于：", font_size=32)
        equivalent_line = VGroup(equivalent_text, equivalent_math1, equivalent_text2).arrange(RIGHT, buff=0.1)
        equivalent_line.next_to(condition_line1, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        final_condition = MathTex(r"|g(t_1) - g(t_2)| \leq k|t_1 - t_2| \quad (t_1 \neq t_2)", font_size=32)
        final_condition.next_to(equivalent_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        part1 = VGroup(part1_title, func_line1, substitution_line, transform_line, condition_line1, equivalent_line, final_condition)
        self.play(Write(part1))
        self.wait(3)
        
        # 淡出第一部分，准备显示第二部分
        self.play(FadeOut(part1))
        
        # 第二部分：分析"斜率绝对值"的几何意义
        part2_title = Text("第二步：分析斜率绝对值的几何意义", font_size=32, color=BLUE)
        part2_title.next_to(solution2_title, DOWN*0.5, aligned_edge=LEFT, buff=0.5)
        
        slope_text = Text("表达式", font_size=32)
        slope_math = MathTex(r"\frac{|g(t_1) - g(t_2)|}{|t_1 - t_2|}", font_size=32)
        slope_text2 = Text("表示函数", font_size=32)
        slope_math2 = MathTex(r"g(t)", font_size=32)
        slope_text3 = Text("上两点连线的斜率的绝对值", font_size=32)
        slope_line1 = VGroup(slope_text, slope_math, slope_text2, slope_math2, slope_text3).arrange(RIGHT, buff=0.1)
        slope_line1.next_to(part2_title, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        requirement_text = Text("要使", font_size=32)
        requirement_math = MathTex(r"|g(t_1) - g(t_2)| \leq k|t_1 - t_2|", font_size=32)
        requirement_text2 = Text("恒成立，需", font_size=32)
        requirement_line = VGroup(requirement_text, requirement_math, requirement_text2).arrange(RIGHT, buff=0.1)
        requirement_line.next_to(slope_line1, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        k_condition_text = Text("即", font_size=32)
        k_condition_text2 = Text("所有两点连线斜率绝对值的最大值", font_size=32)
        k_condition_line = VGroup(k_condition_text, MathTex(r"k \geq", font_size=32), k_condition_text2).arrange(RIGHT, buff=0.1)
        k_condition_line.next_to(requirement_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        derivative_meaning_text = Text("根据导数的几何意义：当两点无限接近时，连线斜率趋近于切线斜率（即", font_size=32)
        derivative_meaning_math = MathTex(r"g'(t)", font_size=32)
        derivative_meaning_text2 = Text("）", font_size=32)
        derivative_meaning_line = VGroup(derivative_meaning_text, derivative_meaning_math, derivative_meaning_text2).arrange(RIGHT, buff=0.1)
        derivative_meaning_line.next_to(k_condition_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        transformation_text = Text("因此，问题转化为：", font_size=32)
        transformation_math = MathTex(r"k \geq |g'(t)|", font_size=32)
        transformation_text2 = Text("的最大值", font_size=32)
        transformation_line = VGroup(transformation_text, transformation_math, transformation_text2).arrange(RIGHT, buff=0.1)
        transformation_line.next_to(derivative_meaning_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        part2 = VGroup(part2_title, slope_line1, requirement_line, k_condition_line, derivative_meaning_line, transformation_line)
        self.play(Write(part2))
        self.wait(3)
        
        # 淡出第二部分，准备显示第三部分
        self.play(FadeOut(part2))
        
        # 第三部分：求g(t)的导数及极值
        part3_title = Text("第三步：求g(t)的导数及极值", font_size=32, color=BLUE)
        part3_title.next_to(solution2_title, DOWN*0.5, aligned_edge=LEFT, buff=0.5)
        
        derivative_title_text = Text("首先求一阶导数", font_size=32)
        derivative_title_math = MathTex(r"g'(t)", font_size=32)
        derivative_title_text2 = Text("：", font_size=32)
        derivative_title_line = VGroup(derivative_title_text, derivative_title_math, derivative_title_text2).arrange(RIGHT, buff=0.1)
        derivative_title_line.next_to(part3_title, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        derivative_calc = MathTex(r"g'(t) = \frac{e^t \cdot 1 - (1 + t)e^t}{(e^t)^2} = \frac{-t}{e^t}", font_size=32)
        derivative_calc.next_to(derivative_title_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        second_derivative_text = Text("为了找", font_size=32)
        second_derivative_math1 = MathTex(r"g'(t)", font_size=32)
        second_derivative_text2 = Text("的极值（从而确定", font_size=32)
        second_derivative_math2 = MathTex(r"|g'(t)|", font_size=32)
        second_derivative_text3 = Text("的范围），再求二阶导数", font_size=32)
        second_derivative_math3 = MathTex(r"g''(t)", font_size=32)
        second_derivative_text4 = Text("：", font_size=32)
        second_derivative_line = VGroup(
            second_derivative_text, second_derivative_math1, second_derivative_text2,
            second_derivative_math2, second_derivative_text3, second_derivative_math3, second_derivative_text4
        ).arrange(RIGHT, buff=0.1)
        second_derivative_line.next_to(derivative_calc, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        second_derivative_calc = MathTex(r"g''(t) = \frac{-e^t + t e^t}{(e^t)^2} = \frac{t - 1}{e^t}", font_size=32)
        second_derivative_calc.next_to(second_derivative_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        zero_point_text = Text("令", font_size=32)
        zero_point_math = MathTex(r"g''(t) = 0", font_size=32)
        zero_point_text2 = Text("，解得", font_size=32)
        zero_point_math2 = MathTex(r"t = 1", font_size=32)
        zero_point_line = VGroup(zero_point_text, zero_point_math, zero_point_text2, zero_point_math2).arrange(RIGHT, buff=0.1)
        zero_point_line.next_to(second_derivative_calc, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        analysis_text1 = Text("当", font_size=32)
        analysis_math1 = MathTex(r"t < 1", font_size=32)
        analysis_text2 = Text("时，", font_size=32)
        analysis_math2 = MathTex(r"g''(t) < 0", font_size=32)
        analysis_text3 = Text("，故", font_size=32)
        analysis_math3 = MathTex(r"g'(t)", font_size=32)
        analysis_text4 = Text("单调递减；", font_size=32)
        analysis_text5 = Text("当", font_size=32)
        analysis_math4 = MathTex(r"t > 1", font_size=32)
        analysis_text6 = Text("时，", font_size=32)
        analysis_math5 = MathTex(r"g''(t) > 0", font_size=32)
        analysis_text7 = Text("，故", font_size=32)
        analysis_math6 = MathTex(r"g'(t)", font_size=32)
        analysis_text8 = Text("单调递增", font_size=32)
        analysis_line = VGroup(
            analysis_text1, analysis_math1, analysis_text2, analysis_math2, 
            analysis_text3, analysis_math3, analysis_text4, analysis_text5, 
            analysis_math4, analysis_text6, analysis_math5, analysis_text7, 
            analysis_math6, analysis_text8
        ).arrange(RIGHT, buff=0.1)
        analysis_line.next_to(zero_point_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        conclusion_text = Text("因此，", font_size=32)
        conclusion_math1 = MathTex(r"g'(t)", font_size=32)
        conclusion_text2 = Text("在", font_size=32)
        conclusion_math2 = MathTex(r"t = 1", font_size=32)
        conclusion_text3 = Text("处取得极小值（也是最小值）：", font_size=32)
        min_value = MathTex(r"g'(1) = \frac{-1}{e^1} = -\frac{1}{e}", font_size=32)
        conclusion_line = VGroup(conclusion_text, conclusion_math1, conclusion_text2, conclusion_math2, conclusion_text3,min_value).arrange(RIGHT, buff=0.1)
        conclusion_line.next_to(analysis_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        part3 = VGroup(part3_title, derivative_title_line, derivative_calc, second_derivative_line, 
                      second_derivative_calc, zero_point_line, analysis_line,
                      conclusion_line, min_value)
        self.play(Write(part3))
        self.wait(3)
        
        # 淡出第三部分，准备显示第四部分
        self.play(FadeOut(part3))
        
        # 第四部分：确定|g'(t)|的最大值
        part4_title = Text("第四步：确定|g'(t)|的最大值", font_size=32, color=BLUE)
        part4_title.next_to(solution2_title, DOWN*0.5, aligned_edge=LEFT, buff=0.5)
        
        analysis_title = Text("分析", font_size=32)
        analysis_title_math = MathTex(r"g'(t)", font_size=32)
        analysis_title_text2 = Text("的变化：", font_size=32)
        analysis_title_line = VGroup(analysis_title, analysis_title_math, analysis_title_text2).arrange(RIGHT, buff=0.1)
        analysis_title_line.next_to(part4_title, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        limit1_text = Text("当", font_size=32)
        limit1_math1 = MathTex(r"t \to +\infty", font_size=32)
        limit1_text2 = Text("时，", font_size=32)
        limit1_math2 = MathTex(r"g'(t) = \frac{-t}{e^t} \to 0", font_size=32)
        limit1_text3 = Text("（指数增长远快于线性增长）", font_size=32)
        limit_line1 = VGroup(limit1_text, limit1_math1, limit1_text2, limit1_math2, limit1_text3).arrange(RIGHT, buff=0.1)
        limit_line1.next_to(analysis_title_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        limit2_text = Text("当", font_size=32)
        limit2_math1 = MathTex(r"t \to -\infty", font_size=32)
        limit2_text2 = Text("时，", font_size=32)
        limit2_math2 = MathTex(r"g'(t) = \frac{-t}{e^t} \to +\infty", font_size=32)
        limit2_text3 = Text("，但结合", font_size=32)
        limit2_math3 = MathTex(r"g'(t)", font_size=32)
        limit2_text4 = Text("在", font_size=32)
        limit2_math4 = MathTex(r"t=1", font_size=32)
        limit2_text5 = Text("处取得最小值", font_size=32)
        limit2_math5 = MathTex(r"-\frac{1}{e}", font_size=32)
        # 前半部分：到“最小值 -1/e”结束，排成第一行
        limit_line2_part1 = VGroup(
            limit2_text, limit2_math1, limit2_text2, limit2_math2, 
            limit2_text3, limit2_math3, limit2_text4, limit2_math4, 
            limit2_text5, limit2_math5
        ).arrange(RIGHT, buff=0.1)

        # 后半部分：从“可知”开始，排成第二行
        limit2_text6 = Text("可知", font_size=32)
        limit2_math6 = MathTex(r"|g'(t)|", font_size=32)
        limit2_text7 = Text("的最大值为", font_size=32)
        limit2_math7 = MathTex(r"\frac{1}{e}", font_size=32)
        limit_line2_part2 = VGroup(
            limit2_text6, limit2_math6, limit2_text7, limit2_math7
        ).arrange(RIGHT, buff=0.1)

        # 组合两行：垂直排列，左对齐，行间距0.2
        limit_line2 = VGroup(limit_line2_part1, limit_line2_part2).arrange(
            DOWN, buff=0.2, aligned_edge=LEFT  # 垂直排列+左对齐，确保排版整齐
        )
        limit_line2.next_to(limit_line1, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        reason_text = Text("（因为", font_size=32)
        reason_math1 = MathTex(r"g'(t)", font_size=32)
        reason_text2 = Text("最小为", font_size=32)
        reason_math2 = MathTex(r"-\frac{1}{e}", font_size=32)
        reason_text3 = Text("，其绝对值就是", font_size=32)
        reason_math3 = MathTex(r"\frac{1}{e}", font_size=32)
        reason_text4 = Text("，且其他点的", font_size=32)
        reason_math4 = MathTex(r"|g'(t)|", font_size=32)
        reason_text5 = Text("不超过此值）", font_size=32)
        reason_line = VGroup(
            reason_text, reason_math1, reason_text2, reason_math2, reason_text3, reason_math3,
            reason_text4, reason_math4, reason_text5
        ).arrange(RIGHT, buff=0.1)
        reason_line.next_to(limit_line2, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        part4 = VGroup(part4_title, analysis_title_line, limit_line1, limit_line2, reason_line)
        self.play(Write(part4))
        self.wait(3)
        
        # 淡出第四部分，准备显示第五部分
        self.play(FadeOut(part4))
        
        # 第五部分：结论
        part5_title = Text("第五步：结论", font_size=32, color=BLUE)
        part5_title.next_to(solution2_title, DOWN*0.5, aligned_edge=LEFT, buff=0.5)
        
        conclusion1_text = Text("要使", font_size=32)
        conclusion1_math = MathTex(r"|g(t_1) - g(t_2)| \leq k|t_1 - t_2|", font_size=32)
        conclusion1_text2 = Text("恒成立，需", font_size=32)
        conclusion2_math = MathTex(r"k \geq \frac{1}{e}", font_size=32)
        conclusion1_line = VGroup(conclusion1_text, conclusion1_math, conclusion1_text2,conclusion2_math).arrange(RIGHT, buff=0.1)
        conclusion1_line.next_to(part5_title, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        #conclusion2_math = MathTex(r"k \geq \frac{1}{e}", font_size=32)
        #conclusion2_math.next_to(conclusion1_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        final_conclusion_text = Text("最终，", font_size=32)
        final_conclusion_math = MathTex(r"k", font_size=32)
        final_conclusion_text2 = Text("的取值范围是", font_size=32)
        final_conclusion_line = VGroup(final_conclusion_text, final_conclusion_math, final_conclusion_text2).arrange(RIGHT, buff=0.1)
        final_conclusion_line.next_to(conclusion1_line, DOWN*0.3, aligned_edge=LEFT, buff=0.3)
        
        final_answer = MathTex(r"k\in\left[\frac{1}{e},+\infty\right)", font_size=36, color=GREEN)
        final_answer.next_to(final_conclusion_line, DOWN*0.3, aligned_edge=LEFT, buff=0.5)
        
        part5 = VGroup(part5_title, conclusion1_line, conclusion2_math, final_conclusion_line, final_answer)
        self.play(Write(part5))
        self.wait(3)