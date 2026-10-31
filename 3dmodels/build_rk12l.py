"""Simplified RK12L12C0A0E, Alps RK12L drawing 1 (mm).

PCB mounting plane Z=0; model Y is opposite KiCad footprint Y.
Origin matches samacsys:RK12L12C. Small undimensioned case details
and the split snap-in spring geometry are approximated.
"""
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parent


def build():
    a = cq.Assembly(name="RK12L12C0A0E")
    metal = cq.Color(0.72, 0.73, 0.75)
    plastic = cq.Color(0.16, 0.18, 0.17)

    # Drawing: body 12 wide, 6+9.5 long; shaft centre 11 from pin row.
    # Case depth and internal layers are nominal; collar face is Z=8.6.
    body = cq.Workplane("XY").box(12, 15.5, 6.6, centered=(True, True, False)).translate((5, 9.25, 0))
    a.add(body, name="housing", color=plastic)
    cap = cq.Workplane("XY").box(12, 15.5, 0.5, centered=(True, True, False)).translate((5, 9.25, 6.6))
    a.add(cap, name="metal_cover", color=metal)
    collar = cq.Workplane("XY").circle(3.6).extrude(1.5).translate((5, 11, 7.1))
    a.add(collar, name="shaft_bearing", color=plastic)
    # LM1=25 from mounting plane; 6 mm shaft, 12 mm long D-flat, 4.5 across.
    shaft = cq.Workplane("XY").circle(3).extrude(25-8.6)
    flat = cq.Workplane("XY").box(12, 6, 12, centered=(True, False, False)).translate((0, 1.5, 13-8.6))
    shaft = shaft.cut(flat).rotate((0, 0, 0), (0, 0, 1), 60).translate((5, 11, 8.6))
    a.add(shaft, name="insulated_D_shaft", color=cq.Color(0.88, 0.87, 0.78))
    # Physical left-to-right pin positions: outer 2,1; inner 1,2; outer 3; inner 3.
    for number, x in [(1, 2), (2, 0), (3, 10), (4, 4), (5, 6), (6, 8)]:
        pin = cq.Workplane("XY").box(0.3, 0.6, 4.2, centered=(True, True, False)).translate((x, 0, -3.5))
        bend = cq.Workplane("XY").box(0.3, 2.1, 0.6, centered=(True, False, False)).translate((x, -0.3, 0.1))
        a.add(pin.union(bend), name=f"terminal_{number}", color=metal)
    # Simplified 2.1 x 2 mm snap-in supports on a 13 x 11 mm grid.
    for number, x in [(7, -1.5), (8, 11.5)]:
        tab = cq.Workplane("XY").box(0.6, 2, 6.5, centered=(True, True, False)).translate((x, 11, -3.2))
        shoulder = cq.Workplane("XY").box(1.6, 2, 0.6, centered=(True, True, False)).translate((x + (0.5 if x < 0 else -0.5), 11, 2.7))
        a.add(tab.union(shoulder), name=f"mounting_tab_{number}", color=metal)
    for _, part in a.traverse():
        if part.obj is not None:
            assert part.obj.val().isValid(), part.name
    a.save(str(ROOT / "RK12L12C0A0E.step"))
    s = cq.importers.importStep(str(ROOT / "RK12L12C0A0E.step")).val()
    assert s.isValid()
    b = s.BoundingBox()
    assert abs(b.zmax - 25) < 1e-5
    print(f"STEP valid: {len(s.Solids())} solids, bounds Z={b.zmin:.2f}..{b.zmax:.2f} mm")


if __name__ == "__main__":
    build()
