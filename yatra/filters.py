from core.utils import BuildFilters
from yatra.models.trip import Trip, UserTrip
from yatra.models.activity import Activity
from yatra.models.bus import Bus
from yatra.models.user import User

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

BusFilter = BuildFilters(
    Bus,
    fizzy_fields=['created_by__name', 'created_by__number', 'trip__name', 'number'],
    date_fields=['created_on']
).build()

UserFilter = BuildFilters(
    User,
    exact_fields=['is_active'],
    fizzy_fields=['name', 'number', 'created_by__name', 'created_by__number'],
    date_fields=['created_on']
).build()

UserTripFilter = BuildFilters(
    UserTrip,
    fizzy_fields=['user__name', 'user__number', 'created_by__name', 'created_by__number'],
    date_fields=['created_on']
).build()