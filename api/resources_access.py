import os

current_dir = os.path.dirname(__file__)
project_dir = os.path.join(current_dir, os.pardir)

export_filename_template = "{}_{}_ensdf.json"
export_cfy_filename_template = "{}_{}_ensdf_cfy.json"


def get_resources_dir():
    return os.path.join(current_dir, os.pardir, 'resources')


def get_settings_filepath():
    return os.path.join(project_dir, 'config', 'settings.conf')


def get_daya_bay_filepath():
    return os.path.join(get_resources_dir(), 'daya_bay', 'arXiv_1607.05378', 'table_12.dat')


def get_independent_base_data_filepath(main_nuclide_name, database_name):
    filename = export_filename_template.format(main_nuclide_name, database_name)
    return os.path.join(project_dir, "parse", "dumps", filename)


def get_cfy_data_filepath(main_nuclide_name, database_name):
    filename = export_cfy_filename_template.format(main_nuclide_name, database_name)
    return os.path.join(project_dir, "parse", "dumps", filename)


def get_dat_export_filepath(main_nuclide_name, postfix):
    exportfn = os.path.join(project_dir, 'output', main_nuclide_name, main_nuclide_name + postfix + ".dat")
    os.makedirs(os.path.dirname(exportfn), exist_ok=True)
    return exportfn


def get_export_daya_bay_filepath():
    exportfn = os.path.join(project_dir, 'output', 'daya_bay.dat')
    os.makedirs(os.path.dirname(exportfn), exist_ok=True)
    return exportfn
