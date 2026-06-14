---
源文件: D:/MinerU-Output/run_2026-06-14_005009/GFE-用户手册/vlm/GFE-用户手册.md
原手册: GFE 用户手册 v3.4.3（2026.3.30），广州颖力科技
提取范围: §1.15.3 作业管理器 + 修订记录 + 附录一~五（用户红框标注章节）
提取日期: 2026-06-14
说明: 仅红框 delta 段落；图片链接与 OCR UI 噪声已剔除，表格原样保留
---

# 1.15.3 作业管理器

# （1）创建作业

点击 Ribbon 栏中的 “作业管理器” 按钮（图 1.15.4-1），弹出作业管理器对话框（图 1.15.4-2），点击左下角“创建”，弹出“创建作业”对话框（图 1.15.4-3），进行 “作业名称”、“模型名称”、“工况”、“目录”、“计算核心” 等设置后，点击 “确定” 完成作业创建。

图 1.15.4-1 作业管理器入口

图 1.15.4-2 作业管理器

图 1.15.4-3 创建作业

# (2) 提交作业

点击作业条目，可以对其进行“编辑”、“复制”、“删除”操作，也可以进行“写出 INP 文件”、“提交”、“监控”（提交后）、“结果”（提交后）、“中断”（提交后）操作。

点击 “提交” 按钮，完成作业提交。

选择 “GFEXN” 作为求解器时，如果该作业中存在未开启几何非线性的分析步，会有弹窗提示，点击确定，将会把所有分析步的几何非线性属性打开。（使用 GFENX 时，一般推荐打开几何非线性）

# （3）导出计算文件

界面提交计算后，将自动导出 inp 和 inpx 文件。如果模型由 ydb 模型导入，还会自动导出 gjdy 文件。

由命令行提交计算，需要已形成 inp 和 inpx 文件。

# （4）移除畸形单元

作业设置--移除单元中，可以设置畸形单元的长宽比、偏斜度、长度、面积、体积等判断指标，满足条件的单元在写出 inp 时，会在 inp 文件中注释掉，即不参与后续计算。

图 1.15.4-4 移除畸形单元

# (5) 高级

写出 Vuel: 勾选后写出 inp 时会将人工边界单元写入到 inp 文件中，并将场地地震动输入生成 vload 文件。

列车载荷写入 inpx：默认勾选，列车载荷信息储存在 inpx 中；若不勾选，列车载荷信息会以节点力载荷的形式写出到 inp 中。

写出 SPH xml 文件：勾选后写出 inp 时会将 SPH 流体动力分析工况写出成 xml 求解文件。

# (6) 批处理参数说明

除作业管理器提交外，还可通过批处理方式提交。当需要提交的任务较多，或需要提交多个相似任务时，采用批处理提交方式较为方便。

批处理提交例子：PrePo.exe-daemon-dat "F:\Data\inp\c3d6.inp" -gfedir

"F:\Data\inp\c3d6" -split 2

参数说明：

<table><tr><td>参数名</td><td>是否必填</td><td>说明</td></tr><tr><td>-daemon</td><td>是</td><td>表示不启动前后处理界面</td></tr><tr><td>-dat</td><td>是</td><td>后跟 inp 文件路径</td></tr><tr><td>-gfeidr</td><td>是</td><td>后跟结果输出目录</td></tr><tr><td>-cpu</td><td>否</td><td>表示使用 GFEXC(旧版 CPU 求解器)计算,与-standard 不可同时使用;-cpu 和-standard 都不包含时,默认使用 GFEXG(显式动力求解器)计算</td></tr><tr><td>-standard</td><td>否</td><td>表示使用 GFEXN(隐式求解器)计算,与-cpu 不可同时使用;-cpu 和-standard 都不包含时,默认使用 GFEXG(显式动力求解器)计算</td></tr><tr><td>-prevdb</td><td>否</td><td>后跟前置 db 路径,常用于大震分析中静力接动力分析,实现地应力平衡,详见案例操作手册。</td></tr><tr><td>-split</td><td>否</td><td>仅用于 linux 版本程序。后跟数字,表示分区数。用于多 GPU 并行计算。</td></tr><tr><td>-scotch</td><td>否</td><td>后跟 x,y,z,xy,yz,xz 或 xyz,表示分区时的切割方向。如指定 x 表示向 x 方向切割,指定 xy 表示先向 x 方向切割、再向 y 方向切割。必须与-split 结合使用。当设置此参数且值为空时默认为 xy。</td></tr><tr><td>-minElemVol</td><td>否</td><td>后跟一个数字,体积小于该值的单元将在预处理中被移除,不参与计算。对于二维单元,此处表示的是面积,一维单元不处理。</td></tr><tr><td>-cutquad</td><td>否</td><td>后跟一个数字,表示曲率,曲率大于该值的四边形将在预处理中被拆分为两个三角形,为 0 时拆分掉所有的四边形,想完全不拆分的话可以设置一个大数。不设置此参数时曲率的默认阈值为</td></tr><tr><td></td><td></td><td>0.2。</td></tr><tr><td>-config</td><td>否</td><td>后跟 config.txt 文件路径。软件按特定优先级从多处查找 config.txt,详见 1.16.3 章末尾的*注。</td></tr><tr><td>-solvemethod</td><td>否</td><td>后跟一个数字,用于指定线性方程组求解所使用的第三方库。0:Pardiso(默认),1:Mumps,2:AMGX。</td></tr><tr><td>-nomiddlenode</td><td>否</td><td>设置此选项时通用接触表面信息中考虑二阶四面体的中间节点。该选项的名称容易误导,后续改进。</td></tr><tr><td>-range</td><td>否</td><td>后跟形如“1-13”,“200-500”,这样的数,例如:-range 200-500。表示对每个*Element,只读取下面的第 200 行到第 500 行。</td></tr><tr><td>-debug</td><td>否</td><td>输出调试文件。开发人员使用</td></tr><tr><td>-searchstep</td><td>否</td><td>已废弃。</td></tr><tr><td colspan="3">下面是一些后来新加的参数选项,习惯上不再包含前面的“-”符号,参数与其后跟的数值之间一般采用“=”接驳,如 include_inner_face=Surf-1。</td></tr><tr><td>all_exterior</td><td>否</td><td>包含此选项时,无论 inp 中是否包含通用接触,总是把通用接触外表面信息传给求解器</td></tr><tr><td>include_inner_face</td><td>否</td><td>可以后跟单元集名称,或不跟任何内容。后跟单元集时,表示只将这个单元集所有的单元面加到通用接触中,不跟单元集时,表示将所有单元面都加到通用接触中。</td></tr><tr><td>splittet2</td><td>否</td><td>后跟两个数字,例如:splittet2=45000,100。第一个数字表示弹性模量,第二个数字表示屈服应力。对于所有的二阶四面体,如果它是弹塑性材料,弹性模量小于指定值,Rate=0 时的最小屈服应力夜宵于指定值,则这个二阶四面体拆分为 4 个六面体</td></tr><tr><td>splittet2-prefea</td><td>否</td><td>后跟一个.feabin 文件的路径。结合 splittet2 参数使用。使用指定的 feabin 文件中的通用接触信息。在使用 splittet2 拆分了二阶四面体后,希望通用接触仍用拆分前的单元面信息时有用。</td></tr><tr><td>tmp-soils</td><td>否</td><td>纯渗流分析计算模式。详见案例操作手册</td></tr><tr><td>test-exchange</td><td>否</td><td>验证 DataExchange 模块读写是否匹配。开发人员使用。</td></tr><tr><td>case-insensitive</td><td>否</td><td>解析 inp 时忽略大小写</td></tr><tr><td>inps</td><td>否</td><td>重启动计算时必填,用于指定 inps 文件的路径</td></tr><tr><td>py-script</td><td>否</td><td>后跟一个 python 脚本路径,用于不打开界面执行 GFE 命令流。一般不跟其他命令行选项结合使用</td></tr><tr><td>check-level</td><td>否</td><td>可以设置为 “None”,“Warning”,“Error”三种,None 表示忽略数检,Warning 表示碰到警告则中止预处理,Error 表示碰到错误中止,默认 Error</td></tr><tr><td>case-insensitive</td><td>否</td><td>打开后解析 inp 时忽略大小写,后处理打开后看到的各类名称也全都会转成大写</td></tr><tr><td>hdf5</td><td>否</td><td>打开后场输出各帧结果存到 FieldOutput 文件夹内的 h5 文件中(每帧一个)。需要边计算边查看结果时打开</td></tr><tr><td>coup-temp-penalty</td><td>否</td><td>后跟一个正实数,用于手动指定热固耦合分析中绑定约束里采用的罚系数。默认根据单元导热系数自动计算,该值跟导热系数正相关,跟单元尺寸负相关</td></tr><tr><td>splitsc</td><td>否</td><td>开启后将复合材料的厚壳单元,根据其截面属性,拆分为多层实体单元</td></tr><tr><td colspan="3">下面的选项主要是 XM 项目用到</td></tr><tr><td>intersect</td><td>否</td><td>XM 项目功能,用于生成指定单元集与厚壳拆分单元集的交集,指定单元集在 inps 文件中定义。该参数必须与参数 splitsc 和 inps 一起使用,否则无效。另外,会根据指定集合名称自动补充截面点输出,指定的积分点和输出分量会根据集合名称自动定义</td></tr><tr><td>fix-dt</td><td>否</td><td>XM项目功能,多分析步计算时开启此选项,会取所有分析步中最大的计算步长,作为所有分析步统一的计算步长</td></tr><tr><td>mergestep</td><td>否</td><td>XM项目功能,用于转换多分析步时,合并单个inp内的多个分析步为一个。</td></tr><tr><td>include-mat</td><td>否</td><td>XM项目功能,用于转换多分析步时,不读取*include输入文件具体信息,而是保留*include的格式。其中输入名称为include.inp的项被忽略。</td></tr><tr><td>fake-material</td><td>否</td><td>XM项目功能,用于在db内写入虚假材料信息,避免重要信息泄露。</td></tr></table>

\*注：电脑上包含多个 GPU 时，批处理文件中需要指定用于计算的 GPU ID。方法：在批处理文件第一行加上 CUDA\_VISIBLE\_DEVICES=0,1,2,3，其中 0,1,2,3 为需要用于 GPU 计算的 GPU ID 号。

# (7) 重启动计算说明

仅支持批处理提交，示例：

PrePo.exe -daemon inps="F:\Data\inp\multi-steps.inps" -gfedir
"F:\Data\inp\multi-steps"

其中 inps 文件是一个文本文件，每行指定一个 inp 文件的路径，从上到下的顺序执行，使用相对路径的时候是相对 inps 文件所在路径。

提交后,程序会将inps中指定的多个inp文件的内容合并成一个包含多个step

的 multi-steps.inp，放在结果目录下，然后计算这个 inp。

本质上是将重启动算例转换为多分析步 inp 进行计算，因此不支持类似中间暂停，然后重新启动计算的操作。

# (8) 静力转动力说明

仅支持批处理提交。

需要在 inpx 中添加以下内容:

\*Param2

STATIC\_TO\_DYNAMIC

\*End

支持多 step。

如果分析步中指定了质量缩放关键字，则计算按照质量缩放的步长，否则会按照静力分析步的初始步长进行质量缩放，如下面的示例，计算步长为 2e-5，总时长为 1，后两位分别是最小步长和最大步长，目前暂未用到。

\*Static

2e-5, 1, 1e-5, 1


修订记录

<table><tr><td>程序版本</td><td>修订日期</td><td>修改说明</td></tr><tr><td>3.4.3</td><td>2026.3.30</td><td>● 人工边界补充说明● 建议网格尺寸计算公式补充● 波速计算说明</td></tr><tr><td>3.4.2</td><td>2026.3.26</td><td>● 新增静力分析线性计算说明● 新增隐式动力分析线性计算说明● 冲击波 B31 单元说明</td></tr><tr><td>3.4.2</td><td>2026.3.26</td><td>● 更新目录</td></tr><tr><td>3.4.2</td><td>2026.3.26</td><td>● 新增 Inpx 关键字说明附录</td></tr><tr><td>3.4.2</td><td>2026.3.26</td><td>● 新增三方向刚度特殊相互作用截图● 新增特殊相互作用容差说明</td></tr><tr><td>3.4.2</td><td>2026.3.24</td><td>● 调整通用接触中设置面面接触的说明</td></tr><tr><td>3.4.2</td><td>2026.3.23</td><td>● 更新 HSS 参数</td></tr><tr><td>3.4.0</td><td>2026.3.13</td><td>● 更新命令行参数 intersect 相关说明</td></tr><tr><td>3.4.0</td><td>2026.3.11</td><td>● 补充命令行参数 py-script, check-level, case-insensitive, hdf5, coup-temp-penalty, splitsc, fix-dt 相关说明</td></tr><tr><td>3.4.0</td><td>2026.3.10</td><td>● 补充命令行参数 mergestep, include-mat, fake-material</td></tr><tr><td>3.4.0</td><td>2026.3.10</td><td>● 补充命令行参数 intersect 相关说明● 完善附录二单元输出关键字截面点相关说明</td></tr><tr><td>3.4.0</td><td>2026.3.5</td><td>● 新增附录二单元输出关键字截面点相关说明</td></tr><tr><td>3.4.0</td><td>2026.3.2</td><td>● 新增 1.5.3(4) 外框扫掠</td></tr><tr><td>3.4.0</td><td>2026.3.2</td><td>● 新增 1.13.2(11)热固耦合分析步</td></tr><tr><td>3.4.0</td><td>2026.2.28</td><td>● 新增 1.13.2(10)渗流分析步● 新增 1.11.19 车轨耦合列车荷载</td></tr><tr><td>3.4.0</td><td>2026.2.24</td><td>● 新增关于边界条件关键字(*boundary)的特殊自由度的解释</td></tr><tr><td>3.4.0</td><td>2026.2.5</td><td>●修正接触对关键字一处参数必要性说明错误</td></tr><tr><td>3.4.0</td><td>2026.2.5</td><td>●更新接触设置属性(摩擦、cohesive)说明</td></tr><tr><td>3.3.0</td><td>2026.2.4</td><td>●更新批处理参数-scotch说明</td></tr><tr><td>3.3.0</td><td>2026.1.13</td><td>●2.6.2层间剪力,补充NFORC说明</td></tr><tr><td>3.3.0</td><td>2026.1.8</td><td>●1.11边界条件与荷载,补充边界荷载传递逻辑</td></tr><tr><td>3.3.0</td><td>2026.1.7</td><td>●1.15.4作业管理器,补充(7)重启动计算说明和(8)静力转动力说明</td></tr><tr><td>3.0.4</td><td>2025.11.19</td><td>●修正空间分布一处文字错误</td></tr><tr><td>内部测试</td><td>2025.10.29</td><td>●特殊相互作用新增表格说明支持的求解器类型</td></tr><tr><td>内部测试</td><td>2025.10.17</td><td>●删除附录二Cohesive Behavior支持</td></tr><tr><td>3.0.0</td><td>2025.09</td><td>●修改边界条件内容,增加特殊相互作用部分模块,增加边界条件与荷载适用范围表●DWG导入说明●更新1.6中(4)关于线控制的说明●材料章节1.8模块增加JH-2、E-v、E-b本构说明●更新1.10.9连接器说明●1.10.10特殊相互作用增加带材料属性的通用约束说明●更新1.11.10列车荷载相应的说明●增加1.13空间分布●更新1.15.1分析步图片及(9)流体动力分析●更新1.15.4中GFEXN的说明●新增1.15.4(6)批处理参数说明●更新1.18.2中人工边界的一些说明●增加1.18.3地震场地反应的反演说明●1.18.14选波工具图片名称勘误●更新1.20流体动力的非牛顿流体的说明●新增2.2.5自定义编号●更新2.4.2切割显示的说明● 增加 2.5.4XY 数据多种 XY 数据运算说明● 增加 2.5.5 阈值过滤中(d)说明● 增加 2.9 导出● 文件格式更新(图前后空一行)● 更新附录二(2)材料,新增*User Material 中各类材料的说明● 更新附录二,新增热固耦合分析相关关键字,包括*Conductivity,*CFlux,*Coupled Temperature-Displacement● 增加通用梁截面的简单叙述● 更新通用梁截面图片以及 truss 单元截面设置说明● 新增材料适用范围表,粘弹性支持的类型更新(材料章节&amp;附录二)● 更新 1.16.3 求解器参数设置</td></tr><tr><td>2.11.5</td><td>2025.02</td><td>● 新增 1.10.8 节连接器属性● 原 1.10.8 节连接器改为 1.10.9,同时连接类型增加说明● 1.11.12 节动水压力删去基本单位限制</td></tr><tr><td>2.11.0</td><td>2024.11</td><td>● 1.11.12 节 动水压力,修正注意事项,补充参数说明</td></tr><tr><td>2.11.0</td><td>2024.11.22</td><td>● 1.1.2 节新增(7)按角度选择● 1.2.2 节新增导出 K 文件和导出 Opensees TCL 文件● 更新 1.2.2(12)导入 DWG 文件,增加参数说明● 1.6(5)扫掠法内容更新● 1.8.3 节新增热膨胀材料● 1.8.4 a.塑性本构、1.8.5 a.混凝土塑性损伤本构、1.8.5 b.一维非线性混凝土本构,新增 Johnson Cook 率效应● 1.8.6 新增 c.基床系数、d.南水本构、e.HSS 本构● 新增 1.8.7 孔隙流体● 1.10.5 冲击波作用新增镜像冲击波选项● 1.10.9 特殊相互作用新增法向只压不拉绑定约束● 新增 1.11.13~1.11.18,孔压、集中孔隙流量、表面孔隙流量、温度、体力、声压新增1.12初始条件,包括应力、速度、孔压、孔隙比、位移、岩土构造二维应力1.14.1新增(9)流体动力分析步1.14.4作业管理器新增(5)高级设置原1.14.5求解器参数设置迁移至1.15节,内容有更新新增1.15大节设置1.17.3节补充拟动力分析的一些说明更新1.17.7施工助手新增1.17.12隧道反应位移法助手新增1.17.13反应位移法助手新增1.17.14节,选波工具新增1.17.15节,非均匀土体(网格插值法)删除原1.16.2节,新增1.18大节,显示设置相关内容新增1.19节流体动力新增2.2.8节梁单元和壳单元拉伸显示2.5.3节自定义场功能重构2.5.4节新增(5)切换Log刻度2.6.5节自动生成计算书功能重构新增2.7 DualSPHysics结果显示新增2.8能量堆叠图</td></tr><tr><td>2.6.0</td><td>2024.3</td><td>1.1.2基本操作内容更新:新增多边形区域选择的鼠标操作说明新增添加、移除、转换三种新选择模式的逻辑说明新增包含、重叠两种框选准则的逻辑说明1.2节新增DWG接口1.3建立几何模型,拆分为三节:1.3草图建模1.4简单几何体建模</td></tr></table>

■ 1.5 几何变换、几何操作  
■ 新增 1.5.2（4）分割操作  
新增 1.5.3 建模操作

1.4 改为 1.6

新增线控制

1.6 改为 1.8

■ 1.8.4 新增蠕变塑性模型

1.8 改为 1.10

■ 1.10.4 多点约束改为 1.10.4 约束、耦合  
新增 1.10.9 特殊相互作用

1.9 改为 1.11

■ 1.11.11 列车荷载内容更新

1.11. 改为 1.13.

■ 1.13.1 新增多种分析类型  
■ 1.13.3 工况--新增生死单元

1.12 改为 1.14

■ 1.14.1「布尔显示」改为「过滤器」。Ribbon 更新  
■ 1.14.3 搜索接触。新增可设置接触类型  
■ 1.14.7 复制网格。UI 更新  
■ 1.14.8 新增工况预览

1.13 改为 1.15

■ 1.15.3 地震场地反应，新增调幅功能说明  
■ 1.15.5 新增隧道设计器  
■ 1.15.6 新增自动生成集合  
■ 1.15.7 新增施工阶段助手

\- 新增 2.2.7 显示梁、壳单元局部坐标系

● 2.5.4 节 XY 数据第（3）小节，新增部分函数

2.5.6 节自动生成计算书重写

新增 2.5.7 节构件性能评价

<table><tr><td></td><td></td><td>附录二(2)新增 Creep,更新超弹、泡棉部分说明(4)Dload 新增 P 标识(5)新增 cohesive 相关关键字(6)新增多种分析步关键字</td></tr><tr><td>1.5.0</td><td>2023.8</td><td>新增 1.9.13 节 动水压力更新 1.2.2(5)YJK 接口截图新增 1.8.8 节 连接器新增 1.13.7 节 消能子结构转换新增 1.14 大节 显示相关,新增 1.14.1 节 颜色设置附录一新增 chklog 文件说明附录二(8)新增 connector 关键字</td></tr><tr><td>1.0.0</td><td>2023.5</td><td>新增 K、Mec、IFC 接口1.4 节网格剖分,重写1.6.3、1.6.6,超弹材料更新,Davidenkov 材料更新1.9.11 列车荷载新增动轮轨力1.9 节边界荷载,新增速度、加速度边界条件1.11.4 节,作业管理器部分新增“移除畸形单元”2.3.4 节,动画,新增缩放/谐波模式2.4.1 节,过滤器,新增按 YJK 构件过滤2.5.1 节,拾取,新增拾取选项2.6.1、2.6.2 节,层间位移角、层间剪力内容重写2.6.4 节,配筋模块,新增轴压比云图、dwg 文件</td></tr><tr><td>0.48.0</td><td>2022.9</td><td>第一次正式发布</td></tr></table>

# 附录一 GFE 的文件系统

GFE 软件前后处理过程中涉及如下文件:

# （1）后缀为 pre 的前处理文件

当用户保存当前模型后，会产生 pre 文件，其中包含了模型几何形状、材料特性、荷载条件、边界条件、网格划分等一系列数据。

# （2）后缀为 stp/step 的几何信息文件

CAD 软件产生的包含了模型几何形状数据的文件，可直接导入 GFE 软件中并生模型。

# (3) 含 dtlmodel.ydb 和 dtlCalc.ydb 的 YJK 模型目录

盈建科软件产生的模型目录，可直接导入 GFE 软件中并生成结构模型，相应的包含几何形状和材料特性等一系列数据。

# （4）后缀为 gmat 的材料信息文件

由 GFE 软件导出的二进制文件，记录材料信息，可直接导入 GFE 软件。导入后会在当前模型的材料下添加 gmat 中记录的材料信息，若存在材料重名，新增材料会自动添加后缀。

# (5) 后缀为 inp 的任务文件

GFE 软件的计算输入文件，又称任务文件，其格式与国际上常用的有限元模型文件 Nastran Inp 相同，可以用文本编辑工具打开。它包含了有限元网格、材料、截面属性、荷载、分析步等计算所需的必要信息。可以由 GFE 软件生成，也可以由用户按照规定格式直接编写。

# (6) 后缀为 inpx 的任务文件

Inp 文件的补充文件, GFE 软件生成 inp 文件时一并生成, 旨在补充一些 GFE 软件中特有而 Nastran Inp 中不支持的功能, 如构件偏心、地震载荷、人工边界、工况、空间分布函数、包络输出等。

# (7) 后缀为 feasta 的监控信息文件

求解状态文件，记录着作业管理器中“监控”输出的信息。可在此文件查中

看求解器在计算各阶段的求解状态，如求解进度、计算耗时、计算中止信息等。
当求解报错时，可在此文件中查看报错原因。

# （8）后缀为 db 的后处理文件

结果数据文件，可在 GFE 软件后处理中打开进行可视化结果查看。

# (9) 后缀为 gjdy 的文件

YJK 模型写 inp 时随同写出的文件，记录了模型的平移旋转信息和几何构件对应的单元信息。

# (10) 后缀为 chklog 的文件

提交计算后，预处理阶段会在结果目录中生成的数据检查文件。

# 附录二 GFE 支持的 INP 关键字

本章列出 GFE 中支持的 INP 关键字类型，旨在阐明 GFE 当前版本对 INP 文件格式的支持范围，对其功能仅作出简单解释，详见 Abaqus Keyword Reference（下称 A）

# （1）有限元网格

\*Node

功能描述：节点

\*Element

功能描述：单元

必要参数：

type: 单元类型

可选参数：

elset: 见 A

\*Nset

功能描述：节点集

必要参数：

nset: 名称

可选参数：

generate: 见 A

\*Elset

功能描述：单元集

# 必要参数：

elset: 名称

# 可选参数:

generate: 见 A

\*Surface

功能描述：表面集

# 必要参数:

name: 名称

# 可选参数:

type（缺省时=element）：表面集的元素类型，比如单元面（element）、节点（node），详见 A。目前仅支持 element

# (2) 材料

\*Material

描述：材料

必要参数:

name: 名称

必要子关键字：\*Density

必要子关键字（互斥）：\*Elastic、\*Elastic+\*Plastic、\*Elastic+\*Mohr Coulomb、

\*Elastic+\*Concrete Damage Plasticity、\*HyperElastic

可选子关键字：\*Damping

\*Acoustic medium

描述：声学介质

层级：归属于其上方最近的\*Material

可选参数:

BULK MODULUS（默认值）

数据行:

BULK MODULUS: 屈服模量、温度

\*Density

描述：密度。与其他类型的本构参数组合使用，不可单独使用

层级：归属于其上方最近的\*Material

数据行：仅支持均匀密度

\*Damping

描述：阻尼。与其他类型的本构参数组合使用，不可单独使用

层级：归属于其上方最近的\*Material

可选参数：

alpha: alpha 阻尼

beta: beta 阻尼

\*Elastic

描述：弹性参数

层级：归属于其上方最近的\*Material

必要同级关键字：\*Density

可选参数:

type（缺省时=isotropic）：见 A。支持 isotropic、lamina（仅显式动力分析）

moduli（缺省时=long term）：见 A

数据行:

istropic: 单行输入。杨氏模量、泊松比

lamina: 单行输入。E1, E2, v12, G12, G13, G23, 共 6 个数

\*Plastic

描述：塑性参数

层级：归属于其上方最近的\*Material

可选参数:

hardening（缺省时=isotropic）：见 A。支持 Isotropic、Johnson Cook

rate: 考虑率效应。

必要同级关键字：\*Density、\*Elastic

数据行:

isotropic: 多行输入。每行分别是屈服应力，塑性应变

johnson cook: 单行输入。A, B, n, m, 共 4 个数

\*Shear Failure（求解器暂时未接）

描述：剪切失效。材料中定义了塑性参数而未定义剪切失效时，剪切失效参数默

认为1E9，1E9

层级：归属于其上方最近的\*Plastic

数据行：仅支持 TABULAR；仅支持前两位

\*Rate Dependent

描述：见 A

可选参数:

type: 见 A。仅支持 Johnson Cook

层级：归属于其上方最近的\*Plastic

数据行：单行。两个公式参数

\*Mohr Coulomb

描述：摩尔库伦

层级：归属于其上方最近的\*Material

数据行：仅支持前两位

必要同级关键字：\*Elastic

\*Mohr Coulomb Hardening

描述：见 A

层级：归属于其上方最近的\*Mohr Coulomb

数据行：仅支持前两位

\*Concrete Damage Plasticity

功描述：混凝土塑性

层级：归属于其上方最近的\*Material

数据行：单行输入。5个公式参数，其中第4位参数目前没实际用到

必要同级关键字: \*Density、\*Elastic、\*Concrete Compression Hardening、\*Concrete Compression Damage、\*Concrete Tension Stiffening、\*Concrete Tension Damage

\*注：GFE 的混凝土塑性损伤本构支持 Johnson Cook 类型的率效应，需要在前处理界面上设置，关键字会在 INPX 文件中生成

\*Concrete Compression Hardening

描述：混凝土压缩硬化

层级：归属于其上方最近的\*Material

数据行：多行输入。每行 2 个参数：屈服应力，非弹性应变

必要同级关键字：\*Density、\*Elastic、\*Concrete Damage Plasticity、\*Concrete

Compression Damage、\*Concrete Tension Stiffening、\*Concrete Tension Damage

\*Concrete Compression Damage

描述：混凝土压缩损伤

可选参数:

tension recovery: 拉损伤刚度恢复。默认值为 0。有效范围[0,1]

层级：归属于其上方最近的\*Material

数据行：多行输入。每行 2 个参数：压缩损伤，非弹性应变

必要同级关键字：\*Density、\*Elastic、\*Concrete Damage Plasticity、\*Concrete

Compression Hardening、\*Concrete Tension Stiffening、\*Concrete Tension Damage

\*Concrete Tension Stiffening

描述：混凝土拉伸刚度

层级：归属于其上方最近的\*Material

数据行：多行输入。每行 2 个参数：屈服应力，开裂应变

必要同级关键字：\*Elastic、\*Concrete Damage Plasticity、\*Concrete Compression

Hardening、\*Concrete Compression Damage、\*Concrete Tension Damage

\*Concrete Tension Damage

描述：混凝土拉伸损伤

层级：归属于其上方最近的\*Material

可选参数:

compression recovery: 压缩刚度恢复。默认值为 1。有效范围[0,1]。

数据行：多行输入。每行 2 个参数：拉伸损伤，非弹性应变

必要同级关键字：\*Density、\*Elastic、\*Concrete Damage Plasticity、\*Concrete

Compression Hardening、\*Concrete Compression Damage、\*Concrete Tension Stiffening

\*Creep

描述：蠕变

层级：归属于其上方最近的\*Material

支持的参数:

law=strain, time=creep

数据行：只读取了前三个数

\*HyperElastic

描述：超弹本构

层级：归属于其上方最近的\*Material

必要同级关键字：\*Density

可选参数：

test data input: 指定试验数据时需要包含该选项

必要参数-计算模型（互斥）：marlow、mooney-rivlin、ogden、yeoh、polynomial、reduced polynomial、arruda-boyce、neo hooke、van der waals

# Marlow:

1. 必须包含 poisson 选项  
2. 必须包含 test data。目前只支持 Uniaxial 和 Planar

# Mooney-Rivlin:

1. 可以设置 test data，也可以直接输入公式参数  
2. test data 的类型目前只支持 Uniaxial。设置了 test data 时必须包含 poisson 选项  
3. 输入公式参数时固定是 3 个数，N 选项无效

# Odgen:

1. 不支持 test data  
2. poisson 选项不起作用  
3. 支持 N=1 到 6，公式参数个数是 N\*3，每行最多 8 个数

# Polynomial:

1. 可以设置 test data，也可以直接输入公式参数  
2. test data 的类型目前只支持 Uniaxial。设置了 test data 时必须包含 poisson 选项和 N 选项，N 只能是 1 或者 2  
3. 输入公式参数时，N 可以是 1 到 6，公式参数个数是 N\*(N+5)/2，每行最多 8 个数

# Reduced Polynomail:

1. 可以设置 test data，也可以直接输入公式参数  
2. 4 种 test data 的类型都支持。设置了 test data 时必须包含 N 选项，可以是 1 到 6  
3. 输入公式参数是，N 可以是 1 到 6，公式参数个数是 N\*2，每行最多 8 个数
其余四种（Yeoh、Arruda-Boyce、Neo Hooke、Van Der Waals）：

1. 不支持 test data; poisson 选项无效；公式参数固定，N 选项无效

2. 公式参数个数:

(1) Yeoh: 6 个  
(2) Arruda-Boyce: 3 个  
(3) Neo Hooke: 2 个  
(4) Van Der Waals: 5 个

# \*Uniaxial Test Data

描述：见 A

层级：归属于其上方最近的\*HyperElastic 或\*HyperFoam

数据行：多行输入。每行两个数

\*注：另外三种，\*Biaxial Test Data、\*Planar Test Data、\*Volumetric Test Data，跟
\*Uniaxial Test Data 数据格式一样

# \*HyperFoam

描述：泡棉材料

层级：归属于其上方最近的\*Material

# 可选参数:

moduli（缺省时=long term）：见 A

N（缺省时=1）：有效范围1到6

poisson: 使用 test data 时必须给出

test data input: 指定试验数据时需要包含该选项

# 数据行:

1. 公式参数。个数等于 N\*3。  
2. 使用 test data，则不需要输入公式参数。目前只支持 Uniaxial

\*ViscoElastic

描述：粘弹性参数

层级：归属于其上方最近的\*Elastic、\*HyperElastic 或\*HyperFoam

# 必要参数：

time: 仅支持 prony

frequency: 仅隐式计算支持 tabular。

# 数据行:

time: 支持多行，每行 3 个参数。

frequency: 支持多行，每行 5 个参数，其中第 3、4 个参数目前未使用，可随意填写。

\*User Material

功描述：GFE 内置自定义材料

层级：归属于其上方最近的\*Material

# 必要参数：

constants: 与数据行参数个数保持一致即可

# 数据行:

第一位为标识位：

0: 保留、

1: 一维非线性混凝土本构

2: Davidenkov 本构、液化 Davidenkov 本构（岩土类）  
3: HSS 本构（岩土类）  
4: 南水本构（岩土类）  
5: 考虑屈曲的钢筋滞回本构  
6: JH-2 本构（陶瓷材料）  
7: E-v 本构（邓肯-张模型）  
8: E-B 本构（邓肯-张改进模型）

公式参数（第二位开始）：

表 7 UserMaterial 本构参数表

<table><tr><td>本构名称</td><td>参数个数</td><td>说明(按 Inp 中的先后顺序)</td></tr><tr><td>一维非线性混凝土</td><td>7</td><td>抗压强度,峰值压缩应变,压缩软化系数,抗拉强度,峰值拉伸应变,拉伸软化系数*注:支持 Johnson Cook 率效应,设置方法跟混凝土塑性损伤本构类似。</td></tr><tr><td>Davidenkov</td><td>6</td><td>杨氏模量,泊松比,A,B,gamma0,tao_max</td></tr><tr><td>液化Davidenkov</td><td>12</td><td>前6个参数同 Davidenkov gamma_tv,m,n,a3,c1,c3</td></tr><tr><td>HSS</td><td>7</td><td>γ0.7:当割线剪切模量衰减到70%GO时对应的剪应变m:剪切模量随σ3上升的幂指数GO,ref:小应变初始参考剪切模量Eur,ref:参考围压下的再加载模量pref:参考围压vur:泊松比σref:截止应力(为了避免当σ3趋近于0时出现零刚度)*注:控制HSS塑性部分用的是MC模型,所以该本构前面必须得有MC本构(*Mohr Coulomb)!</td></tr><tr><td>南水</td><td>11</td><td>C:粘聚力 $\phi$ :内摩擦角 $\Delta\phi$ :是围压 $\sigma3$ 增加一个数量级时峰值摩擦角降低的度数Rf:破坏比K:初始弹性模量系数Kur:卸载回弹模量系数n:弹性模量随 $\sigma3$ 提高的拟合幂次Cd: $\sigma3$ 等于一个标准大气压时的最大收缩体应变nd:收缩体应变随 $\sigma3$ 增加而增加的幂指数Rd:一发生最大收缩时的( $\sigma1-\sigma3$ )与偏应力的渐进值( $\sigma1-\sigma3$ )ult之比pa:标准大气压</td></tr><tr><td>考虑屈曲的钢筋滞回模型</td><td>5</td><td>Es:初始刚度fy:屈服强度Esh/ES:硬化刚度/初始刚度LDR:长细比 $\alpha$ : $\alpha$ 取值在0.75—1.0之间,相关文献建议对于线性硬化的取1.0,而理想弹塑性取0.75。塑性的取0.75</td></tr><tr><td>JH-2</td><td>23</td><td> $\rho0$ :初始密度G:剪切模量A:模型参数N:模型参数B:模型参数M:模型参数C:模型参数edot0:模型参数T:模型参数sigIMax:模型参数sigFMax: 模型参数HEL: 休格尼特弹性极限PHEL: 弹性极限下的压力beta: 模型参数D1: 损伤常数D2: 损伤压力指数efMax: 最大破坏应变efMin: 最小破坏应变FS: 模型参数IDamage: 损伤模式标识K1: 线性状态方程常数K2: 二次状态方程常数K3: 三次状态方程常数</td></tr><tr><td>E-v</td><td>10</td><td>c: 粘聚力 $\phi 0$ : 内摩擦角(角度) $\Delta \phi$ : 非线性摩擦角考虑围压影响的参数,易破碎就高一点10度左右(角度)Rf: 模型参数K: 模型参数n: 模型参数Kur: 模型参数G: 模型参数F: 模型参数D: 模型参数</td></tr><tr><td>E-B</td><td>8</td><td>c: 粘聚力 $\phi 0$ : 内摩擦角(角度) $\Delta \phi$ : 非线性摩擦角考虑围压影响的参数,易破碎就高一点10度左右(角度)Rf: 模型参数K: 模型参数n: 模型参数Kb: 模型参数m: 模型参数</td></tr></table>

# \*Expansion

描述：热膨胀系数。

数据行：单行输入。一个数。

# \*Porous Bulk Moduli

描述：孔隙体积模量。仅支持孔压单元+隐式计算。

数据行：单行输入。两个数，其中第二个数目前实际没用到。

# \*Permeability

描述：渗透性。仅支持孔压单元+隐式计算。

# 必选参数：

type: 目前仅支持 isotropic

specific: 间隙流体比重

数据行：单行输入。一个数。

# \*Conductivity

描述：热传导系数。需要结合热固耦合分析步使用，仅支持 C3D4，详见案例操作手册。

# 可选参数：

type: 目前仅支持 ISO。可以缺省该参数

数据行：单行输入。一个数。

# （3）截面属性

\*Beam Section

功能描述：梁截面属性

必要参数：

Elset: 单元集

Material: 材料

Section: 截面类型, 例: RECT-矩形截面、CIRC-圆形截面。详见 A

数据行：因截面类型而异。详见 A

\*Transverse Shear Stiffness

功能描述：剪切刚度

层级：归属其上方最近的\*Beam Section

数据行：详见 A

\*Shell Section

功能描述：壳截面属性

必要参数：

elset: 单元集

material: 材料

control: 见下文 “\*Section Controls”。具体含义见 A

数据行：仅支持均质截面属性

\*Membrane Section

功能描述：膜截面属性

必要参数:

elset: 单元集

material: 材料

\*Rebar Layer

功能描述：钢筋层

层级：归属其上方最近的\*Shell Section、\*Membrane Section

可选参数：orientation

数据行：详见 A

\*Solid Section

功能描述：实体截面属性

必要参数:

elset: 单元集

material: 材料

control: 见下文 “\*Section Controls”。具体含义见 A

\*Section Controls

功能描述：当前版本，用于 GFE 计算的 INP 中须加上 “\*Section Controls,

Name=ENG, Hourglass=ENHANCED”，并在所有\*Solid Section 和\*Shell Section

的 control 参数中引用这个 “ENG”，即比如 “\*Solid Section, ..., control=ENG”。

GFE 写出的 INP 会自动创建 Section Control 并引用。具体含义见 A。

必要参数：

hourglass=ENHANCED: 详见 A

# （4）边界条件与荷载

# \*Boundary

描述：边界条件。GFE 中的约束、位移、初始速度在 inp 中表示为 Boundary

层级：顶层（表示在 Initial 分析步）或归属于其上方最近的\*Step

# 可选参数:

type=veolocity: 表示速度

type=acceleration: 表示加速度

amplitude: 引用幅值函数名称。当引用了幅值函数时，边界条件数值\*幅值函数=最终数值。用于动力分析

# 数据行:

A 中描述的情况较多较复杂，这里给出 GFE 目前支持的格式，包括两种：

1. 每行四位，分别是“节点集名称或节点编号，首个被约束的自由度，最后一个被约束的自由度，边界条件数值”  
2. 每行两位，分别是“节点集名称或节点编号, ENCASTRE”。表示全约束  
3. 同 1，但是首个被约束的自由度和最后一个被约束的自由度都设为大于 6 的整数，用于表示一些特殊的荷载类型。具体各个整数表示类型如下：

8: 表示孔压或声压（根据节点所属单元类型而定）

11: 热固耦合分析步下的温度荷载。

# \*Cload

描述：集中力。GFE 前处理中创建的列车荷载，写出 inp 时也会转换为集中力荷载

层级：顶层（表示在 Initial 分析步）或归属于其上方最近的\*Step

# 可选参数:

amplitude: 引用幅值函数的名称。当引用了幅值函数时，荷载数值\*幅值函数=最终数值。用于动力分析

数据行：A 中描述的情况较多较复杂，这里给出 GFE 目前支持的格式，每行三位，分别是 “节点集名称或节点编号，自由度，荷载数值”

# \*Dload

描述：见 A。GFE 中的惯性力、线荷载在 inp 中表示为 Dload

层级：顶层（表示在 Initial 分析步）或归属于其上方最近的\*Step

# 可选参数：

amplitude: 引用幅值函数的名称。当引用了幅值函数时，荷载数值\*幅值函数=最终数值。用于动力分析

# 数据行:

A 中描述的情况较多较复杂，这里给出 GFE 目前支持的格式，包括两种：

1. 惯性力：每行六位，分别是“节点集名称或节点编号, Grav, 荷载向量的模长, 分量 1, 分量 2, 分量 3”。注意，后三位的三个分量，仅用于描述力的方向，模长（荷载数值）写在第三位。在 GFE 前处理界面中创建时会自动做归一化和计算模长的工作，不需要额外操作  
2. 线荷载：每行三位，分别是“节点集名称或节点编号, PX, 荷载数值”。其中的 PX 可换成 PY 或 PZ，表示荷载方向  
3. 第二位为 P：先计算出第一位中设置的区域的外表面，面号取 “SNEG”，在这个外表面上施加面压力。类似 Dsload，只是自动做了前面划线的那一步。  
4. 体积力，第二位为 BX、BY 或 BZ，其余与 2 相同

# \*Dsload

描述：见 A。GFE 中压力在 inp 中表示为 Dsload

层级：顶层（表示在 Initial 分析步）或归属于其上方最近的\*Step

# 可选参数：

amplitude: 引用幅值函数的名称。当引用了幅值函数时，荷载数值\*幅值函数=最终数值。用于动力分析

数据行：A 中描述的情况较多较复杂，这里给出 GFE 目前支持的格式，每行三位，分别是 “表面集名称, P, 荷载数值”

# \*Amplitude

描述：幅值函数

必要参数：name

数据行：仅支持 tarbular

\*Mass

描述：节点质量

必要参数：

elset: 质量施加区域，引用单元集名称。该区域的单元类型必须为 Mass。

必要同级关键字：\*Element, type=Mass, elset=单元集名称。每个 Mass 单元包含单元号，以及 1 个节点

数据行：见 A。仅支持各向同性

\*Nonstructural Mass

描述：非结构性质量（均布质量）。

必要参数:

elset: 质量施加区域，引用单元集名称

units: 支持 mass per length（线质量）和 mass per area（面质量）

\*Temperature

描述：温度荷载。仅适用于包含热膨胀系数的材料

可选参数:

amplitude: 幅值函数

数据行：支持多行输入。每行：节点编号或节点集名称，温度数值

\*CFlow:

描述：集中孔隙流量。仅适用于孔压单元+隐式计算

必要参数&数据行：与\*Cload 相同

\*DsFlow

描述：表面孔隙流量。仅适用于孔压单元+隐式计算

必要参数&数据行：与\*Dsload 相同

\*Initial Conditions

描述：初始条件

层级：最外层。不能放在 step 内部。

# 必要参数:

type=stress: 初始应力（仅适用于平面应变单元）

type=velocity: 初始速度

type=pore pressure: 初始孔压（仅适用于孔压单元+隐式计算）

type=ratio: 初始孔隙比（仅适用于孔压单元+隐式计算）

# 数据行:

type=stress: 第一位是单元编号或单元集名称，后续六位是各自由度的初始应求数值，从左到右分别对应 11, 22, 33, 12, 23, 13，其中带 3 的目前不起实际作用

type=velocity: 第一位是节点编号或节点集名称，后续三位分别是 1, 2, 3 自由度的数值

type=pore pressure、type=ratio:

# 有两种情况：

1. 节点编号或节点集名称，数值。表示均匀分布  
2. 节点编号或节点集名称，数值 1，坐标 1，数值 2，坐标 2。表示线性分布，详见 1.12.3 中线性分布的描述

\*CFlux

描述：集中热流量。需要结合热固耦合分析步使用，仅支持 C3D4，详见案例操作手册。

层级：归属于其上方最近的\*Step

数据行：跟 Cload 类似，每行三位，分别是 “节点集名称或节点编号，自由度，荷载数值”

# (5) 相互作用

\*Tie

描述：绑定约束

必要参数：name

可选参数:

position tolerance（缺省时=0）：见 A

cyclic symmetry: 见 A

\*Rigid Body

描述：刚体约束。从属区域必须为刚性单元（R3D3 或 R3D4）

必要参数：ref node、density

必要参数（互斥）：elset、analytical surface

数据行：必须填上厚度（非0值）

\*Embedded Element

描述：嵌入区域

必要参数：host elset

数据行：仅支持填写单元集名称

\*MPC

描述：多点约束

数据行：仅支持 BEAM 和 TIE 两类

\*Contact

描述：通用接触

层级：目前只能位于顶层，后续可能支持置于\*Step 内

必要参数：op=new

\*Contact Inclusions

描述：通用接触的区域

层级：目前只能紧邻\*Contact，位于其下一行

可选参数：all exterior （目前必须使用 all exterior 定义全部的外表面，若要指定两个特定的面，请使用\*Contact Pair）

数据行：需要定义接触的两个表面集。若定义了 all exterior 参数，数据行中的定义无效

\*Contact Property Assignment

描述：接触属性

层级：归属于其上方最近的\*Contact

# 数据行:

1. 对于 cohesive: 前两位是设置接触的两个表面集, 第三位是 Surface Interaction 的名称。即只有 Surface Interaction 中包含 cohesive 参数时, 前两位的区域信息才会被考虑到, 为这个区域设置上 cohesive 属性  
2. 其他情况：仅第三位有效。无视前两位的数据，区域都是通用接触区域

\*Contact Pair

描述：面面接触

必要参数：

interaction: 接触属性。引用\*Surface Interaction 的名称

可选参数:

cpset: 名称

数据行：见 A

\*Surface Interaction

描述：接触属性

必要参数：name

```txt
*Cohesive Behavior
```

功能描述：接触属性

层级：归属于其上方最近的\*Surface Interaction

目前支持的参数设置：

```txt
type=uncoupled
```

数据行：仅读取了前三位

```txt
*Damage Evolution
```

描述：接触属性

层级：归属于其上方最近的\*Surface Interaction

目前支持的参数设置：

```txt
type=energy, softening=linear, mixed mode behavior=power law
```

可选参数:

power: 默认为 2

数据行：仅读取了前三位

```txt
*Damage Initiation
```

描述：接触属性

层级：归属于其上方最近的\*Surface Interaction

目前支持的参数设置:

```gitattributes
criterion=quads
```

数据行：仅读取了前三位

```txt
*Friction
```

描述：摩擦属性

层级：目前只能紧邻\*Surface Interaction，位于其下一行

数据行：仅支持一位，表示摩擦系数

```txt
*Cohesive Behavior
```

功能描述：见 A。测试功能，待完善。UI 上不支持

层级：紧邻\*Surface Interaction

\*Incident Wave Interaction

描述：冲击波

必要参数:

conwep: 见 A

property: 引用\*Incident Wave Interaction Property 的名称

数据行：仅支持 conwep 的情况

\*Incident Wave Interaction Property

描述：冲击波属性

必要参数:

name: 名称

type: 仅支持 air blast 和 surface blast

\*Conwep Charge Property

描述：见 A

层级：归属于其上方最近的\*Incident Wave Interaction Property

\*Spring

描述：弹簧

必要参数：

elset: 弹簧施加区域, 引用单元集名称。该区域的单元类型必须为 Spring1、Spring2 或 SpringA

必要同级关键字：\*Element, type=Spring1/Spring2/SpringA, elset=单元集名称。每个弹簧单元包含单元号，以及1（接地弹簧）或2个节点（两点弹簧）

数据行：支持 Spring1（接地弹簧），Spring2（固定方向的两点弹簧），SpringA（沿两点连线方向的两点弹簧）。仅支持输入自由度、刚度

\*Dashpot

描述：阻尼

必要参数：

elset: 阻尼施加区域,引用单元集名称。该区域的单元类型必须为 Dashpot1、Dashpot2 或 DashpotA

必要同级关键字：\*Element, type=Dashpot1/Dashpot2/DashpotA, elset=单元集名称。每个阻尼单元包含单元号，以及1（接地阻尼）或2个节点（两点阻尼）

数据行: 支持 Dashpot1（接地阻尼）, Dashpot2（固定方向的两点阻尼）, DashpotA（沿两点连线方向的两点阻尼）。仅支持输入自由度、阻尼系数

\*Connector Section

描述：连接器单元截面属性

必要参数：

elset: 截面属性所赋予的单元集

可选参数:

behavior: 连接器行为

必要同级关键字：\*Element, type=CONN3d2, elset=单元集名称。每个连接器单元包含单元号以及2个节点

数据行:

第 1 行：目前仅支持 Catersian、Join、Rotation、Align 四种连接器类型，或者留空。

第 2 行：目前仅支持设置第一个点的局部坐标系

\*Connector Behavior

描述：连接器行为

必要参数:

name: 名称

\*Connector Elasticity

描述：连接器弹性参数

层级：归属于其上方最近的\*Connector Behavior

必要参数：

component

可选参数:

rigid: 表示刚性约束

GFE 自定义参数:

definition=GFE ELA

数据行:

只有一行。

若 definition=GFE ELA: 抗压刚度, 抗拉刚度

否则：抗压刚度。（GFE 中，抗拉刚度=抗压刚度；A 则没有此参数）

\*Connector Plasticity

描述：连接器塑性参数

必要参数：

component

\*Connector Hardening

描述：连接器行为

层级：归属于其上方最近的\*Connector Plasticity

固定参数:

type: 目前仅支持 Kinematic。不写默认等于 Kinematic

必要参数:

definition: A 中的类型目前仅支持 Half Cycle

GFE 自定义参数:

definition=GFE HDN2

definition=GFE BW

definition=GFE PEND

# 数据行:

definition=Half Cycle: 见 A，每行仅支持前两位

definition=GFE HDN2: 一行。屈服力、刚度折减系数

definition=GFE BW: 一行。屈服力、刚度折减系数、屈服指数

definition=GFE PEND: 一行。摩擦系数变化率、屈服位移、快摩擦系数、慢摩擦系数、等效半径

\*Connector Damping

描述：连接器阻尼参数

# 固定参数:

nonlinear: 目前仅支持 nonlinear

# 必要参数：

component

type: A 中的类型目前仅支持 VISCOUS。不写默认是 VISCOUS

GFE 自定义参数:

type=GFE DAMP2

# 数据行:

type=VISCOUS: 见 A

type=GFE DAMP2: 一行。阻尼系数、阻尼指数

# (6) 分析步

\*Step

描述：分析步

必要参数：

name: 名称

nlgeom: 几何非线性开关

必要子关键字（互斥）：\*Static，\*Dyanmic, Explicit 或\*Frequency

必要同级关键字：\*End Step

\*Static

描述：静力分析

层级：归属于其上方最近的\*Step

数据行：共四位，分别是“初始迭代步长，总分析时长，最小迭代步长，最大迭代步长”。实际上目前这四个数据均未使用，但也需要填上数值，按 GFE 前处理界面的数值填上即可

\*Model Change

描述：生死单元

层级：归属于其上方最近的\*Static

支持的参数:

add: 表示激活单元。跟 remove 互斥

remove: 表示移除单元。跟 add 互斥

数据行：单元集名称。支持多行

\*Dynamic

描述：动力分析

层级：归属于其上方最近的\*Step

可选参数:

Explicit: 表示使用显式方法。没有时表示使用隐式方法

# ① 显式方法:

数据行：仅读取了第二位，表示总分析时长。对于动力分析的迭代步长，GFE与Abaqus的逻辑目前不太一样。关于GFE的步长设置，见下文的\*Variable Mass Scaling

必要同级关键字:

\*Bulk Viscosity

0.06, 1.2

该关键字 GFE 未支持，但在与 Abaqus 进行对比时需要加上。具体含义见 A

# ② 隐式方法:

数据行：仅读取了前两位，分别表示固定的计算步长、总分析时长

# \*Variable Mass Scaling

描述：质量缩放。在 GFE 当前版本中，对相应单元进行质量缩放的同时，还会将迭代步长固定为质量缩放中设置的最小步长，而 Abaqus 中实际计算中，实际步长有时会略大于质量缩放中的最小步长

# 必要参数：

dt: 对稳定步长小于 dt 的单元，进行质量缩放

# \*Frequency

描述：模态分析

层级：归属于其上方最近的\*Step

数据行：仅支持第一位。表示取的模态阶数

# \*Modal Dynamic

描述：模态动力分析（即振型叠加法）

层级：归属于其上方最近的\*Step

数据行：支持两位数据，表示时间增量和总分析时长

注意：模态动力分析的上一个分析步必须是模态分析

\*Steady State Dynamics

描述：频响分析

层级：归属于其上方最近的\*Step

# 支持的参数:

direct: 有这个标识表示直接法计算，否则表示模态法

interval: 支持所有类型

scale: 支持所有类型

数据行：根据 interval 和 scale 而定。详见 A

注意：采用模态法计算时，上一个分析步必须是模态分析

\*Response Spectrum

描述：反应谱分析

层级：归属于其上方最近的\*Step

数据行：只读取前五位数据，分别表示反应谱名称、地震动方向对 x, y, z 三轴的余弦值，地震动放缩系数

# 注意:

1. sum 参数目前没有读，在后处理的「自定义场」功能中可以对反应谱结果进行求和

2. 上一个分析步必须是模态分析

\*Spectrum

描述：反应谱。

# 支持的参数:

type: 支持 acceleration、velocity、displacement

数据行：读取三位数据，表示幅值、频率、阻尼比。支持多行

\*Modal Damping

描述：振型阻尼

层级：归属于其上方最近的\*Modal Dynamic、\*Steady State Dynamic 或者

\*Response Spectrum

# 支持的参数:

type: 仅支持 direct（阻尼比）和 rayleigh（瑞利阻尼）

definition: 仅支持 mode（第几阶模态）

field: 仅支持 mechanical

# 数据行:

1. type=direct，读取前三位数据，表示起始模态，截止模态，阻尼比  
2. type=rayleigh，读取前四位数据，表示起始模态，截止模态，alpha 阻尼，beta 阻尼

\*Global Damping

描述：全局阻尼

层级：归属于其上方最近的\*Steady State Dynamic

# 支持的参数:

filed: 仅支持 mechanical

数据行：读取前两位数据，表示 alpha 阻尼，beta 阻尼

\*Visco

描述：考虑粘弹性的静力分析

层级：归属于其上方最近的\*Step

数据行：跟\*Static 相同

\*Geostatic

描述：地应力平衡分析步

层级：归属于其上方最近的\*Step

数据行：跟\*Static 相同

\*Coupled Temperature-Displacement

描述：热固耦合分析。

层级：归属于其上方最近的\*Step

数据行：单行，四个数字，目前只用了前两位，第一位为计算步长，第二位为总时长。

说明：GFE 中目前实现的热固耦合分析与软件 A 不同，识别到该分析步关键字后，会进行一次纯热的有限元分析，算出单元温度变化时程后，将其作为温度荷载再做一次显式动力分析。这个分析步下面的计算步长仅用于纯热计算，时长则同时用于纯热计算和显式动力分析。进行此类计算时，应当用\*Mass Scaling 指定显式动力分析步的计算步长。更具体的信息可见 1.13.2

# \*Soils

描述：渗流分析步

层级：归属于其上方最近的\*Step

数据行：跟\*Static 相同

# (7) 输出请求

\*Output

功能描述：输出请求

层级：归属于其上方最近的\*Step

必要参数 1（互斥）：field、history

必要参数 2（互斥）：time interval、number interval、frequency

\*Node Output

功能描述：子输出-节点

层级：归属于其上方最近的\*Output

可选参数:

nset: 见 A。缺省时为整个模型

variable: 见 A

\*Element Output

功能描述：子输出-单元

层级：归属于其上方最近的\*Output

可选参数:

elset: 见 A。缺省时为整个模型

variable: 见 A

数据行：可以选择在第一个数据行指定输出的截面点，后续数据行格式与其他子输出一致。

# 说明：

1、截面点输出必须与 splitsc 选项结合使用，且最后得到的历史输出里只会对厚壳拆分得到的单元进行输出。若除此之外还指定了其他的单元，则其他单元会被忽略。  
2、若指定了截面点，如果当前的输出类型为场输出，且指定的场输出变量仅包含“LE”，则此单元输出将会强制转为历史输出，并且物理量强制设为“LE”；

若指定的输出变量包含 “LE” 且同时包含其他变量，则会清除对指定截面点的限制。

\*Energy Output

功能描述：子输出-能量

层级：归属于其上方最近的\*Output, history

可选参数:

elset: 见 A。缺省时为整个模型

variable: 见 A

per element set: 见 A。若包含该参数，elset 参数的值无效

\*Contact Output

功能描述：子输出-接触

层级：归属于其上方最近的\*Output

必要参数（互斥）：surface、general contact

可选参数：variable

\*Integrated Output

功能描述：子输出-统计量

层级：归属于其上方最近的\*Output, history

必要参数（互斥）：surface、elset

可选参数：variable

\*Time Points

功能描述：自定义输出时间序列

层级：最顶层，不归属于任何关键字

必要参数：name

可选参数: generate

# 数据行:

含 generate 时，每行的组成为：起始时刻，终止时刻，时间增量

不含 generate 时，列出所有要输出的时间点，每行最多 8 个数，逗号分隔

# 附录三 INPX 文件关键字

\*NameList

功能描述：定义名称列表

可选参数:

name: 该列表自身的名称

数据行：多行，每行一个名称

\*Material

功能描述：定义材料的 Johnson cook rate, concrete rate

必要参数:

name: 对应材料名称的参数

子关键字：\*Johnson cook rate、\$ConcreteRate

\*Rload

功能描述：定义频响分析动态荷载

必要参数:

name: 荷载名称

type: 荷载类型

ref: 荷载引用的静态荷载名称

\*Envelop Ouput

功能描述：定义包络输出

必要参数:

method: 输出方法

step: 输出的分析步名称

\*Custom Property

功能描述：定义特殊相互作用

必要参数:

type: 特殊相互作用类型

parameters: 特殊相互作用参数（刚度、容差等）

surfaces: 特殊相互作用的表面名称

\*Mat Test Data

功能描述：定向材料非线性曲线

必要参数:

name: 非线性曲线的材料名

\*Surface

功能描述：定义人工边界

\*Layer

功能描述：定义地震场地反应土层信息

\*Wave

功能描述：定义地震场地反应波动输入信息

\*Param

功能描述：定义人工边界和地震场地反应参数

\*Param2

功能描述：定义其他全局参数

\*TrainLoad

功能描述：定义列车荷载，与\*Train, \*Track, \*Force 同时使用

\*Train

功能描述：定义列车数据

\*Track

功能描述：定义列车轨道点

\*Force

功能描述：定义轨道点上的力

\$TrainLoad-Coupling

功能描述：定义车轨耦合列车荷载

\*WATER PRESS

功能描述：定义水压力

必要参数:

NAME: 水压力名称

SURF: 水压力作用的表面

\*Modal Damping

功能描述：定义显式动力分析模态阻尼

必要参数:

Modal db: 模态 db 路径

nset: db 内节点集名称

\*End

功能描述：结束上一个关键字，可嵌套

# 附录四 YJK 数据命名规则

工况

Dead，恒载

Live，活载

gk1，自定义工况 1

gk2，自定义工况 2

gk3，自定义工况 3

gk4，自定义工况 4

Comb，组合工况，由各个单工况乘以组合系数求和而得，组合系数同 yjk 重力荷载代表值的组合系数

荷载

LL\_BEAM，梁竖向线荷载

LL\_HORI，梁水平线荷载

LL\_COL，柱水平线荷载

P\_SLAB，板压力

P\_WALL，墙压力

FV，点集中竖向荷载

FH，点水平荷载

附加质量

M\_Point，点质量

M\_BEAM，梁质量

M\_SLAB，板质量

截面与厚度属性、截面与厚度集合的名称，均以截面与厚度标识符开头，后缀为集合的序号

举例：WallC\_Conc800\_C35\_1576、Beam\_H500x200\_Sub0\_Q355\_385

截面与厚度标识符

WallC，剪力墙

WallB，墙梁（采用壳单元模拟的连梁）

Slab，板

Beam，梁

Col，柱

Brace，斜撑

Raft，筏板

Pile，桩

厚度尺寸标识符

Conc，混凝土

St，钢板

截面形状标识符

REC，矩形

H，工字钢

D，圆

CROSS，十字形

BOX，箱形

PIPE，管形

TRAPE，梯形

CROSS\_H，十字形工字钢

CFT\_PIPE，圆钢管混凝土

REC\_H，内置工字形的矩形型钢混凝土

REC\_BOX，内置箱形的矩形型钢混凝土

REC\_CROSS，内置十字形的矩形型钢混凝土

L，L形截面

T，T形截面

REC\_BOX，内置箱形的矩形型钢混凝土

D\_H，内置工字形的圆形型钢混凝土

D\_PIPE，内置管形的圆形型钢混凝土

D\_CROSS，内置管十字形的圆形型钢混凝土

CFT\_BOX，方钢管混凝土

截面形状标识符之后为外轮廓子截面尺寸

矩形，宽 x 高

箱形，宽 x 高

圆形，直径

管形，直径 x 壁厚

工字钢，高 x 宽

T形，宽x高

子截面序号标识符，其中第0个截面为外轮廓子截面

Sub

# 附录五 参考文献


