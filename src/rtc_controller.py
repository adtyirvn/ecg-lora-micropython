import machine
import ntptime


class RTCController:
    def __init__(self):
        self.rtc = machine.RTC()

    def set_from_internet(self):
        try:
            ntptime.settime()
            print("RTC set from internet time.")
        except Exception as e:
            print("Error setting RTC from internet:", e)

    def get_formatted_date(self):
        datetime_tuple = self.rtc.datetime()
        return f"{datetime_tuple[0]:04d}-{datetime_tuple[1]:02d}-{datetime_tuple[2]:02d}"

    def get_formatted_time(self):
        datetime_tuple = self.rtc.datetime()
        formatted_time = f"{datetime_tuple[4]:02d}:{datetime_tuple[5]:02d}:{datetime_tuple[6]:02d}"
        return formatted_time

    def get_datetime(self):
        return self.rtc.datetime()
