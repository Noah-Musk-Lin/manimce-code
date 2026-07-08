# -*- coding: utf-8 -*-
"""
§4.3 线性映射与矩阵 —— Manim 动画脚本
教材：《高等代数学》(第四版) 谢启鸿  第四章 线性映射 §4.3

用法：
    manim -pqh section_4_3.py Scene01_Title          # 渲染单个场景（高清）
    manim -pql section_4_3.py Scene01_Title          # 低质量快速预览
    python render_all.py                              # 渲染全部场景并按顺序拼接（见文末脚本）

场景顺序 (与 PARTS 列表一一对应):
    1.  Scene01_Title          引入：几何与代数
    2.  Scene02_Lemma          引理 4.3.1
    3.  Scene03_BuildMatrix    表示矩阵的构造  (4.3.1)-(4.3.2) 式
    4.  Scene04_Definition     定义：表示矩阵
    5.  Scene05_Theorem1       定理 4.3.1 (T 是线性同构 + 交换图)
    6.  Scene06_Theorem2       定理 4.3.2 (矩阵乘法 = 映射复合)
    7.  Scene07_LVCase         L(V) 情形 与 定理 4.3.3
    8.  Scene08_Corollary      推论 4.3.1
    9.  Scene09_Bridge         基变换的动机
    10. Scene10_Theorem4       定理 4.3.4 (B = P⁻¹AP)   【核心定理】
    11. Scene11_SimilarDef     定义 4.3.1 相似矩阵
    12. Scene12_Proposition    命题 4.3.1 相似是等价关系
    13. Scene13_Summary        总结与展望
"""

from manim import *
import numpy as np
import re as _re

config.background_color = "#0B0E14"

# ----------------------------------------------------------------------
#  字体 / 配色
# ----------------------------------------------------------------------
CJK = "Noto Sans SC"

GOLD    = "#F2C14E"   # 标题 / 强调
C_V     = "#5BC8F5"   # 空间 V / 矩阵 A 相关
C_U     = "#7CD992"   # 空间 U
C_W     = "#FFA45B"   # 空间 W
C_A     = "#5BC8F5"   # 矩阵 A
C_B     = "#FF6F91"   # 矩阵 B
C_P     = "#F2C14E"   # 过渡矩阵 P
C_DEF   = "#4FC3F7"   # 定义 标签色
C_THM   = "#FFA726"   # 定理 标签色
C_LEMMA = "#9CCC65"   # 引理 标签色
C_COR   = "#BA68C8"   # 推论 标签色
C_PROOF = "#7E8AA8"   # 证明 标签色 (banner 用深色字, 背景浅紫灰)
C_PROP  = "#4DD0E1"   # 命题 标签色
TXT     = "#ECECEC"
GREY    = "#8A93A6"
DGREY   = "#5B6275"
PANEL   = "#161B26"

PARTS = [
    "引入", "引理 4.3.1", "表示矩阵的构造", "定义：表示矩阵",
    "定理 4.3.1", "定理 4.3.2", "L(V) 与定理 4.3.3", "推论 4.3.1",
    "基变换的动机", "定理 4.3.4", "相似矩阵", "相似是等价关系", "总结与展望",
]

FRAME_W = config.frame_width
FRAME_H = config.frame_height


# ----------------------------------------------------------------------
#  通用工具函数
# ----------------------------------------------------------------------
def ct(text, size=30, color=TXT, weight=NORMAL, **kwargs):
    """中文 / 西文文本 (Pango, Noto Sans CJK SC)。绝不可在此放 LaTeX 公式。"""
    return Text(text, font=CJK, font_size=size, color=color, weight=weight, **kwargs)


def eq(tex, size=36, color=TXT, **kwargs):
    """LaTeX 公式 (MathTex)。绝不可在此放中文字符。"""
    kwargs.pop("weight", None)
    return MathTex(tex, font_size=size, color=color, **kwargs)


# Unicode → LaTeX 映射（用于 mixed() 函数自动分离中英文/数学符号）
_UNI2LATEX = {
    'φ': r'\varphi', 'ψ': r'\psi', 'α': r'\alpha', 'β': r'\beta',
    'η': r'\eta',   'λ': r'\lambda', 'μ': r'\mu',   'ξ': r'\xi',
    '₁': '{}_1', '₂': '{}_2', '₃': '{}_3', 'ₙ': '{}_n', 'ₘ': '{}_m', 'ₚ': '{}_p',
    'ᵢ': '{}_i', '⁻': '{}^{-}', '¹': '{}^{1}', '₊': '{}_{+}', '₋': '{}_{-}',
    '₌': '{}_{=}', '₍': '{}_{(', '₎': '{}_{)}', '′': r'{}^\prime',
    '→': r'\to', '∈': r'\in', '∀': r'\forall', '∴': r'\therefore',
    '≈': r'\approx', '∘': r'\circ', '×': r'\times', '✓': r'\checkmark',
    '⟺': r'\Longleftrightarrow',
    '①': r'\textcircled{1}', '②': r'\textcircled{2}', '③': r'\textcircled{3}',
    '⋯': r'\cdots', '…': r'\ldots',
    '⟷': r'\longleftrightarrow',
}
_MATH_TRIGGER = set(_UNI2LATEX.keys())


def mixed(text, size=28, color=TXT, math_size=None, **kwargs):
    """
    自动分离中英文与数学符号的混合文本。
    检测到希腊字母/数学符号时，自动拆分为 VGroup(ct(...), eq(...), ...)。

    用法: mixed("线性映射 φ 是抽象的")  →  VGroup(ct("线性映射"), eq(r"\varphi"), ct("是抽象的"))
    """
    weight = kwargs.pop("weight", NORMAL)
    msize = math_size or size + 2

    # 检查是否需要拆分
    if not any(ch in _MATH_TRIGGER for ch in text):
        return ct(text, size=size, color=color, weight=weight, **kwargs)

    # 拆分为 (is_math, substring) 段
    segs = []
    buf = text[0]
    in_math = text[0] in _MATH_TRIGGER
    for ch in text[1:]:
        is_m = ch in _MATH_TRIGGER
        if is_m == in_math:
            buf += ch
        else:
            segs.append((in_math, buf))
            buf = ch
            in_math = is_m
    segs.append((in_math, buf))

    # 构建 VGroup
    parts = []
    for is_math, seg_text in segs:
        if is_math:
            latex = ''.join(_UNI2LATEX.get(ch, ch) for ch in seg_text)
            # 修复连续 Unicode 上/下标产生的无效 LaTeX
            # 例：{}^{-}{}^{1} → ^{-1}（合并连续空基底上标）
            latex = _re.sub(
                r'(\{\}\^\{[^}]*\})+',
                lambda m: '^{' + ''.join(_re.findall(r'\{\}\^\{([^}]*)\}', m.group())) + '}',
                latex,
            )
            latex = _re.sub(
                r'(\{\}_\{[^}]*\})+',
                lambda m: '_{' + ''.join(_re.findall(r'\{\}_\{([^}]*)\}', m.group())) + '}',
                latex,
            )
            parts.append(eq(latex, size=msize, color=color))
        else:
            parts.append(ct(seg_text, size=size, color=color, weight=weight))
    return VGroup(*parts).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def mat(rows, size=32, color=TXT, **kwargs):
    return Matrix(rows, left_bracket="(", right_bracket=")",
                  element_to_mobject_config={"font_size": size, "color": color},
                  **kwargs)


def row(items, size=28, math_size=None, color=TXT, buff=0.16):
    """混排一行：items = [("c","中文"), ("m","x_1"), ...]"""
    math_size = math_size or size + 2
    mobs = []
    for kind, content in items:
        if kind == "c":
            mobs.append(ct(content, size=size, color=color))
        else:
            mobs.append(eq(content, size=math_size, color=color))
    return VGroup(*mobs).arrange(RIGHT, buff=buff, aligned_edge=DOWN)


def fit_width(mobj, max_width=12.6):
    if mobj.width > max_width:
        mobj.scale_to_fit_width(max_width)
    return mobj


# ----------------------------------------------------------------------
#  基类：统一的页眉 / 进度条 / 标签 / 证明结束符
# ----------------------------------------------------------------------
class BaseScene(Scene):
    part_index = 1
    subtitle = ""

    def add_header(self):
        crumb = ct("§4.3  线性映射与矩阵", size=17, color=GREY)
        sub = ct(self.subtitle, size=23, color=GOLD, weight=BOLD)
        head = VGroup(crumb, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        head.to_corner(UL, buff=0.32)

        n = len(PARTS)
        dots = VGroup()
        for i in range(n):
            d = RoundedRectangle(corner_radius=0.025, width=0.40, height=0.085,
                                  stroke_width=0)
            d.set_fill(GOLD if i < self.part_index else "#252A38", opacity=1)
            dots.add(d)
        dots.arrange(RIGHT, buff=0.075)
        dots.to_corner(UR, buff=0.42)

        self.add(head, dots)
        return VGroup(head, dots)

    def banner(self, text, color, size=25):
        tagtxt = ct(text, size=size, color="#0B0E14", weight=BOLD)
        box = RoundedRectangle(corner_radius=0.09, fill_color=color, fill_opacity=1,
                                stroke_width=0,
                                width=tagtxt.width + 0.55, height=tagtxt.height + 0.30)
        tagtxt.move_to(box)
        return VGroup(box, tagtxt)

    def qed_mark(self):
        return Square(side_length=0.15, fill_color=WHITE, fill_opacity=1, stroke_width=0)

    def proof_label(self):
        return self.banner("证明", C_PROOF, size=22)

    def clear_scene(self, extra_wait=0.0):
        if extra_wait:
            self.wait(extra_wait)
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)


# ========================================================================
#  Scene 01 — 片头 + 引入 (motivation)
# ========================================================================
class Scene01_Title(BaseScene):
    part_index = 1
    subtitle = "引入"

    def construct(self):
        # ---------- 片头 ----------
        book = ct("高等代数学（第四版）· 谢启鸿", size=22, color=GREY)
        chapter = ct("第四章　线性映射", size=30, color=TXT)
        title = ct("§4.3   线性映射与矩阵", size=50, color=GOLD, weight=BOLD)
        underline = Line(LEFT, RIGHT, color=GOLD, stroke_width=3)
        tagline = ct("从几何到代数的桥梁", size=26, color=C_DEF)

        book.to_edge(UP, buff=1.0)
        chapter.next_to(book, DOWN, buff=0.5)
        title.next_to(chapter, DOWN, buff=0.55)
        underline.set_width(title.width * 1.05).next_to(title, DOWN, buff=0.22)
        tagline.next_to(underline, DOWN, buff=0.45)

        self.play(FadeIn(book, shift=DOWN * 0.2))
        self.play(Write(chapter))
        self.play(Write(title))
        self.play(Create(underline))
        self.play(FadeIn(tagline, shift=UP * 0.15))
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in [book, chapter, title, underline, tagline]])

        # ---------- 引入 1: 线性映射是抽象的 ----------
        head = self.add_header()

        recap = ct("回顾：我们已定义了线性空间之间的线性映射及其运算", size=27, color=TXT)
        recap.next_to(head, DOWN, buff=0.65).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(recap, shift=DOWN * 0.2))
        self.wait(0.6)

        Vc = Circle(radius=1.05, color=C_V, stroke_width=4).shift(LEFT * 3.6 + DOWN * 0.4)
        Uc = Circle(radius=1.05, color=C_U, stroke_width=4).shift(RIGHT * 3.6 + DOWN * 0.4)
        Vlabel = eq("V", size=38, color=C_V).move_to(Vc)
        Ulabel = eq("U", size=38, color=C_U).move_to(Uc)
        arrow = CurvedArrow(Vc.get_right() + RIGHT * 0.05, Uc.get_left() + LEFT * 0.05,
                             color=TXT, angle=-0.6, stroke_width=4)
        phi_label = eq(r"\varphi", size=34, color=TXT).next_to(arrow, UP, buff=0.05)

        self.play(Create(Vc), Create(Uc), Write(Vlabel), Write(Ulabel))
        self.play(Create(arrow), Write(phi_label))

        note1 = mixed("线性映射 φ 是抽象的「几何」概念，不便于计算", size=26, color=TXT)
        note1.next_to(VGroup(Vc, Uc), DOWN, buff=0.85)
        self.play(FadeIn(note1, shift=UP * 0.2))
        self.wait(1.1)

        note2 = ct("目标：把这个抽象概念『代数化』", size=30, color=GOLD, weight=BOLD)
        note2.move_to(note1)
        self.play(ReplacementTransform(note1, note2))
        self.wait(1.0)

        self.play(FadeOut(recap), FadeOut(note2),
                   FadeOut(VGroup(Vc, Uc, Vlabel, Ulabel, arrow, phi_label)))

        # ---------- 引入 2: 基 -> 坐标 -> 矩阵 ----------
        recall = ct("回顾第三章：取定基后，线性空间与坐标空间同构", size=26, color=TXT)
        recall.next_to(head, DOWN, buff=0.65)
        self.play(FadeIn(recall, shift=DOWN * 0.2))

        Vc2 = Circle(radius=0.5, color=C_V, stroke_width=3).shift(LEFT * 3.6 + UP * 1.4)
        Vlabel2 = eq("V", size=28, color=C_V).move_to(Vc2)
        Uc2 = Circle(radius=0.5, color=C_U, stroke_width=3).shift(RIGHT * 3.6 + UP * 1.4)
        Ulabel2 = eq("U", size=28, color=C_U).move_to(Uc2)

        grid = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=3.2, y_length=2.1,
            background_line_style={"stroke_color": C_V, "stroke_width": 1, "stroke_opacity": 0.55},
        ).shift(LEFT * 3.6 + DOWN * 1.1)
        grid_label = eq(r"\mathbb{K}^n", size=30, color=C_V).next_to(grid, DOWN, buff=0.2)

        grid2 = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1], x_length=3.2, y_length=2.1,
            background_line_style={"stroke_color": C_U, "stroke_width": 1, "stroke_opacity": 0.55},
        ).shift(RIGHT * 3.6 + DOWN * 1.1)
        grid2_label = eq(r"\mathbb{K}^m", size=30, color=C_U).next_to(grid2, DOWN, buff=0.2)

        eta1 = eq(r"\eta_1", size=24, color=GREY).next_to(Vc2, RIGHT, buff=0.55).shift(DOWN*0.6)
        eta2 = eq(r"\eta_2", size=24, color=GREY).next_to(Uc2, LEFT, buff=0.55).shift(DOWN*0.6)
        arr1 = Arrow(Vc2.get_bottom(), grid.get_top(), buff=0.08, color=GREY, stroke_width=3)
        arr2 = Arrow(Uc2.get_bottom(), grid2.get_top(), buff=0.08, color=GREY, stroke_width=3)

        self.play(Create(Vc2), Write(Vlabel2), Create(Uc2), Write(Ulabel2))
        self.play(
            GrowArrow(arr1), GrowArrow(arr2), Write(eta1), Write(eta2),
            FadeIn(grid), Write(grid_label), FadeIn(grid2), Write(grid2_label),
        )
        self.wait(0.7)

        idea = ct("思路：借助基，把线性映射转化为矩阵运算", size=28, color=GOLD, weight=BOLD)
        idea.next_to(VGroup(grid, grid2), DOWN, buff=0.9)
        self.play(FadeIn(idea, shift=UP * 0.2))
        self.wait(1.0)

        left_txt = ct("线性映射", size=38, color=GOLD, weight=BOLD)
        arrow_sym = eq(r"\Longleftrightarrow", size=38, color=GOLD)
        right_txt = ct("矩阵", size=38, color=GOLD, weight=BOLD)
        bigtxt = VGroup(left_txt, arrow_sym, right_txt).arrange(RIGHT, buff=0.3)
        bigtxt.move_to(idea)

        self.play(ReplacementTransform(idea, bigtxt))
        self.wait(1.3)

        self.clear_scene()


# ========================================================================
#  Scene 02 — 引理 4.3.1
# ========================================================================
class Scene02_Lemma(BaseScene):
    part_index = 2
    subtitle = "引理 4.3.1"

    def construct(self):
        head = self.add_header()
        tag = self.banner("引理 4.3.1", C_LEMMA)
        tag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag, shift=DOWN * 0.2))

        headline = ct("线性映射由「基向量的像」完全确定", size=29, color=TXT, weight=BOLD)
        headline.next_to(tag, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(headline, shift=DOWN * 0.15))
        self.wait(0.4)

        setup1 = ct("设 V, U 是数域 K 上的线性空间", size=24, color=GREY)
        setup2 = VGroup(
            ct("V 的一组基为", size=24, color=GREY),
            eq(r"\{e_1,e_2,\ldots,e_n\}", size=27, color=GREY),
        ).arrange(RIGHT, buff=0.15)
        setupg = VGroup(setup1, setup2).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        setupg.next_to(headline, DOWN, buff=0.35).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(setupg, shift=DOWN * 0.1))
        self.wait(0.5)

        # ---- (1) ----
        p1_head = mixed("(1)  若两个线性映射在基上取值相同……", size=25, color=TXT)
        p1_eq = eq(r"\psi(e_i)=\varphi(e_i)\quad (i=1,2,\ldots,n)", size=32, color=C_LEMMA)
        p1_res = VGroup(
            ct("则它们处处相等：", size=25, color=TXT),
            eq(r"\psi=\varphi", size=32, color=GOLD),
        ).arrange(RIGHT, buff=0.2)
        p1 = VGroup(p1_head, p1_eq, p1_res).arrange(DOWN, buff=0.22)
        p1.next_to(setupg, DOWN, buff=0.45).to_edge(LEFT, buff=0.85)

        self.play(FadeIn(p1_head, shift=DOWN * 0.1))
        self.play(Write(p1_eq))
        self.wait(0.3)
        self.play(FadeIn(p1_res, shift=DOWN * 0.1))
        self.wait(1.0)

        # ---- (2) ----
        p2_head = mixed("(2)  任意指定基向量的像……", size=25, color=TXT)
        p2_eq = VGroup(
            eq(r"\beta_1,\beta_2,\ldots,\beta_n\in U", size=30, color=C_LEMMA),
        )
        p2_res = VGroup(
            mixed("就存在唯一的线性映射 φ 使得", size=25, color=TXT),
            eq(r"\varphi(e_i)=\beta_i", size=30, color=GOLD),
        ).arrange(RIGHT, buff=0.2)
        p2 = VGroup(p2_head, p2_eq, p2_res).arrange(DOWN, buff=0.22)
        p2.next_to(p1, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)

        self.play(FadeIn(p2_head, shift=DOWN * 0.1))
        self.play(Write(p2_eq[0]))
        self.wait(0.2)
        self.play(FadeIn(p2_res, shift=DOWN * 0.1))
        self.wait(1.2)

        self.clear_scene()

        # ============== 几何演示 ==============
        head = self.add_header()
        demo_title = ct("几何演示：像由基的像唯一确定", size=27, color=TXT, weight=BOLD)
        demo_title.next_to(head, DOWN, buff=0.5)
        self.play(FadeIn(demo_title, shift=DOWN * 0.15))

        # 左侧: V 平面, 基 e1 e2, 向量 alpha
        plane1 = NumberPlane(
            x_range=[-1, 4, 1], y_range=[-1, 3, 1], x_length=5.0, y_length=3.6,
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.35},
        ).shift(LEFT * 3.5 + DOWN * 0.9)
        plabel1 = eq("V", size=30, color=C_V).next_to(plane1, UP, buff=0.15).align_to(plane1, LEFT)

        lam1, lam2 = 1.3, 1.1
        e1_data, e2_data = (1.6, 0), (0, 1.2)
        origin1 = plane1.coords_to_point(0, 0)
        e1_tip = plane1.coords_to_point(*e1_data)
        e2_tip = plane1.coords_to_point(*e2_data)
        alpha_tip = plane1.coords_to_point(lam1 * e1_data[0] + lam2 * e2_data[0],
                                            lam1 * e1_data[1] + lam2 * e2_data[1])

        e1_arrow = Arrow(origin1, e1_tip, buff=0, color=C_V, stroke_width=5)
        e2_arrow = Arrow(origin1, e2_tip, buff=0, color=C_V, stroke_width=5)
        e1_lab = eq("e_1", size=26, color=C_V).next_to(e1_arrow, DOWN, buff=0.1)
        e2_lab = eq("e_2", size=26, color=C_V).next_to(e2_arrow, LEFT, buff=0.1)

        dash_a = DashedLine(plane1.coords_to_point(lam1 * e1_data[0], lam1 * e1_data[1]),
                             alpha_tip, color=GREY, stroke_width=2)
        dash_b = DashedLine(plane1.coords_to_point(lam2 * e2_data[0], lam2 * e2_data[1]),
                             alpha_tip, color=GREY, stroke_width=2)
        alpha_arrow = Arrow(origin1, alpha_tip, buff=0, color=GOLD, stroke_width=5)
        alpha_lab = eq(r"\alpha=\lambda_1e_1+\lambda_2e_2", size=22, color=GOLD)
        alpha_lab.next_to(alpha_arrow.get_end(), UP, buff=0.12)

        self.play(Create(plane1), Write(plabel1))
        self.play(GrowArrow(e1_arrow), GrowArrow(e2_arrow), Write(e1_lab), Write(e2_lab))
        self.wait(0.3)
        self.play(Create(dash_a), Create(dash_b))
        self.play(GrowArrow(alpha_arrow), Write(alpha_lab))
        self.wait(0.6)

        # 右侧: U 平面, beta1 beta2 任意给定, phi(alpha) 被迫确定
        plane2 = NumberPlane(
            x_range=[-1, 4, 1], y_range=[-1, 3, 1], x_length=5.0, y_length=3.6,
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.35},
        ).shift(RIGHT * 3.5 + DOWN * 0.9)
        plabel2 = eq("U", size=30, color=C_U).next_to(plane2, UP, buff=0.15).align_to(plane2, LEFT)

        origin2 = plane2.coords_to_point(0, 0)
        b1_data, b2_data = (0.8, 1.6), (1.8, 0.3)
        b1_tip = plane2.coords_to_point(*b1_data)
        b2_tip = plane2.coords_to_point(*b2_data)

        b1_arrow = Arrow(origin2, b1_tip, buff=0, color=C_U, stroke_width=5)
        b2_arrow = Arrow(origin2, b2_tip, buff=0, color=C_U, stroke_width=5)
        b1_lab = eq(r"\beta_1=\varphi(e_1)", size=20, color=C_U).next_to(b1_arrow.get_end(), UP, buff=0.08)
        b2_lab = eq(r"\beta_2=\varphi(e_2)", size=20, color=C_U).next_to(b2_arrow.get_end(), DOWN, buff=0.08)

        self.play(Create(plane2), Write(plabel2))
        self.play(GrowArrow(b1_arrow), Write(b1_lab))
        self.play(GrowArrow(b2_arrow), Write(b2_lab))
        self.wait(0.5)

        forced = mixed("φ(e₁), φ(e₂) 一旦给定 ……", size=24, color=TXT)
        forced.next_to(VGroup(plane1, plane2), DOWN, buff=0.55)
        self.play(FadeIn(forced, shift=UP * 0.15))
        self.wait(0.6)

        phi_alpha_data = (lam1 * b1_data[0] + lam2 * b2_data[0],
                           lam1 * b1_data[1] + lam2 * b2_data[1])
        phi_alpha_tip = plane2.coords_to_point(*phi_alpha_data)
        dash_c = DashedLine(plane2.coords_to_point(lam1 * b1_data[0], lam1 * b1_data[1]),
                             phi_alpha_tip, color=GREY, stroke_width=2)
        dash_d = DashedLine(plane2.coords_to_point(lam2 * b2_data[0], lam2 * b2_data[1]),
                             phi_alpha_tip, color=GREY, stroke_width=2)
        phi_alpha_arrow = Arrow(origin2, phi_alpha_tip, buff=0, color=GOLD, stroke_width=5)
        phi_alpha_lab = eq(r"\varphi(\alpha)=\lambda_1\beta_1+\lambda_2\beta_2", size=20, color=GOLD)
        phi_alpha_lab.next_to(phi_alpha_arrow.get_end(), UP, buff=0.12)
        fit_width(phi_alpha_lab, 3.4)

        forced2 = mixed("φ(α) 就被『强行』唯一确定了！", size=26, color=GOLD, weight=BOLD)
        forced2.move_to(forced)

        self.play(Create(dash_c), Create(dash_d))
        self.play(GrowArrow(phi_alpha_arrow), Write(phi_alpha_lab))
        self.play(ReplacementTransform(forced, forced2))
        self.wait(1.3)

        self.clear_scene()

        # ============== 严格证明 ==============
        head = self.add_header()
        ptag = self.proof_label()
        ptag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(ptag, shift=DOWN * 0.2))

        part1lab = ct("(1)  唯一性的证明", size=26, color=TXT, weight=BOLD)
        part1lab.next_to(ptag, DOWN, buff=0.35).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(part1lab, shift=DOWN * 0.1))

        given = VGroup(
            ct("任取 ", size=23, color=GREY), eq(r"\alpha\in V", size=25, color=GREY),
            ct("，设 ", size=23, color=GREY),
            eq(r"\alpha=\lambda_1e_1+\lambda_2e_2+\cdots+\lambda_ne_n", size=22, color=GREY),
        ).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        fit_width(given, 12.3)
        given.next_to(part1lab, DOWN, buff=0.3).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(given, shift=DOWN * 0.1))

        lines = VGroup(
            eq(r"\psi(\alpha) = \psi(\lambda_1e_1+\cdots+\lambda_ne_n)"),
            eq(r"= \lambda_1\psi(e_1)+\cdots+\lambda_n\psi(e_n)"),
            eq(r"= \lambda_1\varphi(e_1)+\cdots+\lambda_n\varphi(e_n)"),
            eq(r"= \varphi(\lambda_1e_1+\cdots+\lambda_ne_n) = \varphi(\alpha)"),
        )
        for l in lines:
            l.scale(0.85)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        lines.next_to(given, DOWN, buff=0.35).to_edge(LEFT, buff=1.3)

        reasons = [
            "（α 的坐标展开）",
            "（ψ 是线性映射）",
            "（已知 ψ(eᵢ)=φ(eᵢ)）",
            "（φ 是线性映射，逆向合并）",
        ]
        self.play(Write(lines[0]))
        for i in range(1, 4):
            r = mixed(reasons[i], size=19, color=GREY)
            r.next_to(lines[i], RIGHT, buff=0.35)
            self.play(Write(lines[i]), FadeIn(r, shift=LEFT * 0.1))
            self.wait(0.25)

        concl = VGroup(
            mixed("对一切 α 成立，故", size=23, color=TXT),
            eq(r"\psi=\varphi", size=30, color=GOLD),
        ).arrange(RIGHT, buff=0.2)
        concl.next_to(lines, DOWN, buff=0.4).to_edge(LEFT, buff=1.3)
        qed = self.qed_mark().next_to(concl, RIGHT, buff=0.25)
        self.play(FadeIn(concl, shift=DOWN * 0.1), FadeIn(qed))
        self.wait(1.2)

        self.clear_scene()

        # (2) existence + uniqueness sketch
        head = self.add_header()
        ptag = self.proof_label()
        ptag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        part2lab = ct("(2)  存在唯一性的证明", size=26, color=TXT, weight=BOLD)
        part2lab.next_to(ptag, DOWN, buff=0.35).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(ptag, shift=DOWN * 0.2), FadeIn(part2lab, shift=DOWN * 0.1))

        exist_lab = self.banner("存在性", C_LEMMA, size=22)
        exist_lab.next_to(part2lab, DOWN, buff=0.35).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(exist_lab))

        define_eq = VGroup(
            ct("定义：", size=23, color=TXT),
            eq(r"\varphi(\alpha):=\lambda_1\beta_1+\lambda_2\beta_2+\cdots+\lambda_n\beta_n", size=28, color=C_LEMMA),
        ).arrange(RIGHT, buff=0.2)
        define_eq.next_to(exist_lab, DOWN, buff=0.3).to_edge(LEFT, buff=1.1)
        fit_width(define_eq, 11.5)
        self.play(FadeIn(define_eq, shift=DOWN * 0.1))
        self.wait(0.4)

        check1 = mixed("✓ 良定义：α 的坐标 (λ₁,…,λₙ) 由基的唯一性保证", size=21, color=GREY)
        check2 = mixed("✓ 线性：直接由定义验证 φ(α+α′)=φ(α)+φ(α′)，φ(kα)=kφ(α)", size=21, color=GREY)
        check3 = mixed("✓ 代入 eᵢ 本身的坐标，得 φ(eᵢ)=βᵢ，正是所要求的", size=21, color=GREY)
        checks = VGroup(check1, check2, check3).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        checks.next_to(define_eq, DOWN, buff=0.35).to_edge(LEFT, buff=1.1)
        for c in checks:
            self.play(FadeIn(c, shift=DOWN * 0.08))
            self.wait(0.2)
        self.wait(0.5)

        uniq_lab = self.banner("唯一性", C_LEMMA, size=22)
        uniq_lab.next_to(checks, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        uniq_txt = ct("由 (1) 立即得到。", size=23, color=TXT)
        uniq_txt.next_to(uniq_lab, RIGHT, buff=0.3)
        qed2 = self.qed_mark().next_to(uniq_txt, RIGHT, buff=0.3)
        self.play(FadeIn(uniq_lab), FadeIn(uniq_txt, shift=DOWN*0.1), FadeIn(qed2))
        self.wait(1.4)

        self.clear_scene()


# ========================================================================
#  Scene 03 — 表示矩阵的构造  (4.3.1)-(4.3.2) 式
# ========================================================================
class Scene03_BuildMatrix(BaseScene):
    part_index = 3
    subtitle = "表示矩阵的构造"

    def construct(self):
        head = self.add_header()

        setup = VGroup(
            ct("设", size=24, color=GREY), eq("V", size=27, color=C_V),
            ct("是", size=24, color=GREY), eq("n", size=27, color=GREY),
            ct("维，基为", size=24, color=GREY), eq(r"\{e_1,\ldots,e_n\}", size=27, color=C_V),
            ct("；", size=24, color=GREY), eq("U", size=27, color=C_U),
            ct("是", size=24, color=GREY), eq("m", size=27, color=GREY),
            ct("维，基为", size=24, color=GREY), eq(r"\{f_1,\ldots,f_m\}", size=27, color=C_U),
        ).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        fit_width(setup, 12.6)
        setup.next_to(head, DOWN, buff=0.55)
        self.play(FadeIn(setup, shift=DOWN * 0.15))
        self.wait(0.5)

        ask = mixed("问题：φ(α) 在基 {f₁,…,fₘ} 下的坐标是什么？", size=26, color=GOLD, weight=BOLD)
        ask.next_to(setup, DOWN, buff=0.45)
        self.play(FadeIn(ask, shift=DOWN * 0.15))
        self.wait(0.9)
        self.play(FadeOut(ask))

        tag431 = self.banner("(4.3.1) 式：基向量的像", C_DEF, size=22)
        tag431.next_to(setup, DOWN, buff=0.45).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag431))

        sys_lines = VGroup(
            eq(r"\varphi(e_1) = a_{11}f_1+a_{12}f_2+\cdots+a_{1m}f_m"),
            eq(r"\varphi(e_2) = a_{21}f_1+a_{22}f_2+\cdots+a_{2m}f_m"),
            eq(r"\vdots"),
            eq(r"\varphi(e_n) = a_{n1}f_1+a_{n2}f_2+\cdots+a_{nm}f_m"),
        )
        for l in sys_lines:
            l.scale(0.74)
        sys_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        sys_lines.next_to(tag431, DOWN, buff=0.3).to_edge(LEFT, buff=1.0)

        self.play(Write(sys_lines[0]))
        self.play(Write(sys_lines[1]))
        self.play(Write(sys_lines[2]))
        self.play(Write(sys_lines[3]))
        self.wait(0.7)

        key = mixed("关键想法：把 φ(eᵢ) 的坐标 (aᵢ₁,…,aᵢₘ) 竖着排成一列！", size=23, color=GOLD)
        fit_width(key, 12.3)
        key.next_to(sys_lines, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(key, shift=DOWN * 0.15))
        self.wait(1.1)

        self.clear_scene()

        # ---------- 组装矩阵 A ----------
        head = self.add_header()
        tag = self.banner("把系数『竖着』排列 → 矩阵 A", C_DEF, size=22)
        tag.next_to(head, DOWN, buff=0.5)
        self.play(FadeIn(tag))

        A = Matrix(
            [
                ["a_{11}", "a_{21}", r"\cdots", "a_{n1}"],
                ["a_{12}", "a_{22}", r"\cdots", "a_{n2}"],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                ["a_{1m}", "a_{2m}", r"\cdots", "a_{nm}"],
            ],
            left_bracket="(", right_bracket=")",
            element_to_mobject_config={"font_size": 30, "color": TXT},
        )
        Alab = VGroup(eq("A", size=34, color=C_A), eq("=", size=34, color=TXT)).arrange(RIGHT, buff=0.15)
        Amat = VGroup(Alab, A).arrange(RIGHT, buff=0.25)
        Amat.next_to(tag, DOWN, buff=0.5)

        self.play(Write(Amat))
        self.wait(0.4)

        col1 = A.get_columns()[0]
        note1 = mixed("第 1 列 = φ(e₁) 的坐标向量", size=22, color=C_A)
        note1.next_to(Amat, DOWN, buff=0.5)
        box1 = SurroundingRectangle(col1, color=C_A, buff=0.12, corner_radius=0.08)
        self.play(Create(box1), FadeIn(note1, shift=UP * 0.1))
        self.wait(0.8)

        col2 = A.get_columns()[1]
        box2 = SurroundingRectangle(col2, color=C_U, buff=0.12, corner_radius=0.08)
        note2 = mixed("第 2 列 = φ(e₂) 的坐标向量", size=22, color=C_U)
        note2.move_to(note1)
        self.play(Transform(box1, box2), ReplacementTransform(note1, note2))
        self.wait(0.6)

        coln = A.get_columns()[3]
        boxn = SurroundingRectangle(coln, color=GOLD, buff=0.12, corner_radius=0.08)
        noten = mixed("第 i 列 = φ(eᵢ) 的坐标向量", size=22, color=GOLD, weight=BOLD)
        noten.move_to(note1)
        self.play(Transform(box1, boxn), ReplacementTransform(note2, noten))
        self.wait(1.2)

        self.play(FadeOut(box1), FadeOut(noten))
        self.wait(0.2)

        deftxt = mixed("这个 m×n 矩阵 A，就称为 φ 在给定基下的『表示矩阵』", size=24, color=TXT)
        fit_width(deftxt, 12.3)
        deftxt.next_to(Amat, DOWN, buff=0.5)
        self.play(FadeIn(deftxt, shift=DOWN * 0.15))
        self.wait(1.2)

        self.clear_scene()

        # ---------- 推导 (4.3.2) ----------
        head = self.add_header()
        tag2 = self.banner("(4.3.2) 式：坐标变换公式", C_DEF, size=22)
        tag2.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag2))

        given = VGroup(
            ct("设", size=23, color=GREY),
            eq(r"\alpha=\lambda_1e_1+\lambda_2e_2+\cdots+\lambda_ne_n", size=27, color=GREY),
        ).arrange(RIGHT, buff=0.15)
        given.next_to(tag2, DOWN, buff=0.3).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(given, shift=DOWN * 0.1))

        deriv1 = eq(r"\varphi(\alpha)=\lambda_1\varphi(e_1)+\lambda_2\varphi(e_2)+\cdots+\lambda_n\varphi(e_n)", size=28)
        deriv2 = eq(r"=\Big(\sum_{i=1}^n \lambda_i a_{i1}\Big)f_1+\Big(\sum_{i=1}^n\lambda_i a_{i2}\Big)f_2+\cdots+\Big(\sum_{i=1}^n\lambda_i a_{im}\Big)f_m", size=22)
        derivg = VGroup(deriv1, deriv2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fit_width(derivg, 12.3)
        derivg.next_to(given, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)

        self.play(Write(deriv1))
        self.wait(0.3)
        self.play(Write(deriv2))
        self.wait(0.8)

        concl = VGroup(
            mixed("即 φ(α) 的第 j 个坐标为", size=23, color=TXT),
            eq(r"\mu_j=\sum_{i=1}^n a_{ij}\lambda_i", size=28, color=GOLD),
        ).arrange(RIGHT, buff=0.2)
        concl.next_to(derivg, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(concl, shift=DOWN * 0.1))
        self.wait(1.1)

        self.clear_scene()

        # ---------- (4.3.2) 矩阵形式 ----------
        head = self.add_header()
        formula_title = ct("(4.3.2) 式：坐标的矩阵形式", size=27, color=TXT, weight=BOLD)
        formula_title.next_to(head, DOWN, buff=0.55)
        self.play(FadeIn(formula_title, shift=DOWN * 0.15))

        mu_vec = mat([["\\mu_1"], ["\\mu_2"], [r"\vdots"], ["\\mu_m"]], size=28)
        lam_vec = mat([["\\lambda_1"], ["\\lambda_2"], [r"\vdots"], ["\\lambda_n"]], size=28)
        Amat2 = Matrix(
            [
                ["a_{11}", "a_{21}", r"\cdots", "a_{n1}"],
                ["a_{12}", "a_{22}", r"\cdots", "a_{n2}"],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                ["a_{1m}", "a_{2m}", r"\cdots", "a_{nm}"],
            ],
            left_bracket="(", right_bracket=")",
            element_to_mobject_config={"font_size": 26, "color": C_A},
        )
        eqsign = eq("=", size=36)
        formula = VGroup(mu_vec, eqsign, Amat2, lam_vec).arrange(RIGHT, buff=0.3)
        fit_width(formula, 12.0)
        formula.move_to(ORIGIN).shift(DOWN * 0.3)

        self.play(Write(mu_vec))
        self.play(Write(eqsign))
        self.play(Write(Amat2))
        self.play(Write(lam_vec))
        self.wait(0.8)

        boxall = SurroundingRectangle(formula, color=GOLD, buff=0.3, corner_radius=0.15)
        label43_2 = ct("(4.3.2)", size=20, color=GOLD).next_to(boxall, RIGHT, buff=0.2)
        self.play(Create(boxall), Write(label43_2))
        self.wait(1.3)

        self.clear_scene()

        # ---------- 转置 注解 ----------
        head = self.add_header()
        note_title = ct("注：A 恰好是 (4.3.1) 式系数表的『转置』", size=26, color=TXT, weight=BOLD)
        note_title.next_to(head, DOWN, buff=0.55)
        self.play(FadeIn(note_title, shift=DOWN * 0.15))

        coeftab = Matrix(
            [
                ["a_{11}", "a_{12}", r"\cdots", "a_{1m}"],
                ["a_{21}", "a_{22}", r"\cdots", "a_{2m}"],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                ["a_{n1}", "a_{n2}", r"\cdots", "a_{nm}"],
            ],
            left_bracket="(", right_bracket=")",
            element_to_mobject_config={"font_size": 24, "color": GREY},
        )
        coeftab_lab = mixed("(4.3.1) 系数表  (n×m)", size=19, color=GREY)
        coefg = VGroup(coeftab, coeftab_lab).arrange(DOWN, buff=0.25)
        coefg.shift(LEFT * 3.4 + DOWN * 0.5)

        arrow_t = Arrow(LEFT * 0.85, RIGHT * 0.85, color=GOLD, stroke_width=4)
        arrow_lab = ct("转置", size=22, color=GOLD).next_to(arrow_t, UP, buff=0.1)
        arrowg = VGroup(arrow_t, arrow_lab).move_to(ORIGIN).shift(DOWN * 0.5)

        Amat3 = Matrix(
            [
                ["a_{11}", "a_{21}", r"\cdots", "a_{n1}"],
                ["a_{12}", "a_{22}", r"\cdots", "a_{n2}"],
                [r"\vdots", r"\vdots", r"\ddots", r"\vdots"],
                ["a_{1m}", "a_{2m}", r"\cdots", "a_{nm}"],
            ],
            left_bracket="(", right_bracket=")",
            element_to_mobject_config={"font_size": 24, "color": C_A},
        )
        Amat3_lab = mixed("表示矩阵 A  (m×n)", size=19, color=C_A)
        Amat3g = VGroup(Amat3, Amat3_lab).arrange(DOWN, buff=0.25)
        Amat3g.shift(RIGHT * 3.4 + DOWN * 0.5)

        self.play(FadeIn(coefg, shift=RIGHT * 0.2))
        self.play(GrowArrow(arrow_t), Write(arrow_lab))
        self.play(FadeIn(Amat3g, shift=LEFT * 0.2))
        self.wait(1.6)

        self.clear_scene()


# ========================================================================
#  Scene 04 — 定义：表示矩阵
# ========================================================================
class Scene04_Definition(BaseScene):
    part_index = 4
    subtitle = "定义：表示矩阵"

    def construct(self):
        head = self.add_header()
        tag = self.banner("定义 4.3", C_DEF)
        tag.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag, shift=DOWN * 0.2))

        defn = mixed("矩阵 A 称为 φ 在基 {e₁,…,eₙ} 与 {f₁,…,fₘ} 下的『表示矩阵』", size=26, color=TXT)
        fit_width(defn, 12.3)
        defn.next_to(tag, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(defn, shift=DOWN * 0.15))
        self.wait(0.7)

        notation = VGroup(
            ct("记号：", size=25, color=GREY),
            eq(r"T(\varphi) = A", size=34, color=GOLD),
        ).arrange(RIGHT, buff=0.25)
        notation.next_to(defn, DOWN, buff=0.5)
        self.play(Write(notation))
        self.wait(0.8)

        Tmap = eq(r"T:\ \mathcal{L}(V,U)\ \longrightarrow\ M_{m\times n}(\mathbb{K})", size=32, color=TXT)
        Tmap.next_to(notation, DOWN, buff=0.55)
        self.play(Write(Tmap))
        self.wait(0.6)

        remark = mixed("φ 取定基后，就被一个矩阵『编码』了", size=26, color=C_DEF)
        remark.next_to(Tmap, DOWN, buff=0.5)
        self.play(FadeIn(remark, shift=DOWN * 0.15))
        self.wait(1.3)

        self.clear_scene()


# ========================================================================
#  Scene 05 — 定理 4.3.1：T 是线性同构 + 交换图
# ========================================================================
class Scene05_Theorem1(BaseScene):
    part_index = 5
    subtitle = "定理 4.3.1"

    def construct(self):
        head = self.add_header()
        tag = self.banner("定理 4.3.1", C_THM)
        tag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag, shift=DOWN*0.2))

        pre_txt = VGroup(
            ct("设 ", size=25, color=TXT),
            eq(r"T: L(V,U) \to M_{m\times n}(K)", size=24, color=GOLD),
            ct(" 是按以上方式定义的映射，则：", size=25, color=TXT),
        ).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
        fit_width(pre_txt, 12.3)
        pre_txt.next_to(tag, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(pre_txt, shift=DOWN*0.1))

        c1 = VGroup(
            ct("(1)  T 是线性同构，即", size=24, color=TXT),
            eq(r"\mathcal{L}(V,U)\cong M_{m\times n}(\mathbb{K})", size=27, color=GOLD),
        ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        c1.next_to(pre_txt, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        fit_width(c1, 12.3)

        c2 = VGroup(
            ct("(2)  交换图成立：", size=24, color=TXT),
            eq(r"\eta_2\circ\varphi=\varphi_A\circ\eta_1", size=27, color=GOLD),
        ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        c2.next_to(c1, DOWN, buff=0.35).to_edge(LEFT, buff=1.0)
        fit_width(c2, 12.3)

        self.play(FadeIn(c1, shift=DOWN*0.1))
        self.play(FadeIn(c2, shift=DOWN*0.1))
        self.wait(1.2)
        self.clear_scene()

        # ---- Commutative diagram ----
        head = self.add_header()
        diag_ttl = ct("交换图（图 4.1）", size=28, color=GOLD, weight=BOLD)
        diag_ttl.next_to(head, DOWN, buff=0.5)
        self.play(Write(diag_ttl))

        VP   = np.array([-3.6,  1.1, 0])
        UP2  = np.array([ 3.6,  1.1, 0])
        KnP  = np.array([-3.6, -1.6, 0])
        KmP  = np.array([ 3.6, -1.6, 0])

        V_m   = eq("V",              size=44, color=C_V).move_to(VP)
        U_m   = eq("U",              size=44, color=C_U).move_to(UP2)
        Kn_m  = eq(r"\mathbb{K}^n", size=34, color=C_V).move_to(KnP)
        Km_m  = eq(r"\mathbb{K}^m", size=34, color=C_U).move_to(KmP)

        phi_a  = Arrow(VP  + RIGHT*0.40, UP2 + LEFT*0.40, buff=0, color=TXT,  stroke_width=4)
        phiA_a = Arrow(KnP + RIGHT*0.90, KmP + LEFT*0.90, buff=0, color=GOLD, stroke_width=4)
        eta1_a = Arrow(VP  + DOWN*0.35,  KnP + UP*0.38,   buff=0, color=C_V,  stroke_width=4)
        eta2_a = Arrow(UP2 + DOWN*0.35,  KmP + UP*0.38,   buff=0, color=C_U,  stroke_width=4)

        phi_l  = eq(r"\varphi",   size=30, color=TXT ).next_to(phi_a,  UP,    buff=0.1)
        phiA_l = eq(r"\varphi_A", size=30, color=GOLD).next_to(phiA_a, DOWN,  buff=0.1)
        eta1_l = eq(r"\eta_1",    size=28, color=C_V ).next_to(eta1_a, LEFT,  buff=0.1)
        eta2_l = eq(r"\eta_2",    size=28, color=C_U ).next_to(eta2_a, RIGHT, buff=0.1)

        self.play(FadeIn(V_m), FadeIn(U_m), FadeIn(Kn_m), FadeIn(Km_m))
        self.play(GrowArrow(phi_a), Write(phi_l))
        self.play(GrowArrow(eta1_a), Write(eta1_l),
                  GrowArrow(eta2_a), Write(eta2_l))
        self.play(GrowArrow(phiA_a), Write(phiA_l))
        self.wait(0.8)

        p1t = VGroup(ct("路径(1): ", size=22, color=C_U), eq(r"\varphi \to \eta_2", size=24, color=C_U)).arrange(RIGHT, buff=0.1).to_corner(DL, buff=0.5)
        p2t = VGroup(ct("路径(2): ", size=22, color=C_V), eq(r"\eta_1 \to \varphi_A", size=24, color=C_V)).arrange(RIGHT, buff=0.1).to_corner(DR, buff=0.5)
        self.play(phi_a.animate.set_color(C_U), eta2_a.animate.set_color(C_U), FadeIn(p1t))
        self.wait(0.5)
        self.play(phi_a.animate.set_color(TXT), eta2_a.animate.set_color(C_U))
        self.play(eta1_a.animate.set_color(C_V), phiA_a.animate.set_color(C_V), FadeIn(p2t))
        self.wait(0.6)
        eqtxt = ct("两条路径结果相同", size=26, color=GOLD, weight=BOLD).to_edge(DOWN, buff=0.65)
        self.play(FadeIn(eqtxt, shift=UP*0.2))
        self.wait(1.3)
        self.clear_scene()

        # ---- Proof sketch ----
        head = self.add_header()
        ptag = self.proof_label()
        ptag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(ptag))

        lintag = self.banner("T 是线性映射", C_LEMMA, size=22)
        lintag.next_to(ptag, DOWN, buff=0.25).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(lintag))

        l1 = eq(r"(\varphi+\psi)(e_i)=\varphi(e_i)+\psi(e_i)\ \Rightarrow\ T(\varphi+\psi)=A+B=T(\varphi)+T(\psi)", size=22)
        l2 = eq(r"(k\varphi)(e_i)=k\varphi(e_i)\ \Rightarrow\ T(k\varphi)=kA=kT(\varphi)", size=22)
        l1.scale(0.72).next_to(lintag, DOWN, buff=0.18).to_edge(LEFT, buff=1.0)
        fit_width(l1, 12.0)
        l2.scale(0.72).next_to(l1, DOWN, buff=0.15).to_edge(LEFT, buff=1.0)
        fit_width(l2, 12.0)
        self.play(Write(l1)); self.wait(0.3)
        self.play(Write(l2)); self.wait(0.5)

        bijtag = self.banner("T 是双射（线性同构）", C_THM, size=22)
        bijtag.next_to(l2, DOWN, buff=0.25).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(bijtag))

        inj_line1 = VGroup(self.banner("单射", C_LEMMA, size=18),
                     eq(r"T(\varphi)=0 \Rightarrow \varphi(e_i)=0\ (\forall i)", size=16, color=TXT))
        inj_line1.arrange(RIGHT, buff=0.3)
        fit_width(inj_line1, 12.3)
        inj_line2 = VGroup(ct("由引理4.3.1(1) 得 ", size=18, color=TXT),
                           eq(r"\varphi=0", size=20, color=GOLD))
        inj_line2.arrange(RIGHT, buff=0.1)
        fit_width(inj_line2, 10.0)
        inj_line2.next_to(inj_line1, DOWN, buff=0.08).align_to(inj_line1, LEFT)
        inj = VGroup(inj_line1, inj_line2)
        inj.next_to(bijtag, DOWN, buff=0.15)

        sur_line1 = VGroup(self.banner("满射", C_THM, size=18),
                     ct("任意 A 由引理4.3.1(2)", size=18, color=TXT))
        sur_line1.arrange(RIGHT, buff=0.3)
        fit_width(sur_line1, 12.3)
        sur_line2 = VGroup(ct("唯一对应 ", size=18, color=TXT),
                           eq(r"\varphi", size=20, color=GOLD),
                           ct(" 使 ", size=18, color=TXT),
                           eq(r"T(\varphi)=A", size=20, color=GOLD))
        sur_line2.arrange(RIGHT, buff=0.1)
        fit_width(sur_line2, 10.0)
        sur_line2.next_to(sur_line1, DOWN, buff=0.08).align_to(sur_line1, LEFT)
        sur = VGroup(sur_line1, sur_line2)
        sur.next_to(inj, DOWN, buff=0.15)

        qed = self.qed_mark().next_to(sur, RIGHT, buff=0.28)
        self.play(FadeIn(inj, shift=DOWN*0.1))
        self.play(FadeIn(sur, shift=DOWN*0.1), FadeIn(qed))
        self.wait(1.4)
        self.clear_scene()


# ========================================================================
#  Scene 06 — 定理 4.3.2：矩阵乘法 = 映射复合
# ========================================================================
class Scene06_Theorem2(BaseScene):
    part_index = 6
    subtitle = "定理 4.3.2"

    def construct(self):
        head = self.add_header()
        tag = self.banner("定理 4.3.2", C_THM)
        tag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag))

        pre = VGroup(
            ct("再设 W 是 K 上线性空间，{", size=24, color=TXT),
            eq(r"g_1,\ldots,g_p", size=26, color=GREY),
            ct("} 是 W 的一组基，", size=24, color=TXT),
            eq(r"\psi\in L(U,W)", size=26, color=GREY),
        ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        fit_width(pre, 12.3)
        pre.next_to(tag, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(pre, shift=DOWN*0.1))

        chain_diag = VGroup(
            eq("V", size=38, color=C_V),
            eq(r"\xrightarrow{\ \varphi\ }", size=32, color=TXT),
            eq("U", size=38, color=C_U),
            eq(r"\xrightarrow{\ \psi\ }", size=32, color=TXT),
            eq("W", size=38, color=C_W),
        ).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        chain_diag.next_to(pre, DOWN, buff=0.5)
        self.play(FadeIn(chain_diag, shift=DOWN*0.1))
        self.wait(0.6)

        result_lhs = eq(r"T(\psi\varphi)", size=36, color=GOLD)
        result_eq1 = eq(r"=\ T(\psi)\,T(\varphi)", size=36, color=GOLD)
        result_eq2 = eq(r"=\ BA", size=36, color=C_A)
        result_row = VGroup(result_lhs, result_eq1, result_eq2).arrange(RIGHT, buff=0.2)
        result_row.next_to(chain_diag, DOWN, buff=0.55)
        box = SurroundingRectangle(result_row, color=GOLD, buff=0.3, corner_radius=0.15)
        self.play(Write(result_lhs)); self.wait(0.2)
        self.play(Write(result_eq1)); self.wait(0.2)
        self.play(Write(result_eq2), Create(box))
        self.wait(0.8)

        key = mixed("矩阵乘法 BA 的几何意义：先做 φ，再做 ψ", size=27, color=C_DEF, weight=BOLD)
        fit_width(key, 12.3)
        key.next_to(box, DOWN, buff=0.5)
        self.play(FadeIn(key, shift=DOWN*0.15))
        self.wait(1.3)
        self.clear_scene()

        # Proof
        head = self.add_header()
        ptag = self.proof_label()
        ptag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(ptag))

        coord_label = mixed("设 α 在 V 的基 {e} 下坐标列向量为 λ", size=24, color=GREY)
        coord_label.next_to(ptag, DOWN, buff=0.35).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(coord_label, shift=DOWN*0.1))

        steps = VGroup(
            VGroup(ct("(1) ", size=23, color=TXT), mixed("φ(α) 在 {f} 下坐标：", size=23, color=TXT),
                   eq(r"\mu = A\lambda", size=28, color=C_A)).arrange(RIGHT, buff=0.15),
            VGroup(ct("(2) ", size=23, color=TXT), mixed("ψ(φ(α)) 在 {g} 下坐标：", size=23, color=TXT),
                   eq(r"\xi = B\mu = B(A\lambda) = BA\lambda", size=28, color=C_B)).arrange(RIGHT, buff=0.15),
            VGroup(ct("(3) ", size=23, color=TXT), mixed("故 ψ∘φ 的表示矩阵为", size=23, color=TXT),
                   eq(r"BA = T(\psi)T(\varphi)", size=28, color=GOLD)).arrange(RIGHT, buff=0.15),
        )
        for s in steps:
            fit_width(s, 12.0)
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        steps.next_to(coord_label, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)

        for i, s in enumerate(steps):
            self.play(FadeIn(s, shift=DOWN*0.1))
            self.wait(0.4)

        concl = VGroup(
            mixed("∴", size=25, color=TXT),
            eq(r"T(\psi\varphi)=T(\psi)T(\varphi)", size=30, color=GOLD),
        ).arrange(RIGHT, buff=0.3)
        concl.next_to(steps, DOWN, buff=0.45).to_edge(LEFT, buff=1.0)
        qed = self.qed_mark().next_to(concl, RIGHT, buff=0.3)
        self.play(FadeIn(concl, shift=DOWN*0.1), FadeIn(qed))
        self.wait(1.3)
        self.clear_scene()


# ========================================================================
#  Scene 07 — L(V) 情形 + 定理 4.3.3 + 推论 4.3.1
# ========================================================================
class Scene07_LVCase(BaseScene):
    part_index = 7
    subtitle = "L(V) 与定理 4.3.3"

    def construct(self):
        head = self.add_header()

        # Setup: special case V=U
        setup_banner = self.banner("特殊情形：V = U，取同一组基", C_DEF, size=22)
        setup_banner.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(setup_banner, shift=DOWN*0.2))

        setup_txt = VGroup(
            ct("此时考察 V 上的全体线性变换空间 ", size=24, color=TXT),
            eq(r"L(V)", size=27, color=GOLD),
            ct("，以及 n 阶矩阵空间 ", size=24, color=TXT),
            eq(r"M_n(K)", size=27, color=GOLD),
        ).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        fit_width(setup_txt, 12.3)
        setup_txt.next_to(setup_banner, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(setup_txt, shift=DOWN*0.1))
        self.wait(0.6)

        tag = self.banner("定理 4.3.3", C_THM)
        tag.next_to(setup_txt, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag))

        stmt1 = VGroup(
            eq(r"T:\mathcal{L}(V)\to M_n(\mathbb{K})", size=29, color=TXT),
            ct("是线性同构，且", size=24, color=TXT),
            ct("还保持乘法", size=27, color=GOLD, weight=BOLD),
        ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        fit_width(stmt1, 12.3)
        stmt1.next_to(tag, DOWN, buff=0.3).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(stmt1, shift=DOWN*0.1))

        stmt2 = VGroup(
            ct("即对任意", size=24, color=GREY),
            eq(r"\varphi,\psi\in\mathcal{L}(V)", size=27, color=GREY),
            ct("有", size=24, color=GREY),
            eq(r"T(\psi\varphi)=T(\psi)T(\varphi)", size=27, color=GOLD),
        ).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        fit_width(stmt2, 12.3)
        stmt2.next_to(stmt1, DOWN, buff=0.3).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(stmt2, shift=DOWN*0.1))
        self.wait(0.8)

        pf_short = ct("证明：由定理 4.3.1（线性同构）和定理 4.3.2（乘法保持）立得", size=23, color=GREY)
        fit_width(pf_short, 12.0)
        pf_short.next_to(stmt2, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        qed = self.qed_mark().next_to(pf_short, RIGHT, buff=0.25)
        self.play(FadeIn(pf_short, shift=DOWN*0.1), FadeIn(qed))
        self.wait(1.2)
        self.clear_scene()

        # Corollary 4.3.1
        head = self.add_header()
        cortag = self.banner("推论 4.3.1", C_COR)
        cortag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(cortag))

        cor1 = VGroup(
            ct("(1)", size=24, color=TXT),
            eq(r"T(I_V)=I_n", size=32, color=GOLD),
        ).arrange(RIGHT, buff=0.3)
        cor1.next_to(cortag, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(cor1, shift=DOWN*0.1))
        pf1 = VGroup(
            ct("（", size=21, color=GREY),
            eq(r"\varphi=I_V", size=22, color=GREY),
            ct(" 时 (4.3.3) 的系数矩阵是 ", size=21, color=GREY),
            eq(r"I_n", size=22, color=GREY),
            ct("，转置也是 ", size=21, color=GREY),
            eq(r"I_n", size=22, color=GREY),
            ct("）", size=21, color=GREY),
        ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
        fit_width(pf1, 12.3)
        pf1.next_to(cor1, DOWN, buff=0.18).to_edge(LEFT, buff=1.3)
        self.play(FadeIn(pf1, shift=DOWN*0.08)); self.wait(0.6)

        cor2_line1 = VGroup(
            ct("(2) ", size=24, color=TXT),
            eq(r"\varphi", size=26, color=GOLD),
            ct(" 是自同构 ", size=24, color=TXT),
            eq(r"\Longleftrightarrow", size=26, color=GOLD),
            eq(r"T(\varphi)", size=26, color=GOLD),
            ct(" 可逆", size=24, color=TXT),
        ).arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        fit_width(cor2_line1, 12.3)
        cor2_line1.next_to(pf1, DOWN, buff=0.4).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(cor2_line1, shift=DOWN*0.1))

        # 将公式拆分为独立部分，用 {} 分组消除 LaTeX 上标歧义
        cor2_line2 = VGroup(
            ct("此时 ", size=24, color=TXT),
            eq(r"T(\varphi^{-1})", size=28, color=GOLD),
            eq(r"=", size=28, color=GOLD),
            eq(r"{T(\varphi)}^{-1}", size=28, color=GOLD),
        ).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        fit_width(cor2_line2, 12.3)
        cor2_line2.next_to(cor2_line1, DOWN, buff=0.2).to_edge(LEFT, buff=1.0)
        self.play(FadeIn(cor2_line2, shift=DOWN*0.1))

        pf2_lines = VGroup(
            VGroup(ct("由 ", size=22, color=GREY),
                   eq(r"\varphi\varphi^{-1}=I_V", size=24, color=GREY),
                   ct(" 两边用 T 作用，利用推论(1)：", size=22, color=GREY)).arrange(RIGHT, buff=0.1, aligned_edge=DOWN),
            eq(r"T(\varphi)T(\varphi^{-1})=T(\varphi\varphi^{-1})=T(I_V)=I_n", size=24),
        )
        pf2_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fit_width(pf2_lines, 12.0)
        pf2_lines.next_to(cor2_line2, DOWN, buff=0.3).to_edge(LEFT, buff=1.3)
        qed2 = self.qed_mark().next_to(pf2_lines, RIGHT, buff=0.25)
        self.play(FadeIn(pf2_lines[0], shift=DOWN*0.1))
        self.play(Write(pf2_lines[1]))
        self.play(FadeIn(qed2))
        self.wait(1.3)
        self.clear_scene()


# ========================================================================
#  Scene 08 — 推论 4.3.1（单独一条值得强调的内容：T 是代数同构）
# ========================================================================
class Scene08_Corollary(BaseScene):
    part_index = 8
    subtitle = "推论 4.3.1"

    def construct(self):
        head = self.add_header()

        sum_title = ct("本节结论的桥梁意义", size=30, color=GOLD, weight=BOLD)
        sum_title.next_to(head, DOWN, buff=0.55)
        self.play(Write(sum_title))

        items = [
            (C_V,    "线性映射 φ∈L(V,U)",    C_A,    "⟷  m×n 矩阵 A",         C_DEF,  "（线性同构 T）"),
            (C_V,    "映射加法 φ+ψ",           C_A,    "⟷  矩阵加法 A+B",         GREY,   ""),
            (C_V,    "数乘 kφ",                C_A,    "⟷  数乘 kA",             GREY,   ""),
            (C_W,    "映射复合 ψ∘φ",           C_B,    "⟷  矩阵乘积 BA",          GOLD,   "（最重要！）"),
            (C_COR,  "可逆映射 φ⁻¹",          C_P,    "⟷  逆矩阵 A⁻¹",          GREY,   ""),
        ]

        rows = VGroup()
        for lc, lt, rc, rt, ec, et in items:
            row_mobj = VGroup(
                mixed(lt, size=24, color=lc),
                mixed(rt, size=24, color=rc),
                mixed(et, size=21, color=ec),
            ).arrange(RIGHT, buff=0.6)
            fit_width(row_mobj, 12.0)
            rows.add(row_mobj)

        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        rows.next_to(sum_title, DOWN, buff=0.55).to_edge(LEFT, buff=0.85)

        for i, r in enumerate(rows):
            self.play(FadeIn(r, shift=DOWN*0.1), run_time=0.5)
            self.wait(0.15)

        self.wait(1.0)

        # Highlight the multiplication row
        mult_box = SurroundingRectangle(rows[3], color=GOLD, buff=0.12, corner_radius=0.1)
        self.play(Create(mult_box))
        key_note = ct("这就是矩阵乘法定义的几何动机！", size=26, color=GOLD, weight=BOLD)
        key_note.to_edge(DOWN, buff=0.6)
        self.play(FadeIn(key_note, shift=UP*0.15))
        self.wait(1.5)
        self.clear_scene()


# ========================================================================
#  Scene 09 — 基变换的动机：同一个 φ，换了基矩阵就变了
# ========================================================================
class Scene09_Bridge(BaseScene):
    part_index = 9
    subtitle = "基变换的动机"

    def construct(self):
        head = self.add_header()

        q_banner = self.banner("核心问题", C_P, size=24)
        q_banner.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(q_banner))

        q_txt = mixed("同一个线性变换 φ，在不同的基下，表示矩阵会不同吗？", size=27, color=TXT, weight=BOLD)
        fit_width(q_txt, 12.3)
        q_txt.next_to(q_banner, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(q_txt, shift=DOWN*0.15))
        self.wait(0.8)

        # Two-basis diagram
        V1 = Circle(radius=0.9, color=C_V, stroke_width=3).shift(LEFT*4.2 + DOWN*0.5)
        V2 = Circle(radius=0.9, color=C_V, stroke_width=3).shift(RIGHT*4.2 + DOWN*0.5)
        V1l = eq("V", size=36, color=C_V).move_to(V1)
        V2l = eq("V", size=36, color=C_V).move_to(V2)
        phi_top = CurvedArrow(V1.get_top()+UP*0.05, V2.get_top()+UP*0.05, angle=-0.7,
                               color=TXT, stroke_width=4)
        phi_tl = eq(r"\varphi", size=28, color=TXT).next_to(phi_top, UP, buff=0.05)

        basis1 = VGroup(
            VGroup(ct("基 {", size=20, color=C_V), eq(r"e_1,\ldots,e_n", size=22, color=C_V), ct("}", size=20, color=C_V)).arrange(RIGHT, buff=0.05),
            ct("表示矩阵", size=20, color=GREY),
            eq("A", size=30, color=C_A),
        ).arrange(DOWN, buff=0.15)
        basis1.next_to(V1, DOWN, buff=0.3)

        basis2 = VGroup(
            VGroup(ct("基 {", size=20, color=C_U), eq(r"f_1,\ldots,f_n", size=22, color=C_U), ct("}", size=20, color=C_U)).arrange(RIGHT, buff=0.05),
            ct("表示矩阵", size=20, color=GREY),
            eq("B", size=30, color=C_B),
        ).arrange(DOWN, buff=0.15)
        basis2.next_to(V2, DOWN, buff=0.3)

        self.play(Create(V1), Create(V2), Write(V1l), Write(V2l))
        self.play(Create(phi_top), Write(phi_tl))
        self.play(FadeIn(basis1, shift=DOWN*0.15))
        self.play(FadeIn(basis2, shift=DOWN*0.15))
        self.wait(0.8)

        neq_txt = VGroup(
            eq("A", size=40, color=C_A),
            eq(r"\neq", size=40, color=GOLD),
            eq("B", size=40, color=C_B),
            ct("（一般地）", size=24, color=GREY),
        ).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        neq_txt.next_to(VGroup(basis1, basis2), DOWN, buff=0.5)
        self.play(FadeIn(neq_txt, shift=UP*0.1))
        self.wait(0.8)

        question = ct("那么 A 和 B 之间究竟有什么关系？", size=27, color=GOLD, weight=BOLD)
        question.next_to(neq_txt, DOWN, buff=0.45)
        self.play(FadeIn(question, shift=DOWN*0.15))
        self.wait(0.8)

        hint = VGroup(
            ct("提示：两组基之间有", size=24, color=GREY),
            ct("过渡矩阵", size=27, color=C_P, weight=BOLD),
            eq("P", size=30, color=C_P),
            mixed("联系它们……", size=24, color=GREY),
        ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        fit_width(hint, 12.3)
        hint.next_to(question, DOWN, buff=0.4)
        self.play(FadeIn(hint, shift=DOWN*0.15))
        self.wait(1.3)
        self.clear_scene()


# ========================================================================
#  Scene 10 — 定理 4.3.4：B = P⁻¹AP  【★ 核心定理】
# ========================================================================
class Scene10_Theorem4(BaseScene):
    part_index = 10
    subtitle = "定理 4.3.4"

    def construct(self):
        # ---- Part 1: Geometric demo (2D example) ----
        head = self.add_header()
        geo_ttl = ct("几何演示：同一映射，两套坐标，两个矩阵", size=26, color=TXT, weight=BOLD)
        geo_ttl.next_to(head, DOWN, buff=0.5)
        self.play(FadeIn(geo_ttl, shift=DOWN*0.15))

        plane = NumberPlane(
            x_range=[-2.5, 2.5, 1], y_range=[-1, 2.5, 1],
            x_length=5.5, y_length=4.4,
            background_line_style={"stroke_color": GREY, "stroke_width": 1, "stroke_opacity": 0.28},
            axis_config={"stroke_color": GREY, "stroke_width": 2},
        ).shift(DOWN*0.55)
        self.play(Create(plane))

        orig = plane.coords_to_point(0, 0)
        # e-basis (blue, standard)
        e1t = plane.coords_to_point(1, 0)
        e2t = plane.coords_to_point(0, 1)
        e1a = Arrow(orig, e1t, buff=0, color=C_V, stroke_width=5)
        e2a = Arrow(orig, e2t, buff=0, color=C_V, stroke_width=5)
        e1l = eq("e_1", size=24, color=C_V).next_to(e1a, DOWN, buff=0.1)
        e2l = eq("e_2", size=24, color=C_V).next_to(e2a, LEFT, buff=0.1)

        # f-basis (gold): f₁=(1,1), f₂=(-1,1)  [45° rotated]
        f1t = plane.coords_to_point(1, 1)
        f2t = plane.coords_to_point(-1, 1)
        f1a = Arrow(orig, f1t, buff=0, color=GOLD, stroke_width=5)
        f2a = Arrow(orig, f2t, buff=0, color=GOLD, stroke_width=5)
        f1l = eq("f_1", size=24, color=GOLD).next_to(f1a.get_end(), UR, buff=0.08)
        f2l = eq("f_2", size=24, color=GOLD).next_to(f2a.get_end(), UL, buff=0.08)

        self.play(GrowArrow(e1a), GrowArrow(e2a), Write(e1l), Write(e2l))
        self.wait(0.3)
        self.play(GrowArrow(f1a), GrowArrow(f2a), Write(f1l), Write(f2l))
        self.wait(0.5)

        # α = (0.5, 1.5) in e-coords = f₁ + 0.5*f₂ in f-coords
        at = plane.coords_to_point(0.5, 1.5)
        aa = Arrow(orig, at, buff=0, color=C_W, stroke_width=5)
        al = VGroup(
            eq(r"\alpha", size=22, color=C_W),
            ct("（e坐标: 0.5, 1.5）", size=17, color=C_V),
        ).arrange(DOWN, buff=0.05)
        al.next_to(aa.get_end(), RIGHT, buff=0.1)

        self.play(GrowArrow(aa), FadeIn(al))
        self.wait(0.6)

        # φ(α): reflection about y-axis → (-0.5, 1.5)
        yaxis_line = Line(plane.coords_to_point(0, -0.9), plane.coords_to_point(0, 2.4),
                           color=WHITE, stroke_width=2.5, stroke_opacity=0.7)
        yaxis_label = ct("反射轴 (y轴)", size=18, color=WHITE).next_to(yaxis_line, RIGHT, buff=0.1)
        yaxis_label.shift(UP*0.5)

        self.play(Create(yaxis_line), FadeIn(yaxis_label))

        pat = plane.coords_to_point(-0.5, 1.5)
        paa = Arrow(orig, pat, buff=0, color=C_B, stroke_width=5)
        pal = VGroup(
            eq(r"\varphi(\alpha)", size=22, color=C_B),
            ct("（e坐标: -0.5, 1.5）", size=17, color=C_V),
        ).arrange(DOWN, buff=0.05)
        pal.next_to(paa.get_end(), LEFT, buff=0.12)

        self.play(GrowArrow(paa), FadeIn(pal))
        self.wait(0.7)

        bottom_note = ct("在 e 基下 A=[[-1,0],[0,1]]；在 f 基下 B=[[0,1],[1,0]]（不同！）", size=21, color=GREY)
        fit_width(bottom_note, 12.3)
        bottom_note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(bottom_note, shift=UP*0.1))
        self.wait(1.3)
        self.clear_scene()

        # ---- Part 2: Theorem statement ----
        head = self.add_header()
        tag = self.banner("定理 4.3.4", C_THM)
        tag.next_to(head, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag))

        setup_lines = VGroup(
            VGroup(ct("设 V 是 K 上 n 维线性空间，", size=22, color=TXT),
                   eq(r"\varphi\in L(V)", size=24, color=GOLD)).arrange(RIGHT, buff=0.1, aligned_edge=DOWN),
            VGroup(ct("两组基：", size=22, color=GREY),
                   eq(r"\{e_1,\ldots,e_n\}", size=24, color=C_V),
                   ct("和", size=22, color=GREY),
                   eq(r"\{f_1,\ldots,f_n\}", size=24, color=C_U),
                   ct("，过渡矩阵为", size=22, color=GREY),
                   eq("P", size=26, color=C_P)).arrange(RIGHT, buff=0.12),
            VGroup(mixed("φ 在 e-基下表示矩阵为", size=22, color=GREY),
                   eq("A", size=26, color=C_A),
                   ct("，在 f-基下为", size=22, color=GREY),
                   eq("B", size=26, color=C_B)).arrange(RIGHT, buff=0.12),
        )
        for s in setup_lines:
            fit_width(s, 12.3)
        setup_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        setup_lines.next_to(tag, DOWN, buff=0.22).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(setup_lines[0], shift=DOWN*0.1))
        self.play(FadeIn(setup_lines[1], shift=DOWN*0.1))
        self.play(FadeIn(setup_lines[2], shift=DOWN*0.1))
        self.wait(0.7)

        # Big result — 使用精确位置，确保在屏幕内
        result_eq = eq(r"B = P^{-1}AP", size=40, color=GOLD)
        # 将公式对齐到 setup_lines 正下方，保持水平居中
        result_eq.align_to(setup_lines, LEFT)
        result_eq.next_to(setup_lines, DOWN, buff=0.28)
        big_box = SurroundingRectangle(result_eq, color=GOLD, buff=0.22, corner_radius=0.2, stroke_width=4)
        self.play(Write(result_eq))
        self.play(Create(big_box))
        self.wait(1.5)
        self.clear_scene()

        # ---- Part 3: Coordinate diagram ----
        head = self.add_header()
        diag_ttl = ct("证明思路：坐标关系图", size=27, color=TXT, weight=BOLD)
        diag_ttl.next_to(head, DOWN, buff=0.5)
        self.play(FadeIn(diag_ttl))

        # Layout: two rows representing α and φ(α), with columns for e-coords and f-coords
        #
        #   (α, e-coords: λ) ---A---> (φ(α), e-coords: ξ)
        #         |P                          |P
        #   (α, f-coords: μ) ---B---> (φ(α), f-coords: η)
        #
        lam_pos  = np.array([-3.8, 0.9, 0])
        xi_pos   = np.array([ 3.8, 0.9, 0])
        mu_pos   = np.array([-3.8,-1.3, 0])
        eta_pos  = np.array([ 3.8,-1.3, 0])

        # 使用分离的 ct()/eq() 节点，避免把中文放入 LaTeX
        lam_top = VGroup(eq(r"\lambda", size=36, color=C_V),
                         mixed("(α的e坐标)", size=19, color=GREY)).arrange(DOWN, buff=0.1).move_to(lam_pos)
        xi_top  = VGroup(eq(r"\xi", size=36, color=C_V),
                         mixed("(φ(α)的e坐标)", size=19, color=GREY)).arrange(DOWN, buff=0.1).move_to(xi_pos)
        mu_bot  = VGroup(eq(r"\mu", size=36, color=C_U),
                         mixed("(α的f坐标)", size=19, color=GREY)).arrange(DOWN, buff=0.1).move_to(mu_pos)
        eta_bot = VGroup(eq(r"\eta", size=36, color=C_U),
                         mixed("(φ(α)的f坐标)", size=19, color=GREY)).arrange(DOWN, buff=0.1).move_to(eta_pos)

        A_arr = Arrow(lam_pos + RIGHT*0.55, xi_pos  + LEFT*0.50,  buff=0, color=C_A, stroke_width=4)
        B_arr = Arrow(mu_pos  + RIGHT*0.55, eta_pos + LEFT*0.55,  buff=0, color=C_B, stroke_width=4)
        # 箭头从下往上：μ→λ 和 η→ξ，表示乘以 P（λ=Pμ, ξ=Pη）
        P1_arr= Arrow(mu_pos  + UP*0.55,    lam_pos + DOWN*0.55,  buff=0, color=C_P, stroke_width=4)
        P2_arr= Arrow(eta_pos + UP*0.55,    xi_pos  + DOWN*0.55,  buff=0, color=C_P, stroke_width=4)

        A_l = eq(r"A\cdot",  size=28, color=C_A).next_to(A_arr, UP, buff=0.1)
        B_l = eq(r"B\cdot",  size=28, color=C_B).next_to(B_arr, DOWN, buff=0.1)
        P1_l= eq(r"\cdot P", size=24, color=C_P).next_to(P1_arr, LEFT, buff=0.1)
        P2_l= eq(r"\cdot P", size=24, color=C_P).next_to(P2_arr, RIGHT, buff=0.1)

        self.play(FadeIn(lam_top), FadeIn(xi_top), FadeIn(mu_bot), FadeIn(eta_bot))
        self.play(GrowArrow(A_arr), Write(A_l))
        self.play(GrowArrow(B_arr), Write(B_l))
        self.play(GrowArrow(P1_arr), Write(P1_l), GrowArrow(P2_arr), Write(P2_l))

        # Annotations
        rel_lam = eq(r"\lambda=P\mu", size=26, color=C_P).next_to(P1_arr, RIGHT, buff=0.35)
        rel_xi  = eq(r"\xi=P\eta", size=26, color=C_P).next_to(P2_arr, LEFT, buff=0.35)
        self.play(Write(rel_lam), Write(rel_xi))
        self.wait(1.1)
        self.clear_scene()

        # ---- Part 4: Algebraic proof ----
        head = self.add_header()
        ptag = self.proof_label()
        ptag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(ptag))

        setup_ref = mixed("记：λ = Pμ (4.3.4)，ξ = Aλ，η = Bμ (4.3.6)，ξ = Pη (4.3.7)", size=22, color=GREY)
        fit_width(setup_ref, 12.0)
        setup_ref.next_to(ptag, DOWN, buff=0.3).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(setup_ref, shift=DOWN*0.1))

        chain_steps = VGroup(
            eq(r"P\eta\ =\ \xi\ =\ A\lambda\ =\ A(P\mu)\ =\ AP\mu", size=32),
            eq(r"\therefore\quad P(B\mu)\ =\ AP\mu\quad (\forall\,\mu)", size=30, color=TXT),
            eq(r"\therefore\quad PB\ =\ AP", size=32, color=C_P),
            eq(r"\therefore\quad B\ =\ P^{-1}AP", size=38, color=GOLD),
        )
        chain_steps.arrange(DOWN, buff=0.38)
        fit_width(chain_steps, 11.0)
        chain_steps.next_to(setup_ref, DOWN, buff=0.45)

        colors = [TXT, TXT, C_P, GOLD]
        for step, color in zip(chain_steps, colors):
            step.set_color(color)
            self.play(Write(step)); self.wait(0.4)

        result_box = SurroundingRectangle(chain_steps[-1], color=GOLD, buff=0.28, corner_radius=0.15, stroke_width=4)
        qed = self.qed_mark().next_to(chain_steps[-1], RIGHT, buff=0.35)
        self.play(Create(result_box), FadeIn(qed))
        self.wait(1.5)
        self.clear_scene()


# ========================================================================
#  Scene 11 — 定义 4.3.1：相似矩阵
# ========================================================================
class Scene11_SimilarDef(BaseScene):
    part_index = 11
    subtitle = "相似矩阵"

    def construct(self):
        head = self.add_header()
        tag = self.banner("定义 4.3.1", C_DEF)
        tag.next_to(head, DOWN, buff=0.55).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag))

        defn_line1 = VGroup(
            ct("若 A, B 是 n 阶方阵，且存在", size=26, color=TXT),
            ct("n 阶可逆矩阵", size=26, color=C_P),
            eq("P", size=30, color=C_P),
            ct("使得", size=26, color=TXT),
        ).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        fit_width(defn_line1, 12.3)
        defn_line1.next_to(tag, DOWN, buff=0.45).to_edge(LEFT, buff=0.85)

        defn_eq = eq(r"B = P^{-1}AP", size=44, color=GOLD)
        defn_eq.next_to(defn_line1, DOWN, buff=0.4)
        defn_box = SurroundingRectangle(defn_eq, color=GOLD, buff=0.35, corner_radius=0.2, stroke_width=3)

        defn_line2 = VGroup(
            ct("则称 A 与 B", size=26, color=TXT),
            ct("相似", size=30, color=GOLD, weight=BOLD),
            ct("，记作", size=26, color=TXT),
            eq(r"A\approx B", size=30, color=GOLD),
        ).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        defn_line2.next_to(defn_eq, DOWN, buff=0.45)

        self.play(FadeIn(defn_line1, shift=DOWN*0.1))
        self.play(Write(defn_eq)); self.play(Create(defn_box))
        self.play(FadeIn(defn_line2, shift=DOWN*0.1))
        self.wait(0.9)

        geom_txt = ct("几何意义：A 和 B 表示同一个线性变换在不同基下的矩阵", size=24, color=C_DEF)
        fit_width(geom_txt, 12.3)
        geom_txt.next_to(defn_line2, DOWN, buff=0.55)
        note_box = SurroundingRectangle(geom_txt, color=C_DEF, buff=0.2, corner_radius=0.1)
        self.play(FadeIn(geom_txt, shift=DOWN*0.1), Create(note_box))
        self.wait(1.3)
        self.clear_scene()


# ========================================================================
#  Scene 12 — 命题 4.3.1：相似是等价关系
# ========================================================================
class Scene12_Proposition(BaseScene):
    part_index = 12
    subtitle = "命题 4.3.1"

    def construct(self):
        head = self.add_header()
        tag = self.banner("命题 4.3.1", C_PROP)
        tag.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(tag))

        intro = mixed("相似关系 A≈B 是 n 阶矩阵集合上的等价关系，即：", size=25, color=TXT)
        fit_width(intro, 12.3)
        intro.next_to(tag, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)
        self.play(FadeIn(intro, shift=DOWN*0.1))

        props = [
            ("自反性", r"A\approx A",
             r"A = I_n^{-1}AI_n"),
            ("对称性", r"A\approx B\Rightarrow B\approx A",
             r"B=P^{-1}AP\Rightarrow A=PBP^{-1}=(P^{-1})^{-1}B(P^{-1})"),
            ("传递性", r"A\approx B,\;B\approx C\Rightarrow A\approx C",
             r"C=(PQ)^{-1}A(PQ)"),
        ]

        all_rows = VGroup()
        for name, stmt, pf in props:
            tag_m = self.banner(name, C_PROP, size=20)
            stmt_m = eq(stmt, size=26, color=TXT)
            pf_m = eq(pf, size=22, color=GREY)
            row_g = VGroup(tag_m,
                           VGroup(stmt_m, pf_m).arrange(DOWN, aligned_edge=LEFT, buff=0.15))
            row_g.arrange(RIGHT, buff=0.35)
            fit_width(row_g, 12.3)
            all_rows.add(row_g)

        all_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        all_rows.next_to(intro, DOWN, buff=0.4).to_edge(LEFT, buff=0.85)

        for r in all_rows:
            self.play(FadeIn(r, shift=DOWN*0.1))
            self.wait(0.4)
        self.wait(1.0)

        # Key point — 左对齐确保"定理"不超出屏幕
        key = ct("定理 4.3.4：同一线性变换在不同基下的表示矩阵必然相似", size=22, color=GOLD, weight=BOLD)
        fit_width(key, 12.0)
        key.next_to(all_rows, DOWN, buff=0.45).align_to(all_rows, LEFT)
        key_box = SurroundingRectangle(key, color=GOLD, buff=0.18, corner_radius=0.1)
        self.play(FadeIn(key, shift=DOWN*0.1), Create(key_box))
        self.wait(1.4)
        self.clear_scene()


# ========================================================================
#  Scene 13 — 总结与展望
# ========================================================================
class Scene13_Summary(BaseScene):
    part_index = 13
    subtitle = "总结与展望"

    def construct(self):
        head = self.add_header()

        sum_title = ct("§4.3  线性映射与矩阵  —  本节小结", size=28, color=GOLD, weight=BOLD)
        sum_title.next_to(head, DOWN, buff=0.5)
        underline = Line(LEFT*4, RIGHT*4, color=GOLD, stroke_width=2).next_to(sum_title, DOWN, buff=0.15)
        self.play(Write(sum_title), Create(underline))
        self.wait(0.4)

        # 构建行：手动拆分确保数学部分用 eq()
        def make_row(color, label, content):
            tag_m = self.banner(label, color, size=17)
            txt_m = mixed(content, size=22, color=TXT)
            row = VGroup(tag_m, txt_m).arrange(RIGHT, buff=0.35)
            fit_width(row, 12.3)
            return row

        def math_row(color, label, *parts):
            """构建含数学公式的行：parts = [("c","中文"), ("m",r"latex"), ...]"""
            tag_m = self.banner(label, color, size=17)
            inner = []
            for kind, text in parts:
                if kind == "c":
                    inner.append(mixed(text, size=22, color=TXT))
                else:
                    inner.append(eq(text, size=24, color=GOLD))
            txt_m = VGroup(*inner).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
            row = VGroup(tag_m, txt_m).arrange(RIGHT, buff=0.35)
            fit_width(row, 12.3)
            return row

        results_rows = VGroup(
            make_row(C_LEMMA, "引理 4.3.1", "线性映射由基向量的像唯一确定"),
            make_row(C_DEF, "定义", "表示矩阵 A（φ 在给定基下）"),
            math_row(C_THM, "定理 4.3.1",
                     ("c", "T: L(V,U) → "), ("m", r"M_{m\times n}(K)"), ("c", " 是线性同构")),
            math_row(C_THM, "定理 4.3.2",
                     ("m", r"T(\psi\varphi)=T(\psi)T(\varphi)"), ("c", " 矩阵乘法=复合")),
            math_row(C_THM, "定理 4.3.3",
                     ("m", r"L(V)"), ("c", " 与 "), ("m", r"M_n(K)"), ("c", " 保持加法和乘法")),
            math_row(C_COR, "推论 4.3.1",
                     ("m", r"\varphi"), ("c", " 可逆 ⟺ "), ("m", r"T(\varphi)"),
                     ("c", " 可逆，"), ("m", r"T(\varphi^{-1}) = T(\varphi)^{-1}")),
            math_row(C_THM, "定理 4.3.4★",
                     ("m", r"B=P^{-1}AP"), ("c", " （同一变换，不同基，表示矩阵相似）")),
            make_row(C_DEF, "定义 4.3.1", "相似矩阵 A≈B"),
            make_row(C_PROP, "命题 4.3.1", "相似是等价关系"),
        )

        results_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        results_rows.next_to(underline, DOWN, buff=0.35).to_edge(LEFT, buff=0.85)

        for i, r in enumerate(results_rows):
            self.play(FadeIn(r, shift=DOWN*0.1), run_time=0.4)
            self.wait(0.08)
        self.wait(0.8)

        # Highlight the core result
        star_box = SurroundingRectangle(results_rows[6], color=GOLD, buff=0.1, corner_radius=0.1, stroke_width=3)
        self.play(Create(star_box))
        self.wait(0.8)
        self.clear_scene()

        # Preview of next chapters
        head = self.add_header()
        preview_ttl = ct("展望：第六章、第七章", size=30, color=GOLD, weight=BOLD)
        preview_ttl.next_to(head, DOWN, buff=0.55)
        self.play(Write(preview_ttl))

        question = mixed("能否找到一组「好的基」，使 φ 的表示矩阵 A 尽量简单？", size=26, color=TXT)
        fit_width(question, 12.3)
        question.next_to(preview_ttl, DOWN, buff=0.5)
        self.play(FadeIn(question, shift=DOWN*0.15))

        previews = VGroup(
            VGroup(self.banner("第六章  特征值", C_THM, size=20),
                   mixed("对角化问题：A ≈ 对角矩阵 diag(λ₁,...,λₙ)?", size=23, color=TXT)).arrange(RIGHT, buff=0.4),
            VGroup(self.banner("第七章  相似标准型", C_THM, size=20),
                   ct("Jordan 标准型：最简单的相似形式", size=23, color=TXT)).arrange(RIGHT, buff=0.4),
        )
        for p in previews:
            fit_width(p, 12.3)
        previews.arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        previews.next_to(question, DOWN, buff=0.5).to_edge(LEFT, buff=0.85)
        for p in previews:
            self.play(FadeIn(p, shift=DOWN*0.15))
            self.wait(0.3)
        self.wait(1.0)

        # Closing
        closing = ct("§4.3  是连接几何与代数最重要的桥梁章节", size=26, color=C_DEF, weight=BOLD)
        fit_width(closing, 12.3)
        closing.next_to(previews, DOWN, buff=0.55)
        c_box = SurroundingRectangle(closing, color=C_DEF, buff=0.22, corner_radius=0.12)
        self.play(FadeIn(closing, shift=DOWN*0.15), Create(c_box))
        self.wait(2.0)
        self.clear_scene()
