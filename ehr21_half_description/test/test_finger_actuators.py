"""EHR21 finger motors select the bridge PD path instead of qpos overwrite."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

try:
    import mujoco
    import numpy as np
except ImportError:
    mujoco = None

MODEL = Path(__file__).resolve().parents[1] / 'urdf/ehr21_half.xml'
FINGERS = [f'{side}_{finger}_joint' for side in ('left', 'right')
           for finger in ('thumb_1', 'thumb_2', 'index_1', 'middle_1', 'ring_1', 'little_1')]


class FingerActuatorTest(unittest.TestCase):
    def test_all_active_fingers_have_named_torque_limited_motors(self):
        root = ET.parse(MODEL).getroot()
        motors = root.findall('actuator/motor')
        self.assertEqual(len(motors), 31)
        for name in FINGERS:
            matches = [m for m in motors if m.get('joint') == name]
            self.assertEqual(len(matches), 1, name)
            self.assertEqual(matches[0].get('name'), name)
            self.assertEqual(matches[0].get('gear'), '1')
            self.assertEqual(matches[0].get('ctrllimited'), 'true')
            self.assertEqual(matches[0].get('ctrlrange'), '-1 1')
        passive = {c.get('joint1') for c in root.findall('equality/joint')}
        self.assertFalse(passive.intersection(m.get('joint') for m in motors))

    @unittest.skipIf(mujoco is None, 'Python MuJoCo not installed')
    def test_pd_closure_does_not_curl_torso(self):
        # Same model and body damping; change only finger drive after 3 s.
        def run(close):
            model = mujoco.MjModel.from_xml_path(str(MODEL))
            data = mujoco.MjData(model)
            ids = [mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, n) for n in FINGERS]
            finger_act = {mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, n): j
                          for n, j in zip(FINGERS, ids)}
            torso = [model.jnt_qposadr[mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, 'torso_'+str(i))]
                     for i in (1, 2, 3)]
            samples = []
            for step in range(14000):
                for act in range(model.nu):
                    joint = model.actuator_trnid[act, 0]
                    name = mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_ACTUATOR, act)
                    velocity = data.qvel[model.jnt_dofadr[joint]]
                    if act in finger_act:
                        lo, hi = model.jnt_range[joint]
                        target = (hi if hi != 0 else lo) if close and step >= 6000 else 0.
                        force = 20*(target-data.qpos[model.jnt_qposadr[joint]])-velocity
                    else:
                        damping = 5 if name.startswith('torso') else (1 if name.startswith('neck') else
                                  (3 if name.endswith(('_1', '_2', '_3', '_4')) else
                                   (2 if name.endswith('_5') else 1)))
                        force = -damping*velocity
                    lo, hi = model.actuator_ctrlrange[act]
                    data.ctrl[act] = np.clip(force/model.actuator_gear[act, 0], lo, hi)
                mujoco.mj_step(model, data)
                if step >= 6000 and step % 20 == 0:
                    samples.append(data.qpos[torso].copy())
            self.assertTrue(np.isfinite(data.qpos).all())
            self.assertFalse(data.warning.number.any())
            # At least the index finger must actually move toward closure.
            index = ids[2]
            if close:
                self.assertLess(data.qpos[model.jnt_qposadr[index]], -.5)
            return np.array(samples)
        baseline = run(False)
        closing = run(True)
        self.assertLess(float(np.abs(closing-baseline).max()), .02)


if __name__ == '__main__':
    unittest.main()
