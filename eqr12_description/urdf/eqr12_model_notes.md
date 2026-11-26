# EQR12 model notes

`eqr12.urdf` and `eqr12.xml` describe the same 17 links. The MJCF uses relative
mesh paths (`../meshes/`) and explicit inertial parameters. Its scene and actuator
layout originated from the EQR11 reference model; runtime loading requires only
this package.

## Base mass and inertia

The CAD mass properties use kg, m, and kg*m^2.
The existing correspondence between the report output frame and `base_link` is
retained. The URDF inertial frame has zero rotation relative to the link frame.

| Parameter | Value |
| --- | --- |
| Base mass / kg | 20.64631829 |
| Center of mass XYZ / m | `0.00316241 0.00419948 -0.04981856` |
| Central Ixx, Iyy, Izz / kg*m^2 | `0.16008971 0.47665242 0.55795957` |
| Central Ixy, Ixz, Iyz / kg*m^2 | `0.00031818 -0.00152430 0.00233940` |
| Total robot mass / kg | 42.64976029 |

The CAD export uses positive products of inertia. Keep the diagonal entries of
its COM-aligned `L` block and negate the off-diagonal entries to obtain the physical
inertia tensor. These values are already about the center of mass; no parallel-axis
translation is applied when writing the URDF. MJCF copies the converted tensor in
`Ixx Iyy Izz Ixy Ixz Iyz` order without another sign change.

The report's output-origin `I` block is used only for cross-checking:
`I_O = I_C + m ((c dot c) E - c c^T)`.
Its maximum component residual is **9.490e-9 kg*m^2**. Independently reconstructing
the COM tensor from the reported principal axes and principal moments gives a
maximum residual of **5.797e-9 kg*m^2**. Both are consistent with the report's
printed precision. The tensor is positive definite and satisfies the principal
moment triangle inequalities.

The other 16 link inertials retain their values. No fixed-link inertia aggregation
is performed: all four foot links remain explicit, and MJCF `fusestatic="false"`
preserves their bodies. `inertiafromgeom="false"` and zero geometry density prevent
visual or collision meshes from changing the specified masses. The URDF and MJCF
have the same total mass; the historical CSV is not an updated parameter source.

## Geometry

All visual meshes use the 17 `_simplified.STL` files: **298,958 triangles**, **14.26 MiB**
in total after the 2026-11-25 motor exterior restoration. The original 17 CAD meshes and 17
unused convex meshes have been removed. The full original resources occupied
95.80 MiB including the Git LFS base mesh; active visuals contained 181,092 triangles.

The 2026-11-25 update restores CAD end-cap steps, perimeter lugs, casing grooves,
and connector profiles on the hip, thigh, and chassis motors. Nine STL files change;
the calf/foot meshes and source URDF/MJCF stay byte-identical. Internal openings
remain capped and small holes simplified. These surfaces are not manufacturing geometry.

The body, motor, leg, and foot meshes contain only closed exterior display surfaces,
with no retained internal assemblies or inner walls. Hollow does not specify a
manufacturable wall thickness. Rubber sole tread blocks/grooves and the original
calf case/cover curves are retained; mounting recesses and internal assembly openings are closed. The first
cleanup erased the sole tread and distorted calf thickness; a subsequent review
replaced all four feet (8,000 triangles each) and calves (14,636 each). The foot
cover envelope uses 0.15 mm overlap allowance at the rubber seat. Thirteen calf
sections have maximum outer Y-boundary error 0.305 mm against the CAD case.
Small assembly details remain simplified. Existing silver-gray colors
remain unchanged; this is not real-robot photo matching. Mesh coordinates, link frames,
and all source URDF/MJCF parameters are unchanged.

The base uses the same CAD source as EQR12W (verified by SHA-256), so its validated
exterior is reused in the same local frame. The original calf geometry also matches
EQR12W, and both packages now use the same mirrored exterior calves. EQR12 feet
are processed from their own CAD geometry; the original left/right tread is not
an exact mirror.
The install step removes the 34 explicitly retired CAD/hull files from an existing
package install directory, while preserving other custom files.

Collision geometry is unchanged: 37 boxes, 12 cylinders, and four spheres,
including 17 overlapping base boxes. Same-body box overlaps do not create robot
self-contact. These shapes approximate the enclosure and leg surfaces rather
than reproducing every CAD recess or small feature. MuJoCo box sizes are half
extents; URDF box sizes are full extents. Both descriptions retain matching shapes
and poses. Visuals use Geom group 1 and collisions use group 3.

## Actuation and state layout

Leg and actuator order is `fl`, `fr`, `hl`, `hr`, with joints 1, 2, and 3 in each leg.
The floating base uses three translation joints and one ball joint: `nq=19`,
`nv=18`, and `nu=12`. Its reference position is `(8, 0, 0.465)` m.

| Joint / role | Motor class | Gear | Motor-side control range / N*m | Joint-side peak / N*m | Armature / kg*m^2 |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 / A | `HY-N8513-X32-IP67-A` | 32 | +/-5.625 | +/-180 | 0.11173888 |
| 2 / H | `HY-N8513-X32-IP67-H` | 32 | +/-5.625 | +/-180 | 0.11173888 |
| 3 / K | `HY-N8513-X32-IP67-K` | 32 | +/-5.625 | +/-180 | 0.11173888 |

All twelve joints use the same **HY-N8513-X32-IP67** motor and 32:1 reduction;
the A/H/K class suffixes distinguish their passive loss settings, not different
motor models. Joint names remain `fl_leg_1` through `hr_leg_3`. The supplied
hardware table lists rated/peak output torque of **48/180 N*m** and rated/peak
output speed of **110/120 RPM**. The user selected hardware peak limits for this
description; these replace the previous 150 N*m and 20 rad/s values.

| Role | Passive damping / N*m*s/rad | Friction loss / N*m |
| --- | ---: | ---: |
| A | 0.23 | 0.45 |
| H | 0.14 | 0.42 |
| K | 0.5 | 0.7 |

`armature` is additional inertia in the joint generalized coordinates; it does not
add body mass. The motor table's input rotating inertia is **109.12 kg*mm^2**,
giving `109.12 * 1e-6 * 32^2 = 0.11173888 kg*m^2` at the output joint. This replaces
the rounded 0.11174 value and matches mjlab's nominal armature. CAD link tensors,
COM frames, cross-term signs, and all four explicit fixed foot links are unchanged;
no inertia aggregation or additional motor body mass is introduced. Total mass
remains **42.64976029 kg** in both files. Passive damping and friction retain the
values above, independently of any active controller gains.

`ctrl` remains motor-side torque, not a position target. The old gears
18/12/19.584 become 32, so controller and force-sensor conversions must use the
new ratio. Each actuator's input clamp and each joint's force clamp both represent
the selected **180 N*m peak** output limit. Actuator force sensors report motor-side
force; multiply by 32 to obtain joint-side torque. Neither current/thermal limits
nor a speed-torque curve are modeled.

The URDF velocity limit and MJCF custom metadata now contain
`120 * 2*pi/60 = 12.5663706143592 rad/s`. MuJoCo does **not** enforce this metadata
as a speed constraint. mjlab separately applies a Python speed limiter at
11.513 rad/s; that limiter and its 150 N*m training cap are not changed by this
description update.

The standalone XML uses the mjlab nominal timestep **0.005 s**, `implicitfast`
integration, and `Newton` solver with 50 iterations. Its existing scene, collision
masks/self-collision policy, floating-base layout, sensors, and torque-input
actuators are retained. mjlab's position PD, free-joint adaptation, initial pose,
and domain randomization remain separate runtime configuration.

Foot body names are `fl_leg_lee`, `fr_leg_lee`, `hl_leg_lee`, and `hr_leg_lee`.
The `home` keyframe sets leg angles `(0, -1.3, 1.6)` rad and initially clears the
ground by approximately 10 mm. It must be selected explicitly and has zero motor
commands; a controller is required to maintain standing.

## Validation

See the [package README](../README.md#validation-scope) for the 2026-11-25 motor and 2026-11-23 exterior
validation. Current source URDF/MJCF files are byte-identical to
the pre-cleanup files, preserving the 42.64976029 kg total mass, fixed-foot inertials,
12 drives, 53 collision primitives, and 42 sensors (55 scalar outputs).

The root README preview uses the CAD zero pose lying down; only the render camera
and base height are adjusted. It does not alter `home`, the default joint pose, or
controller configuration. Tests do not establish closed-loop locomotion performance,
physical hardware calibration, FPS improvement, or MuJoCo 4.0.0 compatibility.

## Additional simulation evidence

The local 2026-11-10 MuJoCo 4.0.0 check loaded the EQR12 configuration from that date,
held suspended READY for eight seconds, and exercised local ROS panel reset and
READY re-entry. The maximum joint target error was about 0.016903 rad. These
results predate the 2026-11-12 motor-rating and solver changes and do not validate
the current configuration, hardware, or a later walking-policy replacement.
