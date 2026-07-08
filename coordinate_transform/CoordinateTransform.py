from manim import *


class CoordinateTransform(Scene):
    def construct(self):
        title = Text("坐标变换可视化", font_size=48).to_edge(UP)
        self.add(title)
        
        # 创建坐标轴
        axes = Axes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            x_length=10,
            y_length=10,
            axis_config={"include_tip": True},
        )
        axes.center()
        
        # 创建网格
        grid = NumberPlane(
            x_range=[-5, 5],
            y_range=[-5, 5],
            x_length=10,
            y_length=10,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
        )
        grid.shift(axes.get_center())
        
        # 原始坐标系标题 - 移到底部
        original_label = Text("原始坐标系", font_size=24, color=WHITE).to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(original_label))
        self.play(DrawBorderThenFill(axes), Create(grid))
        self.wait(1)
        
        # 创建单位矩阵和示例变换矩阵
        identity_matrix = [[1, 0], [0, 1]]
        transform_matrix = [[1.5, 0.5], [0.5, 1.5]]
        shear_matrix = [[1, 1], [0, 1]]
        rotation_matrix = [[0.866, -0.5], [0.5, 0.866]]
        
        # 创建一个点和它的轨迹
        point = Dot(color=RED, radius=0.08)
        point_coords = [2, 1]
        point.move_to(axes.c2p(*point_coords))
        
        # 创建向量箭头
        vector = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(*point_coords),
            color=RED,
            buff=0,
        )
        
        # 标签
        vector_label = MathTex(r"\vec{v} = (2, 1)", font_size=36, color=RED).next_to(vector, UP)
        
        self.play(Create(vector), Write(vector_label))
        self.wait(1)
        
        # 演示不同变换
        self.show_transform(axes, grid, vector, vector_label, point, identity_matrix, "单位矩阵 (不变换)", title)
        self.show_transform(axes, grid, vector, vector_label, point, transform_matrix, "伸缩变换矩阵", title)
        self.show_transform(axes, grid, vector, vector_label, point, shear_matrix, "剪切变换矩阵", title)
        self.show_transform(axes, grid, vector, vector_label, point, rotation_matrix, "旋转变换矩阵", title)
        
    def show_transform(self, axes, grid, vector, vector_label, point, matrix, description, title):
        # 计算变换后的坐标
        new_x = matrix[0][0] * 2 + matrix[0][1] * 1
        new_y = matrix[1][0] * 2 + matrix[1][1] * 1
        
        # 保存网格状态用于恢复
        grid.save_state()
        
        # 变换网格
        self.play(
            FadeOut(vector_label),
            FadeOut(vector),
            FadeOut(point),
        )
        
        # 动画显示网格变换
        transform_desc = Text(description, font_size=28, color=YELLOW).next_to(title, DOWN, buff=0.3)
        matrix_tex = MathTex(f"M = {matrix}", font_size=36).next_to(transform_desc, DOWN, buff=0.3)
        
        self.play(Write(transform_desc))
        self.play(Write(matrix_tex))
        self.wait(0.5)
        
        # 变换网格动画
        self.play(
            grid.animate.apply_matrix(matrix),
            run_time=2
        )
        
        # 显示变换后的向量
        new_vector = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(new_x, new_y),
            color=RED,
            buff=0,
        )
        
        new_point = Dot(color=RED, radius=0.08).move_to(axes.c2p(new_x, new_y))
        
        new_label = MathTex(f"M \\cdot \\vec v = ({new_x:.2f}, {new_y:.2f})", font_size=36, color=RED).next_to(new_vector, UP)
        
        self.play(Create(new_vector), Create(new_point))
        self.play(Write(new_label))
        self.wait(1.5)
        
        # 恢复
        self.play(
            FadeOut(transform_desc),
            FadeOut(matrix_tex),
            FadeOut(new_label),
            FadeOut(new_vector),
            FadeOut(new_point),
            grid.animate.restore(),
        )
        self.wait(0.5)
        
        # 恢复原始向量
        original_vector = Arrow(
            start=axes.c2p(0, 0),
            end=axes.c2p(2, 1),
            color=RED,
            buff=0,
        )
        original_label = MathTex(r"\vec{v} = (2, 1)", font_size=36, color=RED).next_to(original_vector, UP)
        
        self.play(Create(original_vector))
        self.play(Write(original_label))
        self.wait(0.5)


class GridTransformAnimation(Scene):
    def construct(self):
        title = Text("矩阵变换的直观理解", font_size=48).to_edge(UP)
        self.add(title)
        
        # 原始网格
        grid = NumberPlane(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=8,
            y_length=8,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
        )
        grid.shift(DOWN * 0.5)
        
        # 坐标系
        axes = Axes(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=8,
            y_length=8,
        )
        axes.shift(DOWN * 0.5)
        
        self.play(Write(grid), Write(axes))
        self.wait(1)
        
        # 保存状态用于恢复
        grid.save_state()
        
        # 重要向量：i帽和j帽
        i_hat = Arrow(start=axes.c2p(0, 0), end=axes.c2p(1, 0), color=RED, buff=0)
        j_hat = Arrow(start=axes.c2p(0, 0), end=axes.c2p(0, 1), color=GREEN, buff=0)
        
        i_label = MathTex(r"\hat{i}", font_size=36, color=RED).next_to(i_hat, RIGHT)
        j_label = MathTex(r"\hat{j}", font_size=36, color=GREEN).next_to(j_hat, UP)
        
        self.play(Create(i_hat), Create(j_hat))
        self.play(Write(i_label), Write(j_label))
        self.wait(1)
        
        # 解释文本 - 放在网格下方
        explain = Text("矩阵的列就是变换后的基向量", font_size=24).to_edge(DOWN).shift(UP * 2.5)
        self.play(Write(explain))
        self.wait(1)
        
        # 显示变换矩阵的含义 - 放在右侧
        matrix_display = MathTex(
            r"A = \begin{bmatrix} a & c \\ b & d \end{bmatrix}",
            font_size=28
        ).shift(RIGHT * 4, UP * 0.5)
        
        matrix_display2 = MathTex(
            r"\hat{i} \to (a, b)",
            font_size=24
        ).next_to(matrix_display, DOWN, buff=0.3).shift(RIGHT * 0.5)
        
        matrix_display3 = MathTex(
            r"\hat{j} \to (c, d)",
            font_size=24
        ).next_to(matrix_display2, DOWN, buff=0.2)
        
        self.play(Write(matrix_display))
        self.play(Write(matrix_display2), Write(matrix_display3))
        self.wait(2)
        
        # 演示一个具体例子 - 放在左侧
        example_title = Text("示例: 旋转45°", font_size=28, color=YELLOW).shift(LEFT * 4, UP * 0.5)
        
        # 旋转矩阵
        theta = PI / 4
        rot_matrix = [[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]]
        
        example_matrix = MathTex(
            f"R = \\begin{{bmatrix}} {np.cos(theta):.2f} & {-np.sin(theta):.2f} \\\\ "
            f"{np.sin(theta):.2f} & {np.cos(theta):.2f} \\end{{bmatrix}}",
            font_size=36
        ).next_to(example_title, DOWN, buff=0.3)
        
        self.play(Write(example_title))
        self.play(Write(example_matrix))
        self.wait(1)
        
        # 动画旋转
        self.play(
            grid.animate.apply_matrix(rot_matrix),
            i_hat.animate.apply_matrix(rot_matrix),
            j_hat.animate.apply_matrix(rot_matrix),
            i_label.animate.apply_matrix(rot_matrix),
            j_label.animate.apply_matrix(rot_matrix),
            run_time=2
        )
        
        # 更新标签位置
        new_i_pos = axes.c2p(np.cos(theta), np.sin(theta))
        new_j_pos = axes.c2p(-np.sin(theta), np.cos(theta))
        
        i_label_new = MathTex(r"R \cdot \hat{i}", font_size=28, color=RED).next_to(new_i_pos, UR, buff=0.1)
        j_label_new = MathTex(r"R \cdot \hat{j}", font_size=28, color=GREEN).next_to(new_j_pos, UL, buff=0.1)
        
        self.play(
            FadeOut(i_label),
            FadeOut(j_label),
            Write(i_label_new),
            Write(j_label_new)
        )
        
        self.wait(2)
        
        # 恢复 - 重新创建原始网格和向量
        self.play(
            FadeOut(i_label_new),
            FadeOut(j_label_new),
            FadeOut(explain),
            FadeOut(matrix_display),
            FadeOut(example_title),
            FadeOut(example_matrix),
            FadeOut(grid),
            FadeOut(i_hat),
            FadeOut(j_hat),
        )
        
        # 重新创建网格和向量
        grid = NumberPlane(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=8,
            y_length=8,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
        )
        grid.shift(DOWN * 0.5)
        
        i_hat = Arrow(start=axes.c2p(0, 0), end=axes.c2p(1, 0), color=RED, buff=0)
        j_hat = Arrow(start=axes.c2p(0, 0), end=axes.c2p(0, 1), color=GREEN, buff=0)
        
        self.play(Write(grid), Create(i_hat), Create(j_hat))
        
        # 演示剪切变换
        shear_title = Text("示例: 剪切变换", font_size=36, color=YELLOW).next_to(title, DOWN, buff=0.3)
        
        shear_matrix = [[1, 0.8], [0, 1]]
        
        shear_display = MathTex(
            f"S = \\begin{{bmatrix}} 1 & 0.8 \\\\ 0 & 1 \\end{{bmatrix}}",
            font_size=36
        ).next_to(shear_title, DOWN, buff=0.3)
        
        self.play(Write(shear_title))
        self.play(Write(shear_display))
        self.wait(1)
        
        # 恢复网格和向量
        grid_shear = grid.copy()
        i_hat_shear = Arrow(start=axes.c2p(0, 0), end=axes.c2p(1, 0), color=RED, buff=0)
        j_hat_shear = Arrow(start=axes.c2p(0, 0), end=axes.c2p(0, 1), color=GREEN, buff=0)
        
        self.play(
            grid.animate.apply_matrix(shear_matrix),
            i_hat.animate.apply_matrix(shear_matrix),
            j_hat.animate.apply_matrix(shear_matrix),
            run_time=2
        )
        
        self.wait(2)
        
        # 最终标题
        final = Text("矩阵 = 基向量的变换", font_size=40, color=YELLOW).center()
        self.play(Write(final))
        self.wait(2)


class InteractiveTransform(Scene):
    def construct(self):
        title = Text("交互式坐标变换", font_size=40).to_edge(UP).shift(UP * 0.3)
        subtitle = Text("矩阵变换效果示例", font_size=20).next_to(title, DOWN, buff=0.2)
        
        self.add(title, subtitle)
        
        # 坐标轴 - 移到底部避免与标题重叠
        grid = NumberPlane(
            x_range=[-3, 3],
            y_range=[-3, 3],
            x_length=6,
            y_length=6,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
        )
        grid.shift(DOWN * 1.2)
        
        axes = Axes(
            x_range=[-3, 3],
            y_range=[-3, 3],
            x_length=6,
            y_length=6,
        )
        axes.shift(DOWN * 1.2)
        
        self.play(Write(grid), Write(axes))
        
        # 示例点
        point = Dot(color=RED, radius=0.1)
        point.move_to(axes.c2p(1, 1))
        
        point_label = MathTex("(1, 1)", font_size=28, color=RED).next_to(point, UR, buff=0.1)
        
        self.play(Create(point), Write(point_label))
        
        # 原始位置标记
        original_point = Dot(color=GRAY, radius=0.08).move_to(axes.c2p(1, 1))
        
        # 多个变换矩阵示例
        matrices = [
            ([[1.5, 0], [0, 1.5]], "缩放 1.5x", YELLOW),
            ([[1, 0.7], [0, 1]], "水平剪切", BLUE),
            ([[0.866, -0.5], [0.5, 0.866]], "旋转30°", GREEN),
            ([[0.5, 0], [0, 0.5]], "缩小 0.5x", ORANGE),
        ]
        
        # 保存初始状态
        grid.save_state()
        
        for matrix, desc, color in matrices:
            # 计算新位置
            new_x = matrix[0][0] * 1 + matrix[0][1] * 1
            new_y = matrix[1][0] * 1 + matrix[1][1] * 1
            
            # 标题
            transform_title = Text(f"{desc}", font_size=32, color=color).next_to(title, DOWN, buff=0.3)
            matrix_tex = MathTex(f"M = {matrix}", font_size=28).next_to(transform_title, DOWN, buff=0.2)
            
            self.play(Write(transform_title))
            self.play(Write(matrix_tex))
            
            # 变换动画
            new_point = Dot(color=RED, radius=0.1).move_to(axes.c2p(new_x, new_y))
            new_label = MathTex(f"({new_x:.2f}, {new_y:.2f})", font_size=28, color=RED).next_to(new_point, UR, buff=0.1)
            
            self.play(
                grid.animate.apply_matrix(matrix),
                point.animate.move_to(axes.c2p(new_x, new_y)),
            )
            self.play(Write(new_label))
            
            self.wait(1)
            
            # 恢复 - 使用FadeOut/FadeIn方式
            self.play(
                FadeOut(transform_title),
                FadeOut(matrix_tex),
                FadeOut(new_label),
                FadeOut(grid),
                FadeOut(point),
            )
            
            # 重新创建网格和点
            grid = NumberPlane(
                x_range=[-3, 3],
                y_range=[-3, 3],
                x_length=6,
                y_length=6,
                background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
            )
            grid.shift(DOWN * 0.5)
            
            point = Dot(color=RED, radius=0.1)
            point.move_to(axes.c2p(1, 1))
            
            self.play(Write(grid), Create(point))
        
        self.wait(1)


class JacobianVisualization(Scene):
    def construct(self):
        title = Text("雅可比矩阵: 多维坐标变换", font_size=44).to_edge(UP)
        self.add(title)
        
        # 3D 风格展示 (用2D模拟)
        # 原始坐标系
        grid = NumberPlane(
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=4,
            y_length=4,
            background_line_style={"stroke_color": BLUE_E, "stroke_width": 1},
        )
        grid.shift(LEFT * 3)
        
        # 变换后的坐标系  
        grid2 = NumberPlane(
            x_range=[-2, 2],
            y_range=[-2, 2],
            x_length=4,
            y_length=4,
            background_line_style={"stroke_color": GREEN_E, "stroke_width": 1},
        )
        grid2.shift(RIGHT * 3)
        
        # 标签
        original_label = Text("原始空间 (u, v)", font_size=20).next_to(grid, UP)
        transform_label = Text("变换后 (x, y)", font_size=20).next_to(grid2, UP)
        
        self.play(Write(original_label), Write(transform_label))
        self.play(Write(grid), Write(grid2))
        
        # 例子: 极坐标变换 - 放在中间
        formula = MathTex(
            r"x = r\cos\theta,\ y = r\sin\theta",
            font_size=24
        ).next_to(title, DOWN, buff=0.5)
        
        formula2 = MathTex(
            r"J = \begin{bmatrix} \cos\theta & -r\sin\theta \\ \sin\theta & r\cos\theta \end{bmatrix}",
            font_size=22
        ).next_to(formula, DOWN, buff=0.3)
        
        self.play(Write(formula), Write(formula2))
        self.wait(2)
        
        # 动画: 网格变形
        # 径向拉伸
        def radial_transform(point):
            x, y, z = point
            r = np.sqrt(x**2 + y**2)
            theta = np.arctan2(y, x) if x != 0 or y != 0 else 0
            new_r = r * 1.5
            return np.array([new_r * np.cos(theta), new_r * np.sin(theta), z])
        
        self.play(
            grid2.animate.apply_function(radial_transform),
            run_time=2
        )
        
        explanation = Text("面积缩放因子 = det(J)", font_size=28, color=YELLOW).next_to(formula, UP, buff=0.5)
        self.play(Write(explanation))
        
        self.wait(2)


if __name__ == "__main__":
    from manim import config
    config.media_dir = "./media"
    
    # 生成所有场景
    scenes = [
        "CoordinateTransform",
        "GridTransformAnimation", 
        "InteractiveTransform",
        "JacobianVisualization",
    ]
    
    for scene_name in scenes:
        print(f"Rendering {scene_name}...")
        config.output_file = scene_name
        scene = eval(f"{scene_name}()")
        scene.render()
