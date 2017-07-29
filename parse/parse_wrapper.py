import parse.parse_full as parse
from constants import Database
import os

main_nuclides = ['u235', 'pu239', 'u238', 'pu241']

database = Database.JENDL
database_name = Database.NAME_JENDL.value


def parse_nuclide(nuclide):
    exportfilename = os.path.join(parse.scriptdir, "dumps",
                                  parse.export_filename_template.format(nuclide, database_name))
    exportcfyfilename = os.path.join(parse.scriptdir, "dumps",
                                     parse.export_cfy_filename_template.format(nuclide, database_name))
    parse.main_independent(nuclide, database, exportfilename)
    parse.main_cumulative(nuclide, database, exportcfyfilename)


[parse_nuclide(n) for n in main_nuclides]
