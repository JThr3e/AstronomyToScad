from solid import *
from solid.utils import *

## takes in a list of tuples of form (name, x, y, z)
## returns an open scad model of the stars on little cylinders
## on a big cylindrical base
def star_points_to_model(star_data):
    BASE_SIZE = 3
    BASE_RADIUS = 70
    MAX_HEIGHT = 6000
    POLE_RADIUS = 3.5
    HOLE_RADIUS = 2.0
    positive_volumes = [cylinder(h=BASE_SIZE, r=BASE_RADIUS)]
    negative_volumes = []
    for star in star_data:
        name = star[0]
        x = star[1]
        y = star[2]
        z = star[3]
        if name =="Tau Ceti":
            y+=3
        txt = translate([x-4,y+6,0])(
            linear_extrude(4) (text(name, size=2.5))
        )
        pos_vol = translate([x,y,0])(
            cylinder(h=z,r=POLE_RADIUS)
        )
        neg_vol = translate([x,y,-50])(
            cylinder(h=MAX_HEIGHT,r=HOLE_RADIUS)
        )
        positive_volumes.extend([txt, pos_vol])
        negative_volumes.append(neg_vol)

    d = difference()(
        union()(*positive_volumes),
        union()(*negative_volumes)
    )
    return scad_render(d)

