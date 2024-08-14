import time

class WellBreath:
    def __init__(self, 
            temp, 
            humid, 
            co2,
            debug = False, ## default logging is False // not show log
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
        self.debug = debug
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
        self.__func_logging(is_func="logic", action=["temp: "+ str(self.temp), "humid: "+ str(self.humid), "co2: "+ str(self.co2)])
        if self.co2 >= self.thres_co2_mor_than and self.temp < self.thres_temp_mor_than and self.humid < self.thres_humid_mor_than:
            command = self.__func_create_command(action="on", array_command=[self.set_exhaust_name, self.thres_temp_lower_than])
            self.__func_logging(is_func="cmd", action=command)
            return command["srtv"], command["cv"], command["supply"]
        elif self.co2 >= self.thres_co2_mor_than and (self.temp >= self.thres_temp_mor_than or self.humid >= self.thres_humid_mor_than):
            command = self.__func_create_command(action="on",array_command= [self.set_exhaust_name, self.set_supply_high_name])
            self.__func_logging(is_func="cmd", action=command)
            return command["srtv"], command["cv"], command["supply"]
        elif self.co2 < self.thres_co2_low_than and (self.temp >= self.thres_temp_mor_than or self.humid >= self.thres_humid_low_than):
            command = self.__func_create_command(action="on",array_command= [self.set_exhaust_name, self.set_supply_high_name])
            self.__func_logging(is_func="cmd", action=command)
            return command["srtv"], command["cv"], command["supply"]
        elif self.co2 < self.thres_co2_low_than and self.temp < self.thres_temp_lower_than and self.humid < self.thres_humid_low_than:
            command = self.__func_create_command(action="off", array_command=[])
            self.__func_logging(is_func="cmd", action=command)
            return command["srtv"], command["cv"], command["supply"]

    def __func_create_command(self,action, array_command):
        if action == "on":
            if self.set_exhaust_name in array_command and self.set_supply_low_name in array_command:
                return {
                    "srtv":float(0), # default 
                    "cv": float(1), # exhaust fan
                    "supply": float(self.set_channel_cv_supply_low), # supply fan
            
                }
            elif self.set_exhaust_name in array_command and self.set_supply_high_name in array_command:
                return {
                    "srtv":float(0), # default 
                    "cv": float(1), # exhaust fan
                    "supply": float(self.set_channel_cv_supply_high), # supply fan
                }
        elif action == "off":
            return {
                    "srtv": float(0), # default 
                    "cv": float(0), # exhaust fan
                    "supply": float(0), # supply fan
                }
        
    def __func_logging(self, is_func ,action):
        if self.debug:
            current_time = time.time()
            local_time = time.localtime(current_time)
            formatted_time = time.strftime("%d/%m/%Y %H:%M:%S", local_time)
        
            if is_func == "cmd":
                print(formatted_time + " " + "srtv: " + str(action["srtv"]) + " cv: " + str(action["cv"]) + " supply: " + str(action["supply"]))
            elif is_func == "logic":
                action_str = ", ".join(action)
                print(formatted_time + " " + action_str)



# example = WellBreath(
#     temp=55,
#     humid=55,
#     co2=400, 
#     debug=True ## Close debug using False 
#     )


# t, h, c = example.func_wellbreath()

# print(t)
# print(h)
# print(c)