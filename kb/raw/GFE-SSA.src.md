# 地下结构动力分析软件

# GFE-SSA

# ——技术手册

杜修力院士科研团队

广州颖力科技有限公司

2022 年 08 月

V1.0

# 目录

# 前言....-5-

# 第 1 章 地下结构抗震分析方法……-7-

# 1.1 时程分析方法....-7-

1.1.1 控制方程 ..... - 7 -  
1.1.2 人工边界条件 ..... - 9 -  
1.1.3 场地地震反应分析 ..... - 10 -  
1.1.4 地震动输入....- 11 -  
1.1.5 材料非线性本构模型.... - 12 -  
1.1.6 非线性分析的初始应力条件 ..... - 12 -

# 1.2 简化分析方法....-13-

1.2.1 反应加速度法 ..... - 13 -  
1.2.2 反应位移法....-13-

# 第 2 章 典型地铁车站地下结构信息....- 17 -

2.1 车站结构....-17-  
2.2 场地条件....-18-  
2.3 输入地震动....-19-

# 第 3 章 二维时程分析方法……- 21 -

# 3.1 软件操作....-21-

3.1.1 导入结构 ydb 模型.... - 21 -  
3.1.2 创建土体材料及几何....-23-  
3.1.3 整体模型组装....-26-

3.1.4 分析步设置.... - 29 -  
3.1.5 网格划分 ..... - 30 -  
3.1.6 土-结构相互作用设置 ..... - 31 -  
3.1.7 人工边界设置....-33-  
3.1.8 场地地震反应分析与地震动输入.... - 34 -  
3.1.9 场输出设置....-36-  
3.1.10 设置工况并创建任务提交计算 ..... - 38 -

3.2 场地地震反应分析结果....-41-  
3.3 E2 地震线性时程分析结果....- 43 -

3.3.1 结构内力 ..... - 43 -  
3.3.2 结构变形 ..... - 46 -

3.4 E3 地震非线性时程分析结果....-48-

3.4.1 结构损伤 ..... - 48 -  
3.4.2 结构变形 ..... - 50 -

3.5 土层液化对分析结果的影响 ..... - 51 -

3.5.1 层间位移角....-52-  
3.5.2 孔压比....-52-  
3.5.3 结构损伤 ..... - 55 -

# 第 4 章 反应加速度法....- 57 -

4.1 软件操作....-57-

4.1.1 场地地震反应分析与有效反应加速度.... - 57 -  
4.1.2 施加边界条件与惯性力荷载....-62-

4.2 计算结果....-67-

4.2.1 结构内力 ..... - 68 -  
4.2.2 结构变形 ..... - 70 -

# 第 5 章 反应位移法....- 73 -

5.1 软件操作....-73-

5.1.1 场地地震反应分析与三类荷载 ..... - 73 -  
5.1.2 施加边界条件、地基弹簧和三类荷载....-85-

5.2 计算结果....-92-

5.2.1 结构内力 ..... - 93 -  
5.2.2 结构变形 ..... - 95 -

# 第 6 章 三维时程分析方法....- 99 -

6.1 软件操作....-99-  
6.2 E2 地震线性时程分析结果....- 99 -

6.2.1 结构内力 ..... - 100 -  
6.2.2 结构变形 ..... - 114 -

6.3 E3 地震非线性时程分析结果....- 116 -

6.3.1 结构损伤 ..... - 116 -  
6.3.2 结构变形 ..... - 130 -

6.4 土层液化对分析结果的影响 ..... - 131 -

6.4.1 层间位移角....-131-  
6.4.2 孔压比....-132-

# 第 7 章 结论....- 135 -

# 附录一：重力荷载作用静力分析....-137-

附录 1.1 二维模型....-137-

附录 1.2 三维模型....-140-

# 附录二：模态分析 …… - 147 -

附录 2.1 二维模型 ..... - 147 -

附录 2.2 三维模型....-151-

# 前言

随着国民经济持续快速发展以及西部大开发和一带一路战略实施，我国土木基础设施工程建设特别是地下结构和长大隧道建设规模已位居世界首位，并将保持长期大规模高速发展。近年来，世界范围内发生了多次地下结构震害事例，包括1995年日本神户地震，1999年中国台湾集集地震，1999年土耳其科贾埃里地震以及2008年中国汶川地震等。日本神户大地震中，地铁区间隧道及地铁车站遭受了严重破坏，甚至出现大开地铁车站完全塌毁的震害事例，地下结构抗震问题受到关注。我国已颁布实施了地下结构抗震设计规范，如《城市轨道交通结构抗震设计规范》（GB 50909-2014）和《地下结构抗震设计标准》（GB/T51336-2018）。地下结构抗震分析与设计需要考虑土与结构动力相互作用，涉及时程分析方法、反应加速度法和反应位移法等。现有软件尚未集成上述方法，前后处理操作繁琐，三维土-结构系统模型计算效率低。工欲善其事，必先利其器。

广州颖力科技有限公司自主研发了地下结构动力分析软件 GFE-SSA。该软件由有限元求解器模块和前处理模块组成，并可与结构专业设计软件无缝对接进行结构前后处理。GFE 软件的优势与功能特色如下：

（1）“准”一集成了先进的土-结构动力相互作用分析模型与方法，保证计算结果准确。软件的各类单元、本构模型、相互作用、求解算法等对标国际主流通用有限元软件；软件集成了动力人工边界条件、场地地震反应分析、地震动输入等土-结构相互作用分析方法；软件集成了我国地下结构抗震设计规范要求的各类分析方法，包括二维和三维以及线性和非线性时程分析方法、反应加速度法、反应位移法等。  
（2）“快”一采用了多 GPU 并行计算的显式动力求解和编程架构，保证计算过程快速。软件采用 CPU+GPU 异构并行计算的显式动力分析技术，其计算速度是多 CPU 并行计算速度的 10 倍以上。  
（3）“简”一简化了土与结构一体化建模，可进行构件设计并生成计算书，操作简便。可将结构专业设计软件建立的结构模型导入 GFE 软件，之后在 GFE 软件内简单完成土-结构系统建模；基于 GFE 计算得到的结构结果可以完成效应组合、截面验算、配筋、生成计算书等；GFE 软件也支持导入其他有限元软件的计算模型。

本手册首先简介地下结构抗震分析方法；然后以某地铁车站为例，介绍各类分析方法的GFE软件操作并给出计算结果，与主流商业有限元软件结果对比说明GFE软件的优势。

# 第1章 地下结构抗震分析方法

地下结构地震反应分析需要考虑土体与结构之间的动力相互作用。时程分析采用整体分析方法，也称有限元直接法，即建立结构及其周围土体的整体有限元模型，在土体截断边界处施加人工边界条件并输入地震动。本章首先介绍时程分析方法，包括黏弹性人工边界条件、场地地震反应分析、地震动输入、材料非线性本构模型及初始地应力条件等。之后介绍地下结构抗震设计规范要求的简化分析方法，包括反应加速度法和反应位移法。

# 1.1 时程分析方法

# 1.1.1 控制方程

地下结构地震反应分析的整体模型如图 1.1-1 所示。整体分析方法的思路是引入虚拟边界（称作人工边界）截去土体的无限域部分，取出地下结构及其附近土体形成有限域，采用有限元等数值方法进行模拟。

![](../assets/GFE-SSA/cc41761de5f3002f0c42fcbc8de634d2a2a22e51dc91fa0059dd51ea0aaa5987.jpg)

<details>
<summary>text_image</summary>

人工边界
地下结构
土体
人工边界
倾斜入射地震动
</details>

图 1.1-1 地下结构地震反应分析的整体分析模型示意图

根据有限元理论，线弹性有限域的动力有限元方程可以写为：

$$
\left[ \begin{array}{l l} \mathbf {M} _ {R R} & \mathbf {M} _ {R B} \\ \mathbf {M} _ {B R} & \mathbf {M} _ {B B} \end{array} \right] \left\{ \begin{array}{l} \ddot {\mathbf {u}} _ {R} \\ \ddot {\mathbf {u}} _ {B} \end{array} \right\} + \left[ \begin{array}{l l} \mathbf {C} _ {R R} & \mathbf {C} _ {R B} \\ \mathbf {C} _ {B R} & \mathbf {C} _ {B B} \end{array} \right] \left\{ \begin{array}{l} \dot {\mathbf {u}} _ {R} \\ \dot {\mathbf {u}} _ {B} \end{array} \right\} + \left[ \begin{array}{l l} \mathbf {K} _ {R R} & \mathbf {K} _ {R B} \\ \mathbf {K} _ {B R} & \mathbf {K} _ {B B} \end{array} \right] \left\{ \begin{array}{l} \mathbf {u} _ {R} \\ \mathbf {u} _ {B} \end{array} \right\} = \left\{ \begin{array}{l} \mathbf {0} \\ \mathbf {f} _ {B} \end{array} \right\} \tag {1.1-1}
$$

其中，下标 B 和 R 分别表示人工边界自由度和其余自由度；u、 $\dot{u}$ 和 $\ddot{u}$ 分别表示位移、速度和加速度向量；M、C 和 K 分别是质量、阻尼和刚度矩阵； $f_{B}$ 是地震荷载作用下人工边界处被截去的无限域对有限域的作用力。

将人工边界处的总反应分解为散射场和自由场两部分，作用力、位移和速度可以分别分解

为:

$$
\mathbf {f} _ {B} = \mathbf {f} _ {B} ^ {S} + \mathbf {f} _ {B} ^ {F} \tag {1.1-2}
$$

$$
\mathbf {u} _ {B} = \mathbf {u} _ {B} ^ {S} + \mathbf {u} _ {B} ^ {F} \tag {1.1-3}
$$

$$
\dot {\mathbf {u}} _ {B} = \dot {\mathbf {u}} _ {B} ^ {S} + \dot {\mathbf {u}} _ {B} ^ {F} \tag {1.1-4}
$$

其中，自由场用上标 F 表示，由场地反应分析确定；散射场用上标 S 表示，为未知量。

散射场从有限域通过人工边界辐射或者透射进入无限域，采用人工边界条件来模拟，以黏弹性人工边界为例，散射场的作用力和运动关系可以写为：

$$
\mathbf {f} _ {B} ^ {S} = - \mathbf {K} _ {B} ^ {\infty} \mathbf {u} _ {B} ^ {S} - \mathbf {C} _ {B} ^ {\infty} \dot {\mathbf {u}} _ {B} ^ {S} \tag {1.1-5}
$$

其中， $K_{B}^{\infty}$ 和 $C_{B}^{\infty}$ 分别是黏弹性人工边界的弹簧和阻尼系数矩阵，具体取值方法见下一小节。

将式（1.1-3）和式（1.1-4）代入式（1.1-5），然后代入式（1.1-2），最终代入式（1.1-1），整理得：

$$
\left[ \begin{array}{l l} \mathbf {M} _ {R R} & \mathbf {M} _ {R B} \\ \mathbf {M} _ {B R} & \mathbf {M} _ {B B} \end{array} \right] \left\{ \begin{array}{l} \ddot {\mathbf {u}} _ {R} \\ \ddot {\mathbf {u}} _ {B} \end{array} \right\} + \left[ \begin{array}{c c} \mathbf {C} _ {R R} & \mathbf {C} _ {R B} \\ \mathbf {C} _ {B R} & \mathbf {C} _ {B B} + \mathbf {C} _ {B} ^ {\infty} \end{array} \right] \left\{ \begin{array}{l} \dot {\mathbf {u}} _ {R} \\ \dot {\mathbf {u}} _ {B} \end{array} \right\} + \tag {1.1-6}
$$

$$
\left[ \begin{array}{c c} \mathbf {K} _ {R R} & \mathbf {K} _ {R B} \\ \mathbf {K} _ {B R} & \mathbf {K} _ {B B} + \mathbf {K} _ {B} ^ {\infty} \end{array} \right] \left\{ \begin{array}{c} \mathbf {u} _ {R} \\ \mathbf {u} _ {B} \end{array} \right\} = \left\{ \begin{array}{c} \mathbf {0} \\ \mathbf {K} _ {B} ^ {\infty} \mathbf {u} _ {B} ^ {F} + \mathbf {C} _ {B} ^ {\infty} \dot {\mathbf {u}} _ {B} ^ {F} + \mathbf {f} _ {B} ^ {F} \end{array} \right\}
$$

整体分析方法可以考虑有限域内土体和结构的材料和接触等非线性力学行为。此时需要同时考虑地震和体力的共同作用，并且给定体力作用下的初始应力状态作为地震反应分析的初始条件。以式（1.1-6）为例，非线性问题的有限元方程可以进一步写为：

$$
\begin{array}{l} \left[ \begin{array}{c c} \mathbf {M} _ {R R} & \mathbf {M} _ {R B} \\ \mathbf {M} _ {B R} & \mathbf {M} _ {B B} \end{array} \right] \left\{ \begin{array}{c} \ddot {\mathbf {u}} _ {R} \\ \ddot {\mathbf {u}} _ {B} \end{array} \right\} + \left[ \begin{array}{c c} \mathbf {C} _ {R R} & \mathbf {C} _ {R B} \\ \mathbf {C} _ {B R} & \mathbf {C} _ {B B} + \mathbf {C} _ {B} ^ {\infty} \end{array} \right] \left\{ \begin{array}{c} \dot {\mathbf {u}} _ {R} \\ \dot {\mathbf {u}} _ {B} \end{array} \right\} + \left[ \begin{array}{c c} \mathbf {0} & \mathbf {K} _ {R B} \\ \mathbf {K} _ {B R} & \mathbf {K} _ {B B} + \mathbf {K} _ {B} ^ {\infty} \end{array} \right] \left\{ \begin{array}{c} \mathbf {u} _ {R} \\ \mathbf {u} _ {B} \end{array} \right\} \\ + \left[ \begin{array}{c c} \mathbf {f} _ {R} \left(\mathbf {u} _ {R}, \dot {\mathbf {u}} _ {R}\right) & \mathbf {0} \\ \mathbf {0} & \mathbf {0} \end{array} \right] = \left\{ \begin{array}{c} \mathbf {0} \\ \mathbf {K} _ {B} ^ {\infty} \mathbf {u} _ {B} ^ {F} + \mathbf {C} _ {B} ^ {\infty} \dot {\mathbf {u}} _ {B} ^ {F} + \mathbf {f} _ {B} ^ {F} \end{array} \right\} + \left\{ \begin{array}{c} \mathbf {b} _ {R} \\ \mathbf {b} _ {B} \end{array} \right\} + \left\{ \begin{array}{c} \mathbf {0} \\ \mathbf {f} _ {B} ^ {b} \end{array} \right\} \tag {1.1-7} \\ \end{array}
$$

其中， $\mathbf{f}_{R}(\mathbf{u}_{R},\dot{\mathbf{u}}_{R})$ 是非线性内力；b 是体力； $f_{B}^{b}$ 是体力作用下无限域对有限域的作用力。

土-结构动力相互作用时程分析方法的主要步骤包括:

（1）建立土-结构系统的有限元模型；  
（2）施加人工边界条件；  
（3）进行场地地震反应分析，计算并施加人工边界处的等效地震荷载；  
（4）非线性分析还要计算并考虑地震作用前的初始应力条件；  
（5）采用显式或者隐式时间积分算法求解。

# 1.1.2 人工边界条件

《城市轨道交通结构抗震设计规范》（GB50909-2014）中要求地基无限性的模拟应通过在区域边界上引入人工边界加以实现，一般可采用黏性边界或黏弹性边界等合理的边界条件，且侧向人工边界应避免采用固定或自由等不合理的边界条件。黏弹性边界在人工边界的每个自由度上施加一个远端固定的并联弹簧-阻尼器系统，如图 1.1-2 所示。

![](../assets/GFE-SSA/44f3d0e9123269e85a66b7c190b8ef40776e9a88a397f89738e81075d85224b0.jpg)

<details>
<summary>text_image</summary>

FEM boundary
CN
KN
KT
CT
FEM boundary
FEM mesh
Node on FEM boundary
</details>

(a) 二维黏弹性边界

![](../assets/GFE-SSA/a04d3d31d2ee57605aec21ba65058fabfa04125319b8b1ea0249a65fe887c100.jpg)

<details>
<summary>text_image</summary>

N
C_Ni
K_Ni
C_Ti
T_1
i
K_Ti
C_Ti
T_2
y
T_2
C_Ti
K_Ti
C_Ni
T_1
i
T_2
C_Ti
K_Ti
C_Ti
T_1
N
T_2
C_Ti
K_Ti
C_Ni
T_1
i
T_2
C_Ti
K_Ti
C_Ti
T_1
N
T_2
C_Ti
K_Ti
C_Ni
T_1
i
T_2
C_Ti
K_Ti
C_Ni
N
</details>

(b) 三维黏弹性边界  
图 1.1-2 黏弹性边界

二维黏弹性人工边界的弹簧-阻尼元件参数为:

法向 $K_{N}=\frac{1}{1+A}\frac{\lambda+2G}{2r},\quad C_{N}=B\rho c_{p}$ (1.1-8)

切向 $K_{T}=\frac{1}{1+A}\frac{G}{2r},\quad C_{T}=B\rho c_{S}$ (1.1-9)

三维黏弹性人工边界的弹簧-阻尼元件参数为:

法向 $K_{N}=\frac{1}{1+A}\frac{\lambda+2G}{r},\quad C_{N}=B\rho c_{p}$ (1.1-10)

切向

$$
K _ {T} = \frac {1}{1 + A} \frac {G}{r}, \quad C _ {T} = B \rho c _ {s} \tag {1.1-11}
$$

式中， $\rho$ 为介质密度； $c_{p}$ 和 $c_{s}$ 分别为P波和S波波速；长度r可取为近场结构几何中心到该人工边界点所在边界线或面的距离；参数A、B的较优建议值为A=0.8、B=1.1。

GFE 软件提供了二维和三维黏弹性人工边界条件，考虑了模型中土层性质变化及模型边界几何形状非规则性，可快速实现黏弹性人工边界条件的自动施加。

# 1.1.3 场地地震反应分析

在利用时程分析方法开展土-结构动力相互作用分析之前，需要进行场地地震反应分析，将场地反应结果作为土-结构相互作用分析的地震荷载，因而场地反应分析结果的准确性至关重要。

局部场地通常可以简化为水平成层土体模型，在地震动作为平面体波竖直入射情况下，场地地震反应分析属于空间一维问题，即所谓一维场地地震反应分析。土体在地震作用下表现出显著的材料非线性特性，工程中通常采用等效线性化方法模拟土体的材料非线性行为。EERA和SHAKE是典型的等效线性一维场地地震反应分析程序。

![](../assets/GFE-SSA/3804274b2dbcbe0fe8d94d46a9f7b934f031185bcf32d7701e962476cea322d0.jpg)

<details>
<summary>text_image</summary>

基岩地表运动 2uᵢ
场地地表运动 uₛ
一维波动
工程场地
基岩
基岩运动 uᵢ + uᵣ
一维波动
基岩
入射地震动 uᵢ
一维场地地震反应分析
</details>

图 1.1-3 一维场地地震反应分析

一维场地地震反应分析如图 1.1-3 所示，入射地震动为 $u_{i}$ 。忽略地震动在半空间基岩中的传播时间，则基岩地表运动为 $2u_{i}$ 。入射地震动传播进入工程场地获得场地地震反应，场地地表运动为 $u_{s}$ ，基岩运动为 $u=u_{i}+u_{r}$ 。实际工程中，可能给定基岩地表运动、基岩运动或者场地地表运动三个不同位置的地震动作为输入地震动。若已知基岩地表地震动，可将其折半在基岩处输入；若已知基岩地震动，可将其强制在基岩处；若已知场地地表地震动，则需反演得到场地地震反应（等效线性化分析中可以通过正演计算实现）。

GFE 软件提供了等效线性化一维场地地震反应分析模块，可快速实现场地地震反应分析，

并能自动转化为后续土-结构相互作用分析的地震荷载，实现场地反应分析与土-结构相互作用分析间的无缝对接，无需数据的导入导出，操作简便。

![](../assets/GFE-SSA/ff206a7232f4ea4cc8968d18f60daaeb7a6c26ea566a1bb99e691a020f9a9ef0.jpg)  
(a) 平面波 SV 波与 P 波二维输入

![](../assets/GFE-SSA/fab745f33cd5489fbd55c2a7770df36c048e2a279d71a23df6faa9f7323a72ec.jpg)

(b) 平面波 SV 波与 P 波立方体模型三维输入  
![](../assets/GFE-SSA/90b6d0c88249c735d5b84669430b3596ffbf9e93750aa6813b809220c1619d2b.jpg)  
(c) 平面波 SV 波柱体模型与半球模型三维输入  
图 1.1-4 地震动输入算例

# 1.1.4 地震动输入

从式（1.1-7）中可以看到，土-结构相互作用分析的地震荷载是作用于人工边界节点处由场地反应转化的节点力时程，即：

$$
\mathbf {f} _ {B} = \mathbf {K} _ {B} ^ {\infty} \mathbf {u} _ {B} ^ {F} + \mathbf {C} _ {B} ^ {\infty} \dot {\mathbf {u}} _ {B} ^ {F} + \mathbf {f} _ {B} ^ {F} \tag {1.1-12}
$$

GFE 软件提供了基于黏弹性人工边界条件的地震动输入方法，可以考虑不同地震波型（P波、SV 波、SH 波）和不同人工边界几何形状，如图 1.1-4 所示。地震动输入方法实现场地反

应分析与土-结构相互作用分析间的无缝对接，无需数据的导入导出，操作简便。

# 1.1.5 材料非线性本构模型

《城市轨道交通结构抗震设计规范》（GB50909-2014）的3.3.1节中规定“对于高架区间结构、地下车站结构、重点设防类和标准设防类的高架车站结构、重点设防类的区间隧道结构在进行抗震性能Ⅱ要求的设计计算中需进行非线性时程分析”。GFE软件提供了钢筋混凝土和土体的材料非线性本构模型。

对于钢筋混凝土地下结构，GFE 软件在纤维梁单元和分层壳单元中引入了钢筋弹塑性本构模型和混凝土塑性损伤本构模型，可有效模拟钢筋混凝土结构材料非线性力学行为。此外，GFE 软件中预设了 Q235-Q460 钢材、HPB235-HPB500 钢材、C30-C80 混凝土等多种常用材料的非线性模型参数，方便用户直接调用。

对于土体，GFE 软件提供了经典的摩尔库伦模型以及可考虑土体动力特性的 Davidenkov 本构模型。

# 1.1.6 非线性分析的初始应力条件

由式（1.1-7）可知，非线性时程分析需要考虑地震作用前的体力引起的初始应力条件。考虑初始应力条件的土-结构相互作用分析过程为：（1）对土-结构系统模型的人工边界施加法向约束，施加体力进行静力分析；（2）将获得的应力和边界约束力施加于土-结构系统地震反应分析模型，进行体力和地震共同作用下的动力分析。

GFE 软件实现了上述静力和动力两个连续分析过程的连续统一，避免了两个分析过程间数据传递的用户操作。图 1.1-5 给出仅考虑重力而不施加地震荷载时某一水平成层场地的两次静力后的计算结果，由图可见，应力场与自重应力的理论结果一致，且位移场基本为零，说明自重作用下初始应力条件的准确性。

![](../assets/GFE-SSA/04349a9b3f972e826412ecddfa520c0514d375b7d464e7f3ec7be4409c8706d1.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 9.5e3 |
| Orange | ~8.5e3 |
| Yellow | ~7.8e3 |
| Green | ~7.2e3 |
| Cyan | ~6.5e3 |
| Blue | 7.79e5 |
</details>

(a) 竖向应力云图

![](../assets/GFE-SSA/ba50740a52aa2fc16755f6a438a091c4df0170a3f948f3769139680f03b9e8c1.jpg)

<details>
<summary>line</summary>

| 深度 (m) | 竖向应力 (MPa) |
| --- | --- |
| 0 | 0.0 |
| 7 | ~0.08 |
| 14 | ~0.15 |
| 21 | ~0.22 |
| 35 | ~0.32 |
| 42 | ~0.75 |
</details>

(b) 竖向应力沿深度变化曲线  
![](../assets/GFE-SSA/8896ece862cc9fd64197b0167594e9979de28cefcef3f14cdd42141470a6082f.jpg)

<details>
<summary>natural_image</summary>

3D thermal or stress distribution visualization on a rectangular block, with color-coded values ranging from -4.2e-6 (blue) to 1.35e-6 (red)
</details>

(c) 竖向位移云图  
图 1.1-5 自重作用下某水平成层场地的初始状态

# 1.2 简化分析方法

# 1.2.1 反应加速度法

反应加速度法通常用于地下结构二维横断面地震反应分析，是一种简化的静力分析方法。反应加速度法与时程分析方法一样，采用土-结构系统整体分析模型，或称为土层-结构模型，计算模型如图 1.2-1 所示。结构和土体分别采用梁单元和平面应变单元模拟，模型底边界固定、侧边界采用水平滑移边界，整个模型受惯性力荷载作用。

![](../assets/GFE-SSA/dfb8364052eee3da83214695747ab8c6d2d4447ee109a394d4df57d456d50394.jpg)

<details>
<summary>text_image</summary>

水平滑移边界
惯性力
水平滑移边界
固定边界
</details>

图 1.2-1 反应加速度法计算模型

惯性力的计算方法如下。首先进行一维场地地震反应分析，提取地下结构顶、底板位置发生最大相对位移时刻土层的剪应力分布，通过式（1.2-1）计算不同土层深度处的有效反应加速度，然后将其以惯性力方式作用于整个计算模型上进行静力计算。

$$
a _ {i} = \frac {\tau_ {i} - \tau_ {i - 1}}{\rho_ {i} h _ {i}} \tag {1.2-1}
$$

式中： $a_{i}$ 为第 i 层土单元的有效反应加速度； $\rho_{i}$ 为第 i 层土单元的密度； $h_{i}$ 为第 i 层土单元的厚度； $\tau_{i-1}$ 、 $\tau_{i}$ 分别为地下结构发生最大变形时第 i 层土单元顶部与底部的剪应力。

# 1.2.2 反应位移法

反应位移法通常用于地下结构二维横断面地震反应分析，是一种简化的静力分析方法。反应位移法采用土-结构相互作用的子结构分析模型，或称为荷载-结构模型，计算模型如图 1.2-2 所示。结构采用梁单元模拟，土体采用施加于结构周围的地基弹簧模拟，结构-弹簧系统承受三类荷载：土层相对位移、结构惯性力和结构周围土层剪力。

![](../assets/GFE-SSA/6436cfedd584b2d5e28101b87b7472ecd05934515363fa080e0977e7561eae47.jpg)

<details>
<summary>text_image</summary>

土层剪力
土层剪力
惯性力
土层剪力
地基弹簧
土层位移
土层位移
</details>

图 1.2-2 反应位移法计算模型

地基弹簧刚度可由如下两种方法确定。第一种方法是利用基床系数由式（1.2-2）确定：

$$
k = K L d \tag {1.2-2}
$$

式中：k 为压缩或剪切地基弹簧刚度（N/m）；K 为基床系数（N/m³）；L 为沿结构横向的计算长度（m）；d 为沿结构纵向的计算长度（m）。第二种方法是静力有限元法，如图 1.2-3 所示，在去除了结构的孔洞土体中的四个侧面分别施加垂直向和水平向的作用力，然后根据各侧面的位移来确定各面的地基弹簧刚度。

![](../assets/GFE-SSA/f74788079cf0e8818d0fe8caf058551dff6cd2311ad77ef87fcddfcbdd68d525.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
  A["Grid Grid"] --> B["Step 1: q"]
  B --> C["Step 2: q"]
  C --> D["Step 3: q"]
  D --> E["Step 4: q"]
```
</details>

图 1.2-3 采用静力有限元法计算地基弹簧刚度系数

结构-弹簧系统承受的三类荷载由场地地震反应分析确定。进行一维场地地震反应分析，提取地下结构顶、底板位置发生最大相对位移时刻土层位移、加速度和剪应力分布，分别按照如下方法计算三类荷载。

（1）土层相对位移为：

$$
u ^ {\prime} (z) = u (z) - u (z _ {B}) \tag {1.2-3}
$$

式中： $u'$ （z）为深度z处相对于结构底部的自由土层相对位移（m）；u（z）为深度z处自由土层地震反应位移（m）； $u(z_{B})$ 为结构底部 $z_{B}$ 处的自由土层地震反应位移（m）。土层相对位移强制于地基弹簧远端。

(2) 结构惯性力:

$$
f _ {i} = m _ {i} \ddot {u} _ {i} \tag {1.2-4}
$$

式中： $f_{i}$ 为结构 i 单元上作用的惯性力（N）； $m_{i}$ 为结构 i 单元的质量（kg）； $u_{i}$ 为自由土层对应于结构 i 单元位置处的加速度（ $m/s^{2}$ ）。结构惯性力也可作为集中力施加在结构形心上。

（3）结构周围土层剪力可以将相应位置处的土层剪应力转化为节点力得到。矩形结构侧壁剪力也可进行如下简化计算：

$$
\tau_ {s} = \frac {\tau_ {U} + \tau_ {B}}{2} \tag {1.2-5}
$$

式中： $\tau_{S}$ 为矩形结构侧壁所受的剪力（Pa）； $\tau_{U}$ 和 $\tau_{B}$ 分别为结构顶底板位置处自由土层的剪力（Pa）。

# 第2章 典型地铁车站地下结构信息

选用某地铁车站地下结构抗震分析案例测试 GFE 软件。本章介绍该地铁车站结构、场地条件以及输入地震动等参数信息。

# 2.1 车站结构

某车站为两层三跨结构，层高均为7m，结构埋深为4m。结构中柱混凝土强度等级为C50，其余构件混凝土强度等级为C35；结构外墙厚度700mm，底板厚度900mm，中板厚度为400mm，顶板厚度为750mm，中柱的横向和纵向尺寸分别为700mm和1000mm，中柱间距为7500mm。线弹性分析中，混凝土材料为弹性模型。非线性性分析中，混凝土材料为混凝土损伤模型，混凝土构件配筋由盈建科软件给出，混凝土和钢筋基本物理参数按照《混凝土结构设计规范》选取，如表2.1-1和表2.1-2所示。结构和结构横断面分别如图2.1-1和图2.1-2所示。

表 2.1-1 结构混凝土材料参数

<table><tr><td>结构材料</td><td>弹性模量(kPa)</td><td>泊松比</td><td>容重(t/m3)</td><td>抗压强度(kPa)</td><td>峰值压缩应变</td><td>压缩软化系数</td><td>抗拉强度(kPa)</td><td>峰值拉伸应变</td><td>拉伸软化系数</td></tr><tr><td>C35</td><td>3.15e07</td><td>0.2</td><td>2.5</td><td>23400</td><td>0.0015323</td><td>0.95930</td><td>2200</td><td>9.9984e-05</td><td>1.51144</td></tr><tr><td>C50</td><td>3.45e07</td><td>0.2</td><td>2.5</td><td>32400</td><td>0.0016790</td><td>1.49983</td><td>2640</td><td>1.1018e-04</td><td>2.17510</td></tr></table>

表 2.1-2 结构钢筋材料参数

<table><tr><td>结构材料</td><td>弹性模量(kPa)</td><td>泊松比</td><td>容重(t/m3)</td><td>屈服应力(kPa)</td><td>塑性应变</td></tr><tr><td rowspan="2">Q235</td><td rowspan="2">2.06e08</td><td rowspan="2">0.25</td><td rowspan="2">7.8</td><td>235000</td><td>0</td></tr><tr><td>325000</td><td>0.025</td></tr></table>

![](../assets/GFE-SSA/6c7ff38cac78dc7e24ffa2100b1c3533adf1e208f88770cd618fcb3634d6561e.jpg)

<details>
<summary>natural_image</summary>

3D rendering of a green rectangular structure with a blue grid pattern and a small white dot at the top (no text or symbols)
</details>

图 2.1-1 结构模型

![](../assets/GFE-SSA/f54755b924dc11e69c8fd4b6a56d4fa6b49acbf8dae73ab824c22c4a5159d281.jpg)

<details>
<summary>text_image</summary>

750
6425
14000
700
6800
7500
6800
700
900
6350
400
KZ1
700×1000
KZ1
700×1000
KZ1
700×1000
</details>

图 2.1-2 结构横断面

# 2.2 场地条件

线弹性分析中，土层参数如表 2.2-1 所示，各层土的动剪切模量比和阻尼比随剪应变变化曲线如图 2.2-1 所示。非线性性分析中，土体材料非线性可以分别采用 Davidenkov 本构模型和 Mohr-Coulomb 本构模型模拟，两种本构模型参数如表 2.2-2 和表 2.2-3 所示。

表 2.2-1 土层弹性参数信息

<table><tr><td rowspan="2">名称</td><td rowspan="2">层号</td><td colspan="4">材料参数</td></tr><tr><td>厚度(m)</td><td>弹性模量(kPa)</td><td>泊松比</td><td>容重(t/m3)</td></tr><tr><td>粉质黏土素填土</td><td>1</td><td>5</td><td>175574</td><td>0.35</td><td>1.90</td></tr><tr><td>粉质黏土</td><td>2</td><td>20</td><td>380085</td><td>0.29</td><td>1.92</td></tr><tr><td>粉质黏土</td><td>3</td><td>16</td><td>504811</td><td>0.28</td><td>1.95</td></tr><tr><td>微风化石灰石</td><td>4</td><td>9</td><td>6017540</td><td>0.25</td><td>2.30</td></tr></table>

![](../assets/GFE-SSA/3978f3a5f527c45ef8d3bded937b6b2a4a9434583f8d6063ef1c31cf950e8daa.jpg)

<details>
<summary>line</summary>

| 剪应变 | 第一层土 (G/Gmax) | 第二层土 (G/Gmax) | 第三层土 (G/Gmax) | 第一层土 (阻尼比%) | 第二层土 (阻尼比%) | 第三层土 (阻尼比%) |
| --- | --- | --- | --- | --- | --- | --- |
| 1E-5 | ~0.96 | ~0.98 | ~0.99 | ~2.1 | ~1.3 | ~1.0 |
| 1E-4 | ~0.80 | ~0.94 | ~0.95 | ~3.7 | ~2.5 | ~3.7 |
| 1E-3 | ~0.30 | ~0.74 | ~0.58 | ~8.5 | ~7.0 | ~6.3 |
| 0.01 | ~0.10 | ~0.14 | ~0.08 | ~12.0 | ~10.5 | ~8.2 |
</details>

图 2.2-1 土层动剪切模量比和阻尼比随剪应变变化曲线

表 2.2-2 Davidenkov 本构模型车站结构周围土层信息

<table><tr><td rowspan="2">名称</td><td rowspan="2">层号</td><td colspan="3">材料参数</td></tr><tr><td>A</td><td>B</td><td> $\gamma_0$ </td></tr><tr><td>粉质黏土素填土</td><td>1</td><td>1.04</td><td>0.4</td><td>0.00036</td></tr><tr><td>粉质黏土</td><td>2</td><td>1.09</td><td>0.41</td><td>0.00037</td></tr><tr><td>粉质黏土</td><td>3</td><td>1.08</td><td>0.46</td><td>0.00041</td></tr></table>

表 2.2-3 Mohr-Coulomb 本构模型车站结构周围土层信息

<table><tr><td rowspan="2">名称</td><td rowspan="2">层号</td><td colspan="3">材料参数</td></tr><tr><td>摩擦角(°)</td><td>剪胀角(°)</td><td>黏聚力(kPa)</td></tr><tr><td>粉质黏土素填土</td><td>1</td><td>8</td><td>4</td><td>10</td></tr><tr><td>粉质黏土</td><td>2</td><td>18</td><td>9</td><td>33</td></tr><tr><td>粉质黏土</td><td>3</td><td>19</td><td>9.5</td><td>35</td></tr></table>

# 2.3 输入地震动

场地地震安全性评价报告给出了基岩地表的 E2 和 E3 地震动，其加速度时程分别如图 2.3-1 和图 2.3-2 所示，分别用于线弹性和非线性分析。

![](../assets/GFE-SSA/1cf7aa7ceb1092b0b0a1600252b1d0991baf495eddcfd34af7cc94de00f51c33.jpg)

<details>
<summary>line</summary>

| 时间/s | \(加速度/m/s^{2}\) |
| --- | --- |
| 0 | 0 |
| ~4 | ~1.7 |
| ~9 | ~1.4 |
| ~18 | ~0.4 |
| ~27 | ~0.1 |
| ~36 | 0 |
| ~45 | 0 |
</details>

图 2.3-1 基岩地表 E2 地震动加速度时程

![](../assets/GFE-SSA/ac4ec3859d983dd8f2c6faf728487485e989b5034c809ab99d39c879032c268d.jpg)

<details>
<summary>line</summary>

| 时间/s | \(加速度/m/s^{2}\) |
| --- | --- |
| 0 | 0 |
| ~3 | ~2.4 |
| ~4 | ~-2.0 |
| ~6 | ~2.5 |
| ~7 | ~-2.6 |
| ~9 | ~2.0 |
| ~10 | ~-2.6 |
| ~12 | ~2.0 |
| ~13 | ~-2.8 |
| ~15 | ~2.6 |
| ~16 | ~-2.8 |
| ~18 | ~1.3 |
| ~20 | ~1.0 |
| ~22 | ~0.6 |
| ~24 | ~0.5 |
| ~26 | ~0.4 |
| ~28 | ~0.3 |
| ~30 | ~0.2 |
| ~32 | ~0.2 |
| ~34 | ~0.1 |
| ~36 | ~0.1 |
| ~38 | ~0.1 |
| ~40 | ~0.1 |
| ~42 | ~0.1 |
| ~44 | ~0.1 |
</details>

图 2.3-2 基岩地表 E3 地震动加速度时程

# 第3章 二维时程分析方法

GFE 软件集成了第一章的土-结构相互作用时程分析方法。针对第二章给出的地铁车站地下结构抗震分析案例，本章采用 GFE 软件完成二维横断面时程分析。首先介绍二维时程分析方法在 GFE 软件中的操作步骤，然后给出地铁车站地震反应计算结果。通过与某国际先进通用有限元软件（简称软件 A）的计算结果对比，验证 GFE 软件的可靠性和优势。

# 3.1 软件操作

GFE 软件进行二维时程分析的主要步骤有：导入结构 ydb 模型、创建土体材料及几何、整体模型组装、分析步设置、网格划分、土-结构相互作用设置、人工边界设置、场地地震反应分析与地震动输入、场输出设置、设置工况并创建任务提交计算。非线性与线性时程分析的操作步骤大同小异，都由上述 10 个步骤完成，只在某些步骤上略有不同：导入 ydb 模型时，非线性分析需要选择导入结构专业设计软件 YJK 配筋或默认配筋，结构材料需要选择“塑性”；创建的幅值函数需为 E3 地震动测量数据，并在地震场地反应分析的“地震水准”中勾选 E3；创建工况时，在动力分析步前需要设置模型整体重力载荷下的静力分析步以做地应力平衡。

# 3.1.1 导入结构 ydb 模型

点击【Import /导入】选择【Import YJK DB /导入 YJK 数据库】，弹出对话框中选择需要导入的 ydb 文件，点击【Open /打开】弹出导入设置对话框，根据需求进行设置或保持默认设置，点击【OK /确认】完成模型导入，如图 3.1-1 所示。

![](../assets/GFE-SSA/d921be1497231a5362938ce6e457fa5d775cd8664dcae3522845154b6a651fdf.jpg)

![](../assets/GFE-SSA/ba6b948799949aaf51c96302e5d3c089e373f515e757a053a3b63b641a9eefc0.jpg)  
图 3.1-1 ydb 模型导入

# 3.1.2 创建土体材料及几何

# （1）创建土层材料

右键点击【Materials /材料】，点击【Create/创建】弹出【Create Material /创建材料】窗口，在【Name /名称】中输入土层材料名称，点击【OK /确定】，点击【General /常规类】、【Density /密度】，在【Mass Density /质量密度】中输入土层的密度，如图 3.1-2。点击【Elasticity/弹性类】、【Elastic /弹性类】，在【Young's Modulus /杨氏模量】中输入土层的杨氏模量，在【Poisson /泊松比】里输入泊松比点击【OK /确认】，周围土体的材料创建完成，如图 3.1-3。

![](../assets/GFE-SSA/2c4f895aa2b88d8b29ec3c0779fd360acd002d0e98d7f498d4713950db68ed68.jpg)

图 3.1-2 Material /材料窗口-常规类  
![](../assets/GFE-SSA/9eebf33152bc672fbfd19d8a91bc56234b8c2add33e457eb346bce256ed15e68.jpg)  
图 3.1-3 Material /材料窗口-弹性类

# (2) 创建土层

各土层材料创建完毕后即可创建土层，具体步骤如图 3.1-4 所示。

![](../assets/GFE-SSA/a2905f075d0b7aaebe6b55afc09984b84b4e47793125c74e07ec68fd3b9e821c.jpg)  
图 3.1-4 创建土层

# （3）创建土体几何

根据土层创建土体几何，右键点击【Creat Soil/创建土体】，二维分析时选择【2D】，【Soil Layers/土层】选择上一步创建的土层，【Length/宽度】输入土体长度尺寸，点击【OK/确认】

完成土体几何创建，如图 3.1-5 所示。

![](../assets/GFE-SSA/55a0c86c54263d0141b39eb9aa21a346a4352036f53fab04bf2ef1a53c3cf009.jpg)  
图 3.1-5 创建土体几何

# 3.1.3 整体模型组装

结构、地连墙和土体模型创建完成后，需要对其进行组装，形成可用于计算的整体模型。组装过程包括调整土与结构间相对位置和对土进行裁剪操作。

# （1）调整土与结构间相对位置

可通过平移操作调整土与结构间相对位置，具体操作如图 3.1-6 所示，可通过输入平移向量或选择两几何点的方式进行平移。

![](../assets/GFE-SSA/a19d0e397763313cfcc14b0246ee2fa9aad82d3761beefd29598eb3733233b47.jpg)

<details>
<summary>text_image</summary>

Import...
Export...
Create Box
Create Cylinder
Create Sphere
1
Translate
Boolean
Operation
Rotate
Scale
Boolean
Display
View
Find
Contact
Modeling
Display
Node
Element
Surfaces
2.激活、选择视图中需要移动的对象
3.平移方式
4.输入移动向量
Geometries
Vector
0.0, 0.0, 0.0
Yes
No
Output
Total nodes: 4
Self mass: 132 000000
E:/微云/LCZL/2D/erweijiegou.ydb - GFE PrePo
不结构
导入...
导入...
导出...
CAD
Create箱体
创建圆柱形
布尔
旋转
布尔
视图
寻找
网格
查询
拾取
作业
设置
建模
显示
工具
其他
节点
单元
表面
2.激活、选择视图中需要移动的对象
3.平移方式
4.输入移动向量
几何
矢量
50,0,0
是
否
输出
</details>

图 3.1-6 平移操作

(2) 裁剪布尔操作

土与结构相对位置调整后，结构几何嵌入到土体几何中，需要对土体几何进行裁剪以得到容纳结构的空间。先根据结构外轮廓边创建面实体作为裁剪土体的工具，操作过程如图 3.1-7 所示。

![](../assets/GFE-SSA/54dadd183c868e1b7451093eee2d80886c069a019de156afbcba0e95d774c4c3.jpg)  
图 3.1-7 创建面实体

点击【Boolean Operation /布尔运算】进行布尔操作，下方选择【Cut /裁剪】操作，点击【Continue /继续】继续，按操作提示分别选择土体作为裁剪对象和刚创建的面实体作为裁剪工具，点击【OK】完成布尔操作，如图 3.1-8 所示。

![](../assets/GFE-SSA/44c4be736de0b7d63d674cd7715b614c1208d0addc3d648be87ece2e99bbd765.jpg)  
图 3.1-8 裁剪布尔操作

# 3.1.4 分析步设置

右键点击【Steps】，出现静力通用和动力显式两个选项设置，进行二维横断面动力时程分析时，应该选择动力显式，如图 3.1-9。

![](../assets/GFE-SSA/9372fe05fe03d0df0fb840fc51e4cfbff87d09e17026de0a2b014950696c07ff.jpg)  
图 3.1-9 分析步设置

# 3.1.5 网格划分

在工具栏中激活几何体选择, 视图中选择需要划分网格的几何体, 点击【Mesh /网格划分】, 弹出网格划分设置对话框, 见图 3.1-10, 根据实际分析模型选择单元类型及网格尺寸, 点击【OK /确认】完成网格划分。

![](../assets/GFE-SSA/418e2099e4d2a3fdf71d470ad94d80b791ff9fbded0ebd590ca04b9ff1d302c3.jpg)  
图 3.1-10 网格划分设置

# 3.1.6 土-结构相互作用设置

土-结构的相互作用包括结构与土的 Tie 约束和地连墙 Embed 嵌入土内。

# （1）查找 Tie 接触对

在工具栏中，选择【Find Contact /寻找接触】，见图 3.1-11 所示，在【Search Domain】中会出现四种选择方式，用户可以选择任何一种方式进行分网，之后选择【Search /搜索】，软件会自动寻找土与结构模型间的接触，寻找完成后操作【Ok /确认】按钮。

![](../assets/GFE-SSA/4c04130740732d6d6c973475dc519a41ae875be83c9771c3f650266f1f6056aa.jpg)  
图 3.1-11 查找接触对

# (2) 嵌入约束

创建嵌入约束前应先分别创建地连墙的几何集合和土体几何，分别作为嵌入区域和被嵌

入区域。嵌入约束操作过程如图 3.1-12 所示。

![](../assets/GFE-SSA/e4ebf881863757e975c5225b40c153c056be7df983e73a8462a6ec48f19a1ca0.jpg)  
图 3.1-12 嵌入约束

# 3.1.7 人工边界设置

GFE 软件中设置人工边界需要两步，第一步建立一个表面，点击【Surfaces /表面集】按

钮，选择所见土体的外边缘，点击【Continue /继续】完成表面的建立，见图 3.1-13；第二步建立人工边界，点击【Art BCs /人工边界】，之后选择结构和所建立的表面，点击【OK /确认】完成人工边界的设置，见图 3.1-14。

![](../assets/GFE-SSA/87ffa8663eee0f78a10cf6cd95b04c9de103d596a7dbfc6aa9766293015cc0b1.jpg)

图 3.1-13 建立表面  
![](../assets/GFE-SSA/f874aac133e0976450dffc323d592f2f48ec9d0508d001a01c7f4978b48497f0.jpg)  
图 3.1-14 建立人工边界

# 3.1.8 场地地震反应分析与地震动输入

双击【Amplitudes/幅值函数】按钮，点击【OK/确认】，之后选择导入按钮，导入的地震动可以为 txt 文件也可以用户手动录入，选择【OK/确认】，地震动导入完成，如图 3.1-15 所示。

![](../assets/GFE-SSA/f838085b49b39fc295c27fd331a38f0ca71b150726e7249e79bee779ccfc273b.jpg)  
图 3.1-15 导入地震动

地震动导入完成后，可在 GFE 软件中进行场地分析。首先点击【ERA /地震场地反应】，在弹出的【Earthquake site Response Analysis /地震场地反应分析】窗口中进行设置。在【Use for/ 用于】下拉列表中，选择【Time History /时程分析】；在【Input Loc/输入位置】中可以选

择地表输入、基岩输入和基岩露头三种输入位置，用户可根据实际情况进行选择；在【Amplitude/幅值函数】中选择地震方向及测量地震数据。操作完成后点击【Save/保存】保存。若用户想要查看场地分析结果，可以点击【Compute/计算】按钮，之后选择【Result/结果】查看场地分析结果，具体见图3.1-16所示。

![](../assets/GFE-SSA/fa6364b0f9f06a86485ef3f995cc4a476bc04f80297de85791488693c73390e4.jpg)  
图 3.1-16 场地分析

# 3.1.9 场输出设置

点击模型树【Field Output Requests /场输出请求】，弹出【Edit Output Request /编辑场输出请求】窗口，如图 3.1-17。在【Edit Output Request /编辑场输出请求】窗口中，在【Time interval /时间间隔】中可设定输出间隔时间，点击【Add /增加】，弹出【Add SubOutput /新建子输出】窗口，点击【Node /节点】和【Element /单元】可选择节点或者单元输出，点击后在【SubOutput /子输出】中出现新增的输出【SubOut-1（Node）/子输出-1（节点）】，选中后，在右侧【Symbol /符号】下可勾选输出内容。

![](../assets/GFE-SSA/e45fb49d651647f7a2e937b57618945e58c62976d123f0df69e82bf3cb7d2b17.jpg)  
（a）点击【Field Output Requests /场输出请求】

![](../assets/GFE-SSA/514735ea0b83286376e71a83a5516b4972ccd922031f3bb38d38e1a67553eb99.jpg)  
图 3.1-17 场输出设置

# 3.1.10 设置工况并创建任务提交计算

提交计算前需先设置计算工况，操作流程如图 3.1-18 所示。

![](../assets/GFE-SSA/342b45a6222565df1a26a5931f560c4e8951b2f9636257675f0768755920105a.jpg)  
图 3.1-18 工况设置

完成上述步骤后，在【Job Manager /作业管理器】窗口中，点击【Create /创建】，弹出【Create Job /创建作业】窗口，在 Job Name 中对工作命名，选择工况，点击【Continue /继续】，弹出【Edit Job /编辑作业】，点击【OK /确认】完成任务创建。【Job Manager /作业管理器】

窗口选中创建的 Job，点击【Submit /提交】提交计算，点击【Monitor /监控】监控计算过程，计算完成后点击【Results /结果】可进入后处理查看结果，操作流程如图 3.1-19 所示。

![](../assets/GFE-SSA/6e211d16988883b8bce71584582e5e9617725aebe87fa8a2495509cfd32fed65.jpg)  
(a) 创建作业

![](../assets/GFE-SSA/cb7c42c64def4925d5d0b346f37461e845e6016e76d162f282b58583b4fa16e7.jpg)  
(b) 提交计算  
图 3.1-19 创建任务提交计算

# 3.2 场地地震反应分析结果

分别进行 E2 和 E3 地震作用下一维场地地震反应分析，场地土体峰值加速度、峰值相对位移和峰值剪应力沿深度分布结果如图 3.2-1 和图 3.2-2 所示。

![](../assets/GFE-SSA/542da88ccc07b0e03bc143d8faf9e79c69e13cdf5bfb9e7758a5cc191402113a.jpg)

<details>
<summary>line</summary>

| Depth (m) | Acceleration \((m/s^{2})\) |
| --- | --- |
| 0 | ~-1.7 |
| -5 | ~-1.0 |
| -10 | ~-0.8 |
| -15 | ~-0.6 |
| -20 | ~-0.4 |
| -25 | ~-0.3 |
| -30 | ~-0.4 |
| -35 | ~-0.5 |
| -40 | ~-0.4 |
| -45 | ~-0.3 |
| -50 | ~-0.2 |
| -55 | ~-0.1 |
| -60 | ~0.0 |
| -65 | ~0.1 |
| -70 | ~0.2 |
| -75 | ~0.1 |
| -80 | ~0.0 |
</details>

(a) 峰值加速度

![](../assets/GFE-SSA/b20f0c9bc9e3bd0d4af470ae1aaedf2dde8f788b2a29892f4f09aec9417ac0a1.jpg)

<details>
<summary>line</summary>

| 深度/m | 相对位移/m |
| --- | --- |
| 0 | ~0.0065 |
| -10 | ~0.0045 |
| -20 | ~0.0040 |
| -30 | ~0.0035 |
| -40 | ~0.0030 |
| -50 | ~0.0025 |
| -60 | ~0.0020 |
| -70 | ~0.0015 |
| -80 | 0.0000 |
</details>

(b) 峰值相对位移

![](../assets/GFE-SSA/2c418ad288c12c869eaeb280741e3c9a31ae43d5194bd8c07eb789e2641194c3.jpg)

<details>
<summary>line</summary>

| 深度/m | 剪应力/kPa |
| --- | --- |
| 0 | 0 |
| -20 | ~25 |
| -40 | ~40 |
| -60 | ~45 |
| -80 | ~50 |
</details>

(c) 峰值剪应力

图 3.2-1 E2 地震作用下场地地震反应分析结果  
![](../assets/GFE-SSA/84b9eb43704b07a15aa77117bb8620ae2fe51301e0abb9183443923b002fcd08.jpg)

<details>
<summary>line</summary>

| 深度/m | 加速度 \((m/s^{2})\) |
| --- | --- |
| 0 | ~2.9 |
| -10 | ~1.8 |
| -20 | ~1.3 |
| -30 | ~1.1 |
| -40 | ~1.3 |
| -50 | ~1.2 |
| -60 | ~1.1 |
| -70 | ~1.1 |
| -80 | ~1.1 |
</details>

(a) 峰值加速度

![](../assets/GFE-SSA/e94f7d7ee22665af4fb18278398d19c6045195c9d94aed080ae9c942547bd1df.jpg)

<details>
<summary>line</summary>

| 深度/m | 相对位移/m |
| --- | --- |
| 0 | ~0.0065 |
| -10 | ~0.0045 |
| -20 | ~0.0040 |
| -40 | ~0.0030 |
| -60 | ~0.0020 |
| -80 | ~0.0005 |
</details>

(b) 峰值相对位移

![](../assets/GFE-SSA/9ad5b1f92dcfddf0a9207dfd5fdd2d1f2ebd7473ba70a127dae96d910899c6c9.jpg)

<details>
<summary>line</summary>

| 深度/m | 剪应力/kPa |
| --- | --- |
| 0 | 0 |
| -20 | ~50 |
| -40 | ~75 |
| -60 | ~110 |
| -80 | 140 |
</details>

(c) 峰值剪应力  
图 3.2-2 E3 地震作用下场地地震反应分析结果

# 3.3 E2 地震线性时程分析结果

采用 GFE 软件建立的横断面分析模型如图 3.3-1 所示。结构模型尺寸 X\*Y=22.5m\*14m，网格尺寸为 1m，结构构件均采用梁单元模拟。土层模型尺寸 X\*Y=200m\*50m，网格尺寸为 1m。结构单元与周围土层接触部分采用绑定约束，土层左右侧面和底面设置黏弹性人工边界并输入 E2 地震场地反应。

![](../assets/GFE-SSA/810fb31acd839c2afb94ee655ec0a0167e6ed96fa9c25bd61af97e68373a9f2d.jpg)

<details>
<summary>natural_image</summary>

Abstract layered diagram with horizontal stripes and a central rectangular block, no text or symbols present
</details>

图 3.3-1 土-结构系统横断面分析模型

# 3.3.1 结构内力

# (a) 剪力

图 3.3-2 给出地震作用下结构剪力时程最大值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中最大值为 356kN，软件 A 计算结果云图中最大值为 357kN，二者的差异率为 0.28%。

![](../assets/GFE-SSA/5862e227c2be84a907ce9563f22f67c22b0aaa0e51a91949a3ffbaf690122e7b.jpg)  
+3.57e2

![](../assets/GFE-SSA/4adbdccd30a6ed6400813019982d557aaaa9a4fbbd759f6c1b416e7deb6a1517.jpg)  
+1.84e0 (kN)

![](../assets/GFE-SSA/43918bf0e47c29a3e42ca8995b9b1b54ee17a2aa8be32160933415b38854ee13.jpg)

<details>
<summary>natural_image</summary>

Color gradient bar with 12 vertical lines, transitioning from red to blue (no text or symbols)
</details>

(a) GFE 计算结果  
(b) 软件 A 计算结果  
图 3.3-2 结构剪力时程最大值分布

图 3.3-3 给出图 3.3-2 中结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的剪力值。由图可知，GFE 软件和软件 A 计算结果较为相近，两者的差异率均小于 1%。

![](../assets/GFE-SSA/13744d8dfb5fd49fd9f0b08bd344afb7344d4586e4b1f6419a90e2e87d104e56.jpg)

<details>
<summary>bar</summary>

| Category | 软件A (kN) | GFE (kN) | 差异率 |
| --- | --- | --- | --- |
| 底板端部 | 313.1 | 314.5 | 0.45% |
| 侧墙底部 | 357 | 356.2 | 0.22% |
| 顶板端部 | 84.1 | 83.4 | 0.83% |
| 侧墙顶部 | 205.5 | 207.1 | 0.77% |
</details>

图 3.3-3 结构典型部位剪力最大值

图 3.3-4 给出侧墙底部剪力时程曲线。由图可知，GFE 软件和软件 A 计算侧墙底部剪力时程结果吻合较好。

![](../assets/GFE-SSA/6efe4f983c96c9e0a3832ed197516f2d8956cf167545a2284ccafb993607b18e.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE (kN) | 软件A (kN) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~-400 | ~-400 |
| ~10 | ~-250 | ~-250 |
| ~14 | ~-300 | ~-300 |
| ~20 | ~0 | ~0 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 3.3-4 结构侧墙底部剪力时程曲线

# (b) 弯矩

图 3.3-5 给出地震作用下结构弯矩时程最大值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中最大值为 $558kN\cdot m$ ，软件 A 计算结果云图中最大值为 $561kN\cdot m$ ，二者的差异率为 0.53%。

![](../assets/GFE-SSA/f3cbf8ec1a261c14e0b4af90abd74ada2cb7ceae4b9d21691c6a6d8f71784d98.jpg)

![](../assets/GFE-SSA/684aefc1f5ab64ac5523deb5c6a3d4081e1e420c7d33761c54e168490fb793b2.jpg)

<details>
<summary>heatmap</summary>

| Color | Value \((kN \cdot m)\) |
| --- | --- |
| Red | +5.61e2 |
| Orange | +5.61e2 |
| Yellow | +5.61e2 |
| Light Green | +5.61e2 |
| Green | +5.61e2 |
| Cyan | +5.61e2 |
| Blue | +6.69e-2 |
</details>

(a) GFE 计算结果  
(b) 软件 A 计算结果  
图 3.3-5 结构弯矩时程最大值分布

图 3.3-6 给出图 3.3-5 中结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的弯矩值。由图可知，GFE 软件和软件 A 计算结果较为相近，两者的差异率均小于 1.5%。

![](../assets/GFE-SSA/1a8c9bdddea4b64070dbe0fddf278d3633d2f7cc5ed8b990f6b85d7c96ff124e.jpg)

<details>
<summary>bar</summary>

| Category | Software A \((kN \cdot m)\) | GFE \((kN \cdot m)\) | Diffusion Rate (%) |
| --- | --- | --- | --- |
| 底板端部 | 492.3 | 495.8 | 0.71 |
| 侧墙底部 | 525.8 | 525.8 | 0.00 |
| 顶板端部 | 300.3 | 303.7 | 1.13 |
| 侧墙顶部 | 234.2 | 236.4 | 0.94 |
</details>

图 3.3-6 结构典型部位弯矩最大值

图 3.3-7 给出侧墙底部弯矩时程曲线。由图可知，GFE 软件和软件 A 计算侧墙底部弯矩时程结果吻合较好。

![](../assets/GFE-SSA/3a10bffb70cf6c680102edb76bcf2ad8d237b63b8d839d26982c95b01ba1e70e.jpg)

<details>
<summary>line</summary>

| 时间/s | \(GFE (kN \cdot m)\) | 软件A \((kN \cdot m)\) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~520 | ~520 |
| ~7 | ~-480 | ~-480 |
| ~10 | ~-450 | ~-450 |
| ~14 | ~-450 | ~-450 |
| ~15 | ~380 | ~380 |
| ~16 | ~-450 | ~-450 |
| ~20 | ~-100 | ~-100 |
| ~30 | ~0 | ~0 |
| 40 | 0 | 0 |
</details>

图 3.3-7 结构侧墙底部弯矩时程曲线

# 3.3.2 结构变形

# (a) 水平位移

图 3.3-8 给出位移反应较大时刻土-结构系统模型的水平位移云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算云图结果中的最大水平位移为 0.0381m，软件 A 计算云图结果中的最大水平位移为 0.0380m，二者的差异率仅为 0.26%。

![](../assets/GFE-SSA/ff2f26654b7fd417c85efab7c526de2990d803e50dc8c59d60b98157a8a74875.jpg)

<details>
<summary>natural_image</summary>

Color gradient contour plot showing layered structure with a central white square feature (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/9d1ac7ca889b6333b15df180a3b1ec23ac6713aeabd914305307652240bb7ceb.jpg)

<details>
<summary>natural_image</summary>

Color gradient contour plot showing layered structure with a small rectangular object at the center (no text or symbols)
</details>

![](../assets/GFE-SSA/051bf63a4c2cd6a3092bcc6ad59838ec4833b8d8a332f087945924559fa1fa5a.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (m) |
| --- | --- |
| Red | +3.81e-2 |
| Orange | +3.81e-2 |
| Yellow | +3.81e-2 |
| Green | +3.81e-2 |
| Cyan | +2.70e-2 |
| Blue | +2.70e-2 |
</details>

(b) 软件 A 计算结果  
图 3.3-8 土-结构系统的水平位移云图（放大 200 倍）

图 3.3-9 给出图 3.3-8 中结构的水平位移云图。由图可知，GFE 软件和软件 A 计算结果吻合较好，其中 GFE 软件计算的最大水平位移为 0.0376m，软件 A 计算的最大水平位移为 0.0376m，二者完全相同。

![](../assets/GFE-SSA/8ec4383e3f04ba2fe449769e4fd473ae11657e42d0fb5b7b0be1c51fe3e0b7f9.jpg)

<details>
<summary>natural_image</summary>

Simple geometric diagram with a grid of colored lines and a blue base, no text or symbols present.
</details>

+3.80e-2

![](../assets/GFE-SSA/7a526b2047595e91999f0574c68bf916db7d90057ce7efc3ec3946c29944bb02.jpg)

<details>
<summary>natural_image</summary>

Simple geometric grid pattern with colored lines and no text or symbols
</details>

-3.40e-2 (m)  
![](../assets/GFE-SSA/095c9a93346f6e7ba5c2d11bbc8190d33e3e976853863cd92d6352df42e59701.jpg)

<details>
<summary>natural_image</summary>

Color gradient bar with 12 vertical lines, transitioning from red to blue (no text or symbols)
</details>

(a) GFE 计算结果  
(b) 软件 A 计算结果  
图 3.3-9 结构水平位移云图（放大 200 倍）

# (b) 层间位移角

图 3.3-10 给出结构各层的层间位移角结果。由图可知，GFE 软件和软件 A 计算的层间位移角结果吻合较好，GFE 软件计算的最大层间位移角为 1/1118，软件 A 计算的最大层间位移角为 1/1136，二者的差异率仅为 1.58%。

![](../assets/GFE-SSA/62e4816878374d8f877f72ce3387d1925160551a98bd718eccab488e2118a7b7.jpg)

<details>
<summary>line</summary>

| 层数 | GFE | 软件A |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 1 |
| 2 | 1 | 2 |
</details>

层间位移角  
图 3.3-10 结构各层层间位移角

结构底层层间位移角最大，图 3.3-11 给出结构底层层间位移角时程曲线。由图可知，软件 A 和 GFE 软件计算的底层层间位移角时程结果吻合较好。

![](../assets/GFE-SSA/679cb3e5dbfc637b0d0c9c0320ea5cddd3736e8e66a7d1161f4813ffe7466b7d.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE (层间位移角) | 软件A (层间位移角) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~1/2500 | ~1/2500 |
| ~8 | ~1/2000 | ~1/2000 |
| ~14 | ~1/2000 | ~1/2000 |
| ~20 | ~0 | ~0 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 3.3-11 结构底层层间位移角时程曲线

# 3.4 E3 地震非线性时程分析结果

建立的有限元模型尺寸和网格划分与3.3节相同。为模拟材料非线性，结构梁单元采用一维混凝土塑性损伤本构，材料参数见表2.1-1。土层的本构模型分别采用Davidenkov本构模型和Mohr-Coulomb本构模型，土层材料参数见表2.2-2-表2.2-3。重力荷载作用下的结果见附录一。由于与软件A中材料非线性本构模型的差异，本小节仅给出GFE软件的计算结果。

# 3.4.1 结构损伤

图 3.4-1 和图 3.4-2 分别给出非线性时程分析最终时刻结构的压损伤云图和拉损伤云图。由图 3.4-1 可知，采用不同土体本构模型，地铁车站压损伤云图分布差异不大，压损伤均发生在中柱支座处，最大压损伤为 0.325 和 0.189。由图 3.4-2 可知，该模型采用不同土体本构模型，地铁车站拉损伤云图差异不大，车站侧墙与顶板、中板连接部位以及车站中柱与顶板、中板连接部位附近结构的损伤比较明显，尤其是侧墙和顶板的连接部位。图 3.4-3 给出了钢筋塑性损伤云图。从图中可以看出，两种土体本构模型下，钢筋均发生了一定程度的屈服变形，但数值很小。

![](../assets/GFE-SSA/1962b9ec924c6d0b03ae8a0f0917d7d2a22fb637f820c3873675c3b316d27953.jpg)  
图 3.4-1 结构压损伤云图

![](../assets/GFE-SSA/14e921de36c2d5d4fe16913c9c56c73d396596cc0a130c0a37fb306cf8703f03.jpg)  
图 3.4-2 结构拉损伤云图

![](../assets/GFE-SSA/5bb6e93e02d5c5e20d19b8ede40a4d187e546014bea5a08d980c7f53b6e8933a.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | +2.20e-4 |
| Orange | +2.20e-4 |
| Yellow | +2.20e-4 |
| Light Green | +2.20e-4 |
| Green | +2.20e-4 |
| Teal | +2.20e-4 |
| Cyan | +2.20e-4 |
| Light Blue | +2.20e-4 |
| Blue | -1.47e-4 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/db44b85f8dfc4d036e35afd8cfef5f7c45b6e742795890d3d245be30015b4f0b.jpg)

<details>
<summary>heatmap</summary>

| Quadrant | Value Range |
| --- | --- |
| Top-Left | N/A |
| Top-Right | N/A |
| Bottom-Left | N/A |
| Bottom-Right | N/A |
</details>

(b) Mohr-Coulomb 本构模型  
图 3.4-3 钢筋塑性损伤云图

# 3.4.2 结构变形

图 3.4-4 给出地震作用下结构各层的层间位移角。由图可知，土体采用 Davidenkov 本构模型和 Mohr-Coulomb 本构模型计算所得最大层间位移角分别为 1/456 和 1/599，两种本构模型时车站结构均发生了较大的层间变形，但均未超过规范规定的限值 1/250。

![](../assets/GFE-SSA/7c45097c07db6aba2a4bb8106351be7ee39ce5067320408a3f5f72b5bab01822.jpg)

<details>
<summary>line</summary>

| 层数 | 层间位移角 |
| --- | --- |
| 0 | 0 |
| 1 | 1/500 |
| 2 | 1/500 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/03f97092aba465d0f6d5ca7f8e30bf44223b17e4e52c786c12dfa3cbe3e033dc.jpg)

<details>
<summary>line</summary>

| 层数 | 层间位移角 |
| --- | --- |
| 0 | 0 |
| 1 | 1/500 |
| 2 | 1/250 |
</details>

(b) Mohr-Coulomb 本构模型  
图 3.4-4 结构各层层间位移角

![](../assets/GFE-SSA/c7228a5b74684c81dd029b1b52e08048b35b7c8e156db93aa155b47150be9440.jpg)

<details>
<summary>line</summary>

| 时间/s | 层间位移角 |
| --- | --- |
| 0 | 0 |
| ~4 | ~1500 |
| ~12 | ~1500 |
| ~15 | ~1500 |
| ~20 | ~100 |
| ~30 | ~100 |
| 40 | ~100 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/8a9f26087ca402cedd05c1fe3db9ade21372943d3344d2196045ef07eb2a25a5.jpg)

<details>
<summary>line</summary>

| 时间/s | 层间位移角 |
| --- | --- |
| 0 | 0 |
| ~4 | ~150 |
| ~6 | ~-150 |
| ~8 | ~150 |
| ~10 | ~-150 |
| ~12 | ~150 |
| ~14 | ~-150 |
| ~16 | ~150 |
| ~18 | ~-150 |
| ~20 | ~150 |
| ~22 | ~-150 |
| ~24 | ~150 |
| ~26 | ~-150 |
| ~28 | ~150 |
| ~30 | ~-150 |
| ~32 | ~150 |
| ~34 | ~-150 |
| ~36 | ~150 |
| ~38 | ~-150 |
| 40 | 0 |
</details>

(b) Mohr-Coulomb 本构模型  
图 3.4-5 结构底层层间位移角时程曲线

# 3.5 土层液化对分析结果的影响

GFE 支持考虑土层液化的 Davidenkov 本构模型，对上节 E3 地震非线性时程分析中的 Davidenkov 模型考虑中间土层的液化，分析中间土层液化对最终计算结果的影响。液化的土层位于结构周围，如图 3.5-1 所示。土层的液化参数为 $\gamma_{tv}=0.001$ , m=0.345, n=6.689, a3=0.45, c1=1.051, c3=1.25。

![](../assets/GFE-SSA/50b97f8f2f3c88465ab5a461b8d3418ca4574f44e6f8c6fffd330b9f2c87b3a0.jpg)

<details>
<summary>natural_image</summary>

3D diagram of a rectangular plate with a central rectangular block and a purple textured strip, with XYZ coordinate axes at the base (no text or symbols)
</details>

图 3.5-1 土层液化区域

# 3.5.1 层间位移角

![](../assets/GFE-SSA/20a59f27eb96ff1acd2d068a17d6f1e4fee980041f42fff9b1f7a76b6f9d5533.jpg)

<details>
<summary>line</summary>

| 层数 | Davidenkov模型 (layer spacing) | Davidenkov液化模型 (layer spacing) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1/500 | ~1/150 |
| 2 | 1/500 | ~1/150 |
</details>

图 3.5-2 液化层间位移角对比

# 3.5.2 孔压比

孔压比是考察土层液化程度的关键物理量, 分别选取六个时刻的孔压比云图(图 3.5-3), 可知土层在 10.6s 内基本已经全部液化。

![](../assets/GFE-SSA/720136b2ba9bf00f97dd9bccd33f766fb8520e1de2728d27fd1036f16fd1b5b8.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 8.810E-01 |
| Orange-Red | 8.076E-01 |
| Orange | 7.342E-01 |
| Yellow-Orange | 6.608E-01 |
| Yellow | 5.874E-01 |
| Light Green | 5.139E-01 |
| Green | 4.405E-01 |
| Teal | 3.671E-01 |
| Cyan | 2.937E-01 |
| Light Blue | 2.203E-01 |
| Blue | 1.468E-01 |
| Dark Blue | 7.342E-02 |
| Darkest Blue | 0.000E+00 |
</details>

(a)t=3.85s

![](../assets/GFE-SSA/20ff723415a24b118c78b9b47ec98a6d949804f24f8972badaacbc9c1f334a6d.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 1.000E+00 |
| Orange-Red | 9.167E-01 |
| Orange | 8.333E-01 |
| Yellow-Orange | 7.500E-01 |
| Yellow | 6.667E-01 |
| Light Green | 5.833E-01 |
| Green | 5.000E-01 |
| Teal | 4.167E-01 |
| Cyan | 3.333E-01 |
| Light Blue | 2.500E-01 |
| Blue | 1.667E-01 |
| Dark Blue | 8.333E-02 |
| Deep Blue | 0.000E+00 |
</details>

(b)t=4.15s

![](../assets/GFE-SSA/6097482fedbcdc15ae244291c203e9db66e1322e6bf535220ef88882067d9720.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 1.000E+00 |
| Orange-Red | 9.167E-01 |
| Orange | 8.333E-01 |
| Yellow-Orange | 7.500E-01 |
| Yellow | 6.667E-01 |
| Light Green | 5.833E-01 |
| Green | 5.000E-01 |
| Teal | 4.167E-01 |
| Cyan | 3.333E-01 |
| Light Blue | 2.500E-01 |
| Blue | 1.667E-01 |
| Dark Blue | 8.333E-02 |
| Deep Blue | 0.000E+00 |
</details>

(c)t=4.5s

![](../assets/GFE-SSA/b04594a29e5356053fe736a7d8ec6db00065ef097c8b279d7ccb76251f7efab8.jpg)  
图 5.3-3 土层孔压比云图

分别选取土体 55295、55016、54497 和 54393 号单元的作出孔压比曲线, 如图 3.5-5 所示, 可见土层约从 5s 开始液化, 在 12s 后孔压比达到 1 已完全液化。

![](../assets/GFE-SSA/3e6853bc6b6ec4a55ea56c9076f245ffb5204fb1fd73f881d0b6084352f59935.jpg)  
图 5.3-4 提取单元位置

![](../assets/GFE-SSA/29aeb8d3acef450c75ce34145d1b612962437feabed1a4fcc6005041705739c2.jpg)

<details>
<summary>line</summary>

| 时间 (s) | 孔压比 |
| --- | --- |
| 0 | 0 |
| ~4 | 0 |
| ~4.2 | 0.1 |
| ~4.5 | 0.12 |
| ~4.8 | 0.68 |
| ~5.2 | 0.86 |
| ~6 | 1.0 |
| 30 | 1.0 |
</details>

(a)E55295 单元

![](../assets/GFE-SSA/b191d479fbf963319bf51839e6b84c4b3d2acae345ad994b48519c256adcd566.jpg)

<details>
<summary>line</summary>

| 时间 (s) | 孔压比 |
| --- | --- |
| 0 | 0 |
| 5 | 0 |
| 5 | ~0.25 |
| 5 | ~0.28 |
| 5 | ~0.58 |
| 6 | ~0.58 |
| 6 | ~0.82 |
| 8 | ~0.82 |
| 8 | ~0.93 |
| 12 | ~0.93 |
| 12 | 1 |
| 30 | 1 |
</details>

(b)E55016 单元

![](../assets/GFE-SSA/649c0f968c2684cad64cac3fbc4ccdb8919f389d78daa48de3b6f61b8c0f5927.jpg)

<details>
<summary>line</summary>

| 时间 (s) | 孔压比 |
| --- | --- |
| 0 | 0 |
| ~4.5 | 0 |
| ~4.8 | ~0.73 |
| ~5.2 | ~0.84 |
| ~6.5 | 1 |
| 30 | 1 |
</details>

(c)E54497 单元

![](../assets/GFE-SSA/cb3572f0989e9546113ff077b313a29619004802aa45220319c99e502a242c17.jpg)

<details>
<summary>line</summary>

| 时间 (s) | 孔压比 |
| --- | --- |
| 0 | 0 |
| 5 | 0 |
| 5 | ~0.22 |
| 6 | ~0.22 |
| 6 | ~0.94 |
| 7 | ~0.94 |
| 7 | 1 |
| 30 | 1 |
</details>

(d)E54393 单元  
图 3.5-5 孔压比时程曲线

# 3.5.3 结构损伤

![](../assets/GFE-SSA/5cd576229687b56ac4d55e72c145ddb206669f1c663d57ca924a83ebaba1f111.jpg)

图 3.5-6 结构受压损伤对比  
![](../assets/GFE-SSA/b916b3d3f3777bade09d4bfc2b0ad6deea0c0e95bee0cb8328bae8275f5d4986.jpg)  
(a)不液化  
(b)液化  
图 3.5-7 结构受拉损伤对比

# 第4章 反应加速度法

GFE 软件集成了地下结构抗震设计规范中的反应加速度法。针对第二章给出的地铁车站地下结构抗震分析案例，本章采用 GFE 软件完成二维横断面反应加速度法分析。首先介绍反应加速度法在 GFE 软件中的操作步骤，然后给出地铁车站地震反应计算结果。通过与某国际先进通用有限元软件（简称软件 A）的计算结果对比，验证 GFE 软件的可靠性和优势。

# 4.1 软件操作

GFE 软件进行反应加速度法计算时，土-结构系统模型建立过程与第 3.1 节类似，此处不再赘述。主要介绍场地地震反应分析、有效反应加速度计算、土-结构系统惯性力施加等软件操作过程。

# 4.1.1 场地地震反应分析与有效反应加速度

双击模型树中【ERA/地震场地反应】分支，弹出【Earthquake site Response Analysis/地震场地反应分析】窗口，如图4.1-1所示。在【Use for/用于】下拉列表中，选择【Pseudo Dyna/拟动力分析】，在【Amplitude/幅值函数】中勾选【x:Amp-1】，在【Struc Top-Bot Depth/结构顶底点深度】中输入结构的深度范围。点击【Compute/计算】，点击【Result/结果】，弹出【ERA result/场地分析结果】窗口。

![](../assets/GFE-SSA/82330bcb1833eb4109ad5c420094c319a6ad754b6fc297b0afdc7396cb7f01b7.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
  A["Model-1\nGeometries\nSets\nSurfaces\nMaterials\nSections\nBCs & Loads\nSteps\nCases\nInteractions\nAmplitudes\nField Output Requests\nHistory Output Requests\nERA\nArt BCs\nSoils"] --> B["Earthquake site Response Analysis"]
  B --> C["Name: VibLoad-1\nUse for: Pseudo Dyna\nInput Loc: Outcrop\nEarthquake Level: E2"]
  C --> D["Amplitude\n□ x: Amp-1\n□ y: Amp-1\nResult>>"]
  D --> E["Soil: Soil1D-1"]
  E --> F["PD\nStruc Top-Bot Depth: 2 - 17.43\nCompute Quit"]
```
</details>

![](../assets/GFE-SSA/c3183692525ef0644d1005d2f7f8676960b5fa790c24e529b98f292f4af9ed66.jpg)

<details>
<summary>text_image</summary>

模型
Model-1
几何
集合
表面集
材料
截面属性
边界条件与荷载
分析步
工况
相互作用
幅值函数
场输出请求
历史输出请求
地震场地反应
人工边界
一维土层
地震场地反应分析
名称: VibLoad-1
用于: 拟动力分析
输入位置: 基岩露头
地震水准: E2
幅值函数
x: Amp-1
y: Amp-1
结果>>
土层信息: Soil1D-1
拟动力
结构顶底点深度: 2 - 17.43
计算 退出
</details>

（a）双击【ERA/地震场地反应】  
![](../assets/GFE-SSA/e6a40fae40c49c990b8769b1464ebc3230db2ede8b2d396f4663165805d1af0d.jpg)

<details>
<summary>text_image</summary>

Earthquake site Response Analysis
Name: VibLoad-1
Use for: Pseudo Dyna
Input Loc: Outcrop
Earthquake Level: E2
Advanced>>
Amplitude
x: Amp-1
y: Amp-1
Result>>
Soil: Soil1D-1
PD
Struc Top-Bot Depth: 2 - 17.43
Compute Quit
</details>

![](../assets/GFE-SSA/d47a5944caa15a77d1304dff0e7e4305456d14e1fb6b334ddbc30abe40645175.jpg)

<details>
<summary>text_image</summary>

地震场地反应分析
名称: VibLoad-1
用于: 拟动力分析
输入位置: 基岩露头
地震水准: E2
高级>>
幅值函数
x: Amp-1
y: DistAmp-1
结果>>
土层信息: Soil1D-1
拟动力
结构顶底点深度: 2 - 17.43
计算 退出
</details>

(b) 【Earthquake site Response Analysis /地震场地反应分析】窗口操作  
图 4.1-1 土层场地地震反应分析

在【ERA Result/场地分析结果】窗口中可查看场地分析结果，选择【AR/反应加速度】，变量选择【A/加速度】，即得到结构顶、底板位移差最大时刻的加速度曲线。点击【Table/表格】可得到曲线数据，此时第一列数据为土层深度，在【Top coord of depth dir/顶部坐标（深度方向）】中输入土层顶部坐标，第一列数据即变为土层y坐标值。复制表格中数据到Excel中进行升序排列即可得到按空间分布的加速度数据。双击【Amplitudes/幅值函数】，创建加速度数值的幅值函数命名为【Amp-AX】，将空间分布加速度数据粘贴其中即可，如图4.1-2所示。

![](../assets/GFE-SSA/fefbe15b2d9bba4a95970e14d632ba3e1b4810fd5acfa8685d2be939019acd00.jpg)

![](../assets/GFE-SSA/1f3e8ae303d4564ccd24185dfa00eb45d4b94be5e10abc83b0a3676cd7aed224.jpg)  
(a) 最大加速度曲线

![](../assets/GFE-SSA/cb2d83498402b0ec2535a6a1ce4465278640f189bc80aa2b7fe913578639fa3d.jpg)

(b) 最大加速度值  
![](../assets/GFE-SSA/1692ef741ba70dbdeb853117e365e868bbee5f8a173508d8f7c4fca43be31ae9.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
  A["Model-1\nGeometries\nSets\nSurfaces\nMaterials\nSections\nBCs & Loads\nSteps\nCases\nInteractions\nAmplitudes\nAmp-1\nACC\nACC2\nField Output Requests\nHistory Output Requests\nVibration Loads\nArt BCs\nSoils"] --> B["Create Amplitude ? X\nName: Amp-AX\nOK Cancel"]
```
</details>

![](../assets/GFE-SSA/1488c8cd061655b31bf875305b564b436c09f369b92c803c69860b9075df257d.jpg)

<details>
<summary>text_image</summary>

Model-1
几何
iieaou
dilianaiana
Face-1
SoilGeom-1
集合
表面集
材料
截面属性
边界条件与荷载
分析步
工况
相互作用
幅值函数
Amp-1
ACC
ACC2
Amp-2
Amp-3
场输出请求
历史输出请求
波动荷载
人工边界
一维土层
创建 幅值
?
×
名称: Amp-AX
确定
取消
TOP
X
</details>

（c）双击【Amplitudes /幅值函数】创建最大加速度数值的幅值函数

![](../assets/GFE-SSA/7c7712cb3946e232b8a2be95caa4dfc60accdca018c247aa4b379cb8a05e5f41.jpg)  
(d) 将最大加速度值粘贴至【Amp-AX】  
图 4.1-2 创建最大加速度幅值曲线

# 4.1.2 施加边界条件与惯性力荷载

# (a) 施加边界条件

反应加速度法模型需要底面固定约束，左右侧面竖向约束。先创建集合，双击模型树的【Sets/集合】，弹出【Dialog/对话框】窗口，选中左右侧面，创建左右侧面的集合，命名为

【Set-X】，同样的选中底面，创建底面的集合，命名为【Set-Y】，如图 4.1-3 和图 4.1-4 所示。

![](../assets/GFE-SSA/f85539c9fcc78331babb8117c23c50eab267fb98b6786854e443810830e11f2a.jpg)  
图 4.1-3 创建土-结构模型侧面集合

![](../assets/GFE-SSA/af8e20205247228c464a6f45a08a0709803bb260be4c36b7cee5a6c6e33b9917.jpg)  
图 4.1-4 创建土-结构模型底面集合

双击【BCs & Loads /边界条件与荷载】，弹出【Boundary Condition & Load /边界条件与荷载】窗口。在【Boundary Condition & Load /边界条件与荷载】窗口中输入【Name /名称】，【Type /类型】选择【Encastre /全约束】，点击【Region /区域】设置按钮，选择刚建立的底面集合【Set-Y】，点击【OK】，底面边界条件建立完成，如图 4.1-5 所示。

![](../assets/GFE-SSA/49eff2faa143fd1ccd4a285df8e76473d04debaf151cb037a7a03b3c1a01b9fa.jpg)  
图 4.1-5 创建土-结构模型底面边界条件

再次双击【BCs & Loads /边界条件与荷载】，弹出【Boundary Condition & Load /边界条件与荷载】窗口，输入【Name /名字】，【Type /类型】选择【Displacement/Rotation /位移/转动位移】，点击【Region /区域】设置按钮，选择刚建立的左右侧面集合【Set-X】，由于需要约束竖向，因此勾选【U2】，在后面空格中写0，点击【OK /确定】，完成模型左右侧面竖向约束，如图4.1-6所示。

![](../assets/GFE-SSA/9021336db0e13c91c6a130b2280de8ad53e6e1681539b16a71bb98d5b4c2f4de.jpg)  
图 4.1-6 创建土-结构模型侧面竖向约束

# (b) 施加惯性力荷载

双击【BCs & Loads /边界条件与荷载】，弹出【Boundary Condition & Load /边界条件与荷载】窗口，输入【Name /名字】，【Type /类型】选择【Gravity /惯性力】，【Region /区域】默认为【Whole Model /整个模型】，【Component 1 /分量 1】后写 1，【Distribution /空间分布】选择【Y】，【Amplitude /幅值函数】选择上个步骤中创建的最大加速度【Amp-AX】，点击【OK】完成创建，如图 4.1-7 所示。

![](../assets/GFE-SSA/5f72e29aa605fe9507cf0f802d828985da96b037295afb9063409dad0297808c.jpg)  
图 4.1-7 施加惯性力

# 4.2 计算结果

采用 GFE 软件建立的横断面分析模型图如图 4.2-1 所示。结构模型尺寸 X\*Y=22.5m\*14m，网格尺寸为 1m，结构构件均采用梁单元模拟。土层模型尺寸 X\*Y=200m\*50m，网格尺寸为 1m。结构单元与周围土层接触部分采用绑定约束，土层底部固定约束，两侧采用竖向位移约束。

![](../assets/GFE-SSA/6b40755f4e9943db7e70aadf83456ea0d9e4dbaae486daa66b51bd54d17116d0.jpg)

<details>
<summary>natural_image</summary>

Abstract layered diagram with horizontal stripes and a central rectangular block, no text or symbols present
</details>

图 4.2-1 土-结构系统横断面分析模型

# 4.2.1 结构内力

# (a) 剪力

图 4.2-2 给出结构剪力云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算的结果云图中最大剪力为 481kN，软件 A 计算的结果云图中最大剪力为 483kN，二者的差异率仅为 0.41%。

![](../assets/GFE-SSA/0728be39b5e5badedc9570c5c985b064c8455df0523ccdfd1a294e6a919bfbd6.jpg)  
(a) GFE 计算结果

![](../assets/GFE-SSA/6fdef2c875ffcee83bd6efeddfbcff8a1f560f345a1730709a889c7c22594a64.jpg)

![](../assets/GFE-SSA/002ffedd1f1b851af4783b093a36009a21d32a9c02f920f439026674b708f350.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +4.83e2 |
| Orange | ~4.5e2 |
| Yellow | ~4.2e2 |
| Green | ~3.9e2 |
| Cyan | ~3.6e2 |
| Blue | -3.86e2 |
</details>

(b) 软件 A 计算结果  
图 4.2-2 结构剪力云图

图 4.2-3 给出结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的剪力值。由图可知，GFE 软件和软件 A 计算结果较为相近，两者的差异率均小于 1%。

![](../assets/GFE-SSA/d31e2883750d9cdcf4dc1a13ad48b36c3855d2739b796775cd859f893740578c.jpg)

<details>
<summary>bar</summary>

| Category | Software A (kN) | GFE (kN) | Diffusion Rate (%) |
| :--- | :--- | :--- | :--- |
| 底板端部 | -386.3 | -382.6 | 0.96 |
| 侧墙底部 | 482.8 | 480.5 | 0.48 |
| 顶板端部 | -145.1 | -144.3 | 0.55 |
| 侧墙顶部 | 367.7 | 365.4 | 0.63 |
</details>

图 4.2-3 结构典型部位剪力

# (b) 弯矩

图 4.2-4 给出结构弯矩云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算的结果云图中最大弯矩为 $652kN\cdot m$ ，软件 A 计算的结果云图中最大弯矩为 $673kN\cdot m$ ，二者的差异率为 3.12%。

![](../assets/GFE-SSA/443eb89a5a7ae566b2d2d42c6ff7989d4730d5f16d52a80e6274df335bda8f80.jpg)

<details>
<summary>heatmap</summary>

| Metric | Value |
| --- | --- |
| GFE Calculation Result | +6.73e2 |
| Software A Calculation Result | -6.67e2 \((kN \cdot m)\) |
</details>

图 4.2-4 结构弯矩云图

图 4.2-5 给出结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的弯矩值。由图可知，GFE 软件和软件 A 计算结果较为相近，两者的差异率均小于 3.5%。

![](../assets/GFE-SSA/fbb6de5928edd8b0d645f4fd0b016cd7f7eef6bfac6a7f2ef70d19246d017296.jpg)

<details>
<summary>bar</summary>

| Category | SoftwareA \((kN \cdot m)\) | GFE \((kN \cdot m)\) |
| --- | --- | --- |
| 底板端部 | 672.7 | 652 |
| 侧墙底部 | -638.2 | -617.7 |
| 顶板端部 | 509.2 | 494.3 |
| 侧墙顶部 | 402.2 | 391.8 |
</details>

图 4.2-5 结构典型部位弯矩

# 4.2.2 结构变形

# (a) 水平位移

图 4.2-6 给出结构的水平位移云图。由图可知，GFE 软件和软件 A 计算的结果较为接近，其中 GFE 软件计算的云图结果中最大水平位移为 -0.0282m，软件 A 计算的云图结果中最大水平位移为 -0.0281m，二者的差异率仅为 0.35%。

![](../assets/GFE-SSA/5d1a35c6dff40787e144630039556a9a011b956af4ceebcaed118dc59c5edd25.jpg)

<details>
<summary>heatmap</summary>

| Metric | Value Range (m) |
| --- | --- |
| (a) GFE 计算结果 | -1.23e-2 ~ -2.82e-2 |
| (b) 软件 A 计算结果 | -2.82e-2 ~ -2.82e-2 |
</details>

图 4.2-6 结构水平位移云图（放大 500 倍）

# (b) 层间位移角

图 4.2-7 给出结构各层的层间位移角。由图可知，GFE 软件和软件 A 计算的层间位移角非常接近，其中 GFE 软件计算的最大层间位移角为 1/1044，软件 A 计算的最大层间位移角为 1/1043，二者的差异率仅为 0.16%。

![](../assets/GFE-SSA/4ca8a1aa44801bdbb79ce3d957f034cb7eccf6ab7d7729d9d80b71a5c0f916fe.jpg)

<details>
<summary>line</summary>

| 层数 | GFE (层间位移角) | 软件A (层间位移角) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1/1000 | 1/1000 |
| 2 | ~0.8 | ~0.8 |
</details>

图 4.2-7 结构各层的层间位移角

# 第5章 反应位移法

GFE 软件集成了地下结构抗震设计规范中的反应位移法。针对第二章给出的地铁车站地下结构抗震分析案例，本章采用 GFE 软件完成二维横断面反应位移法分析。首先介绍反应位移法在 GFE 软件中的操作步骤，然后给出地铁车站地震反应计算结果。通过与某国际先进通用有限元软件（简称软件 A）的计算结果对比，验证 GFE 软件的可靠性和优势。

# 5.1 软件操作

反应位移法采用荷载-结构模型。GFE 软件建立地下结构模型的过程可参考第 3.1 节，此处不再赘述。主要介绍场地地震反应分析并计算土层加速度、剪力和相对位移，以及对结构施加边界条件、地基弹簧和三类荷载等软件操作过程。

# 5.1.1 场地地震反应分析与三类荷载

场地地震反应分析流程与上一章反应加速度法一致，在此不再赘述。下面介绍提取土层加速度、剪力和相对位移的操作过程。

在【EERA Result/场地分析结果】窗口中可查看场地分析结果，选择【AR/反应加速度】，变量选择【A/加速度】，即得到结构顶底位移差最大时刻的土层加速度曲线。点击【Table/表格】可得到曲线数据，此时第一列数据为土层深度，在【Top coord of depth dir/顶部坐标（深度方向）】中输入土层顶部坐标，第一列数据即变为土层y坐标值。复制表格中数据到Excel中进行升序排列即可得到按空间分布的加速度数据。双击【Amplitudes/幅值函数】，创建加速度数值的幅值函数命名为【Amp-AX】，将空间分布加速度数据粘贴其中即可。上述操作过程如图5.1-1所示。

同样的方式，在【AR/反应加速度】下，变量选择【U/位移】，得到结构顶底位移差最大时刻的土层位移曲线；选择【S/应力】得到结构顶底位移差最大时刻的土层剪应力曲线。再分别创建两条曲线的空间分布数据，分别命名为【Amp-UX】和【Amp-SX】。操作过程分别如图 5.1-2 和图 5.1-3 所示。值得注意的是，位移曲线【Amp-UX】为相对结构最低点的位移，因此创建 Amp 时需将【UX】数据减去结构最低点处的位移值得到【Amp-UX】。

![](../assets/GFE-SSA/4060240f19bbfdd1ab17bd9ee66e3400908224c5dd9107ef67a16413ec79261e.jpg)  
(a) 土层加速度曲线

![](../assets/GFE-SSA/f396d54d45b5a3fcb2c8251fe0fa9b9763e1b3adc37926c7921530a3eabb6b3a.jpg)  
(b) 土层加速度值

![](../assets/GFE-SSA/762ef01651a817bb7202bd7221c3bc374bde26d2b1ceb4f3d7fa5e13ce609bb6.jpg)  
（c）双击【Amplitudes /幅值函数】创建土层加速度数值的幅值函数

![](../assets/GFE-SSA/2c6e0b671b3e5409ffdb229e286db9b2a32047a9a6e7d6d38afa0c7bc55cb266.jpg)  
(d) 将土层加速度值粘贴至【Amp-AX】  
图 5.1-1 创建土层加速度

![](../assets/GFE-SSA/0cf354def7989813235e1adf0737700271dcc4287af67985956dbabad1cf8980.jpg)  
(a) 土层位移曲线

![](../assets/GFE-SSA/762dece8f43260a2c0cbd293c35ba815d71413c4a4a1be5302a33f056893d5c7.jpg)  
(b) 土层位移数值

![](../assets/GFE-SSA/f0c88683b6758b6077b42fadf9ddfbae097b0d4e8c63ca15ec5eafa3a4ef8035.jpg)  
(c) 双击【Amplitudes /幅值函数】创建土层位移数值的曲线

![](../assets/GFE-SSA/599eeee77c32bbee500ac4e90eef2ab3b50b69b96f8bcdd60da050addb1893a6.jpg)  
图 5.1-2 创建土层位移

![](../assets/GFE-SSA/7c5f44589f355a09ae003c330d6d433736be5ae57a0357a62ac48d90bd4acf4f.jpg)  
(a) 土层剪应力曲线

![](../assets/GFE-SSA/6d97e44d0ac732d715a3e8a82399103b8a92d1eb771f1821ddbdbc611e4924ba.jpg)  
(b) 土层剪应力数值

![](../assets/GFE-SSA/c90d109778626325a1e28dd3c384940028f40e36e996da9b4e6fe2cf64e40281.jpg)  
(c) 双击【Amplitudes /幅值函数】创建土层剪应力数值的曲线

![](../assets/GFE-SSA/65d4db6a3f8e4fde45380264c8501e1a7baa80858723a8fc4c5274564af1be85.jpg)  
(d) 将土层位移值粘贴至【Amp-SX】  
图 5.1-3 创建土层剪应力

# 5.1.2 施加边界条件、地基弹簧和三类荷载

# (a) 施加位移约束边界条件

先创建结构地连墙底部两点的几何集合【Set-base】，双击【BCs & Loads /边界条件与荷

载】创建边界条件，弹出窗口中分别约束底部两点【Set-base】的 U1 和 U2 位移，如图 5.1-4 所示。

![](../assets/GFE-SSA/fd4eed5d41e4470e77d1310455de810f07a025b5fa100fb61d6969d666131434.jpg)  
图 5.1-4 施加位移约束边界条件

# (b) 施加地基弹簧

对结构与土接触的界面添加地基弹簧。在创建边界弹簧前需先对结构划分网格，创建节点集合，如图 5.1-5 所示，再在节点集上添加弹簧。双击模型树中【Springs/Dashpots/弹簧/阻尼】，

弹出窗口中给弹簧边界命名，分别设置弹簧类型、施加区域、弹簧方向和弹簧刚度，点击【OK/确定】完成地基弹簧创建，如图 5.1-6 所示。

![](../assets/GFE-SSA/d7fbb16b31ee144221b98fb5e93dfb27c9a7db6999ff897c18bbe27e5d410d24.jpg)  
图 5.1-5 创建节点集

![](../assets/GFE-SSA/e7b6675167d5c1f8e166244fad86bd313b37ca5f67edd0de9f9abd7cacfbd474.jpg)  
图 5.1-6 施加地基弹簧

# (c) 施加惯性力

双击【BCs & Loads /边界条件与荷载】，弹出【Boundary Condition & Load /边界条件与荷载】窗口，输入【Name /名称】，【Type /类型】选择【Gravity /惯性力】，【Region /区域】

默认为【Whole Model/整个模型】，【Component 1/分量 1】后写 1，【Distribution/分布】选择【Y】，【Amplitude/幅值函数】选择上个步骤中创建的最大加速度【AX】，点击【OK/确定】完成创建。上述过程如图 5.1-7。

![](../assets/GFE-SSA/085cffd729ef33647973363f28a1b4dd71ecc43bd543c2366ae2e672a9ec4aa1.jpg)  
图 5.1-7 施加惯性力

# (d) 施加相对位移

在上下和左右侧面施加位移，以左侧面为例，双击【BCs & Loads/边界条件与荷载】，弹

出【Boundary Condition & Load /边界条件与荷载】窗口，输入【Name /名称】，【Type /类型】选择【Line Load /线荷载】，【Region /区域】选择左边侧面的集合（需提前创建），【Component 1 /分量 1】后写区域的 X 向弹簧刚度，【Distribution /空间分布】选择【Y】，【Amplitude /幅值函数】选择上个步骤中创建的最大相对位移【deltaUX】，点击【OK /确定】完成创建。如图 5.1-8。按相同的步骤创建其余面的相对位移力。

![](../assets/GFE-SSA/a3216868687e922b9f3d2aaaa09bd3cfe69d37c28b6bea189a05132ba50ed5b0.jpg)

<details>
<summary>text_image</summary>

Model
Surfaces
Materials
TU1-1
TU1-2
TU1-3
TU2-4
TU3-5
TU3-6
TU4-7
TU5-8
TU6-9
TU7-10
TU8-11
C1_Mat35
C1_Mat50
Sections 1.双击创建
BCs & Loads
BC-1
gravity
shearforce-1
shearforce-2
shearforce-3
shearforce-4
xiangduiweiyili-1
xiangduiweiyili-2
xiangduiweiyili-3
xiangduiweiyili-4
xiangduiweiyili-6
Steps
Cases
Interactions
Amplitudes
Field Output Requests
Boundary Condition & Load
Name: xiangduiweiyili-2
Type: Line load 2.选择line load类型
Region: left-xia 3.选择区域
Component 1: 40000 4.输入X向弹簧刚度
Component 2: 0
Component 3: 0
Amplitude: (Instantaneous)
Distribution
Type: Y
Direction: 0,0,0
Amplitude: deltaUX
5.选择空间分布
OK Cancel
</details>

![](../assets/GFE-SSA/a5b4714b021b0f73f1724b4265145edc74329d5df0eed181dcbd9c4ec51e3089.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph TD
  A["Model-1\n几何\nLLZ\n集合\n表面集\n材料\n截面属性\n边界条件与荷载\nBC-1\ngravity\nshearforce-1\nshearforce-2\nshearforce-3\nshearforce-4\nxiangduiweiyili-1\nxiangduiweiyili-2\nxiangduiweiyili-3\nxiangduiweiyili-4\nxiangduiweiyili-5\nxiangduiweiyili-6\n分析步\n工况\n相互作用\n幅值函数\nAmp-1\nAX\nSX\ndeltaUX\nAmp-SX\n场输出请求\n历史输出请求\n波动荷载\n边界条件与荷载\n名称: xiangduiweiyili-2\n类型: 线荷载\n区域: left-xia\n分量 1: 60000\n分量 2: 0\n分量 3: 0\n幅值函数: (瞬时)\n空间分布\n类型: Y\n方向: 0,0,0\n幅值函数: deltaUX\n确定 取消
```
</details>

图 5.1-8 施加相对位移

# (5) 施加剪应力

剪应力施加于与土层接触的界面，即结构上下面和左右侧面。以左侧面为例，双击【BCs & Loads /边界条件与荷载】，弹出【Boundary Condition & Load /边界条件与荷载】窗口，输入【Name /名称】，【Type /类型】选择【Line Load /线荷载】，【Region /区域】选择左边侧面的集合（需提前创建），【Component 2 / 分量 2】写-1，【Distribution /空间分布】选择【Y】，【Amplitude】选择上个步骤中创建的剪应力【SX】，点击【OK】完成创建。上述过程如图 5.1-9。按照相同的步骤施加其余面的剪应力。

![](../assets/GFE-SSA/b13460a62c9faed2362357ee0505ff67f8272c6fce6712661614736ae0bb1788.jpg)  
图 5.1-9 施加剪应力

# 5.2 计算结果

采用 GFE 软件建立的结构横断面分析模型如图 5.2-1 所示。结构模型尺寸

$X*Y=22.5m*14m$ ，网格尺寸为1m，结构构件均采用梁单元模拟。结构两侧设置地连墙，地连墙长33m，网格尺寸为1m，采用梁单元模拟，地连墙和结构采用绑定约束，在结构和地连墙的周边设置法向地基弹簧和切向地基弹簧。

![](../assets/GFE-SSA/a7b6fe9ed376625d3dcb94196aa9b6ff3387f1021454b5e22c649a1fa2b51988.jpg)  
图 5.2-1 结构横断面分析模型

# 5.2.1 结构内力

# (a) 剪力

图 5.2-2 给出结构剪力云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算的结果云图中最大剪力为 -323kN，软件 A 计算的结果云图中最大剪力为 -326kN，二者的差异率仅为 0.92%。

图 5.2-3 给出结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的剪力值。由图可知，GFE 软件和软件 A 计算结果极为接近，两者差异率均小于 1%。

![](../assets/GFE-SSA/362a1655bb8b16c7a70b6864dc7f669ecc60b93b785f0e2dc9ef99edab50d06a.jpg)

<details>
<summary>heatmap</summary>

| Metric | Value |
| --- | --- |
| GFE Calculation Result | +1.72e2 |
| Software A Calculation Result | -3.27e2 (kN) |
</details>

图 5.2-2 结构剪力云图

![](../assets/GFE-SSA/89020753f0a12d7ab61433c75dbf2c8c25fe5680a3065014619bb6ab0b1cbb92.jpg)

<details>
<summary>bar</summary>

| Category | Software A (kN) | GFE (kN) |
| --- | --- | --- |
| 底板端部 | 129.1 | 129.1 |
| 侧墙底部 | -135.3 | -135.3 |
| 顶板端部 | 42.4 | 42.3 |
| 侧墙顶部 | -126 | -125.7 |
</details>

图 5.2-3 结构典型部位剪力

# (b) 弯矩

图 5.2-4 给出结构弯矩云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算的最大弯矩为 -729kN·m，软件 A 计算的最大弯矩为 -747kN·m，二者的差异率为 2.41%。

![](../assets/GFE-SSA/4bfb4d6a951f83dd903b9d154420f4ea35d2a4c3641a807bb80c8b64a2ac0448.jpg)  
+5.42e2

![](../assets/GFE-SSA/a60de19f78610561cfadc8c5e2c57dfc996774c94bb53fb3df9acdb4271cb5cf.jpg)

![](../assets/GFE-SSA/5726d97f5caf99f49690d92fb9deb762a6bee914e2ec229c0d4ca3bd3f08caa7.jpg)

<details>
<summary>natural_image</summary>

Color gradient bar with 12 segments in red to blue (no text or symbols)
</details>

(a) GFE 计算结果  
-7.47e2 (kN·m)  
(b) 软件 A 计算结果  
图 5.2-4 结构弯矩云图

图 5.2-5 给出结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的弯矩值。由图可知，GFE 软件和软件 A 计算结果较为接近，两者的差异率均小于 3.5%。

![](../assets/GFE-SSA/62cd3e145376623662f0a9c716663c4afb3465d1d71f88c150b93dd8c1873bf1.jpg)

<details>
<summary>bar</summary>

| Category | SoftwareA \((kN \cdot m)\) | GFE \((kN \cdot m)\) | Difference (%) |
| --- | --- | --- | --- |
| 底板端部 | 433.1 | 421.2 | 2.75% |
| 侧墙底部 | 541.5 | 526.6 | 2.75% |
| 顶板端部 | 253.7 | 246 | 3.04% |
| 侧墙顶部 | -747.4 | -728.7 | 2.54% |
</details>

图 5.2-5 结构典型部位弯矩

# 5.2.2 结构变形

# (a) 水平位移

图 5.2-6 给出结构水平位移云图。由图可知，GFE 软件和软件 A 计算的结果较为接近，

其中 GFE 软件计算的最大水平位移为 0.0142m，软件 A 计算的最大水平位移为 0.0142m，二者完全一致。

![](../assets/GFE-SSA/129d6eb5ba30c951b9a5bd880ed5f9463fe95953908949557bd91b39f867da49.jpg)

<details>
<summary>natural_image</summary>

Abstract geometric pattern with vertical lines and color gradients (no text or symbols)
</details>

+1.42e-2

![](../assets/GFE-SSA/475b33f07315965032068069270376f57a1a7323e3fc782f818454924428cae7.jpg)

<details>
<summary>natural_image</summary>

Simple line drawing of a ladder with colored segments (no text or symbols)
</details>

0.00 (m)  
![](../assets/GFE-SSA/a81e2c8e97c5f65f662100d1ae217c5ad0bcc4bdcfb3c39b94acb7601ee33e70.jpg)  
(a) GFE 计算结果  
(b) 软件 A 计算结果  
图 5.2-6 结构水平位移云图（放大 200 倍）

# (b) 层间位移角

图 5.2-7 给出结构各层的层间位移角。由图可知，GFE 软件和软件 A 计算的层间位移角极为接近，其中 GFE 软件计算的最大层间位移角为 1/1214，软件 A 计算的最大层间位移角为 1/1213，二者的差异率仅为 0.08%。

![](../assets/GFE-SSA/7b883ba2963b3aeb99a192000c1e5c24e564924251f67520a61d372df7a44219.jpg)

<details>
<summary>line</summary>

| 层数 | GFE (cm) | 软件A (cm) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | ~2200 | ~2200 |
| 2 | ~2400 | ~2400 |
</details>

图 5.2-7 结构各层的层间位移角

# 第6章 三维时程分析方法

针对第二章给出的地铁车站地下结构抗震分析案例，本章采用 GFE 软件完成三维时程分析，给出地铁车站地震反应计算结果。通过与某国际先进通用有限元软件（简称软件 A）的计算结果对比，验证 GFE 软件的可靠性和优势。

# 6.1 软件操作

三维时程分析的 GFE 操作流程与二维时程分析基本一致，具体可参见 3.1 节时程分析的 10 个步骤，此处不再赘述。三维时程与二维时程的区别仅在模型维度上不同：导入 ydb 模型时，二维时程在 “模型维度” 上选择 “2D”，而三维时程选择 “3D”；二维时程生成二维土体，三维时程生成三维土体；三维时程在进行裁剪布尔操作时可由导入 ydb 时生成的外轮廓实体进行裁剪而无需额外的创建几何体操作；寻找接触时二维时程选择 “查找几何边”，三维时程选择 “查找几何面” 等。

# 6.2 E2 地震线性时程分析结果

采用 GFE 软件建立的三维土-结构系统分析模型如图 6.2-1 所示。土-结构系统模型的尺寸 X\*Y\*Z=500m\*200m\*50m，模型总节点数 602126 个，总单元数 3209579 个，其中梁单元数 2736 个，壳单元 44813 个，实体单元 3162030 个。土体采用一阶四面体单元模拟，网格尺寸为 3m；车站楼板和侧墙采用壳单元模拟，车站梁柱采用梁单元模拟，网格尺寸为 1.0m。

GFE 采用 2080 单显卡 GPU 双精度并行计算的总时间为 504min，采用 2080 双显卡 GPU 双精度并行计算的总时间为 263min，软件 A 采用 12 核 CPU 双精度并行计算的总时间为 2778min。可以看到，GFE 软件的计算耗时仅为软件 A 的 1/10，极大提高了三维时程分析的计算效率。

![](../assets/GFE-SSA/b502ad1e25168bb7b4d28ae052cbcae0d1f6db3337392079f5d03816bcd632a9.jpg)

<details>
<summary>text_image</summary>

200m
50m
500m
</details>

图 6.2-1 三维土-结构系统分析模型

# 6.2.1 结构内力

# (a) 梁柱轴力

图 6.2-2 和图 6.2-3 分别给出梁柱轴力时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 752kN，软件 A 计算结果云图中绝对值最大为 728kN，二者的差异率为 3.30%。

![](../assets/GFE-SSA/c996933538f227f12269edef391f6f983c84f362906517b98f343e5efbb80b71.jpg)  
图 6.2-2 梁柱轴力时程最大值分布

![](../assets/GFE-SSA/da2fa88eb0ad1c0c5072567364ee3edc4057bdb205ae3758fb7e9079339e1db1.jpg)  
图 6.2-3 梁柱轴力时程最小值分布

图 6.2-4 给出柱上 4498050 号单元位置。图 6.2-5 给出柱上 4498050 号单元轴力时程曲线。由图可知，GFE 软件和软件 A 计算梁柱轴力时程结果吻合较好，其中 GFE 软件计算的最大轴力为 -113.864kN，软件 A 计算的最大轴力为 -113.972kN，二者的差异率仅为 0.09%。

![](../assets/GFE-SSA/4271af543127757267ac4049722d28bdc43a83d4c330422915406b1269d3b92f.jpg)

<details>
<summary>text_image</summary>

Sequence of light blue dots with a red box highlighting the final cluster
</details>

(a) 整体展示

![](../assets/GFE-SSA/896b5451a6f05885e8f4574244f3480f7ad76a6e7250a4923a9d10b5ce9ce6b8.jpg)

<details>
<summary>text_image</summary>

Ele_4498050
</details>

(b) 局部展示  
图 6.2-4 柱上 4498050 单元位置

![](../assets/GFE-SSA/8e1b500dcfae202158895d99c284fcfa045f569c7f3cbf6c4802443a95d3debd.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE (kN) | 软件A (kN) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~7 | ~80 | ~-120 |
| ~14 | ~80 | ~-80 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 6.2-5 柱上 4498050 号单元轴力时程曲线

# (b) 梁柱弯矩

图 6.2-6 和图 6.2-7 分别给出梁柱 1 方向弯矩时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 663kN.m，软件 A 计算结果云图中绝对值最大为 668kN.m，二者的差异率仅为 0.75%。

![](../assets/GFE-SSA/1eb8fa391589de1f5e0a511fc5e01c54fdf5cee70bf9f24fa515a1aec854eeca.jpg)  
图 6.2-6 梁柱 1 方向弯矩时程最大值分布

![](../assets/GFE-SSA/1328a8fee37244b732a8c23225057377399c58580869cd25e5923b69c5d5474a.jpg)  
图 6.2-7 梁柱 1 方向弯矩时程最小值分布

图 6.2-8 给出柱上 4498050 号单元 1 方向弯矩时程曲线。由图可知，GFE 软件和软件 A 计算梁柱弯矩时程结果吻合较好，其中 GFE 软件计算的最大弯矩为 -170.754kN.m，软件 A 计算的最大弯矩为 -169.367kN.m，二者的差异率仅为 0.81%。

![](../assets/GFE-SSA/d19515fffd25f709481a8ac4fbd167778a6d01f7e2156937dbf127543cebffd6.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE \((kN \cdot m)\) | 软件A \((kN \cdot m)\) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~-170 | ~-160 |
| ~8 | ~150 | ~150 |
| ~11 | ~150 | ~150 |
| ~14 | ~120 | ~120 |
| ~15 | ~-130 | ~-130 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 6.2-8 柱上 4498050 号单元 1 方向弯矩时程曲线

# (c) 楼板轴力

图 6.2-9 和图 6.2-10 分别给出楼板 1 方向轴力时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 714kN，软件 A 计算结果云图中绝对值最大为 708kN，二者的差异率仅为 0.85%。

![](../assets/GFE-SSA/b364518f3f901d1606685adfae974b658cd058e4e707745543fecdac92cdc838.jpg)  
图 6.2-9 楼板 1 方向轴力时程最大值分布

![](../assets/GFE-SSA/b954ed9c38c1ff59dd6e94906dc232a12fdac061250e0d7622083a4a01ade2b8.jpg)  
图 6.2-10 楼板 1 方向轴力时程最小值分布

图 6.2-11 给出楼板 4503337 号单元位置。图 6.2-12 给出楼板 4503337 号单元 1 方向轴力时程曲线。由图可知，GFE 软件和软件 A 计算楼板轴力时程结果吻合较好，其中 GFE 软件计算的最大轴力为 -120.516kN，软件 A 计算的最大轴力为 -124.742kN，二者的差异率为 3.51%。

![](../assets/GFE-SSA/dc30dd685d6003f0761cc2d0fc557ac1d5e561d19bbda1c3b734198b187d3558.jpg)

<details>
<summary>natural_image</summary>

Blue layered metal structure with a red square highlighting a specific section (no text or symbols)
</details>

(a) 整体展示

![](../assets/GFE-SSA/8443c79ffce3cee2838cfca70b10d46c1fa9b96640be2220fce15bd02ede7a38.jpg)

<details>
<summary>text_image</summary>

Ele_4503337
</details>

(b) 局部展示

图 6.2-11 楼板 4503337 号单元位置  
![](../assets/GFE-SSA/4bd7180d0720120f80baec6d7ba94d5f746f35591baed83a6b9790dfbbecb4fb.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE (kN) | 软件A (kN) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~80 | ~80 |
| ~8 | ~-120 | ~-100 |
| ~10 | ~50 | ~50 |
| ~15 | ~70 | ~70 |
| ~20 | ~20 | ~20 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 6.2-12 楼板 4503337 号单元 1 方向轴力时程曲线

图 6.2-13 和图 6.2-14 分别给出地震作用下楼板 2 方向轴力时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 600kN，软件 A 计算结果云图中绝对值最大为 646kN，二者的差异率为 7.12%。

![](../assets/GFE-SSA/299cc9d5ba0c37f7809efef28c08fc72ba04b5f4362c9eaf37eb86e8a3bb634b.jpg)  
图 6.2-13 楼板 2 方向轴力时程最大值分布

![](../assets/GFE-SSA/be50236a1742c86056aba7bcc7f1e6c7f3e5a06dbba10ff222b56d357db97546.jpg)

<details>
<summary>natural_image</summary>

Thermal or density visualization of a layered rectangular structure with red, green, and blue gradients (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/7886d58d5b58476fdb1a61539c27c6e135a11aafe5fab5d9f13bb7fffcd079ee.jpg)

<details>
<summary>natural_image</summary>

3D visualization of a layered structure with color-coded stress or deformation (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/b5a58c5bb94a6f1abed36c0bd6ac68c42a2ec69c1b49bc703ef4d2ff7667b249.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | -6.74e-1 |
| Orange | -6.74e-1 |
| Yellow | -6.74e-1 |
| Green | -6.74e-1 |
| Cyan | -6.74e-1 |
| Blue | -6.74e-1 |
| Dark Blue | -6.46e2 |
</details>

图 6.2-14 楼板 2 方向轴力时程最小值分布

图 6.2-15 给出楼板 4503337 号单元 2 方向轴力时程曲线。由图可知，GFE 软件和软件 A 计算楼板轴力时程结果吻合较好，其中 GFE 软件计算的最大轴力为 538.547kN，软件 A 计算的最大轴力为 577.140kN，二者的差异率为 7.17%。

![](../assets/GFE-SSA/420b9541f39dc98e17ad78b5101916e1d6faa06d6e31571bdd2aa0550e0dbb64.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE (kN) | 软件A (kN) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 10 | ~150 | ~150 |
| 20 | ~50 | ~50 |
| 30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 6.2-15 楼板 4503337 号单元 2 方向轴力时程曲线

# (d) 楼板弯矩

图 6.2-16 和图 6.2-17 分别给出楼板 1 方向弯矩时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 121kN.m，软件 A 计算结果云图中绝对值最大为 121kN.m，二者完全相同。

![](../assets/GFE-SSA/2e1aa499a43973e565d87da30874f92f7458d8cac10090aa909062bdbaa3a46f.jpg)

<details>
<summary>text_image</summary>

(a) GFE 计算结果
(b) 软件 A 计算结果
+1.21e2	+1.36e-2 (kN·m)
</details>

图 6.2-16 楼板 1 方向弯矩时程最大值分布

![](../assets/GFE-SSA/9e4641e794557fa1c7f74289c1c0cbe6425d23359d42c9e8e4c1924004aef1f9.jpg)

<details>
<summary>text_image</summary>

(a) GFE 计算结果
(b) 软件 A 计算结果
-1.05e-2
-1.19e2 (kN·m)
</details>

图 6.2-17 楼板 1 方向弯矩时程最小值分布

图 6.2-18 给出楼板 4503337 号单元 1 方向弯矩时程曲线。由图可知，GFE 软件和软件 A 计算楼板弯矩时程结果吻合较好，其中 GFE 软件计算的最大弯矩为 117.955kN.m，软件 A 计算的最大弯矩为 115.269kN.m，二者的差异率为 2.28%。

![](../assets/GFE-SSA/dcf72aa831d39b648771b13c47e7545aacc3bf02f420fdadfa6481b411a969c4.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE \((kN \cdot m)\) | 软件A \((kN \cdot m)\) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~110 | ~100 |
| ~7 | ~-100 | ~-90 |
| ~10 | ~-90 | ~-80 |
| ~14 | ~80 | ~75 |
| ~15 | ~-90 | ~-85 |
| ~20 | ~10 | ~5 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 6.2-18 楼板 4503337 号单元 1 方向弯矩时程曲线

图 6.2-19 和图 6.2-20 分别给出楼板 2 方向弯矩时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 580kN.m，软件 A 计算结果云图中绝对值最大为 589kN.m，二者的差异率为 1.53%。

![](../assets/GFE-SSA/ce06ed711fb7734c89117a05bfe62bcd7d091f8bfc10daeff550789da4cf66c9.jpg)  
图 6.2-19 楼板 2 方向弯矩时程最大值分布

![](../assets/GFE-SSA/88ede5e5751cdfd93661866b61fedf382d855a223a8fba705e3487edc1729080.jpg)

<details>
<summary>natural_image</summary>

Thermal or heat map visualization of a rectangular object with red and green color gradients (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/5c0a607b9314d2604c682b9e63d9cfcd5a959c5196adc3d6678ec89b9b1676f4.jpg)

<details>
<summary>natural_image</summary>

3D rendered diagram of layered red rectangular structures with a 3D coordinate system (X, Y, Z) indicator, no text or symbols present.
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/c2caed877878677a2fc10b03149d3cb8a45480e566a18ee6f8f87fdc93fff097.jpg)

<details>
<summary>heatmap</summary>

| Color | Value \((kN \cdot m)\) |
| --- | --- |
| Red | -2.02e-2 |
| Orange | -2.02e-2 |
| Yellow | -2.02e-2 |
| Green | -2.02e-2 |
| Cyan | -2.02e-2 |
| Blue | -5.85e2 |
</details>

图 6.2-20 楼板 2 方向弯矩时程最小值分布

图 6.2-21 给出楼板 4503337 号单元 2 方向弯矩时程曲线。由图可知，GFE 软件和软件 A 计算楼板弯矩时程结果吻合较好，其中 GFE 软件计算的最大弯矩为 580.155kN.m，软件 A 计算的最大弯矩为 585.816kN.m，二者的差异率为 0.98%。

![](../assets/GFE-SSA/384f9f7bf681c32e6745f289a1e4f8892d6c0616ded9fa979f029c47cf31d51c.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE \((kN \cdot m)\) | 软件A \((kN \cdot m)\) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~550 | ~550 |
| ~7 | ~-550 | ~-550 |
| ~10 | ~-500 | ~-500 |
| ~14 | ~-500 | ~-500 |
| ~15 | ~400 | ~400 |
| ~16 | ~-500 | ~-500 |
| ~20 | ~0 | ~0 |
| ~30 | 0 | 0 |
| 40 | 0 | 0 |
</details>

图 6.2-21 楼板 4503337 号单元 2 方向弯矩时程曲线

# (e) 侧墙轴力

图 6.2-22 和图 6.2-23 分别给出侧墙 1 方向轴力时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 676kN，软件 A 计算结果云图中绝对值最大为 670kN，二者的差异率为 0.90%。

![](../assets/GFE-SSA/bdbd69a5d2b21c8bc06b3cab40a38d636031196c936bc64ad02d638787bbcc72.jpg)

<details>
<summary>heatmap</summary>

| Result Type | Description |
| --- | --- |
| (a) GFE 计算结果 | Heatmap visualization of the GFE model showing force distribution. |
| (b) 软件 A 计算结果 | Heatmap visualization of the Software A model showing force distribution. |
</details>

图 6.2-22 侧墙 1 方向轴力时程最大值分布

![](../assets/GFE-SSA/f3251de3aed3413143064a28106ada0fdc3e375a8d474871644030affe4b4105.jpg)

<details>
<summary>text_image</summary>

(a) GFE 计算结果
(b) 软件 A 计算结果
-4.44e1
-6.60e2 (kN)
</details>

图 6.2-23 侧墙 1 方向轴力时程最小值分布

图 6.2-24 和图 6.2-25 分别给出侧墙 2 方向轴力时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 509kN，软件 A 计算结果云图中绝对值最大为 509kN，二者完全相同。

![](../assets/GFE-SSA/153a8cf93c3a99336c22ff3d107a7a7f91c79a5fe06bc35a195fc23a22ec59cb.jpg)

<details>
<summary>text_image</summary>

(a) GFE 计算结果
(b) 软件 A 计算结果
+5.00e2
+1.70e0 (kN)
</details>

图 6.2-24 侧墙 2 方向轴力时程最大值分布

![](../assets/GFE-SSA/186d23b3da4b5f0a2597ba77849a22e142caf4282a25ea0bf21746f9b39255b9.jpg)

<details>
<summary>heatmap</summary>

| Result Type | Description |
| --- | --- |
| (a) GFE 计算结果 | Heatmap visualization of the GFE model showing force distribution. |
| (b) 软件 A 计算结果 | Heatmap visualization of the Software A model showing force distribution. |
</details>

图 6.2-25 侧墙 2 方向轴力时程最小值分布

# (f) 侧墙弯矩

图 6.2-26 和图 6.2-27 分别给出侧墙 1 方向弯矩时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 112kN.m，软件 A 计算结果云图中绝对值最大为 113kN.m，二者的差异率为 0.88%。

![](../assets/GFE-SSA/984a7d0a25119a86a3ba8ac5bcea50bd59f8218c4fb8edd1e386f9f1e7cd8bd4.jpg)

<details>
<summary>text_image</summary>

(a) GFE 计算结果
(b) 软件 A 计算结果
+1.13e2
+7.84e-2 (kN·m)
</details>

图 6.2-26 侧墙 1 方向弯矩时程最大值分布

![](../assets/GFE-SSA/1b16a3c4baa6b82f38d6f515dabe96da358d324f913b502717df904cc53b5bf5.jpg)  
图 6.2-27 侧墙 1 方向弯矩时程最小值分布

图 6.2-28 和图 6.2-29 分别给出侧墙 2 方向弯矩时程最大值和最小值分布云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算结果云图中绝对值最大为 507kN.m，软件 A 计算结果云图中绝对值最大为 508kN.m，二者的差异率为 0.20%。

![](../assets/GFE-SSA/13bc29c69ae9e311af4af68fc9802a2445496570f89fec82a4fe1c3a12042053.jpg)  
图 6.2-28 侧墙 2 方向弯矩时程最大值分布

![](../assets/GFE-SSA/d4fea39c6c308922a6ded9f5bc6a9f7869ca6fda99f69175aa16e83c28d2663d.jpg)

<details>
<summary>text_image</summary>

(a) GFE 计算结果
(b) 软件 A 计算结果
-4.10e-2                    -4.56e2 (kN·m)
</details>

图 6.2-29 侧墙 2 方向弯矩时程最小值分布

# 6.2.2 结构变形

# (a) 水平位移

图 6.2-30 给出位移反应较大时刻车站结构的水平位移云图。由图可知，GFE 软件和软件 A 计算的结果吻合较好，其中 GFE 软件计算云图结果中的最大水平位移为 0.0291m，软件 A 计算云图结果中的最大水平位移为 0.0299m，二者的差异率仅为 2.68%。

![](../assets/GFE-SSA/148e42f1f854cf40e871fb03a349a528eaa963d719f792a9b32418dc76170234.jpg)

<details>
<summary>natural_image</summary>

3D rendered elongated object with rainbow gradient from red to green (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/b1c6572f4214631ae85fe8d7d97230f3839cdebbfde7c6e1d5459bde14c99ffe.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (m) |
| --- | --- |
| Red | +3.00e-2 |
| Orange | +3.00e-2 |
| Yellow | +3.00e-2 |
| Light Green | +3.00e-2 |
| Green | +3.00e-2 |
| Cyan | +3.00e-2 |
| Blue | +3.00e-2 |
| Dark Blue | +1.90e-2 |
</details>

(b) 软件 A 计算结果  
图 6.2-30 车站结构水平位移云图（放大 200 倍）

图 6.2-31 给出图 6.2-30 中结构中间断面的水平位移云图。由图可知，GFE 软件和软件 A 计算结果吻合较好，其中 GFE 软件计算的最大水平位移为 0.0291m，软件 A 计算的最大水平位移为 0.0299m，二者的差异率仅为 2.68%。

![](../assets/GFE-SSA/476a5cbccb2893aa5fb0d446f146857d2d1b63467506deef5285a467b7b3e14e.jpg)

<details>
<summary>natural_image</summary>

Simple 3D geometric shape with rainbow-colored edges, no text or symbols present
</details>

+3.00e-2

![](../assets/GFE-SSA/5ce8ac981a5f2d4fce2f10c89f3a2c6daa85e09eba310f053eb3502740618d3a.jpg)

<details>
<summary>flowchart</summary>

```mermaid
graph LR
  A["Red Path"] --> B["Green Path"]
  B --> C["Blue Path"]
  C --> D["Data Point 1"]
  C --> E["Data Point 2"]
  D --> F["Final Result"]
  E --> F
```
</details>

+1.90e-2 (m)

![](../assets/GFE-SSA/368f274b62b482fa717be1c325321d3c9598eb662f134731000eced6183c4ac4.jpg)

<details>
<summary>natural_image</summary>

Color gradient bar with 12 vertical lines, transitioning from red to blue (no text or symbols)
</details>

(a) GFE 计算结果  
(b) 软件 A 计算结果  
图 6.2-31 结构中间断面水平位移云图（放大 200 倍）

# (b) 层间位移角

图 6.2-32 给出图 6.2-31 结构中间断面各层的层间位移角结果。由图可知，GFE 软件和软件 A 计算的层间位移角结果吻合较好，GFE 软件计算的最大层间位移角为 1/1127，软件 A 计算的最大层间位移角为 1/1140，二者的差异率仅为 1.15%。

![](../assets/GFE-SSA/f6956486d44c2d3d5b42e760fd3b096a8c1d2750664f8188177bf8465816fa44.jpg)

<details>
<summary>line</summary>

| 层数 | GFE (层间位移角) | 软件A (层间位移角) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | ~1/800 | 1 |
| 2 | ~1/800 | 2 |
</details>

图 6.2-32 结构各层层间位移角

结构中间断面底层层间位移角最大，图 6.2-33 给出结构底层层间位移角时程曲线。由图

可知，GFE 软件和软件 A 计算的底层层间位移角时程结果吻合较好。

![](../assets/GFE-SSA/d241f5c6b80707aebeb0f72de3be3ccc498258a63f53788c0934d3d517cfe7b1.jpg)

<details>
<summary>line</summary>

| 时间/s | GFE (层间位移角) | 软件A (层间位移角) |
| --- | --- | --- |
| 0 | 0 | 0 |
| ~4 | ~1/800 | ~1/800 |
| ~6 | ~-1/2500 | ~-1/2500 |
| ~8 | ~1/2000 | ~1/2000 |
| ~10 | ~-1/2500 | ~-1/2500 |
| ~12 | ~1/2000 | ~1/2000 |
| ~14 | ~-1/2500 | ~-1/2500 |
| ~16 | ~1/2000 | ~1/2000 |
| ~18 | ~-1/2500 | ~-1/2500 |
| ~20 | ~1/2000 | ~1/2000 |
| ~22 | ~-1/2500 | ~-1/2500 |
| ~24 | ~1/2000 | ~1/2000 |
| ~26 | ~-1/2500 | ~-1/2500 |
| ~28 | ~1/2000 | ~1/2000 |
| ~30 | ~-1/2500 | ~-1/2500 |
| ~32 | ~1/2000 | ~1/2000 |
| ~34 | ~-1/2500 | ~-1/2500 |
| ~36 | ~1/2000 | ~1/2000 |
| ~38 | ~-1/2500 | ~-1/2500 |
| 40 | 0 | 0 |
</details>

图 6.2-33 结构底层层间位移角时程曲线

# 6.3 E3 地震非线性时程分析结果

建立的有限元模型尺寸和网格划分与6.2节相同。为模拟材料非线性，结构梁单元采用一维混凝土塑性损伤本构；结构分层壳单元采用平面应力混凝土塑性损伤本构，材料参数见表2.1-1。钢筋由YJK软件给出，通过接口程序导入GFE。土层的本构模型分别采用Davidenkov本构模型和Mohr-Coulomb本构模型，土层材料参数见表2.2-2-表2.2-3。重力荷载作用下的结果见附录一。由于与软件A中材料非线性本构模型的差异，本小节仅给出GFE软件的计算结果。

# 6.3.1 结构损伤

# (a) 梁的损伤

图 6.3-1\~图 6.3-3 和图 6.3-4\~图 6.3-6 分别给出非线性时程分析最终时刻梁的压损伤云图和拉损伤云图。由图可知，采用不同土体本构模型，地铁车站的损伤云图分布差异不大，但损伤最大值结果有一定差异。由于混凝土抗拉强度低，梁的拉损伤值远远超过压损伤值，而且拉损伤值集中于梁柱支座处，其中第二层梁损伤最为严重，最大达 0.96；受压损伤较小。

![](../assets/GFE-SSA/579352094f060f3d558c9cdc0aaeecd8f6380dd8b5f19693600874751b24ca27.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 5.20e-3 |
| Orange | 5.20e-3 |
| Yellow | 5.20e-3 |
| Light Green | 5.20e-3 |
| Green | 5.20e-3 |
| Cyan | 5.20e-3 |
| Blue | 5.20e-3 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/ce83910df5988d587732a5a952ff14b5251786ac00ec0c0c0ba4857ae14ab314.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 2.00e-2 |
| Orange | 2.00e-2 |
| Yellow | 2.00e-2 |
| Light Green | 2.00e-2 |
| Green | 2.00e-2 |
| Cyan | 2.00e-2 |
| Blue | 2.00e-2 |
| Dark Blue | 2.00e-2 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-1 第一层梁压损伤云图

![](../assets/GFE-SSA/8d91a85ca97a95d21b74463194b3d0afa8b634901aa3eadf86abb96ccb4b8fed.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 3.40e-3 |
| Orange | 3.40e-3 |
| Yellow | 3.40e-3 |
| Green | 3.40e-3 |
| Cyan | 3.40e-3 |
| Blue | 3.40e-3 |
| Dark Blue | 3.40e-3 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/544106fd2e81a913c37d556cc7991ae61331200796a3a861a725f878a173e392.jpg)

<details>
<summary>heatmap</summary>

| Color | Value |
| --- | --- |
| Red | 3.30e-2 |
| Orange | 3.30e-2 |
| Yellow | 3.30e-2 |
| Green | 3.30e-2 |
| Cyan | 3.30e-2 |
| Blue | 3.30e-2 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-2 第二层梁压损伤云图

![](../assets/GFE-SSA/6bac44ee00bd1fbe3c287ead21c495a3234681ab59a48a07f2da9fa111b769c9.jpg)

<details>
<summary>heatmap</summary>

| Color | Value |
| --- | --- |
| Red | 4.20e-3 |
| Orange | 4.20e-3 |
| Yellow | 4.20e-3 |
| Green | 4.20e-3 |
| Cyan | 4.20e-3 |
| Blue | 4.20e-3 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/5a9149f872629e350891bd66ee8d6040caf629289346f81023b2c5bed6242a85.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 2.60e-2 |
| Orange | 2.60e-2 |
| Yellow | 2.60e-2 |
| Light Green | 2.60e-2 |
| Green | 2.60e-2 |
| Cyan | 2.60e-2 |
| Blue | 2.60e-2 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-3 第三层梁压损伤云图

![](../assets/GFE-SSA/bbfa44d0bfe9bc99a8ef1982cc870054b50230c62134e5b2f601558c7aed70b6.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 2.20e-1 |
| Orange | 2.20e-1 |
| Yellow | 2.20e-1 |
| Green | 2.20e-1 |
| Cyan | 2.20e-1 |
| Blue | 2.20e-1 |
| Dark Blue | 0.00 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/9ab2bdd682d60f8fbd93ef6646db1c75ecbcfcbc888477952cc024d8871ff539.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 6.80e-1 |
| Orange | 6.80e-1 |
| Yellow | 6.80e-1 |
| Green | 6.80e-1 |
| Cyan | 6.80e-1 |
| Blue | 6.80e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-4 第一层梁拉损伤云图

![](../assets/GFE-SSA/5cc7295898ab69ba136af5897f5bc4ba98e43f56f3cf39cebfe046f9328b6a5b.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 4.60e-1 |
| Orange | 4.60e-1 |
| Yellow | 4.60e-1 |
| Light Green | 4.60e-1 |
| Green | 4.60e-1 |
| Cyan | 4.60e-1 |
| Blue | 4.60e-1 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/db5235aafe8528d83c671eeba457524120dfdd14c0e74069aad0e2313bb8e0c6.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 9.60e-1 |
| Orange | 9.60e-1 |
| Yellow | 9.60e-1 |
| Light Green | 9.60e-1 |
| Green | 9.60e-1 |
| Cyan | 9.60e-1 |
| Blue | 9.60e-1 |
| Dark Blue | 9.60e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-5 第二层梁拉损伤云图

![](../assets/GFE-SSA/6b78b5e62e89e63fbe62c8de6975459cd4cf4326d161659b82726bd538b00f86.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 7.30e-1 |
| Orange | 7.30e-1 |
| Yellow | 7.30e-1 |
| Light Green | 7.30e-1 |
| Green | 7.30e-1 |
| Cyan | 7.30e-1 |
| Blue | 7.30e-1 |
| Dark Blue | 7.30e-1 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/81bb1e1cfa5015bfc4a46d4bbba5f8ae3613ccbd264ecd2cd1735445f991c892.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 9.60e-1 |
| Orange | 9.60e-1 |
| Yellow | 9.60e-1 |
| Light Green | 9.60e-1 |
| Green | 9.60e-1 |
| Cyan | 9.60e-1 |
| Blue | 9.60e-1 |
| Dark Blue | 9.60e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-6 第三层梁拉损伤云图

# (b) 楼板的损伤

图 6.3-7\~图 6.3-9 和图 6.3-10\~图 6.3-12 分别给出非线性时程分析最终时刻楼板的压损伤云图和拉损伤云图。由图可知，采用不同土体本构模型，地铁车站的损伤云图分布差异不大，但损伤最大值结果有一定差异。如上，由于混凝土抗拉强度低，楼板的拉损伤值远远超过压损伤值，受压损伤较小。

![](../assets/GFE-SSA/f15c2d58822167e245718dae68c4f0ba87ddc3bf2c6b9b658236eb8a8066fe1e.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 4.00e-4 |
| Orange | 4.00e-4 |
| Yellow | 4.00e-4 |
| Light Green | 4.00e-4 |
| Green | 4.00e-4 |
| Cyan | 4.00e-4 |
| Light Blue | 4.00e-4 |
| Blue | 4.00e-4 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/cd08b15c3199ff088640a016e76087c02f28a46e3b07f5cafd5f677e1e73da53.jpg)

<details>
<summary>heatmap</summary>

| Color Range | Value Range |
| --- | --- |
| Red | 3.30e-3 ~ 0.00 |
| Orange | 3.30e-3 ~ 0.00 |
| Yellow | 3.30e-3 ~ 0.00 |
| Light Green | 3.30e-3 ~ 0.00 |
| Green | 3.30e-3 ~ 0.00 |
| Cyan | 3.30e-3 ~ 0.00 |
| Light Blue | 3.30e-3 ~ 0.00 |
| Medium Blue | 3.30e-3 ~ 0.00 |
| Dark Blue | 3.30e-3 ~ 0.00 |
</details>

(b) Mohr-Coulomb 本构模型

图 6.3-7 第一层楼板压损伤  
![](../assets/GFE-SSA/39f89730d1ae0215d7a79fa21ef6db961ac0ddcf9b33d98fb79cac548e010eec.jpg)

<details>
<summary>heatmap</summary>

| Color Range | Value Range |
| --- | --- |
| Red | 3.80e-4 ~ 0.00 |
| Orange | 3.80e-4 ~ 0.00 |
| Yellow | 3.80e-4 ~ 0.00 |
| Light Green | 3.80e-4 ~ 0.00 |
| Green | 3.80e-4 ~ 0.00 |
| Cyan | 3.80e-4 ~ 0.00 |
| Light Blue | 3.80e-4 ~ 0.00 |
| Blue | 3.80e-4 ~ 0.00 |
| Dark Blue | 3.80e-4 ~ 0.00 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/9c727b802d9fe4c00d3e474e36364cbd87804c66baa1a0055ae31394b4ce83a5.jpg)

<details>
<summary>heatmap</summary>

| Color Range | Value |
| --- | --- |
| Red | 1.10e-2 |
| Orange | 1.10e-2 |
| Yellow | 1.10e-2 |
| Light Green | 1.10e-2 |
| Green | 1.10e-2 |
| Cyan | 1.10e-2 |
| Light Blue | 1.10e-2 |
| Dark Blue | 0.00 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-8 第二层楼板压损伤

![](../assets/GFE-SSA/79dcb6c5a5ea6dc7a99f3bc7817573527bddf54799a5e9d20263dbab852346c5.jpg)

<details>
<summary>natural_image</summary>

Blue rectangular block with a horizontal yellow line at the top (no text or symbols)
</details>

![](../assets/GFE-SSA/b1dac0c4b0a53d109aa4670c293ede11a3dec963fc16d14dd37157cf69c8b90d.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 3.70e-4 |
| Orange | 3.70e-4 |
| Yellow | 3.70e-4 |
| Light Green | 3.70e-4 |
| Green | 3.70e-4 |
| Cyan | 3.70e-4 |
| Blue | 3.70e-4 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/30c344c22f86e8b5377ca565a4dfdfc8913ed13233b01b5c6bf6a3a4a684373a.jpg)

<details>
<summary>text_image</summary>

Cropped image showing partial text with blue background and pixelated pattern, likely from a document or form.
</details>

![](../assets/GFE-SSA/712c0446e85496086ac61efdbb1d6d8d841307d41e3fa0f09f73c25aac90dd64.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 4.50e-3 |
| Orange | 4.50e-3 |
| Yellow | 4.50e-3 |
| Light Green | 4.50e-3 |
| Green | 4.50e-3 |
| Cyan | 4.50e-3 |
| Blue | 4.50e-3 |
| Dark Blue | 4.50e-3 |
</details>

(b) Mohr-Coulomb 本构模型

图 6.3-9 第三层楼板压损伤  
![](../assets/GFE-SSA/34bcb9efcec281c3fa792fd16b8063a18ebfb63d2d2d7a47a3eaf57f68087478.jpg)

<details>
<summary>natural_image</summary>

Solid blue rectangular frame with a row of small square markers at the top and bottom (no text or symbols)
</details>

![](../assets/GFE-SSA/2c636b8d66458e0dba02a223743cc41e6dc7b879d2a9f0913ce748cac6fdff42.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 4.00e-1 |
| Orange-Red | 4.00e-1 |
| Orange | 4.00e-1 |
| Yellow-Orange | 4.00e-1 |
| Yellow | 4.00e-1 |
| Yellow-Green | 4.00e-1 |
| Green | 4.00e-1 |
| Green-Cyan | 4.00e-1 |
| Cyan | 4.00e-1 |
| Light Blue | 4.00e-1 |
| Blue | 4.00e-1 |
| Dark Blue | 4.00e-1 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/591e09d9380d62494dc56209b63bb0579cb8cee9d569e49350e83d7c385dd322.jpg)

<details>
<summary>natural_image</summary>

Blue rectangular frame with evenly spaced yellow dots on top, no text or symbols visible
</details>

![](../assets/GFE-SSA/c8c4e530472bf13112593823abb43a8137d656d39f2008328d9d01d315e7e5ed.jpg)

<details>
<summary>heatmap</summary>

| Color Gradient | Value |
| --- | --- |
| Red | 4.00e-1 |
| Orange | 4.00e-1 |
| Yellow | 4.00e-1 |
| Light Green | 4.00e-1 |
| Green | 4.00e-1 |
| Cyan | 4.00e-1 |
| Blue | 4.00e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-10 第一层楼板拉损伤

![](../assets/GFE-SSA/526a6fa652e99e7b695a12fc7e897bc1632308de703fb2066bcccbb45aa9f5a0.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 0.00~4.00e-1 |
| Orange | 0.00~4.00e-1 |
| Yellow | 0.00~4.00e-1 |
| Light Green | 0.00~4.00e-1 |
| Green | 0.00~4.00e-1 |
| Cyan | 0.00~4.00e-1 |
| Light Blue | 0.00~4.00e-1 |
| Blue | 0.00~4.00e-1 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/35975ad7a3c3d61e8c63dc60de1cd2ca0c0bd67cf9c33517654b6d7d4f423ef2.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 0.00~4.00e-1 |
| Orange | 0.00~4.00e-1 |
| Yellow | 0.00~4.00e-1 |
| Light Green | 0.00~4.00e-1 |
| Green | 0.00~4.00e-1 |
| Cyan | 0.00~4.00e-1 |
| Light Blue | 0.00~4.00e-1 |
| Blue | 0.00~4.00e-1 |
</details>

(b) Mohr-Coulomb 本构模型

图 6.3-11 第二层楼板拉损伤  
![](../assets/GFE-SSA/579a4b7028118800d76f09ddf46ded4a3e149932dffd8ec5cb40da0ed67e61d9.jpg)

<details>
<summary>heatmap</summary>

| Color Range | Value Range |
| --- | --- |
| Red | 4.00e-1 |
| Orange | ~3.50e-1 |
| Yellow | ~3.00e-1 |
| Green | ~2.50e-1 |
| Cyan | ~2.00e-1 |
| Light Blue | ~1.50e-1 |
| Blue | 0.00 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/1d9f0e65318b3f9a18b9681e68a516138186e07036e999f856b37031c0e97afb.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 0.00~4.00e-1 |
| Orange | 0.00~4.00e-1 |
| Yellow | 0.00~4.00e-1 |
| Green | 0.00~4.00e-1 |
| Cyan | 0.00~4.00e-1 |
| Blue | 0.00~4.00e-1 |
| Dark Blue | 0.00~4.00e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-12 第三层楼板拉损伤

# (c) 侧墙的损伤

图 6.3-13\~图 6.3-14 和图 6.3-15\~图 6.3-16 分别给出非线性时程分析最终时刻侧墙的压损伤云图和拉损伤云图。由图可知，采用不同土体本构模型，地铁车站的损伤云图分布差异不大。如上，由于混凝土抗拉强度低，侧墙的拉损伤值远远超过压损伤值，而且拉损伤值集中于侧墙上端和下端，最大拉损伤值达 0.4，受压损伤较小。

![](../assets/GFE-SSA/3fc36ab8c5986a5543c04de80ea1a3b55721d80051abef10a4658c8c1fa0ac72.jpg)

<details>
<summary>heatmap</summary>

| Metric | Value |
| --- | --- |
| Maximum Value | 5.30e-4 |
| Minimum Value | 0.00 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/3edcf76b19010b96ba19819a34acd3c4cd2b2bdeb652a17b5e7d3f5a5c80ee80.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 7.30e-4 |
| Orange | 7.30e-4 |
| Yellow | 7.30e-4 |
| Green | 7.30e-4 |
| Cyan | 7.30e-4 |
| Blue | 0.00 |
</details>

(b) Mohr-Coulomb 本构模型

图 6.3-13 第二层侧墙压损伤  
![](../assets/GFE-SSA/7105f053c2c48f90bd965d6f638206e32703b07d0a84f9dae3616c2c3704f6e3.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 3.80e-4 |
| Orange | 3.80e-4 |
| Yellow | 3.80e-4 |
| Green | 3.80e-4 |
| Cyan | 3.80e-4 |
| Blue | 0.00 |
</details>

(a) Davidenkov 本构模型  
![](../assets/GFE-SSA/8975ed009abcea4befcb3c0f91eb9b16e805febc525cc6e2c53477862ac318a9.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 1.40e-3 |
| Orange | 1.40e-3 |
| Yellow | 1.40e-3 |
| Green | 1.40e-3 |
| Cyan | 1.40e-3 |
| Blue | 1.40e-3 |
| Dark Blue | 0.00 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-14 第三层侧墙压损伤

![](../assets/GFE-SSA/aa9ebf42b74adfdd154d13912e7d1b83197f8372fbc7a0d2f662b948f0a0a960.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 4.00e-1 |
| Orange | ~3.50e-1 |
| Yellow | ~3.00e-1 |
| Green | ~2.50e-1 |
| Cyan | ~2.00e-1 |
| Light Blue | ~1.50e-1 |
| Blue | 0.00 |
</details>

(a) Davidenkov 本构模型  
![](../assets/GFE-SSA/a5ae3e403d0d548d9794bf4a42415f5dcd046c50ab6bffaf00fc3611bed82959.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 0.00~4.00e-1 |
| Orange | 0.00~4.00e-1 |
| Yellow | 0.00~4.00e-1 |
| Green | 0.00~4.00e-1 |
| Cyan | 0.00~4.00e-1 |
| Blue | 0.00~4.00e-1 |
</details>

(b) Mohr-Coulomb 本构模型

图 6.3-15 第二层侧墙拉损伤  
![](../assets/GFE-SSA/f1ea45dc5531a8017a531b9a6e892839140a36d9b38e06c28fcf26a9564a272a.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 3.80e-4 |
| Orange | ~3.80e-4 |
| Yellow | ~3.80e-4 |
| Green | ~3.80e-4 |
| Cyan | ~3.80e-4 |
| Blue | 0.00 |
</details>

(a) Davidenkov 本构模型  
![](../assets/GFE-SSA/284e9a5b59113b85af81efb8eafc9aa936443ccb5a5cc0f969f6599f1d87aaa3.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 4.00e-1 |
| Orange | 4.00e-1 |
| Yellow | 4.00e-1 |
| Light Green | 4.00e-1 |
| Green | 4.00e-1 |
| Cyan | 4.00e-1 |
| Light Blue | 4.00e-1 |
| Blue | 4.00e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-16 第三层侧墙拉损伤

# (d) 柱的损伤

图 6.3-17\~图 6.3-18 和图 6.3-19\~图 6.3-20 分别给出非线性时程分析最终时刻柱的压损伤云图和拉损伤云图。由图可知，采用不同土体本构模型，地铁车站的损伤云图分布差异不大。柱的拉损伤和压损伤均比较大，而且拉损伤值集中于柱和板连接处，最大拉损伤值达 0.99，受压损伤值较小。

![](../assets/GFE-SSA/4031647c5845d1f39959ae772906d5b6a8e00af6cea1822c62cc76fa5b09926d.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 1.80e-1 |
| Orange | 1.80e-1 |
| Yellow | 1.80e-1 |
| Green | 1.80e-1 |
| Cyan | 1.80e-1 |
| Blue | 1.80e-1 |
| Dark Blue | 0.00 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/5a845b8dd8ab9223ec95db0c78795351a91480a4d2ddbc7fc101fa2d5384d1df.jpg)

<details>
<summary>heatmap</summary>

| Color | Intensity Range |
| --- | --- |
| Red | 2.30e-1 ~ 0.00 |
| Orange | 2.30e-1 ~ 0.00 |
| Yellow | 2.30e-1 ~ 0.00 |
| Green | 2.30e-1 ~ 0.00 |
| Cyan | 2.30e-1 ~ 0.00 |
| Blue | 2.30e-1 ~ 0.00 |
| Dark Blue | 2.30e-1 ~ 0.00 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-17 第二层柱压损伤

![](../assets/GFE-SSA/92176d12e40d8b35cd3ed1370638ed77814b0c36275a2bbbff74cc51e60fbcbc.jpg)  
图 6.3-18 第三层柱压损伤

![](../assets/GFE-SSA/a425f94d9afecf2c22f7903d37b17fd95ddb25acf93da2cee847719afc7d4ae9.jpg)  
图 6.3-19 第二层柱拉损伤

![](../assets/GFE-SSA/69fcbda5fc6bccd7c0605e17bb03ee6a48e38a588d9ca62ff9ce20c9fdd128f8.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range |
| --- | --- |
| Red | 0.00~9.60e-1 |
| Orange | 0.00~9.60e-1 |
| Yellow | 0.00~9.60e-1 |
| Green | 0.00~9.60e-1 |
| Cyan | 0.00~9.60e-1 |
| Blue | 0.00~9.60e-1 |
| Dark Blue | 0.00~9.60e-1 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/b337580699034135f07cb36e32341a3db690cdeef1ff2010f1acfb83f78fcd3e.jpg)

<details>
<summary>heatmap</summary>

| Color | Intensity Range |
| --- | --- |
| Red | 0.00~0.99e-1 |
| Orange | 0.00~0.99e-1 |
| Yellow | 0.00~0.99e-1 |
| Green | 0.00~0.99e-1 |
| Cyan | 0.00~0.99e-1 |
| Blue | 0.00~0.99e-1 |
| Dark Blue | 0.00~0.99e-1 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-20 第三层柱拉损伤

# (e) 楼板和侧墙钢筋的塑性应变

图 6.3-21 和图 6.3-22 分别给出非线性时程分析最终时刻楼板和侧墙钢筋 1 方向和 2 方向的塑性应变云图。由图可知，采用不同土体本构模型，地铁车站的塑性应变分布差异不大。最终时刻楼板和侧墙钢筋 1 方向和 2 方向的塑性应变分别为 0 和 3.25e-4。

![](../assets/GFE-SSA/2cad104c0e103a21a60832d0896d8cbd669233eab495d0afbc2f82b1b19c92a5.jpg)

<details>
<summary>natural_image</summary>

3D model of a blue rectangular structure with a vertical cutout, rendered in a gradient blue color scale (no text or symbols on the model itself)
</details>

(a) Davidenkov 本构模型  
![](../assets/GFE-SSA/8d701a4d1886f1e2356e9709b79b48133ab2f3046b1ec4d7d8d8481371bd146b.jpg)

<details>
<summary>natural_image</summary>

3D model of a blue structural beam with a U-shaped end, showing coordinate axes (X, Y, Z) and a color gradient legend (PE, R_PE1), no text or symbols present.
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-21 楼板和侧墙钢筋 1 方向塑性应变

![](../assets/GFE-SSA/3d310e9b938c3c92c6705014894339792255c2a9433c7f86befdd9f8075bf92d.jpg)

<details>
<summary>surface_3d</summary>

| Color | PE, R_PE2 |
| --- | --- |
| Red | 3.25E-04 |
| Orange | 2.98E-04 |
| Yellow | 2.71E-04 |
| Light Green | 2.43E-04 |
| Green | 2.16E-04 |
| Teal | 1.89E-04 |
| Cyan | 1.62E-04 |
| Light Blue | 1.35E-04 |
| Blue | 1.08E-04 |
| Dark Blue | 8.12E-05 |
| Deep Blue | 5.41E-05 |
| Very Deep Blue | 2.71E-05 |
| Deepest Blue | 0.005E+00 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/3f9941af7cf4be91075ec4723f30139fa82724ec364b8d67cf34bc49a2f58501.jpg)

<details>
<summary>surface_3d</summary>

| Color | PE, R_PE2 |
| --- | --- |
| Red | 3.25E-04 |
| Orange | 2.98E-04 |
| Yellow-Orange | 2.71E-04 |
| Yellow | 2.43E-04 |
| Light Green | 2.16E-04 |
| Green | 1.89E-04 |
| Teal | 1.62E-04 |
| Cyan | 1.35E-04 |
| Light Blue | 1.08E-04 |
| Blue | 8.12E-05 |
| Dark Blue | 5.41E-05 |
| Deep Blue | 2.71E-05 |
| Darkest Blue | 0.00E+00 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-22 楼板和侧墙钢筋 2 方向塑性应变

# (f) 梁柱钢筋的塑性应变

图 6.3-23 分别给出非线性时程分析最终时刻梁柱钢筋塑性应变云图。由图可知，最终时刻梁柱钢筋塑性应变为 3.81e-4。

![](../assets/GFE-SSA/49af980c2a5862519e030fac426216fcfa9fdf251f131ffedd5bd68d06a5dbf0.jpg)

<details>
<summary>heatmap</summary>

| Color | PE, PE11 |
| --- | --- |
| Red | 3.81E-04 |
| Orange-Red | 3.46E-04 |
| Orange | 3.11E-04 |
| Yellow-Orange | 2.76E-04 |
| Yellow | 2.41E-04 |
| Light Green | 2.06E-04 |
| Green | 1.71E-04 |
| Light Green | 1.36E-04 |
| Cyan | 1.02E-04 |
| Light Blue | 6.66E-05 |
| Blue | 3.17E-05 |
| Dark Blue | -3.26E-06 |
| Deep Blue | -3.82E-05 |
</details>

图 6.3-23 梁柱钢筋塑性应变（Mohr-Coulomb 本构模型）

# 6.3.2 结构变形

图 6.3-24 给出结构各层的层间位移角。由图可知，土体采用 Davidenkov 本构模型和 Mohr-Coulomb 本构模型计算所得最大层间位移角分别为 1/502 和 1/532，两种本构模型时车站结构均发生了较大的层间变形，但均未超过规范规定的限值 1/250。图 6.3-25 给出结构底层层间位移角时程曲线。

![](../assets/GFE-SSA/9a4f2162954d78675a7169aafb5c4b651103ea295f7f8049e5ab98f289ea7df4.jpg)

<details>
<summary>line</summary>

| 层数 | 层间位移角 |
| --- | --- |
| 0 | 0 |
| 1 | 1/500 |
| 2 | 1/500 |
</details>

(a) Davidenkov 本构模型

![](../assets/GFE-SSA/9d694a08aa67ce1757c484743753c7f771110803d6cac8b4f30d40f5cfd2cdb1.jpg)

<details>
<summary>line</summary>

| 层数 | 层间位移角 |
| --- | --- |
| 0 | 0 |
| 1 | 1/500 |
| 2 | 1/500 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-24 结构各层层间位移角

![](../assets/GFE-SSA/85b4ba2de09bd7f9d04674a85f512e2153a3232c0154281c128d5ebcde893cd8.jpg)

<details>
<summary>line</summary>

| 时间/s | 层间位移角 |
| --- | --- |
| 0 | 0 |
| ~4 | ~-0.45 |
| ~11 | ~0.35 |
| ~15 | ~-0.40 |
| ~20 | ~0.10 |
| ~30 | ~0.05 |
| 40 | 0 |
</details>

(a) Davidenkov 本构模型  
![](../assets/GFE-SSA/5b64deeb94bb4ae8354d2799a7e4e99b077ced9a34baf4f3cac99525dcb4a23e.jpg)

<details>
<summary>line</summary>

| 时间/s | 层间位移角 |
| --- | --- |
| 0 | 0 |
| ~4 | ~-0.45 |
| ~6 | ~0.25 |
| ~8 | ~0.25 |
| ~10 | ~0.15 |
| ~12 | ~0.40 |
| ~14 | ~-0.45 |
| ~16 | ~0.20 |
| ~18 | ~-0.30 |
| ~20 | ~-0.15 |
| ~22 | ~-0.15 |
| ~24 | ~-0.10 |
| ~26 | ~-0.10 |
| ~28 | ~-0.10 |
| ~30 | ~-0.10 |
| ~32 | ~-0.10 |
| ~34 | ~-0.10 |
| ~36 | ~-0.10 |
| ~38 | ~-0.10 |
| 40 | ~-0.10 |
</details>

(b) Mohr-Coulomb 本构模型  
图 6.3-25 结构底层层间位移角时程曲线

# 6.4 土层液化对分析结果的影响

GFE 支持考虑土层液化的 Davidenkov 本构模型，对上节 E3 地震非线性时程分析中的 Davidenkov 模型考虑中间土层的液化，分析中间土层液化对最终分析结果的影响。液化的土层位于结构周围，如图 6.4-1 所示。土层的液化参数为 $\gamma_{tv}=0.001$ ，m=0.345，n=6.689，a3=0.45，c1=1.051，c3=1.25。

![](../assets/GFE-SSA/d72c6b421adda5bf554f5780e6b080f28e0b04abd397daac5a754715d1e1740e.jpg)

<details>
<summary>natural_image</summary>

3D diagram of a rectangular object with a horizontal stripe and XYZ axis indicators (no text or symbols)
</details>

图 6.4-1 土层液化区域

# 6.4.1 层间位移角

考虑土层液化后的层间位移角结果对比如图 6.4-2 所示。

![](../assets/GFE-SSA/bfef5bead951afbb23cda9bf5e1e219b0d9a7925e9990aa80201a553bd4a73c1.jpg)

<details>
<summary>line</summary>

| 层数 | Davidenkov本构模型 (cm) | Davidenkov液化模型 (cm) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1/500 | 1/125 |
| 2 | 1/500 | 1/100 |
</details>

图 6.4-2 液化层间位移角对比

# 6.4.2 孔压比

孔压比是考察土层液化程度的关键物理量, 针对考虑液化的土层, 分别选取四个时刻的孔压比云图（图 6.4-3），可知土层在 5s 内基本已经全部液化。

![](../assets/GFE-SSA/4c629bdbbce7df7bfbfd52ee0bc665501c30e3c510868b51c5a308c413e0fabb.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 7.85E-01 |
| Orange-Red | 7.20E-01 |
| Orange | 6.54E-01 |
| Yellow-Orange | 5.89E-01 |
| Yellow | 5.23E-01 |
| Light Green | 4.58E-01 |
| Green | 3.93E-01 |
| Teal | 3.27E-01 |
| Cyan | 2.62E-01 |
| Light Blue | 1.96E-01 |
| Blue | 1.31E-01 |
| Dark Blue | 6.54E-02 |
| Deep Blue | 0.00E+00 |
</details>

(a) t=3.5s  
![](../assets/GFE-SSA/7b7ede016d83f0e99d77fe4231450dfb7fe643885732fe7bcbd133b6c92f8c98.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 1.00E+00 |
| Orange-Red | 9.17E-01 |
| Orange | 8.33E-01 |
| Yellow-Orange | 7.50E-01 |
| Yellow | 6.67E-01 |
| Yellow-Green | 5.83E-01 |
| Green | 5.00E-01 |
| Light Green | 4.17E-01 |
| Cyan | 3.33E-01 |
| Light Blue | 2.50E-01 |
| Blue | 1.67E-01 |
| Dark Blue | 8.33E-02 |
| Deep Blue | 0.00E+00 |
</details>

(b) t=4.0s

![](../assets/GFE-SSA/580cde06ff0d5dbf51cdd95d7008238e8cbd75b224ef0e4e8f9197cecfd0dacd.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 1.00E+00 |
| Orange-Red | 9.17E-01 |
| Orange | 8.33E-01 |
| Yellow-Orange | 7.50E-01 |
| Yellow | 6.67E-01 |
| Light Green | 5.83E-01 |
| Green | 5.00E-01 |
| Teal | 4.17E-01 |
| Cyan | 3.33E-01 |
| Light Blue | 2.50E-01 |
| Blue | 1.67E-01 |
| Dark Blue | 8.33E-02 |
| Deep Blue | 0.00E+00 |
</details>

(c) t=4.5s

![](../assets/GFE-SSA/b660855260cae4a3c5dc1e011ee9531e112801e0e2f1af8b7a2f0ca5231a069b.jpg)

<details>
<summary>heatmap</summary>

| Color Range | SDV Value |
| --- | --- |
| Red | 1.00E+00 |
| Orange-Red | 9.17E-01 |
| Orange | 8.33E-01 |
| Yellow-Orange | 7.50E-01 |
| Yellow | 6.67E-01 |
| Light Green | 5.83E-01 |
| Green | 5.00E-01 |
| Teal | 4.17E-01 |
| Cyan | 3.33E-01 |
| Light Blue | 2.50E-01 |
| Blue | 1.67E-01 |
| Dark Blue | 8.33E-02 |
| Deep Blue | 0.00E+00 |
</details>

(d) t=5.0s  
图 6.4-3 土层孔压比云图

分别选取土体 2786473、2954156、2721123 和 3153159 号单元的作出孔压比曲线，单元提取位置如图 6.4-4 所示，孔压比曲线如图 6.4-5 所示，可见土层约从 3.5s 开始液化，在 5\~7s 后孔压比达到 1 已完全液化。

![](../assets/GFE-SSA/b23f41eecbaed2a504d68dbdf66c4e303720fd46f08be5571f3e8b60effc2867.jpg)  
图 6.4-3 单元提取位置

![](../assets/GFE-SSA/02cd0b4317460b335511854b93a51f42a3766dafc16071af0f422a0d6a354437.jpg)

<details>
<summary>line</summary>

| 时间/s | 孔压比 |
| --- | --- |
| 0 | 0 |
| ~4 | 0 |
| ~4 | ~0.88 |
| ~6 | ~0.88 |
| ~6 | 1 |
| 40 | 1 |
</details>

(a)E2786473 单元

![](../assets/GFE-SSA/8680181a3c7eb0d97b1898a37ef5b8e0907ed043efef261c0cc6807215b8d5e8.jpg)

<details>
<summary>line</summary>

| 时间/s | 孔压比 |
| --- | --- |
| 0 | 0 |
| ~3 | 0 |
| ~3.5 | ~0.16 |
| ~4 | ~0.47 |
| ~6 | ~0.47 |
| ~6.5 | ~0.61 |
| ~7 | 1.0 |
| 40 | 1.0 |
</details>

(b)E2954156 单元

![](../assets/GFE-SSA/db48781029cba54c1c010f9e8995ed555b6cdf477ba4528cafe50f2fa9ba8f42.jpg)

<details>
<summary>line</summary>

| 时间/s | 孔压比 |
| --- | --- |
| 0 | 0 |
| ~4 | 0 |
| ~4.5 | ~0.75 |
| ~5 | 1 |
| 40 | 1 |
</details>

(c)E2721123 单元

![](../assets/GFE-SSA/3a946d4d2654b726bdf29fcdae968de453dccc14eb232c422d3e29e82b53141c.jpg)

<details>
<summary>line</summary>

| 时间/s | 孔压比 |
| --- | --- |
| 0 | 0 |
| ~4 | 0 |
| ~4.5 | ~0.85 |
| ~5 | ~0.85 |
| ~6 | 1 |
| 40 | 1 |
</details>

(d)E3153159 单元  
图 6.4-5 孔压比时程曲线

# 第7章 结论

GFE 软件研发团队已通过多个地下结构抗震分析案例对 GFE 软件进行了测试，均表明 GFE 软件“准、快、简”的三大特色和优势。限于篇幅，本手册仅给出一个地铁车站地下结构抗震分析测试案例。开展了 E2 地震作用下线弹性分析，分别采用了二维和三维时程分析方法、二维反应加速度法和二维反应位移法；开展了 E3 地震下非线性分析，土体分别采用 Davidenkov 和 Mohr-Coulomb 本构模型进行了二维和三维时程分析。表 7-1 给出地下结构最大层间位移角结果，表 7-2 给出 E2 地震作用下三维时程分析计算用时，其中软件 A 为某国际先进通用有限元软件计算结果和用时。上述测试结果表明了 GFE 软件具有如下特色与优势。

# 一、GFE 软件计算 “准”。

1. 对比 GFE 软件与软件 A 计算得到的 E2 地震下结构最大层间位移角，反应位移法、反应加速度法、二维和三维时程分析方法的差异率分别为 0.13%、0.19%、1.52% 和 1.15%，表明 GFE 软件具有国际主流通用有限元软件的计算准确度。手册中结构内力、结构损伤等结果具有同样结论。  
2. GFE 软件支持 E3 地震作用下二维和三维非线性时程分析，计算结果符合认知，满足现行地下结构抗震设计规范对分析方法的要求。非线性分析结果也表明，结构产生的塑性损伤不容忽视，个别部位的混凝土和钢筋发生了较明显的非线性变形。  
3. 结构最大层间位移角结果均未超过现行地下结构抗震设计规范要求的限值，该结构满足抗震设计要求。对比 E2 地震下各类方法计算的结构最大层间位移角表明，二维和三维时程分析的差异率仅为 0.80%、反应加速度法和反应位移法相对于时程分析的误差分别为 7.36% 和 7.72%，符合一般认识。

# 二、GFE 软件计算 “快”。

E2 地震作用下三维时程分析计算用时表明，GFE 软件采用 2080 双卡 GPU 用时 263 分钟，软件 A 采用 16 核 CPU 并行计算用时 2778 分钟，GFE 软件计算用时仅为软件 A 的 1/10，速度提升 10 倍。测试 2000 万自由度模型时，计算速度可以提升 30-50 倍。

# 三、GFE 软件操作 “简”。

针对地下结构抗震分析的土-结构相互作用分析方法以及土-结构系统建模和后处理，现有通用有限元软件操作极为繁琐。GFE 软件集成了上述分析方法，并且与盈建科 YJK 软件无缝对接进行结构前后处理，整个建模、分析和后处理过程操作简单。

表 7-1 地下结构最大层间位移角

<table><tr><td rowspan="2">分析方法</td><td colspan="4">E2 地震线弹性分析</td><td colspan="4">E3 地震非线性分析</td></tr><tr><td>反应位移法</td><td>反应加速度法</td><td>二维时程方法</td><td>三维时程方法</td><td>二维 DD</td><td>二维 MC</td><td>三维 DD</td><td>三维 MC</td></tr><tr><td>GFE</td><td>1/1214</td><td>1/1044</td><td>1/1118</td><td>1/1127</td><td>1/456</td><td>1/599</td><td>1/502</td><td>1/532</td></tr><tr><td>软件 A</td><td>1/1213</td><td>1/1042</td><td>1/1135</td><td>1/1140</td><td>-</td><td>-</td><td>-</td><td>-</td></tr></table>

表 7-2 E2 地震作用下三维时程分析计算用时

<table><tr><td rowspan="2">计算软件和硬件环境</td><td colspan="2">GFE</td><td>软件A</td></tr><tr><td>GPU(2080单卡)</td><td>GPU(2080双卡)</td><td>16核CPU并行</td></tr><tr><td>计算时间(min)</td><td>504</td><td>263</td><td>2778</td></tr></table>

# 附录一：重力荷载作用静力分析

# 附录 1.1 二维模型

# (a) 结构内力

附图 1.1-1 给出重力作用下结构的轴力云图。由图可知，GFE 软件和软件 A 计算的结构轴力吻合较好，其中 GFE 软件计算的最大轴力为 -821kN，软件 A 计算的最大轴力为 -823kN，二者的差异率仅为 0.24%。

![](../assets/GFE-SSA/ce2121f8956633401f9b68158f5063ee810c80d41a7220dc830cac6969889d47.jpg)

![](../assets/GFE-SSA/4722823c1883522ef880e06b813d8c72281e3424f28ecf28860620bdd327610c.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +1.66e2 |
| Orange | — |
| Yellow | — |
| Light Green | — |
| Green | — |
| Cyan | — |
| Blue | -8.23e2 |
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/62ec78c758a6ba6c5d4dcf7ab15152f20e76058d3ff016be5357e3add89fa384.jpg)  
(b) 软件 A 计算结果  
附图 1.1-1 结构轴力云图

附图 1.1-2 给出重力作用下结构典型部位（顶板端部、侧墙顶部、侧墙底部、底板端部）的轴力。由图可知，GFE 软件和软件 A 计算的结构轴力较为接近，差异率小于 2%。

![](../assets/GFE-SSA/49efe4ac79b0d88c5302fcbf35ea52c9c589ffd84826f8dec8bb6172c59f21f3.jpg)

<details>
<summary>bar</summary>

| Category | 软件A (kN) | GFE (kN) | 差异率 |
| --- | --- | --- | --- |
| 底板端部 | -679.5 | -685.2 | 0.83% |
| 侧墙底部 | -610.6 | -615.5 | 0.80% |
| 顶板端部 | 103.6 | 105.5 | 1.80% |
| 侧墙顶部 | -269 | -268.5 | 0.19% |
</details>

附图 1.1-2 结构轴力对比

附图 1.1-3 给出重力作用下结构弯矩云图。由图可知，GFE 软件和软件 A 计算的结构弯矩云图吻合较好，其中 GFE 软件计算的最大弯矩为 $563kN\cdot m$ ，软件 A 计算的最大弯矩为 $584kN\cdot m$ ，二者的差异率为 3.60%。

![](../assets/GFE-SSA/1626273c8a694d9fb0eeec56a3464b55530522a92b53b457ff2bc70d1e649ee2.jpg)

<details>
<summary>heatmap</summary>

| Metric | Value Range |
| --- | --- |
| (a) GFE 计算结果 | +5.84e2 ~ -5.52e2 \((kN \cdot m)\) |
| (b) 软件 A 计算结果 | -5.52e2 (kN·m) |
</details>

附图 1.1-3 结构弯矩云图

附图 1.1-4 给出重力作用下结构典型部位（侧墙顶部、侧墙底部、底板端部）的弯矩。由图可知，GFE 软件和软件 A 计算的结构弯矩较为接近，差异率小于 4%。

![](../assets/GFE-SSA/a7807e77bf8560a60e0b0a6f3c579979768fbace484b920b337816a5db4ee9ff.jpg)

<details>
<summary>bar</summary>

| Category | 软件A \((kN \cdot m)\) | GFE \((kN \cdot m)\) | 差异率 |
| --- | --- | --- | --- |
| 底板端部 | -492 | -475.2 | 3.41% |
| 侧墙底部 | 584.3 | 562.5 | 3.73% |
| 侧墙顶部 | 128.7 | 125.9 | 2.18% |
</details>

附图 1.1-4 结构弯矩对比

# (b) 结构变形

附图 1.1-5 给出重力作用下土-结构系统模型的竖向位移云图。由图可知，GFE 软件和软件 A 计算的模型的位移吻合较好，其中 GFE 软件计算的最大位移为 -0.0616m，软件 A 计算的最大位移为 -0.0616m，二者完全相同。

![](../assets/GFE-SSA/23fe676731a93495b3d33ca92d3c6ff8a1d9ed3e8ff8f47a5c81ba7b8f928252.jpg)

<details>
<summary>natural_image</summary>

Thermal or fluid simulation visualization with a central white square and gradient color scale (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/29799b8153d5f4ae60ce4ece855c06aeb37122d886904208ed4e68f01ba5a378.jpg)

<details>
<summary>natural_image</summary>

Thermal or fluid simulation visualization with a central white grid and gradient color gradient (no text or symbols)
</details>

(b) 软件 A 计算结果

![](../assets/GFE-SSA/2bab2ec37a659e626111717f21ab093f14da1589e7e50e543abe92ce9de1e2e6.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (m) |
| --- | --- |
| Red | N/A |
| Orange | N/A |
| Yellow | N/A |
| Green | N/A |
| Cyan | N/A |
| Blue | -6.16e-2 |
</details>

附图 1.1-5 土-结构系统模型的竖向位移云图

附图 1.1-6 给出重力作用下结构的竖向位移云图。由图可知，GFE 软件和软件 A 计算的结构的位移吻合较好，其中 GFE 软件计算的最大位移为 -0.0450m，软件 A 计算的最大位移为 -0.0456m，二者的差异率为 0.13%。

![](../assets/GFE-SSA/8813f2cf4c41494b44af6cc068a3af128bae0a4f97beef9e0393141bbc4dce4f.jpg)  
附图 1.1-6 结构的竖向位移云图

# 附录 1.2 三维模型

# (a) 结构内力

附图 1.3-1 给出重力作用下梁柱轴力云图。由图可知，GFE 软件和软件 A 计算的梁柱轴力吻合较好，其中 GFE 软件计算的最大轴力为 -8390kN，软件 A 计算的最大轴力为 -8400kN，二者的差异率为 0.15%。

![](../assets/GFE-SSA/01a580e2858cfecddafccfcb6b7f264e181da11742d90f2f2b0942ddcad05050.jpg)

<details>
<summary>natural_image</summary>

Pure architectural line drawing of a multi-level structure without any text, numbers, or symbols
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/3d0bbfffac1bf671e4a67b4771865714963804e9b81463e4188a8d4c494b40a2.jpg)

<details>
<summary>natural_image</summary>

Diagram showing parallel colored lines with vertical bars and a 3D coordinate system (X, Y, Z) at the bottom left, no text or symbols present.
</details>

(b) 软件 A 计算结果

![](../assets/GFE-SSA/108c4dfe0c400c14380a4ea6e7dad003483fdcd1dff3fe47ddeff46fbe44b2b1.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +5.05e2 |
| Orange | — |
| Yellow | — |
| Green | — |
| Cyan | — |
| Blue | -8.40e3 |
</details>

附图 1.3-1 梁柱轴力云图

附图 1.3-2 给出重力作用下梁柱剪力云图。由图可知，GFE 软件和软件 A 计算的梁柱剪力吻合较好，其中 GFE 软件计算的最大剪力为 2500kN，软件 A 计算的最大剪力为 2540kN，二者的差异率为 1.69%。

![](../assets/GFE-SSA/cb31e6252f088e9231f32e27c52975e01d7973885ee921fb1ef19533d4f2266e.jpg)

<details>
<summary>natural_image</summary>

Pure architectural line drawing of a multi-story building with green and yellow structural elements (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/d615dff1deaa793620309072bde9e96356b234cb9c46b49f47d040f52a6713f3.jpg)

<details>
<summary>natural_image</summary>

3D wireframe diagram of a structural beam with coordinate axes (X, Y, Z) shown in the corner, no text or symbols present.
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/0feca33b1c05b0672931fa235eb1eeb7d293e336fb0a79ccce0d459dca7fff20.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +2.54e3 |
| Orange | ~2.5e3 |
| Yellow | ~2.0e3 |
| Green | ~1.5e3 |
| Cyan | ~1.0e3 |
| Blue | -2.54e3 |
</details>

附图 1.3-2 梁柱剪力云图

附图 1.3-3 给出重力作用下梁柱 1 方向弯矩云图。由图可知，GFE 软件和软件 A 计算的梁柱弯矩吻合较好，其中 GFE 软件计算的最大弯矩为 -2270kN·m，软件 A 计算的最大弯矩为 -2360kN·m，二者的差异率为 3.40%。

![](../assets/GFE-SSA/42851654acc5c1b1d2b3401059765f40b39a611c154744d5d9d56be125fbebbf.jpg)

<details>
<summary>natural_image</summary>

Pure architectural line drawing of a multi-level structure with vertical supports and horizontal beams (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/dc8d6da15495b3137a3663ba5ea6e86ec5bb1e697726c0b988d021e00f14e27b.jpg)

<details>
<summary>natural_image</summary>

3D diagram of a layered structure with green and blue lines, labeled X, Y, Z axes (no text or symbols on the diagram itself)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/21afcb9e18fd4dbe743a14692de604290baf2eb1832dba4ebc8f5c3535af289b.jpg)

<details>
<summary>heatmap</summary>

| Color | Value \((kN \cdot m)\) |
| --- | --- |
| Red | +2.19e3 |
| Orange | +2.19e3 |
| Yellow | +2.19e3 |
| Light Green | +2.19e3 |
| Green | +2.19e3 |
| Cyan | +2.19e3 |
| Blue | -2.36e3 |
</details>

附图 1.3-3 梁柱 1 方向弯矩云图

附图 1.3-4 给出重力作用下梁柱 2 方向弯矩云图。由图可知，GFE 软件和软件 A 计算的梁柱弯矩吻合较好，其中 GFE 软件计算的最大弯矩为 -228kN·m，软件 A 计算的最大弯矩为 -227kN·m，二者的差异率为 0.44%。

![](../assets/GFE-SSA/2d97ba55a6d935fe81e003af6001ad54fab9e013d92d4d077f7f937cd946a044.jpg)

<details>
<summary>natural_image</summary>

Green grid pattern with horizontal and vertical lines, no text or symbols present
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/90e752ee6e20a1f5f9085780a4998e4ef1a65ec3599050c6fd44f9456d81a093.jpg)

<details>
<summary>natural_image</summary>

3D coordinate system diagram with X, Z axes and a grid pattern (no text or labels)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/eb6efab1f809919eb0ef04d6a66dc88c8e4440d655d475ca41f29ff2ae71fd10.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range \((kN \cdot m)\) |
| --- | --- |
| Red | +2.24e2 |
| Orange | +2.24e2 |
| Yellow | +2.24e2 |
| Green | +2.24e2 |
| Cyan | +2.24e2 |
| Blue | -2.28e2 |
</details>

附图 1.3-4 梁柱 2 方向弯矩云图

附图 1.3-5 给出重力作用下楼板 1 方向轴力云图。由图可知，GFE 软件和软件 A 计算的

楼板轴力吻合较好,其中 GFE 软件计算的最大轴力为-717kN,软件 A 计算的最大轴力为-691kN,二者的差异率为 3.76%。

![](../assets/GFE-SSA/e15380fc28c7a86c1231ab6378149eef034771a6187a7360d8a57e99806e92c2.jpg)

<details>
<summary>natural_image</summary>

Color-coded thermal or density distribution visualization on a rectangular object (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/dd2c3bbeada7a0bc6c58061803e300c6d02842746a1c7b1978596adbeb867af0.jpg)

<details>
<summary>natural_image</summary>

3D simulation visualization of a layered structure with color-coded stress or deformation zones (no text or symbols)
</details>

(b) 软件 A 计算结果

![](../assets/GFE-SSA/540049ba6ab1fd03b7644ba024ccba5c67c942cf301a83d056ee9ea5da3dfe7a.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +3.63e2 |
| Orange | ~3.5e2 |
| Yellow | ~3.2e2 |
| Green | ~2.9e2 |
| Cyan | ~2.6e2 |
| Blue | -7.17e2 |
</details>

附图 1.3-5 楼板 1 方向轴力云图

附图 1.3-6 给出重力作用下楼板 2 方向轴力云图。由图可知，GFE 软件和软件 A 计算的楼板轴力吻合较好，其中 GFE 软件计算的最大轴力为 -1070kN，软件 A 计算的最大轴力为 -960kN，二者的差异率为 11.46%。

![](../assets/GFE-SSA/3f749f34e30f9eb72dcd74a29380cda31a55ae514055e1e120e3b49c942595bd.jpg)

<details>
<summary>natural_image</summary>

Color-coded 3D rectangular block with orange, green, and blue regions, no text or symbols visible
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/cc78ed616e7361836174be2567a61c887e25e52909eb4afb97ecaae7b39dce64.jpg)

<details>
<summary>natural_image</summary>

3D schematic of a layered structure with color-coded regions and XYZ axis indicators (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/cd01a22dc2db1de009c24e78e260379cbf57fad742613628facee90bbacdd792.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | N/A |
| Orange | N/A |
| Yellow | N/A |
| Green | N/A |
| Cyan | N/A |
| Blue | N/A |
| Dark Blue | N/A |
</details>

附图 1.3-6 楼板 2 方向轴力云图

附图 1.3-7 给出重力作用下楼板 1 方向弯矩云图。由图可知，GFE 软件和软件 A 计算的楼板弯矩吻合较好，其中 GFE 软件计算的最大弯矩为 $450kN\cdot m$ ，软件 A 计算的最大弯矩为 $441kN\cdot m$ ，二者的差异率为 2.04%。

![](../assets/GFE-SSA/b401532afbda0121de06e157cc19a67efaffa76d513207c1d24769af54ee90c4.jpg)

<details>
<summary>natural_image</summary>

Green rectangular object with red dots and yellow markings, no visible text or symbols
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/ade267e6d3b9a1acd1d40e9c8c9229402ab2a04f529f3afa575c0b977da90956.jpg)

<details>
<summary>natural_image</summary>

3D diagram of a layered structure with color-coded elements and XYZ axis indicators (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/937ef18f27f539a490f2a2b9a22edbc616d721bd51c7069bff99f07be69ffbd9.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | N/A |
| Orange | N/A |
| Yellow | N/A |
| Green | N/A |
| Cyan | N/A |
| Blue | -4.50e2 |
</details>

附图 1.3-7 楼板 1 方向弯矩云图

附图 1.3-8 给出重力作用下楼板 2 方向弯矩云图。由图可知，GFE 软件和软件 A 计算的楼板弯矩吻合较好，其中 GFE 软件计算的最大弯矩为 -544kN·m，软件 A 计算的最大弯矩为 -529kN·m，二者的差异率为 2.84%。

![](../assets/GFE-SSA/6cd2f915bb39db15d913f34e05f4edbf265f0a66a436ff1e5f46323cd1dbbefe.jpg)

<details>
<summary>natural_image</summary>

3D rendered diagram of a layered structure with horizontal green bands and scattered orange/red dots (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/8b5fc16579ded8deb30c47d1fe76a4493db331593fa3b29530c26a943a1c10b1.jpg)

<details>
<summary>natural_image</summary>

3D diagram of layered green structure with red and blue nodes, labeled X, Y, Z axes (no text or symbols beyond axis labels)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/730a5182121efa7d4ab4f7757f0938a4d8171929beb40e05f9fd014afda562e2.jpg)

<details>
<summary>heatmap</summary>

| Color | Value Range \((kN \cdot m)\) |
| --- | --- |
| Red | +4.87e2 |
| Orange | +4.87e2 |
| Yellow | +4.87e2 |
| Light Green | +4.87e2 |
| Green | +4.87e2 |
| Cyan | +4.87e2 |
| Blue | -5.44e2 |
</details>

附图 1.3-8 楼板 2 方向弯矩云图

附图 1.3-9 给出重力作用下侧墙轴力云图。由图可知，GFE 软件和软件 A 计算的侧墙轴力吻合较好，其中 GFE 软件计算的最大轴力为 -839kN，软件 A 计算的最大轴力为 -797kN，二者的差异率为 5.27%。

![](../assets/GFE-SSA/e98130814beb602c87e063e8b6e8988df9f511bc09e72ea6196ccb590e742e28.jpg)

<details>
<summary>natural_image</summary>

3D rendered yellow rectangular prism with a black horizontal line, no text or symbols present
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/6ac1352f623786da47e0db3ce52c4a9616a44c0fe3fa8d9b4a1dd7c17754c24b.jpg)

<details>
<summary>natural_image</summary>

3D rendered rectangular beam with color gradient and XYZ coordinate axes (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/0f152a75b056d996367e8abf0887ff433f43a0b9ced0a230072140579d503385.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +2.37e3 |
| Orange | +2.37e3 |
| Yellow | +2.37e3 |
| Light Green | +2.37e3 |
| Green | +2.37e3 |
| Cyan | +2.37e3 |
| Blue | -8.39e2 |
</details>

附图 1.3-9 侧墙轴力云图

附图 1.3-10 给出重力作用下侧墙剪力云图。由图可知，GFE 软件和软件 A 计算的侧墙剪力吻合较好，其中 GFE 软件计算的最大剪力为 -984kN，软件 A 计算的最大剪力为 -1030kN，二者的差异率为 4.39%。

![](../assets/GFE-SSA/455a59aeddcd6e98c6948ab42949cd76b83fea6da7e7078635e89ddf03ae1319.jpg)

<details>
<summary>natural_image</summary>

Green rectangular object with horizontal line and small blue markings, no visible text or symbols
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/75f63989c46aa46dc7cd4039458d8d9f8303867b7bc42b70c8fc6e3c1fa88980.jpg)

<details>
<summary>natural_image</summary>

3D rendered rectangular prism with color gradient and XYZ axis indicators (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/e0b183d8c447b293d65321292e903e5d969f5ccf42af44a766f54d56b984d525.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (kN) |
| --- | --- |
| Red | +1.70e2 |
| Orange | ~1.5e2 |
| Yellow | ~1.2e2 |
| Green | ~1.0e2 |
| Cyan | ~8.0e1 |
| Blue | -1.03e3 |
</details>

附图 1.3-10 侧墙剪力云图

附图 1.3-11 给出重力作用下侧墙 1 方向弯矩云图。由图可知，GFE 软件和软件 A 计算的侧墙弯矩吻合较好，其中 GFE 软件计算的最大弯矩为 -450kN·m，软件 A 计算的最大弯矩为 -434kN·m，二者的差异率为 3.69%。

![](../assets/GFE-SSA/e4f870d97e1aa919cfb90f4c46e14c6572637961ab5e998e6a300cc2ab4fc8f6.jpg)

(a) GFE 计算结果  
![](../assets/GFE-SSA/1ec6b3ce1fa7309652132811143ad3f2e7944087285b5c50d5c8b16209957e40.jpg)

<details>
<summary>natural_image</summary>

3D diagram of a green rectangular prism with XYZ coordinate axes labeled (no text or symbols beyond axis labels)
</details>

(b) 软件 A 计算结果

![](../assets/GFE-SSA/533651d500fba7741486578103a1df4b17136c8b821aadbe0036357a40b25cd1.jpg)

<details>
<summary>heatmap</summary>

| Color | Value \((kN \cdot m)\) |
| --- | --- |
| Red | +4.67e2 |
| Orange | ~4.50e2 |
| Yellow | ~4.40e2 |
| Green | ~4.30e2 |
| Cyan | ~4.20e2 |
| Blue | -4.50e2 |
</details>

附图 1.3-11 侧墙 1 方向弯矩云图

附图 1.3-12 给出重力作用下侧墙 2 方向弯矩云图。由图可知，GFE 软件和软件 A 计算的侧墙弯矩吻合较好，其中 GFE 软件计算的最大弯矩为 -517kN·m，软件 A 计算的最大弯矩为 -507kN·m，二者的差异率为 1.97%。

![](../assets/GFE-SSA/9729d3590a552f21a0bf8aa3e7ebe20e7eda8fd81936a77b9ff875dfc87e9e5e.jpg)

<details>
<summary>natural_image</summary>

3D rendered rectangular object with a horizontal line, no text or symbols visible
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/3b7744941d9b3cbaf6577f89a97bd06e172b323d9b068320729f3945b530b73b.jpg)

<details>
<summary>natural_image</summary>

3D rendered rectangular beam with color gradient and XYZ coordinate axes (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/ca4042daa653298fdb6503e6656df240b8809bded6de6bff3833640b9efef38b.jpg)

<details>
<summary>heatmap</summary>

| Color | Value \((kN \cdot m)\) |
| --- | --- |
| Red | +4.72e2 |
| Orange | N/A |
| Yellow | N/A |
| Green | N/A |
| Cyan | N/A |
| Blue | -5.17e2 |
</details>

附图 1.3-12 侧墙 2 方向弯矩云图

# (a) 结构变形

附图 1.2-13 给出重力作用下结构的竖向位移云图。由图可知，GFE 软件和软件 A 计算的结构竖向位移吻合较好，其中 GFE 软件计算的最大位移为 -0.0485m，软件 A 计算的最大位移为 -0.0487m，二者的差异率为 0.41%。

![](../assets/GFE-SSA/05e3142bc6852884cfa1dafcd2acd43d5d361644ed8d142a4d5fe09a561c3fc9.jpg)

<details>
<summary>natural_image</summary>

3D rendered rectangular object with a gradient color gradient from blue to green (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/4617ba8d3203c0afd23e3b0b0e4a28f473f91460a356774b6d9d51cd8b1ecf23.jpg)

<details>
<summary>natural_image</summary>

3D rendered model of a rectangular beam with color gradient and XYZ coordinate axes (no text or symbols)
</details>

(b) 软件 A 计算结果  
![](../assets/GFE-SSA/6b4842cb33e3c68c6e467cc4efed05275d17ff2d06935fb6fa2dbe1829e55de5.jpg)

<details>
<summary>heatmap</summary>

| Color | Value (m) |
| --- | --- |
| Red | -3.40e-2 |
| Orange | -3.40e-2 |
| Yellow | -3.40e-2 |
| Green | -3.40e-2 |
| Cyan | -3.40e-2 |
| Blue | -4.87e-2 |
</details>

附图 1.2-13 结构竖向位移（放大 500 倍）

附图 1.2-14 给出附图 1.2-13 结构中间断面的竖向位移云图。由图可知，GFE 软件和软件 A 计算的结构竖向位移吻合较好，其中 GFE 软件计算的最大位移为 -0.0485m，软件 A 计算的最大位移为 -0.0487m，二者的差异率为 0.41%。

![](../assets/GFE-SSA/fe0c3919f883c6ed83daa14812c318f60c5f9f05fa4c53d0601c2985ddb201a9.jpg)

<details>
<summary>heatmap</summary>

| Metric | Value (m) |
| --- | --- |
| (a) GFE 计算结果 | -3.40e-2 |
| (b) 软件 A 计算结果 | -4.87e-2 |
</details>

附图 1.2-14 结构竖向位移

# 附录二：模态分析

# 附录 2.1 二维模型

# (a) 固有频率

附表 2.2-1 给出模型前 10 阶固有频率。由表可知，GFE 软件和软件 A 计算的模型固有频率差异率小于 0.05%。

附表 2.1-1 固有频率

<table><tr><td rowspan="2">阶数</td><td colspan="3">固有频率(Hz)</td></tr><tr><td>软件A</td><td>GFE</td><td>差异率(%)</td></tr><tr><td>1</td><td>1.2420</td><td>1.24204</td><td>0.00</td></tr><tr><td>2</td><td>1.5861</td><td>1.58615</td><td>0.00</td></tr><tr><td>3</td><td>2.1963</td><td>2.19644</td><td>0.01</td></tr><tr><td>4</td><td>2.2397</td><td>2.23978</td><td>0.00</td></tr><tr><td>5</td><td>2.2515</td><td>2.25166</td><td>0.01</td></tr><tr><td>6</td><td>2.4156</td><td>2.41606</td><td>0.02</td></tr><tr><td>7</td><td>2.4672</td><td>2.46773</td><td>0.02</td></tr><tr><td>8</td><td>2.9053</td><td>2.90588</td><td>0.02</td></tr><tr><td>9</td><td>2.9437</td><td>2.94481</td><td>0.04</td></tr><tr><td>10</td><td>3.1357</td><td>3.13589</td><td>0.01</td></tr></table>

# (b) 振型

附图 2.1-1\~图 2.1-6 给出模型的前三阶振型。由图可知，GFE 软件和软件 A 计算的模型前三阶振型基本一致。

![](../assets/GFE-SSA/49ead898eadff83a7deef4afb793b7d0eab09c0915c39b833b23dfecf9cbc9a0.jpg)

<details>
<summary>natural_image</summary>

Color gradient diagram of a layered structure with a white grid overlay (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/2b7452689c07cc1ca8a6afa2b4be62bfd7bb87a1e4e7a508371f21214571fd71.jpg)

<details>
<summary>natural_image</summary>

Color gradient contour plot showing layered structure with a white rectangular feature on the right side (no text or symbols)
</details>

(b) 软件 A 计算结果

附图 2.1-1 土-结构系统一阶振型  
![](../assets/GFE-SSA/6595eddfaf6675f6c6853bcb7a0b92486ed0a26337b94fc4848abde639905aa7.jpg)

<details>
<summary>natural_image</summary>

Color gradient visualization of a symmetrical mechanical or fluid system with no text or symbols
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/fb2a9f5884a8174d4239853c2415dd77f21cdb9700cc3a0a435066c3b7f8c3d1.jpg)

<details>
<summary>natural_image</summary>

Color gradient visualization of a symmetrical mechanical or fluid system with no text or symbols
</details>

(b) 软件 A 计算结果  
附图 2.1-2 土-结构系统二阶振型

![](../assets/GFE-SSA/f591051abc4ea8e384245025cfddcb0e7bc81d7e6a77bbf525bfe35a8a8647bf.jpg)

<details>
<summary>natural_image</summary>

Color-coded contour map of a wave-like structure with a grid overlay (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/1b4506c610626ea0af2a7868df447a04001169bde94df13dfd9310bcd7de40bf.jpg)

<details>
<summary>natural_image</summary>

Color-coded contour map of a curved surface with a grid overlay and a small window on the right (no text or symbols)
</details>

(b) 软件 A 计算结果

附图 2.1-3 土-结构系统三阶振型  
![](../assets/GFE-SSA/62bcfc0a66738f17b75add0106b70bd0d2eefc61eb690a56fb17e1ca56482dfa.jpg)

<details>
<summary>natural_image</summary>

Simple geometric diagram with a grid of colored curved lines and a horizontal line, no text or symbols present.
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/0d3075d5d1eb11f5fa091dc89323934dadf64719c9e5bb837fc41176a9b66a92.jpg)

<details>
<summary>natural_image</summary>

Simple line drawing of a 3x3 grid with curved lines and a horizontal green line (no text or symbols)
</details>

(b) 软件 A 计算结果  
附图 2.1-4 结构一阶振型

![](../assets/GFE-SSA/6496eb5a72d3877584978e1a87eb3b3c543512585d128919bfeecce0badc2cf3.jpg)

<details>
<summary>natural_image</summary>

Simple geometric grid pattern with colored lines forming a 3x3 rectangular shape (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/e77a271198c212a166308bf675e33e5b7429e81294ccefba4ff98697a40a276c.jpg)  
(b) 软件 A 计算结果  
附图 2.1-5 结构二阶振型

![](../assets/GFE-SSA/8216a03a49f335fc3421e27d6c901a695f03bd9f4ae09f276680b22b26bca092.jpg)

<details>
<summary>natural_image</summary>

Simple 3x3 grid with colored borders, no text or symbols present
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/9a58b9c8741f5a72aed807cafdf656ca624ac845bedc4395b9ab21fa000fbcb0.jpg)

<details>
<summary>natural_image</summary>

Simple 3x3 grid with colored lines, no text or symbols present
</details>

(b) 软件 A 计算结果  
附图 2.1-6 结构三阶振型

# 附录 2.2 三维模型

# (a) 固有频率

附表 2.2-1 给出模型前 10 阶固有频率。由表可知，GFE 软件和软件 A 计算所得模型固有频率接近，差异小于 0.4%。

附表 2.2-1 固有频率

<table><tr><td rowspan="2">阶数</td><td colspan="3">固有频率(Hz)</td></tr><tr><td>软件A</td><td>GFE</td><td>差异率%</td></tr><tr><td>1</td><td>1.8221</td><td>1.82834</td><td>0.34</td></tr><tr><td>2</td><td>1.8286</td><td>1.82988</td><td>0.07</td></tr><tr><td>3</td><td>1.8419</td><td>1.84350</td><td>0.09</td></tr><tr><td>4</td><td>1.8627</td><td>1.86464</td><td>0.10</td></tr><tr><td>5</td><td>1.8948</td><td>1.89916</td><td>0.23</td></tr><tr><td>6</td><td>1.9157</td><td>1.91600</td><td>0.02</td></tr><tr><td>7</td><td>1.9789</td><td>1.98147</td><td>0.13</td></tr><tr><td>8</td><td>1.9826</td><td>1.98372</td><td>0.06</td></tr><tr><td>9</td><td>2.0523</td><td>2.05354</td><td>0.06</td></tr><tr><td>10</td><td>2.0722</td><td>2.07438</td><td>0.11</td></tr></table>

# (b) 振型

附图 2.2-1\~图 2.2-6 给出模型前三阶振型。由图可知，GFE 软件和软件 A 计算的模型前三阶振型一致。

![](../assets/GFE-SSA/e5f5fd9a20e37672b9dc675a2b6685d819e8cb16ed6e81dc71ea473d16a523cd.jpg)

<details>
<summary>natural_image</summary>

3D thermal or fluid simulation visualization on a rectangular block, showing gradient from blue to red (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/e2af6a8523c421403166009d80f6d44d47a9f36912e75282caa4f0dc59eafc66.jpg)

<details>
<summary>natural_image</summary>

3D thermal or fluid simulation visualization on a rectangular block, showing gradient from blue to red (no text or symbols)
</details>

(b) 软件 A 计算结果  
附图 2.2-1 土-结构系统一阶振型

![](../assets/GFE-SSA/f97d665fc5a7a28d6bed644d4b8a505d1bbbcf84b6f1faa41606e62b0f128937.jpg)

<details>
<summary>natural_image</summary>

3D thermal or fluid simulation visualization showing a central blue vortex surrounded by gradient fields (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/fc671db877a383e14ef3b9bd9dd5a4fc3b5202ae27b8023318e92d1ce6fd81a3.jpg)

<details>
<summary>natural_image</summary>

3D thermal or fluid simulation visualization on a rectangular block, showing a central red hotspot surrounded by gradient gradients (no text or symbols)
</details>

(b) 软件 A 计算结果

附图 2.2-2 土-结构系统二阶振型  
![](../assets/GFE-SSA/67c78ace8ff5fbdc75a8ed5a9f472b9d490dc96e9d61e1dee377c8872164f70b.jpg)

<details>
<summary>natural_image</summary>

3D thermal or fluid simulation visualization with color gradient and two circular hotspots (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/696846eba30de031e7d38cd7f9eabd276452f6eb15576bac591a4f950a8a17df.jpg)

<details>
<summary>natural_image</summary>

3D thermal or fluid simulation visualization with color gradient, showing two distinct circular hotspots on a curved surface (no text or symbols)
</details>

(b) 软件 A 计算结果  
附图 2.2-3 土-结构系统三阶振型

![](../assets/GFE-SSA/4c2ac94d8aa4b4bea36914d006c2c21a58058e5f488bff2be872fa4d89d0b939.jpg)

<details>
<summary>natural_image</summary>

3D surface plot with color gradient from blue to red, no text or symbols present
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/51698143d221c1c64b85f5a5faeb63f7eb2b864ccfe1511bdde457990cf38583.jpg)

<details>
<summary>natural_image</summary>

3D surface plot of a curved object with color gradient from blue to red, no text or symbols present
</details>

(b) 软件 A 计算结果

附图 2.2-4 结构一阶振型  
![](../assets/GFE-SSA/473cad7fa9496721be4bb4940cc2de4a826e8c0896975b574b3bf5fe0b69b2f4.jpg)

<details>
<summary>natural_image</summary>

3D rendered beam with rainbow gradient from red to blue (no text or symbols)
</details>

(a) GFE 计算结果

![](../assets/GFE-SSA/924a7d37805372c54f6ad5efd0eb372f60c3c5d71c393ac93c42216b99d43023.jpg)

<details>
<summary>natural_image</summary>

3D rendered beam with rainbow gradient and no text or symbols
</details>

(b) 软件 A 计算结果

附图 2.2-5 结构二阶振型  
![](../assets/GFE-SSA/ddba85284a362f9c6750c1e5b66f08c47d2e382efcbcf7abdcf7092b999750cc.jpg)

<details>
<summary>natural_image</summary>

3D finite element model of a curved beam with color gradient indicating stress or deformation (no text or symbols)
</details>

(a) GFE 计算结果  
![](../assets/GFE-SSA/b34d85558c7750a06786cb8784620535ba3dd6c72021204985b8455ba940bb11.jpg)

<details>
<summary>natural_image</summary>

3D thermal simulation visualization of a curved beam with color gradient (no text or symbols)
</details>

(b) 软件 A 计算结果  
附图 2.2-6 结构三阶振型