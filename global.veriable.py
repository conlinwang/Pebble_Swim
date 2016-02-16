# global.veriable.py
g_data = None
step_count_x_result = None


#----------------------------------
def foo():
    print "data in foo:", g_data


#----------------------------------
def main():
    global g_data
    g_data = 1
    
    print "data in main:", g_data

    foo()

    print step_count_x_result
    step_count_x()
    print step_count_x_result
#----------------------------------


def step_count_x():
	global step_count_x_result
	step_count_x_result = 100

#----------------------------------	

main()