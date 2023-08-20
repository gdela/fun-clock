from rtc import RTC

rtc = RTC()

class JustTime:
    
    def __init__(self, hour, minute, second=0):
        self.hour = hour
        self.minute = minute
        self.second = second
        
    @staticmethod
    def now() -> JustTime:
        now = rtc.datetime
        return JustTime(now.tm_hour, now.tm_min, now.tm_sec)
    
    def diff_seconds_to(self, other:JustTime) -> int:
        a = self.hour * 60 * 60 + self.minute * 60 + self.second
        b = other.hour * 60 * 60 + other.minute * 60 + other.second
        return a - b
        
    def __str__(self):
        return f'{self.hour:02d}:{self.minute:02d}:{self.second:02d}'


if __name__ == '__main__':
    print(JustTime(12,59).diff_seconds_to(JustTime(8,34)) / 60)
    print(JustTime(12,59).diff_seconds_to(JustTime(13,15)) / 60)      