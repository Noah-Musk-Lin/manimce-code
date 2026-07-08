from manim import*
class Tem(Scene):
    def construct(self):
        c = Circle(radius=3,color=BLUE,fill_opacity=0.5).move_to(LEFT*2)
        self.play(Create(c))
        self.wait()
        
        