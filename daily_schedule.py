class DailySchedule:
    day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    def __init__(self, day_name, start_time, stop_time):
        self.day_name = day_name
        self.start_time = start_time
        self.stop_time = stop_time

    @property
    def day_name(self):
        return self._day_name
    
    @day_name.setter
    def day_name(self, value):
        if value not in self.day_options:
            raise ValueError(f"{value} not found in list of acceptable values for day name. Acceptable values include {self.day_options}")
        self._day_name = value

#TODO: Create a class that inherits from DailySchedule. Call it DailyMealSchedule. Additional field = meal_name with options [Breakfast, Lunch, Dinner]
class DailyMealSchedule(DailySchedule):
    meal_options = ["Breakfast", "Lunch", "Dinner"]
    def __init__(self, day_name, start_time, stop_time, meal_name):
        super().__init__(day_name, start_time, stop_time)
        self.meal_name = meal_name

    @property
    def meal_name(self):
        return self._meal_name
    
    @meal_name.setter
    def meal_name(self, value):
        if value not in self.meal_options:
            raise ValueError(f"{value} not found in list of acceptable values for meals. Acceptable values include {self.meal_options}")
        self._meal_name = value
    

    
