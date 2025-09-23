from core.utils import BuildFilters
from yatra.models.trip import Trip

TripFilter = BuildFilters(
    Trip,
    exact_fields=['started', 'ended'],
    fizzy_fields=['name'],
    date_fields=['created_on', 'started_on', 'ended_on']
).build()

