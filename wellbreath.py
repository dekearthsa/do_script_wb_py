class WellBreath:

    def __init__(self, 
                 temp, 
                 humid, 
                 co2,
                 thres_co2_mor_than = 1000,
                 thres_co2_low_than = 750,
                 thres_temp_mor_than = 35,
                 thres_temp_lower_than = 30,
                 thres_humid_mor_than = 75,
                 thres_humid_low_than = 70,
                 set_exhaust_name = "exhaust_fan", ## set exhaust name 
                 set_supply_low_name = "supply_low", ## set supply fan low name 
                 set_supply_high_name = "supply_high", ## set supply fan high name
                 set_channel_cv_supply_low = 33, ## using channel 1 as supply low 
                 set_channel_cv_supply_high = 66 ## using channel 2 as supply high
                 ):
        
        self.temp = temp
        self.humid = humid
        self.co2 = co2
        self.thres_co2_mor_than = thres_co2_mor_than
        self.thres_co2_low_than = thres_co2_low_than
        self.thres_temp_mor_than = thres_temp_mor_than
        self.thres_temp_lower_than = thres_temp_lower_than
        self.thres_humid_mor_than = thres_humid_mor_than
        self.thres_humid_low_than = thres_humid_low_than
        self.set_exhaust_name = set_exhaust_name
        self.set_supply_low_name = set_supply_low_name
        self.set_supply_high_name = set_supply_high_name
        self.set_channel_cv_supply_low = set_channel_cv_supply_low
        self.set_channel_cv_supply_high = set_channel_cv_supply_high

    def func_wellbreath(self):
        if self.co2 >= self.thres_co2_mor_than and self.temp < self.thres_temp_mor_than and self.humid < self.thres_humid_mor_than:
            command = self.__func_create_command("on", [self.set_exhaust_name, self.thres_temp_lower_than])
            return command
        elif self.co2 >= self.thres_co2_mor_than and (self.temp >= self.thres_temp_mor_than or self.humid >= self.thres_humid_mor_than):
            command = self.__func_create_command("on", [self.set_exhaust_name, self.set_supply_high_name])
            return command
        elif self.co2 < self.thres_co2_low_than and (self.temp >= self.thres_temp_mor_than or self.humid >= self.thres_humid_low_than):
            command = self.__func_create_command("on", [self.set_exhaust_name, self.set_supply_high_name])
            return command
        elif self.co2 < self.thres_co2_low_than and self.temp < self.thres_temp_lower_than and self.humid < self.thres_humid_low_than:
            command = self.__func_create_command("off", [])
            return command

    def __func_create_command(self,action, array_command):
        if action == "on":
            if self.set_exhaust_name in array_command and self.set_supply_low_name in array_command:
                return {
                    "srtv":0, # default 
                    "cv": 1, # exhaust fan
                    "supply": self.set_channel_cv_supply_low, # supply fan
            
                }
            elif self.set_exhaust_name in array_command and self.set_supply_high_name in array_command:
                return {
                    "srtv":0, # default 
                    "cv": 1, # exhaust fan
                    "supply": self.set_channel_cv_supply_high, # supply fan
                }
        elif action == "off":
            return {
                    "srtv": 0, # default 
                    "cv": 0, # exhaust fan
                    "supply": 0, # supply fan
                }
        
example = WellBreath(temp=35,humid=55,co2=400)
t, h, c = example.func_wellbreath()

print(t)
print(h)
print(c)