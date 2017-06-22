import setup
import main

main_nuclides = ['u235', 'pu239', 'u238', 'pu241']


def calculate_for_nuclide(nuclide):
    setup.element_name = nuclide
    base_data = setup.load_independent_base_data()
    cfy_data = setup.load_cfy_data()
    for tk in setup.times.keys():
        time = setup.times[tk]
        print("Calculating {} for time {}".format(nuclide, tk))
        main.calculate_spectrum_for_time(base_data, time, tk)
    print("Calculation for CFY")
    main.calculate_spectrum_for_cfy(cfy_data)

if __name__ == '__main__':
    [calculate_for_nuclide(n) for n in main_nuclides]
