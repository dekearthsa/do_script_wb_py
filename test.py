import wellbreath

demo_temp =  {
    "sc_indoor": 36,
    "sc_outdoor": 10,
    "sc_attic": 10
}
demo_humid = {
    "sc_indoor": 55,
    "sc_outdoor": 10,
    "sc_attic": 10
}
demo_co2 =   {
    "sc_indoor": 500,
    "sc_outdoor": 10,
    "sc_attic": 10
}

set_func_wellbreath = wellbreath.WellBreath(debug=True)
data  = set_func_wellbreath.func_wellbreath(temp=demo_temp, humid=demo_humid, co2=demo_co2)
print(data)

