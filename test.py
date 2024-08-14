import wellbreath

set_func_wellbreath = wellbreath.WellBreath(
    temp= 37, 
    humid=55, 
    co2=500, 
    debug=True
    )

data  = set_func_wellbreath.func_wellbreath()
print(data)