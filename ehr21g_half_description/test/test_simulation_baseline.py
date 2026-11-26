"""Verify EHR21G lightweight URDF/MJCF mass properties and shared EHR21 structure."""
from copy import deepcopy
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET


PACKAGE = Path(__file__).resolve().parents[1]
BASELINE = PACKAGE.parent / "ehr21_half_description"


def structure(element):
    return (element.tag, element.attrib, [structure(child) for child in element])


class SimulationBaselineTest(unittest.TestCase):
    def test_mass_properties_consistency(self):
        """Check URDF, Pin URDF, and MJCF inertial counts and total masses."""
        urdf_root = ET.parse(PACKAGE / "urdf/ehr21g_half.urdf").getroot()
        urdf_links = {
            link.get("name"): link.find("inertial")
            for link in urdf_root.findall("link")
            if link.find("inertial") is not None
        }
        self.assertEqual(len(urdf_links), 35)
        self.assertAlmostEqual(
            sum(float(inrt.find("mass").get("value")) for inrt in urdf_links.values()),
            53.03483401,
            places=8,
        )

        pin_root = ET.parse(PACKAGE / "urdf/ehr21g_half_pin.urdf").getroot()
        pin_links = [link for link in pin_root.findall("link") if link.find("inertial") is not None]
        self.assertEqual(len(pin_links), 27)
        self.assertAlmostEqual(
            sum(float(link.find("inertial/mass").get("value")) for link in pin_links),
            52.92505625,
            places=8,
        )
        for link in pin_links:
            name = link.get("name")
            ref = urdf_links[name]
            actual = link.find("inertial")
            self.assertAlmostEqual(
                float(actual.find("mass").get("value")),
                float(ref.find("mass").get("value")),
                places=10,
            )

        mjcf_root = ET.parse(PACKAGE / "urdf/ehr21g_half.xml").getroot()
        bodies = [b for b in mjcf_root.findall(".//body") if b.find("inertial") is not None]
        self.assertEqual(len(bodies), 32)
        self.assertAlmostEqual(
            sum(float(b.find("inertial").get("mass")) for b in bodies),
            53.03483401,
            places=8,
        )

        merged_cameras = {
            "neck_l2": float(urdf_links["gemini336l_l1"].find("mass").get("value")),
            "l_arm_l7": float(urdf_links["gemini305_l2"].find("mass").get("value")),
            "r_arm_l7": float(urdf_links["gemini305_l1"].find("mass").get("value")),
        }
        for body in bodies:
            name = body.get("name")
            actual = body.find("inertial")
            expected_mass = float(urdf_links[name].find("mass").get("value")) + merged_cameras.get(name, 0.0)
            self.assertAlmostEqual(float(actual.get("mass")), expected_mass, places=9)

    def test_base_mesh_is_ehr21g_specific(self):
        original = ET.parse(BASELINE / "urdf/ehr21_half.xml").getroot()
        gripper = ET.parse(PACKAGE / "urdf/ehr21g_half.xml").getroot()
        original_asset = original.find('asset/mesh[@name="base_link_simplified"]')
        gripper_asset = gripper.find('asset/mesh[@name="base_link_simplified"]')

        self.assertEqual(gripper_asset.get("file"), "base_link_simplified.STL")
        ehr21_mesh = BASELINE / "meshes" / original_asset.get("file")
        ehr21g_mesh = PACKAGE / "meshes" / gripper_asset.get("file")
        self.assertTrue(ehr21g_mesh.is_file())
        self.assertNotEqual(ehr21_mesh.read_bytes(), ehr21g_mesh.read_bytes())

    def test_shared_control_structure_matches_ehr21(self):
        original = ET.parse(BASELINE / "urdf/ehr21_half.xml").getroot()
        gripper = ET.parse(PACKAGE / "urdf/ehr21g_half.xml").getroot()
        for section in ("compiler", "option", "size", "visual", "default", "keyframe"):
            self.assertEqual(
                structure(original.find(section)),
                structure(gripper.find(section)),
                section,
            )

        hand_joints = set()
        for side in ("l", "r"):
            terminal = original.find(f'.//body[@name="{side}_arm_l7"]')
            for child in terminal:
                if child.tag != "joint":
                    hand_joints.update(joint.get("name") for joint in child.iter("joint"))

        worlds = [deepcopy(root.find("worldbody")) for root in (original, gripper)]
        for world in worlds:
            for body in world.iter("body"):
                for inertial in list(body.findall("inertial")):
                    body.remove(inertial)
        for side in ("l", "r"):
            for world in worlds:
                terminal = world.find(f'.//body[@name="{side}_arm_l7"]')
                for child in list(terminal):
                    if child.tag != "joint":
                        terminal.remove(child)
        self.assertEqual(structure(worlds[0]), structure(worlds[1]))

        for section in ("actuator", "sensor", "equality"):
            expected = {
                item.get("name"): structure(item)
                for item in original.find(section)
                if (section != "equality" or item.tag == "connect")
                and (section != "actuator" or item.get("joint") not in hand_joints)
            }
            actual = {item.get("name"): structure(item) for item in gripper.find(section)}
            for name, item in expected.items():
                self.assertEqual(item, actual[name], name)

        original_meshes = {item.get("name"): item for item in original.findall("asset/mesh")}
        common_count = 0
        for mesh in gripper.findall("asset/mesh"):
            if not mesh.get("file").startswith("ehr21/"):
                continue
            common_count += 1
            source = original_meshes[mesh.get("name")].get("file")
            self.assertEqual(
                (BASELINE / "meshes" / source).read_bytes(),
                (PACKAGE / "meshes" / mesh.get("file")).read_bytes(),
                mesh.get("name"),
            )
        self.assertGreater(common_count, 20)
        self.assertEqual(len(gripper.findall("actuator/motor")), 21)
        self.assertEqual(len(gripper.findall("equality/connect")), 4)
        self.assertEqual(len(gripper.findall("equality/joint")), 2)
        for side in ("l", "r"):
            self.assertIsNotNone(gripper.find(f'actuator/motor[@joint="{side}_fg_0"]'))
            self.assertIsNone(gripper.find(f'actuator/motor[@joint="{side}_fg_1"]'))
            mimic = gripper.find(f'equality/joint[@joint1="{side}_fg_1"]')
            self.assertEqual(mimic.get("joint2"), f"{side}_fg_0")
            self.assertEqual(mimic.get("polycoef"), "0 -1 0 0 0")
        self.assertEqual(gripper.findall(".//camera"), [])


if __name__ == "__main__":
    unittest.main()
