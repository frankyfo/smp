from downtime.models import Location

values = []


def load_from_file():
    with open('downtime/utils/cities.csv') as f:
        reader = (line.strip().split(',') for line in f)
        next(reader)
        for line in reader:
            site = Location.objects.create(
                id=len(Location.objects.all()),
                name=line[1],
                region=line[2]
            )
