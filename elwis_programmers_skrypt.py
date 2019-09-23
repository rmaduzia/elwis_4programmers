import json

import os
import cgi
from dateutil import parser
from datetime import date
from datetime import datetime
import sys

global AutoStartDataFileName
global file_limits_per_user
global file_with_messages
global file_error_logs
global limit_msg_per_time
global max_total_msg
global max_msg_per_usr
global actual_date
today_date_for_logs = date.today()

max_msg_per_usr = 5

file_limits_per_user = "limits_per_user_" + str(today_date_for_logs) + ".txt"
AutoStartDataFileName = "AutoStartData_" + str(today_date_for_logs) + ".txt"
file_with_messages = "messages_body_" + str(today_date_for_logs) + ".txt"
file_error_logs = "error_logs_" + str(today_date_for_logs) + ".txt"
limit_msg_per_time = parser.parse("0:00:10.898005")  # 10 sekund
max_total_msg = 400
actual_date = (datetime.now())

global user_ip_filter  # w tej zmiennej bedzie przypisane ip user
user_ip_filter = "192.168.1.1"


class users_filtr():
    def __init__(self, value_field_to_filtr):
        self.value_field_to_filtr = value_field_to_filtr
        json_data_from_file= self.read_values_from_file_limits(value_field_to_filtr)
        self.export_json_to_file(json_data_from_file)

    def read_values_from_file_limits(self, user_ip):
        if os.path.isfile(file_limits_per_user) == True:        
            with open(file_limits_per_user, 'r+') as file_read_write:
                whole_columns = json.load(file_read_write)
            return users_filtr.increasing_amount(self, whole_columns, user_ip)
            
        else:
            json_to_write_limits_per_user={
                "datas":[{
                "amount_msg": 1,
                "user_id": self.value_field_to_filtr}]}
            return json_to_write_limits_per_user
                        
    def export_json_to_file(self, json_done):
        with open(file_limits_per_user, 'w') as file_write:
            json.dump(json_done, file_write, indent=4)

    def increasing_amount(self, whole_columns, user_ip):
        value_exist = False
        for i in whole_columns["datas"]:
            if i["user_id"] == user_ip:
                value_exist = True
                i["amount_msg"] = i["amount_msg"] + 1
                if i["amount_msg"] > max_msg_per_usr:
                    error_logs_writter(datetime.now().strftime("%H:%M:%S") + " przekroczono limit wiadomosci per user ip: " + str(i["amount_msg"]))
                    sys.exit()
            if value_exist == True:
                return whole_columns
            else:
                entry={"amount_msg": 1,
                       "user_id": self.value_field_to_filtr}
                whole_columns['datas'].append(entry)
                return whole_columns


class AutoStart:
    def __init__(self):

        if os.path.isfile(AutoStartDataFileName) == True:
            with open(AutoStartDataFileName, 'r+') as file_read_write:
                whole_columns = json.load(file_read_write)
                json_data_rdy = self.AutoStartFilter(whole_columns, actual_date, max_total_msg, limit_msg_per_time)
                file_read_write.seek(0)
                json.dump(json_data_rdy, file_read_write)
                file_read_write.truncate()
        else:
            #File AutoStartData.txt don't exist
            self.AutoStartFileDoesNotExist(actual_date)

    def AutoStartFilter(self, whole_columns, actual_date, max_total_msg, limit_msg_per_time ):
        msg_counter = whole_columns["amount_msg"]
        previous_date = whole_columns["actual_date_json"]
        previous_date_parsed_str = parser.parse(previous_date)
        addition_dates = actual_date - previous_date_parsed_str
        
        if int(msg_counter) < max_total_msg:
            addition_dates = (datetime.min + addition_dates).time()
            if str(addition_dates) > str(limit_msg_per_time).split(" ")[1]:
                msg_counter = int(msg_counter) + 1
                str_to_write_auto_start_file = {
                    "amount_msg": msg_counter,
                    "actual_date_json": str(actual_date)
                }

                return str_to_write_auto_start_file

            else:
                error_logs_writter(datetime.now().strftime("%H:%M:%S") + " zbyt wczesnie wyslana wiadomosci")
                return whole_columns
                #Too many msg per limited time

        else:
            error_logs_writter(datetime.now().strftime("%H:%M:%S") + " przykroczono limit wiadomosci")
            return whole_columns
            #("Too many msg in total")
        
    def AutoStartFileDoesNotExist(self, actual_date):
        with open(AutoStartDataFileName, 'w+') as file_read_write:

            str_to_write_auto_start_file = {
                "amount_msg": 1,
                "actual_date_json":str(actual_date)
                }
                
            json.dump(str_to_write_auto_start_file, file_read_write)
 
              
    def detect_method_request(self):
        if cgi.escape(os.environ["REQUEST_METHOD"]) == "POST":
            pass
        else:
            print("inna metoda wykonawcza")
        

class WriteToCsvFile:
    def __init__(self, title, email, body):
        try:
            self.title = title
            self.email = email
            self.body = body
            fo = open(file_with_messages, "a+")
            fo.write("title: "+ self.title+'\n' + "email: " + self.email+'\n\n' + self.body+'\n\n' )
            fo.close()
        except Exception as e:
            error_logs_writter(datetime.now().strftime("%H:%M:%S") + e)
            

class error_logs_writter:
    def __init__(self, message):
        self.write_error_logs_to_file(message)
    def write_error_logs_to_file(self, body):
        f = open(file_error_logs, "a")
        f.write(body+'\n')



if __name__ == "__main__":

    #tutaj wykonuje sie filtrownaie per ip
    users_filtr(user_ip_filter)
    kl = AutoStart()


    with open('jsons.txt') as json_file:
        json_receive = json.load(json_file)

    try:
        p1 = WriteToCsvFile(json_receive["tittle"], json_receive["email"], json_receive["content"])

    except Exception as e:
        error_logs_writter(str(datetime.now().strftime("%H:%M:%S")) + str(e))
