from datetime import date
import json
import os
import sys







    

class users_filtr():
    def __init__(self, value_field_to_filtr):
        today_date_for_logs = date.today()
        global file_limits_per_user
        file_limits_per_user = "limits_per_user_"+str(today_date_for_logs)+".txt"

        self.value_field_to_filtr = value_field_to_filtr
        json_data_from_file= self.read_values_from_file_limits(value_field_to_filtr)
        self.export_json_to_file(json_data_from_file)

    def read_values_from_file_limits(self, user_ip):
        if os.path.isfile(file_limits_per_user) == True:
            value_exist = False
            with open(file_limits_per_user, 'r+') as file_read_write:
                whole_columns = json.load(file_read_write)
            for i in whole_columns["datas"]:
                print(i)
                if i["user_id"] == user_ip:
                    value_exist = True
                    i["amount_msg"] = i["amount_msg"] + 1
            if value_exist == True:
                return whole_columns
            else:
                entry={"amount_msg": 1,
                       "user_id": self.value_field_to_filtr}
                whole_columns['datas'].append(entry)
                return whole_columns
        else:
            json_to_write_limits_per_user={
                "datas":[{
                "amount_msg": 1,
                "user_id": self.value_field_to_filtr}]}
            return json_to_write_limits_per_user
                        
    def export_json_to_file(self, json_done):
        with open(file_limits_per_user, 'w') as file_write:
            json.dump(json_done, file_write, indent=4)


if __name__ == "__main__":

     users_filtr(sys.argv[1])

    








