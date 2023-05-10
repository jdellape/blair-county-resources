class Service:
    def __init__(self, name):
        self.name = name
        self.has_schedule = False #default schedule to False as only a small number of services offered on schedule

    def set_weekly_schedule(self, value):
        self.has_schedule = True
        self.weekly_schedule = value.__dict__