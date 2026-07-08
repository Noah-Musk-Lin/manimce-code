# ManimCE 数学动画合集 · Math Animation Collection

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://www.manim.community/"><img src="https://img.shields.io/badge/Manim-Community_v0.18+-15C39B?logo=manim&logoColor=white" alt="Manim"></a>
  <img src="https://img.shields.io/badge/Scripts-53+-9CF" alt="Scripts">
  <a href="./LICENSE"><img src="https://img.shields.io/badge/License-MIT-green" alt="License"></a>
  <img src="https://img.shields.io/badge/Language-中文_|_English-ff69b4" alt="Language">
</p>

<br>

> **数学不是看着别人做就能学会的——你得自己动手，亲眼看到它发生。**
>
> 这个仓库汇集了我用 ManimCommunity 制作的数学动画。每一个脚本，都是对"这个定理到底在说什么"的一次追问。
>
> **You don't learn math by watching someone else do it — you learn by seeing it happen with your own eyes.**
>
> This repository collects my math animations built with ManimCommunity. Each script is an attempt to answer: "What is this theorem really saying?"

<br>

---

## 🎬 这是什么？ · What is this?

[3Blue1Brown](https://www.3blue1brown.com/) 的 Grant Sanderson 创建了 [manim](https://github.com/3b1b/manim) —— 一个精确的程序化动画引擎，专为制作解释性数学视频而生。本仓库基于其社区维护版 **ManimCommunity**，将一系列高等数学中的核心概念以可视化的方式呈现。

每个 `.py` 文件对应一个数学主题的完整动画。它们被设计为**独立的场景**，可以直接渲染成视频——就像 3b1b 的视频那样，让抽象的公式在屏幕上"活"过来。

Grant Sanderson of [3Blue1Brown](https://www.3blue1brown.com/) created [manim](https://github.com/3b1b/manim) — an engine for precise programmatic animations, designed for creating explanatory math videos. This repository uses its community-maintained fork, **ManimCommunity**, to visualize core concepts from advanced mathematics.

Each `.py` file is a complete animation for one mathematical topic, designed as a **standalone scene** that renders directly to video — letting abstract formulas come to life on screen, just like a 3b1b video.

## 📺 关注我 · Follow

<p align="center">
  <a href="https://space.bilibili.com/3494372465183405">
    <img src="https://img.shields.io/badge/Bilibili-哔哩哔哩-00A1D6?logo=bilibili&logoColor=white&style=for-the-badge" alt="Bilibili">
  </a>
  &nbsp;
  <a href="https://v.douyin.com/sDg6IeYwx-M/">
    <img src="https://img.shields.io/badge/Douyin-抖音_LinXMath-000000?logo=tiktok&logoColor=white&style=for-the-badge" alt="Douyin">
  </a>
</p>

## 📚 主题分类 · Topics

> 共 **53 个脚本**，按数学主题分组。每个脚本都包含了渲染时使用的场景类名。
>
> **53 scripts** in total, organized by mathematical topic. Each includes the scene class name for rendering.

### 📐 微积分与实分析 · Calculus & Real Analysis

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `LagrangeMeanValueTheorem.py` | 拉格朗日中值定理 | `LagrangeMeanValueTheorem` |
| `Lagrange3D.py` | 拉格朗日中值定理（3D 版） | `Lagrange3D` |
| `TaylorExpansion2D.py` | 二元泰勒展开 | `TaylorExpansion2D` |
| `taylor_series.py` | 泰勒级数（7 个场景） | `A1`–`A7` |
| `NestedIntervalTheoremA.py` | 闭区间套定理 | `NestedIntervalTheoremA` |
| `零点定理.py` | 零点定理（Bolzano） | `A1` |
| `ArchimedesArea.py` | 阿基米德穷竭法 | `ArchimedesArea` |

### 🧮 线性代数 · Linear Algebra

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `BlockMatrix.py` | 分块矩阵 | `BlockMatrixScene` |
| `MatrixMultiplicationScene.py` | 矩阵乘法 | `MatrixMultiplicationScene` |
| `LaplaceExpansion.py` | 行列式拉普拉斯展开 | `LaplaceExpansion` |
| `cauchy_binet_manim.py` | 柯西–比内公式 | `CauchyBinetFormula` |
| `matrix_inverse_animation.py` | 逆矩阵 | `MatrixInverseExplanation` |
| `JacobianDeterminant.py` | 雅可比行列式 | `JacobianDeterminant` |
| `affine_proof.py` | 仿射变换证明 | `AffineProof` |
| `linear_extension_theorem.py` | 线性延拓定理 | `LinearExtensionScene1` |

### 🔮 复分析 · Complex Analysis

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `CauchyRiemannEquations.py` | 柯西–黎曼方程 | `CauchyRiemannEquations` |
| `Proof of Euler Formula change.py` | 欧拉公式的证明 | `EulerFormulaProof` |

### 🌊 常微分方程 · Ordinary Differential Equations

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `ODE.py` | 常微分方程导论 | `ODE` |
| `Ordinary Differential Equation.py` | 常微分方程 | `OrdinaryDifferentialEquation` |
| `ODESubstitutionMethods.py` | ODE 换元法 | `ODESubstitutionMethods` |
| `DirectionField.py` | 方向场 | `DirectionField` |
| `DirectionFieldMulti.py` | 方向场图集 | `DirectionFieldGallery` |
| `ode_max_interval.py` | ODE 最大存在区间 | `ODEMaxIntervalScene` |
| `Wronskian.py` | 朗斯基行列式 | `Wronskian` |

### 📏 几何与曲线 · Geometry & Curves

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `ApolloniusCircleExpress.py` | 阿波罗尼奥斯圆 | `ApolloniusCircleExpress` |
| `ArbitraryAngle.py` | 任意角 | `ArbitraryAngle` |
| `CircleToTriangle.py` | 圆化三角形（等积变换） | `CircleToTriangle` |
| `circle.py` | 圆的面积 | `Circle_Area` |
| `Cut.py` | 圆面积切割法 | `Ultimate_Version_Circle_Area` |
| `Ultimate Version Circle Area.py` | 圆面积（终极版） | `Ultimate_Version_Circle_Area` |
| `EllipsePerpendicularSegments.py` | 椭圆垂直径段 | `EllipsePerpendicularSegments` |
| `ellipsoid.py` | 椭球面（3D） | `Ellipsoid` |
| `heart.py` | 心形曲线 | `HeartCurve` |
| `archimedean_spiral.py` | 阿基米德螺线 | `ArchimedeanSpiral` |
| `RightTriangle.py` | 直角三角形 | `RightTriangle` |
| `RightTriangleWithMidsegment.py` | 直角三角形中位线 | `RightTriangleWithMidsegment` |
| `SatelliteDishAnimation.py` | 卫星天线（抛物面反射） | `SatelliteDishAnimation` |
| `三角函数.py` | 三角函数单位圆（3D） | `TrigCircle3D` |

### 🗺️ 坐标变换与可视化 · Coordinate Transform

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `CoordinateTransform.py` | 坐标变换与雅可比 | `CoordinateTransform` |
| `ax.py` | 平滑坐标系 | `SmoothCoordinateSystem` |
| `vortex_animation.py` | 3D 涡旋 | `ThreeDVortex` |

### ⚡ 代数与不等式 · Algebra & Inequalities

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `SolveInequality.py` | 解不等式 | `SolveInequalityProblem` |
| `SolveInequalityProblem.py` | 不等式问题 | `SolveInequalityProblem` |
| `MultiLinearRecurrence.py` | 多元线性递推 | `MultiLinearRecurrence` |

### 🤖 算法 · Algorithms

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `BinarySearchExplanation.py` | 二分查找 | `BinarySearchExplanation` |
| `OPENGL.py` | 二分查找（OpenGL 交互版） | `BinarySearchDemo` |

### 🧪 示例与测试 · Examples & Tests

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `SquareToCircle.py` | 方变圆（入门示例） | `SquareToCircle` |
| `sample.py` | 变换示例 | `TransformExample` |
| `new.py` | 三角函数 3D（草稿） | `TrigCircle3D` |
| `TA.py` / `Test.py` | 测试场景 | `Test` |
| `cirecle.py` / `test2.py` | 草稿与测试 | `Tem` / `EulerFormulaProof` |

---

## 🚀 快速开始 · Getting Started

### 1. 安装 ManimCommunity

```bash
pip install manim
```

> **注意：** 这不是 Grant 原始仓库中的 `manimgl`，而是社区维护版。两者不兼容，本仓库所有脚本均基于 ManimCommunity 编写。
>
> **Note:** This is the community-maintained `manim` (ManimCommunity), NOT Grant's original `manimgl`. The two are incompatible. All scripts in this repo are written for ManimCommunity.

### 2. 安装系统依赖

| 工具 | 用途 | 下载 |
| --- | --- | --- |
| **LaTeX** (MiKTeX / TeX Live) | 数学公式渲染 | [miktex.org](https://miktex.org/) / [tug.org/texlive](https://tug.org/texlive/) |
| **FFmpeg** | 视频编码 | [ffmpeg.org](https://ffmpeg.org/) |

### 3. 渲染动画

```bash
# 低质量快速预览（开发用）
manim -pql <script>.py <SceneClass>

# 高质量最终渲染
manim -pqh <script>.py <SceneClass>

# 4K 渲染
manim -pqk <script>.py <SceneClass>
```

**示例：** 渲染拉格朗日中值定理动画

```bash
manim -pql LagrangeMeanValueTheorem.py LagrangeMeanValueTheorem
```

| 参数 | 含义 |
| --- | --- |
| `-p` | 渲染完成后自动播放预览 |
| `-ql` | 480p 低质量（快速迭代） |
| `-qh` | 1080p 高质量 |
| `-qk` | 4K 超高清 |
| `<SceneClass>` | 场景类名，参见上方表格 |

### 4. 一次渲染多个场景

如果想批量渲染，可以写一个简单的脚本：

```python
# render_all.py
import subprocess, sys

scripts = [
    ("LagrangeMeanValueTheorem.py", "LagrangeMeanValueTheorem"),
    ("TaylorExpansion2D.py", "TaylorExpansion2D"),
    # ... 更多场景
]

for script, scene in scripts:
    subprocess.run(["manim", "-pqh", script, scene])
```

```bash
python render_all.py
```

---

## 📁 目录结构 · Project Structure

```text
manimce code/
├── README.md                         # 本文件
├── LICENSE                           # MIT 许可证
├── .gitignore                        # Git 忽略规则
├── custom_config.yml                 # Manim 自定义配置
│
├── *.py                              # 各数学主题的动画脚本（53+）
│
├── media/                            # 渲染输出（gitignore）
│   ├── videos/                       #   视频文件
│   └── images/                       #   图片文件
│
└── __pycache__/                      # Python 缓存（gitignore）
```

---

## 📦 依赖 · Dependencies

| 依赖 | 版本 | 说明 |
| --- | --- | --- |
| Python | ≥ 3.8 | — |
| ManimCommunity (`manim`) | ≥ 0.18.0 | 核心动画引擎 |
| LaTeX | 任意发行版 | 数学公式排版 |
| FFmpeg | 任意版本 | 视频编码输出 |

---

## 🙏 致谢与参考 · Credits & References

本仓库的代码风格和动画设计深受以下资源启发：

- **[3Blue1Brown](https://www.3blue1brown.com/)** — Grant Sanderson 的数学视频开创了"可视觉化的数学"这一表达方式。他创建的 [manim](https://github.com/3b1b/manim) 是这个项目的基石。
- **[ManimCommunity](https://www.manim.community/)** — 社区维护版 manim，提供了更完善的文档和更活跃的开发生态。
- **[manimce code-style skill](/skills/manim-code-style/)** — 本仓库配套的代码规范与最佳实践指南。

> 如果你还没有看过 3b1b 的视频，强烈建议从[线性代数的本质](https://www.3blue1brown.com/topics/linear-algebra)系列开始。这些视频不仅教会你数学，更教会你*如何思考数学*。
>
> **If you haven't watched 3b1b's videos yet, start with [Essence of Linear Algebra](https://www.3blue1brown.com/topics/linear-algebra).** These videos don't just teach you math — they teach you *how to think about math*.

---

## 🤝 参与贡献 · Contributing

欢迎任何形式的贡献！以下是一些你可以做的事情：

- 🐛 **报 Bug** — 如果某个脚本无法渲染或渲染效果有误，请提 Issue
- 💡 **新动画** — 有想要可视化的数学概念？提 Issue 或直接发 PR
- 🎨 **改进** — 对现有动画的视觉效果、代码结构有改进建议？欢迎 PR
- 📖 **文档** — 发现文档错误或不清晰的地方，随时修正

新增脚本时请尽量遵循现有的代码风格和命名规范。可以参考 [SquareToCircle.py](SquareToCircle.py) 作为入门模板。

---

## 📄 许可 · License

本项目采用 [MIT License](./LICENSE) 开源。你可以自由地使用、修改和分发这些代码。

This project is open-sourced under the [MIT License](./LICENSE). You are free to use, modify, and distribute the code.

---

<p align="center">
  Made with ❤️ and a lot of <code>self.play()</code> calls
  <br>
  <sub>© 2026 LinXMath · Bilibili: <a href="https://space.bilibili.com/3494372465183405">林深不见鹿</a> · Douyin: <a href="https://v.douyin.com/sDg6IeYwx-M/">LinXMath</a></sub>
</p>
