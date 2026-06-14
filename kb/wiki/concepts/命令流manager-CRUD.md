---
title: "命令流manager-CRUD — GFE 命令流核心建模范式"
type: concept
tags: [concept, gfe, 命令流, api]
created: 2026-06-04
updated: 2026-06-04
---

> GFE 命令流（PrePo 内嵌 pybind11 API）的核心建模范式：每模块暴露一个单例管理器 `X_mgr()`；建模 = 构造对象 → 设属性 → `mgr.add(obj)`；工况则用 case 的一组 setter 把步 / 边界 / 荷载 / 生死单元挂上。

## 定义（三段式 + 工况装配）
1. **取管理器**：`amp_mgr() / bc_mgr() / sect_mgr() / tie_mgr() / soil_mgr() / step_mgr() / case_mgr()` …… 每模块一个单例。注意 soil 双命名空间：soil_mgr 在 GFE.Pre.soil，几何构建器 box_builder/data_builder 另在 GFE.soil。
2. **建对象 + 设属性**：构造对应类（如 `boundary.boundary()`、`section.property_solid()`），用 def_readwrite 属性赋值（name / type / set / value / mat_name …）。
3. **加入**：`mgr.add(obj, inner=False, auto_name=False)`；另有独立方法 `mgr.auto_name(prefix, has0=False)` 生成不冲突名。查改用 `find / name_list / contains / edit / rename`；`delete*` 标「疑似改模型，未实调用」慎用。
- **工况装配（case）**：`set_bcs / set_vload / set_artbc / set_fieldReqs / set_elemAdd / set_elemDel(步名, [名])`（v3.2.2 起为 setter 形式；旧版为映射属性形态，两态并存待仲裁）；`steps` 须显式激活。各对象引用哪种集合见 [[GFE对象引用关系]]。

## 在本库中的位置
- 文法全貌：[[GFE-命令流API规格]]；官方手册同范式：[[GFE-Cmd]]
- 真实例子：[[GFE-CmdKB-400galVC.src]]、[[GFE-命令流SSI骨架]]

相关：[[GFE对象引用关系]] · [[GFE-CmdKB]] · [[单元生死]] · [[PrePo]]
