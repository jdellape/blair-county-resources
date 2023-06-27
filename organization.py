#File for defining the organization object
class Organization:
    def __init__(self, name, address_line_one, city, zip_code, phone_num):
        self.name = name
        self.address_line_one = address_line_one
        self.city = city
        self.state_code = 'PA'
        self.zip_code = zip_code
        self.phone_num = phone_num
        self.services = {} #initialize as empty dictionary

    #Add additional setters for attributes that exist for some but not all orgs
    def set_contact(self, value):
        self.contact_name = value

    def set_email(self, value):
        self.email = value

    def set_hours_of_operation(self, value):
        self.hours_of_operation = value

    #Orgs povide an array of services
    #Service objects will contain weekly schedule objects (if applicable)
    def add_service(self, value):
        #TODO: value should be array. Can add validation here
        if value.has_schedule == False:
            self.services[value.name] = {'has_schedule':value.has_schedule}
        elif value.has_schedule == True:
            self.services[value.name] = {'has_schedule':value.has_schedule, 'schedule':value.schedule}

    
