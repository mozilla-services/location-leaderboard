from django.contrib.gis.utils import LayerMapping
from django.core.management.base import BaseCommand

from leaderboard.locations.models import Country


field_mapping = {
    'fips': 'FIPS',
    'iso2': 'ISO2',
    'iso3': 'ISO3',
    'un': 'UN',
    'name': 'NAME',
    'area': 'AREA',
    'pop2005': 'POP2005',
    'region': 'REGION',
    'subregion': 'SUBREGION',
    'lon': 'LON',
    'lat': 'LAT',
    'geometry': 'MULTIPOLYGON',
}


class Command(BaseCommand):
    help = 'Import country boundaries from a SHP file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str)

    def handle(self, *args, **options):
        LayerMapping(
            Country,
            options['file_path'],
            field_mapping,
            transform=False,
            encoding='iso-8859-1',
        ).save(strict=True, verbose=True)
