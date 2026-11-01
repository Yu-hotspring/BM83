"""Sato Parts knobs fitted to the existing footprint-aligned potentiometers.

Dimensions from sources/K-*_dimension.gif. Knurl count/depth, chamfers,
screw socket and paint details are illustrative. Threads are omitted.
Knob bottom is local Z=0 and the insertion axis is +Z.
"""
from pathlib import Path
from math import sin, cos, pi
import cadquery as cq
from build_rk12l import build as rk12

ROOT = Path(__file__).resolve().parent
SILVER = cq.Color(.76, .77, .79)
DARK = cq.Color(.08, .08, .09)


def knob(name, diameter, height, bore_depth, recess_dia, recess_depth, screw_z, screw_dia):
    radius = diameter / 2
    # Nominal longitudinal knurl. The drawing does not specify tooth geometry.
    teeth = 100 if diameter == 30 else 60
    pts = [( (radius if i % 2 == 0 else radius-.13)*cos(pi*i/teeth),
             (radius if i % 2 == 0 else radius-.13)*sin(pi*i/teeth))
           for i in range(2*teeth)]
    base_height = 3 if diameter == 30 else 0
    grip = cq.Workplane('XY').polyline(pts).close().extrude(height-base_height).translate((0,0,base_height))
    body = grip
    if base_height:
        body = body.union(cq.Workplane('XY').circle(radius).extrude(base_height))
    body = body.cut(cq.Workplane('XY').circle(3.05).extrude(bore_depth))
    body = body.cut(cq.Workplane('XY').circle(recess_dia/2).extrude(recess_depth))
    # One radial set screw, opposite the index mark. No helical thread.
    hole = cq.Solid.makeCylinder(screw_dia/2, radius, cq.Vector(0,-radius,screw_z), cq.Vector(0,1,0))
    body = body.cut(hole)
    a = cq.Assembly(name=name)
    if diameter == 30:
        groove = cq.Workplane('XY').box(.65,.5,height-3,centered=(True,False,False)).translate((0,radius-.45,3))
        body = body.cut(groove)
        index = cq.Workplane('XY').box(.55,.12,height-3,centered=(True,False,False)).translate((0,radius-.44,3))
    else:
        dot = cq.Workplane('XY').center(0,4.5).circle(.6).extrude(.04).translate((0,0,height-.04))
        body = body.cut(dot)
        index = dot
    a.add(body, name='aluminium', color=SILVER)
    a.add(index, name='index_mark', color=DARK)
    screw = cq.Solid.makeCylinder(screw_dia/2-.05, radius-3.1-.3,
                                  cq.Vector(0,-radius+.3,screw_z), cq.Vector(0,1,0))
    a.add(screw, name='set_screw', color=DARK)
    return a


def save(a, filename):
    a.save(str(ROOT / filename))
    s = cq.importers.importStep(str(ROOT / filename)).val()
    assert s.isValid(), filename
    b = s.BoundingBox()
    print(filename, 'valid', len(s.Solids()), 'solids; bounds',
          tuple(round(v,3) for v in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)))
    return s


def main():
    k59 = knob('K_59_M_AG',30,16,12,21,3,7,4)
    k29 = knob('K_29_6_1',13.7,13.5,11.6,11,2,5,3)
    save(k59,'K-59-M-AG.step')
    save(k29,'K-29-6.1.step')
    # RK12 axis is (5,11), shaft tip Z=25. Insertion depth 12 => bottom Z=13.
    large = cq.Assembly(name='RK12L12C0A0E_with_K_59_M_AG')
    large.add(rk12(write_step=False), name='potentiometer')
    large.add(k59, name='knob', loc=cq.Location(cq.Vector(5,11,13)))
    s = save(large,'RK12L12C0A0E_with_K-59-M-AG.step')
    assert abs(s.BoundingBox().zmax-29)<1e-5
    # RK097 axis +X through (Y=2.5,Z=6.5); shaft tip X=25.
    # Blind bore 11.6 => bottom X=13.4; knob face X=26.9.
    small = cq.Assembly(name='RK09712200HA_with_K_29_6_1')
    pot = cq.importers.importStep(str(ROOT/'RV_2C_RK09712200HA.step'))
    small.add(pot, name='potentiometer', color=cq.Color(.25,.25,.25))
    small.add(k29, name='knob', loc=cq.Location(cq.Vector(13.4,2.5,6.5), cq.Vector(0,1,0),90))
    s = save(small,'RV_2C_RK09712200HA_with_K-29-6.1.step')
    assert abs(s.BoundingBox().xmax-26.9)<1e-5
    # Ensure neither knob collides with the existing shaft/case.
    p12 = cq.importers.importStep(str(ROOT/'RK12L12C0A0E.step')).val()
    p09 = pot.val()
    n12 = k59.toCompound().translate((5,11,13))
    n09 = k29.toCompound().rotate((0,0,0),(0,1,0),90).translate((13.4,2.5,6.5))
    for name,p,n in [('RK12',p12,n12),('RK09',p09,n09)]:
        overlap = p.intersect(n).Volume()
        assert overlap < 1e-5, (name, overlap)
        print(name,'pot/knob overlap mm^3:',overlap)


if __name__ == '__main__':
    main()
