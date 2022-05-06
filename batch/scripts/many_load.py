import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript many_load

from unesco.models import Category, State, Iso, Region, Site


def run():
    fhand = open('unesco/whc-sites-2018-clean.csv')  
    reader = csv.reader(fhand)
    next(reader)  # Advance past the header

    Category.objects.all().delete()
    State.objects.all().delete()
    Iso.objects.all().delete()
    Region.objects.all().delete()
    Site.objects.all().delete()

    # Format
    # name  description justification year  longitude latitude  area_hectares category  state region  iso

    for row in reader:
        
        name = row[0]
        print(name)

        ca, created = Category.objects.get_or_create(name=row[7])
        st, created = State.objects.get_or_create(name=row[8])
        iso, created = Iso.objects.get_or_create(name=row[-1])
        reg, created = Region.objects.get_or_create(name=row[-2])

        try:
            year = int(row[3])
        except:
            year = None

        try:
            latitude = float(row[5])
        except:
            latitude = None

        try:
            longitude = float(row[4])
        except:
            longitude = None

        try:
            description = row[1]
        except:
            description = None

        try:
            justification = row[2]
        except:
            justification = None

        try:
            area_hectares = float(row[6])
        except:
            area_hectares = None

        si = Site(name=name, description=description, year=year, justification=justification, longitude=longitude, latitude=latitude, area_hectares=area_hectares, category=ca, region=reg, iso=iso, state=st)
        si.save()
