function outTable = printInteriorAsym(Planet)

    boundaries = Planet.boundaries;
    sig = Planet.sig;

    % Check to see if first entry is zero radius and chop it off if so
    if boundaries(1) == 0
        boundaries = boundaries(2:end);
        sig = sig(2:end);
    end
    
    % Condense zero-conductivity layers down to each be a single layer
    countCond = 1;
    sigCond = sig;
    boundCond = boundaries;
    for i=2:size(sig,2)
        countCond = countCond + 1;
        if sig(i)<1e-8 && sig(i-1)<1e-8
            countCond = countCond - 1;
            sig(i) = 1e-10;
        end

        sigCond(countCond) = sig(i);
        boundCond(countCond) = boundaries(i);
    end
    sigCond = sigCond(1:countCond);
    boundCond = boundCond(1:countCond);
    
    % Add ionosphere to conductivity list
    if isfield(Planet,'ionos_bounds')
        boundOut = [boundCond Planet.boundaries(end)+Planet.ionos_bounds];
        sigOut = [sigCond Planet.ionosPedersen_sig];
    else
        boundOut = boundCond;
        sigOut = sigCond;
    end
    
    % Set boundary deviations to zero for compatibility; we will specify them
    % another way or manually later.
    bcdevs = zeros(1,size(boundOut,2));
    % Create a Matlab table and print to a file
    outTable = table(boundOut',sigOut',bcdevs');
    outTable.Properties.VariableNames = {'Radius (m)', 'Conductivity (S/m)', 'Bdy deviation (ε/R)'};
    
end