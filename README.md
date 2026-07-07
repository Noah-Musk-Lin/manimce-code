# ManimCE 数学动画合集 · ManimCE Math Animation Collection

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Manim](https://img.shields.io/badge/Manim-Community-15C39B)
![Scripts](https://img.shields.io/badge/Scripts-53+-9CF)

> 使用 ManimCommunity 引擎制作的一组数学概念可视化动画，涵盖微积分、线性代数、复分析、常微分方程、几何等主题。
>
> A collection of math concept visualizations built with the ManimCommunity engine, covering calculus, linear algebra, complex analysis, ODEs, geometry, and more.

## ✨ 简介 · Introduction

本仓库收录个人学习与教学过程中制作的 manim 动画脚本，旨在把抽象的数学概念用可视化的方式呈现出来。每个 `.py` 文件是一个独立的动画场景，可单独渲染。

This repository collects manim animation scripts created for personal study and teaching, aiming to visualize abstract math concepts. Each `.py` file is a standalone scene that can be rendered independently.

## 📺 关注我 · Follow

- **哔哩哔哩 · Bilibili**：<https://space.bilibili.com/3494372465183405>
- **抖音 · Douyin**：`LinXMath`

## 📚 主题分类 · Topics

共 53 个脚本，按数学主题分类如下。表中“场景类”为渲染时传入的类名。
53 scripts in total, grouped by mathematical topic. The "Scene" column is the class name passed when rendering.

### 微积分与实分析 · Calculus & Real Analysis

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `LagrangeMeanValueTheorem.py` | 拉格朗日中值定理 · Lagrange Mean Value Theorem | `LagrangeMeanValueTheorem` |
| `Lagrange3D.py` | 拉格朗日中值定理（3D）· Lagrange MVT in 3D | `Lagrange3D` |
| `TaylorExpansion2D.py` | 二元泰勒展开 · 2D Taylor Expansion | `TaylorExpansion2D` |
| `taylor_series.py` | 泰勒级数（7 场景）· Taylor Series | `A1`–`A7` |
| `NestedIntervalTheoremA.py` | 闭区间套定理 · Nested Interval Theorem | `NestedIntervalTheoremA` |
| `零点定理.py` | 零点定理 · Bolzano's Theorem | `A1` |
| `ArchimedesArea.py` | 阿基米德穷竭法 · Method of Exhaustion | `ArchimedesArea` |

### 线性代数 · Linear Algebra

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `BlockMatrix.py` | 分块矩阵 · Block Matrix | `BlockMatrixScene` |
| `MatrixMultiplicationScene.py` | 矩阵乘法 · Matrix Multiplication | `MatrixMultiplicationScene` |
| `LaplaceExpansion.py` | 行列式拉普拉斯展开 · Laplace Expansion | `LaplaceExpansion` |
| `cauchy_binet_manim.py` | 柯西-比内公式 · Cauchy–Binet Formula | `CauchyBinetFormula` |
| `matrix_inverse_animation.py` | 逆矩阵 · Matrix Inverse | `MatrixInverseExplanation` |
| `JacobianDeterminant.py` | 雅可比行列式 · Jacobian Determinant | `JacobianDeterminant` |
| `affine_proof.py` | 仿射变换证明 · Affine Transform Proof | `AffineProof` |
| `linear_extension_theorem.py` | 线性延拓定理 · Linear Extension Theorem | `LinearExtensionScene1` |

### 复分析 · Complex Analysis

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `CauchyRiemannEquations.py` | 柯西-黎曼方程 · Cauchy–Riemann Equations | `CauchyRiemannEquations` |
| `Proof of Euler Formula change.py` | 欧拉公式证明 · Euler's Formula Proof | `EulerFormulaProof` |

### 常微分方程 · Ordinary Differential Equations

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `ODE.py` | 常微分方程 · ODE Introduction | `ODE` |
| `Ordinary Differential Equation.py` | 常微分方程 · ODE | `OrdinaryDifferentialEquation` |
| `ODESubstitutionMethods.py` | ODE 换元法 · ODE Substitution Methods | `ODESubstitutionMethods` |
| `DirectionField.py` | 方向场 · Direction Field | `DirectionField` |
| `DirectionFieldMulti.py` | 方向场图集 · Direction Field Gallery | `DirectionFieldGallery` |
| `ode_max_interval.py` | ODE 最大存在区间 · Max Existence Interval | `ODEMaxIntervalScene` |
| `Wronskian.py` | 朗斯基行列式 · Wronskian | `Wronskian` |

### 几何与曲线 · Geometry & Curves

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `ApolloniusCircleExpress.py` | 阿波罗尼奥斯圆 · Apollonius Circle | `ApolloniusCircleExpress` |
| `ArbitraryAngle.py` | 任意角 · Arbitrary Angle | `ArbitraryAngle` |
| `CircleToTriangle.py` | 圆化三角形（等积变换）· Circle to Triangle | `CircleToTriangle` |
| `circle.py` | 圆面积 · Area of a Circle | `Circle_Area` |
| `Cut.py` | 圆面积切割法 · Circle Area by Cutting | `Ultimate_Version_Circle_Area` |
| `Ultimate Version Circle Area.py` | 圆面积终极版 · Circle Area (Ultimate) | `Ultimate_Version_Circle_Area` |
| `EllipsePerpendicularSegments.py` | 椭圆垂直径段 · Ellipse Perpendicular Segments | `EllipsePerpendicularSegments` |
| `ellipsoid.py` | 椭球面（3D）· Ellipsoid | `Ellipsoid` |
| `heart.py` | 心形曲线 · Heart Curve | `HeartCurve` |
| `archimedean_spiral.py` | 阿基米德螺线 · Archimedean Spiral | `ArchimedeanSpiral` |
| `RightTriangle.py` | 直角三角形 · Right Triangle | `RightTriangle` |
| `RightTriangleWithMidsegment.py` | 直角三角形中位线 · Right Triangle Midsegment | `RightTriangleWithMidsegment` |
| `SatelliteDishAnimation.py` | 卫星天线（抛物面）· Satellite Dish | `SatelliteDishAnimation` |
| `三角函数.py` | 三角函数单位圆（3D）· Trig Unit Circle | `TrigCircle3D` |

### 坐标变换与可视化 · Coordinate Transform & Visualization

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `CoordinateTransform.py` | 坐标变换与雅可比 · Coordinate Transform & Jacobian | `CoordinateTransform` |
| `ax.py` | 平滑坐标系 · Smooth Coordinate System | `SmoothCoordinateSystem` |
| `vortex_animation.py` | 3D 涡旋 · 3D Vortex | `ThreeDVortex` |

### 代数与不等式 · Algebra & Inequalities

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `SolveInequality.py` | 解不等式 · Solving Inequalities | `SolveInequalityProblem` |
| `SolveInequalityProblem.py` | 不等式问题 · Inequality Problem | `SolveInequalityProblem` |
| `MultiLinearRecurrence.py` | 多元线性递推 · Multi-Linear Recurrence | `MultiLinearRecurrence` |

### 算法 · Algorithms

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `BinarySearchExplanation.py` | 二分查找 · Binary Search | `BinarySearchExplanation` |
| `OPENGL.py` | 二分查找（OpenGL）· Binary Search (OpenGL) | `BinarySearchDemo` |

### 示例与测试 · Examples & Tests

| 脚本 · Script | 主题 · Topic | 场景类 · Scene |
| --- | --- | --- |
| `SquareToCircle.py` | 方变圆（入门示例）· Square to Circle | `SquareToCircle` |
| `sample.py` | 变换示例 · Transform Example | `TransformExample` |
| `new.py` | 三角函数 3D（草稿）· Trig 3D (draft) | `TrigCircle3D` |
| `TA.py` / `Test.py` | 测试场景 · Test scenes | `Test` |
| `cirecle.py` / `test2.py` | 草稿与测试 · Drafts & tests | `Tem` / `EulerFormulaProof` |

## 🚀 运行方法 · Usage

### 1. 安装依赖 · Install dependencies

```bash
# 安装 ManimCommunity / Install ManimCommunity
pip install manim
```

还需安装系统依赖：**LaTeX**（MiKTeX / TeX Live，用于公式渲染）与 **FFmpeg**（用于视频编码）。
Additional system dependencies: **LaTeX** (MiKTeX / TeX Live, for math formulas) and **FFmpeg** (for video encoding).

### 2. 渲染动画 · Render an animation

```bash
# 低质量预览（快速）· Low quality preview (fast)
manim -pql <script>.py <SceneClass>

# 高质量渲染 · High quality render
manim -pqh <script>.py <SceneClass>
```

示例 · Example:

```bash
manim -pql LagrangeMeanValueTheorem.py LagrangeMeanValueTheorem
```

参数说明：`-p` 预览，`-ql` 低质量，`-qh` 高质量；`<SceneClass>` 见上方各表。
Flags: `-p` preview, `-ql` low quality, `-qh` high quality; `<SceneClass>` is listed in the tables above.

## 📦 依赖 · Dependencies

- Python 3.8+
- ManimCommunity (`manim`)
- LaTeX（公式渲染 · for math formulas）
- FFmpeg（视频编码 · for video encoding）

## 📁 目录结构 · Directory Structure

```text
manimce code/
├── *.py              # 动画脚本 · animation scripts
├── media/            # 渲染输出（已 gitignore）· render output (gitignored)
├── __pycache__/      # Python 缓存（已 gitignore）· Python cache (gitignored)
├── .gitignore
└── README.md
```

## 🤝 贡献 · Contributing

欢迎提 Issue 或 PR 补充新的动画脚本或改进现有动画。新增脚本请遵循现有的命名与代码风格。
Issues and PRs are welcome to add new animations or improve existing ones. Please follow the existing naming and code style for new scripts.

## 📄 许可 · License

个人学习项目，仅供交流学习。
Personal learning project, for educational use only.
