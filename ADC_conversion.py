def ADC_to_perc(ADC_value):
    perc = (-0.21) * ADC_value + 198.9  # Mit Werten von 470 für 100% Bodenfeuchtigkeit und 945 für 0% Bodenfeuchtigkeit
    if perc > 100:
        perc = 100
    if perc < 0:
        perc = 0
    return perc