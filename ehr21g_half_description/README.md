# ehr21g_half_description

EHR21G Half（二指平行夹爪半身操作平台）描述包，与 `ehr21_half_description` 同平台，末端执行器为 2 自由度平行夹爪（`l/r_fg_0` 主动指、`l/r_fg_1` 从动指齿轮反向联动），配备腕部 Gemini305 深度相机×2 与头部 Gemini336L 深度相机×1。

## 模型文件

- `urdf/ehr21g_half.urdf`：ROS 标准完整 URDF（35 个带惯量连杆，总质量 `53.03483401 kg`，33 个基本体碰撞）。
- `urdf/ehr21g_half_pin.urdf`：Pinocchio 17 自由度参考模型（省略腰部与腕部并联辅助分支，27 个带惯量连杆，总质量 `52.92505625 kg`）。
- `urdf/ehr21g_half.xml`：MuJoCo 控制仿真模型（总质量 `53.03483401 kg`，含 4 条腰腕 `<connect>` 闭环约束、2 条夹爪联动约束、21 路执行器及 35 个基本体碰撞）。

## 网格资源（`meshes/` 共 88 个轻量化 STL，约 3.68 MB）

- `23` 个 `*_simplified.STL`：去内构低面数单色网格（含 EHR21G 专用底座与二指夹爪网格）。
- `27` 个 `*_vis_<color>.STL`：分色外表面视觉网格（供 URDF 直接加载）。
- `meshes/ehr21/` 下 `38` 个公共低面数网格：供 `ehr21g_half.xml` 独立复用的躯干、头颈与上臂分色网格。

## 质量、质心与惯量约定

- 连杆质量、质心和惯量来自二指夹爪版 CAD 质量属性（质心处对齐输出坐标系的惯性张量，SolidWorks 正惯性积取反写入非对角项）。
- `ehr21g_half.xml` 将固定相机质量与惯量按平行轴定理合并入对应安装刚体（`gemini336l_l1` 并入 `neck_l2`，`gemini305_l1` 并入 `r_arm_l7`，`gemini305_l2` 并入 `l_arm_l7`），并以 `fullinertia` 表达。
- `r_arm_l5`、`r_arm_l51`、`r_arm_l6` 在 `ehr21g_half.xml` 中沿用 EHR21 右腕局部坐标系（相对 URDF 局部 Y 偏移 `-0.0058709 m`）。

## 夹爪闭合说明

主动指 `*_fg_0` 行程为 `[-0.1299, 0.9076] rad`，零角度并非完全闭合位。控制模型排除了 `l_fg_l0/l_fg_l1` 与 `r_fg_l0/r_fg_l1` 同侧指间简化碰撞盒自接触，保留与外部物体及其他连杆的碰撞。

## 测试

```bash
python3 -m unittest discover -s test -p 'test_*.py'
```
