# elwis_4programmers

Json data as input from file "jsons.txt"

Limits are declared as global variables in script:
max_msg_per_usr - limit for messages per user

limit_msg_per_time - limit for messages per time ("0:00:10.000000" it's 10 seconds)

max_total_msg - total quantity limit

Variable IP Filter is now static (user_ip_filter = "192.168.1.1")

We should set the value from CGI module


If you want to run tests:

-put all files at same directory

-in test_elwis_calosc_new.py for variable "stat_date_str" set today date

-run: "pytest -v"


Each time you run the test, new content files are created. We need to remove them before running again tests
