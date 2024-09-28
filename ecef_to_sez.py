# ecef_to_sez.py
#
# Usage: python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km
#  Converts ecef vector components to sez
#  
# Parameters:
# o_x_km= ecef origin of SEZ frame x position in km 
# o_y_km = ecef origin of SEZ frame y position in km 
# o_z_km= ecef origin of SEZ frame z position in km 
# x_km= x in km
# y_km= y in km
# z_km= z in km

#
# Output:
#  Prints the s, e and z vectors in km
#
# Written by Anushka Devarajan
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0

# import Python modules
import math # math module
import sys  # argv


# "constants"
R_E_KM = 6378.137
E_E    = 0.081819221456

# helper functions

# initialize script arguments
o_x_km=float('nan') #latitude in degrees
o_y_km= float('nan') #longitude in degrees
o_z_km= float('nan') #height above the ellipsoid in km
x_km = float('nan') # SEZ south-component in km
y_km = float('nan') # SEZ east-component in km
z_km = float('nan') # SEZ z-component in km


# parse script arguments
if len(sys.argv)==7:
  o_x_km = float(sys.argv[1])
  o_y_km= float(sys.argv[2])
  o_z_km= float(sys.argv[3])
  x_km = float(sys.argv[4])
  y_km = float(sys.argv[5])
  z_km = float(sys.argv[6])
else:
  print(\
   'Usage: '\
   'python3 ecef_to_sez.py o_x_km o_y_km o_z_km x_km y_km z_km'\
  )
  exit()


def calc_denom(ecc, lat_rad):
  return math.sqrt(1.0-(ecc**2)*(math.sin(lat_rad)**2))

# calculate longitude
lon_rad = math.atan2(y_km,x_km)
lon_deg = lon_rad*180.0/math.pi

# initialize lat_rad, r_lon_km, r_z_km
lat_rad = math.asin(z_km/math.sqrt(x_km**2+y_km**2+z_km**2))
r_lon_km = math.sqrt(x_km**2+y_km**2)
prev_lat_rad = float('nan')

# iteratively find latitude
c_E = float('nan')
count = 0
while (math.isnan(prev_lat_rad) or abs(lat_rad-prev_lat_rad)>10e-7) and count<5:
  denom = calc_denom(E_E,lat_rad)
  c_E = R_E_KM/denom
  prev_lat_rad = lat_rad
  lat_rad = math.atan((z_km+c_E*(E_E**2)*math.sin(lat_rad))/r_lon_km)
  count = count+1
  
# calculate hae
hae_km = r_lon_km/math.cos(lat_rad)-c_E

#ecef coordinates
ecef_x_km=o_x_km-x_km
ecef_y_km=o_y_km-y_km
ecef_z_km=o_z_km-z_km

#inverse rotations
sez_s_km=(ecef_x_km*math.sin(lat_rad)*math.cos(lon_rad)+ecef_y_km*math.sin(lat_rad)*math.sin(lon_rad)-ecef_z_km*math.cos(lat_rad))
sez_e_km=(ecef_y_km*math.cos(lon_rad)-ecef_x_km*math.sin(lon_rad))
sez_z_km=(ecef_x_km*math.cos(lat_rad)*math.cos(lon_rad)+ecef_y_km*math.cos(lat_rad)*math.sin(lon_rad)+math.sin(lat_rad)*ecef_z_km)

print(sez_s_km)
print(sez_e_km)
print(sez_z_km)