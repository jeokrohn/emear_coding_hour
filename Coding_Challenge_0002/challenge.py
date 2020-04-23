"""
Given a list of well formatted texts [fields separated by semicolon] - Build a dictionary with below requirements :
+ Each element of the list will be represented as a (key,value) into the dictionary.
+ The Key should be the first element of the text and the Value should be the full text itself.

Check Example :

list_of_text = ["0001;02-03-20 13:00;In-progress", "0002":"0002;02-04-20 13:00;Done";  "0003;02-05-20
13:00;Not-Started"]

final_result_dict_of_texts = {"0001":"0001;02-03-20 13:00;In-progress", "0002":"0002;02-04-20 13:00;Done",
"0003":"0003;02-05-20 13:00;Not-Started"}
"""


def long_version():
    list_of_text = ["0001;02-03-20 13:00;In-progress", "0002;02-04-20 13:00;Done", "0003;02-05-20 13:00;Not-Started"]

    # initialize as empty dictionary
    result = {}

    # iterate over the items in the list
    for text in list_of_text:
        # extract key by splitting on ";". The key is the 1st part of the result
        key = text.split(';')[0]

        # add the full text to the dictionary using the obtained key
        result[key] = text
    print(result)


def short_version():
    list_of_text = ["0001;02-03-20 13:00;In-progress", "0002;02-04-20 13:00;Done", "0003;02-05-20 13:00;Not-Started"]

    # generatore expression: iterate over the items in the list
    # * key/value pairs where the key is obtained by extracting the 1st part of a semicolon separated list
    result = {text.split(';')[0]: text for text in list_of_text}

    print(result)


def fun_with_tuples():
    list_of_text = ["0001;02-03-20 13:00;In-progress", "0002;02-04-20 13:00;Done", "0003;02-05-20 13:00;Not-Started"]

    # generator statement: generates tuples of key/value pairs
    keys_and_values = ((text.split(';')[0], text) for text in list_of_text)

    # list comprehension to create the dictionary. Using tuple unpacking
    result = {k: v for k, v in keys_and_values}

    print(result)


if __name__ == '__main__':
    long_version()
    short_version()
    fun_with_tuples()