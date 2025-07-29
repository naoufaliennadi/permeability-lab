import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#  System Variables
diamater = .021 #  m
area = .000346185 #  m^2

#  Fluid Properties
density = 1000 # kg/m^3
viscosity = .001 #  pa*s

#  Cake Properties
permeability_m2 = 0 #  m^2
permeability_darcy = 0 #  darcy
length = .08 #  m
mean_particle_size = .479 #  mm

#  Operating Variables
water_heights = np.array([.43, .48, .53, .58, .63, .73, .83]) #  m
extrac_weight = np.array([0, 0, 0, 0, 0, 0, 0]) #  kg
pressure_diff = density*9.8*(water_heights+length) #  Pa
pressure_gradient = pressure_diff/length #  Pa/m

#  Measurements
mass_flow_rate = []
mean_velocity = []

#  Verification
reynolds_number = np.array([])
pressure_depletion = np.array([])

#  Calculate Values
for i in range(7,0,-1):
    df = pd.read_csv("./data/example{}.csv".format(i))
    coeffs = coefficients = np.polyfit(df["time, s"], df["mass, g"], 1)
    mass_flow_rate.append(coeffs[0])
    mean_velocity.append(coeffs[0]/1000/density/area)

mass_flow_rate = np.array(mass_flow_rate)
mean_velocity = np.array(mean_velocity)

permeability_m2 = mean_velocity*viscosity*length/pressure_diff
permeability_darcy = permeability_m2/9.869233*10**13

reynolds_number = density*mean_velocity*mean_particle_size/1000/viscosity
pressure_depletion = mean_velocity*9.8*density*60 #  Pa/min

#  Plot
x = np.append(pressure_gradient,-pressure_gradient)
y = np.append(mean_velocity*viscosity/9.869233*10**13,-mean_velocity*viscosity/9.869233*10**13)
slope, intercept = np.polyfit(x, y, 1)
r2 = np.corrcoef(x, y)[0, 1]**2
plt.title("Permeability Experiment")
plt.plot(x, x*slope+intercept,label="f(x) = {:.2f}x".format(slope))
plt.scatter(x,y,label="R2 = {:.2f}".format(r2))
plt.ylim(0)
plt.xlim(x[0])
plt.xlabel("ΔΦ/L")
plt.ylabel("v*μ")
plt.legend()
plt.grid()
plt.savefig("Example")

#  Output
#  TODO: Make this output to a proper file
print("Reynold's number", reynolds_number)
print("Pressure Depletion (Pa/min)", pressure_depletion)
print("Permeability (darcy)", permeability_darcy)
