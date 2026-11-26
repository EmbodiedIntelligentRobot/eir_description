# ehr21_half_description

EHR21 Half（天行者二号半身灵巧手平台）描述包，基于移动升降底座，搭载 3 自由度腰部（含并联机构）、3 自由度颈部、双臂各 7 关节（含腕部并联机构）、因时灵巧手及头部 Gemini336L 深度相机。

## 模型文件

- `urdf/ehr21_half.urdf`：ROS 标准完整 URDF（68 连杆，42 个基本体碰撞，`0` 个网格碰撞体）。
- `urdf/ehr21_half_pin.urdf`：Pinocchio 19 自由度参考模型（59 连杆，去除腰/腕并联辅助分支，保留 41 个基本体碰撞）。
- `urdf/ehr21_half.xml`：MuJoCo 完整版控制仿真 MJCF（总质量 `50.364033 kg`，含闭环约束、执行器、IMU/关节传感器及 41 个基本体碰撞）。

## 网格资源（`meshes/` 共 74 个，2.47 MB）

- `19` 个 `*_simplified.STL`：去除电机定转子、PCB、紧固件等全部内构后的低面数单色网格。
- `31` 个 `*_vis_<color>.STL`：实机参考分色外表面视觉网格（单层封闭 `torso_l3`/`neck_l2` 外壳、胸前红色 `EIR TECHNOLOGY` 三维标识、黑头壳+亮黑面罩及手掌腕部分色）。
- `24` 个 `left_/right_*.STL`：轻量化灵巧手指节网格。

## 测试

```bash
python3 -m unittest discover -s test -p 'test_*.py'
```
