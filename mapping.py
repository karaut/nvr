from alert_check import nvr


def get_nvr(ip,port,user_name,password):
    return nvr(ip,port,user_name,password)

mp = {"daua":get_nvr}