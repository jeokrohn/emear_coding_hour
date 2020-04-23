"""
Given a list of well formatted texts [fields separated by semicolon] - Build a dictionary with below requirements :
+ Each element of the list will be represented as a (key,value) into the dictionary.
+ The Key should be the first element of the text and the Value should be the full text itself.

Check Example :

list_of_text = ["0001;02-03-20 13:00;In-progress", "0002":"0002;02-04-20 13:00;Done";  "0003;02-05-20 13:00;Not-Started"]

final_result_dict_of_texts = {"0001":"0001;02-03-20 13:00;In-progress", "0002":"0002;02-04-20 13:00;Done", "0003":"0003;02-05-20 13:00;Not-Started"}
"""


def long_version():
    list_of_text = ["0001;02-03-20 13:00;In-progress", "0002;02-04-20 13:00;Done", "0003;02-05-20 13:00;Not-Started"]
    result = {}
    for text in list_of_text:
        key = text.split(';')[0]
        result[key] = text
    print(result)


def short_version():
    list_of_text = ["0001;02-03-20 13:00;In-progress", "0002;02-04-20 13:00;Done", "0003;02-05-20 13:00;Not-Started"]
    result = {text.split(';')[0]: text for text in list_of_text}
    print(result)

if __name__ == '__main__':
    long_version()
    short_version()
