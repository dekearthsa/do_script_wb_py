import wellbreath

## {
##     srtv: 0 # default 
##     cv: 0 # exhaust off 
##     cv: 1 # exhaust on
##     supply: 33 # ch 1   # use as low 
##     supply: 66 # ch 2   # use as high
##     supply: 100 # ch 3
## }

demo_temp =  {
    "sc_indoor": 21.1,
    "sc_outdoor": 10,
    "sc_attic": 10
}
demo_humid = {
    "sc_indoor": 11.4,
    "sc_outdoor": 10,
    "sc_attic": 10
}
demo_co2 =   {
    "sc_indoor": 2440.1,
    "sc_outdoor": 10,
    "sc_attic": 10
}

set_func_wellbreath = wellbreath.WellBreath(debug=True)
data  = set_func_wellbreath.func_wellbreath(temp=demo_temp, humid=demo_humid, co2=demo_co2)
print(data)

