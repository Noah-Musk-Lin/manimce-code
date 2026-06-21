from manim import *
import numpy as np
import os

class BinarySearchExplanation(Scene):
    def construct(self):

        # 标题
        title = Text("二分法求函数零点", font_size=48, color=BLUE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)
        
        # 介绍二分法
        intro_text = VGroup(
            Text("二分法基本思想:", font_size=36, color=YELLOW),
            Text("1. 在区间[a,b]上，函数f(x)连续", font_size=28),
            Text("2. 如果f(a)·f(b) < 0，则区间内存在零点", font_size=28),
            Text("3. 取中点c=(a+b)/2，计算f(c)", font_size=28),
            Text("4. 根据f(c)的符号，缩小区间", font_size=28),
            Text("5. 重复直到区间足够小", font_size=28)
        )
        intro_text.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        intro_text.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(intro_text))
        self.wait(3)
        
        # 清除介绍文本
        self.play(FadeOut(intro_text))
        
        # 创建坐标轴
        axes = Axes(
            x_range=[0, 2.1, 0.1],
            y_range=[-2, 4, 1],
            x_length=8,
            y_length=6,
            axis_config={"color": WHITE, "stroke_width": 2},
            x_axis_config={
                "numbers_to_include": [1, 2],
                "numbers_with_elongated_ticks": [1,2],
            },
            y_axis_config={
                "numbers_to_include": [-2, 0, 2, 4],
            },
            tips=False
        )
        axes.shift(DOWN * 0.5)
        
        # 定义函数 f(x) = x^2 - 2
        def func(x):
            return x**2 - 2
        
        # 绘制函数图像
        graph = axes.plot(func, x_range=[0, 2.5], color=GREEN, stroke_width=4)
        graph_label = VGroup(
            MathTex("f(x)=", font_size=36),
            MathTex("x^2-2", font_size=36)
        ).arrange(RIGHT, buff=0.1)
        graph_label.next_to(axes.coords_to_point(2.2, func(2.2)), UR)
        
        # 显示坐标轴和函数
        self.play(Create(axes))
        self.play(Create(graph), Write(graph_label))
        self.wait(1)
        
        # 显示零点位置
        zero_point = axes.coords_to_point(np.sqrt(2), 0)
        zero_dot = Dot(zero_point, color=RED, radius=0.08)
        zero_label = VGroup(
            Text("零点: ", font_size=24, color=RED),
            MathTex("x=\\sqrt{2}", font_size=24, color=RED)
        ).arrange(RIGHT, buff=0.1).next_to(zero_dot, DOWN*3.5)
        
        # 添加零点时播放声音
        self.play(Create(zero_dot), Write(zero_label))
        click_sound = "D:/manim/Code/assets/sounds/click.wav"
        self.add_sound(click_sound)
        self.wait(2)
        
        # 初始区间 [1,2]
        a, b = 1, 2
        a_point = axes.coords_to_point(a, 0)
        b_point = axes.coords_to_point(b, 0)
        
        a_dot = Dot(a_point, color=BLUE, radius=0.06)
        b_dot = Dot(b_point, color=BLUE, radius=0.06)
        
        a_label = Text("a", font_size=24, color=BLUE).next_to(a_dot, DOWN*2.5)
        b_label = Text("b", font_size=24, color=BLUE).next_to(b_dot, DOWN*2.5)
        
        # 显示区间
        interval_line = Line(a_point, b_point, color=BLUE, stroke_width=6)
        
        # 添加区间端点时播放pop声音
        pop_file = "D:/manim/Code/assets/sounds/pop.wav"
        
        self.play(
            Create(a_dot), Write(a_label),
        )
        self.add_sound(pop_file)  # 改为pop声音
        self.play(
            Create(b_dot), Write(b_label),
        )
        self.add_sound(pop_file)  # 改为pop声音
        self.play(Create(interval_line))
        self.wait(1)
        
        # 显示函数值
        f_a = func(a)
        f_b = func(b)
        
        a_func_dot = Dot(axes.coords_to_point(a, f_a), color=BLUE, radius=0.05)
        b_func_dot = Dot(axes.coords_to_point(b, f_b), color=BLUE, radius=0.05)
        
        a_func_label = VGroup(
            MathTex("f(a)=", font_size=28, color=BLUE),
            MathTex(f"{f_a}", font_size=28, color=BLUE)
        ).arrange(RIGHT, buff=0.1).next_to(a_func_dot, LEFT)
        
        b_func_label = VGroup(
            MathTex("f(b)=", font_size=28, color=BLUE),
            MathTex(f"{f_b}", font_size=28, color=BLUE)
        ).arrange(RIGHT, buff=0.1).next_to(b_func_dot, RIGHT)
        
        self.play(
            Create(a_func_dot), Write(a_func_label),
        )
        self.add_sound(pop_file)
        self.play(
            Create(b_func_dot), Write(b_func_label),
        )
        self.add_sound(pop_file)
        self.wait(1)
        
        # 检查 f(a)·f(b) < 0
        check_text = MathTex("f(a) \\cdot f(b) < 0", font_size=32, color=YELLOW)
        check_text.to_edge(UP).shift(DOWN * 1.5)
        
        self.play(Write(check_text))
        bell_sound = "D:/manim/Code/assets/sounds/bell.wav"
        self.add_sound(bell_sound)
        self.wait(2)
        
        # 存储迭代信息
        iterations = []
        colors = [ORANGE, PURPLE, PINK, GOLD]
        
        # 进行4次迭代
        for i in range(4):
            # 清除上一次的中点和函数值点（除了第一次）
            if i > 0:
                self.play(
                    FadeOut(c_dot), FadeOut(c_label),
                    FadeOut(midpoint_line),
                    FadeOut(c_func_dot), FadeOut(c_func_label)
                )
            
            # 取中点
            c = (a + b) / 2
            c_point = axes.coords_to_point(c, 0)
            c_dot = Dot(c_point, color=colors[i], radius=0.06)
            c_label = Text("c", font_size=24, color=colors[i]).next_to(c_dot, DOWN*2.5)
            
            # 中点线
            midpoint_line = DashedLine(
                axes.coords_to_point(c, 0),
                axes.coords_to_point(c, func(c)),
                color=colors[i], stroke_width=3
            )
            
            # 添加中点时播放pop声音
            self.play(
                Create(c_dot), Write(c_label),
                Create(midpoint_line) 
            )
            self.add_sound(pop_file)  # 改为pop声音
            
            # 计算 f(c)
            f_c = func(c)
            c_func_dot = Dot(axes.coords_to_point(c, f_c), color=colors[i], radius=0.05)
            c_func_label = VGroup(
                MathTex("f(c)=", font_size=28, color=colors[i]),
                MathTex(f"{f_c:.3f}", font_size=28, color=colors[i])
            ).arrange(RIGHT, buff=0.1).next_to(c_func_dot, LEFT)
            
            self.play(
                Create(c_func_dot), Write(c_func_label)
            )
            self.add_sound(pop_file)
            self.wait(0.5)
            
            # 判断符号并更新区间
            if f_c * f_a < 0:
                new_b = c
                current_a_point = axes.coords_to_point(a, 0)
                new_b_point = axes.coords_to_point(new_b, 0)
                
                new_interval_text = VGroup(
                    Text(f"第{i+1}次迭代: ", font_size=24, color=YELLOW),
                    MathTex("f(a) \\cdot f(c) < 0", font_size=24, color=YELLOW),
                    Text("零点在[a,c]区间", font_size=24, color=YELLOW)
                ).arrange(DOWN*1.5, aligned_edge=LEFT)
                
                new_interval_line = Line(current_a_point, new_b_point, color=colors[i], stroke_width=6)
                
                new_b_dot = Dot(new_b_point, color=colors[i], radius=0.06)
                new_b_label = Text("b", font_size=24, color=colors[i]).next_to(new_b_dot, DOWN)
                
                self.play(
                    Transform(b_dot, new_b_dot),
                    Transform(b_label, new_b_label),
                    Transform(interval_line, new_interval_line)
                )
                whoosh_file = "D:/manim/Code/assets/sounds/whoosh.wav"
                self.add_sound(whoosh_file)

                b = new_b
                f_b = f_c
            else:
                new_a = c
                new_a_point = axes.coords_to_point(new_a, 0)
                current_b_point = axes.coords_to_point(b, 0)
                
                new_interval_text = VGroup(
                    Text(f"第{i+1}次迭代: ", font_size=24, color=YELLOW),
                    MathTex("f(c) \\cdot f(b) < 0", font_size=24, color=YELLOW),
                    Text("零点在[c,b]区间", font_size=24, color=YELLOW)
                ).arrange(DOWN*1.5, aligned_edge=LEFT)
                
                new_interval_line = Line(new_a_point, current_b_point, color=colors[i], stroke_width=6)
                
                new_a_dot = Dot(new_a_point, color=colors[i], radius=0.06)
                new_a_label = Text("a", font_size=24, color=colors[i]).next_to(new_a_dot, DOWN)
                
                self.play(
                    Transform(a_dot, new_a_dot),
                    Transform(a_label, new_a_label),
                    Transform(interval_line, new_interval_line)
                )
                self.add_sound(whoosh_file)
                
                a = new_a
                f_a = f_c
            
            new_interval_text.to_edge(UP).shift(DOWN * 1.5)
            self.play(Transform(check_text, new_interval_text))
            self.add_sound(bell_sound)
            self.wait(1)
            
            # 记录迭代信息
            iterations.append({
                "iteration": i+1,
                "a": a,
                "b": b,
                "c": c,
                "error": abs(c - np.sqrt(2))
            })
            
            self.wait(1)
        
        # 清除中间文本
        self.play(FadeOut(check_text))
        
        # 显示最终结果
        final_title = Text("二分法结果:", font_size=36, color=GREEN)
        final_title.to_edge(UP).shift(DOWN * 1)
        
        a_result = MathTex(f"a = {a:.5f}", font_size=32)
        b_result = MathTex(f"b = {b:.5f}", font_size=32)
        c_result = MathTex(f"c = {c:.5f}", font_size=32)
        
        true_zero = VGroup(
            Text("真实零点: ", font_size=32),
            MathTex("\\sqrt{2} = ", font_size=32),
            MathTex(f"{np.sqrt(2):.5f}", font_size=32)
        ).arrange(RIGHT, buff=0.1)
        
        error = VGroup(
            Text("误差: ", font_size=32),
            MathTex(f"{abs(c - np.sqrt(2)):.5f}", font_size=32)
        ).arrange(RIGHT, buff=0.1)
        
        final_result = VGroup(
            final_title,
            a_result,
            b_result,
            c_result,
            true_zero,
            error
        )
        final_result.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        final_result.to_edge(UP).shift(DOWN * 1)
        
        self.play(Write(final_result))
        success_file = "D:/manim/Code/assets/sounds/success.wav"
        self.add_sound(success_file)
        self.wait(3)
        
        # 所有内容淡出
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(1)
        
        # 显示所有迭代结果
        results_title = Text("4次二分法迭代结果", font_size=36, color=BLUE)
        results_title.to_edge(UP)
        self.play(Write(results_title))
        self.add_sound(pop_file)  # 表格标题使用pop声音
        
        # 创建迭代结果表格
        if len(iterations) >= 4:
            table_data = [
                ["迭代", "a", "b", "中点c", "误差"],
                ["1", f"{iterations[0]['a']:.4f}", f"{iterations[0]['b']:.4f}", 
                 f"{iterations[0]['c']:.4f}", f"{iterations[0]['error']:.6f}"],
                ["2", f"{iterations[1]['a']:.4f}", f"{iterations[1]['b']:.4f}", 
                 f"{iterations[1]['c']:.4f}", f"{iterations[1]['error']:.6f}"],
                ["3", f"{iterations[2]['a']:.4f}", f"{iterations[2]['b']:.4f}", 
                 f"{iterations[2]['c']:.4f}", f"{iterations[2]['error']:.6f}"],
                ["4", f"{iterations[3]['a']:.4f}", f"{iterations[3]['b']:.4f}", 
                 f"{iterations[3]['c']:.4f}", f"{iterations[3]['error']:.6f}"]
            ]
            
            table = Table(
                table_data,
                include_outer_lines=True
            ).scale(0.7)
            
            table.next_to(results_title, DOWN, buff=0.5)
            
            for i in range(5):
                table.add_highlighted_cell((0, i), color=YELLOW)
            
            self.play(Create(table))
            self.add_sound(pop_file)  # 表格创建使用pop声音
            self.wait(2)
            
            # 显示真实值和最终近似值
            final_approx = VGroup(
                Text("最终近似值: ", font_size=32, color=GREEN),
                MathTex(f"x \\approx {iterations[3]['c']:.6f}", font_size=32, color=GREEN)
            ).arrange(RIGHT, buff=0.1)
            
            true_value = VGroup(
                Text("真实值: ", font_size=32, color=RED),
                MathTex("x = \\sqrt{2}", font_size=32, color=RED),
                MathTex(f"\\approx {np.sqrt(2):.6f}", font_size=32, color=RED)
            ).arrange(RIGHT, buff=0.1)
            
            final_error = VGroup(
                Text("最终误差: ", font_size=32, color=ORANGE),
                MathTex(f"{iterations[3]['error']:.6f}", font_size=32, color=ORANGE)
            ).arrange(RIGHT, buff=0.1)
            
            results_group = VGroup(final_approx, true_value, final_error)
            results_group.arrange(DOWN*0.5, aligned_edge=LEFT, buff=0.3)
            results_group.next_to(table, DOWN*0.5, buff=0.5)
            
            self.play(Write(results_group))
            self.add_sound(success_file)
            self.wait(2)

            self.play(FadeOut(results_title, table, results_group))

            # 显示收敛性分析
            convergence_title = Text("收敛性分析:", font_size=36, color=YELLOW)
            
            error_formula = MathTex("\\text{error} \\leq \\frac{b-a}{2^{n+1}}", font_size=32)
            
            theoretical_bound = VGroup(
                Text("理论误差上界 = ", font_size=28),
                MathTex("\\frac{2-1}{2^{4+1}} = \\frac{1}{32} = 0.03125", font_size=28)
            ).arrange(RIGHT, buff=0.1)
            
            actual_error = VGroup(
                Text("实际误差 = ", font_size=28),
                MathTex(f"{iterations[3]['error']:.6f}", font_size=28)
            ).arrange(RIGHT, buff=0.1)
            
            convergence_text = VGroup(
                convergence_title,
                error_formula,
                theoretical_bound,
                actual_error
            )
            convergence_text.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            convergence_text.to_edge(UP).shift(DOWN * 1)
            
            self.play(Write(convergence_text))
            self.add_sound(bell_sound)
            self.wait(2)
        
        # 总结
        summary_text = VGroup(
            Text("二分法总结:", font_size=36, color=YELLOW),
            Text("• 简单直观，易于实现", font_size=28),
            Text("• 收敛速度稳定，每次迭代误差减半", font_size=28),
            Text("• 需要函数连续且f(a)·f(b)<0", font_size=28),
            Text("• 线性收敛，收敛速度为1/2", font_size=28),
            Text("• 误差界限: error ≤ (b-a)/2^(n+1)", font_size=28)
        )
        summary_text.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        summary_text.to_edge(DOWN)
        
        self.play(Write(summary_text))
        self.add_sound(success_file)
        self.wait(3)
        
        # 结束
        end_text = Text("谢谢观看!", font_size=48, color=BLUE)
        self.play(FadeOut(*self.mobjects))
        self.play(Write(end_text))
        self.add_sound(bell_sound)
        self.wait(2)