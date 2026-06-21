# -*- coding: utf-8 -*-
from manim import *


class TransformExample(Scene):
    def construct(self):

        banner = ManimBanner()
        banner.shift(UP * 0.5)
        self.play(banner.create(), run_time=1)
        self.play(banner.animate.scale(0.3), run_time=0.5)
        self.play(banner.expand(), run_time=1)

        t = Text("测试中文能否显示").next_to(banner, DOWN * 2)
        tex = VGroup(
            Text("测试数学公式:", font_size=30),
            Tex(r"$\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}$"),
        )
        tex.arrange(RIGHT, buff=SMALL_BUFF)
        tex.next_to(t, DOWN)
        self.play(Write(t), run_time=1)
        self.play(Write(tex), run_time=1)

        self.wait()
        
# 上面的代码文件名称：sample.py
#运行代码：manim -p .\sample.py