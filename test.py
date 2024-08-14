import wellbreath

set_func_wellbreath = wellbreath.WellBreath(
    temp= 37, 
    humid=55, 
    co2=500, 
    debug=True
    )

strv, cv, supply = set_func_wellbreath.func_wellbreath()
print("str: "+ str(strv) + " " + "cv: "+ str(cv) + " " + "supply: " + str(supply))