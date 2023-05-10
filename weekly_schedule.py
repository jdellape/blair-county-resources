class WeeklySchedule:
    """Hold an array of daily schedules passed via setattr() in app."""
    def __init__(self):
        self.daily_schedules = []
        
    def add_daily_schedule(self, value):
        self.daily_schedules.append(value.__dict__)