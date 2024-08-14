import time 


current_time = time.time()
local_time = time.localtime(current_time)
formatted_time = time.strftime("%d/%m/%Y %H:%M:%S", local_time)
print(formatted_time)