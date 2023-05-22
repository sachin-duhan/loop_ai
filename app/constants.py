import os

raw_data = {
    "store_data": "1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025",
    "business_hours_data": "1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg",
    "timezone_data": "101P9quxHoMZMZCVWQ5o-shonk2lgK1-o",
}

REDIS_JOBS_TABLE = "csv_processing_jobs"

DEFAULT_TIMEZONE = "America/Chicago"

LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "data"
)

PRFETCH_DATA_TO_DB = False
