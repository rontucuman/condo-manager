import datetime
import decimal


class Reservation:
    row_number: int
    reservation_id: int
    receipt_id: int
    common_area_id: int
    user_id: int
    username: str
    common_area_name: str
    begin_reservation_date: datetime.date
    end_reservation_date: datetime.date
    amount: decimal
    is_confirmed: bool
    is_canceled: bool
    receipt_filename: str
    status: str


    def __init__(self):
        self.row_number = 0
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
        self.status = ''

