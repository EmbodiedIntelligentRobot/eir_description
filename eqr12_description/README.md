# EQR12 quadruped model

ROS 2 URDF and MuJoCo MJCF descriptions of the EQR12 quadruped: 17 links,
12 revolute joints, four fixed foot joints, and a total mass of **42.64976029 kg**.

| Resource | Purpose |
| --- | --- |
| [eqr12.urdf](urdf/eqr12.urdf) | ROS 2 geometry, joints, and inertial parameters |
| [eqr12.xml](urdf/eqr12.xml) | MuJoCo scene, actuators, sensors, and dynamics |
| [Model notes](urdf/eqr12_model_notes.md) | Parameter conventions, interfaces, and validation scope |
| `meshes/*_simplified.STL` | 17 hollow exterior visual meshes, 298,958 triangles in total |

## Update on 2026-11-25

- Restore the CAD exterior of the four hip motors, four thigh motors, and four
  chassis motors: end-cap steps, perimeter lugs, casing grooves, and connector profiles.
  Replace nine STL assets. Keep a single exterior surface without internal parts;
  internal openings remain capped and small holes are simplified.
- Current resources: **17 binary STL files, 298,958 visual triangles, 14.26 MiB**.
  Preserve the silver-gray materials, calf and foot meshes, and all URDF/MJCF bytes,
  including inertia, collisions, joints, drives, sensors, and `home`.
- Regenerate the root README prone GIF from these meshes. Closed-surface and
  self-intersection checks pass; motor radial profiles improve against source CAD.
  MuJoCo 3.8.1 zero/home tests each run 1,000 steps with identical before/after states.
  Isaac Sim 5.1.0 passes URDF import, material/mass/joint checks, four-view rendering,
  and 1,000 passive simulation steps. URDF/MJCF/USD assembly coordinates match.
  No FPS, closed-loop, or hardware test was performed; these are display surfaces,
  not manufacturing geometry. The dated records below describe earlier versions.

## Update on 2026-11-23

- Remove internal CAD assemblies from the body, motors, legs, and feet. Keep closed,
  single-layer exterior display surfaces, the main silhouette, and rubber sole
  tread blocks and grooves.
  Restore the CAD calf case and covers, close the assembly openings, and remove
  enclosed internal surfaces. The calf shell follows the source thickness variation.
  Hollow here means no internal parts or inner walls; it does not specify a manufacturable wall thickness.
- Keep the existing silver-gray material values. This is geometry cleanup, without
  real-robot photo matching or recoloring.
- Reduce active visual triangles from **181,092 to 109,624 (39.5%)**. Remove 17 original
  CAD files and 17 unused convex files, leaving **17 STL files, 5.23 MiB** instead of
  **51 files, 95.80 MiB (94.5%)**. The old size includes the full Git LFS base mesh,
  not its 133-byte pointer. Retain the existing `_simplified.STL` names and link frames.
- Keep the source URDF/MJCF byte-identical, including all masses, inertias, joints,
  53 collision primitives, drives, sensors, and `home`. No inertia is recomputed from
  the new surface meshes and no fixed links are merged in the source model.
- Add the EQR12 entry, model details, and a prone rotation preview to the root README.
  The GIF uses the current CAD zero pose, 480×480, 150 frames, 30 ms/frame. Camera and
  placement changes apply only during rendering; the standing `home` keyframe is unchanged.

A subsequent part-by-part review found that the initial convex foot shell erased
sole grooves and that the calf reconstruction introduced thickness errors and ripples.
Those meshes are replaced: each foot has 8,000 triangles and each calf 14,636. The
foot cover is a closed envelope with a 0.15 mm overlap allowance at the rubber seat.
More triangles are retained to preserve exterior geometry. The two robots share the
same source calf geometry; their final calves use matching left/right mirrored shells.

Historical CSV/JSON data below retain their original values and dates. Their old CAD
filenames/hashes can be traced in Git history; they are not the current mesh manifest
or current validation result. Runtime descriptions are `eqr12.urdf` and `eqr12.xml`.

## Update on 2026-11-12

- Identify leg joints 1/2/3 as A/H/K roles of the **HY-N8513-X32-IP67** motor.
  The MJCF classes use the suffixes `-A`, `-H`, and `-K`; all existing joint,
  actuator, link, and sensor interface names remain unchanged.
- Use the selected hardware peaks: **180 N*m** output torque and **120 RPM**
  (**12.5663706143592 rad/s**) in the URDF limits and MJCF metadata. The motor's
  rated output torque is **48 N*m**; the peak is not a continuous-duty rating.
- Retain motor-side torque input. All twelve actuator gears are **32** and their
  input range is **+/-5.625 N*m**, giving **+/-180 N*m** at the joint. Actuator force
  sensors remain motor-side; multiply by 32 for joint-side torque.
- Set joint armature to **0.11173888 kg*m^2**, calculated as
  `109.12 kg*mm^2 * 1e-6 * 32^2`. Keep the existing role-specific passive damping
  and friction loss. Link inertials, total mass, meshes, and collision geometry
  retain their values.
- Match mjlab's nominal **0.005 s** timestep, `implicitfast` integrator, and
  `Newton` solver. Keep this package's torque-driven scene and self-collision
  settings; position PD, randomization, and the Python velocity limiter are not
  added. The URDF/XML velocity value is metadata and does not clamp MuJoCo speed.

These hardware peak limits intentionally differ from mjlab's current training
limits of 150 N*m and 11.513 rad/s. The separate training project is unchanged.
The 5.3:1 wheel motor in the supplied table is not used by this twelve-joint
point-foot model.

## Update on 2026-11-10

- Replace the base enclosure mesh and regenerate its simplified and convex variants:
  **968,206**, **96,820**, and **604** triangles, respectively. The simplified mesh
  has approximately one tenth of the original triangle count. Coordinates and
  overall dimensions remain **489 x 303 x 198 mm**.
- Update `base_link` mass, center of mass, and central inertia from the revised CAD
  report in both URDF and MJCF. Base mass changes from **20.687890** to
  **20.64631829 kg**; total mass changes from **42.691332** to **42.64976029 kg**.
- Set the joint-side MuJoCo `armature` to **0.11174 kg*m^2** for each of the twelve
  actuated joints. This explicit simulation setting is separate from CAD rigid-body
  inertia; damping, friction, gear ratios, and torque limits retain their values.
- Keep all 17 simplified visual meshes and the existing 53 collision primitives.
  The base collision model remains a union of 17 boxes. Convex meshes are retained
  as resources and are not referenced by the current URDF or MJCF.

## Build and run

With ROS 2 Humble build dependencies installed, run from the repository root:

```bash
source /opt/ros/humble/setup.bash
colcon build --packages-select eqr12_description
source install/setup.bash
```

Overlay installation removes the 34 explicitly retired CAD/whole-link hull files
from this package's install directory, so deleted internal geometry is not retained
from an earlier install. Other user-provided files are preserved. Copy installs,
`--symlink-install`, `cmake --install --prefix`, and `DESTDIR` staging were checked.

Activate a Python environment with MuJoCo, then run from the repository root:

```bash
python -m mujoco.viewer --mjcf=eqr12_description/urdf/eqr12.xml
```

The exterior revision is tested with MuJoCo **3.8.1**; the historical motor update
was tested with 3.11.0. MuJoCo 4.0.0 has not been retested for this revision.
Geom group 1 contains visuals and group 3 contains robot collision geometry. The `home` keyframe must be selected explicitly; it does not supply a
standing controller.


## Isaac Sim

Import `urdf/eqr12.urdf` into Isaac Sim. This package does not provide USD assets;
previously exported external USD files must be regenerated to include the new meshes.
URDF does not encode MJCF armature, solver, motor-side gear mapping, or sensors.
A training asset needs those settings configured separately. The passive test USD
is not a fully configured training asset.

## Validation scope

The 2026-11-25 motor checks are listed in the latest update above.
The 2026-11-23 exterior checks and limitations are retained below. Collision shapes remain engineering approximations.

- All 17 visuals pass closed-surface, consistent-winding, self-intersection, and
  exterior-component visibility checks. Three body sections show only the exterior
  boundary. Each part is compared with its original CAD in six orthographic views;
  zero/home assembly views are also inspected. These checks compare CAD appearances,
  not real-robot photos. Earlier whole-model silhouette scores missed the foot/calf
  defects and are not used as evidence that local exterior details are preserved.
- Thirteen calf sections (X=0–300 mm, every 25 mm) have maximum outer Y-boundary
  error **0.305 mm** against the CAD case; the old EQR12 shell had **2.004 mm**.
  All eight calf meshes across EQR12/EQR12W have exactly matching mirrored vertices.
  For the front-left ground-facing foot region (Z < -15 mm), the 99th-percentile
  sampled surface distance is **0.190 mm**, versus **2.753 mm** for the old hull.
  The sample includes closed recesses, so this percentile is not a global error bound.
  Old calf and foot meshes fail the new local checks; all four feet retain sole tread.
  Foot tread is checked against each foot's own CAD: the source left/right tread
  is not an exact mirror, so the wheel/calf mirror claim does not apply to feet.
- ROS `check_urdf`, CMake build/install, installed mesh references, and installed
  MJCF loading pass. URDF and MJCF source files are byte-identical to the baseline.
- MuJoCo 3.8.1 compiled inertials, joints, collision shapes, actuators, and sensors
  match the baseline. Zero/home each run 1,000 steps with the same small bounded
  input (0.005 s/step, 5 s per pose): state difference **0**, no numerical warnings.
- Isaac Sim 5.1.0 imports the actual URDF, preserves all 17 visual meshes/materials,
  and verifies 12 driven DOFs and runtime mass **42.64975739 kg**, matching the source
  within floating-point precision. Four RTX views and 1,000 passive PhysX steps
  (0.005 s/step, 5 s) pass. The test uses a floating base, merged fixed joints,
  disabled drives and self-collision, and changes only the external test USD.
  The importer reports axis realignment for fixed foot joints.
- All 150 GIF frames decode and fit inside the camera view. Rendering leaves source
  model files and meshes unchanged.

FPS, closed-loop standing/walking, policy performance, self-collision configuration,
hardware calibration, and physical robot operation have not been validated by these
checks. Mesh reduction does not imply the same percentage increase in frame rate.
