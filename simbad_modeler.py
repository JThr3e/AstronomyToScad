import astroquery
from astroquery.simbad import Simbad
from astropy.coordinates import SkyCoord
import astropy.units as u
import math
import astro_model_constructor

simbad = astroquery.simbad.Simbad()
simbad.add_votable_fields('plx')

# Get Right ascension centered on sol in galactic ecliptic
# See https://simbad.cds.unistra.fr/guide/sim-fscript.htx 
# Section "4.3.2 Coordinates" for more details on format string
simbad.add_votable_fields('ra(d;A;GAL;J2000;2000)', 'dec(d;D;GAL;J2000;2000)')
simbad.remove_votable_fields('coordinates')

def get_star_info(name):
    result_table = simbad.query_object(name)
    
    # Access Table fields to grab, RA, Dec, and parallax
    ra_deg = result_table['RA_d_A_GAL_J2000_2000'][0]
    dec_deg = result_table['DEC_d_D_GAL_J2000_2000'][0] 
    plx = result_table['PLX_VALUE'][0]
    
    
    if name == "61 Cygni":
        # data missing from simbad
        dist = 11.41
    else:
        # Get distance in light years
        dist = (1./(plx/1000.))*3.26156
    
    #Get radius and z distance using distance and declination
    r_dist = math.cos(math.radians(dec_deg))*dist
    z_dist = math.sin(math.radians(dec_deg))*dist

    #print(name)
    #print("RA (degrees):", ra_deg)
    #print("Dec (degrees):", dec_deg)
    #print("parallax (pc):", 1./(plx/1000.))
    #print("r_distance (ly):", r_dist)
    #print("z_distance (ly):", z_dist)
    #print("distance (ly):", dist)
    #print("+++++++++++++++++++++")

    #Get the x y coordinates using right ascension and radius distance 
    x_dist = math.cos(math.radians(ra_deg))*r_dist
    y_dist = math.sin(math.radians(ra_deg))*r_dist

    return (name, x_dist, y_dist, z_dist)


def scale_info_for_model(star_info):
    new_info = []
    for star in star_info:
        offset_z = 16
        x = star[1]
        y = star[2]
        z = star[3]
        # assuming units are mm, this will make it such that
        # 1cm = 2 light years
        x = (x/2.)*10 
        y = (y/2.)*10
        z = ((z+offset_z)/2.)*10
        new_info.append((star[0], x,y,z))
    return new_info


star_info = [("Sol", 0., 0., 0.)]
with open("stars.txt", "r") as f:
    stars = f.read()
    for star in stars.splitlines():
        # ignore stars with #
        if star[0] == "#":
            continue
        else:
            star_info.append(get_star_info(star))


star_info.sort(key=lambda x: x[3])
star_info = scale_info_for_model(star_info)
#for star in star_info:
#    print(star)

scad = astro_model_constructor.star_points_to_model(star_info)
print(scad)
