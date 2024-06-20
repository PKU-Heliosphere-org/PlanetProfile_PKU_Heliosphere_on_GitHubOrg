import numpy as npimport matplotlib.pyplot as pltfrom PlanetProfile.Thermodynamics.HydroEOS import GetOceanEOS, GetPfreezeimport timedef best_fit_line_plot(x, y, x_label, y_label, title):    '''    Plot data in scatterplot with best fit line    '''    slope, intercept = np.polyfit(x, y, 1)    best_fit_line = slope * x+ intercept    fig = plt.figure()    ax1 = fig.add_subplot(111)    ax1.scatter(x, y, color='blue', label='Data points')    ax1.plot(x, best_fit_line, color='red', label='Best fit line')    ax1.axhline(0, color='green', linestyle='--', label='No pressure difference')    ax1.set_xlabel(x_label)    ax1.set_ylabel(y_label)    ax1.set_title(title)def benchmark_with_gsw_version_two():    '''    Benchmark reaktoro with gsw and seafreeze to find freezing pressures for given array of bottom temperatures    '''    # Establish temperature range to find bottom pressures    temperature_range = np.linspace(263.15, 270.15, 10)    # Establish pressure limits to search over and the resolution    P_MPa = np.arange(0.01, 150, 0.05)    # Array that stores reaktoro bottom pressure results    rkt_bPressure_results = []    # Time how long reaktoro takes    start_time = time.time()    # REAKTORO RESULTS    # Go through each bottom temperature in range, obtaining the MeltEOS identically to how PlanetoProfile does it (line 262-264 of SetupInit.py)    for temperature in temperature_range:        T_K = np.linspace(temperature - 0.01, temperature + 0.01, 11)        # Prescribe "CustomSolution", the name for PlanetProfile to use Reaktoro framework        meltEOS = GetOceanEOS("CustomSolution", 0, P_MPa, T_K, 'Vance2018', 'Millero', 'Vance2018', 'lookup')        rkt_bPressure_results.append(GetPfreeze(meltEOS, 1, temperature,                                           PLower_MPa=0.01, PUpper_MPa=150.01, PRes_MPa=1, UNDERPLATE=False))    rkt_time = time.time()    # GSW RESULTS    # Identical process to above but instead use GSW framework    gsw_bPressure_results = []    for temperature in temperature_range:        T_K = np.linspace(temperature-0.01, temperature+0.01, 11)        meltEOS = GetOceanEOS("Seawater", 0, P_MPa, T_K, 'Vance2018', 'Millero', 'Vance2018', 'lookup')        gsw_bPressure_results.append(GetPfreeze(meltEOS, 1, temperature,                                           PLower_MPa=0.01, PUpper_MPa=150.01, PRes_MPa=1, UNDERPLATE=False))    gsw_time = time.time()    # Print run times    print("RKT Runtime: ", rkt_time-start_time)    print("GSW Runtime: ", gsw_time-rkt_time)    # Convert lists into numpy arrays so they can be subtracted    rkt_bPressure_results = np.array(rkt_bPressure_results)    gsw_bPressure_results = np.array(gsw_bPressure_results)    # Find pressure difference between reaktoro and gsw    pressure_difference_results = rkt_bPressure_results-gsw_bPressure_results    # Graph the difference in pressure difference as a function of    x_label = 'Bottom temperature (K)'    y_label = 'Reaktoro bottom pressure - GSW bottom pressure (MPa)'    title = 'Difference in bottom pressure between Reaktoro and GSW for Pure water'    best_fit_line_plot(temperature_range, pressure_difference_results, x_label, y_label, title)    # Print pressure difference results    print(pressure_difference_results)    print("--------------------")    print(f"Average pressure difference: {np.average(abs(pressure_difference_results))}")    print("--------------------")    plt.show()if __name__ == "__main__":    # Call benchmark method    benchmark_with_gsw_version_two()