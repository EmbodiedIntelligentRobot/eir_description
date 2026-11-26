# AIQ11 Pro Sensor Frames

## 腿部参数

腿部 armature、frictionloss、damping 来自双腿台架重测，须配合驱动参数使用；`damping` 是被动阻尼 B，
不是训练 Kd。各关节参数定义在 `urdf/aiq11_pro.xml` 与 `urdf/aiq11_pro_simplified.xml` 中。

## 质量与惯量（2026-11-05）

各连杆的质量、质心和惯量基于 2026-11-05 修订版 CAD 装配体质量属性更新，活动关节保持既有角度限位。

- 数据块坐标系对应同名 link（`base_frame`→`base_link`，`imu_frame`→`imu_l0`）。取质心处、对齐 link 坐标系的 Lxx…Lzz，并将惯性积取反写入张量；MJCF 沿用原有惯量表示及合并方式（IMU 并入 `base_link`、脚掌并入 `*_leg_l6`），仅新整手和拆出旧手掌后的腕部使用完整惯性张量。
- 双手的 CAD 质量和惯量分别集中在固定连接的 `l_hand_l0`、`r_hand_l0` 上，质量均为 **0.58650977 kg**，左右手局部质心和惯量数值一致。左右手原有的 16 个手指 link/body 名称、坐标系、父子层级和零位外观保留。
- 完整 `aiq11_pro.urdf` 和 `aiq11_pro.xml` 按要求恢复 16 个手指活动关节，沿用原坐标、转轴和限位；完整 XML 恢复原有 10 个手指电机，共 42 个执行器，同名坐标 site 继续保留。为满足 MuJoCo 的活动刚体惯性要求，每个手指 link/body 在其局部原点增加数值正则项：质量 `1e-5 kg`，对角惯量各 `1e-9 kg·m²`，非对角项为零。16 个连杆共增加 `0.00016 kg`（0.16 g，约占整机质量 0.000365%），不改动 CAD 整手集中惯量；这些极小值用于模型加载和近似运动，不代表真实指节质量分布。已用 MuJoCo 3.10.0 验证无驱动和手指驱动各 0.5 秒仿真无警告。
- `aiq11_pro_pin.urdf` 和 `aiq11_pro_simplified.xml` 保持固定手指配置，原手指坐标系仍可用于定位；简化 MJCF 为 32 个执行器，可正常加载。手腕关节继续保留。未使用仅包含手掌底座的 `*_hand_l0_simplified.STL` 替代整手外观。
- `*_arm_l7` 只保留 CAD 腕部自身惯性，不再重复包含旧手掌。前后 336 相机未列入 CAD 资料，保留各 0.10348 kg。
- 整手惯量坐标系按用户要求以左侧为准：左右 `hand_0` 固定连接均为零旋转，右侧原有的 Z 轴 0.18229 rad 旋转已移除，URDF 与 MJCF 同步。
- `l_arm_l5` 使用修订 TXT 的原值，不再额外沿 Y 方向镜像：质量 0.34324948 kg，质心 Y 为 +0.00022567 m。`l_arm_l51`、`l_arm_l52`、`l_arm_l6` 同样按资料原值同步。腕部网格及左侧辅助关节安装位置已按 `aiq12jh-j` 导出资料更新，详见下文。
- 完整 URDF 和 MJCF 的机器人质量均为 **43.82076678 kg**，即新版 TXT 的各部件质量合计 43.61364678 kg，加两台相机的 0.20696 kg，再加手指数值正则质量 0.00016 kg。
- `aiq11_pro_pin.urdf`、`aiq11_pro_simplified.xml` 按既有结构省略 20 个辅助连杆（共 0.51906589 kg），机器人质量均为 **43.30154089 kg**。楼梯、CREF 场景通过 attach 引用主模型，自动生效。

## 腕部网格更新（2026-11-05）

更新范围为腕部与三指灵巧手网格。范围为左右 `arm_l5/l51/l52/l6/l7` 和全部 `fg` 网格，共 26 个；原始 STL 与对应 `_simplified.STL` 保持一致来源，各简化文件保留更新前的三角面数。`arm_l5/l51/l52/l6` 分别为 3452/400/200/2456 面。

新左右腕部几何在各自局部坐标系中同向。与现有源文件逐字节相同的 18 个网格保留原有简化结果；其余腕部几何经三角面坐标核对与原右侧几何相同，复用对应右侧简化结果，避免重复减面引入额外误差。新源文件 `l_arm_l5.STL` 另含一段位于 Y=-0.502～-0.478 m 的重复 `arm_l52`（730 面），替换版本仅保留 34520 面的腕部主体，下载目录中的原文件未改动。

完整 URDF/MJCF 同步左侧 `arm_51` 安装位置为 `(0, -0.0145, -0.0355)`，`arm_52` 为 `(0.015, -0.008, 0)`；MJCF 左腕闭链锚点同步为 `(0.001, -0.0015, -0.055)`。控制轴、限位、驱动和质量惯量保持原值。Pin 版及简化 MJCF 无这两个辅助关节，通过共享网格获得更新。未使用的 `_convex.STL` 不在此次替换范围内。

## 视觉网格、配色与碰撞体优化（2026-11-20）

- 完全剔除电机、轴承、PCB、散热片、内部连杆与螺钉等全部不可见内构与零件细节，并对双层带孔 `torso_l3` 与 `neck_l3` 重构光滑封闭单层外包络（相机槽由单层外壳切分凹槽，修剪饰件内伸凸耳）；移除旧高精度 `<link>.STL`、未使用 `*_convex.STL` 及多色连杆冗余 `*_simplified.STL`，`meshes/` 由 `302` 个减至 `117` 个活动文件（`5087.3 KB` / `4.97 MB`，含 `42` 个 `*_simplified.STL` 与 `75` 个 `*_vis_<color>.STL`）。`aiq11_pro.xml` 与 `aiq11_pro_simplified.xml` 分别使用 `117` 网格（`103,992` 面，较原 `331,689` 面 `-68.6%`）和 `97` 网格（`97,273` 面，较原 `322,575` 面 `-69.8%`）。
- 按实机照片应用 `aiq_*` 材质组（白/草绿壳体、橄榄绿手掌、白色指节、浅薄荷指尖、蓝色鞋面与深灰鞋底等）；前胸相机槽上方新增贴合曲面的白色 `EIR TECHNOLOGY` 三维标识（`torso_l3_vis_white.STL`）；头部 `neck_l3` 前脸面板保持素白（`aiq_white`）先不上色，保留绿色眉弓、上方大耳与两侧绿色颞部小耳朵（`neck_l3_vis_green.STL`）以及深灰颈圈（`neck_l3_vis_dark.STL`）。
- 全部模型碰撞体替换为极简基本体（MJCF `23` 个 + `24` 组 `<contact><exclude>`，URDF `23` 个，`0` 个网格碰撞体），保持 `group="1"/"2"`、触地高度（MJCF `leg_l6 z=-0.044 m`，URDF `foot_l0 z=-0.017 m`）及全套质量惯量、关节、闭链和物理/传感器参数不变（脚底中段碰撞体采用纵向胶囊/圆柱）。

## 头部曲面表情投影更新（2026-11-25）

- 对照实机亮屏照片与表情源图，将 `neck_l3` 单层闭合外包络沿绿色波浪眉弓下缘及两侧眉梢经饱满脸颊至下巴的光滑超椭圆圆弧无缝切分为素白后脑/下颌壳（`neck_l3_vis_white.STL`，`5,651` 面）与前脸曲面投影罩（`neck_l3_vis_face.obj`，`1,460` 面，经 `216` 个共享接缝顶点切向光顺，配套 `neck_l3_vis_face.mtl` 与边界钳位多尺度调和延拓默认贴图 `neck_l3_vis_face.png`，`768×510`），横向铺满至两侧眉弓外缘并采用与高度无关的无失真共形 UV 投影贴合饱满脸颊与下颌圆弧，壳内保持单层无内壁重叠。
- 除默认微笑表情（`neck_l3_vis_face.png` / 材质 `aiq_face`）外，`meshes/faces/` 收录经鼻梁配准与边界调和延拓的 `14` 张同尺寸（`768×510`）静态预设表情贴图（共 `15` 套静态表情），并在 `aiq11_pro.xml` 与 `aiq11_pro_simplified.xml` 中预注册对应纹理与材质，同时为前脸几何体赋名 `neck_l3_vis_face`：

| 序号 | 贴图路径（相对于 `meshes/`） | MJCF 纹理名 | MJCF 材质名 | 表情说明 |
| --- | --- | --- | --- | --- |
| 00 | `neck_l3_vis_face.png` | `aiq_face_tex` | `aiq_face` | 默认微笑（初始加载） |
| 01 | `faces/face_01_angry.png` | `aiq_face_tex_angry` | `aiq_face_angry` | 生气 / 严肃 |
| 02 | `faces/face_02_cute.png` | `aiq_face_tex_cute` | `aiq_face_cute` | 乖巧抿嘴笑 |
| 03 | `faces/face_03_worried.png` | `aiq_face_tex_worried` | `aiq_face_worried` | 担忧 / 委屈 |
| 04 | `faces/face_04_skeptical.png` | `aiq_face_tex_skeptical` | `aiq_face_skeptical` | 半睁眼狐疑 |
| 05 | `faces/face_05_glance.png` | `aiq_face_tex_glance` | `aiq_face_glance` | 斜视打量 |
| 06 | `faces/face_06_sleepy.png` | `aiq_face_tex_sleepy` | `aiq_face_sleepy` | 困倦半闭眼 |
| 07 | `faces/face_07_happy.png` | `aiq_face_tex_happy` | `aiq_face_happy` | 开心露舌笑 |
| 08 | `faces/face_08_laugh.png` | `aiq_face_tex_laugh` | `aiq_face_laugh` | 欢快大笑 |
| 09 | `faces/face_09_surprised.png` | `aiq_face_tex_surprised` | `aiq_face_surprised` | 惊讶圆嘴 |
| 10 | `faces/face_10_nervous.png` | `aiq_face_tex_nervous` | `aiq_face_nervous` | 紧张抿嘴 |
| 11 | `faces/face_11_curious.png` | `aiq_face_tex_curious` | `aiq_face_curious` | 好奇小嘴 |
| 12 | `faces/face_12_squint.png` | `aiq_face_tex_squint` | `aiq_face_squint` | 紧闭挤眼 |
| 13 | `faces/face_13_sad.png` | `aiq_face_tex_sad` | `aiq_face_sad` | 难过张嘴 |
| 14 | `faces/face_14_blink.png` | `aiq_face_tex_blink` | `aiq_face_blink` | 闭眼微笑 / 眨眼 |

- MuJoCo 动态切换示例（主模型可直接改 `geom_matid` 零拷贝切换预设材质；`<attach>` 地形场景或自定义帧动画可直接刷新 `aiq_face_tex` 像素缓冲区）：

```python
face_gid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_GEOM, "neck_l3_vis_face")
m.geom_matid[face_gid] = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_MATERIAL, "aiq_face_happy")
```

- `meshes/` 现共 `136` 个活动文件（`119` 个 STL、`1` 个 OBJ、`1` 个 MTL、`15` 个 PNG，合计 `9494.2 KB` / `9.27 MiB`），完整版与简化/Pin 版分别编译 `120` 网格（`112,157` 面）与 `100` 网格（`105,438` 面）；碰撞体、质量惯量、关节、驱动、闭链及传感器参数与云端最新保持零改动。

## Sensor Frame Conventions

All sensor frames use the local coordinate system of their Gemini link and
retain its orientation. `*_link` is used consistently in URDF and as the
MuJoCo site name.

## Frame Purpose

- `*_rgb_camera_link`: RGB camera optical origin.
- `*_depth_camera_link`: depth camera optical origin.
- `*_laser_emitter_link`: laser emission origin. In simulation, use this
  frame as the ray origin when constructing a depth scanning camera.

## Offsets

For `gemini_336_lf` and `gemini_336_lb`, whose link origin is the RGB camera
origin:

| Frame | Local XYZ (m) |
| --- | --- |
| RGB camera | `0 0 0` |
| Depth camera | `-0.014 0 0` |
| Laser emitter | `0.011 0 0` |

For `gemini_336l_l0`, whose link origin is the depth camera origin:

| Frame | Local XYZ (m) |
| --- | --- |
| Depth camera | `0 0 0` |
| RGB camera | `0.02375 0 0` |
| Laser emitter | `0.0475 0 0` |

## MuJoCo Stair Test

The full MJCF defaults to flat ground: ramps, platforms, stairs, the sofa and
the perception validation cube are commented out in `urdf/aiq11_pro.xml`.
The retained stair course has ten boxes and a landing: 0.10 m rise per step,
0.50 m landing height, first front edge at x=2 m, centreline y=0.
Terrain uses group 0 so the parkour policy's group 0/1 rays can detect it.
Before generating a full stair-test scene, uncomment the stair block marked
`Disabled for flat-ground regression; enable for stair tests.` The script
changes the start position only and does not enable commented geometry.

The full model starts at `(0, 0, 0.85)`; its default viewer camera follows
`base_link`. Interactive mouse orbit while tracking requires the updated
`eir_mujoco` viewer. The policy uses the robot's front Gemini site independently.
The wrist rotor inertia is on driven `arm_51`, with zero on passive `arm_6`.

The simplified MJCF starts at `(0, 0, 0.95)`.
The helper below generates a separate model 0.8 m before its own first stair,
aligned with the stair centreline, preserving the source base height:

```bash
python3 aiq11_pro_description/scenes/make_stair_scene.py \
  --variant full --output /tmp/aiq11_pro_stairs.xml
python3 aiq11_pro_description/scenes/make_stair_scene.py \
  --variant simplified --output /tmp/aiq11_pro_simplified_stairs.xml
```

Commands above run from the repository root. After building the ROS package,
the script is also installed under
`$(ros2 pkg prefix --share aiq11_pro_description)/scenes/`.
Pass the generated XML path to the MuJoCo viewer or simulator's model loader.
Existing output files are not overwritten. The generated XML references the
current package's assets using absolute paths; regenerate it after moving the
package or updating the canonical model. Stair geometry, joint limits and
dynamics are inherited from the selected model.

The start position is a `base_link` body offset. These models use three slide
joints and a ball joint for the floating base, so base translation in `qpos`
is relative to this offset. A simulator that overwrites `qpos` on reset must
account for that offset when requesting an absolute world position.

### 10级往返楼梯

`urdf/aiq11_pro_stairs10.xml` 使用原PRO机器人和物理选项，仅引用新的
`urdf/terrains/stairs_10x15cm_landing2m.xml` 地形。上行10次抬升，每次0.15 m，
相邻踏面长0.30 m，顶高1.50 m，平台长2.00 m，另一侧对称下降10次。
平台作为第10级顶面，前后各9块独立踏面；第10次下降回到地面。宽2.00 m，
起始立面 x=2.00 m，平台 x=4.70～6.70 m，终点 x=9.40 m。
旧15级场景保留；资源加载通过不代表完整上下楼运动验收。
