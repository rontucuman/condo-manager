import datetime


class Reservation:
    def __init__(self):
        self.reservation_id = 0
        self.receipt_id = 0
        self.common_area_id = 0
        self.user_id = 0
        self.username = ''
        self.common_area_name = ''
        # self.reservation_date = datetime.datetime.now()
        self.begin_reservation_date = datetime.datetime.now()
        self.end_reservation_date = datetime.datetime.now()
        self.amount = 0
        self.is_confirmed = False
        self.is_canceled = False
        self.receipt_filename = ''

