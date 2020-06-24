"""
Build a wonderful program that help record users below details with following requirements :
(id, firstname, email, country, city, zipCode, currentRole, currentCompany, contacts, gender, jobsHistory, Birthday)

1/ Contacts attribute should be the list of contact of the user. One contact entry should follow this format :
{"type": "mobile", "number":123456789, "code":48}. Types could be fix, mobile, office or other.

2/ JobsHistory attribute should be also a list of the user past jobs. One job entry should follow this format :
{"role": "cisconian", "company": "cisco", "started": "24-01-2000", "ended": "24-01-3000", "stayed": "1000 yrs 0
months 0 days"}

3/ The stayed attribut inside each job entry, should be deducted from the started & ended values.

4/ Brithday attribute should be into this string format: "Friday 01 January 2020"

5/ the id of each user record should be generated automatically with the python **uuid** module.

6/ Each user record should be formated and saved like one line into Json format inside a file called
"users-records.json". Use the Python built-in **JSON** module.

7/ Each time a new user record is created, trace that action into a log file named "users.log". Each log entry should
contain the timestamp and the user id and the user firstname with a the mention "created". Use the Python built-in**
logging** module.

8/ Harden as much the code so that user enter a valid value. Also handle any exceptions and structure your code with
functions as much you can so further features addition or improvement could be simple.

** Don't hesitate to use any external module (like "colored" for example) to put some color into your console display
maybe when asking specific question to user or when confirming to user that the record was successfully created.
Feel free to beautify. You can find that external module (colored) and its detailed usage at this link
https://pypi.org/project/colored/
"""

import logging
import datetime
import re
import uuid
from typing import List, Optional, Any, get_args, get_origin

from pydantic import BaseModel, Field, EmailStr, ValidationError, validator
from pydantic.fields import ModelField

USER_FILE = 'users-records.json'
DATE_FORMAT = '%d-%m-%Y'

def choice(prompt: str, options: str) -> str:
    options = list(options)
    while (r := input(prompt).lower()) not in options:
        pass
    return r


def yes_no(prompt: str):
    return choice(prompt, 'yn') == 'y'


class InputMixin:
    """
    Mixin to add capability to add an object from the console via the from_console class method
    """
    def log_created(self):
        pass

    @classmethod
    def list_from_console(cls, name: str, values=None):
        values = values or []
        print(f'{name}: enter list of {cls.__name__} objects')
        index = 0
        while True:
            index += 1
            print(f'--{cls.__name__} #{index}--')
            if len(values) >= index:
                edit_value = values[index - 1]
            else:
                edit_value = None
            v = cls.from_console(current_value=edit_value)
            if v is None:
                index -= 1
            elif len(values) >= index:
                values[index - 1] = v
            else:
                values.append(v)
            if yes_no(f'Enter further {cls.__name__} objects? (Y/N)'):
                continue
            break
        if index:
            values = values[:index]
        else:
            values = []
        return values

    @classmethod
    def from_console(cls, current_value=None):
        """
        Input object from console and
        :return: object or None if input failed
        """
        print(f'Enter values for new {cls.__name__} object')
        obj = None
        if current_value is not None:
            assert isinstance(current_value, cls)
            values = {k: current_value.__dict__[k] for k in cls.__fields__}
        else:
            values = dict()
        while True:
            for name, field in cls.__fields__.items():
                field: ModelField
                if field.default:
                    # no need to edit this value
                    continue
                if field.field_info.extra.get('no_edit'):
                    # no need to edit this value
                    continue
                current_value = values.get(name)
                # check if this is a generic (List)
                ot = field.outer_type_
                args = get_args(ot)
                if args:
                    # this is a generic type
                    # we only support lists of InputMixin subclasses
                    origin = get_origin(ot)
                    if origin == list and issubclass(args[0], InputMixin):
                        v = args[0].list_from_console(name=name, values=current_value)
                    else:
                        raise NotImplementedError
                else:
                    if current_value is not None:
                        # already have a value
                        # prompt with value and offer option to enter empty string to keep current value
                        v = input(f'{cls.__name__}.{name} ({current_value}), ENTER to keep: ')
                        v = v or current_value
                    else:
                        v = input(f'{cls.__name__}.{name}:')
                values[name] = v
            try:
                obj = cls(**values)
            except ValidationError as e:
                print('Invalid input')
                for error in e.raw_errors:
                    print(f'{error._loc}: input=\'{values[error._loc]}\', error: {error.exc}')
                if not yes_no('Re-enter? (Y/N)'):
                    break
            else:
                break
        if obj:
            obj.log_created()
        return obj


class Contact(BaseModel, InputMixin):
    type: str
    number: int
    code: int


def date_validation(v: str) -> str:
    """
    Validate a date string to be dd-mm-yyyy
    :param v: value to be validated
    :return: validated string
    :raises: ValueError for unacceptable dates
    """
    v = v.strip()
    try:
        datetime.datetime.strptime(v, '%d-%m-%Y')
    except ValueError:
        raise ValueError('Dates have to be in DD.MM.YYYY format')
    return v.strip()


class JobHistory(BaseModel, InputMixin):
    role: str
    company: str
    started: str
    ended: str
    # stayed: avoid editing. This value is calculated
    # we are not using a @property b/c properties are not serialized by BaseModel.json()
    stayed: str = Field(no_edit=True)

    @validator('started', 'ended')
    def validate_started_ended(cls, v: str, values):
        """
        Validator for started and ended fields. Make sure the fields are in dd-mm-yyyy format.
        :param v: value to validate
        :param values: values already set
        :return: validates value
        :raises: ValueError for unacceptable values
        """
        started = values.get('started')
        v = date_validation(v)

        def sortable(date_str):
            """
            get a string in form YYYYMMDD
            :param date_str: date in DD-MM-YYYY
            :return: YYYYMMDD
            """
            return f'{date_str[-4:]}{date_str[3:5]}{date_str[:2]}'

        if started and sortable(started) > sortable(v):
            raise ValueError('started needs to be before ended')
        return v

    @staticmethod
    def stayed_from_started_ended(started, ended):
        """
        2/ JobsHistory attribute should be also a list of the user past jobs. One job entry should follow this format :
        {"role": "cisconian", "company": "cisco", "started": "24-01-2000", "ended": "24-01-3000", "stayed": "1000 yrs 0
        months 0 days"}

        3/ The stayed attribut inside each job entry, should be deducted from the started & ended values.
        :param started:
        :param ended:
        :return:
        """

        try:
            started = datetime.datetime.strptime(started, DATE_FORMAT)
            ended = datetime.datetime.strptime(ended, DATE_FORMAT)
        except ValueError:
            return None
        diff_year = ended.year - started.year
        diff_month = ended.month - started.month
        diff_day = ended.day - started.day
        if diff_day < 0:
            # add days of previous month
            last_day_of_previous_month = ended - datetime.timedelta(days=ended.day)
            diff_day += last_day_of_previous_month.day
            diff_month -= 1
        if diff_month < 0:
            diff_month += 12
            diff_year -= 1
        return f'{diff_year} yrs {diff_month} months {diff_day} days'

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.stayed = self.stayed_from_started_ended(self.started, self.ended)


user_log = logging.getLogger(f'{__name__}.User')
fh = logging.FileHandler('users.log')
fh.setFormatter(logging.Formatter(fmt='%(asctime)s - %(message)s'))
user_log.addHandler(fh)
user_log.setLevel(logging.INFO)


class User(BaseModel, InputMixin):
    id: str = Field(default_factory=lambda: f'{uuid.uuid4()}')
    firstname: str
    email: EmailStr
    country: str
    city: str
    zipCode: str
    currentRole: str
    currentCompany: str
    gender: str
    birthday: str
    contacts: List[Contact]
    jobHistory: List[JobHistory]

    @validator('birthday')
    def validate_birthday(cls, v: str):
        """
        Validatoor for birthday field
        Brithday attribute should be into this string format: "Friday 01 January 2020"
        we also allow dd-mm-yyyy
        :param v: value to validate
        :return: validated and in desired format
        :raises: ValueError for unacceptable values
        """

        date_format = '%A %d %B %Y'
        v = v.strip()
        try:
            date = datetime.datetime.strptime(v, date_format)
            return v
        except Exception:
            pass
        # we also allow dd-mm-yyyy
        date_validation(v)
        return datetime.date(year=int(v[-4:]), month=int(v[3:5]), day=int(v[:2])).strftime(date_format)

    def log_created(self)->None:
        """
        Write a log entry for each user created. Only for users created via console
        :return: None
        """
        user_log.info(f'{self.id}, {self.firstname} created')


if __name__ == '__main__':
    users = []
    try:
        with open(USER_FILE, mode='r') as user_file:
            users = [User.parse_raw(line) for line in user_file.readlines()]
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'Problem reading users from file: {e}')

    print(f'{len(users)} users read from file({USER_FILE})')
    print('\n'.join(f'{u}' for u in users))

    while yes_no('Add another user? (Y/N)'):
        u = User.from_console()
        if u is not None:
            users.append(u)
            with open(USER_FILE, mode='w') as user_file:
                user_file.write('\n'.join(u.json() for u in users))
