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
        formatted_datetime = "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(datetime_tuple[0], datetime_tuple[1], datetime_tuple[2], datetime_tuple[3], datetime_tuple[4], datetime_tuple[5])
        return formatted_datetime
    
    def get_datetime(self):
        return self.rtc.datetime()
