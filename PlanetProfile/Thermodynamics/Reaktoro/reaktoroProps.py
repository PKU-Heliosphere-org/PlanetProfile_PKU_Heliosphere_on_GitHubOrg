import reaktoro as rktimport numpy as npimport logging# Assign loggerlog = logging.getLogger('PlanetProfile')class RktPhase():    def __init__(self, aqueous_species_list, speciation_ratio_mol_kg, TMin_K, TMax_K, PMin_MPa, PMax_MPa):        self.aqueous_species_list = aqueous_species_list        self.speciation_ratio_mol_kg = speciation_ratio_mol_kg        self.TMin_K = TMin_K        self.TMax_K = TMax_K        self.PMin_MPa = PMin_MPa        self.PMax_MPa = PMax_MPa    def __call__(self, P_MPa, T_K, grid = False):        # Convert a 0-d numpy array into a float        if np.size(P_MPa) == 1:            P_MPa = np.atleast_1d(P_MPa)        if np.size(T_K) == 1:            T_K = np.atleast_1d(T_K)        # Similar approach to SF, where we specify the P_MPa and T_K at equilibrium, and ice_freezing function returns        # if ice has formed or not at given temperature and pressure. Then, GetZero function will query over pressures to find        # bottom pressure at which ice begins to form for bottom pressure.        return ice_freezing(self.aqueous_species_list, self.speciation_ratio_mol_kg, P_MPa, T_K).astype(np.int_)        '''        # IDENTICAL APPROACH TO GSW        # 1. Subtract the freezing temperature from the input temperature        # 2. Compare to zero -- if we are below the freezing temp, it's ice I, above, liquid        # 3. Cast the above comparison (True if less than Tfreeze, False if greater) to int,        #       so that we get 1 if we are below the freezing temp and 0 if above.        return (T_K - rkt_t_freeze(self.aqueous_species_list, self.speciation_ratio_mol_kg, P_MPa, self.TMin_K,                            self.TMax_K) < 0).astype(np.int_)        Alternative approach is to obtain Pfreezing from the prescribed T_K, since the way PlanetProfile obtains the Melting EOS,        this class will not have access to the hydrosphere TMin and TMax which I am using to constrain Reaktoro's search.        Instead, can use the constraints of         PMin to PMax to find the freezing pressure for a prescribed temperature via Reaktoro.        return (P_MPa - rkt_p_freeze(self.aqueous_species_list, self.speciation_ratio_mol_kg, T_K, self.PMin_MPa,                            self.PMax_MPa) < 0).astype(np.int_)        '''def SpeciesParser(species_string_with_ratios):    '''    Converts the provided String of species and their molar ratios into formats necessary for Reaktoro. Namely, creates    a String of all the species in the list and a dictionary with 'active' species that are added to solution (the observer species are    automatically generated to be 1e-16 moles in the solution by Reaktoro). It also returns the w_ppt of the solution. If any of the species do not exist in the database Reaktoro is implementing    (namely frezchem), this method raises an error that the species does not exist.     Parameters     ----------     species_string_with_ratios: String of all the species that should be considered in aqueous phase and their corresponding molar ratios.        For example, "Cl-: 19.076, Na+: 5.002, Ca2+: 0.0"     Returns     -------     aqueous_species_string: String that has all species names that should be considered in aqueous phase     speciation_ratio_mol_kg: Dictionary of active species and the values of their molar ratio (mol/kg of water)     w_ppt: The total grams of solute/kg of solution    '''    db = rkt.PhreeqcDatabase("frezchem.dat")    aqueous_species_string = ""    speciation_ratio_mol_kg = {}    # Go through each species and corresponding ratio_mol_kg and add to corresponding lists    for species_with_ratio in species_string_with_ratios.split(", "):        species, ratio_mol_kg = species_with_ratio.split(": ")        # Ensure that species is in frezchem database and if not then raise error        try:            db.species(species)        except:            raise ValueError(f'{species} does not exist in the frezchem database. Check that it is spelled correctly')        aqueous_species_string = aqueous_species_string + species + " "        # Check if the species is active (amount > 0 mol) and if so, add it to the dictionary        if (float(ratio_mol_kg) > 0):            speciation_ratio_mol_kg[species] = float(ratio_mol_kg)    # Check if water is in the aqueous species string and dictionary and if not, add it, ensuring to update the weight to be 1kg    if not "H2O" in aqueous_species_string:        aqueous_species_string = aqueous_species_string + "H2O "    speciation_ratio_mol_kg.update({"H2O": float(1/rkt.waterMolarMass)}) #Adds mols of H2O for 1kg of total solution    # Return the species string and dictionary (remove the trailing white space from the String as well with rstrip())    return aqueous_species_string.rstrip(" "), speciation_ratio_mol_kgdef ices_phases_amount_mol(props: rkt.ChemicalProps):    '''    Calculate the total amount of moles of all ices in the current state using its associated properties. Function is used in    the ice constraint for rkt_p_freeze().    '''    # Gather all the ices in the system    ice_indices = props.indicesPhasesWithSolidState()    ice_phase_amount = 0    for index in ice_indices:        ice_phase_amount += props.speciesAmount(index)    return props.speciesAmount("Ice(s)")# MAY NEED TO BE FURTHER EDIT TO TAKE IN LIST OF P_MPa and T_K that have size greater than 1def ice_freezing(aqueous_species_list, speciation_ratio_mol_kg, P_MPa, T_K):    """     Calculates whether ice is freezing at the given temperature and pressure. Utilizes the reaktoro framework to     constrain the equilibrium position at the prescribed pressure and temperature with the given composition,     and determines if ice has formed at a significant threshold of 1e-14, therefore calculating the phase of the composition     and returning true if the phase is ice and false if the phase is liquid.     Parameters     ----------     aqueous_species_list: aqueous species in reaction. Should be formatted in one long string with a space in between each species     speciation_ratio_mol_kg: the ratio of species in the aqueous solution in mol/kg of water. Should be a dictionary     with the species as the key and its ratio as its value.     P_MPa: the desired equilibrium freezing pressure(s).     T_K: the desired equilibrium freezing temperature(s).     Returns     -------     ice_present_array: an array of true and falses that indicate whether for prescribed P_MPa and T_K, if there is ice present at significant threshold of 1e-14.     """    # Initilialize the database with frezchem    db = rkt.PhreeqcDatabase("frezchem.dat")    # Prescribe the solution    solution = rkt.AqueousPhase(aqueous_species_list)    # Obtain all related solid phases    solids = rkt.MineralPhases()    # Initialize the system    system = rkt.ChemicalSystem(db, solution, solids)    # Create constraints on equilibrium - pressure and significant threshold for ice    specs = rkt.EquilibriumSpecs(system)    specs.pressure()    specs.temperature()    # Create a solver object    solver = rkt.EquilibriumSolver(specs)    # Create a chemical state and its associated properties    state = rkt.ChemicalState(system)    props = rkt.ChemicalProps(state)    ice_present_array = []    for P in P_MPa:        if P < 200:            for T in T_K:                # Prescribe the equilibrium constraints on pressure at P_MPa, ice phase amount at the significant threshold,                # and the temperatures to query over                conditions = rkt.EquilibriumConditions(specs)                conditions.pressure(P, "MPa")                conditions.temperature(T, "K")                # Populate the state with the prescribed species at the given ratios                for ion, ratio in speciation_ratio_mol_kg.items():                    state.add(ion, ratio, "mol")                # Solve the equilibrium problem                result = solver.solve(state, conditions)                # Update the properties                props.update(state)                # Check if the result failed, and if it did, then print an error and return 0 (SHOULD THINK OF WHAT TO DO                # IN THIS SIUTATION)                if result.failed():                    log.warning(f"Unsuccessful computation at: {props.pressure() / 1e+6} MPa and {props.temperature()} K")                    log.warning("Reaktoro gets as close to equilibrium as possible. Will return the current state's ice present, but should be noted.")                    ice_amount = props.speciesAmount("Ice(s)")                    ice_present_array.append(ice_amount > 1e-14)                    # Reset the state                    state = rkt.ChemicalState(system)                else:                    # Otherwise, add whether ice is present above significant threshold of 1e-14                    ice_amount = props.speciesAmount("Ice(s)")                    ice_present_array.append(ice_amount > 1e-14)                    # Reset the state                    state = rkt.ChemicalState(system)        else:            ice_present_array.append(np.float_(0))    # Convert the p_temperature_K list into an array and return    ice_present_array = np.array(ice_present_array)    return ice_present_arraydef rkt_t_freeze(aqueous_species_list, speciation_ratio_mol_kg, P_MPa, TMin_K, TMax_K):    """     Calculates the temperature at which the prescribed aqueous solution freezes. Utilizes the reaktoro framework to     constrain the equilibrium position at the prescribed pressure, the lower and upper limits of temperature (in MPa),     and the total amount of ice at a significant threshold of 1e-14, therefore calculating and returning the     temperature (within the range) at which ice begins to form.     Parameters     ----------     aqueous_species_list: aqueous species in reaction. Should be formatted in one long string with a space in between each species     speciation_ratio_mol_kg: the ratio of species in the aqueous solution in mol/kg of water. Should be a dictionary     with the species as the key and its ratio as its value.     P_MPa: the desired equilibrium freezing pressure(s). If P_MPa is a list, then we must return the associated freezing temperature for each pressure.     TMin_K: the lower limit of temperature that Reaktoro should query over     TMax_K: the upper limit of temperature that Reaktoro should query over     Returns     -------     t_freezing_K: the temperature at which the solution begins to freeze. If P_MPa is a list, then returns an equal size list with associated bottom temperatures.     """    # Initilialize the database with frezchem    db = rkt.PhreeqcDatabase("frezchem.dat")    # Prescribe the solution    solution = rkt.AqueousPhase(aqueous_species_list)    # Obtain all related solid phases    solids = rkt.MineralPhases()    # Initialize the system    system = rkt.ChemicalSystem(db, solution, solids)    # Create constraints on equilibrium - pressure and significant threshold for ice    specs = rkt.EquilibriumSpecs(system)    specs.pressure()    specs.unknownTemperature()    # Create equilibrium constraint on the phase amount of ices to 1e-14    # This constraint will allow Reaktoro to query for the pressure at which ice begins to form at the prescribed pressure    ice_phase_final = 1e-14  # Establish the desired equilibrium amount of total ices (1e-14 moles)    idx_ice_phase = specs.addInput("IP")    ices_phase_constraint = rkt.EquationConstraint()    ices_phase_constraint.id = "icePhaseAmountConstraint"    ices_phase_constraint.fn = lambda props, w: ices_phases_amount_mol(props) - w[idx_ice_phase]    specs.addConstraint(ices_phase_constraint)    # Create a solver object    solver = rkt.EquilibriumSolver(specs)    # Create a chemical state and its associated properties    state = rkt.ChemicalState(system)    props = rkt.ChemicalProps(state)    # Check if pressure is a list and if so, then query over each pressure and obtain the associated bottom temperature    t_freezing_K = []    # Use a for loop to go through each pressure    for pressure in P_MPa:        if pressure < 200:            # Prescribe the equilibrium constraints on pressure at P_MPa, ice phase amount at the significant threshold,            # and the temperatures to query over            conditions = rkt.EquilibriumConditions(specs)            conditions.pressure(pressure, "MPa")            conditions.set("IP", ice_phase_final)            conditions.setLowerBoundTemperature(TMin_K, "K")            conditions.setUpperBoundTemperature(TMax_K, "K")            # Populate the state with the prescribed species at the given ratios            for ion, ratio in speciation_ratio_mol_kg.items():                state.add(ion, ratio, "mol")            # Solve the equilibrium problem            result = solver.solve(state, conditions)            # Update the properties            props.update(state)            # Check if the result failed, and if it did, then print an error and return 0 (SHOULD THINK OF WHAT TO DO            # IN THIS SIUTATION)            if result.failed():                log.warning("Unsuccessful computation at:", props.pressure()/1e+6, "MPa")                log.warning("Returning zero as the bottom temperature. Should be handled accordingly.")                t_freezing_K.append(np.float_(0))                # Reset the state                state = rkt.ChemicalState(system)            else:                # Otherwise, return the equilibrium state's temperature, which is the bottom temperature in K, converted to a numpy float                equilibrium_temperature = props.temperature()                print(f"{equilibrium_temperature}K at {pressure} MPa")                t_freezing_K.append(round(np.float_(equilibrium_temperature), 2))                # Reset the state                state = rkt.ChemicalState(system)        else:            t_freezing_K.append(np.float_(0))    # Convert the p_temperature_K list into an array and return    t_freezing_K = np.array(t_freezing_K)    return t_freezing_K# Pressure freezing calculation; not utilized currentlydef rkt_p_freeze(aqueous_species_list, speciation_ratio_mol_kg, T_K, PLower_MPa, PUpper_MPa):    """    Calculates the pressure at which the prescribed aqueous solution freezes. Utilizes the reaktoro framework to    constrain the equilibrium position at the prescribed T_K, the lower and upper limits of pressure (in MPa),    and the total amount of ice at a significant threshold of 1e-14, therefore calculating and returning the    pressure (within the range) at which ice begins to form.    Parameters    ----------    aqueous_species_list: aqueous species in reaction. Should be formatted in one long string with a space in between each species    speciation_ratio_mol_kg: the ratio of species in the aqueous solution in mol/kg of water. Should be a dictionary    with the species as the key and its ratio as its value.    T_freezing_K: the desired equilibrium freezing temperature    PLower_MPa: the lower limit of pressure that Reaktoro should query over    PUpper_MPa: the upper limit of pressure that Reaktoro should query over    Returns    -------    p_freezing_MPa: the pressure at which the solution begins to freeze    """    # Initilialize the database with frezchem    db = rkt.PhreeqcDatabase("frezchem.dat")    # Prescribe the solution    solution = rkt.AqueousPhase(aqueous_species_list)    # Obtain all related solid phases    solids = rkt.MineralPhases("Ice(s)")    # Initialize the system    system = rkt.ChemicalSystem(db, solution, solids)    # Create constraints on equilibrium - temperature and significant threshold for ice    specs = rkt.EquilibriumSpecs(system)    specs.temperature()    # Create equilibrium constraint on the phase amount of ices to 1e-14    # This constraint will allow Reaktoro to query for the pressure at which ice begins to form at the prescribed temperature    ice_phase_final = 1e-14 # Establish the desired equilibrium amount of total ices (1e-14 moles)    idx_ice_phase = specs.addInput("IP")    ices_phase_constraint = rkt.EquationConstraint()    ices_phase_constraint.id = "icePhaseAmountConstraint"    ices_phase_constraint.fn = lambda props, w: ices_phases_amount_mol(props) - w[idx_ice_phase]    specs.addConstraint(ices_phase_constraint)    # Create a solver object    solver = rkt.EquilibriumSolver(specs)    # Create a chemical state and its associated properties    state = rkt.ChemicalState(system)    props = rkt.ChemicalProps(state)    # Check if pressure is a list and if so, then query over each pressure and obtain the associated bottom temperature    p_freezing_MPa = []    # Use a for loop to go through each temperature    for temperature in T_K:        # Prescribe the equilibrium constraints on temperature at T_K, ice phase amount at the significant threshold,        # and the pressures to query over        conditions = rkt.EquilibriumConditions(specs)        conditions.temperature(temperature, "K")        conditions.set("IP", ice_phase_final)        conditions.setLowerBoundPressure(PLower_MPa, "MPa")        conditions.setUpperBoundPressure(PUpper_MPa, "MPa")        # Populate the state with the prescribed species at the given ratios        for ion, ratio in speciation_ratio_mol_kg.items():            state.add(ion, ratio, "mol")        # Add a kg of water to the state        # Solve the equilibrium problem        result = solver.solve(state, conditions)        # Update the properties        props.update(state)        # Check if the result failed, and if it did, then it is likely because the freezing pressure could not be found given the pressure constraints.        # Thus, check if the state has reached the pressure limits so append the constraint and add this        if result.failed():            # Check if we have reached the upper pressure constraint            if props.pressure() == PUpper_MPa:                print("Have reached the upper pressure constraint of ", props.pressure, "MPa. Consider raising PMax_MPa")            print("Returning zero as the bottom pressure. Should be handled accordingly.")            p_freezing_MPa.append(np.float_(0))            # Reset the state            state = rkt.ChemicalState(system)        else:            # Otherwise, return the equilibrium state's pressure, which is the bottom pressure (converted to MPa from Pa)            equilibrium_pressure = props.pressure() / 1e+6            print(f"{equilibrium_pressure}MPa at {temperature} K")            p_freezing_MPa.append(equilibrium_pressure)            # Reset the state            state = rkt.ChemicalState(system)    # Convert the p_temperature_K list into an array and return    p_freezing_MPa = np.array(p_freezing_MPa)    return p_freezing_MPa