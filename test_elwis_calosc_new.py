import elwis_calosc_new
import os
import json
from datetime import datetime
import time
from dateutil import parser


global limits_file_usr
global first_ip
global error_file
global start_file
global actual_datetime
global json_example_file
global content_file


stat_date_str="2019-09-23"

limits_file_usr = "limits_per_user_"+stat_date_str+".txt"
error_file = "error_logs_"+stat_date_str+".txt"
first_ip = "192.168.1.1"
start_file = "AutoStartData_"+stat_date_str+".txt"
actual_datetime = datetime.now()
json_example_file = "jsons_example.txt"
content_file = "messages_body_"+stat_date_str+".txt"

def read_strings_from_file(file):
    with open(file, 'r') as file_read:
        data = file_read.read()
        file_read.close()
    return data

def read_json_from_file(file):
    with open(file, 'r') as file_read:
        content = json.load(file_read)
        file_read.close()
    return content

def write_json_to_file(file,body):
    with open(file, 'r+') as file_write:
        file_write.seek(0)
        json.dump(body, file_write)
        file_write.truncate()
        file_write.close()


#test klasy users_filtr
def test_first_users_filtr():

    ob = elwis_calosc_new.users_filtr(first_ip)
    ob.read_values_from_file_limits(first_ip)

    assert os.path.isfile(limits_file_usr) == True

def test_first_users_filtr_check_content():
    content_json = read_json_from_file(limits_file_usr)
    example_json = {'datas': [{'amount_msg': 1, 'user_id': '192.168.1.1'}]}
    assert example_json == content_json


def test_first_users_filtr_increasing_amount():
    example_json = {'datas': [{'amount_msg': 2, 'user_id': '192.168.1.1'}]}

    json_content = read_json_from_file(limits_file_usr)
    increment_content =  elwis_calosc_new.users_filtr.increasing_amount("",json_content, first_ip)
    assert example_json == increment_content


#wyjatek z racji tego, że skrypt nie jest dalej przetwarzany, gdy limit został przekrocozny
def test_first_users_filtr_limits_per_ip():
    try:
        for i in range(1,6):
            elwis_calosc_new.users_filtr("192.168.1.1")

        content_json = read_json_from_file(limits_file_usr)

        assert os.path.isfile(error_file) == True
        assert elwis_calosc_new.max_msg_per_usr == content_json["datas"][0]["amount_msg"]
    except:
        pass


#test klasy AutoStart
def test_autostart_class():
    ob = elwis_calosc_new.AutoStart()
    content_json = read_json_from_file(start_file)
    example_json = {"amount_msg": 1, "actual_date_json": str(elwis_calosc_new.actual_date)}

    assert os.path.isfile(start_file) == True
    assert example_json == content_json

def test_autostart_filter_max_msgs():
    elwis_calosc_new.max_total_msg = 6
    elwis_calosc_new.limit_msg_per_time = parser.parse("0:00:1.898005")  # 1 sekunda

    for i in range(1,8):
        elwis_calosc_new.actual_date = (datetime.now())
        content_json = read_json_from_file(start_file)
        ob = elwis_calosc_new.AutoStart.AutoStartFilter("",content_json, elwis_calosc_new.actual_date,
                                                        elwis_calosc_new.max_total_msg,
                                                        elwis_calosc_new.limit_msg_per_time)
        write_json_to_file(start_file,ob)
        time.sleep(2)
    
    assert content_json["amount_msg"] == elwis_calosc_new.max_total_msg


#test klasy zapisującej wiadomości użytkowników
def test_write_users_msgs():
    json_data = read_json_from_file(json_example_file)
    elwis_calosc_new.WriteToCsvFile(json_data["tittle"], json_data["email"], json_data["content"])

    f = open(content_file,'r')
    body_verify = f.readlines()

    assert body_verify[0] == "title: Sampel\n"
    assert body_verify[1] == "email: sampel@email.pl\n"
    assert body_verify[2] == "\n"
    assert body_verify[3] == "Sampel wiadomosci\n"
    assert body_verify[4] == "\n"
    assert os.path.isfile(content_file) == True



