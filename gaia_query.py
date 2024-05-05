import astroquery.gaia
import requests
import tqdm

num_stars = 200

query = f"""SELECT TOP {num_stars} dr3.designation, dr3.ra, dr3.dec, dr3.phot_g_mean_mag, dr3.distance_gspphot
FROM gaiadr3.gaia_source as dr3
ORDER BY dr3.distance_gspphot ASC
"""

job = astroquery.gaia.Gaia.launch_job(query)
table = job.get_results()


session = requests.Session()
headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

for i in tqdm.tqdm(range(0, len(table["DESIGNATION"]))):
    x = session.get("https://cds.unistra.fr/cgi-bin/nph-sesame/A?"+table["DESIGNATION"][i], headers=headers)
    x=x.text
    name = x[x.find("%I.0")+5:x.find("\n",x.find("%I.0"))]
    table["DESIGNATION"][i] = name

table.pprint_all(max_lines=500, max_width=100)

