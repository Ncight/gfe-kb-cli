# GFE 命令流 API 原始自省规格（1607 符号 + 签名）
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本。


---

## 自省符号清单
`01_API规格与文法\gfe_api_spec.txt`

# GFE 命令流 API 规格 (运行时自省 + TypeError 逼签名)
# 共 1607 条符号

[mod]   GFE.Pre
[mod]   GFE.Pre.amplitude
[class] GFE.Pre.amplitude.amp_mgr
[func]  GFE.Pre.amplitude.amp_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.amplitude.amp_mgr.add    1. (self: GFE.Pre.amplitude.manager, obj: GFE::Function, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.amplitude.manager, obj: GFE::Function, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.amplitude.amp_mgr.auto_name    1. (self: GFE.Pre.amplitude.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.amplitude.manager, arg0: GFE::Function) -> str
[func]  GFE.Pre.amplitude.amp_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.amplitude.amp_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.amplitude.amp_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.amplitude.amp_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.amplitude.amp_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.amplitude.amp_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.amplitude.amp_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.amplitude.amp_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.amplitude.amp_mgr.edit    1. (self: GFE.Pre.amplitude.manager, obj: GFE::Function) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.amplitude.manager, obj: GFE::Function) -> generic_mgr.generic.status
[enum]  GFE.Pre.amplitude.amp_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.amplitude.amp_mgr.find    1. (self: GFE.Pre.amplitude.manager, arg0: str) -> GFE::Function
[func]  GFE.Pre.amplitude.amp_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.amplitude.amp_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.amplitude.amp_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.amplitude.amp_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.amplitude.amp_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.amplitude.amp_mgr.status
[prop]  GFE.Pre.amplitude.amp_mgr.status.CODE
[prop]  GFE.Pre.amplitude.amp_mgr.status.MESSAGE
[func]  GFE.Pre.amplitude.amp_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.amplitude.amplitude
[prop]  GFE.Pre.amplitude.amplitude.gravity
[prop]  GFE.Pre.amplitude.amplitude.name
[prop]  GFE.Pre.amplitude.amplitude.spectrum_type
[prop]  GFE.Pre.amplitude.amplitude.type
[prop]  GFE.Pre.amplitude.amplitude.value
[class] GFE.Pre.amplitude.manager
[mod]   GFE.Pre.artbc
[class] GFE.Pre.artbc.art_bc
[prop]  GFE.Pre.artbc.art_bc.center
[prop]  GFE.Pre.artbc.art_bc.centered
[prop]  GFE.Pre.artbc.art_bc.name
[prop]  GFE.Pre.artbc.art_bc.structure
[prop]  GFE.Pre.artbc.art_bc.surface
[class] GFE.Pre.artbc.artbc_mgr
[func]  GFE.Pre.artbc.artbc_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.artbc.artbc_mgr.add    1. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.artbc.artbc_mgr.auto_name    1. (self: GFE.Pre.artbc.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.artbc.manager, arg0: GFE::ArtBC) -> str
[func]  GFE.Pre.artbc.artbc_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.artbc.artbc_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.artbc.artbc_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.artbc.artbc_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.artbc.artbc_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.artbc.artbc_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.artbc.artbc_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.artbc.artbc_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.artbc.artbc_mgr.edit    1. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC) -> generic_mgr.generic.status
[enum]  GFE.Pre.artbc.artbc_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.artbc.artbc_mgr.find    1. (self: GFE.Pre.artbc.manager, arg0: str) -> GFE::ArtBC
[func]  GFE.Pre.artbc.artbc_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.artbc.artbc_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.artbc.artbc_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.artbc.artbc_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.artbc.artbc_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.artbc.artbc_mgr.status
[func]  GFE.Pre.artbc.artbc_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.artbc.manager
[mod]   GFE.Pre.boundary
[class] GFE.Pre.boundary.bc_mgr
[func]  GFE.Pre.boundary.bc_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.boundary.bc_mgr.add    1. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.boundary.bc_mgr.auto_name    1. (self: GFE.Pre.boundary.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.boundary.manager, arg0: GFE::GenericBC) -> str
[func]  GFE.Pre.boundary.bc_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.boundary.bc_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.boundary.bc_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.boundary.bc_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.boundary.bc_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.boundary.bc_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.boundary.bc_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.boundary.bc_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.boundary.bc_mgr.edit    1. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC) -> generic_mgr.generic.status
[enum]  GFE.Pre.boundary.bc_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.boundary.bc_mgr.find    1. (self: GFE.Pre.boundary.manager, arg0: str) -> GFE::GenericBC
[func]  GFE.Pre.boundary.bc_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.boundary.bc_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.boundary.bc_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.boundary.bc_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.boundary.bc_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.boundary.bc_mgr.status
[func]  GFE.Pre.boundary.bc_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.boundary.boundary
[prop]  GFE.Pre.boundary.boundary.amplitude
[prop]  GFE.Pre.boundary.boundary.amplitude_im
[prop]  GFE.Pre.boundary.boundary.distribution
[prop]  GFE.Pre.boundary.boundary.has_if
[prop]  GFE.Pre.boundary.boundary.if_acce
[prop]  GFE.Pre.boundary.boundary.if_acce_path
[prop]  GFE.Pre.boundary.boundary.if_force
[prop]  GFE.Pre.boundary.boundary.if_grade
[prop]  GFE.Pre.boundary.boundary.if_itv
[prop]  GFE.Pre.boundary.boundary.if_mode
[prop]  GFE.Pre.boundary.boundary.if_param
[prop]  GFE.Pre.boundary.boundary.if_tot
[prop]  GFE.Pre.boundary.boundary.name
[prop]  GFE.Pre.boundary.boundary.set
[prop]  GFE.Pre.boundary.boundary.track_coord
[prop]  GFE.Pre.boundary.boundary.track_id
[prop]  GFE.Pre.boundary.boundary.type
[prop]  GFE.Pre.boundary.boundary.valid_dof
[prop]  GFE.Pre.boundary.boundary.value
[prop]  GFE.Pre.boundary.boundary.value_im
[class] GFE.Pre.boundary.generic_bc
[prop]  GFE.Pre.boundary.generic_bc.name
[prop]  GFE.Pre.boundary.generic_bc.type
[class] GFE.Pre.boundary.manager
[mod]   GFE.Pre.case
[class] GFE.Pre.case.case
[prop]  GFE.Pre.case.case.name
[func]  GFE.Pre.case.case.set_artbc    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_bcs    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_elemAdd    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_elemDel    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_fieldReqs    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_histReqs    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_initialConditions    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[func]  GFE.Pre.case.case.set_vload    1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
[prop]  GFE.Pre.case.case.steps
[class] GFE.Pre.case.case_mgr
[func]  GFE.Pre.case.case_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.case.case_mgr.add    1. (self: GFE.Pre.case.manager, obj: GFE::Case, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.case.manager, obj: GFE::Case, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.case.case_mgr.auto_name    1. (self: generic_mgr.generic, prefix: str, has0: bool = False) -> str
[func]  GFE.Pre.case.case_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.case.case_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.case.case_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.case.case_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.case.case_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.case.case_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.case.case_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.case.case_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.case.case_mgr.edit    1. (self: GFE.Pre.case.manager, obj: GFE::Case) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.case.manager, obj: GFE::Case) -> generic_mgr.generic.status
[enum]  GFE.Pre.case.case_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.case.case_mgr.find    1. (self: GFE.Pre.case.manager, arg0: str) -> GFE::Case
[func]  GFE.Pre.case.case_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.case.case_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.case.case_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.case.case_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.case.case_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.case.case_mgr.status
[func]  GFE.Pre.case.case_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.case.manager
[mod]   GFE.Pre.document
[class] GFE.Pre.document.application
[func]  GFE.Pre.document.current_document    () -> GFE.Pre.document.document
[class] GFE.Pre.document.document
[func]  GFE.Pre.document.get_document    1. (arg0: int) -> GFE.Pre.document.document
[func]  GFE.Pre.document.set_application    (疑似改模型, 未实调用)
[func]  GFE.Pre.document.set_application_by_ui    (疑似改模型, 未实调用)
[func]  GFE.Pre.document.set_current    (疑似改模型, 未实调用)
[mod]   GFE.Pre.field
[class] GFE.Pre.field.discrete_field
[prop]  GFE.Pre.field.discrete_field.datatype
[prop]  GFE.Pre.field.discrete_field.default
[prop]  GFE.Pre.field.discrete_field.field
[prop]  GFE.Pre.field.discrete_field.id
[prop]  GFE.Pre.field.discrete_field.name
[prop]  GFE.Pre.field.discrete_field.type
[class] GFE.Pre.field.expression_field
[prop]  GFE.Pre.field.expression_field.expression
[prop]  GFE.Pre.field.expression_field.name
[class] GFE.Pre.field.field_manager
[func]  GFE.Pre.field.field_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.field.field_manager.add    1. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.field.field_manager.auto_name    1. (self: GFE.Pre.field.field_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.field.field_manager, arg0: GFE::Pre::Field) -> str
[func]  GFE.Pre.field.field_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.field.field_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.field.field_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.field.field_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.field.field_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.field.field_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.field.field_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.field.field_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.field.field_manager.edit    1. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field) -> generic_mgr.generic.status
[enum]  GFE.Pre.field.field_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.field.field_manager.find    1. (self: GFE.Pre.field.field_manager, arg0: str) -> GFE::Pre::Field
[func]  GFE.Pre.field.field_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.field.field_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.field.field_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.field.field_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.field.field_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.field.field_manager.status
[func]  GFE.Pre.field.field_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.field.field_mgr
[mod]   GFE.Pre.geometry
[class] GFE.Pre.geometry.geo_mgr
[func]  GFE.Pre.geometry.geo_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.geometry.geo_mgr.add    1. (self: GFE.Pre.geometry.manager, arg0: str, arg1: TopoDS_Shape) -> tuple[GFE::Geometry, generic_mgr.generic.err_code]
[func]  GFE.Pre.geometry.geo_mgr.auto_name    1. (self: generic_mgr.generic, prefix: str, has0: bool = False) -> str
[func]  GFE.Pre.geometry.geo_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.geometry.geo_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.geometry.geo_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.geometry.geo_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.geometry.geo_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.geometry.geo_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.geometry.geo_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.geometry.geo_mgr.delete_all    (疑似改模型, 未实调用)
[enum]  GFE.Pre.geometry.geo_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.geometry.geo_mgr.find    1. (self: GFE.Pre.geometry.manager, arg0: str) -> GFE::Geometry ; 2. (self: GFE.Pre.geometry.manager, arg0: int) -> GFE::Geometry
[func]  GFE.Pre.geometry.geo_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.geometry.geo_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.geometry.geo_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.geometry.geo_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.geometry.geo_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.geometry.geo_mgr.status
[func]  GFE.Pre.geometry.geo_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.geometry.manager
[class] GFE.Pre.geometry.object
[func]  GFE.Pre.geometry.object.id    1. (self: GFE.Pre.geometry.object) -> int
[prop]  GFE.Pre.geometry.object.name
[func]  GFE.Pre.geometry.object.shape    1. (self: GFE.Pre.geometry.object) -> TopoDS_Shape
[mod]   GFE.Pre.initial_condition
[class] GFE.Pre.initial_condition.InitGeostaticStress
[prop]  GFE.Pre.initial_condition.InitGeostaticStress.name
[prop]  GFE.Pre.initial_condition.InitGeostaticStress.set_name
[prop]  GFE.Pre.initial_condition.InitGeostaticStress.value
[class] GFE.Pre.initial_condition.InitPorePress
[prop]  GFE.Pre.initial_condition.InitPorePress.is_constant
[prop]  GFE.Pre.initial_condition.InitPorePress.name
[prop]  GFE.Pre.initial_condition.InitPorePress.set_name
[prop]  GFE.Pre.initial_condition.InitPorePress.value
[class] GFE.Pre.initial_condition.InitRatio
[prop]  GFE.Pre.initial_condition.InitRatio.is_constant
[prop]  GFE.Pre.initial_condition.InitRatio.name
[prop]  GFE.Pre.initial_condition.InitRatio.set_name
[prop]  GFE.Pre.initial_condition.InitRatio.value
[class] GFE.Pre.initial_condition.InitSaturation
[prop]  GFE.Pre.initial_condition.InitSaturation.name
[prop]  GFE.Pre.initial_condition.InitSaturation.saturation
[prop]  GFE.Pre.initial_condition.InitSaturation.set_name
[class] GFE.Pre.initial_condition.InitStress
[prop]  GFE.Pre.initial_condition.InitStress.distribution
[prop]  GFE.Pre.initial_condition.InitStress.name
[prop]  GFE.Pre.initial_condition.InitStress.set_name
[prop]  GFE.Pre.initial_condition.InitStress.value
[class] GFE.Pre.initial_condition.InitTemperature
[prop]  GFE.Pre.initial_condition.InitTemperature.dis_field
[prop]  GFE.Pre.initial_condition.InitTemperature.name
[prop]  GFE.Pre.initial_condition.InitTemperature.set_name
[prop]  GFE.Pre.initial_condition.InitTemperature.value
[class] GFE.Pre.initial_condition.InitVelocity
[prop]  GFE.Pre.initial_condition.InitVelocity.distribution
[prop]  GFE.Pre.initial_condition.InitVelocity.name
[prop]  GFE.Pre.initial_condition.InitVelocity.set_name
[prop]  GFE.Pre.initial_condition.InitVelocity.valid_dof
[prop]  GFE.Pre.initial_condition.InitVelocity.value
[class] GFE.Pre.initial_condition.InitialCondition
[prop]  GFE.Pre.initial_condition.InitialCondition.name
[prop]  GFE.Pre.initial_condition.InitialCondition.set_name
[class] GFE.Pre.initial_condition.ic_mgr
[func]  GFE.Pre.initial_condition.ic_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.initial_condition.ic_mgr.add    1. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.initial_condition.ic_mgr.auto_name    1. (self: GFE.Pre.initial_condition.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.initial_condition.manager, arg0: GFE.Pre.initial_condition.InitialCondition) -> str
[func]  GFE.Pre.initial_condition.ic_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.initial_condition.ic_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.initial_condition.ic_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.initial_condition.ic_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.initial_condition.ic_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.initial_condition.ic_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.initial_condition.ic_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.initial_condition.ic_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.initial_condition.ic_mgr.edit    1. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition) -> generic_mgr.generic.status
[enum]  GFE.Pre.initial_condition.ic_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.initial_condition.ic_mgr.find    1. (self: GFE.Pre.initial_condition.manager, arg0: str) -> GFE.Pre.initial_condition.InitialCondition
[func]  GFE.Pre.initial_condition.ic_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.initial_condition.ic_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.initial_condition.ic_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.initial_condition.ic_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.initial_condition.ic_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.initial_condition.ic_mgr.status
[func]  GFE.Pre.initial_condition.ic_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.initial_condition.manager
[mod]   GFE.Pre.interaction
[class] GFE.Pre.interaction.conn_beh_mgr
[func]  GFE.Pre.interaction.conn_beh_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.conn_beh_mgr.add    1. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.conn_beh_mgr.auto_name    1. (self: GFE.Pre.interaction.connector_behavior_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.connector_behavior_manager, arg0: GFE.Pre.interaction.connector_behavior) -> str
[func]  GFE.Pre.interaction.conn_beh_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_beh_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_beh_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_beh_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.conn_beh_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.conn_beh_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.conn_beh_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.conn_beh_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.conn_beh_mgr.edit    1. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.conn_beh_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.conn_beh_mgr.find    1. (self: GFE.Pre.interaction.connector_behavior_manager, arg0: str) -> Optional[GFE.Pre.interaction.connector_behavior]
[func]  GFE.Pre.interaction.conn_beh_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_beh_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.conn_beh_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.conn_beh_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.conn_beh_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.conn_beh_mgr.status
[func]  GFE.Pre.interaction.conn_beh_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.conn_prop_mgr
[func]  GFE.Pre.interaction.conn_prop_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.conn_prop_mgr.add    1. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.conn_prop_mgr.auto_name    1. (self: GFE.Pre.interaction.connector_property_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.connector_property_manager, arg0: GFE.Pre.interaction.connector_section) -> str
[func]  GFE.Pre.interaction.conn_prop_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_prop_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_prop_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_prop_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.conn_prop_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.conn_prop_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.conn_prop_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.conn_prop_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.conn_prop_mgr.edit    1. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.conn_prop_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.conn_prop_mgr.find    1. (self: GFE.Pre.interaction.connector_property_manager, arg0: str) -> GFE.Pre.interaction.connector_section
[func]  GFE.Pre.interaction.conn_prop_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.conn_prop_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.conn_prop_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.conn_prop_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.conn_prop_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.conn_prop_mgr.status
[func]  GFE.Pre.interaction.conn_prop_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.connector_base
[class] GFE.Pre.interaction.connector_behavior
[prop]  GFE.Pre.interaction.connector_behavior.behaviors
[prop]  GFE.Pre.interaction.connector_behavior.name
[class] GFE.Pre.interaction.connector_behavior_manager
[class] GFE.Pre.interaction.connector_damping
[prop]  GFE.Pre.interaction.connector_damping.component
[prop]  GFE.Pre.interaction.connector_damping.type
[prop]  GFE.Pre.interaction.connector_damping.values
[class] GFE.Pre.interaction.connector_elastic
[prop]  GFE.Pre.interaction.connector_elastic.component
[prop]  GFE.Pre.interaction.connector_elastic.compressive_stiffness
[prop]  GFE.Pre.interaction.connector_elastic.rigid
[prop]  GFE.Pre.interaction.connector_elastic.tensile_stiffness
[class] GFE.Pre.interaction.connector_plastic
[prop]  GFE.Pre.interaction.connector_plastic.component
[prop]  GFE.Pre.interaction.connector_plastic.kh_define
[prop]  GFE.Pre.interaction.connector_plastic.kh_values
[class] GFE.Pre.interaction.connector_property_manager
[class] GFE.Pre.interaction.connector_section
[prop]  GFE.Pre.interaction.connector_section.behavior
[prop]  GFE.Pre.interaction.connector_section.connector_type
[prop]  GFE.Pre.interaction.connector_section.material
[prop]  GFE.Pre.interaction.connector_section.name
[prop]  GFE.Pre.interaction.connector_section.orientation
[prop]  GFE.Pre.interaction.connector_section.orientation2
[prop]  GFE.Pre.interaction.connector_section.set_name
[class] GFE.Pre.interaction.contact
[prop]  GFE.Pre.interaction.contact.damageEvolution
[prop]  GFE.Pre.interaction.contact.damageInitiation
[prop]  GFE.Pre.interaction.contact.friction
[prop]  GFE.Pre.interaction.contact.isCohesive
[prop]  GFE.Pre.interaction.contact.name
[prop]  GFE.Pre.interaction.contact.power
[prop]  GFE.Pre.interaction.contact.surface
[prop]  GFE.Pre.interaction.contact.type
[class] GFE.Pre.interaction.contact_manager
[func]  GFE.Pre.interaction.contact_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.contact_manager.add    1. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.contact_manager.auto_name    1. (self: GFE.Pre.interaction.contact_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.contact_manager, arg0: GFE.Pre.interaction.contact) -> str
[func]  GFE.Pre.interaction.contact_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.contact_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.contact_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.contact_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.contact_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.contact_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.contact_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.contact_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.contact_manager.edit    1. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.contact_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.contact_manager.find    1. (self: GFE.Pre.interaction.contact_manager, arg0: str) -> GFE.Pre.interaction.contact
[func]  GFE.Pre.interaction.contact_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.contact_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.contact_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.contact_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.contact_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.contact_manager.status
[func]  GFE.Pre.interaction.contact_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.contact_mgr
[class] GFE.Pre.interaction.embed
[prop]  GFE.Pre.interaction.embed.embedded_names
[prop]  GFE.Pre.interaction.embed.exterior_tolerance
[prop]  GFE.Pre.interaction.embed.host_name
[prop]  GFE.Pre.interaction.embed.id
[prop]  GFE.Pre.interaction.embed.name
[prop]  GFE.Pre.interaction.embed.roundoff_tolerance
[class] GFE.Pre.interaction.embed_manager
[func]  GFE.Pre.interaction.embed_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.embed_manager.add    1. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.embed_manager.auto_name    1. (self: GFE.Pre.interaction.embed_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.embed_manager, arg0: GFE::Embed) -> str
[func]  GFE.Pre.interaction.embed_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.embed_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.embed_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.embed_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.embed_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.embed_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.embed_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.embed_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.embed_manager.edit    1. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.embed_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.embed_manager.find    1. (self: GFE.Pre.interaction.embed_manager, arg0: str) -> GFE::Embed
[func]  GFE.Pre.interaction.embed_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.embed_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.embed_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.embed_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.embed_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.embed_manager.status
[func]  GFE.Pre.interaction.embed_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.embed_mgr
[class] GFE.Pre.interaction.general_section
[prop]  GFE.Pre.interaction.general_section.material
[prop]  GFE.Pre.interaction.general_section.set_name
[class] GFE.Pre.interaction.incident_wave
[prop]  GFE.Pre.interaction.incident_wave.id
[prop]  GFE.Pre.interaction.incident_wave.is_node_set
[prop]  GFE.Pre.interaction.incident_wave.mag_scale_factor
[prop]  GFE.Pre.interaction.incident_wave.name
[prop]  GFE.Pre.interaction.incident_wave.node_id
[prop]  GFE.Pre.interaction.incident_wave.prop_name
[prop]  GFE.Pre.interaction.incident_wave.set_name
[prop]  GFE.Pre.interaction.incident_wave.surf_name
[prop]  GFE.Pre.interaction.incident_wave.time_detonation
[class] GFE.Pre.interaction.incident_wave_manager
[func]  GFE.Pre.interaction.incident_wave_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.incident_wave_manager.add    1. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.incident_wave_manager.auto_name    1. (self: GFE.Pre.interaction.incident_wave_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.incident_wave_manager, arg0: GFE::IncidentWave) -> str
[func]  GFE.Pre.interaction.incident_wave_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.incident_wave_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.incident_wave_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.incident_wave_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.incident_wave_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.incident_wave_manager.edit    1. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.incident_wave_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.incident_wave_manager.find    1. (self: GFE.Pre.interaction.incident_wave_manager, arg0: str) -> GFE::IncidentWave
[func]  GFE.Pre.interaction.incident_wave_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.incident_wave_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.incident_wave_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.incident_wave_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.incident_wave_manager.status
[func]  GFE.Pre.interaction.incident_wave_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.incident_wave_property
[prop]  GFE.Pre.interaction.incident_wave_property.data
[prop]  GFE.Pre.interaction.incident_wave_property.def
[prop]  GFE.Pre.interaction.incident_wave_property.id
[prop]  GFE.Pre.interaction.incident_wave_property.name
[class] GFE.Pre.interaction.incident_wave_property_manager
[func]  GFE.Pre.interaction.incident_wave_property_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.incident_wave_property_manager.add    1. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.incident_wave_property_manager.auto_name    1. (self: GFE.Pre.interaction.incident_wave_property_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.incident_wave_property_manager, arg0: GFE::IncidentWaveProperty) -> str
[func]  GFE.Pre.interaction.incident_wave_property_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_property_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_property_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_property_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.incident_wave_property_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.incident_wave_property_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.incident_wave_property_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.incident_wave_property_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.incident_wave_property_manager.edit    1. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.incident_wave_property_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.incident_wave_property_manager.find    1. (self: GFE.Pre.interaction.incident_wave_property_manager, arg0: str) -> GFE::IncidentWaveProperty
[func]  GFE.Pre.interaction.incident_wave_property_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.incident_wave_property_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.incident_wave_property_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.incident_wave_property_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.incident_wave_property_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.incident_wave_property_manager.status
[func]  GFE.Pre.interaction.incident_wave_property_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.iw_mgr
[class] GFE.Pre.interaction.iw_prop_mgr
[class] GFE.Pre.interaction.mpc
[prop]  GFE.Pre.interaction.mpc.name
[prop]  GFE.Pre.interaction.mpc.ref_node
[prop]  GFE.Pre.interaction.mpc.set_name
[prop]  GFE.Pre.interaction.mpc.type
[class] GFE.Pre.interaction.mpc_manager
[func]  GFE.Pre.interaction.mpc_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.mpc_manager.add    1. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.mpc_manager.auto_name    1. (self: GFE.Pre.interaction.mpc_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.mpc_manager, arg0: GFE.Pre.interaction.mpc) -> str
[func]  GFE.Pre.interaction.mpc_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.mpc_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.mpc_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.mpc_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.mpc_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.mpc_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.mpc_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.mpc_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.mpc_manager.edit    1. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.mpc_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.mpc_manager.find    1. (self: GFE.Pre.interaction.mpc_manager, arg0: str) -> GFE.Pre.interaction.mpc
[func]  GFE.Pre.interaction.mpc_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.mpc_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.mpc_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.mpc_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.mpc_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.mpc_manager.status
[func]  GFE.Pre.interaction.mpc_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.mpc_mgr
[class] GFE.Pre.interaction.rigid_body
[prop]  GFE.Pre.interaction.rigid_body.density
[prop]  GFE.Pre.interaction.rigid_body.id
[prop]  GFE.Pre.interaction.rigid_body.name
[prop]  GFE.Pre.interaction.rigid_body.ref_node
[prop]  GFE.Pre.interaction.rigid_body.ref_set
[prop]  GFE.Pre.interaction.rigid_body.set_name
[prop]  GFE.Pre.interaction.rigid_body.thickness
[prop]  GFE.Pre.interaction.rigid_body.type
[class] GFE.Pre.interaction.rigid_manager
[func]  GFE.Pre.interaction.rigid_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.rigid_manager.add    1. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.rigid_manager.auto_name    1. (self: GFE.Pre.interaction.rigid_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.rigid_manager, arg0: GFE::RigidBody) -> str
[func]  GFE.Pre.interaction.rigid_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.rigid_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.rigid_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.rigid_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.rigid_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.rigid_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.rigid_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.rigid_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.rigid_manager.edit    1. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.rigid_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.rigid_manager.find    1. (self: GFE.Pre.interaction.rigid_manager, arg0: str) -> GFE::RigidBody
[func]  GFE.Pre.interaction.rigid_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.rigid_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.rigid_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.rigid_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.rigid_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.rigid_manager.status
[func]  GFE.Pre.interaction.rigid_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.rigid_mgr
[class] GFE.Pre.interaction.sd_mgr
[func]  GFE.Pre.interaction.sd_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.sd_mgr.add    1. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.sd_mgr.auto_name    1. (self: GFE.Pre.interaction.spring_dashpot_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.spring_dashpot_manager, arg0: GFE::SpringDashpot) -> str
[func]  GFE.Pre.interaction.sd_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.sd_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.sd_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.sd_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.sd_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.sd_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.sd_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.sd_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.sd_mgr.edit    1. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.sd_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.sd_mgr.find    1. (self: GFE.Pre.interaction.spring_dashpot_manager, arg0: str) -> GFE::SpringDashpot
[func]  GFE.Pre.interaction.sd_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.sd_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.sd_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.sd_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.sd_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.sd_mgr.status
[func]  GFE.Pre.interaction.sd_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.spec_mgr
[func]  GFE.Pre.interaction.spec_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.spec_mgr.add    1. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.spec_mgr.auto_name    1. (self: GFE.Pre.interaction.special_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.special_manager, arg0: GFE::SpecialInteraction) -> str
[func]  GFE.Pre.interaction.spec_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.spec_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.spec_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.spec_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.spec_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.spec_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.spec_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.spec_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.spec_mgr.edit    1. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.spec_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.spec_mgr.find    1. (self: GFE.Pre.interaction.special_manager, arg0: str) -> GFE::SpecialInteraction
[func]  GFE.Pre.interaction.spec_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.spec_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.spec_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.spec_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.spec_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.spec_mgr.status
[func]  GFE.Pre.interaction.spec_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.special_interaction
[prop]  GFE.Pre.interaction.special_interaction.name
[prop]  GFE.Pre.interaction.special_interaction.namelist
[prop]  GFE.Pre.interaction.special_interaction.parameters
[prop]  GFE.Pre.interaction.special_interaction.type
[class] GFE.Pre.interaction.special_manager
[class] GFE.Pre.interaction.spring_dashpot
[prop]  GFE.Pre.interaction.spring_dashpot.coefficient
[prop]  GFE.Pre.interaction.spring_dashpot.dof
[prop]  GFE.Pre.interaction.spring_dashpot.dof2
[prop]  GFE.Pre.interaction.spring_dashpot.id
[prop]  GFE.Pre.interaction.spring_dashpot.name
[prop]  GFE.Pre.interaction.spring_dashpot.nodes
[prop]  GFE.Pre.interaction.spring_dashpot.nset
[prop]  GFE.Pre.interaction.spring_dashpot.nset2
[prop]  GFE.Pre.interaction.spring_dashpot.orientation
[prop]  GFE.Pre.interaction.spring_dashpot.stiffness
[prop]  GFE.Pre.interaction.spring_dashpot.type
[class] GFE.Pre.interaction.spring_dashpot_manager
[class] GFE.Pre.interaction.surface_pair
[prop]  GFE.Pre.interaction.surface_pair.first_surf
[prop]  GFE.Pre.interaction.surface_pair.name
[prop]  GFE.Pre.interaction.surface_pair.param_number
[prop]  GFE.Pre.interaction.surface_pair.parameters
[prop]  GFE.Pre.interaction.surface_pair.second_surf
[prop]  GFE.Pre.interaction.surface_pair.type
[class] GFE.Pre.interaction.tie_manager
[func]  GFE.Pre.interaction.tie_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.interaction.tie_manager.add    1. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.interaction.tie_manager.auto_name    1. (self: GFE.Pre.interaction.tie_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.interaction.tie_manager, arg0: GFE::SurfacePair) -> str
[func]  GFE.Pre.interaction.tie_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.tie_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.tie_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.tie_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.tie_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.tie_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.interaction.tie_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.tie_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.interaction.tie_manager.edit    1. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair) -> generic_mgr.generic.status
[enum]  GFE.Pre.interaction.tie_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.interaction.tie_manager.find    1. (self: GFE.Pre.interaction.tie_manager, arg0: str) -> GFE::SurfacePair
[func]  GFE.Pre.interaction.tie_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.interaction.tie_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.tie_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.tie_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.interaction.tie_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.interaction.tie_manager.status
[func]  GFE.Pre.interaction.tie_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.interaction.tie_mgr
[mod]   GFE.Pre.material
[class] GFE.Pre.material.bed_coefficient
[prop]  GFE.Pre.material.bed_coefficient.kh
[prop]  GFE.Pre.material.bed_coefficient.kv
[class] GFE.Pre.material.concrete_damaged
[prop]  GFE.Pre.material.concrete_damaged.comp_damage
[prop]  GFE.Pre.material.concrete_damaged.comp_harden
[prop]  GFE.Pre.material.concrete_damaged.comp_recov
[prop]  GFE.Pre.material.concrete_damaged.has_jc_rate
[prop]  GFE.Pre.material.concrete_damaged.jc_rate_C
[prop]  GFE.Pre.material.concrete_damaged.jc_rate_Ep0_dot1
[prop]  GFE.Pre.material.concrete_damaged.n_comp_damage
[prop]  GFE.Pre.material.concrete_damaged.n_comp_harden
[prop]  GFE.Pre.material.concrete_damaged.n_plasticity
[prop]  GFE.Pre.material.concrete_damaged.n_tens_damage
[prop]  GFE.Pre.material.concrete_damaged.n_tens_stiff
[prop]  GFE.Pre.material.concrete_damaged.plasticity
[prop]  GFE.Pre.material.concrete_damaged.tens_damage
[prop]  GFE.Pre.material.concrete_damaged.tens_recov
[prop]  GFE.Pre.material.concrete_damaged.tens_stiff
[class] GFE.Pre.material.creep
[prop]  GFE.Pre.material.creep.data
[prop]  GFE.Pre.material.creep.law
[prop]  GFE.Pre.material.creep.nRow
[prop]  GFE.Pre.material.creep.time
[class] GFE.Pre.material.damping
[prop]  GFE.Pre.material.damping.n_param
[prop]  GFE.Pre.material.damping.params
[class] GFE.Pre.material.density
[prop]  GFE.Pre.material.density.n_param
[prop]  GFE.Pre.material.density.params
[prop]  GFE.Pre.material.density.temp_dp
[class] GFE.Pre.material.elastic
[prop]  GFE.Pre.material.elastic.compression
[prop]  GFE.Pre.material.elastic.moduli_time_scale
[prop]  GFE.Pre.material.elastic.n_param
[prop]  GFE.Pre.material.elastic.params
[prop]  GFE.Pre.material.elastic.temp_dp
[prop]  GFE.Pre.material.elastic.tension
[prop]  GFE.Pre.material.elastic.type
[enum]  GFE.Pre.material.entry_type  = Density, Elastic, Plastic, HyperFoam, HyperElastic, Damping, ViscoElastic, ConcreteDamaged, MohrCoulomb, User, TestData, Creep, Permeability, PorousBulkModuli, Sorption, Expansion, BedCoefficient, RateDependent
[class] GFE.Pre.material.expansion
[prop]  GFE.Pre.material.expansion.sub_type
[prop]  GFE.Pre.material.expansion.value
[class] GFE.Pre.material.hyperelastic
[prop]  GFE.Pre.material.hyperelastic.N
[prop]  GFE.Pre.material.hyperelastic.biaxial
[prop]  GFE.Pre.material.hyperelastic.has_poisson
[prop]  GFE.Pre.material.hyperelastic.he_type
[prop]  GFE.Pre.material.hyperelastic.moduli_time_scale
[prop]  GFE.Pre.material.hyperelastic.params
[prop]  GFE.Pre.material.hyperelastic.planar
[prop]  GFE.Pre.material.hyperelastic.poisson
[prop]  GFE.Pre.material.hyperelastic.temp_dp
[prop]  GFE.Pre.material.hyperelastic.test_data
[prop]  GFE.Pre.material.hyperelastic.uniaxial
[prop]  GFE.Pre.material.hyperelastic.volumetric
[class] GFE.Pre.material.hyperfoam
[prop]  GFE.Pre.material.hyperfoam.N
[prop]  GFE.Pre.material.hyperfoam.biaxial
[prop]  GFE.Pre.material.hyperfoam.moduli_time_scale
[prop]  GFE.Pre.material.hyperfoam.params
[prop]  GFE.Pre.material.hyperfoam.planar
[prop]  GFE.Pre.material.hyperfoam.simple_shear
[prop]  GFE.Pre.material.hyperfoam.temp_dp
[prop]  GFE.Pre.material.hyperfoam.test_data
[prop]  GFE.Pre.material.hyperfoam.uniaxial
[prop]  GFE.Pre.material.hyperfoam.volumetric
[class] GFE.Pre.material.manager
[func]  GFE.Pre.material.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.material.manager.add    1. (self: GFE.Pre.material.manager, obj: GFE::Material, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.material.manager, obj: GFE::Material, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.material.manager.auto_name    1. (self: GFE.Pre.material.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.material.manager, arg0: GFE::Material) -> str
[func]  GFE.Pre.material.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.material.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.material.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.material.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.material.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.material.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.material.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.material.manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.material.manager.edit    1. (self: GFE.Pre.material.manager, obj: GFE::Material) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.material.manager, obj: GFE::Material) -> generic_mgr.generic.status
[enum]  GFE.Pre.material.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.material.manager.find    1. (self: GFE.Pre.material.manager, arg0: str) -> GFE::Material
[func]  GFE.Pre.material.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.material.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.material.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.material.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.material.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.material.manager.status
[func]  GFE.Pre.material.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.material.mat_general
[class] GFE.Pre.material.mat_mgr
[class] GFE.Pre.material.mat_permeability
[prop]  GFE.Pre.material.mat_permeability.entities
[class] GFE.Pre.material.mat_sorption
[prop]  GFE.Pre.material.mat_sorption.entities
[class] GFE.Pre.material.material
[func]  GFE.Pre.material.material.as_elastic    1. (self: GFE.Pre.material.material, rou: float, e: float, nu: float) -> None
[prop]  GFE.Pre.material.material.entries
[prop]  GFE.Pre.material.material.name
[class] GFE.Pre.material.mohr_coulomb
[prop]  GFE.Pre.material.mohr_coulomb.cohesion
[prop]  GFE.Pre.material.mohr_coulomb.n_cohesion
[prop]  GFE.Pre.material.mohr_coulomb.n_plasticity
[prop]  GFE.Pre.material.mohr_coulomb.plasticity
[class] GFE.Pre.material.plastic
[prop]  GFE.Pre.material.plastic.harden_type
[prop]  GFE.Pre.material.plastic.has_jc_rate
[prop]  GFE.Pre.material.plastic.jc_rate_C
[prop]  GFE.Pre.material.plastic.jc_rate_Ep0_dot1
[prop]  GFE.Pre.material.plastic.params
[prop]  GFE.Pre.material.plastic.rate_dp
[prop]  GFE.Pre.material.plastic.temp_dp
[class] GFE.Pre.material.porous_bulk_moduli
[prop]  GFE.Pre.material.porous_bulk_moduli.permeating_fluid
[prop]  GFE.Pre.material.porous_bulk_moduli.solid_grains
[class] GFE.Pre.material.rate_dependent
[prop]  GFE.Pre.material.rate_dependent.sub_type
[prop]  GFE.Pre.material.rate_dependent.value
[class] GFE.Pre.material.test_data
[prop]  GFE.Pre.material.test_data.n_test_data
[prop]  GFE.Pre.material.test_data.test_data
[class] GFE.Pre.material.user
[prop]  GFE.Pre.material.user.constants
[prop]  GFE.Pre.material.user.n_constants
[prop]  GFE.Pre.material.user.user_type
[class] GFE.Pre.material.viscoelastic
[prop]  GFE.Pre.material.viscoelastic.n_param
[prop]  GFE.Pre.material.viscoelastic.params
[prop]  GFE.Pre.material.viscoelastic.type
[mod]   GFE.Pre.mesh
[class] GFE.Pre.mesh.element
[prop]  GFE.Pre.mesh.element.eid
[prop]  GFE.Pre.mesh.element.node_size
[prop]  GFE.Pre.mesh.element.nodes
[prop]  GFE.Pre.mesh.element.state
[prop]  GFE.Pre.mesh.element.sub_type
[class] GFE.Pre.mesh.manager
[func]  GFE.Pre.mesh.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.mesh.manager.add    1. (self: GFE.Pre.mesh.manager, arg0: str, arg1: GFE::Pre::Gfe_MeshData) -> tuple[GFE::MeshObj, generic_mgr.generic.err_code] ; 2. (self: GFE.Pre.mesh.manager, arg0: str, arg1: float, arg2: float, arg3: float) -> tuple[GFE::MeshObj, generic_mgr.generic.err_code]
[func]  GFE.Pre.mesh.manager.auto_name    1. (self: generic_mgr.generic, prefix: str, has0: bool = False) -> str
[func]  GFE.Pre.mesh.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.mesh.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.mesh.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.mesh.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.mesh.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.mesh.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.mesh.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.mesh.manager.delete_all    (疑似改模型, 未实调用)
[enum]  GFE.Pre.mesh.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.mesh.manager.find    1. (self: GFE.Pre.mesh.manager, arg0: str) -> GFE::MeshObj ; 2. (self: GFE.Pre.mesh.manager, arg0: int) -> GFE::MeshObj
[func]  GFE.Pre.mesh.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.mesh.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.mesh.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.mesh.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.mesh.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.mesh.manager.status
[func]  GFE.Pre.mesh.manager.update    (疑似改模型, 未实调用)
[func]  GFE.Pre.mesh.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.mesh.mesh_data
[func]  GFE.Pre.mesh.mesh_data.add_element    1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> tuple[int, bool] ; 2. (self: GFE.Pre.mesh.mesh_data, arg0: list[GFE.Pre.mesh.element]) -> tuple[int, bool]
[func]  GFE.Pre.mesh.mesh_data.add_node    1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.node) -> tuple[int, bool] ; 2. (self: GFE.Pre.mesh.mesh_data, arg0: list[GFE.Pre.mesh.node]) -> tuple[int, bool]
[func]  GFE.Pre.mesh.mesh_data.get_element    1. (self: GFE.Pre.mesh.mesh_data, eid: int) -> GFE.Pre.mesh.element
[func]  GFE.Pre.mesh.mesh_data.get_element_subtype    1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> int ; 2. (self: GFE.Pre.mesh.mesh_data, eid: int) -> int
[func]  GFE.Pre.mesh.mesh_data.get_element_surface    1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> list[int] ; 2. (self: GFE.Pre.mesh.mesh_data, arg0: int) -> list[int] ; 3. (self: GFE.Pre.mesh.mesh_data, element: GFE.Pre.mesh.element, face_id: int) -> list[int] ; 4. (self: GFE.Pre.mesh.mesh_data, eid: int, face_id: int) -> list[int]
[func]  GFE.Pre.mesh.mesh_data.get_element_type    1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> int ; 2. (self: GFE.Pre.mesh.mesh_data, eid: int) -> int
[func]  GFE.Pre.mesh.mesh_data.get_node    1. (self: GFE.Pre.mesh.mesh_data, nid: int) -> GFE.Pre.mesh.node
[func]  GFE.Pre.mesh.mesh_data.rebuild_surface    1. (self: GFE.Pre.mesh.mesh_data) -> bool
[func]  GFE.Pre.mesh.mesh_data.remove_element    (疑似改模型, 未实调用)
[class] GFE.Pre.mesh.mesh_mgr
[class] GFE.Pre.mesh.mesh_obj
[prop]  GFE.Pre.mesh.mesh_obj.doc
[func]  GFE.Pre.mesh.mesh_obj.each_et_elems    1. (self: GFE.Pre.mesh.mesh_obj) -> QMap<QString,QVariant>
[func]  GFE.Pre.mesh.mesh_obj.each_et_nodes    1. (self: GFE.Pre.mesh.mesh_obj) -> QMap<QString,QVariant>
[func]  GFE.Pre.mesh.mesh_obj.element_data    1. (self: GFE.Pre.mesh.mesh_obj) -> tuple[list[int], list[int]]
[func]  GFE.Pre.mesh.mesh_obj.et_elems    1. (self: GFE.Pre.mesh.mesh_obj, arg0: str) -> list[int]
[func]  GFE.Pre.mesh.mesh_obj.et_elems_by_id    1. (self: GFE.Pre.mesh.mesh_obj, arg0: int, arg1: int) -> list[int]
[func]  GFE.Pre.mesh.mesh_obj.et_nodes    1. (self: GFE.Pre.mesh.mesh_obj, arg0: str) -> list[int]
[func]  GFE.Pre.mesh.mesh_obj.et_nodes_by_id    1. (self: GFE.Pre.mesh.mesh_obj, arg0: int, arg1: int) -> list[int]
[func]  GFE.Pre.mesh.mesh_obj.geo_obj    1. (self: GFE.Pre.mesh.mesh_obj) -> GFE.Pre.geometry.object
[func]  GFE.Pre.mesh.mesh_obj.get_node_coordinate    1. (self: GFE.Pre.mesh.mesh_obj, arg0: int) -> Optional[Vec3D]
[func]  GFE.Pre.mesh.mesh_obj.id    1. (self: GFE.Pre.mesh.mesh_obj) -> int
[func]  GFE.Pre.mesh.mesh_obj.is_valid    1. (self: GFE.Pre.mesh.mesh_obj) -> bool
[prop]  GFE.Pre.mesh.mesh_obj.label
[func]  GFE.Pre.mesh.mesh_obj.mesh    (疑似改模型, 未实调用)
[prop]  GFE.Pre.mesh.mesh_obj.mesh_data
[func]  GFE.Pre.mesh.mesh_obj.name    1. (self: GFE.Pre.mesh.mesh_obj) -> str
[func]  GFE.Pre.mesh.mesh_obj.node_data    1. (self: GFE.Pre.mesh.mesh_obj) -> tuple[list[int], list[Vec3D]]
[func]  GFE.Pre.mesh.mesh_obj.prs    1. (self: GFE.Pre.mesh.mesh_obj) -> TPrsStd_AISPresentation
[func]  GFE.Pre.mesh.mesh_obj.transformation    1. (self: GFE.Pre.mesh.mesh_obj) -> gp_Trsf
[class] GFE.Pre.mesh.node
[prop]  GFE.Pre.mesh.node.nid
[prop]  GFE.Pre.mesh.node.xyz
[mod]   GFE.Pre.orientation
[class] GFE.Pre.orientation.manager
[func]  GFE.Pre.orientation.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.orientation.manager.add    1. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.orientation.manager.auto_name    1. (self: GFE.Pre.orientation.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.orientation.manager, arg0: GFE::Pre::Orientation) -> str
[func]  GFE.Pre.orientation.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.orientation.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.orientation.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.orientation.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.orientation.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.orientation.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.orientation.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.orientation.manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.orientation.manager.edit    1. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation) -> generic_mgr.generic.status
[enum]  GFE.Pre.orientation.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.orientation.manager.find    1. (self: GFE.Pre.orientation.manager, arg0: str) -> GFE::Pre::Orientation
[func]  GFE.Pre.orientation.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.orientation.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.orientation.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.orientation.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.orientation.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.orientation.manager.status
[func]  GFE.Pre.orientation.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.orientation.orientation
[prop]  GFE.Pre.orientation.orientation.data
[prop]  GFE.Pre.orientation.orientation.definition
[prop]  GFE.Pre.orientation.orientation.name
[prop]  GFE.Pre.orientation.orientation.type
[class] GFE.Pre.orientation.orientation_mgr
[mod]   GFE.Pre.output
[class] GFE.Pre.output.contact_output
[prop]  GFE.Pre.output.contact_output.general_contact
[prop]  GFE.Pre.output.contact_output.name
[prop]  GFE.Pre.output.contact_output.reg_type
[prop]  GFE.Pre.output.contact_output.surface
[prop]  GFE.Pre.output.contact_output.var_option
[prop]  GFE.Pre.output.contact_output.variables
[class] GFE.Pre.output.element_output
[prop]  GFE.Pre.output.element_output.elset
[prop]  GFE.Pre.output.element_output.name
[prop]  GFE.Pre.output.element_output.reg_type
[prop]  GFE.Pre.output.element_output.var_option
[prop]  GFE.Pre.output.element_output.variables
[class] GFE.Pre.output.energy_output
[prop]  GFE.Pre.output.energy_output.elset
[prop]  GFE.Pre.output.energy_output.name
[prop]  GFE.Pre.output.energy_output.per_element_set
[prop]  GFE.Pre.output.energy_output.reg_type
[prop]  GFE.Pre.output.energy_output.var_option
[prop]  GFE.Pre.output.energy_output.variables
[class] GFE.Pre.output.field_mgr
[func]  GFE.Pre.output.field_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.output.field_mgr.add    1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.output.field_mgr.auto_name    1. (self: GFE.Pre.output.field_mgr, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.output.field_mgr, arg0: GFE::Pre::OutputRequest) -> str
[func]  GFE.Pre.output.field_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.field_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.field_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.field_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.field_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.field_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.field_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.output.field_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.output.field_mgr.edit    1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status
[enum]  GFE.Pre.output.field_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.output.field_mgr.find    1. (self: GFE.Pre.output.out_req_mgr, nameFind a GFE::Pre::OutputRequest by name: str) -> GFE::Pre::OutputRequest
[func]  GFE.Pre.output.field_mgr.find_all    1. (self: GFE.Pre.output.out_req_mgr) -> list[GFE::Pre::OutputRequest]
[func]  GFE.Pre.output.field_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.field_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.field_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.field_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.field_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.output.field_mgr.status
[func]  GFE.Pre.output.field_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.output.history_mgr
[func]  GFE.Pre.output.history_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.output.history_mgr.add    1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.output.history_mgr.auto_name    1. (self: GFE.Pre.output.history_mgr, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.output.history_mgr, arg0: GFE::Pre::OutputRequest) -> str
[func]  GFE.Pre.output.history_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.history_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.history_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.history_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.history_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.history_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.history_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.output.history_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.output.history_mgr.edit    1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status
[enum]  GFE.Pre.output.history_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.output.history_mgr.find    1. (self: GFE.Pre.output.out_req_mgr, nameFind a GFE::Pre::OutputRequest by name: str) -> GFE::Pre::OutputRequest
[func]  GFE.Pre.output.history_mgr.find_all    1. (self: GFE.Pre.output.out_req_mgr) -> list[GFE::Pre::OutputRequest]
[func]  GFE.Pre.output.history_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.history_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.history_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.history_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.history_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.output.history_mgr.status
[func]  GFE.Pre.output.history_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.output.integrated_output
[prop]  GFE.Pre.output.integrated_output.elset
[prop]  GFE.Pre.output.integrated_output.name
[prop]  GFE.Pre.output.integrated_output.reg_type
[prop]  GFE.Pre.output.integrated_output.surface
[prop]  GFE.Pre.output.integrated_output.var_option
[prop]  GFE.Pre.output.integrated_output.variables
[class] GFE.Pre.output.node_output
[prop]  GFE.Pre.output.node_output.name
[prop]  GFE.Pre.output.node_output.nset
[prop]  GFE.Pre.output.node_output.reg_type
[prop]  GFE.Pre.output.node_output.var_option
[prop]  GFE.Pre.output.node_output.variables
[class] GFE.Pre.output.out_req_mgr
[func]  GFE.Pre.output.out_req_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.output.out_req_mgr.add    1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.output.out_req_mgr.auto_name    1. (self: generic_mgr.generic, prefix: str, has0: bool = False) -> str
[func]  GFE.Pre.output.out_req_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.out_req_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.out_req_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.out_req_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.out_req_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.out_req_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.output.out_req_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.output.out_req_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.output.out_req_mgr.edit    1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status
[enum]  GFE.Pre.output.out_req_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.output.out_req_mgr.find    1. (self: GFE.Pre.output.out_req_mgr, nameFind a GFE::Pre::OutputRequest by name: str) -> GFE::Pre::OutputRequest
[func]  GFE.Pre.output.out_req_mgr.find_all    1. (self: GFE.Pre.output.out_req_mgr) -> list[GFE::Pre::OutputRequest]
[func]  GFE.Pre.output.out_req_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.output.out_req_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.out_req_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.out_req_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.output.out_req_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.output.out_req_mgr.status
[func]  GFE.Pre.output.out_req_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.output.output_request
[prop]  GFE.Pre.output.output_request.frequency
[prop]  GFE.Pre.output.output_request.method
[prop]  GFE.Pre.output.output_request.name
[prop]  GFE.Pre.output.output_request.number_interval
[prop]  GFE.Pre.output.output_request.step
[prop]  GFE.Pre.output.output_request.sub_output
[prop]  GFE.Pre.output.output_request.time_interval
[prop]  GFE.Pre.output.output_request.time_points
[prop]  GFE.Pre.output.output_request.time_type
[prop]  GFE.Pre.output.output_request.type
[prop]  GFE.Pre.output.output_request.var_option
[class] GFE.Pre.output.sub_output
[prop]  GFE.Pre.output.sub_output.name
[prop]  GFE.Pre.output.sub_output.reg_type
[prop]  GFE.Pre.output.sub_output.var_option
[prop]  GFE.Pre.output.sub_output.variables
[mod]   GFE.Pre.section
[class] GFE.Pre.section.manager
[func]  GFE.Pre.section.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.section.manager.add    1. (self: GFE.Pre.section.manager, obj: GFE::Property, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.section.manager, obj: GFE::Property, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.section.manager.auto_name    1. (self: GFE.Pre.section.manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.section.manager, arg0: GFE::Property) -> str
[func]  GFE.Pre.section.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.section.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.section.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.section.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.section.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.section.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.section.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.section.manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.section.manager.edit    1. (self: GFE.Pre.section.manager, obj: GFE::Property) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.section.manager, obj: GFE::Property) -> generic_mgr.generic.status
[enum]  GFE.Pre.section.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.section.manager.find    1. (self: GFE.Pre.section.manager, arg0: str) -> GFE::Property
[func]  GFE.Pre.section.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.section.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.section.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.section.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.section.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.section.manager.status
[func]  GFE.Pre.section.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.section.property
[prop]  GFE.Pre.section.property.elset_name
[prop]  GFE.Pre.section.property.name
[prop]  GFE.Pre.section.property.type
[class] GFE.Pre.section.property_beam
[prop]  GFE.Pre.section.property_beam.direction
[prop]  GFE.Pre.section.property_beam.elset_name
[prop]  GFE.Pre.section.property_beam.fiber_num
[prop]  GFE.Pre.section.property_beam.mat_name
[prop]  GFE.Pre.section.property_beam.name
[prop]  GFE.Pre.section.property_beam.params
[prop]  GFE.Pre.section.property_beam.shape
[prop]  GFE.Pre.section.property_beam.shape_params
[prop]  GFE.Pre.section.property_beam.shear
[prop]  GFE.Pre.section.property_beam.type
[class] GFE.Pre.section.property_beam_general
[prop]  GFE.Pre.section.property_beam_general.axis
[prop]  GFE.Pre.section.property_beam_general.density
[prop]  GFE.Pre.section.property_beam_general.elset_name
[prop]  GFE.Pre.section.property_beam_general.name
[prop]  GFE.Pre.section.property_beam_general.param1
[prop]  GFE.Pre.section.property_beam_general.param2
[prop]  GFE.Pre.section.property_beam_general.poisson
[prop]  GFE.Pre.section.property_beam_general.type
[class] GFE.Pre.section.property_bush
[prop]  GFE.Pre.section.property_bush.elset_name
[prop]  GFE.Pre.section.property_bush.name
[prop]  GFE.Pre.section.property_bush.params
[prop]  GFE.Pre.section.property_bush.type
[class] GFE.Pre.section.property_membrane
[prop]  GFE.Pre.section.property_membrane.elset_name
[prop]  GFE.Pre.section.property_membrane.has_rebar
[prop]  GFE.Pre.section.property_membrane.mat_name
[prop]  GFE.Pre.section.property_membrane.name
[prop]  GFE.Pre.section.property_membrane.rebar
[prop]  GFE.Pre.section.property_membrane.thickness
[prop]  GFE.Pre.section.property_membrane.type
[class] GFE.Pre.section.property_shell
[prop]  GFE.Pre.section.property_shell.elset_name
[prop]  GFE.Pre.section.property_shell.has_rebar
[prop]  GFE.Pre.section.property_shell.integral_point
[prop]  GFE.Pre.section.property_shell.layer_num
[prop]  GFE.Pre.section.property_shell.mat_name
[prop]  GFE.Pre.section.property_shell.name
[prop]  GFE.Pre.section.property_shell.params
[prop]  GFE.Pre.section.property_shell.rebar
[prop]  GFE.Pre.section.property_shell.thickness
[prop]  GFE.Pre.section.property_shell.type
[class] GFE.Pre.section.property_solid
[prop]  GFE.Pre.section.property_solid.elset_name
[prop]  GFE.Pre.section.property_solid.has_thickness
[prop]  GFE.Pre.section.property_solid.mat_name
[prop]  GFE.Pre.section.property_solid.name
[prop]  GFE.Pre.section.property_solid.thickness
[prop]  GFE.Pre.section.property_solid.type
[class] GFE.Pre.section.rebar_layer
[prop]  GFE.Pre.section.rebar_layer.layer_name
[prop]  GFE.Pre.section.rebar_layer.mat_name
[prop]  GFE.Pre.section.rebar_layer.orientation_name
[prop]  GFE.Pre.section.rebar_layer.params
[prop]  GFE.Pre.section.rebar_layer.rebar_geometry
[prop]  GFE.Pre.section.rebar_layer.rebar_num
[class] GFE.Pre.section.sect_mgr
[mod]   GFE.Pre.set
[class] GFE.Pre.set.basic_set
[func]  GFE.Pre.set.basic_set.add_attribute    1. (self: GFE.Pre.set.gset, arg0: int, arg1: bool) -> None
[func]  GFE.Pre.set.basic_set.get_shapes    1. (self: GFE.Pre.set.basic_set) -> list[TopoDS_Shape]
[func]  GFE.Pre.set.basic_set.get_shapes_id    1. (self: GFE.Pre.set.basic_set) -> list[Annotated[list[int], FixedSize(3)]]
[prop]  GFE.Pre.set.basic_set.name
[func]  GFE.Pre.set.basic_set.set_shapes    1. (self: GFE.Pre.set.basic_set, arg0: list[TopoDS_Shape]) -> None
[func]  GFE.Pre.set.basic_set.set_shapes_id    1. (self: GFE.Pre.set.basic_set, arg0: list[Annotated[list[int], FixedSize(3)]]) -> None
[class] GFE.Pre.set.elset
[prop]  GFE.Pre.set.elset.data
[prop]  GFE.Pre.set.elset.name
[prop]  GFE.Pre.set.elset.unsort
[class] GFE.Pre.set.elset_manager
[func]  GFE.Pre.set.elset_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.set.elset_manager.add    1. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.set.elset_manager.auto_name    1. (self: GFE.Pre.set.elset_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.set.elset_manager, arg0: GFE::Pre::ElSet) -> str
[func]  GFE.Pre.set.elset_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.elset_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.elset_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.elset_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.elset_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.elset_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.elset_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.set.elset_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.set.elset_manager.edit    1. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet) -> generic_mgr.generic.status
[enum]  GFE.Pre.set.elset_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.set.elset_manager.find    1. (self: GFE.Pre.set.elset_manager, arg0: str) -> GFE::Pre::ElSet
[func]  GFE.Pre.set.elset_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.elset_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.elset_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.elset_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.elset_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.set.elset_manager.status
[func]  GFE.Pre.set.elset_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.set.elset_mgr
[class] GFE.Pre.set.gset
[func]  GFE.Pre.set.gset.add_attribute    1. (self: GFE.Pre.set.gset, arg0: int, arg1: bool) -> None
[prop]  GFE.Pre.set.gset.name
[class] GFE.Pre.set.gset_manager
[func]  GFE.Pre.set.gset_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.set.gset_manager.add    1. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 3. (self: GFE.Pre.set.gset_manager, name: str, shapes: list[TopoDS_Shape], hidden: bool = False, auto name: bool = False) -> generic_mgr.generic.status ; 4. (self: GFE.Pre.set.gset_manager, name: str, shapes: list[Annotated[list[int], FixedSize(3)]], hidden: bool = False, auto name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.set.gset_manager.auto_name    1. (self: GFE.Pre.set.gset_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.set.gset_manager, arg0: GFE::Pre::GSet) -> str
[func]  GFE.Pre.set.gset_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.gset_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.gset_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.gset_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.gset_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.gset_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.gset_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.set.gset_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.set.gset_manager.edit    1. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet) -> generic_mgr.generic.status
[enum]  GFE.Pre.set.gset_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.set.gset_manager.find    1. (self: GFE.Pre.set.gset_manager, arg0: str) -> GFE::Pre::GSet
[func]  GFE.Pre.set.gset_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.gset_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.gset_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.gset_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.gset_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.set.gset_manager.status
[func]  GFE.Pre.set.gset_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.set.gset_mgr
[class] GFE.Pre.set.nset
[prop]  GFE.Pre.set.nset.data
[prop]  GFE.Pre.set.nset.name
[prop]  GFE.Pre.set.nset.unsort
[class] GFE.Pre.set.nset_manager
[func]  GFE.Pre.set.nset_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.set.nset_manager.add    1. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.set.nset_manager.auto_name    1. (self: GFE.Pre.set.nset_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.set.nset_manager, arg0: GFE::Pre::NSet) -> str
[func]  GFE.Pre.set.nset_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.nset_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.nset_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.nset_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.nset_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.nset_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.set.nset_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.set.nset_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.set.nset_manager.edit    1. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet) -> generic_mgr.generic.status
[enum]  GFE.Pre.set.nset_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.set.nset_manager.find    1. (self: GFE.Pre.set.nset_manager, arg0: str) -> GFE::Pre::NSet
[func]  GFE.Pre.set.nset_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.set.nset_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.nset_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.nset_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.set.nset_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.set.nset_manager.status
[func]  GFE.Pre.set.nset_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.set.nset_mgr
[mod]   GFE.Pre.soil
[class] GFE.Pre.soil.manager
[func]  GFE.Pre.soil.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.soil.manager.add    1. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.soil.manager.auto_name    1. (self: GFE.Pre.soil.soil_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.soil.soil_manager, arg0: GFE::Pre::Soil1D) -> str
[func]  GFE.Pre.soil.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.soil.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.soil.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.soil.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.soil.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.soil.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.soil.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.soil.manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.soil.manager.edit    1. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D) -> generic_mgr.generic.status
[enum]  GFE.Pre.soil.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.soil.manager.find    1. (self: GFE.Pre.soil.soil_manager, arg0: str) -> GFE::Pre::Soil1D
[func]  GFE.Pre.soil.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.soil.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.soil.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.soil.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.soil.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.soil.manager.status
[func]  GFE.Pre.soil.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.soil.soil
[prop]  GFE.Pre.soil.soil.bedrock_mat
[prop]  GFE.Pre.soil.soil.depth
[prop]  GFE.Pre.soil.soil.depth_dir
[prop]  GFE.Pre.soil.soil.materials
[prop]  GFE.Pre.soil.soil.name
[class] GFE.Pre.soil.soil_manager
[class] GFE.Pre.soil.soil_mgr
[mod]   GFE.Pre.sph
[class] GFE.Pre.sph.sph_manager
[func]  GFE.Pre.sph.sph_manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.sph.sph_manager.add    1. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.sph.sph_manager.auto_name    1. (self: GFE.Pre.sph.sph_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.sph.sph_manager, arg0: GFE::Pre::SPH) -> str
[func]  GFE.Pre.sph.sph_manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.sph.sph_manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.sph.sph_manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.sph.sph_manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.sph.sph_manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.sph.sph_manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.sph.sph_manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.sph.sph_manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.sph.sph_manager.edit    1. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH) -> generic_mgr.generic.status
[enum]  GFE.Pre.sph.sph_manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.sph.sph_manager.find    1. (self: GFE.Pre.sph.sph_manager, arg0: str) -> GFE::Pre::SPH
[func]  GFE.Pre.sph.sph_manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.sph.sph_manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.sph.sph_manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.sph.sph_manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.sph.sph_manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.sph.sph_manager.status
[func]  GFE.Pre.sph.sph_manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.sph.sph_mgr
[mod]   GFE.Pre.step
[enum]  GFE.Pre.step.StepType  = Initial, DynamicExplicit, StaticGeneral, Frequency, SteadyStateDynamics, GeoStatic, ModalDynamic2, DynamicImplicit, ResponseSpectrum2, Soils, SPH, CoupledTemp
[class] GFE.Pre.step.analysis_step
[prop]  GFE.Pre.step.analysis_step.description
[prop]  GFE.Pre.step.analysis_step.name
[prop]  GFE.Pre.step.analysis_step.nlgeom
[class] GFE.Pre.step.dyn_modal_damping
[prop]  GFE.Pre.step.dyn_modal_damping.db
[prop]  GFE.Pre.step.dyn_modal_damping.set_name
[prop]  GFE.Pre.step.dyn_modal_damping.values
[class] GFE.Pre.step.dynamic_explicit_step
[prop]  GFE.Pre.step.dynamic_explicit_step.description
[prop]  GFE.Pre.step.dynamic_explicit_step.mass_scaling
[prop]  GFE.Pre.step.dynamic_explicit_step.modal_damping
[prop]  GFE.Pre.step.dynamic_explicit_step.name
[prop]  GFE.Pre.step.dynamic_explicit_step.nlgeom
[prop]  GFE.Pre.step.dynamic_explicit_step.period
[class] GFE.Pre.step.dynamic_implicit_step
[prop]  GFE.Pre.step.dynamic_implicit_step.description
[prop]  GFE.Pre.step.dynamic_implicit_step.direct
[prop]  GFE.Pre.step.dynamic_implicit_step.explicit_
[prop]  GFE.Pre.step.dynamic_implicit_step.gfe_linear
[prop]  GFE.Pre.step.dynamic_implicit_step.init_inc
[prop]  GFE.Pre.step.dynamic_implicit_step.max_inc
[prop]  GFE.Pre.step.dynamic_implicit_step.min_inc
[prop]  GFE.Pre.step.dynamic_implicit_step.name
[prop]  GFE.Pre.step.dynamic_implicit_step.nlgeom
[prop]  GFE.Pre.step.dynamic_implicit_step.period
[class] GFE.Pre.step.frequency_step
[prop]  GFE.Pre.step.frequency_step.description
[prop]  GFE.Pre.step.frequency_step.eigen
[prop]  GFE.Pre.step.frequency_step.name
[prop]  GFE.Pre.step.frequency_step.nlgeom
[class] GFE.Pre.step.geo_static_step
[prop]  GFE.Pre.step.geo_static_step.description
[prop]  GFE.Pre.step.geo_static_step.init_inc
[prop]  GFE.Pre.step.geo_static_step.max_inc
[prop]  GFE.Pre.step.geo_static_step.min_inc
[prop]  GFE.Pre.step.geo_static_step.name
[prop]  GFE.Pre.step.geo_static_step.nlgeom
[prop]  GFE.Pre.step.geo_static_step.period
[class] GFE.Pre.step.global_damping
[prop]  GFE.Pre.step.global_damping.alpha
[prop]  GFE.Pre.step.global_damping.beta
[prop]  GFE.Pre.step.global_damping.field
[prop]  GFE.Pre.step.global_damping.structual
[enum]  GFE.Pre.step.global_damping_field  = All, Mechanical, Acoustic
[class] GFE.Pre.step.manager
[func]  GFE.Pre.step.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.step.manager.add    1. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.step.manager.auto_name    1. (self: GFE.Pre.step.step_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.step.step_manager, arg0: GFE::Pre::AnalysisStep) -> str
[func]  GFE.Pre.step.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.step.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.step.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.step.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.step.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.step.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.step.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.step.manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.step.manager.edit    1. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep) -> generic_mgr.generic.status
[enum]  GFE.Pre.step.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.step.manager.find    1. (self: GFE.Pre.step.step_manager, arg0: str) -> GFE::Pre::AnalysisStep
[func]  GFE.Pre.step.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.step.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.step.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.step.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.step.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.step.manager.status
[func]  GFE.Pre.step.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.step.mass_scaling
[prop]  GFE.Pre.step.mass_scaling.frequency
[prop]  GFE.Pre.step.mass_scaling.region
[prop]  GFE.Pre.step.mass_scaling.target_time
[prop]  GFE.Pre.step.mass_scaling.type
[class] GFE.Pre.step.modal_damping
[prop]  GFE.Pre.step.modal_damping.data
[prop]  GFE.Pre.step.modal_damping.definition
[prop]  GFE.Pre.step.modal_damping.field
[prop]  GFE.Pre.step.modal_damping.type
[enum]  GFE.Pre.step.modal_damping_definition  = Mode, Freq
[enum]  GFE.Pre.step.modal_damping_field  = All, Mechanical, Acoustic
[enum]  GFE.Pre.step.modal_damping_type  = Direct, Composite, Rayleigh, Structural
[class] GFE.Pre.step.modal_dynamic_step
[prop]  GFE.Pre.step.modal_dynamic_step.cont
[prop]  GFE.Pre.step.modal_dynamic_step.description
[prop]  GFE.Pre.step.modal_dynamic_step.modal_damping
[prop]  GFE.Pre.step.modal_dynamic_step.name
[prop]  GFE.Pre.step.modal_dynamic_step.nlgeom
[prop]  GFE.Pre.step.modal_dynamic_step.time_increment
[prop]  GFE.Pre.step.modal_dynamic_step.time_period
[class] GFE.Pre.step.response_spectrum_step
[prop]  GFE.Pre.step.response_spectrum_step.data
[prop]  GFE.Pre.step.response_spectrum_step.description
[prop]  GFE.Pre.step.response_spectrum_step.modal_damping
[prop]  GFE.Pre.step.response_spectrum_step.name
[prop]  GFE.Pre.step.response_spectrum_step.nlgeom
[prop]  GFE.Pre.step.response_spectrum_step.spectrum
[prop]  GFE.Pre.step.response_spectrum_step.sum
[class] GFE.Pre.step.soils_step
[prop]  GFE.Pre.step.soils_step.cetol
[prop]  GFE.Pre.step.soils_step.description
[prop]  GFE.Pre.step.soils_step.end
[prop]  GFE.Pre.step.soils_step.init_inc
[prop]  GFE.Pre.step.soils_step.is_consolidation
[prop]  GFE.Pre.step.soils_step.max_inc
[prop]  GFE.Pre.step.soils_step.min_inc
[prop]  GFE.Pre.step.soils_step.name
[prop]  GFE.Pre.step.soils_step.nlgeom
[prop]  GFE.Pre.step.soils_step.period
[prop]  GFE.Pre.step.soils_step.utol
[class] GFE.Pre.step.sph_step
[prop]  GFE.Pre.step.sph_step.auto_area
[prop]  GFE.Pre.step.sph_step.b
[prop]  GFE.Pre.step.sph_step.beam_sect
[prop]  GFE.Pre.step.sph_step.box_area
[prop]  GFE.Pre.step.sph_step.cflnumber
[prop]  GFE.Pre.step.sph_step.coefh
[prop]  GFE.Pre.step.sph_step.coefsound
[prop]  GFE.Pre.step.sph_step.description
[prop]  GFE.Pre.step.sph_step.distance
[prop]  GFE.Pre.step.sph_step.excute_para
[prop]  GFE.Pre.step.sph_step.gamma
[prop]  GFE.Pre.step.sph_step.gravity
[prop]  GFE.Pre.step.sph_step.h
[prop]  GFE.Pre.step.sph_step.hswl
[prop]  GFE.Pre.step.sph_step.lattice
[prop]  GFE.Pre.step.sph_step.massbound
[prop]  GFE.Pre.step.sph_step.massfluid
[prop]  GFE.Pre.step.sph_step.name
[prop]  GFE.Pre.step.sph_step.nlgeom
[prop]  GFE.Pre.step.sph_step.objects
[prop]  GFE.Pre.step.sph_step.pointref
[prop]  GFE.Pre.step.sph_step.rhop0
[prop]  GFE.Pre.step.sph_step.rhopgradient
[prop]  GFE.Pre.step.sph_step.shell_sect
[prop]  GFE.Pre.step.sph_step.speedsound
[prop]  GFE.Pre.step.sph_step.speedsystem
[class] GFE.Pre.step.static_general_step
[prop]  GFE.Pre.step.static_general_step.description
[prop]  GFE.Pre.step.static_general_step.init_inc
[prop]  GFE.Pre.step.static_general_step.max_inc
[prop]  GFE.Pre.step.static_general_step.min_inc
[prop]  GFE.Pre.step.static_general_step.name
[prop]  GFE.Pre.step.static_general_step.nlgeom
[prop]  GFE.Pre.step.static_general_step.period
[class] GFE.Pre.step.steady_dyn_step
[prop]  GFE.Pre.step.steady_dyn_step.data
[prop]  GFE.Pre.step.steady_dyn_step.description
[prop]  GFE.Pre.step.steady_dyn_step.direct
[func]  GFE.Pre.step.steady_dyn_step.get_single_points    1. (self: GFE.Pre.step.steady_dyn_step, arg0: list[float]) -> list[float]
[prop]  GFE.Pre.step.steady_dyn_step.global_damping
[prop]  GFE.Pre.step.steady_dyn_step.interval
[prop]  GFE.Pre.step.steady_dyn_step.modal_damping
[prop]  GFE.Pre.step.steady_dyn_step.name
[prop]  GFE.Pre.step.steady_dyn_step.nlgeom
[prop]  GFE.Pre.step.steady_dyn_step.scale
[class] GFE.Pre.step.step_manager
[class] GFE.Pre.step.step_mgr
[mod]   GFE.Pre.surface
[class] GFE.Pre.surface.element_surface
[prop]  GFE.Pre.surface.element_surface.data
[prop]  GFE.Pre.surface.element_surface.elsets
[prop]  GFE.Pre.surface.element_surface.name
[class] GFE.Pre.surface.geometry_surface
[prop]  GFE.Pre.surface.geometry_surface.data
[func]  GFE.Pre.surface.geometry_surface.get_shape    1. (self: GFE.Pre.surface.geometry_surface, arg0: Handle_TDocStd_Document) -> list[tuple[int, TopoDS_Shape, int]]
[prop]  GFE.Pre.surface.geometry_surface.name
[prop]  GFE.Pre.surface.geometry_surface.to_node_surface
[class] GFE.Pre.surface.manager
[func]  GFE.Pre.surface.manager.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.surface.manager.add    1. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.surface.manager.auto_name    1. (self: GFE.Pre.surface.surface_mgr, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.surface.surface_mgr, arg0: GFE::Pre::Surface) -> str
[func]  GFE.Pre.surface.manager.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.surface.manager.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.surface.manager.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.surface.manager.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.surface.manager.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.surface.manager.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.surface.manager.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.surface.manager.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.surface.manager.edit    1. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface) -> generic_mgr.generic.status
[enum]  GFE.Pre.surface.manager.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.surface.manager.find    1. (self: GFE.Pre.surface.surface_mgr, arg0: str) -> GFE::Pre::Surface
[func]  GFE.Pre.surface.manager.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.surface.manager.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.surface.manager.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.surface.manager.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.surface.manager.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.surface.manager.status
[func]  GFE.Pre.surface.manager.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.surface.node_surface
[prop]  GFE.Pre.surface.node_surface.data
[prop]  GFE.Pre.surface.node_surface.name
[class] GFE.Pre.surface.surf_mgr
[class] GFE.Pre.surface.surface
[prop]  GFE.Pre.surface.surface.name
[class] GFE.Pre.surface.surface_mgr
[mod]   GFE.Pre.vibration
[class] GFE.Pre.vibration.vib_mgr
[func]  GFE.Pre.vibration.vib_mgr.activate    1. (self: generic_mgr.generic, arg0: str, arg1: bool) -> None
[func]  GFE.Pre.vibration.vib_mgr.add    1. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
[func]  GFE.Pre.vibration.vib_mgr.auto_name    1. (self: GFE.Pre.vibration.vibraload_manager, prefix: str, has0: bool = False) -> str ; 2. (self: GFE.Pre.vibration.vibraload_manager, arg0: GFE::VibraLoad) -> str
[func]  GFE.Pre.vibration.vib_mgr.contains    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.vibration.vib_mgr.contains_all    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.vibration.vib_mgr.contains_hidden    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.vibration.vib_mgr.count    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.vibration.vib_mgr.count_all    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.vibration.vib_mgr.count_hidden    1. (self: generic_mgr.generic) -> int
[func]  GFE.Pre.vibration.vib_mgr.delete    (疑似改模型, 未实调用)
[func]  GFE.Pre.vibration.vib_mgr.delete_all    (疑似改模型, 未实调用)
[func]  GFE.Pre.vibration.vib_mgr.edit    1. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad) -> generic_mgr.generic.status
[enum]  GFE.Pre.vibration.vib_mgr.err_code  = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
[func]  GFE.Pre.vibration.vib_mgr.find    1. (self: GFE.Pre.vibration.vibraload_manager, arg0: str) -> GFE::VibraLoad
[func]  GFE.Pre.vibration.vib_mgr.is_active    1. (self: generic_mgr.generic, arg0: str) -> bool
[func]  GFE.Pre.vibration.vib_mgr.name_all    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.vibration.vib_mgr.name_hidden    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.vibration.vib_mgr.name_list    1. (self: generic_mgr.generic) -> list[str]
[func]  GFE.Pre.vibration.vib_mgr.rename    1. (self: generic_mgr.generic, arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode
[class] GFE.Pre.vibration.vib_mgr.status
[func]  GFE.Pre.vibration.vib_mgr.valid_tag    1. (self: generic_mgr.generic, arg0: bool) -> set[int]
[class] GFE.Pre.vibration.vibra_load
[prop]  GFE.Pre.vibration.vibra_load.amp_bottom_x
[prop]  GFE.Pre.vibration.vibra_load.amp_bottom_y
[prop]  GFE.Pre.vibration.vibra_load.amp_bottom_z
[prop]  GFE.Pre.vibration.vibra_load.input_loc
[prop]  GFE.Pre.vibration.vibra_load.is_outcrop
[prop]  GFE.Pre.vibration.vibra_load.level
[prop]  GFE.Pre.vibration.vibra_load.name
[prop]  GFE.Pre.vibration.vibra_load.pwave_dir
[func]  GFE.Pre.vibration.vibra_load.set_parameter    1. (self: GFE.Pre.vibration.vibra_load, arg0: str, arg1: str) -> None
[prop]  GFE.Pre.vibration.vibra_load.soil
[class] GFE.Pre.vibration.vibraload_manager
[mod]   GFE.draft
[enum]  GFE.draft.Normal  = X, Y, Z
[enum]  GFE.draft.OpMode  = OP_None, OP_Point, OP_Line, OP_Polyline, OP_Rect, OP_Arc_Three_Point, OP_Arc_Centre_Point, OP_Circle_Three_Point, OP_Circle_Centre_Point, OP_Translate, OP_Mirror_Point, OP_Mirror_Axis, OP_Rotate, OP_Scale, OP_Fill_Area, OP_Array, OP_RoundArray, OP_Extrude, OP_Revolute, CST_Horizontal, CST_Vertical, CST_Length, CST_Parallel, CST_Perpendicular, CST_Tangent
[enum]  GFE.draft.SnapObjMode  = SO_None, SO_Point, SO_Edge, SO_Surface
[class] GFE.draft.controller
[func]  GFE.draft.controller.add_arc_centre    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.add_arc_points    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.add_circle_centre    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.add_circle_points    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.add_line    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.add_point    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.add_polyline    1. (self: GFE.draft.controller, arg0: list[Annotated[list[float], FixedSize(2)]]) -> None
[func]  GFE.draft.controller.add_rectangle    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)]) -> None
[func]  GFE.draft.controller.array_selected    1. (self: GFE.draft.controller, extend_x: int, extend_y: int, offset_x: float, offset_y: float) -> None
[func]  GFE.draft.controller.clear    (疑似改模型, 未实调用)
[func]  GFE.draft.controller.constrain_selected_horizontal    1. (self: GFE.draft.controller) -> None
[func]  GFE.draft.controller.constrain_selected_length    1. (self: GFE.draft.controller, arg0: float) -> None
[func]  GFE.draft.controller.constrain_selected_parallel    1. (self: GFE.draft.controller, set_ref: bool) -> None
[func]  GFE.draft.controller.constrain_selected_perpendicular    1. (self: GFE.draft.controller, set_ref: bool) -> None
[func]  GFE.draft.controller.constrain_selected_tangent    1. (self: GFE.draft.controller, set_ref: bool) -> None
[func]  GFE.draft.controller.constrain_selected_vertical    1. (self: GFE.draft.controller) -> None
[func]  GFE.draft.controller.export    (疑似改模型, 未实调用)
[func]  GFE.draft.controller.fill_selected    1. (self: GFE.draft.controller) -> None
[func]  GFE.draft.controller.import_shape    (疑似改模型, 未实调用)
[func]  GFE.draft.controller.input    1. (self: GFE.draft.controller, arg0: float, arg1: float) -> None
[func]  GFE.draft.controller.input_selected    1. (self: GFE.draft.controller) -> int
[func]  GFE.draft.controller.mirror_selected    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: bool) -> None ; 2. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: bool) -> None
[func]  GFE.draft.controller.redo    1. (self: GFE.draft.controller) -> None
[func]  GFE.draft.controller.remove_selected    (疑似改模型, 未实调用)
[func]  GFE.draft.controller.rotate_selected    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: float, arg2: bool) -> None
[func]  GFE.draft.controller.round_array_selected    1. (self: GFE.draft.controller, count: int, rad: float, centre_x: float, centre_y: float) -> None
[func]  GFE.draft.controller.scale_selected    1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: float, arg2: bool) -> None
[func]  GFE.draft.controller.select_face    1. (self: GFE.draft.controller, u: float, v: float, replace: bool = True) -> None ; 2. (self: GFE.draft.controller, umin: float, umax: float, vmin: float, vmax: float, replace: bool = True) -> None
[func]  GFE.draft.controller.select_line    1. (self: GFE.draft.controller, u: float, v: float, replace: bool = True) -> None ; 2. (self: GFE.draft.controller, umin: float, umax: float, vmin: float, vmax: float, replace: bool = True) -> None
[func]  GFE.draft.controller.select_point    1. (self: GFE.draft.controller, u: float, v: float, replace: bool = True) -> None ; 2. (self: GFE.draft.controller, umin: float, umax: float, vmin: float, vmax: float, replace: bool = True) -> None
[func]  GFE.draft.controller.select_snaped    1. (self: GFE.draft.controller, arg0: bool) -> None
[func]  GFE.draft.controller.set_constrain_value    1. (self: GFE.draft.controller, arg0: float) -> None
[func]  GFE.draft.controller.set_copy_transform    1. (self: GFE.draft.controller, arg0: bool) -> None
[func]  GFE.draft.controller.set_normal    1. (self: GFE.draft.controller, arg0: int) -> None ; 2. (self: GFE.draft.controller, arg0: Vec3D, arg1: Vec3D, arg2: Vec3D) -> None
[func]  GFE.draft.controller.set_operate_mode    1. (self: GFE.draft.controller, arg0: GFE::Draft::DraftController::OpMode) -> None ; 2. (self: GFE.draft.controller, arg0: int) -> None
[func]  GFE.draft.controller.set_snap_object    1. (self: GFE.draft.controller, arg0: list[bool]) -> None ; 2. (self: GFE.draft.controller, arg0: GFE::Draft::DraftController::SnapObjMode) -> None ; 3. (self: GFE.draft.controller, arg0: int) -> None
[func]  GFE.draft.controller.set_snap_tolerance    1. (self: GFE.draft.controller, arg0: float) -> None
[func]  GFE.draft.controller.snap_object    1. (self: GFE.draft.controller, arg0: float, arg1: float) -> None ; 2. (self: GFE.draft.controller, arg0: float, arg1: float, arg2: float, arg3: float) -> None
[func]  GFE.draft.controller.split_selected    1. (self: GFE.draft.controller) -> None
[func]  GFE.draft.controller.translate_selected    1. (self: GFE.draft.controller, begin: Annotated[list[float], FixedSize(2)], end: Annotated[list[float], FixedSize(2)], copy: bool = False) -> None ; 2. (self: GFE.draft.controller, vector: Annotated[list[float], FixedSize(2)], copy: bool = False) -> None
[func]  GFE.draft.controller.undo    1. (self: GFE.draft.controller) -> None
[func]  GFE.draft.get_current    () -> GFE.draft.controller
[mod]   GFE.geometry
[mod]   GFE.geometry.contact_pair
[func]  GFE.geometry.contact_pair.search_edge    1. (master shape: TopoDS_Shape, slave shape: TopoDS_Shape, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]] ; 2. (master shape: str, slave shape: str, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]]
[func]  GFE.geometry.contact_pair.search_face    1. (master shape: TopoDS_Shape, slave shape: TopoDS_Shape, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]] ; 2. (master shape: str, slave shape: str, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]]
[mod]   GFE.geometry.geoprim
[class] GFE.geometry.geoprim.builder
[func]  GFE.geometry.geoprim.builder.common    1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape]) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str]) -> bool
[func]  GFE.geometry.geoprim.builder.cut    1. (self: GFE.geometry.geoprim.builder, shape_be_cut: TopoDS_Shape, shapes_to_cut: list[TopoDS_Shape]) -> TopoDS_Shape ; 2. (self: GFE.geometry.geoprim.builder, name_be_cut: str, names_to_cut: list[str], remove origin: bool = False) -> bool
[func]  GFE.geometry.geoprim.builder.extrude    1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: Annotated[list[float], FixedSize(3)]) -> list[TopoDS_Shape]
[func]  GFE.geometry.geoprim.builder.make_array    1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: int, arg2: int, arg3: int, arg4: Annotated[list[float], FixedSize(3)]) -> list[TopoDS_Shape]
[func]  GFE.geometry.geoprim.builder.make_round_array    1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: int, arg2: float, arg3: Annotated[list[float], FixedSize(3)], arg4: Annotated[list[float], FixedSize(3)]) -> list[TopoDS_Shape]
[func]  GFE.geometry.geoprim.builder.merge    1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape]) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], replace_set: bool = False) -> bool
[func]  GFE.geometry.geoprim.builder.redo    1. (self: GFE.geometry.geoprim.builder) -> None
[func]  GFE.geometry.geoprim.builder.revolve    1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: Annotated[list[float], FixedSize(3)], arg2: Annotated[list[float], FixedSize(3)], arg3: float) -> list[TopoDS_Shape]
[func]  GFE.geometry.geoprim.builder.rotate    1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], axis_loc: Annotated[list[float], FixedSize(3)], axis_dir: Annotated[list[float], FixedSize(3)], angle: float, copy: bool = False) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], axis_loc: Annotated[list[float], FixedSize(3)], axis_dir: Annotated[list[float], FixedSize(3)], angle: float, copy: bool = False) -> int
[func]  GFE.geometry.geoprim.builder.scale    1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], factor: float, copy: bool = False) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], factor: float, copy: bool = False) -> int ; 3. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], centre: Annotated[list[float], FixedSize(3)], factor: float, copy: bool = False) -> list[TopoDS_Shape] ; 4. (self: GFE.geometry.geoprim.builder, names: list[str], centre: Annotated[list[float], FixedSize(3)], factor: float, copy: bool = False) -> int
[func]  GFE.geometry.geoprim.builder.split    1. (self: GFE.geometry.geoprim.builder, shape_be_splitted: TopoDS_Shape, shapes_to_split: list[TopoDS_Shape]) -> TopoDS_Shape ; 2. (self: GFE.geometry.geoprim.builder, name_be_splitted: str, names_to_split: list[str], remove origin: bool = False) -> bool
[func]  GFE.geometry.geoprim.builder.translate    1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], vector: Annotated[list[float], FixedSize(3)], copy: bool = False) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], vector: Annotated[list[float], FixedSize(3)], copy: bool = False) -> int
[func]  GFE.geometry.geoprim.builder.undo    1. (self: GFE.geometry.geoprim.builder) -> None
[func]  GFE.geometry.geoprim.set_tolerance_limit    1. (arg0: float) -> None
[mod]   GFE.geometry.geotool
[func]  GFE.geometry.geotool.centre_of_mass    1. (arg0: TopoDS_Shape) -> Vec3D
[func]  GFE.geometry.geotool.children    1. (arg0: TopoDS_Shape) -> list[TopoDS_Shape] ; 2. (arg0: TopoDS_Shape, arg1: int) -> list[TopoDS_Shape]
[func]  GFE.geometry.geotool.get_id_by_shape    1. (arg0: TopoDS_Shape) -> Annotated[list[int], FixedSize(3)]
[func]  GFE.geometry.geotool.get_selected_shape    1. (arg0: TopAbs_ShapeEnum) -> list[TopoDS_Shape]
[func]  GFE.geometry.geotool.get_selected_shape_id    1. (arg0: TopAbs_ShapeEnum) -> list[Annotated[list[int], FixedSize(3)]]
[func]  GFE.geometry.geotool.get_shape_box    1. (arg0: TopoDS_Shape, arg1: float) -> Bnd_Box
[func]  GFE.geometry.geotool.get_shape_box_range    1. (arg0: TopoDS_Shape, arg1: float) -> Annotated[list[float], FixedSize(6)]
[func]  GFE.geometry.geotool.get_shape_by_id    1. (arg0: int, arg1: int, arg2: int) -> TopoDS_Shape
[func]  GFE.geometry.geotool.insidebox    1. (arg0: TopoDS_Shape, arg1: Bnd_Box) -> bool
[func]  GFE.geometry.geotool.make_compound    1. (arg0: list[TopoDS_Shape], arg1: bool) -> TopoDS_Shape
[mod]   GFE.geometry.mesh_generator
[class] GFE.geometry.mesh_generator.controller
[prop]  GFE.geometry.mesh_generator.controller.auto_transfinite
[prop]  GFE.geometry.mesh_generator.controller.generate_dim
[prop]  GFE.geometry.mesh_generator.controller.geom_to_type
[prop]  GFE.geometry.mesh_generator.controller.number_option
[func]  GFE.geometry.mesh_generator.controller.set_approximate_size    1. (self: GFE.geometry.mesh_generator.controller, arg0: float) -> None
[func]  GFE.geometry.mesh_generator.controller.set_as_default    1. (self: GFE.geometry.mesh_generator.controller) -> None
[prop]  GFE.geometry.mesh_generator.controller.size_option
[prop]  GFE.geometry.mesh_generator.controller.string_option
[prop]  GFE.geometry.mesh_generator.controller.sweep_option
[prop]  GFE.geometry.mesh_generator.controller.user_option
[class] GFE.geometry.mesh_generator.curve_control
[prop]  GFE.geometry.mesh_generator.curve_control.count
[prop]  GFE.geometry.mesh_generator.curve_control.density
[prop]  GFE.geometry.mesh_generator.curve_control.edges
[prop]  GFE.geometry.mesh_generator.curve_control.set_name
[class] GFE.geometry.mesh_generator.generator
[func]  GFE.geometry.mesh_generator.generator.mesh    (疑似改模型, 未实调用)
[class] GFE.geometry.mesh_generator.gmsh_control
[class] GFE.geometry.mesh_generator.sweep_control
[prop]  GFE.geometry.mesh_generator.sweep_control.body
[prop]  GFE.geometry.mesh_generator.sweep_control.dx
[prop]  GFE.geometry.mesh_generator.sweep_control.dy
[prop]  GFE.geometry.mesh_generator.sweep_control.dz
[prop]  GFE.geometry.mesh_generator.sweep_control.layers
[prop]  GFE.geometry.mesh_generator.sweep_control.ratio
[prop]  GFE.geometry.mesh_generator.sweep_control.recomb_lateral
[prop]  GFE.geometry.mesh_generator.sweep_control.recomb_source
[prop]  GFE.geometry.mesh_generator.sweep_control.source
[prop]  GFE.geometry.mesh_generator.sweep_control.target
[mod]   GFE.io
[func]  GFE.io.get_current    () -> GFE.io.instance
[mod]   GFE.io.inpio
[class] GFE.io.inpio.writer
[func]  GFE.io.inpio.writer.perform    1. (self: GFE.io.inpio.writer) -> bool
[func]  GFE.io.inpio.writer.set_case    1. (self: GFE.io.inpio.writer, arg0: str) -> None
[func]  GFE.io.inpio.writer.set_trainload2inpx    1. (self: GFE.io.inpio.writer, arg0: bool) -> None
[class] GFE.io.instance
[func]  GFE.io.instance.import_yjk    (疑似改模型, 未实调用)
[func]  GFE.io.instance.open_dwg    1. (self: GFE.io.instance, u8path: str, parameter: list[int]) -> None
[func]  GFE.io.instance.open_inp    1. (self: GFE.io.instance, u8path: str) -> bool
[func]  GFE.io.instance.open_pre    1. (self: GFE.io.instance, u8path: str, merge: bool = False, prefix: str = 'Part') -> bool
[mod]   GFE.occ
[attr]  GFE.occ.COMPOUND = <ShapeType>
[attr]  GFE.occ.EDGE = <ShapeType>
[attr]  GFE.occ.FACE = <ShapeType>
[attr]  GFE.occ.SHAPE = <ShapeType>
[attr]  GFE.occ.SHELL = <ShapeType>
[attr]  GFE.occ.SOLID = <ShapeType>
[enum]  GFE.occ.ShapeType  = VERTEX, EDGE, WIRE, FACE, SHELL, SOLID, COMPOUND, SHAPE
[attr]  GFE.occ.VERTEX = <ShapeType>
[attr]  GFE.occ.WIRE = <ShapeType>
[class] GFE.occ.box
[func]  GFE.occ.box.enlarge    1. (self: GFE.occ.box, arg0: float) -> None
[mod]   GFE.occ.brep_prim
[func]  GFE.occ.brep_prim.make_box    1. (dx: float, dy: float, dz: float) -> GFE.occ.shape ; 2. (pt1: Vec3D, pt2: Vec3D) -> GFE.occ.shape
[func]  GFE.occ.brep_prim.make_cone    1. (bot_r: float, h: float, top_r: float = 0) -> GFE.occ.shape
[func]  GFE.occ.brep_prim.make_cylinder    1. (r: float, h: float) -> GFE.occ.shape
[func]  GFE.occ.brep_prim.make_sphere    1. (r: float) -> GFE.occ.shape
[func]  GFE.occ.brep_prim.make_torus    1. (r1: float, r2: float) -> GFE.occ.shape
[func]  GFE.occ.brep_prim.make_wedge    1. (dx: float, dy: float, dz: float, xmin: float, xmax: float, zmin: float, zmax: float) -> GFE.occ.solid
[class] GFE.occ.compound
[func]  GFE.occ.compound.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.compound.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.edge
[func]  GFE.occ.edge.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.edge.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.face
[func]  GFE.occ.face.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.face.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.shape
[func]  GFE.occ.shape.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.shape.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.shell
[func]  GFE.occ.shell.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.shell.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.solid
[func]  GFE.occ.solid.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.solid.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.vertex
[func]  GFE.occ.vertex.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.vertex.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[class] GFE.occ.wire
[func]  GFE.occ.wire.is_null    1. (self: GFE.occ.shape) -> bool
[func]  GFE.occ.wire.is_same    1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool
[mod]   GFE.soil
[class] GFE.soil.box_builder
[func]  GFE.soil.box_builder.build    1. (self: GFE.soil.box_builder) -> list[list[TopoDS_Shape]]
[func]  GFE.soil.box_builder.perform    1. (self: GFE.soil.box_builder) -> list[list[TopoDS_Shape]]
[func]  GFE.soil.box_builder.set_height    1. (self: GFE.soil.box_builder, height: list[float], depth: int) -> None
[func]  GFE.soil.box_builder.set_parameter    1. (self: GFE.soil.box_builder, length: float, width: float) -> None
[class] GFE.soil.data_builder
[func]  GFE.soil.data_builder.build    1. (self: GFE.soil.data_builder) -> bool
[prop]  GFE.soil.data_builder.dimension
[prop]  GFE.soil.data_builder.layer_material
[prop]  GFE.soil.data_builder.layer_shape
[prop]  GFE.soil.data_builder.name
[func]  GFE.soil.data_builder.perform    1. (self: GFE.soil.data_builder) -> bool
