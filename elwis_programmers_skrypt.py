import json
import sys
import csv
import datetime
import os
import cgi
from dateutil import parser
js = '{"tittle": "Lorem ipsum", "email": "dolor@amet.com", "content": "hello world!"}'

y=json.loads(js)

#print (datetime.datetime.now())

#print(y["tittle"])




actual_date= (datetime.datetime.now())


class AutoStart:
    def __init__(self):
        limit_msg_per_time = parser.parse("0:00:30.898005") #30 sekund
        AutoStartDataFileName="AutoStartData_temp.txt"
        max_total_msg = 400
        max_total_msg=400
        
        if os.path.isfile(AutoStartDataFileName) == True:
            with open(AutoStartDataFileName, 'r+') as file_read_write:
                whole_columns= file_read_write.read()

                msg_counter = (whole_columns).split("|")[0]

                previous_date = (whole_columns).split("|")[1]

                previous_date_parsed_str = parser.parse(previous_date)
                print(str(actual_date) + "   aktualna data")
                print (str(previous_date_parsed_str) + "  previous_date_parsed_str")
                substract_dates = actual_date - previous_date_parsed_str
                if int(msg_counter) < max_total_msg:
                    substract_dates = (datetime.datetime.min + substract_dates).time()
                    if  str(substract_dates) > str(limit_msg_per_time).split(" ")[1]:
                        msg_counter = int(msg_counter) + 1
                        file_read_write.seek(0)
                        file_read_write.write(str(msg_counter)+ "|"+ str(actual_date)) #write data inside file
                        file_read_write.truncate()
                        print("wykonuje sie")
                    else:
                        print("Too many msg per limited time")
                        file_read_write.seek(0)
                        file_read_write.write(str(msg_counter)+ "|"+ str(actual_date)) #write data inside file
                        file_read_write.truncate()

                else:
                    ("Too many msg in total")

              
        else:
            print("File AutoStartData.txt don't exist")
        
            with open(AutoStartDataFileName, 'w+') as file_read_write:
                file_read_write.seek(0)
                file_read_write.write("1|" + str(actual_date)) #write data inside file


    def time_checking(self):
        print("lol")
        
    def detect_method_request(self):
        if cgi.escape(os.environ["REQUEST_METHOD"]) == "POST":
            pass
        else:
            print("inna metoda wykonawcza")
        

class WriteToCsvFile:
    def __init__(self, title, email, body):
        self.title = title
        self.email = email
        self.body = body
        fo = open("body.txt", "a+")
        fo.write("title: "+ self.title+'\n' + "email: " + self.email+'\n\n' + self.body+'\n\n' )
        fo.close()


if __name__ == "__main__":


    kl = AutoStart()


    with open('jsons.txt') as json_file:  
        json_receive = json.load(json_file)
    
    p1= WriteToCsvFile(json_receive["tittle"], json_receive["email"], json_receive["content"])
    #p1= WriteToCsvFile("Witramy panstwa", "cos@interia.pl", "jakas trescsssssssssss")
    
    #input("Press enter to exit ;)")


