# -*- coding: utf-8 -*-
r"""二分查找 高级可视化动画
Binary Search — 数组演示 + 公式讲解同步进行

运行:
  manim -pqh "OPENGL.py" BinarySearchDemo
"""
from manim import *


# ═════════════════════════════════════════════════════════════
# 配色方案 — 暗色主题 / 无白色文字
# ═════════════════════════════════════════════════════════════
BG        = "#10131A"   # 背景
PANEL     = "#1A1F2B"   # 面板
INK       = "#E8ECF1"   # 主文字（近白但不刺眼）
MUTED     = "#8892A6"   # 次要文字
EDGE      = "#596275"   # 边框线条

GREEN     = "#4CC38A"   # 找到 / 成功
YELLOW    = "#F6C85F"   # mid / 警告
ORANGE    = "#FF9F43"   # 右半区 / 更新
RED       = "#FF6B6B"   # high / 左半区
BLUE      = "#6CA8FF"   # low / 信息
PURPLE    = "#C792EA"   # 装饰
TEAL      = "#63D2D6"   # 数组值
PINK      = "#F48FB1"   # 渐变用

# 多彩渐变（无白色）
GRAD_RAINBOW  = [GREEN, BLUE, YELLOW, RED, PURPLE, ORANGE, TEAL]
GRAD_TITLE    = [TEAL, GREEN, YELLOW, ORANGE]
GRAD_WARM     = [ORANGE, YELLOW, GOLD, RED]
GRAD_COOL     = [BLUE, TEAL, GREEN]
GRAD_CODE     = [GREEN, TEAL, BLUE, PURPLE]

FONT_CN  = "Microsoft YaHei"
FONT_MONO = "Consolas"


# ═════════════════════════════════════════════════════════════
# 场景
# ═════════════════════════════════════════════════════════════
class BinarySearchDemo(Scene):
    def construct(self):
        self.camera.background_color = BG

        # 数据
        values = [3, 7, 12, 18, 25, 31, 42, 56, 63, 71, 80, 88, 94, 99, 105]
        target = 71
        n = len(values)

        # ═══════════════════════════════════════════════════════
        # 0. 封面
        # ═══════════════════════════════════════════════════════
        self.play_cover(values, target)

        # ═══════════════════════════════════════════════════════
        # 1. 问题设置 — 数组 + 目标
        # ═══════════════════════════════════════════════════════
        self.array_cells = self.play_problem_setup(values, target)

        # ═══════════════════════════════════════════════════════
        # 2. 算法公式面板
        # ═══════════════════════════════════════════════════════
        algo_panel = self.play_algorithm_intro()

        # ═══════════════════════════════════════════════════════
        # 3. 逐步演示
        # ═══════════════════════════════════════════════════════
        self.play_step(values, self.array_cells, target, 1,
                       0, n - 1, (0 + n - 1) // 2,
                       values[7], "<", "目标在右半区",
                       "low = mid + 1 = 8", algo_panel)

        self.play_step(values, self.array_cells, target, 2,
                       8, n - 1, (8 + n - 1) // 2,
                       values[11], ">", "目标在左半区",
                       "high = mid - 1 = 10", algo_panel)

        self.play_step(values, self.array_cells, target, 3,
                       8, 10, (8 + 10) // 2,
                       values[9], "=", "在索引 9 处找到！✓",
                       "", algo_panel, is_final=True)

        # ═══════════════════════════════════════════════════════
        # 4. 复杂度 + 代码
        # ═══════════════════════════════════════════════════════
        self.play_complexity_and_code(algo_panel, values, target)

    # ══════════════════════════════════════════════════════════
    # 封面
    # ══════════════════════════════════════════════════════════
    def play_cover(self, values, target):
        """设计感封面：标题 + 数组缩影 + 渐变装饰"""
        # 网格背景
        grid = VGroup()
        for x in [i * 0.6 for i in range(-11, 12)]:
            line = Line([x, -3.6, 0], [x, 3.6, 0],
                       color="#222A3A", stroke_width=0.6)
            line.set_opacity(0.28 if abs(x) % 1 else 0.45)
            grid.add(line)
        for y in [i * 0.6 for i in range(-6, 7)]:
            line = Line([-7, y, 0], [7, y, 0],
                       color="#222A3A", stroke_width=0.6)
            line.set_opacity(0.28 if abs(y) % 1 else 0.45)
            grid.add(line)

        # 边框
        frame = Rectangle(width=11.8, height=6.4,
                          stroke_color="#2E384D", stroke_width=1.2)

        # 装饰色条
        accent = VGroup(
            Line([-5.4, 2.0, 0], [-3.5, 2.0, 0], color=GREEN, stroke_width=3),
            Line([-5.4, 1.85, 0], [-4.7, 1.85, 0], color=ORANGE, stroke_width=3),
            Line([-5.4, 1.70, 0], [-4.2, 1.70, 0], color=BLUE, stroke_width=3),
        )

        # 标题
        kicker = Text("SEARCH ALGORITHM", font=FONT_CN, font_size=14, color=BLUE)
        kicker.move_to([-3.3, 1.3, 0])
        title = Text("BINARY SEARCH", font=FONT_CN, font_size=52,
                     weight=BOLD, color=INK)
        title.move_to([-2.0, 0.55, 0])
        cn_title = Text("二分查找算法演示", font=FONT_CN, font_size=30, color=INK)
        cn_title.move_to([-2.5, -0.06, 0])
        subtitle = Text("有序数组 · 折半搜索 · O(log n) · 三步定位",
                        font=FONT_CN, font_size=18, color=MUTED)
        subtitle.move_to([-2.5, -0.62, 0])

        # 标签组
        chips = VGroup(
            self.make_chip("已排序数组", GREEN),
            self.make_chip("O(log n)", ORANGE),
            self.make_chip("分治思想", BLUE),
        )
        chips.arrange(RIGHT, buff=0.14)
        chips.move_to([-2.65, -1.12, 0])

        # 数组缩影（封面用）
        mini_cells = self.make_mini_array(values, target)
        mini_cells.move_to([2.5, -0.1, 0])

        # 扫描线
        scan = Line([-5.6, -2.8, 0], [-5.6, 2.8, 0],
                    color=GREEN, stroke_width=1.8)
        scan.set_opacity(0.3)

        cover = VGroup(grid, frame, accent, kicker, title, cn_title,
                       subtitle, chips, mini_cells, scan)

        self.play(FadeIn(grid), Create(frame), run_time=0.7)
        self.play(LaggedStart(Create(accent),
                              FadeIn(kicker, shift=RIGHT * 0.18),
                              lag_ratio=0.18), run_time=0.6)
        self.play(FadeIn(title, shift=UP * 0.15),
                  FadeIn(cn_title, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(subtitle),
                  LaggedStart(*[FadeIn(c, shift=UP * 0.06) for c in chips],
                              lag_ratio=0.12), run_time=0.7)
        self.play(LaggedStart(Create(mini_cells), lag_ratio=0.05), run_time=1.0)
        self.play(scan.animate.shift(RIGHT * 11.2),
                  run_time=1.1, rate_func=linear)
        self.wait(0.4)
        self.play(FadeOut(cover, shift=UP * 0.1), run_time=0.7)

    def make_mini_array(self, values, target):
        """封面用迷你数组"""
        group = VGroup()
        cell_w = 0.34
        gap = 0.06
        total_w = len(values) * cell_w + (len(values) - 1) * gap
        start_x = -total_w / 2 + cell_w / 2

        for i, v in enumerate(values):
            box = RoundedRectangle(
                width=cell_w, height=0.34,
                corner_radius=0.03,
                stroke_color=GREEN if v == target else "#3B465C",
                stroke_width=1.4,
                fill_color="#151B26", fill_opacity=1,
            )
            box.move_to([start_x + i * (cell_w + gap), 0, 0])
            txt = Text(str(v), font=FONT_MONO, font_size=11,
                       color=GREEN if v == target else INK)
            txt.move_to(box)
            group.add(VGroup(box, txt))
        return group

    def make_chip(self, text, color):
        """彩色小标签"""
        label = Text(text, font=FONT_CN, font_size=12, color=INK)
        box = RoundedRectangle(
            width=label.width + 0.28, height=0.3,
            corner_radius=0.07,
            stroke_color=color, stroke_width=1.1,
            fill_color=color, fill_opacity=0.12,
        )
        label.move_to(box)
        return VGroup(box, label)

    # ══════════════════════════════════════════════════════════
    # 问题设置
    # ══════════════════════════════════════════════════════════
    def play_problem_setup(self, values, target):
        """绘制完整数组 + 问题描述"""
        # 标题
        self.show_stage("问题：在有序数组中查找目标值")

        # 绘制数组
        array_cells = self.make_array_cells(values)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in array_cells],
                        lag_ratio=0.04),
            run_time=1.8,
        )

        # 数组标签
        arr_label = Text("有序数组 A[0..14]", font=FONT_CN, font_size=16, color=MUTED)
        arr_label.next_to(
            VGroup(*array_cells).arrange(RIGHT, buff=0.06),
            DOWN, buff=0.25,
        )
        self.play(FadeIn(arr_label, shift=UP * 0.06))

        # 右侧面板：问题描述
        panel = self.make_info_panel(
            "📋 问题设定",
            [
                f"数组长度 n = {len(values)}",
                f"所有元素 严格递增",
                f"目标值 T = {target}",
                "每次比较排除一半",
                "最多 ⌈log₂ 15⌉ = 4 步",
            ],
            accent=TEAL,
        )
        panel.move_to([5.5, 2.0, 0])
        self.play(FadeIn(panel, shift=LEFT * 0.15), run_time=0.7)

        # 高亮目标
        self.play(
            array_cells[9][0].animate.set_stroke(GREEN, width=3.5)
                              .set_fill("#1A3A2A", opacity=1),
            array_cells[9][1].animate.set_color(GREEN),
            run_time=0.7,
        )
        self.wait(1.2)
        self.play(FadeOut(panel), FadeOut(arr_label), run_time=0.5)

        return array_cells

    def make_array_cells(self, values):
        """构建数组单元格列表，每个是 VGroup(box, value_text, index_text)"""
        cells = []
        cell_w = 0.72
        gap = 0.08
        total_w = len(values) * cell_w + (len(values) - 1) * gap
        start_x = -total_w / 2 + cell_w / 2
        y = -0.45

        for i, v in enumerate(values):
            x = start_x + i * (cell_w + gap)
            box = RoundedRectangle(
                width=cell_w, height=0.68,
                corner_radius=0.06,
                stroke_color="#3B465C", stroke_width=2,
                fill_color="#171C27", fill_opacity=1,
            )
            box.move_to([x, y, 0])
            box.set_z_index(2)

            val_txt = Text(str(v), font=FONT_MONO, font_size=20, color=INK)
            val_txt.move_to(box.get_center() + UP * 0.08)
            val_txt.set_z_index(8)

            idx_txt = Text(str(i), font=FONT_MONO, font_size=12, color=MUTED)
            idx_txt.move_to(box.get_center() + DOWN * 0.22)
            idx_txt.set_z_index(8)

            cells.append(VGroup(box, val_txt, idx_txt))
        return cells

    # ══════════════════════════════════════════════════════════
    # 算法公式介绍
    # ══════════════════════════════════════════════════════════
    def play_algorithm_intro(self):
        """展示二分查找伪代码面板"""
        self.show_stage("算法：维护三个指针 low / high / mid")

        lines = [
            (r"low \leftarrow 0,\; high \leftarrow n-1", BLUE),
            (r"\mathbf{while}\; low \le high:", PURPLE),
            (r"\quad mid \leftarrow \lfloor(low + high)/2\rfloor", YELLOW),
            (r"\quad \mathbf{if}\; A[mid] < T:\; low \leftarrow mid+1", GREEN),
            (r"\quad \mathbf{else\;if}\; A[mid] > T:\; high \leftarrow mid-1", ORANGE),
            (r"\quad \mathbf{else}:\; \mathbf{return}\; mid \;\checkmark", GREEN),
        ]

        algo_group = VGroup()
        for text, color in lines:
            m = MathTex(text, font_size=20, color=color)
            algo_group.add(m)
        algo_group.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        algo_group.move_to([-4.5, 2.0, 0])

        box = RoundedRectangle(
            width=algo_group.width + 0.7, height=algo_group.height + 0.6,
            corner_radius=0.08,
            stroke_color=BLUE, stroke_width=1.5,
            fill_color=PANEL, fill_opacity=0.95,
        )
        box.move_to(algo_group)
        box.set_z_index(0)

        title = Text("▎二分查找伪代码", font=FONT_CN, font_size=16, color=BLUE)
        title.next_to(box, UP, buff=0.07)
        title.align_to(box, LEFT)

        algo_panel = VGroup(box, title, algo_group)
        self.play(FadeIn(box), FadeIn(title), run_time=0.5)
        self.play(LaggedStart(*[Write(m) for m in algo_group],
                              lag_ratio=0.1), run_time=1.5)
        self.wait(1.0)
        return algo_panel

    # ══════════════════════════════════════════════════════════
    # 单步执行
    # ══════════════════════════════════════════════════════════
    def play_step(self, values, array_cells, target, step_num,
                  low, high, mid, mid_val, cmp_op, _result_cn, update_cn,
                  _algo_panel, is_final=False):
        """执行一步二分查找"""

        # --- 步骤标题 ---
        stage_text = f"第 {step_num} 步：计算 mid 并比较"
        if is_final:
            stage_text = f"第 {step_num} 步：找到目标！"
        self.show_stage(stage_text)

        # --- 已淘汰区间变灰 ---
        eliminated_anims = []
        for i in range(len(values)):
            if step_num >= 2 and i < low:
                eliminated_anims.append(
                    array_cells[i][0].animate.set_fill("#111520", opacity=0.6)
                                     .set_stroke("#2A3040", width=1.2))
                eliminated_anims.append(
                    array_cells[i][1].animate.set_color("#4A5060"))
            if step_num >= 3 and i > high:
                eliminated_anims.append(
                    array_cells[i][0].animate.set_fill("#111520", opacity=0.6)
                                     .set_stroke("#2A3040", width=1.2))
                eliminated_anims.append(
                    array_cells[i][1].animate.set_color("#4A5060"))

        if eliminated_anims:
            self.play(*eliminated_anims, run_time=0.6)

        # --- 当前搜索区间高亮 ---
        range_anims = []
        for i in range(low, high + 1):
            range_anims.append(
                array_cells[i][0].animate.set_fill("#192438", opacity=1)
                                 .set_stroke(BLUE, width=2.5))
        if range_anims:
            self.play(*range_anims, run_time=0.5)

        # --- low 指针 ---
        arrow_low = self.make_pointer_arrow(array_cells[low], DOWN, BLUE)
        lbl_low = MathTex(r"\text{low}=" + str(low), font_size=22, color=BLUE)
        lbl_low.next_to(arrow_low, DOWN, buff=0.06)

        # --- high 指针 ---
        arrow_high = self.make_pointer_arrow(array_cells[high], DOWN, RED)
        lbl_high = MathTex(r"\text{high}=" + str(high), font_size=22, color=RED)
        lbl_high.next_to(arrow_high, DOWN, buff=0.06)

        self.play(
            Create(arrow_low), Write(lbl_low),
            Create(arrow_high), Write(lbl_high),
            run_time=0.7,
        )

        # --- mid 指针（从上方指入）---
        arrow_mid = Arrow(
            start=array_cells[mid].get_top() + UP * 0.7,
            end=array_cells[mid].get_top() + UP * 0.05,
            color=YELLOW, stroke_width=5,
            max_tip_length_to_length_ratio=0.15,
        )
        lbl_mid = MathTex(r"\text{mid}=" + str(mid), font_size=24, color=YELLOW)
        lbl_mid.next_to(arrow_mid, UP, buff=0.06)

        # mid 高亮框
        mid_highlight = SurroundingRectangle(
            array_cells[mid][0],
            color=YELLOW, stroke_width=4.5,
            buff=0.06, corner_radius=0.08,
        )
        mid_highlight.set_z_index(5)

        self.play(
            Create(arrow_mid), Write(lbl_mid),
            Create(mid_highlight),
            run_time=0.8,
        )

        # --- 右侧状态面板（精简） ---
        target_val = str(target)
        if cmp_op == "<":
            compare_line = f"{mid_val} < {target_val} → 向右搜索"
        elif cmp_op == ">":
            compare_line = f"{mid_val} > {target_val} → 向左搜索"
        else:
            compare_line = f"{mid_val} == {target_val}  ✓ 找到！"

        state_lines = [
            f"low={low}  high={high}",
            f"mid = ({low}+{high})/2 = {mid}",
            compare_line,
        ]
        if update_cn:
            state_lines.append(update_cn)

        accent_color = GREEN if is_final else (ORANGE if cmp_op == ">" else BLUE)

        panel = self.make_info_panel(
            f"📍 第 {step_num} 步", state_lines, accent=accent_color, small=True,
        )
        panel.move_to([5.5, 2.0, 0])

        self.play(FadeIn(panel, shift=LEFT * 0.12), run_time=0.6)

        # --- 比较动画：mid 格变色 ---
        compare_color = GREEN if is_final else (RED if cmp_op == ">" else ORANGE)
        self.play(
            array_cells[mid][0].animate.set_fill(compare_color, opacity=0.25)
                                .set_stroke(compare_color, width=3.5),
            array_cells[mid][1].animate.set_color(compare_color),
            run_time=0.6,
        )

        self.wait(2.0)

        # --- 找到时的特殊动画 ---
        if is_final:
            found_glow = SurroundingRectangle(
                array_cells[mid][0],
                color=GREEN, stroke_width=6,
                buff=0.1, corner_radius=0.1,
            )
            found_glow.set_z_index(10)
            badge = Text("✓ FOUND", font=FONT_CN, font_size=20, color=GREEN)
            badge.next_to(found_glow, UP, buff=0.12)
            badge.set_z_index(11)

            self.play(
                Create(found_glow),
                Write(badge),
                array_cells[mid][0].animate.set_fill("#1A3A2A", opacity=1)
                                    .set_stroke(GREEN, width=4),
                run_time=1.0,
            )
            self.wait(1.5)

            # 清理
            pointers = VGroup(arrow_low, lbl_low, arrow_high, lbl_high,
                              arrow_mid, lbl_mid, mid_highlight)
            self.play(FadeOut(pointers), FadeOut(panel), run_time=0.6)
            return

        # --- 更新动画：缩小搜索范围 ---
        if cmp_op == "<":
            # 淘汰左边
            for i in range(low, mid + 1):
                self.play(
                    array_cells[i][0].animate.set_fill("#111520", opacity=0.55)
                                      .set_stroke("#2A3040", width=1.2),
                    array_cells[i][1].animate.set_color("#4A5060"),
                    run_time=0.04,
                )
        else:
            # 淘汰右边
            for i in range(mid, high + 1):
                self.play(
                    array_cells[i][0].animate.set_fill("#111520", opacity=0.55)
                                      .set_stroke("#2A3040", width=1.2),
                    array_cells[i][1].animate.set_color("#4A5060"),
                    run_time=0.04,
                )

        self.wait(0.8)

        # --- 清理指针和面板 ---
        pointers = VGroup(arrow_low, lbl_low, arrow_high, lbl_high,
                          arrow_mid, lbl_mid, mid_highlight)
        self.play(FadeOut(pointers), FadeOut(panel), run_time=0.5)

        # 重置 mid 格颜色
        self.play(
            array_cells[mid][0].animate.set_fill("#111520", opacity=0.55)
                                .set_stroke("#2A3040", width=1.2),
            array_cells[mid][1].animate.set_color("#4A5060"),
            run_time=0.3,
        )

    def make_pointer_arrow(self, cell, direction, color):
        """创建指向单元格的箭头"""
        if np.allclose(direction, DOWN):
            start = cell.get_bottom() + DOWN * 0.65
            end   = cell.get_bottom() + DOWN * 0.05
        else:
            start = cell.get_top() + UP * 0.65
            end   = cell.get_top() + UP * 0.05
        arrow = Arrow(start, end, color=color, stroke_width=4.5,
                      max_tip_length_to_length_ratio=0.14)
        return arrow

    # ══════════════════════════════════════════════════════════
    # 复杂度 + 代码结尾
    # ══════════════════════════════════════════════════════════
    def play_complexity_and_code(self, algo_panel, values, target):
        """展示核心代码"""
        self.show_stage("核心代码")

        # 清除算法面板
        self.play(FadeOut(algo_panel, shift=RIGHT * 0.2), run_time=0.5)

        # 代码块 — 使用 Manim 内置 Code 对象
        code_text = """def binary_search(a, target):
    low, high = 0, len(a) - 1
    while low <= high:
        mid = (low + high) // 2
        if a[mid] < target:
            low = mid + 1
        elif a[mid] > target:
            high = mid - 1
        else:
            return mid
    return -1"""

        code_block = Code(
            code_string=code_text,
            tab_width=4,
            language="Python",
            add_line_numbers=False,
            background="rectangle",
            background_config={
                "fill_color": PANEL,
                "fill_opacity": 0.97,
                "stroke_color": GREEN,
                "stroke_width": 1.8,
                "corner_radius": 0.1,
            },
            paragraph_config={
                "font": "Consolas",
                "font_size": 16,
                "line_spacing": 0.55,
                "alignment": "left",
            },
        )
        code_block.move_to([0, 0.15, 0])

        self.play(FadeIn(code_block, shift=UP * 0.1), run_time=1.2)
        self.wait(2.5)

        # --- 收尾 ---
        if hasattr(self, 'array_cells'):
            self.play(FadeOut(VGroup(*self.array_cells), shift=DOWN * 0.15),
                      run_time=0.8)

        self.wait(1.5)
        self.play(FadeOut(code_block), run_time=1.0)

    # ══════════════════════════════════════════════════════════
    # 工具方法
    # ══════════════════════════════════════════════════════════
    def show_stage(self, text):
        """显示阶段标题（顶部居中，短暂显示）"""
        stage = Text(text, font=FONT_CN, font_size=20, color=BLUE)
        stage.move_to([0, 3.35, 0])
        self.play(FadeIn(stage, shift=DOWN * 0.1), run_time=0.35)
        self.wait(0.2)
        self.play(FadeOut(stage), run_time=0.35)

    def make_info_panel(self, title, lines, accent=BLUE, small=False):
        """创建信息面板 — 纯 Text，避免 LaTeX 中文问题"""
        title_size = 13 if small else 16
        line_size  = 12 if small else 15
        line_buff  = 0.08 if small else 0.14
        h_pad      = 1.0 if small else 1.6
        w_pad      = 0.5 if small else 0.7

        title_mob = Text(title, font=FONT_CN, font_size=title_size, color=INK)

        line_mobs = VGroup()
        for line in lines:
            if not line.strip():
                spacer = Text(" ", font=FONT_CN, font_size=4)
                line_mobs.add(spacer)
                continue
            display = Text(line, font=FONT_CN, font_size=line_size, color=INK)
            line_mobs.add(display)

        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=line_buff)

        # 外面板
        height = line_mobs.height + title_mob.height + h_pad
        width = max(line_mobs.width, title_mob.width) + w_pad

        box = RoundedRectangle(
            width=width, height=height,
            corner_radius=0.1,
            stroke_color=accent, stroke_width=1.8,
            fill_color=PANEL, fill_opacity=0.96,
        )
        box.set_z_index(5)

        title_mob.next_to(box, UP, buff=0.08)
        title_mob.align_to(box, LEFT)
        title_mob.set_z_index(8)

        line_mobs.next_to(title_mob, DOWN, buff=0.2)
        line_mobs.align_to(box, LEFT).shift(RIGHT * 0.2)
        line_mobs.set_z_index(8)

        panel = VGroup(box, title_mob, line_mobs)
        return panel


# ═════════════════════════════════════════════════════════════
# 运行: manim -pqh "OPENGL (2).py" BinarySearchDemo
# ═════════════════════════════════════════════════════════════
