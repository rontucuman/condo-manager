import datetime


class CustomFilters:
    filter_username: str
    filter_common_area_name: str
    filter_begin_reservation_date: datetime.date
    filter_end_reservation_date: datetime.date
    filter_status: str

    def __init__(self):
        self.filter_username = ''
        self.filter_common_area_name = ''
        self.filter_begin_reservation_date = ''
        self.filter_end_reservation_date = ''
        self.filter_status = ''
