# AIQ11 Pro hand kinematics

`three_finger_four_bar.csv` contains the analytical active-to-passive joint
mapping for the three-finger hand four-bar linkages. Angles are in radians.
Finger numbers use the same robot-relative convention on both hands:

- `fg1`: the single-DOF main finger (`fg1_1` to passive joint `fg1_2`)
- `fg2`: the two-DOF secondary finger closest to the robot body
- `fg3`: the two-DOF secondary finger farthest from the robot body

The `main` curve applies to `fg1`. The `secondary` curve applies to the
`fg2_1`/`fg3_1` active joints and their `fg2_2`/`fg3_2` passive joints.
The numbering is independent of the viewing direction.

The table was calculated from mechanical linkage parameters and still requires
validation on the physical robot. Keep the numeric samples unchanged until
that validation is complete.
