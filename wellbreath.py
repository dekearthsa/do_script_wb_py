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
## status Dtype bool (status operate logic if fail it will return False otherwise is True )
## err_desc Dtype string (show description of fail operation in logic if nothing fail will return none)


class WellBreath:
    def __init__(self, 
            debug=False,  # default logging is False // not show log
            thres_co2_mor_than=1000,
            thres_co2_low_than=750,
            thres_temp_mor_than=35,
            thres_temp_lower_than=30,
            thres_humid_mor_than=75,
            thres_humid_low_than=70,
            set_exhaust_name="exhaust_fan",  # set exhaust name 
            set_supply_low_name="supply_low",  # set supply fan low name 
            set_supply_high_name="supply_high",  # set supply fan high name
            set_channel_cv_supply_low=33,  # using channel 1 as supply low 
            set_channel_cv_supply_high=66,  # using channel 2 as supply high
            set_range_val_co2=range(0, 5001),  # range type 0-5000 ppm
            set_range_val_temp=range(-50, 101),  # range type -50-100 °C
            set_range_val_humid=range(0, 101)  # range type 0 - 100 %RH
        ):

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

    def func_wellbreath(self, temp, humid, co2):
        if self.__func_range_value_data(temp=temp["sc_indoor"], humid=humid["sc_indoor"], co2=co2["sc_indoor"]):
            return self.__create_response(0.0, 0.0, 0.0, False, "Range temp, humid, or CO2 is out of threshold.")
        
        if co2["sc_indoor"] >= self.thres_co2_mor_than:
            if temp["sc_indoor"] < self.thres_temp_mor_than and humid["sc_indoor"] < self.thres_humid_mor_than:
                return self.__execute_command(True, [self.set_exhaust_name, self.set_supply_low_name])
            else:
                return self.__execute_command(True, [self.set_exhaust_name, self.set_supply_high_name])
        elif co2["sc_indoor"] < self.thres_co2_low_than:
            if temp["sc_indoor"] >= self.thres_temp_mor_than or humid["sc_indoor"] >= self.thres_humid_low_than:
                return self.__execute_command(True, [self.set_exhaust_name, self.set_supply_high_name])
            elif temp["sc_indoor"] < self.thres_temp_lower_than and humid["sc_indoor"] < self.thres_humid_low_than:
                return self.__execute_command(False, [])
        
        return self.__create_response(0.0, 0.0, 0.0, True, None)
    
    def __execute_command(self, state_on, array_command):
        command = self.__func_create_command(state_on, array_command)
        self.__func_logging(is_func="cmd", action=command)
        return self.__create_response(command["srtv"], command["cv"], command["supply"], True, None)
    
    def __create_response(self, srtv, cv, supply, status, err_desc):
        return {
            "srtv": srtv,
            "cv": cv,
            "supply": supply,
            "status": status,
            "err_desc": err_desc
        }

    def __func_create_command(self, state_on, array_command):
        if state_on:
            if self.set_exhaust_name in array_command:
                supply_value = self.set_channel_cv_supply_low if self.set_supply_low_name in array_command else self.set_channel_cv_supply_high
                return {"srtv": 0.0, "cv": 1.0, "supply": float(supply_value)}
        return {"srtv": 0.0, "cv": 0.0, "supply": 0.0}

    def __func_logging(self, is_func, action):
        if not self.debug:
            return
        
        co2_range_str = f"{self.set_range_val_co2.start}-{self.set_range_val_co2.stop-1}"
        temp_range_str = f"{self.set_range_val_temp.start}-{self.set_range_val_temp.stop-1}"
        humid_range_str = f"{self.set_range_val_humid.start}-{self.set_range_val_humid.stop-1}"    
        current_time = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime())
        print(current_time + " " +"Theshold co2 more than: ", self.thres_co2_mor_than)
        print(current_time + " " +"Theshold co2 lower than: ", self.thres_co2_low_than)
        print(current_time + " " +"Theshold temp more than: ", self.thres_temp_mor_than)
        print(current_time + " " +"Theshold temp lower than: ", self.thres_temp_lower_than)
        print(current_time + " " +"Theshold humid more than: ", self.thres_humid_mor_than)
        print(current_time + " " +"Theshold humid lower than: ", self.thres_humid_low_than)
        print(f"{current_time}"+ " " +f"Range threshold set is Co2 range: {co2_range_str} Temp range: {temp_range_str} Humid range: {humid_range_str}")
        if is_func == "cmd":
            print(f"{current_time} srtv: {action['srtv']} cv: {action['cv']} supply: {action['supply']}")
        elif is_func == "logic":
            action_str = ", ".join(action)
            print(f"{current_time} {action_str}")

    def __func_range_value_data(self,temp, humid, co2):
        return not (temp in self.set_range_val_temp and co2 in self.set_range_val_co2 and humid in self.set_range_val_humid)
