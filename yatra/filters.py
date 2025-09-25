from core.utils import BuildFilters
from yatra.models.trip import Trip
from yatra.models.activity import Activity

TripFilter = BuildFilters(
    Trip,
    exact_fields=['started', 'ended'],
    fizzy_fields=['name'],
    date_fields=['created_on', 'started_on', 'ended_on']
).build()

ActivityFilter = BuildFilters(
    Activity,
    exact_fields=['started', 'ended'],
    fizzy_fields=['trip__name', 'name', 'created_by__name', 'created_by__number'],
    date_fields=['created_on', 'started_on', 'ended_on']
).build()