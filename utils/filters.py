def filter_by_yields(elements, low_border):
    return [el for el in elements if el['y'] > low_border]


def filter_light_nuclides(elements, min_a):
    return [el for el in elements if el["a"] > min_a]


def filter_beta_decayable(data):
    # filtered = []
    # for full_branch in data:
    #     if 'branch' in full_branch:
    #         branch = full_branch['branch']
    #         filtered_branch = []
    #         for nuclide in branch:
    #             if nuclide['q'] > 0.511 and not '%' in str(nuclide['hl']):
    #                 filtered_branch.append(nuclide)
    #         full_branch['branch'] = filtered_branch
    #         filtered.append(full_branch)
    # return filtered
    d = [e for e in data if e['branch']]
    return d


def filter_beta_decayable_cfy(data):
    d = [e for e in data if 'nuclide' in e and not '%' in str(e['nuclide']['hl'])]
    return d
