import time
## python 3.8.5 version  ##

## {
##     srtv: 0 # default 
##     cv: 0 # exhaust off 
##     cv: 1 # exhaust on
##     supply: 33 # ch 1   # use as low 
##     supply: 66 # ch 2   # use as high
##     supply: 100 # ch 3
## }

## Parameter ## 
## temp (data temp from outside this function)
## humid (data humid from outside this function)
## co2 (data co2 from outside this function)
## debug (default is False to show log change it to True)
## thres_co2_mor_than (thres_co2_mor_than is threshold of Co2 when higher than... default is 1000)
## thres_co2_low_than (thres_co2_low_than is threshold of Co2 when lower than... default is 750)
## thres_temp_mor_than (thres_temp_mor_than is threshold of temp when higher than... default is 35)
## thres_temp_lower_than (thres_temp_lower_than is threshold of temp when lower than... default is 30)
## thres_humid_mor_than (thres_humid_mor_than is threshold of humid when higher than...  default is 75)
## thres_humid_low_than (thres_humid_low_than is threshold of humid when lower than...  default is 70)
## set_exhaust_name (set_exhaust_name is action command name of exhaust fan default is exhaust_fan)
## set_supply_low_name (set_supply_low_name is action command name of supply fan low speed default is supply_low)
## set_supply_high_name (set_supply_high_name is action command name of supply fan high speed default is supply_high)
## set_channel_cv_supply_low (set_channel_cv_supply_low  is channel of supply fan low speed  default is 33)
## set_channel_cv_supply_high (set_channel_cv_supply_high is channel of supply fan high speed default default is 66)

## Output data is ##
## srtv Dtype float
## cv Dtype float
## supply Dtype float

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
            set_channel_cv_supply_high = 66, ## using channel 2 as supply high
            set_range_val_co2 = range(0,5001), ## range type 0-500 ppm
            set_range_val_temp = range(-50, 101), ## range type -50-100 °C
            set_range_val_humid = range(0, 101), ## range type 0 - 100 %RH
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
        self.set_range_val_co2 = set_range_val_co2
        self.set_range_val_temp = set_range_val_temp
        self.set_range_val_humid = set_range_val_humid

    def func_wellbreath(self):
        self.__func_logging(is_func="logic", action=["temp: "+ str(self.temp), "humid: "+ str(self.humid), "co2: "+ str(self.co2)])
        err_range = self.__func_range_value_data()
        if err_range:
            return {
                "strv": 0.0,
                "cv": 0.0,
                "supply":0.0,
                "status": False,
                "err_desc": "range temp or humid or co2 is lower or over range threshold."
            }
        else:
            if self.co2 >= self.thres_co2_mor_than and self.temp < self.thres_temp_mor_than and self.humid < self.thres_humid_mor_than:
                command = self.__func_create_command(state_off_on=True, array_command=[self.set_exhaust_name, self.thres_temp_lower_than])
                self.__func_logging(is_func="cmd", action=command)
                set_dict_cmd = {
                    "strv": command["srtv"],
                    "cv": command["cv"],
                    "supply": command["supply"],
                    "status": True,
                    "err_desc": None
                }
                return set_dict_cmd
            elif self.co2 >= self.thres_co2_mor_than and (self.temp >= self.thres_temp_mor_than or self.humid >= self.thres_humid_mor_than):
                command = self.__func_create_command(state_off_on=True,array_command= [self.set_exhaust_name, self.set_supply_high_name])
                self.__func_logging(is_func="cmd", action=command)
                set_dict_cmd = {
                    "strv": command["srtv"],
                    "cv": command["cv"],
                    "supply": command["supply"],
                    "status": True,
                    "err_desc": None
                }
                return set_dict_cmd
            elif self.co2 < self.thres_co2_low_than and (self.temp >= self.thres_temp_mor_than or self.humid >= self.thres_humid_low_than):
                command = self.__func_create_command(state_off_on=True,array_command= [self.set_exhaust_name, self.set_supply_high_name])
                self.__func_logging(is_func="cmd", action=command)
                set_dict_cmd = {
                    "strv": command["srtv"],
                    "cv": command["cv"],
                    "supply": command["supply"],
                    "status": True,
                    "err_desc": None
                }
                return set_dict_cmd
            elif self.co2 < self.thres_co2_low_than and self.temp < self.thres_temp_lower_than and self.humid < self.thres_humid_low_than:
                command = self.__func_create_command(state_off_on=False, array_command=[])
                self.__func_logging(is_func="cmd", action=command)
                set_dict_cmd = {
                    "strv": command["srtv"],
                    "cv": command["cv"],
                    "supply": command["supply"],
                    "status": True,
                    "err_desc": None
                }
                return set_dict_cmd

    def __func_create_command(self,state_off_on, array_command):
        if state_off_on:
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
        else:
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
                # Convert the range objects to strings
                co2_range_str = f"{self.set_range_val_co2.start}-{self.set_range_val_co2.stop-1}"
                temp_range_str = f"{self.set_range_val_temp.start}-{self.set_range_val_temp.stop-1}"
                humid_range_str = f"{self.set_range_val_humid.start}-{self.set_range_val_humid.stop-1}"

                print("range threshold set is " + " " + "Co2 range: " + co2_range_str + " " + "Temp range: " + temp_range_str + " " + "Humid range: " + humid_range_str)
                print(formatted_time + " " + action_str)

    def __func_range_value_data(self):
        if self.temp in self.set_range_val_temp and self.co2 in self.set_range_val_co2 and self.humid in self.set_range_val_humid:
            return False
        else:
            return True
