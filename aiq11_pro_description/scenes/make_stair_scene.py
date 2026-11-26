#!/usr/bin/env python3
"""Generate an AIQ11 Pro stair-test MJCF from a canonical model."""

import argparse
from pathlib import Path
import xml.etree.ElementTree as ET


MODEL_FILES = {
    "full": "aiq11_pro.xml",
    "simplified": "aiq11_pro_simplified.xml",
}


def make_stair_scene(variant: str, output: Path) -> Path:
    model_dir = Path(__file__).resolve().parents[1] / "urdf"
    source = model_dir / MODEL_FILES[variant]
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    tree = ET.parse(source, parser=parser)
    root = tree.getroot()
    base = root.find("worldbody/body[@name='base_link']")
    compiler = root.find("compiler")
    if base is None or compiler is None:
        raise ValueError(f"Missing base_link or compiler in {source}")
    first = root.find("worldbody/geom[@name='stair1']")
    if first is None:
        raise ValueError(f"Missing enabled stair1 in {source}")
    position = [float(value) for value in first.get("pos", "").split()]
    size = [float(value) for value in first.get("size", "").split()]
    base_position = base.get("pos", "").split()
    if len(position) != 3 or not size or len(base_position) != 3:
        raise ValueError(f"Invalid stair1 or base_link geometry in {source}")
    base.set("pos", f"{position[0] - size[0] - 0.8:g} {position[1]:g} {base_position[2]}")

    # The generated XML can live outside the description package.
    for attribute in ("meshdir", "texturedir"):
        directory = compiler.get(attribute)
        if directory is not None:
            compiler.set(attribute, str((model_dir / directory).resolve()))

    output = output.expanduser().resolve()
    with output.open("xb") as stream:
        tree.write(stream, encoding="utf-8", xml_declaration=True)
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=MODEL_FILES, default="full")
    parser.add_argument("--output", type=Path, required=True,
                        help="New output XML path; existing files are not overwritten")
    args = parser.parse_args()
    try:
        output = make_stair_scene(args.variant, args.output)
    except (OSError, ET.ParseError, ValueError) as error:
        parser.error(str(error))
    print(output)


if __name__ == "__main__":
    main()
