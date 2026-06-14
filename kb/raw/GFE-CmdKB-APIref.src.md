# GFE 命令流 API 速查（787 函数）
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本，2026-06-10 Fable 二审后刷新（ADR-0001：派生快照随主库可变）。

# GFE 命令流 API 权威速查 (自省 1607 符号 + RTTI 453 类；数据源含 787 函数全签名，本页显式收录 259 条专有函数 + 通用 CRUD 见"通用模式"节)
数据源: gfe_api_spec.txt + gfe_mutating_sigs.txt(78改模型函数, 位于 D:\GFE\gfe_mutating_sigs.txt, 不在本目录) + gfe_cpp_classes.txt

## 通用模式
- 管理器单例: 对象管理器模块（GFE.Pre 下 amplitude/material/set/step 等）`X_mgr()` 返回绑定当前文档的单例；document/draft/io 用 current_document()/get_current()，geoprim/soil 用 builder 类，occ.brep_prim/geotool/contact_pair 为模块级函数
- 建模套路: 构造对象 -> 设属性(def_readwrite 字段) -> `mgr.add(obj, inner=False, auto_name=False)`
- 标准 CRUD(所有 mgr 共有): `activate`, `auto_name`, `contains`, `contains_all`, `contains_hidden`, `count`, `count_all`, `count_hidden`, `delete`, `delete_all`, `is_active`, `name_all`, `name_hidden`, `name_list`, `rename`, `valid_tag`
- 标准 CRUD 16 函数签名表（所有 mgr 通用，一次性给出，self 均为 generic_mgr.generic）:
  | 函数 | 签名 | 备注 |
  |---|---|---|
  | activate | `(arg0: str, arg1: bool) -> None` | ⚠第二参 bool 必填 |
  | auto_name | `(prefix: str, has0: bool = False) -> str` / `(arg0: obj) -> str` | 两个重载 |
  | contains / contains_all / contains_hidden | `(arg0: str) -> bool` | |
  | count / count_all / count_hidden | `() -> int` | |
  | delete | `(arg0: list[str]) -> None` | ⚠参数是 list[str] 不是单个 str，`delete("Name")` 会错 |
  | delete_all | `() -> None` | |
  | is_active | `(arg0: str) -> bool` | |
  | name_all / name_hidden / name_list | `() -> list[str]` | |
  | rename | `(arg0: str, arg1: str) -> OCC_GenericMgr2::ErrCode` | ⚠返回类型特殊 |
  | valid_tag | `(arg0: bool) -> set[int]` | |
- err_code: UNDEFINED/SUCCESS/NAME_REPEATED/NAME_ILLEGAL/CHILD_NOT_EXIST/MISS_REFERENCE


---
## GFE.Pre.amplitude
**类**: amp_mgr, amp_mgr.status, amplitude, manager

**`amp_mgr`**
- `add` 1. (self: GFE.Pre.amplitude.manager, obj: GFE::Function, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.amplitude.manager, obj: GFE::Function, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.amplitude.manager, obj: GFE::Function) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.amplitude.manager, obj: GFE::Function) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.amplitude.manager, arg0: str) -> GFE::Function

**`amp_mgr.status`**
- 属性: `CODE`, `MESSAGE`

**`amplitude`**
- 属性: `gravity`, `name`, `spectrum_type`, `type`, `value`

**枚举**:
- `amp_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.artbc
**类**: art_bc, artbc_mgr, artbc_mgr.status, manager

**`art_bc`**
- 属性: `center`, `centered`, `name`, `structure`, `surface`

**`artbc_mgr`**
- `add` 1. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.artbc.manager, obj: GFE::ArtBC) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.artbc.manager, arg0: str) -> GFE::ArtBC

**枚举**:
- `artbc_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.boundary
**类**: bc_mgr, bc_mgr.status, boundary, generic_bc, manager

**`bc_mgr`**
- `add` 1. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.boundary.manager, obj: GFE::GenericBC) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.boundary.manager, arg0: str) -> GFE::GenericBC

**`boundary`**
- 属性: `amplitude`, `amplitude_im`, `distribution`, `has_if`, `if_acce`, `if_acce_path`, `if_force`, `if_grade`, `if_itv`, `if_mode`, `if_param`, `if_tot`, `name`, `set`, `track_coord`, `track_id`, `type`, `valid_dof`, `value`, `value_im`

**`generic_bc`**
- 属性: `name`, `type`

**枚举**:
- `bc_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.case
**类**: case, case_mgr, case_mgr.status, manager

**`case`**
- 属性: `name`, `steps`
- `set_artbc` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_bcs` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_elemAdd` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_elemDel` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_fieldReqs` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_histReqs` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_initialConditions` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None
- `set_vload` 1. (self: GFE.Pre.case.case, arg0: str, arg1: list[str]) -> None

**`case_mgr`**
- `add` 1. (self: GFE.Pre.case.manager, obj: GFE::Case, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.case.manager, obj: GFE::Case, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.case.manager, obj: GFE::Case) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.case.manager, obj: GFE::Case) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.case.manager, arg0: str) -> GFE::Case

**枚举**:
- `case_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.document
**类**: application, document

**`(mod)`**
- `current_document` () -> GFE.Pre.document.document
- `get_document` 1. (arg0: int) -> GFE.Pre.document.document
- `set_application` 1. (arg0: GFE.Pre.document.application) -> None
- `set_application_by_ui` 1. () -> None
- `set_current` 1. (arg0: GFE.Pre.document.document) -> bool

---
## GFE.Pre.field
**类**: discrete_field, expression_field, field_manager, field_manager.status, field_mgr

**`discrete_field`**
- 属性: `datatype`, `default`, `field`, `id`, `name`, `type`

**`expression_field`**
- 属性: `expression`, `name`

**`field_manager`**
- `add` 1. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.field.field_manager, obj: GFE::Pre::Field) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.field.field_manager, arg0: str) -> GFE::Pre::Field

**枚举**:
- `field_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.geometry
**类**: geo_mgr, geo_mgr.status, manager, object

**`geo_mgr`**
- `add` 1. (self: GFE.Pre.geometry.manager, arg0: str, arg1: TopoDS_Shape) -> tuple[GFE::Geometry, generic_mgr.generic.err_code]
- `find` 1. (self: GFE.Pre.geometry.manager, arg0: str) -> GFE::Geometry ; 2. (self: GFE.Pre.geometry.manager, arg0: int) -> GFE::Geometry

**`object`**
- 属性: `name`
- `id` 1. (self: GFE.Pre.geometry.object) -> int
- `shape` 1. (self: GFE.Pre.geometry.object) -> TopoDS_Shape

**枚举**:
- `geo_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.initial_condition
**类**: InitGeostaticStress, InitPorePress, InitRatio, InitSaturation, InitStress, InitTemperature, InitVelocity, InitialCondition, ic_mgr, ic_mgr.status, manager

**`InitGeostaticStress`**
- 属性: `name`, `set_name`, `value`

**`InitPorePress`**
- 属性: `is_constant`, `name`, `set_name`, `value`

**`InitRatio`**
- 属性: `is_constant`, `name`, `set_name`, `value`

**`InitSaturation`**
- 属性: `name`, `saturation`, `set_name`

**`InitStress`**
- 属性: `distribution`, `name`, `set_name`, `value`

**`InitTemperature`**
- 属性: `dis_field`, `name`, `set_name`, `value`

**`InitVelocity`**
- 属性: `distribution`, `name`, `set_name`, `valid_dof`, `value`

**`InitialCondition`**
- 属性: `name`, `set_name`

**`ic_mgr`**
- `add` 1. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.initial_condition.manager, obj: GFE.Pre.initial_condition.InitialCondition) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.initial_condition.manager, arg0: str) -> GFE.Pre.initial_condition.InitialCondition

**枚举**:
- `ic_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.interaction
**类**: conn_beh_mgr, conn_beh_mgr.status, conn_prop_mgr, conn_prop_mgr.status, connector_base, connector_behavior, connector_behavior_manager, connector_damping, connector_elastic, connector_plastic, connector_property_manager, connector_section, contact, contact_manager, contact_manager.status, contact_mgr, embed, embed_manager, embed_manager.status, embed_mgr, general_section, incident_wave, incident_wave_manager, incident_wave_manager.status, incident_wave_property, incident_wave_property_manager, incident_wave_property_manager.status, iw_mgr, iw_prop_mgr, mpc, mpc_manager, mpc_manager.status, mpc_mgr, rigid_body, rigid_manager, rigid_manager.status, rigid_mgr, sd_mgr, sd_mgr.status, spec_mgr, spec_mgr.status, special_interaction, special_manager, spring_dashpot, spring_dashpot_manager, surface_pair, tie_manager, tie_manager.status, tie_mgr

**`conn_beh_mgr`**
- `add` 1. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_behavior_manager, obj: GFE.Pre.interaction.connector_behavior) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.connector_behavior_manager, arg0: str) -> Optional[GFE.Pre.interaction.connector_behavior]

**`conn_prop_mgr`**
- `add` 1. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.connector_property_manager, obj: GFE.Pre.interaction.connector_section) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.connector_property_manager, arg0: str) -> GFE.Pre.interaction.connector_section

**`connector_behavior`**
- 属性: `behaviors`, `name`

**`connector_damping`**
- 属性: `component`, `type`, `values`

**`connector_elastic`**
- 属性: `component`, `compressive_stiffness`, `rigid`, `tensile_stiffness`

**`connector_plastic`**
- 属性: `component`, `kh_define`, `kh_values`

**`connector_section`**
- 属性: `behavior`, `connector_type`, `material`, `name`, `orientation`, `orientation2`, `set_name`

**`contact`**
- 属性: `damageEvolution`, `damageInitiation`, `friction`, `isCohesive`, `name`, `power`, `surface`, `type`

**`contact_manager`**
- `add` 1. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.contact_manager, obj: GFE.Pre.interaction.contact) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.contact_manager, arg0: str) -> GFE.Pre.interaction.contact

**`embed`**
- 属性: `embedded_names`, `exterior_tolerance`, `host_name`, `id`, `name`, `roundoff_tolerance`

**`embed_manager`**
- `add` 1. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.embed_manager, obj: GFE::Embed) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.embed_manager, arg0: str) -> GFE::Embed

**`general_section`**
- 属性: `material`, `set_name`

**`incident_wave`**
- 属性: `id`, `is_node_set`, `mag_scale_factor`, `name`, `node_id`, `prop_name`, `set_name`, `surf_name`, `time_detonation`

**`incident_wave_manager`**
- `add` 1. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_manager, obj: GFE::IncidentWave) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.incident_wave_manager, arg0: str) -> GFE::IncidentWave

**`incident_wave_property`**
- 属性: `data`, `def`, `id`, `name`

**`incident_wave_property_manager`**
- `add` 1. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.incident_wave_property_manager, obj: GFE::IncidentWaveProperty) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.incident_wave_property_manager, arg0: str) -> GFE::IncidentWaveProperty

**`mpc`**
- 属性: `name`, `ref_node`, `set_name`, `type`

**`mpc_manager`**
- `add` 1. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.mpc_manager, obj: GFE.Pre.interaction.mpc) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.mpc_manager, arg0: str) -> GFE.Pre.interaction.mpc

**`rigid_body`**
- 属性: `density`, `id`, `name`, `ref_node`, `ref_set`, `set_name`, `thickness`, `type`

**`rigid_manager`**
- `add` 1. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.rigid_manager, obj: GFE::RigidBody) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.rigid_manager, arg0: str) -> GFE::RigidBody

**`sd_mgr`**
- `add` 1. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.spring_dashpot_manager, obj: GFE::SpringDashpot) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.spring_dashpot_manager, arg0: str) -> GFE::SpringDashpot

**`spec_mgr`**
- `add` 1. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.special_manager, obj: GFE::SpecialInteraction) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.special_manager, arg0: str) -> GFE::SpecialInteraction

**`special_interaction`**
- 属性: `name`, `namelist`, `parameters`, `type`

**`spring_dashpot`**
- 属性: `coefficient`, `dof`, `dof2`, `id`, `name`, `nodes`, `nset`, `nset2`, `orientation`, `stiffness`, `type`

**`surface_pair`**
- 属性: `first_surf`, `name`, `param_number`, `parameters`, `second_surf`, `type`

**`tie_manager`**
- `add` 1. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.interaction.tie_manager, obj: GFE::SurfacePair) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.interaction.tie_manager, arg0: str) -> GFE::SurfacePair

**枚举**:
- `conn_beh_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `conn_prop_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `contact_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `embed_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `incident_wave_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `incident_wave_property_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `mpc_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `rigid_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `sd_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `spec_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `tie_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.material
**类**: bed_coefficient, concrete_damaged, creep, damping, density, elastic, expansion, hyperelastic, hyperfoam, manager, manager.status, mat_general, mat_mgr, mat_permeability, mat_sorption, material, mohr_coulomb, plastic, porous_bulk_moduli, rate_dependent, test_data, user, viscoelastic

**`bed_coefficient`**
- 属性: `kh`, `kv`

**`concrete_damaged`**
- 属性: `comp_damage`, `comp_harden`, `comp_recov`, `has_jc_rate`, `jc_rate_C`, `jc_rate_Ep0_dot1`, `n_comp_damage`, `n_comp_harden`, `n_plasticity`, `n_tens_damage`, `n_tens_stiff`, `plasticity`, `tens_damage`, `tens_recov`, `tens_stiff`

**`creep`**
- 属性: `data`, `law`, `nRow`, `time`

**`damping`**
- 属性: `n_param`, `params`

**`density`**
- 属性: `n_param`, `params`, `temp_dp`

**`elastic`**
- 属性: `compression`, `moduli_time_scale`, `n_param`, `params`, `temp_dp`, `tension`, `type`

**`expansion`**
- 属性: `sub_type`, `value`

**`hyperelastic`**
- 属性: `N`, `biaxial`, `has_poisson`, `he_type`, `moduli_time_scale`, `params`, `planar`, `poisson`, `temp_dp`, `test_data`, `uniaxial`, `volumetric`

**`hyperfoam`**
- 属性: `N`, `biaxial`, `moduli_time_scale`, `params`, `planar`, `simple_shear`, `temp_dp`, `test_data`, `uniaxial`, `volumetric`

**`manager`**
- `add` 1. (self: GFE.Pre.material.manager, obj: GFE::Material, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.material.manager, obj: GFE::Material, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.material.manager, obj: GFE::Material) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.material.manager, obj: GFE::Material) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.material.manager, arg0: str) -> GFE::Material

**`mat_permeability`**
- 属性: `entities`

**`mat_sorption`**
- 属性: `entities`

**`material`**
- 属性: `entries`, `name`
- `as_elastic` 1. (self: GFE.Pre.material.material, rou: float, e: float, nu: float) -> None

**`mohr_coulomb`**
- 属性: `cohesion`, `n_cohesion`, `n_plasticity`, `plasticity`

**`plastic`**
- 属性: `harden_type`, `has_jc_rate`, `jc_rate_C`, `jc_rate_Ep0_dot1`, `params`, `rate_dp`, `temp_dp`

**`porous_bulk_moduli`**
- 属性: `permeating_fluid`, `solid_grains`

**`rate_dependent`**
- 属性: `sub_type`, `value`

**`test_data`**
- 属性: `n_test_data`, `test_data`

**`user`**
- 属性: `constants`, `n_constants`, `user_type`

**`viscoelastic`**
- 属性: `n_param`, `params`, `type`

**枚举**:
- `entry_type` = Density, Elastic, Plastic, HyperFoam, HyperElastic, Damping, ViscoElastic, ConcreteDamaged, MohrCoulomb, User, TestData, Creep, Permeability, PorousBulkModuli, Sorption, Expansion, BedCoefficient, RateDependent
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.mesh
**类**: element, manager, manager.status, mesh_data, mesh_mgr, mesh_obj, node

**`element`**
- 属性: `eid`, `node_size`, `nodes`, `state`, `sub_type`

**`manager`**
- `add` 1. (self: GFE.Pre.mesh.manager, arg0: str, arg1: GFE::Pre::Gfe_MeshData) -> tuple[GFE::MeshObj, generic_mgr.generic.err_code] ; 2. (self: GFE.Pre.mesh.manager, arg0: str, arg1: float, arg2: float, arg3: float) -> tuple[GFE::MeshObj, generic_mgr.generic.err_code]
- `find` 1. (self: GFE.Pre.mesh.manager, arg0: str) -> GFE::MeshObj ; 2. (self: GFE.Pre.mesh.manager, arg0: int) -> GFE::MeshObj
- `update` 1. (self: GFE.Pre.mesh.manager, arg0: str, arg1: GFE::Pre::Gfe_MeshData) -> None ; 2. (self: GFE.Pre.mesh.manager, arg0: int, arg1: GFE::Pre::Gfe_MeshData) -> None

**`mesh_data`**
- `add_element` 1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> tuple[int, bool] ; 2. (self: GFE.Pre.mesh.mesh_data, arg0: list[GFE.Pre.mesh.element]) -> tuple[int, bool]
- `add_node` 1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.node) -> tuple[int, bool] ; 2. (self: GFE.Pre.mesh.mesh_data, arg0: list[GFE.Pre.mesh.node]) -> tuple[int, bool]
- `get_element` 1. (self: GFE.Pre.mesh.mesh_data, eid: int) -> GFE.Pre.mesh.element
- `get_element_subtype` 1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> int ; 2. (self: GFE.Pre.mesh.mesh_data, eid: int) -> int
- `get_element_surface` 1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> list[int] ; 2. (self: GFE.Pre.mesh.mesh_data, arg0: int) -> list[int] ; 3. (self: GFE.Pre.mesh.mesh_data, element: GFE.Pre.mesh.element, face_id: int) -> list[int] ; 4. (self: GFE.Pre.mesh.mesh_data, eid: int, face_id: int) -> list[int]
- `get_element_type` 1. (self: GFE.Pre.mesh.mesh_data, arg0: GFE.Pre.mesh.element) -> int ; 2. (self: GFE.Pre.mesh.mesh_data, eid: int) -> int
- `get_node` 1. (self: GFE.Pre.mesh.mesh_data, nid: int) -> GFE.Pre.mesh.node
- `rebuild_surface` 1. (self: GFE.Pre.mesh.mesh_data) -> bool
- `remove_element` 1. (self: GFE.Pre.mesh.mesh_data, eid: int) -> bool

**`mesh_obj`**
- 属性: `doc`, `label`, `mesh_data`
- `each_et_elems` 1. (self: GFE.Pre.mesh.mesh_obj) -> QMap<QString,QVariant>
- `each_et_nodes` 1. (self: GFE.Pre.mesh.mesh_obj) -> QMap<QString,QVariant>
- `element_data` 1. (self: GFE.Pre.mesh.mesh_obj) -> tuple[list[int], list[int]]
- `et_elems` 1. (self: GFE.Pre.mesh.mesh_obj, arg0: str) -> list[int]
- `et_elems_by_id` 1. (self: GFE.Pre.mesh.mesh_obj, arg0: int, arg1: int) -> list[int]
- `et_nodes` 1. (self: GFE.Pre.mesh.mesh_obj, arg0: str) -> list[int]
- `et_nodes_by_id` 1. (self: GFE.Pre.mesh.mesh_obj, arg0: int, arg1: int) -> list[int]
- `geo_obj` 1. (self: GFE.Pre.mesh.mesh_obj) -> GFE.Pre.geometry.object
- `get_node_coordinate` 1. (self: GFE.Pre.mesh.mesh_obj, arg0: int) -> Optional[Vec3D]
- `id` 1. (self: GFE.Pre.mesh.mesh_obj) -> int
- `is_valid` 1. (self: GFE.Pre.mesh.mesh_obj) -> bool
- `mesh` 1. (self: GFE.Pre.mesh.mesh_obj) -> GFE.Pre.mesh.mesh_data
- `name` 1. (self: GFE.Pre.mesh.mesh_obj) -> str
- `node_data` 1. (self: GFE.Pre.mesh.mesh_obj) -> tuple[list[int], list[Vec3D]]
- `prs` 1. (self: GFE.Pre.mesh.mesh_obj) -> TPrsStd_AISPresentation
- `transformation` 1. (self: GFE.Pre.mesh.mesh_obj) -> gp_Trsf

**`node`**
- 属性: `nid`, `xyz`

**枚举**:
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.orientation
**类**: manager, manager.status, orientation, orientation_mgr

**`manager`**
- `add` 1. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.orientation.manager, obj: GFE::Pre::Orientation) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.orientation.manager, arg0: str) -> GFE::Pre::Orientation

**`orientation`**
- 属性: `data`, `definition`, `name`, `type`

**枚举**:
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.output
**类**: contact_output, element_output, energy_output, field_mgr, field_mgr.status, history_mgr, history_mgr.status, integrated_output, node_output, out_req_mgr, out_req_mgr.status, output_request, sub_output

**`contact_output`**
- 属性: `general_contact`, `name`, `reg_type`, `surface`, `var_option`, `variables`

**`element_output`**
- 属性: `elset`, `name`, `reg_type`, `var_option`, `variables`

**`energy_output`**
- 属性: `elset`, `name`, `per_element_set`, `reg_type`, `var_option`, `variables`

**`field_mgr`**
- `add` 1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.output.out_req_mgr, nameFind a GFE::Pre::OutputRequest by name: str) -> GFE::Pre::OutputRequest ⚠自省伪迹：参数实名 name（docstring 混入参数名）
- `find_all` 1. (self: GFE.Pre.output.out_req_mgr) -> list[GFE::Pre::OutputRequest]

**`history_mgr`**
- `add` 1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.output.out_req_mgr, nameFind a GFE::Pre::OutputRequest by name: str) -> GFE::Pre::OutputRequest ⚠自省伪迹：参数实名 name（docstring 混入参数名）
- `find_all` 1. (self: GFE.Pre.output.out_req_mgr) -> list[GFE::Pre::OutputRequest]

**`integrated_output`**
- 属性: `elset`, `name`, `reg_type`, `surface`, `var_option`, `variables`

**`node_output`**
- 属性: `name`, `nset`, `reg_type`, `var_option`, `variables`

**`out_req_mgr`**
- `add` 1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.output.out_req_mgr, obj: GFE::Pre::OutputRequest) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.output.out_req_mgr, nameFind a GFE::Pre::OutputRequest by name: str) -> GFE::Pre::OutputRequest ⚠自省伪迹：参数实名 name（docstring 混入参数名）
- `find_all` 1. (self: GFE.Pre.output.out_req_mgr) -> list[GFE::Pre::OutputRequest]

**`output_request`**
- 属性: `frequency`, `method`, `name`, `number_interval`, `step`, `sub_output`, `time_interval`, `time_points`, `time_type`, `type`, `var_option`

**`sub_output`**
- 属性: `name`, `reg_type`, `var_option`, `variables`

**枚举**:
- `field_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `history_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `out_req_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.section
**类**: manager, manager.status, property, property_beam, property_beam_general, property_bush, property_membrane, property_shell, property_solid, rebar_layer, sect_mgr

**`manager`**
- `add` 1. (self: GFE.Pre.section.manager, obj: GFE::Property, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.section.manager, obj: GFE::Property, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.section.manager, obj: GFE::Property) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.section.manager, obj: GFE::Property) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.section.manager, arg0: str) -> GFE::Property

**`property`**
- 属性: `elset_name`, `name`, `type`

**`property_beam`**
- 属性: `direction`, `elset_name`, `fiber_num`, `mat_name`, `name`, `params`, `shape`, `shape_params`, `shear`, `type`

**`property_beam_general`**
- 属性: `axis`, `density`, `elset_name`, `name`, `param1`, `param2`, `poisson`, `type`

**`property_bush`**
- 属性: `elset_name`, `name`, `params`, `type`

**`property_membrane`**
- 属性: `elset_name`, `has_rebar`, `mat_name`, `name`, `rebar`, `thickness`, `type`

**`property_shell`**
- 属性: `elset_name`, `has_rebar`, `integral_point`, `layer_num`, `mat_name`, `name`, `params`, `rebar`, `thickness`, `type`

**`property_solid`**
- 属性: `elset_name`, `has_thickness`, `mat_name`, `name`, `thickness`, `type`

**`rebar_layer`**
- 属性: `layer_name`, `mat_name`, `orientation_name`, `params`, `rebar_geometry`, `rebar_num`

**枚举**:
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.set
**类**: basic_set, elset, elset_manager, elset_manager.status, elset_mgr, gset, gset_manager, gset_manager.status, gset_mgr, nset, nset_manager, nset_manager.status, nset_mgr

**`basic_set`**
- 属性: `name`
- `add_attribute` 1. (self: GFE.Pre.set.gset, arg0: int, arg1: bool) -> None
- `get_shapes` 1. (self: GFE.Pre.set.basic_set) -> list[TopoDS_Shape]
- `get_shapes_id` 1. (self: GFE.Pre.set.basic_set) -> list[Annotated[list[int], FixedSize(3)]]
- `set_shapes` 1. (self: GFE.Pre.set.basic_set, arg0: list[TopoDS_Shape]) -> None
- `set_shapes_id` 1. (self: GFE.Pre.set.basic_set, arg0: list[Annotated[list[int], FixedSize(3)]]) -> None

**`elset`**
- 属性: `data`, `name`, `unsort`

**`elset_manager`**
- `add` 1. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.elset_manager, obj: GFE::Pre::ElSet) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.set.elset_manager, arg0: str) -> GFE::Pre::ElSet

**`gset`**
- 属性: `name`
- `add_attribute` 1. (self: GFE.Pre.set.gset, arg0: int, arg1: bool) -> None

**`gset_manager`**
- `add` 1. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 3. (self: GFE.Pre.set.gset_manager, name: str, shapes: list[TopoDS_Shape], hidden: bool = False, auto name: bool = False) -> generic_mgr.generic.status ; 4. (self: GFE.Pre.set.gset_manager, name: str, shapes: list[Annotated[list[int], FixedSize(3)]], hidden: bool = False, auto name: bool = False) -> generic_mgr.generic.status ⚠自省伪迹：参数实名 auto_name（无空格）
- `edit` 1. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.gset_manager, obj: GFE::Pre::GSet) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.set.gset_manager, arg0: str) -> GFE::Pre::GSet

**`nset`**
- 属性: `data`, `name`, `unsort`

**`nset_manager`**
- `add` 1. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.set.nset_manager, obj: GFE::Pre::NSet) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.set.nset_manager, arg0: str) -> GFE::Pre::NSet

**枚举**:
- `elset_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `gset_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `nset_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.soil
**类**: manager, manager.status, soil, soil_manager, soil_mgr

**`manager`**
- `add` 1. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.soil.soil_manager, obj: GFE::Pre::Soil1D) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.soil.soil_manager, arg0: str) -> GFE::Pre::Soil1D

**`soil`**
- 属性: `bedrock_mat`, `depth`, `depth_dir`, `materials`, `name`

**枚举**:
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.sph
**类**: sph_manager, sph_manager.status, sph_mgr

**`sph_manager`**
- `add` 1. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.sph.sph_manager, obj: GFE::Pre::SPH) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.sph.sph_manager, arg0: str) -> GFE::Pre::SPH

**枚举**:
- `sph_manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.step
**类**: analysis_step, dyn_modal_damping, dynamic_explicit_step, dynamic_implicit_step, frequency_step, geo_static_step, global_damping, manager, manager.status, mass_scaling, modal_damping, modal_dynamic_step, response_spectrum_step, soils_step, sph_step, static_general_step, steady_dyn_step, step_manager, step_mgr

**`analysis_step`**
- 属性: `description`, `name`, `nlgeom`

**`dyn_modal_damping`**
- 属性: `db`, `set_name`, `values`

**`dynamic_explicit_step`**
- 属性: `description`, `mass_scaling`, `modal_damping`, `name`, `nlgeom`, `period`

**`dynamic_implicit_step`**
- 属性: `description`, `direct`, `explicit_`, `gfe_linear`, `init_inc`, `max_inc`, `min_inc`, `name`, `nlgeom`, `period`

**`frequency_step`**
- 属性: `description`, `eigen`, `name`, `nlgeom`

**`geo_static_step`**
- 属性: `description`, `init_inc`, `max_inc`, `min_inc`, `name`, `nlgeom`, `period`

**`global_damping`**
- 属性: `alpha`, `beta`, `field`, `structual`

**`manager`**
- `add` 1. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.step.step_manager, obj: GFE::Pre::AnalysisStep) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.step.step_manager, arg0: str) -> GFE::Pre::AnalysisStep

**`mass_scaling`**
- 属性: `frequency`, `region`, `target_time`, `type`

**`modal_damping`**
- 属性: `data`, `definition`, `field`, `type`

**`modal_dynamic_step`**
- 属性: `cont`, `description`, `modal_damping`, `name`, `nlgeom`, `time_increment`, `time_period`

**`response_spectrum_step`**
- 属性: `data`, `description`, `modal_damping`, `name`, `nlgeom`, `spectrum`, `sum`

**`soils_step`**
- 属性: `cetol`, `description`, `end`, `init_inc`, `is_consolidation`, `max_inc`, `min_inc`, `name`, `nlgeom`, `period`, `utol`

**`sph_step`**
- 属性: `auto_area`, `b`, `beam_sect`, `box_area`, `cflnumber`, `coefh`, `coefsound`, `description`, `distance`, `excute_para`, `gamma`, `gravity`, `h`, `hswl`, `lattice`, `massbound`, `massfluid`, `name`, `nlgeom`, `objects`, `pointref`, `rhop0`, `rhopgradient`, `shell_sect`, `speedsound`, `speedsystem`

**`static_general_step`**
- 属性: `description`, `init_inc`, `max_inc`, `min_inc`, `name`, `nlgeom`, `period`

**`steady_dyn_step`**
- 属性: `data`, `description`, `direct`, `global_damping`, `interval`, `modal_damping`, `name`, `nlgeom`, `scale`
- `get_single_points` 1. (self: GFE.Pre.step.steady_dyn_step, arg0: list[float]) -> list[float]

**枚举**:
- `StepType` = Initial, DynamicExplicit, StaticGeneral, Frequency, SteadyStateDynamics, GeoStatic, ModalDynamic2, DynamicImplicit, ResponseSpectrum2, Soils, SPH, CoupledTemp
- `global_damping_field` = All, Mechanical, Acoustic
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE
- `modal_damping_definition` = Mode, Freq
- `modal_damping_field` = All, Mechanical, Acoustic
- `modal_damping_type` = Direct, Composite, Rayleigh, Structural

---
## GFE.Pre.surface
**类**: element_surface, geometry_surface, manager, manager.status, node_surface, surf_mgr, surface, surface_mgr

**`element_surface`**
- 属性: `data`, `elsets`, `name`

**`geometry_surface`**
- 属性: `data`, `name`, `to_node_surface`
- `get_shape` 1. (self: GFE.Pre.surface.geometry_surface, arg0: Handle_TDocStd_Document) -> list[tuple[int, TopoDS_Shape, int]]

**`manager`**
- `add` 1. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.surface.surface_mgr, obj: GFE::Pre::Surface) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.surface.surface_mgr, arg0: str) -> GFE::Pre::Surface

**`node_surface`**
- 属性: `data`, `name`

**`surface`**
- 属性: `name`

**枚举**:
- `manager.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.Pre.vibration
**类**: vib_mgr, vib_mgr.status, vibra_load, vibraload_manager

**`vib_mgr`**
- `add` 1. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad, inner: bool = False, auto_name: bool = False) -> generic_mgr.generic.status
- `edit` 1. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad) -> generic_mgr.generic.status ; 2. (self: GFE.Pre.vibration.vibraload_manager, obj: GFE::VibraLoad) -> generic_mgr.generic.status
- `find` 1. (self: GFE.Pre.vibration.vibraload_manager, arg0: str) -> GFE::VibraLoad

**`vibra_load`**
- 属性: `amp_bottom_x`, `amp_bottom_y`, `amp_bottom_z`, `input_loc`, `is_outcrop`, `level`, `name`, `pwave_dir`, `soil`
- `set_parameter` 1. (self: GFE.Pre.vibration.vibra_load, arg0: str, arg1: str) -> None

**枚举**:
- `vib_mgr.err_code` = UNDEFINED, SUCCESS, NAME_REPEATED, NAME_ILLEGAL, CHILD_NOT_EXIST, MISS_REFERENCE

---
## GFE.draft
**类**: controller

**`(mod)`**
- `get_current` () -> GFE.draft.controller

**`controller`**
- `add_arc_centre` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: Annotated[list[float], FixedSize(2)]) -> None
- `add_arc_points` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: Annotated[list[float], FixedSize(2)]) -> None
- `add_circle_centre` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)]) -> None
- `add_circle_points` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: Annotated[list[float], FixedSize(2)]) -> None
- `add_line` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)]) -> None
- `add_point` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)]) -> None
- `add_polyline` 1. (self: GFE.draft.controller, arg0: list[Annotated[list[float], FixedSize(2)]]) -> None
- `add_rectangle` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)]) -> None
- `array_selected` 1. (self: GFE.draft.controller, extend_x: int, extend_y: int, offset_x: float, offset_y: float) -> None
- `clear` 1. (self: GFE.draft.controller) -> None
- `constrain_selected_horizontal` 1. (self: GFE.draft.controller) -> None
- `constrain_selected_length` 1. (self: GFE.draft.controller, arg0: float) -> None
- `constrain_selected_parallel` 1. (self: GFE.draft.controller, set_ref: bool) -> None
- `constrain_selected_perpendicular` 1. (self: GFE.draft.controller, set_ref: bool) -> None
- `constrain_selected_tangent` 1. (self: GFE.draft.controller, set_ref: bool) -> None
- `constrain_selected_vertical` 1. (self: GFE.draft.controller) -> None
- `export` 1. (self: GFE.draft.controller) -> TopoDS_Shape
- `fill_selected` 1. (self: GFE.draft.controller) -> None
- `import_shape` 1. (self: GFE.draft.controller, arg0: TopoDS_Shape, arg1: Vec3D) -> None
- `input` 1. (self: GFE.draft.controller, arg0: float, arg1: float) -> None
- `input_selected` 1. (self: GFE.draft.controller) -> int
- `mirror_selected` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: bool) -> None ; 2. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: Annotated[list[float], FixedSize(2)], arg2: bool) -> None
- `redo` 1. (self: GFE.draft.controller) -> None
- `remove_selected` 1. (self: GFE.draft.controller) -> None
- `rotate_selected` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: float, arg2: bool) -> None
- `round_array_selected` 1. (self: GFE.draft.controller, count: int, rad: float, centre_x: float, centre_y: float) -> None
- `scale_selected` 1. (self: GFE.draft.controller, arg0: Annotated[list[float], FixedSize(2)], arg1: float, arg2: bool) -> None
- `select_face` 1. (self: GFE.draft.controller, u: float, v: float, replace: bool = True) -> None ; 2. (self: GFE.draft.controller, umin: float, umax: float, vmin: float, vmax: float, replace: bool = True) -> None
- `select_line` 1. (self: GFE.draft.controller, u: float, v: float, replace: bool = True) -> None ; 2. (self: GFE.draft.controller, umin: float, umax: float, vmin: float, vmax: float, replace: bool = True) -> None
- `select_point` 1. (self: GFE.draft.controller, u: float, v: float, replace: bool = True) -> None ; 2. (self: GFE.draft.controller, umin: float, umax: float, vmin: float, vmax: float, replace: bool = True) -> None
- `select_snaped` 1. (self: GFE.draft.controller, arg0: bool) -> None
- `set_constrain_value` 1. (self: GFE.draft.controller, arg0: float) -> None
- `set_copy_transform` 1. (self: GFE.draft.controller, arg0: bool) -> None
- `set_normal` 1. (self: GFE.draft.controller, arg0: int) -> None ; 2. (self: GFE.draft.controller, arg0: Vec3D, arg1: Vec3D, arg2: Vec3D) -> None
- `set_operate_mode` 1. (self: GFE.draft.controller, arg0: GFE::Draft::DraftController::OpMode) -> None ; 2. (self: GFE.draft.controller, arg0: int) -> None
- `set_snap_object` 1. (self: GFE.draft.controller, arg0: list[bool]) -> None ; 2. (self: GFE.draft.controller, arg0: GFE::Draft::DraftController::SnapObjMode) -> None ; 3. (self: GFE.draft.controller, arg0: int) -> None
- `set_snap_tolerance` 1. (self: GFE.draft.controller, arg0: float) -> None
- `snap_object` 1. (self: GFE.draft.controller, arg0: float, arg1: float) -> None ; 2. (self: GFE.draft.controller, arg0: float, arg1: float, arg2: float, arg3: float) -> None
- `split_selected` 1. (self: GFE.draft.controller) -> None
- `translate_selected` 1. (self: GFE.draft.controller, begin: Annotated[list[float], FixedSize(2)], end: Annotated[list[float], FixedSize(2)], copy: bool = False) -> None ; 2. (self: GFE.draft.controller, vector: Annotated[list[float], FixedSize(2)], copy: bool = False) -> None
- `undo` 1. (self: GFE.draft.controller) -> None

**枚举**:
- `Normal` = X, Y, Z
- `OpMode` = OP_None, OP_Point, OP_Line, OP_Polyline, OP_Rect, OP_Arc_Three_Point, OP_Arc_Centre_Point, OP_Circle_Three_Point, OP_Circle_Centre_Point, OP_Translate, OP_Mirror_Point, OP_Mirror_Axis, OP_Rotate, OP_Scale, OP_Fill_Area, OP_Array, OP_RoundArray, OP_Extrude, OP_Revolute, CST_Horizontal, CST_Vertical, CST_Length, CST_Parallel, CST_Perpendicular, CST_Tangent
- `SnapObjMode` = SO_None, SO_Point, SO_Edge, SO_Surface

---
## GFE.geometry.contact_pair

**`(mod)`**
- `search_edge` 1. (master shape: TopoDS_Shape, slave shape: TopoDS_Shape, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]] ; 2. (master shape: str, slave shape: str, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]]
- `search_face` 1. (master shape: TopoDS_Shape, slave shape: TopoDS_Shape, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]] ; 2. (master shape: str, slave shape: str, tolerance: float) -> list[tuple[set[tuple[int, int]], set[tuple[int, int]]]]

---
## GFE.geometry.geoprim
**类**: builder

**`(mod)`**
- `set_tolerance_limit` 1. (arg0: float) -> None

**`builder`**
- `common` 1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape]) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str]) -> bool
- `cut` 1. (self: GFE.geometry.geoprim.builder, shape_be_cut: TopoDS_Shape, shapes_to_cut: list[TopoDS_Shape]) -> TopoDS_Shape ; 2. (self: GFE.geometry.geoprim.builder, name_be_cut: str, names_to_cut: list[str], remove origin: bool = False) -> bool
- `extrude` 1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: Annotated[list[float], FixedSize(3)]) -> list[TopoDS_Shape]
- `make_array` 1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: int, arg2: int, arg3: int, arg4: Annotated[list[float], FixedSize(3)]) -> list[TopoDS_Shape]
- `make_round_array` 1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: int, arg2: float, arg3: Annotated[list[float], FixedSize(3)], arg4: Annotated[list[float], FixedSize(3)]) -> list[TopoDS_Shape]
- `merge` 1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape]) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], replace_set: bool = False) -> bool
- `redo` 1. (self: GFE.geometry.geoprim.builder) -> None
- `revolve` 1. (self: GFE.geometry.geoprim.builder, arg0: list[TopoDS_Shape], arg1: Annotated[list[float], FixedSize(3)], arg2: Annotated[list[float], FixedSize(3)], arg3: float) -> list[TopoDS_Shape]
- `rotate` 1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], axis_loc: Annotated[list[float], FixedSize(3)], axis_dir: Annotated[list[float], FixedSize(3)], angle: float, copy: bool = False) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], axis_loc: Annotated[list[float], FixedSize(3)], axis_dir: Annotated[list[float], FixedSize(3)], angle: float, copy: bool = False) -> int
- `scale` 1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], factor: float, copy: bool = False) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], factor: float, copy: bool = False) -> int ; 3. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], centre: Annotated[list[float], FixedSize(3)], factor: float, copy: bool = False) -> list[TopoDS_Shape] ; 4. (self: GFE.geometry.geoprim.builder, names: list[str], centre: Annotated[list[float], FixedSize(3)], factor: float, copy: bool = False) -> int
- `split` 1. (self: GFE.geometry.geoprim.builder, shape_be_splitted: TopoDS_Shape, shapes_to_split: list[TopoDS_Shape]) -> TopoDS_Shape ; 2. (self: GFE.geometry.geoprim.builder, name_be_splitted: str, names_to_split: list[str], remove origin: bool = False) -> bool
- `translate` 1. (self: GFE.geometry.geoprim.builder, shapes: list[TopoDS_Shape], vector: Annotated[list[float], FixedSize(3)], copy: bool = False) -> list[TopoDS_Shape] ; 2. (self: GFE.geometry.geoprim.builder, names: list[str], vector: Annotated[list[float], FixedSize(3)], copy: bool = False) -> int
- `undo` 1. (self: GFE.geometry.geoprim.builder) -> None

---
## GFE.geometry.geotool

**`(mod)`**
- `centre_of_mass` 1. (arg0: TopoDS_Shape) -> Vec3D
- `children` 1. (arg0: TopoDS_Shape) -> list[TopoDS_Shape] ; 2. (arg0: TopoDS_Shape, arg1: int) -> list[TopoDS_Shape]
- `get_id_by_shape` 1. (arg0: TopoDS_Shape) -> Annotated[list[int], FixedSize(3)]
- `get_selected_shape` 1. (arg0: TopAbs_ShapeEnum) -> list[TopoDS_Shape]
- `get_selected_shape_id` 1. (arg0: TopAbs_ShapeEnum) -> list[Annotated[list[int], FixedSize(3)]]
- `get_shape_box` 1. (arg0: TopoDS_Shape, arg1: float) -> Bnd_Box
- `get_shape_box_range` 1. (arg0: TopoDS_Shape, arg1: float) -> Annotated[list[float], FixedSize(6)]
- `get_shape_by_id` 1. (arg0: int, arg1: int, arg2: int) -> TopoDS_Shape
- `insidebox` 1. (arg0: TopoDS_Shape, arg1: Bnd_Box) -> bool
- `make_compound` 1. (arg0: list[TopoDS_Shape], arg1: bool) -> TopoDS_Shape

---
## GFE.geometry.mesh_generator
**类**: controller, curve_control, generator, gmsh_control, sweep_control

**`controller`**
- 属性: `auto_transfinite`, `generate_dim`, `geom_to_type`, `number_option`, `size_option`, `string_option`, `sweep_option`, `user_option`
- `set_approximate_size` 1. (self: GFE.geometry.mesh_generator.controller, arg0: float) -> None
- `set_as_default` 1. (self: GFE.geometry.mesh_generator.controller) -> None

**`curve_control`**
- 属性: `count`, `density`, `edges`, `set_name`

**`generator`**
- `mesh` 1. (self: GFE.geometry.mesh_generator.generator, arg0: list[str], arg1: GFE.geometry.mesh_generator.controller) -> int

**`sweep_control`**
- 属性: `body`, `dx`, `dy`, `dz`, `layers`, `ratio`, `recomb_lateral`, `recomb_source`, `source`, `target`

---
## GFE.io
**类**: instance

**`(mod)`**
- `get_current` () -> GFE.io.instance

**`instance`**
- `import_yjk` 1. (self: GFE.io.instance, u8path: str, para_int: list[int], para_str: list[str], to_cur_win: bool, name_prefix: str, is_accessory: bool) -> bool
- `open_dwg` 1. (self: GFE.io.instance, u8path: str, parameter: list[int]) -> None
- `open_inp` 1. (self: GFE.io.instance, u8path: str) -> bool
- `open_pre` 1. (self: GFE.io.instance, u8path: str, merge: bool = False, prefix: str = 'Part') -> bool

---
## GFE.io.inpio
**类**: writer

**`writer`**
- `perform` 1. (self: GFE.io.inpio.writer) -> bool
- `set_case` 1. (self: GFE.io.inpio.writer, arg0: str) -> None
- `set_trainload2inpx` 1. (self: GFE.io.inpio.writer, arg0: bool) -> None

---
## GFE.occ
**类**: box, compound, edge, face, shape, shell, solid, vertex, wire

**`box`**
- `enlarge` 1. (self: GFE.occ.box, arg0: float) -> None

**`compound`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`edge`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`face`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`shape`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`shell`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`solid`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`vertex`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**`wire`**
- `is_null` 1. (self: GFE.occ.shape) -> bool
- `is_same` 1. (self: GFE.occ.shape, arg0: GFE.occ.shape) -> bool

**枚举**:
- `ShapeType` = VERTEX, EDGE, WIRE, FACE, SHELL, SOLID, COMPOUND, SHAPE

---
## GFE.occ.brep_prim

**`(mod)`**
- `make_box` 1. (dx: float, dy: float, dz: float) -> GFE.occ.shape ; 2. (pt1: Vec3D, pt2: Vec3D) -> GFE.occ.shape
- `make_cone` 1. (bot_r: float, h: float, top_r: float = 0) -> GFE.occ.shape
- `make_cylinder` 1. (r: float, h: float) -> GFE.occ.shape
- `make_sphere` 1. (r: float) -> GFE.occ.shape
- `make_torus` 1. (r1: float, r2: float) -> GFE.occ.shape
- `make_wedge` 1. (dx: float, dy: float, dz: float, xmin: float, xmax: float, zmin: float, zmax: float) -> GFE.occ.solid

---
## GFE.soil
**类**: box_builder, data_builder

**`box_builder`**
- `build` 1. (self: GFE.soil.box_builder) -> list[list[TopoDS_Shape]]
- `perform` 1. (self: GFE.soil.box_builder) -> list[list[TopoDS_Shape]]
- `set_height` 1. (self: GFE.soil.box_builder, height: list[float], depth: int) -> None
- `set_parameter` 1. (self: GFE.soil.box_builder, length: float, width: float) -> None

**`data_builder`**
- 属性: `dimension`, `layer_material`, `layer_shape`, `name`
- `build` 1. (self: GFE.soil.data_builder) -> bool
- `perform` 1. (self: GFE.soil.data_builder) -> bool