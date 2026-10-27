"""Build footprint-aligned STEP models (millimetres, +Z above PCB).

Requires cadquery 2.6+. Imported originals are retained in sources/.
KiCad footprint Y is the negative of model Y. No board placement is baked in.
"""
from pathlib import Path
import cadquery as cq

ROOT = Path(__file__).resolve().parent
SOURCES = ROOT / "sources"


def imported(name):
    return cq.importers.importStep(str(SOURCES / name))


def save(shape, name, color=(0.25, 0.25, 0.25)):
    assembly = cq.Assembly(name=name)
    assembly.add(shape, name="component", color=cq.Color(*color))
    assembly.save(str(ROOT / (name + ".step")))
    assert shape.val().isValid(), name


# Source pins: X = -2.5, 0, 2.5 and Y = 5, 7.5.
# Target model pins: X = 0, -2.5 and Y = 0, 2.5, 5.
save(imported("RK09712200HA.stp").rotate((0, 0, 0), (0, 0, 1), 90)
     .translate((5, 2.5, 0)), "RV_2C_RK09712200HA")

# Rotate the source upright; coil pins become (0,0) and (7.5,0).
save(imported("G2R-1-E-DC24.stp").rotate((0, 0, 0), (1, 0, 0), 90)
     .rotate((0, 0, 0), (0, 0, 1), -90)
     .translate((3.75, -12.5, 13.48)), "G2R-1-E-DC24")

save(imported("BM83SM1-00AB.stp").translate((0, 0, 0.3)), "Microchip_BM83")

# Manufacturer model is upside down, with pins at Z=14.5 and case at Z=0.
# Flip, put the mounting plane at Z=0, and align the pin row to model Y=0.
save(imported("M78AR-0.5 3D Mechanical.stp")
     .rotate((0, 0, 0), (1, 0, 0), 180)
     .translate((0, 1.679371, 10.4)), "M78AR-0.5")

save(imported("USB_C_HRO_TYPE-C-31-M-12.step")
     .rotate((0, 0, 0), (1, 0, 0), 90)
     .translate((-4.47, -3.65, 0)), "USB_C_HRO_TYPE-C-31-M-12", (0.72, 0.72, 0.75))

save(imported("JST_B2P-VH.step").rotate((0, 0, 0), (0, 0, 1), 90)
     .translate((3.96, 0, 0)), "JST_B2P-VH", (0.9, 0.88, 0.78))

# Generic 5W cement resistor. Body follows the existing 22 x 10 footprint;
# height 9 mm is a nominal SQP/SQ 5W package, since no MPN is specified.
cement = cq.Assembly(name="CEMENT_RESISTOR_5W")
body = cq.Workplane("XY").box(22, 10, 9, centered=(True, True, False))
cement.add(body, name="ceramic", color=cq.Color(0.94, 0.93, 0.87))
for sign in (-1, 1):
    horizontal = cq.Solid.makeCylinder(0.4, 3, cq.Vector(sign*11, 0, 4.5), cq.Vector(sign, 0, 0))
    vertical = cq.Solid.makeCylinder(0.4, 7.5, cq.Vector(sign*14, 0, -3), cq.Vector(0, 0, 1))
    cement.add(cq.Compound.makeCompound([horizontal, vertical]), name=f"lead_{sign}", color=cq.Color(0.7, 0.7, 0.72))
cement.save(str(ROOT / "CEMENT_RESISTOR_5W.step"))

# Keystone 3557-2: manufacturer catalogue drawing, 19.8 x 6.8 x 7.4 mm,
# 2.8 mm pin projection. Use the board's exact 13.47 x 3.4 mm pin grid.
# Contact spring details and moulded features are simplified; no fuse fitted.
holder = cq.Assembly(name="Keystone_3557-2_simplified")
case = cq.Workplane("XY").box(19.8, 6.8, 7.4, centered=(True, True, False))
for x in (-6.735, 6.735):
    opening = cq.Workplane("XY").box(4.6, 4.4, 6.4, centered=(True, True, False)).translate((x, 0, 1.1))
    case = case.cut(opening)
    for y in (-1.7, 1.7):
        pin = cq.Workplane("XY").box(0.41, 0.8, 3.8, centered=(True, True, False)).translate((x, y, -2.8))
        holder.add(pin, name=f"pin_{x}_{y}", color=cq.Color(0.72, 0.72, 0.75))
    for y in (-1.4, 1.4):
        spring = cq.Workplane("XY").box(3.8, 0.41, 5.6, centered=(True, True, False)).translate((x, y, 1.2))
        holder.add(spring, name=f"contact_{x}_{y}", color=cq.Color(0.72, 0.72, 0.75))
holder.add(case, name="nylon", color=cq.Color(0.08, 0.08, 0.09))
holder.save(str(ROOT / "Keystone_3557-2_simplified.step"))
print("Built 8 footprint-aligned STEP models.")
