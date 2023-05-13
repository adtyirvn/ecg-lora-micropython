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
    
    def get_formatted_datetime(self):
        datetime_tuple = self.rtc.datetime()
        formatted_date = "{:04d}-{:02d}-{:02d}".format(
        datetime_tuple[0], datetime_tuple[1], datetime_tuple[2])
        formatted_time = "{:02d}:{:02d}:{:02d}".format(
        datetime_tuple[4], datetime_tuple[5], datetime_tuple[6])
        print(f"{formatted_date} {formatted_time}")
        return formatted_date, formatted_time
    
    def get_datetime(self):
        return self.rtc.datetime()
