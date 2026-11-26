"""The passive rod ends must allow spatial motion while closing both rods."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

PACKAGE = Path(__file__).resolve().parents[1]


class WaistClosedChainTest(unittest.TestCase):
    def test_both_half_models_use_unlimited_passive_ball_joints(self):
        for name in ('ehr21_half', 'ehr21g_half'):
            with self.subTest(model=name):
                root = ET.parse(PACKAGE.parent / (name + '_description') / 'urdf' / (name + '.xml')).getroot()
                for joint_name in ('torso_32', 'torso_34'):
                    joint = root.find(f'.//joint[@name="{joint_name}"]')
                    self.assertEqual(joint.get('type'), 'ball')
                    self.assertEqual(joint.get('limited'), 'false')
                    self.assertEqual(joint.get('class'), 'fake_joint_param')
                    for attribute in ('axis', 'range', 'actuatorfrcrange'):
                        self.assertNotIn(attribute, joint.attrib)
                    self.assertFalse(root.findall(f'actuator/*[@joint="{joint_name}"]'))
                for index, body in ((1, 'torso_l32'), (2, 'torso_l34')):
                    connection = root.find(f'equality/connect[@name="waist-{index}"]')
                    self.assertEqual(connection.get('body1'), body)
                    self.assertEqual(connection.get('body2'), 'torso_l1')
                    self.assertEqual(connection.get('anchor'), '-0.003 0 -0.065')
                for joint_name in ('torso_31', 'torso_33'):
                    joint = root.find(f'.//joint[@name="{joint_name}"]')
                    self.assertEqual(joint.get('type', 'hinge'), 'hinge')
                    self.assertEqual(joint.get('axis'), '1 0 0')
                    self.assertTrue(root.findall(f'actuator/motor[@joint="{joint_name}"]'))


if __name__ == '__main__':
    unittest.main()
