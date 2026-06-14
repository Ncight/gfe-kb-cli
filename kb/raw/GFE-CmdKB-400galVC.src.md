# GFE 命令流真实工程状态 dump：400galW7-VC（39层弹塑性 SSI，小型管理器）
> 来源：D:\GFE\GFE_KB（gfe-command-stream skill 维护的命令流知识库）。本文件为 raw 检索源副本。


---

## _index.md
`04_状态dump\400galW7VC\_index.md`

# 400galW7VC.txt — 按管理器索引

| 管理器 | 对象数 | 行数 | 文件 | 对象名预览 |
|---|---|---|---|---|
| `GFE.Pre.geometry.geo_mgr` | 3 | 4 | geometry_geo_mgr.txt | SuperStru, Soil-1, WallSurface |
| `GFE.Pre.mesh.mesh_mgr` | 3 | 4 | mesh_mesh_mgr.txt | SuperStru, Soil-1, WallSurface |
| `GFE.Pre.material.mat_mgr` | 35 | 106 | material_mat_mgr.txt | C1_Mat30, C2_Mat30, C1_Mat35, C2_Mat35, C1_Mat40, C2_Mat40, C1_Mat50, C2_Mat50, C1_Mat55, C2_Mat55 ... |
| `GFE.Pre.set.elset_manager` | 2 | 10 | set_elset_manager.txt | ElementSet-1, ElementSet-qun |
| `GFE.Pre.set.gset_manager` | 2676 | 5354 | set_gset_manager.txt | Comb_PointForce_2157, Comb_PointLoad_1836, Comb_PointLoad_1837, Comb_PointLoad_1838, Comb_PointLoad_1839, Comb_PointLoad_1840, Comb_PointLoad_1841, Comb_PointLoad_1842, Comb_PointLoad_1843, Comb_PointLoad_1844 ... |
| `GFE.Pre.set.nset_manager` | 1 | 5 | set_nset_manager.txt | NodeSet-1 |
| `GFE.Pre.section.sect_mgr` | 1101 | 12040 | section_sect_mgr.txt | WallC_Conc1500_C50_958, WallC_Conc700_C50_959, WallC_Conc400_C50_960, WallC_Conc600_C50_961, WallC_Conc800_C50_962, WallC_Conc300_C50_963, WallC_Conc900_C50_964, WallC_Conc500_C50_965, WallC_Conc1000_C50_966, WallC_Conc799_C80_967 ... |
| `GFE.Pre.step.step_manager` | 3 | 20 | step_step_manager.txt | Initial, StaticStep, DynamicStep |
| `GFE.Pre.boundary.bc_mgr` | 2202 | 46243 | boundary_bc_mgr.txt | Dead_LL_BEAM20_1087, Dead_LL_BEAM11_1088, Dead_LL_BEAM15_1089, Dead_LL_BEAM7_1090, Dead_LL_BEAM18_1091, Dead_LL_BEAM3_1092, Dead_LL_BEAM30_1093, Live_LL_BEAM17_1094, Dead_LL_BEAM16_1095, Dead_LL_BEAM21_1096 ... |
| `GFE.Pre.interaction.embed_manager` | 3 | 23 | interaction_embed_manager.txt | Embed-1, Embed-2, Embed-3 |
| `GFE.Pre.interaction.tie_manager` | 2 | 15 | interaction_tie_manager.txt | Tie-diban, Tie-2 |
| `GFE.Pre.amplitude.amp_mgr` | 6 | 37 | amplitude_amp_mgr.txt | 400galElcentro, Amp-1, Amp-X, Amp-Y, Amp-Z, Amp-DY |
| `GFE.Pre.surface.surf_mgr` | 200 | 802 | surface_surf_mgr.txt | Dead_P_SLAB10_2158, Dead_P_SLAB5_2159, Dead_P_SLAB3_2160, Dead_P_SLAB15_2161, Dead_P_SLAB13_2162, Dead_P_SLAB13_2163, Dead_P_SLAB15_2164, Dead_P_SLAB5_2165, Dead_P_SLAB5_2166, Dead_P_SLAB14_2167 ... |
| `GFE.Pre.surface.surface_mgr` | 200 | 801 | surface_surface_mgr.txt | Dead_P_SLAB10_2158, Dead_P_SLAB5_2159, Dead_P_SLAB3_2160, Dead_P_SLAB15_2161, Dead_P_SLAB13_2162, Dead_P_SLAB13_2163, Dead_P_SLAB15_2164, Dead_P_SLAB5_2165, Dead_P_SLAB5_2166, Dead_P_SLAB14_2167 ... |
| `GFE.Pre.output.field_mgr` | 7 | 86 | output_field_mgr.txt | FO-Static, FO-DynaPla-All, FO-DynaPla-Jiegou, FO-DynaPla-ShearForce, EO-DynaPla-Max, EO-DynaPla-Min, FieldOutput-1 |
| `GFE.Pre.output.history_mgr` | 2 | 26 | output_history_mgr.txt | HistoryOutput-1, HistoryOutput-2 |
| `GFE.Pre.vibration.vib_mgr` | 1 | 12 | vibration_vib_mgr.txt | VibLoad-1 |
| `GFE.Pre.vibration.vibraload_manager` | 1 | 11 | vibration_vibraload_manager.txt | VibLoad-1 |
| `GFE.Pre.artbc.artbc_mgr` | 1 | 7 | artbc_artbc_mgr.txt | ArtBC-1 |
| `GFE.Pre.soil.soil_manager` | 1 | 7 | soil_soil_manager.txt | Soil1D-1 |
| `GFE.Pre.case.case_mgr` | 7 | 22 | case_case_mgr.txt | Dead, Live, 消防车_gk2, gk3, Comb, 400galElcentro, 400galElcentrostatic |

## 空管理器
`GFE.Pre.interaction.conn_beh_mgr`, `GFE.Pre.interaction.conn_prop_mgr`, `GFE.Pre.interaction.connector_behavior_manager`, `GFE.Pre.interaction.connector_property_manager`, `GFE.Pre.interaction.contact_manager`, `GFE.Pre.interaction.incident_wave_manager`, `GFE.Pre.interaction.incident_wave_property_manager`, `GFE.Pre.interaction.iw_mgr`, `GFE.Pre.interaction.iw_prop_mgr`, `GFE.Pre.interaction.mpc_manager`, `GFE.Pre.interaction.rigid_manager`, `GFE.Pre.interaction.sd_mgr`, `GFE.Pre.interaction.spec_mgr`, `GFE.Pre.interaction.special_manager`, `GFE.Pre.interaction.spring_dashpot_manager`, `GFE.Pre.orientation.orientation_mgr`, `GFE.Pre.initial_condition.ic_mgr`, `GFE.Pre.field.field_manager`, `GFE.Pre.sph.sph_manager`



---

## soil_soil_manager.txt
`04_状态dump\400galW7VC\soil_soil_manager.txt`

```python
# ==== soil_soil_manager.txt ====
### MANAGER GFE.Pre.soil.soil_manager()  -> 1 objects
  OBJ 'Soil1D-1' : soil
    .bedrock_mat = 'tu16'
    .depth = [1.5, 1.5, 1.0, 1.0, 3.35, 3.5, 3.0, 6.0, 4.0, 15.0, 15.0, 2.0, 3.0, 3.0, 3.0, 10.0]
    .depth_dir = 2
    .materials = ['tu1', 'tu2', 'tu3', 'tu4', 'tu5', 'tu6', 'tu7', 'tu8', 'tu9', 'tu10', 'tu11', 'tu12', 'tu13', 'tu14', 'tu15', 'tu16']
    .name = 'Soil1D-1'
```


---

## material_mat_mgr.txt
`04_状态dump\400galW7VC\material_mat_mgr.txt`

```python
# ==== material_mat_mgr.txt ====
### MANAGER GFE.Pre.material.mat_mgr()  -> 35 objects
  OBJ 'C1_Mat30' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[30000000.0, 20100.0, 0.0014719, 0.746531, 2010.0, 9.52563e-05, 1.2625], n_constants=7, user_type=1)]
    .name = 'C1_Mat30'
  OBJ 'C2_Mat30' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[30000000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.00563985, 2.69984e-05, 0.0274575, 8.56531e-05, 0.0605393, 0.000159258, 0.0988933, 0.000241002, 0.138773, 0.000327736, 0.178137, 0.000417865, 0.215959, 0.000510519, 0.251782, 0.000605202, 0.285459, 0.00070162, 0.317004, 0.000799598, 0.502373, 0.00160842, 0.628039, 0.00245107, 0.713761, 0.00327296, 0.773477, 0.00407272, 0.816318, 0.00485613, 0.847966, 0.0056281, 0.87197, 0.00639198, 0.890601, 0.00715006, 0.905355, 0.00790385, 0.917242, 0.00865441], comp_harden=[14472.0, 0.0, 16623.4, 2.69984e-05, 17825.4, 8.56531e-05, 18578.8, 0.000159258, 19088.2, 0.000241002, 19447.7, 0.000327736, 19705.5, 0.000417865, 19887.5, 0.000510519, 20008.6, 0.000605202, 20077.7, 0.00070162, 20100.0, 0.000799598, 17879.8, 0.00160842, 14644.5, 0.00245107, 12032.0, 0.00327296, 10083.2, 0.00407272, 8624.93, 0.00485613, 7510.16, 0.0056281, 6637.6, 0.00639198, 5939.41, 0.00715006, 5369.8, 0.00790385, 4897.19, 0.00865441], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=21, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00374808, 1.71706e-06, 0.0185059, 5.94001e-06, 0.0428385, 1.19048e-05, 0.07377, 1.93224e-05, 0.109028, 2.8065e-05, 0.4, 0.00014426], tens_recov=0.0, tens_stiff=[1447.07, 0.0, 1674.24, 1.71706e-06, 1829.1, 5.94001e-06, 1931.71, 1.19048e-05, 1990.73, 1.93224e-05, 2010.0, 2.8065e-05, 1787.27, 0.00014426])]
    .name = 'C2_Mat30'
  OBJ 'C1_Mat35' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[31500000.0, 23400.0, 0.00153229, 0.959297, 2200.0, 9.9984e-05, 1.51144], n_constants=7, user_type=1)]
    .name = 'C1_Mat35'
  OBJ 'C2_Mat35' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[31500000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.00435274, 2.48057e-05, 0.0219896, 8.00743e-05, 0.0498449, 0.000150718, 0.0831993, 0.000230165, 0.11879, 0.000315227, 0.154675, 0.000404225, 0.189773, 0.000496216, 0.223525, 0.000590649, 0.255675, 0.000687194, 0.286141, 0.000785649, 0.478165, 0.00165172, 0.613261, 0.00255388, 0.705534, 0.00342137, 0.769234, 0.00425836, 0.814451, 0.00507482, 0.847523, 0.00587777, 0.872388, 0.00667161, 0.891541, 0.00745911, 0.906605, 0.00824205, 0.918671, 0.00902163], comp_harden=[16848.0, 0.0, 19196.3, 2.48057e-05, 20585.4, 8.00743e-05, 21490.2, 0.000150718, 22117.6, 0.000230165, 22568.1, 0.000315227, 22894.8, 0.000404225, 23127.1, 0.000496216, 23282.4, 0.000590649, 23371.3, 0.000687194, 23400.0, 0.000785649, 20193.3, 0.00165172, 15849.4, 0.00255388, 12597.5, 0.00342137, 10306.6, 0.00425836, 8662.1, 0.00507482, 7443.23, 0.00587777, 6511.35, 0.00667161, 5779.27, 0.00745911, 5190.74, 0.00824205, 4708.26, 0.00902163], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=21, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00391821, 1.86887e-06, 0.0193571, 6.43905e-06, 0.0446144, 1.28462e-05, 0.0764653, 2.07623e-05, 0.112512, 3.00429e-05, 0.4, 0.000150806], tens_recov=0.0, tens_stiff=[1583.89, 0.0, 1835.08, 1.86887e-06, 2004.22, 6.43905e-06, 2115.5, 1.28462e-05, 2179.24, 2.07623e-05, 2200.0, 3.00429e-05, 1958.72, 0.000150806])]
    .name = 'C2_Mat35'
  OBJ 'C1_Mat40' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[32500000.0, 26800.0, 0.00158943, 1.16978, 2390.0, 0.000104481, 1.78262], n_constants=7, user_type=1)]
    .name = 'C1_Mat40'
  OBJ 'C2_Mat40' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[32500000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.0032522, 2.22809e-05, 0.0170734, 7.32754e-05, 0.0398574, 0.000139807, 0.0681011, 0.000215739, 0.0991035, 0.000297934, 0.131106, 0.000384672, 0.163039, 0.000474959, 0.194281, 0.000568197, 0.224492, 0.00066402, 0.253508, 0.000762202, 0.451906, 0.00168949, 0.59681, 0.0026522, 0.695756, 0.00356412, 0.76347, 0.00443714, 0.811092, 0.00528584, 0.845637, 0.00611927, 0.871426, 0.00694274, 0.89117, 0.00775946, 0.906619, 0.0085714, 0.918937, 0.00937987], comp_harden=[19296.0, 0.0, 21799.1, 2.22809e-05, 23369.4, 7.32754e-05, 24434.7, 0.000139807, 25194.5, 0.000215739, 25750.8, 0.000297934, 26159.4, 0.000384672, 26452.6, 0.000474959, 26650.0, 0.000568197, 26763.3, 0.00066402, 26800.0, 0.000762202, 22449.5, 0.00168949, 16947.4, 0.0026522, 13095.8, 0.00356412, 10508.5, 0.00443714, 8711.76, 0.00528584, 7411.22, 0.00611927, 6434.26, 0.00694274, 5677.09, 0.00775946, 5074.84, 0.0085714, 4585.35, 0.00937987], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=21, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00368321, 1.88072e-06, 0.0184727, 6.54622e-06, 0.0429335, 1.31339e-05, 0.0740255, 2.13138e-05, 0.109433, 3.094e-05, 0.4, 0.000158439], tens_recov=0.0, tens_stiff=[1720.72, 0.0, 1992.03, 1.88072e-06, 2176.0, 6.54622e-06, 2297.5, 1.31339e-05, 2367.25, 2.13138e-05, 2390.0, 3.094e-05, 2125.53, 0.000158439])]
    .name = 'C2_Mat40'
  OBJ 'C1_Mat50' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[34500000.0, 32400.0, 0.00167902, 1.49983, 2640.0, 0.000110181, 2.1751], n_constants=7, user_type=1)]
    .name = 'C1_Mat50'
  OBJ 'C2_Mat50' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[34500000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.00228344, 1.96025e-05, 0.0125082, 6.58677e-05, 0.0301916, 0.000127742, 0.0530013, 0.000199684, 0.0788816, 0.000278699, 0.106356, 0.000363066, 0.134441, 0.000451753, 0.162502, 0.000544123, 0.190149, 0.000639775, 0.21715, 0.000738459, 0.423015, 0.00176504, 0.580484, 0.00281846, 0.687371, 0.00379428, 0.759496, 0.00471967, 0.809559, 0.00561623, 0.845478, 0.00649567, 0.872049, 0.00736439, 0.892237, 0.00822603, 0.907932, 0.00908277, 0.920376, 0.00993602], comp_harden=[23328.0, 0.0, 26106.3, 1.96025e-05, 27965.1, 6.58677e-05, 29285.3, 0.000127742, 30258.2, 0.000199684, 30987.1, 0.000278699, 31531.4, 0.000363066, 31926.6, 0.000451753, 32194.8, 0.000544123, 32349.7, 0.000639775, 32400.0, 0.000738459, 25922.0, 0.00176504, 18517.4, 0.00281846, 13790.4, 0.00379428, 10802.8, 0.00471967, 8810.29, 0.00561623, 7407.96, 0.00649567, 6375.79, 0.00736439, 5588.03, 0.00822603, 4968.9, 0.00908277, 4470.48, 0.00993602], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=21, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00403742, 2.12027e-06, 0.0200603, 7.29316e-06, 0.0461357, 1.45017e-05, 0.078806, 2.33575e-05, 0.115554, 3.36901e-05, 0.4, 0.000165651], tens_recov=0.0, tens_stiff=[1900.73, 0.0, 2205.19, 2.12027e-06, 2407.72, 7.29316e-06, 2540.02, 1.45017e-05, 2615.48, 2.33575e-05, 2640.0, 3.36901e-05, 2353.1, 0.000165651])]
    .name = 'C2_Mat50'
  OBJ 'C1_Mat55' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[35500000.0, 35500.0, 0.00172745, 1.67933, 2710.0, 0.000112405, 2.34345], n_constants=7, user_type=1)]
    .name = 'C1_Mat55'
  OBJ 'C2_Mat55' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[35500000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.00190853, 1.82975e-05, 0.0106658, 6.21351e-05, 0.0261607, 0.000121502, 0.0465358, 0.000191211, 0.0700334, 0.000268376, 0.09533, 0.000351309, 0.121505, 0.000438977, 0.147941, 0.000530733, 0.174238, 0.000626167, 0.200144, 0.000725019, 0.409443, 0.00180639, 0.573081, 0.00290672, 0.683691, 0.00391462, 0.757805, 0.00486656, 0.808938, 0.00578771, 0.845444, 0.006691, 0.872342, 0.00758329, 0.892712, 0.00846838, 0.908503, 0.00934856, 0.920996, 0.0102252], comp_harden=[25560.0, 0.0, 28477.9, 1.82975e-05, 30489.6, 6.21351e-05, 31949.9, 0.000121502, 33043.1, 0.000191211, 33871.5, 0.000268376, 34495.3, 0.000351309, 34950.9, 0.000438977, 35261.5, 0.000530733, 35441.4, 0.000626167, 35500.0, 0.000725019, 27731.0, 0.00180639, 19288.6, 0.00290672, 14127.5, 0.00391462, 10952.6, 0.00486656, 8871.34, 0.00578771, 7423.55, 0.006691, 6366.74, 0.00758329, 5565.17, 0.00846838, 4938.2, 0.00934856, 4435.36, 0.0102252, 4023.68, 0.0110993], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=22, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00436953, 2.28244e-06, 0.0214553, 7.76619e-06, 0.048875, 1.53294e-05, 0.0828315, 2.45464e-05, 0.120655, 3.52312e-05, 0.4, 0.000167696], tens_recov=0.0, tens_stiff=[1972.72, 0.0, 2292.52, 2.28244e-06, 2502.13, 7.76619e-06, 2637.93, 1.53294e-05, 2715.02, 2.45464e-05, 2740.0, 3.52312e-05, 2446.74, 0.000167696])]
    .name = 'C2_Mat55'
  OBJ 'C1_Mat60' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[36000000.0, 38500.0, 0.00177005, 1.85419, 2850.0, 0.000114805, 2.535], n_constants=7, user_type=1)]
    .name = 'C1_Mat60'
  OBJ 'C2_Mat60' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[36000000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.00151722, 1.65165e-05, 0.00868705, 5.68367e-05, 0.0217312, 0.000112329, 0.0392969, 0.000178335, 0.0599719, 0.000252184, 0.0826269, 0.000332264, 0.106435, 0.000417575, 0.130815, 0.000507477, 0.15537, 0.000601559, 0.179834, 0.000699561, 0.392389, 0.00183646, 0.562744, 0.00298295, 0.677551, 0.00402169, 0.75404, 0.00499894, 0.806552, 0.00594339, 0.843895, 0.0068692, 0.871322, 0.00778366, 0.892037, 0.00869077, 0.908062, 0.00959289, 0.920715, 0.0104915], comp_harden=[27720.0, 0.0, 30721.5, 1.65165e-05, 32866.4, 5.68367e-05, 34465.2, 0.000112329, 35685.4, 0.000178335, 36623.3, 0.000252184, 37336.9, 0.000332264, 37862.1, 0.000417575, 38222.1, 0.000507477, 38431.6, 0.000601559, 38500.0, 0.000699561, 29414.4, 0.00183646, 19983.0, 0.00298295, 14430.5, 0.00402169, 11091.8, 0.00499894, 8933.88, 0.00594339, 7446.97, 0.0068692, 6368.85, 0.00778366, 5555.15, 0.00869077, 4921.1, 0.00959289, 4414.12, 0.0104915], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=21, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00424766, 2.28805e-06, 0.0209089, 7.80041e-06, 0.047781, 1.54336e-05, 0.0812102, 2.47666e-05, 0.118593, 3.56152e-05, 0.4, 0.000171748], tens_recov=0.0, tens_stiff=[2051.91, 0.0, 2382.78, 2.28805e-06, 2601.08, 7.80041e-06, 2743.04, 1.54336e-05, 2823.8, 2.47666e-05, 2850.0, 3.56152e-05, 2543.06, 0.000171748])]
    .name = 'C2_Mat60'
  OBJ 'C1_Mat80' : material
    .entries = [density(n_param=1, params=[2.5], temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0]), user(constants=[38000000.0, 50200.0, 0.00192259, 2.49053, 3110.0, 0.000120286, 3.01863], n_constants=7, user_type=1)]
    .name = 'C1_Mat80'
  OBJ 'C2_Mat80' : material
    .entries = [density(n_param=1, params=[2.6], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[38000000.0, 0.2], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.18849555921538758, 0.0]), concrete_damaged(comp_damage=[0.0, 0.0, 0.000655828, 1.08212e-05, 0.00406341, 3.91061e-05, 0.0108593, 8.05277e-05, 0.0207833, 0.000132448, 0.0333265, 0.000193192, 0.0479667, 0.000261666, 0.0642461, 0.000337143, 0.0817886, 0.000419137, 0.100295, 0.00050733, 0.119532, 0.000601519, 0.340497, 0.00195076, 0.532495, 0.00325731, 0.660173, 0.00439935, 0.743675, 0.00546237, 0.800151, 0.00648684, 0.839848, 0.00749055, 0.868737, 0.00848205, 0.890394, 0.00946584, 0.907043, 0.0104445, 0.920119, 0.0114195], comp_harden=[36144.0, 0.0, 39423.8, 1.08212e-05, 42040.4, 3.91061e-05, 44157.8, 8.05277e-05, 45876.2, 0.000132448, 47259.4, 0.000193192, 48348.8, 0.000261666, 49172.1, 0.000337143, 49747.7, 0.000419137, 50087.8, 0.00050733, 50200.0, 0.000601519, 35458.3, 0.00195076, 22338.5, 0.00325731, 15469.8, 0.00439935, 11604.3, 0.00546237, 9203.54, 0.00648684, 7591.6, 0.00749055, 6443.73, 0.00848205, 5588.75, 0.00946584, 4929.2, 0.0104445, 4405.96, 0.0114195], comp_recov=1.0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, n_comp_damage=21, n_comp_harden=21, n_plasticity=1, n_tens_damage=7, n_tens_stiff=7, plasticity=[35.0, 0.1, 1.16, 0.6666666666666666, 0.005], tens_damage=[0.0, 0.0, 0.00472924, 2.57116e-06, 0.0226818, 8.58658e-06, 0.0510896, 1.68176e-05, 0.0859443, 2.67983e-05, 0.1245, 3.8326e-05, 0.4, 0.000178234], tens_recov=0.0, tens_stiff=[2239.02, 0.0, 2603.89, 2.57116e-06, 2841.5, 8.58658e-06, 2994.92, 1.68176e-05, 3081.86, 2.67983e-05, 3110.0, 3.8326e-05, 2780.93, 0.000178234])]
    .name = 'C2_Mat80'
  OBJ 'HRB400' : material
    .entries = [density(n_param=1, params=[7.8], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[200000000.0, 0.25], temp_dp=False, tension=False, type=0), plastic(harden_type=0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, params=[1000000000.0, 1000000000.0, 400000.0, 0.0, 540000.0, 0.075], rate_dp=False, temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0])]
    .name = 'HRB400'
  OBJ 'Q345' : material
    .entries = [density(n_param=1, params=[7.8], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[206000000.0, 0.25], temp_dp=False, tension=False, type=0), plastic(harden_type=0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, params=[1000000000.0, 1000000000.0, 345000.0, 0.0, 475000.0, 0.09], rate_dp=False, temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0])]
    .name = 'Q345'
  OBJ 'Q390' : material
    .entries = [density(n_param=1, params=[7.8], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[206000000.0, 0.25], temp_dp=False, tension=False, type=0), plastic(harden_type=0, has_jc_rate=False, jc_rate_C=0.0, jc_rate_Ep0_dot1=0.0, params=[1000000000.0, 1000000000.0, 390000.0, 0.0, 520000.0, 0.09], rate_dp=False, temp_dp=False), damping(n_param=2, params=[0.18849555921538758, 0.0])]
    .name = 'Q390'
  OBJ 'tu1' : material
    .entries = [density(n_param=1, params=[1.63], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[108300.0, 0.25, 1.02, 0.44, 0.00045, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu1'
  OBJ 'tu2' : material
    .entries = [density(n_param=1, params=[1.63], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[108300.0, 0.25, 1.0, 0.45, 0.00055, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu2'
  OBJ 'tu3' : material
    .entries = [density(n_param=1, params=[1.63], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[108300.0, 0.25, 1.0, 0.45, 0.0006, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu3'
  OBJ 'tu4' : material
    .entries = [density(n_param=1, params=[1.6], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[108500.0, 0.45, 1.1, 0.46, 0.00085, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu4'
  OBJ 'tu5' : material
    .entries = [density(n_param=1, params=[1.99], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[248500.0, 0.3, 1.0, 0.45, 0.0007, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu5'
  OBJ 'tu6' : material
    .entries = [density(n_param=1, params=[1.99], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[248500.0, 0.3, 1.0, 0.45, 0.0007, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu6'
  OBJ 'tu7' : material
    .entries = [density(n_param=1, params=[2.09], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[694900.0, 0.23, 1.05, 0.44, 0.0005, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu7'
  OBJ 'tu8' : material
    .entries = [density(n_param=1, params=[2.09], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[694900.0, 0.23, 1.1, 0.46, 0.0009, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu8'
  OBJ 'tu9' : material
    .entries = [density(n_param=1, params=[2.09], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[694900.0, 0.23, 1.1, 0.46, 0.0009, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu9'
  OBJ 'tu10' : material
    .entries = [density(n_param=1, params=[2.1], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[850500.0, 0.22, 1.1, 0.46, 0.0009, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu10'
  OBJ 'tu11' : material
    .entries = [density(n_param=1, params=[2.1], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[850500.0, 0.22, 1.05, 0.44, 0.0005, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu11'
  OBJ 'tu12' : material
    .entries = [density(n_param=1, params=[2.09], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[694900.0, 0.23, 1.1, 0.46, 0.001, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu12'
  OBJ 'tu13' : material
    .entries = [density(n_param=1, params=[2.1], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[850500.0, 0.22, 1.05, 0.44, 0.0005, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu13'
  OBJ 'tu14' : material
    .entries = [density(n_param=1, params=[2.1], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[850500.0, 0.22, 1.05, 0.44, 0.0005, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu14'
  OBJ 'tu15' : material
    .entries = [density(n_param=1, params=[1.99], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[248500.0, 0.3, 1.0, 0.45, 0.0006, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu15'
  OBJ 'tu16' : material
    .entries = [density(n_param=1, params=[2.15], temp_dp=False), damping(n_param=2, params=[0.3141592653589793, 0.0]), user(constants=[2294900.0, 0.001, 1.0, 0.5, 0.01, 100000.0], n_constants=6, user_type=2)]
    .name = 'tu16'
  OBJ 'zhuangtong' : material
    .entries = [density(n_param=1, params=[2.08], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[2551600.0, 0.24], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.2, 0.0])]
    .name = 'zhuangtong'
  OBJ 'zhuangqun' : material
    .entries = [density(n_param=1, params=[2.08], temp_dp=False), elastic(compression=False, moduli_time_scale=0, n_param=2, params=[2551600.0, 0.24], temp_dp=False, tension=False, type=0), damping(n_param=2, params=[0.2, 0.0])]
    .name = 'zhuangqun'
```


---

## step_step_manager.txt
`04_状态dump\400galW7VC\step_step_manager.txt`

```python
# ==== step_step_manager.txt ====
### MANAGER GFE.Pre.step.step_manager()  -> 3 objects
  OBJ 'Initial' : analysis_step
    .description = ''
    .name = 'Initial'
    .nlgeom = False
  OBJ 'StaticStep' : static_general_step
    .description = ''
    .init_inc = 0.01
    .max_inc = 0.1
    .min_inc = 1e-05
    .name = 'StaticStep'
    .nlgeom = False
    .period = 1.0
  OBJ 'DynamicStep' : dynamic_explicit_step
    .description = ''
    .mass_scaling = [mass_scaling(frequency=100, region='*', target_time=5e-05, type=1)]
    .modal_damping = None
    .name = 'DynamicStep'
    .nlgeom = False
    .period = 35.0
```


---

## case_case_mgr.txt
`04_状态dump\400galW7VC\case_case_mgr.txt`

```python
# ==== case_case_mgr.txt ====
### MANAGER GFE.Pre.case.case_mgr()  -> 7 objects
  OBJ 'Dead' : case
    .name = 'Dead'
    .steps = ['Initial', 'StaticStep']
  OBJ 'Live' : case
    .name = 'Live'
    .steps = ['Initial', 'StaticStep']
  OBJ '消防车_gk2' : case
    .name = '消防车_gk2'
    .steps = ['Initial', 'StaticStep']
  OBJ 'gk3' : case
    .name = 'gk3'
    .steps = ['Initial', 'StaticStep']
  OBJ 'Comb' : case
    .name = 'Comb'
    .steps = ['Initial', 'StaticStep']
  OBJ '400galElcentro' : case
    .name = '400galElcentro'
    .steps = ['Initial', 'StaticStep', 'DynamicStep']
  OBJ '400galElcentrostatic' : case
    .name = '400galElcentrostatic'
    .steps = ['Initial', 'StaticStep']
```


---

## amplitude_amp_mgr.txt
`04_状态dump\400galW7VC\amplitude_amp_mgr.txt`

```python
# ==== amplitude_amp_mgr.txt ====
### MANAGER GFE.Pre.amplitude.amp_mgr()  -> 6 objects
  OBJ '400galElcentro' : amplitude
    .gravity = 0.0
    .name = '400galElcentro'
    .spectrum_type = -1
    .type = 0
    .value = <list len 5500>
  OBJ 'Amp-1' : amplitude
    .gravity = 0.0
    .name = 'Amp-1'
    .spectrum_type = -1
    .type = 4
    .value = [0.0, 0.0, 1.0, 1.0]
  OBJ 'Amp-X' : amplitude
    .gravity = 0.0
    .name = 'Amp-X'
    .spectrum_type = -1
    .type = 0
    .value = <list len 3420>
  OBJ 'Amp-Y' : amplitude
    .gravity = 0.0
    .name = 'Amp-Y'
    .spectrum_type = -1
    .type = 0
    .value = <list len 3420>
  OBJ 'Amp-Z' : amplitude
    .gravity = 0.0
    .name = 'Amp-Z'
    .spectrum_type = -1
    .type = 0
    .value = <list len 3420>
  OBJ 'Amp-DY' : amplitude
    .gravity = 0.0
    .name = 'Amp-DY'
    .spectrum_type = -1
    .type = 0
    .value = [0.0, 1.0, 55.0, 1.0]
```


---

## vibration_vib_mgr.txt
`04_状态dump\400galW7VC\vibration_vib_mgr.txt`

```python
# ==== vibration_vib_mgr.txt ====
### MANAGER GFE.Pre.vibration.vib_mgr()  -> 1 objects
  OBJ 'VibLoad-1' : vibra_load
    .amp_bottom_x = 'Amp-X'
    .amp_bottom_y = 'Amp-Y'
    .amp_bottom_z = 'Amp-Z'
    .input_loc = -1
    .is_outcrop = True
    .level = 0
    .name = 'VibLoad-1'
    .pwave_dir = 2
    .soil = 'Soil1D-1'

```


---

## vibration_vibraload_manager.txt
`04_状态dump\400galW7VC\vibration_vibraload_manager.txt`

```python
# ==== vibration_vibraload_manager.txt ====
### MANAGER GFE.Pre.vibration.vibraload_manager()  -> 1 objects
  OBJ 'VibLoad-1' : vibra_load
    .amp_bottom_x = 'Amp-X'
    .amp_bottom_y = 'Amp-Y'
    .amp_bottom_z = 'Amp-Z'
    .input_loc = -1
    .is_outcrop = True
    .level = 0
    .name = 'VibLoad-1'
    .pwave_dir = 2
    .soil = 'Soil1D-1'
```


---

## artbc_artbc_mgr.txt
`04_状态dump\400galW7VC\artbc_artbc_mgr.txt`

```python
# ==== artbc_artbc_mgr.txt ====
### MANAGER GFE.Pre.artbc.artbc_mgr()  -> 1 objects
  OBJ 'ArtBC-1' : art_bc
    .center = []
    .centered = False
    .name = 'ArtBC-1'
    .structure = 'SuperStru'
    .surface = 'PickedSurf-1'
```


---

## interaction_tie_manager.txt
`04_状态dump\400galW7VC\interaction_tie_manager.txt`

```python
# ==== interaction_tie_manager.txt ====
### MANAGER GFE.Pre.interaction.tie_manager()  -> 2 objects
  OBJ 'Tie-diban' : surface_pair
    .first_surf = 'Raft'
    .name = 'Tie-diban'
    .param_number = 1
    .parameters = [0.1]
    .second_surf = 'tudimian'
    .type = 0
  OBJ 'Tie-2' : surface_pair
    .first_surf = 'wallsizhou'
    .name = 'Tie-2'
    .param_number = 1
    .parameters = [0.1]
    .second_surf = 'tusizhou2'
    .type = 0
```


---

## interaction_embed_manager.txt
`04_状态dump\400galW7VC\interaction_embed_manager.txt`

```python
# ==== interaction_embed_manager.txt ====
### MANAGER GFE.Pre.interaction.embed_manager()  -> 3 objects
  OBJ 'Embed-1' : embed
    .embedded_names = ['Col_D1200_Sub0_C50_814']
    .exterior_tolerance = 0.8
    .host_name = 'wallsurface'
    .id = 2
    .name = 'Embed-1'
    .roundoff_tolerance = 1e-06
  OBJ 'Embed-2' : embed
    .embedded_names = ['Col_D1200_HRB400_815']
    .exterior_tolerance = 0.8
    .host_name = 'wallsurface'
    .id = 3
    .name = 'Embed-2'
    .roundoff_tolerance = 1e-06
  OBJ 'Embed-3' : embed
    .embedded_names = ['Col_D_PIPE1600_Sub0_C50_778', 'Col_D_PIPE1600_Sub1_Q390_779', 'Col_D_PIPE2000_Sub0_C50_796', 'Col_D_PIPE2000_Sub1_Q390_797']
    .exterior_tolerance = 0.5
    .host_name = 'wallsurface'
    .id = 4
    .name = 'Embed-3'
    .roundoff_tolerance = 1e-06

```


---

## geometry_geo_mgr.txt
`04_状态dump\400galW7VC\geometry_geo_mgr.txt`

```python
# ==== geometry_geo_mgr.txt ====
### MANAGER GFE.Pre.geometry.geo_mgr()  -> 3 objects  [仅列名]
  OBJ 'SuperStru'
  OBJ 'Soil-1'
  OBJ 'WallSurface'
```


---

## output_field_mgr.txt
`04_状态dump\400galW7VC\output_field_mgr.txt`

```python
# ==== output_field_mgr.txt ====
### MANAGER GFE.Pre.output.field_mgr()  -> 7 objects
  OBJ 'FO-Static' : output_request
    .frequency = 0
    .method = 0
    .name = 'FO-Static'
    .number_interval = 0
    .step = ''
    .sub_output = [node_output(name='SubOut-1', nset='', reg_type=-1, var_option=-1, variables=['RF', 'RM', 'U', 'UR']), element_output(elset='', name='SubOut-2', reg_type=-1, var_option=-1, variables=['E', 'S', 'SF', 'SM'])]
    .time_interval = 1.0
    .time_points = ''
    .time_type = 0
    .type = 0
    .var_option = -1
  OBJ 'FO-DynaPla-All' : output_request
    .frequency = 0
    .method = 0
    .name = 'FO-DynaPla-All'
    .number_interval = 0
    .step = ''
    .sub_output = [node_output(name='SubOut-1', nset='', reg_type=-1, var_option=-1, variables=['A', 'AR', 'CF', 'RF', 'RM', 'U', 'UR', 'V', 'VR']), element_output(elset='', name='SubOut-2', reg_type=-1, var_option=-1, variables=['E', 'ELEN', 'EMSF', 'EVOL', 'LE', 'LEP', 'MPSTATUS', 'PE', 'PEEQ', 'PEEQR', 'S', 'SDV', 'STATUS']), element_output(elset='jiegou', name='SubOut-3', reg_type=0, var_option=-1, variables=['DAMAGEC', 'DAMAGET', 'E', 'ELEN', 'EMSF', 'EVOL', 'IsRemoved', 'LE', 'NFORC', 'PE', 'PEEQ', 'S', 'SDEG', 'SDV', 'SE', 'SF', 'SM', 'STATUS'])]
    .time_interval = 0.10000000149011612
    .time_points = ''
    .time_type = 0
    .type = 0
    .var_option = -1
  OBJ 'FO-DynaPla-Jiegou' : output_request
    .frequency = 0
    .method = 0
    .name = 'FO-DynaPla-Jiegou'
    .number_interval = 0
    .step = 'Step-1'
    .sub_output = [node_output(name='SubOut-1', nset='StoryDrift-AllFloor', reg_type=0, var_option=-1, variables=['U'])]
    .time_interval = 0.019999999552965164
    .time_points = ''
    .time_type = 0
    .type = 0
    .var_option = -1
  OBJ 'FO-DynaPla-ShearForce' : output_request
    .frequency = 0
    .method = 0
    .name = 'FO-DynaPla-ShearForce'
    .number_interval = 0
    .step = ''
    .sub_output = [element_output(elset='StoryShear-All', name='SubOut-1', reg_type=0, var_option=-1, variables=['NFORC1', 'NFORC2'])]
    .time_interval = 0.019999999552965164
    .time_points = ''
    .time_type = 0
    .type = 0
    .var_option = -1
  OBJ 'EO-DynaPla-Max' : output_request
    .frequency = 0
    .method = 2
    .name = 'EO-DynaPla-Max'
    .number_interval = 0
    .step = ''
    .sub_output = [element_output(elset='jiegou', name='SubOut-1', reg_type=0, var_option=-1, variables=['DAMAGEC', 'DAMAGET', 'SDEG', 'SF', 'SM']), node_output(name='SubOut-2', nset='jiegou', reg_type=0, var_option=-1, variables=['A', 'RF', 'U'])]
    .time_interval = 0.0
    .time_points = ''
    .time_type = 0
    .type = 2
    .var_option = -1
  OBJ 'EO-DynaPla-Min' : output_request
    .frequency = 0
    .method = 3
    .name = 'EO-DynaPla-Min'
    .number_interval = 0
    .step = ''
    .sub_output = [element_output(elset='jiegou', name='SubOut-1', reg_type=0, var_option=-1, variables=['DAMAGEC', 'DAMAGET', 'SDEG', 'SF', 'SM']), node_output(name='SubOut-3', nset='', reg_type=-1, var_option=-1, variables=['A', 'RF', 'U'])]
    .time_interval = 0.0
    .time_points = ''
    .time_type = 0
    .type = 2
    .var_option = -1
  OBJ 'FieldOutput-1' : output_request
    .frequency = 0
    .method = 0
    .name = 'FieldOutput-1'
    .number_interval = 0
    .step = ''
    .sub_output = [contact_output(general_contact=True, name='SubOut-1', reg_type=3, surface='', var_option=-1, variables=['CFN', 'CFORCE', 'CSDMG', 'CSQUADSCRT', 'CSTRESS'])]
    .time_interval = 0.10000000149011612
    .time_points = ''
    .time_type = 0
    .type = 0
    .var_option = -1

```


---

## output_history_mgr.txt
`04_状态dump\400galW7VC\output_history_mgr.txt`

```python
# ==== output_history_mgr.txt ====
### MANAGER GFE.Pre.output.history_mgr()  -> 2 objects
  OBJ 'HistoryOutput-1' : output_request
    .frequency = 0
    .method = 0
    .name = 'HistoryOutput-1'
    .number_interval = 0
    .step = ''
    .sub_output = [energy_output(elset='', name='SubOut-11', per_element_set=False, reg_type=-1, var_option=-1, variables=['ALLEN'])]
    .time_interval = 0.10000000149011612
    .time_points = ''
    .time_type = 0
    .type = 1
    .var_option = -1
  OBJ 'HistoryOutput-2' : output_request
    .frequency = 0
    .method = 0
    .name = 'HistoryOutput-2'
    .number_interval = 0
    .step = ''
    .sub_output = [node_output(name='SubOut-12', nset='NodeSet-1', reg_type=1, var_option=-1, variables=['A', 'RF', 'U', 'V'])]
    .time_interval = 0.0020000000949949026
    .time_points = ''
    .time_type = 0
    .type = 1
    .var_option = -1
#   getter out_req_mgr() threw TypeError
```
