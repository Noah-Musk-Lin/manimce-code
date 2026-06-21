from manim import *

class ArchimedesArea(Scene):
    def construct(self):
        # 创建核心元素
        circle = Circle(radius=2, color=BLUE)
        square_in = RegularPolygon(4, radius=2).set_color(RED)
        square_out = RegularPolygon(4, radius=2/np.cos(np.pi/4)).set_color(GREEN)
        
        # 添加初始图形
        self.add(circle)
        self.play(Create(square_in), Create(square_out))
        self.wait(1)
        
        # 动态增加边数（示例从4边到24边）
        for n in range(4, 25):
            angle = 2*np.pi/n
            in_poly = RegularPolygon(n, radius=2).rotate(angle/2).set_color(RED)
            out_poly = RegularPolygon(n, radius=2/np.cos(angle/2)).set_color(GREEN)
            
            # 平滑过渡动画
            self.play(
                ReplacementTransform(square_in, in_poly),
                ReplacementTransform(square_out, out_poly),
                run_time=0.5
            )
            square_in, square_out = in_poly, out_poly
            
            # 添加面积比较文本（示例）
            if n == 4:
                text_in = Text("内接多边形面积 < 圆面积  外切多边形面积 > 圆面积",font_size=36).next_to(in_poly, UP*5)
                #text_out = Text("外切多边形面积 > 圆面积",font_size=36).next_to(out_poly, UP)
                self.play(Write(text_in),)
                self.wait(1)
        
        # 最终极限展示
        limit_text = Text("当边数趋于无限大时，多边形面积趋于πr²",font_size=36).to_edge(DOWN)
        self.play(ReplacementTransform(text_in, limit_text))
        self.wait(2)
