'''
This in file handel doing works in web server but not services.
for example processing front data function do work handeling
send data frontend in do_POST function and output a dictionery
from information in data e.x email, username, password
'''

def processing_front_data(post_data_bytes:bytes) -> dict:
    """
    This function in input a bytes str data and convert str data
    seperate with '&' input data and in a loop on each us from items
    convert data to tow part key and value and append in post_dict
    dictonery.
    :param post_data_bytes:(ByteStr)
        data in frontend content e.c "b'username=mohammad&email=mohammadhoseinajorloo@gmail.com&password=12345678'"
    :return post_dict:(dict)
        processing data e.c "{"username" : "mohammad", "email" : "mohammadhoseinajorloo@gmail.com", "password" : "12345678"}
    """
    post_dict = {}
    post_data_str = post_data_bytes.decode("UTF-8")
    post_data_split = post_data_str.split("&")
    for item in post_data_split:
        key = item.split("=")[0]
        value = item.split("=")[1]
        post_dict[key] = value

    return post_dict