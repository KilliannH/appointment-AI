# -*- coding: utf-8 -*-
from gtts import gTTS   # Text to speech
import locale
import datetime
import time
import os
import json
import http.client

conn = http.client.HTTPConnection("localhost", 3000)

class Jarvis:
    def __init__(self):
        locale.setlocale(locale.LC_TIME, '')
        date_stuff = self.get_dates_keywords() # not so great name to get weekdays, months in fr and so on
        self.weekdays = date_stuff[0],
        self.months = date_stuff[1],
        self.years = date_stuff[2],
        self.days_in_numbers = date_stuff[3]
        self.ignored_words = ["le", "la", "les", "de", "d'", "du", "des", "un", "une", "à la", "de la", "aux", "de l'"]
        self.common_date_keywords = ["aujourd'hui", "demain", "après demain",
                                      "dans deux jours", "dans trois jours",
                                      "la semaine prochaine", "dans une semaine",
                                      "dans deux semaines", " dans quinze jours",
                                      "lundi prochain", "mardi prochain",
                                      "mercredi prochain", "jeudi prochain",
                                      "vendredi prochain", "samedi prochain",
                                      "dimanche prochain"]

        self.dict_date_keywords = {"aujourd'hui": "today", "demain": "tomorrow",
                                   "cette semaine": "thisWeek", "la semaine prochaine": "nextWeek",
                                   "ce mois ci": "thisMonth"}

        self.appointments = self.get_appointments_for_period("")
        # on init we get all appointments from db

    @staticmethod
    def speak(text_to_speech):
        print("jarvis :" + text_to_speech)
        tts = gTTS(text_to_speech, 'fr')
        tts.save("audio.mp3")
        os.system("mpg123 audio.mp3")
        os.remove("audio.mp3")
        # Have to play with this for perfs / rapidity issues

    #            /////* MAIN FUNCTION */

    def think(self, audiosource):
        if "comment ça va" in audiosource:
            self.speak("ça va bien.")
        elif "ça va" in audiosource:
            self.speak("ça va bien.")

        if "quelle heure est-il" in audiosource:
            self.speak('il est ' + time.strftime('%-H') + ' heure ' + time.strftime('%M'))
        elif "quelle heure il est" in audiosource:
            self.speak('il est ' + time.strftime('%-H') + ' heure ' + time.strftime('%M'))

        if "liste moi les rendez-vous" in audiosource:
            list_by_keywords = audiosource.split("rendez-vous")[1]
            list_by_keywords = list_by_keywords.split(" ")

            keyword_detected = ""

            date_keyword_string = self.list_sorted_by_ignored_keywords(list_by_keywords)
            print(date_keyword_string)

            for key, value in self.dict_date_keywords.items():
                if key in date_keyword_string:
                    keyword_detected = key

            if keyword_detected != "":
                appointments_for_period = self.get_appointments_for_period(keyword_detected)
            else:
                appointments_for_period = self.appointments # no query in db needed, just list them all

            appointment_list = self.get_appointments_list_names_dates(appointments_for_period)

            if appointment_list != "":
                self.speak(appointment_list)
            else:
                self.speak("Vous n'avez pas de rendez-vous pour cette période.")

        if "liste les rendez-vous" in audiosource:
            '''list_by_keywords = audiosource.split("rendez-vous")[1]
            list_by_keywords = list_by_keywords.split(" ")

            keyword_detected = ""

            date_keyword_string = self.list_sorted_by_ignored_keywords(list_by_keywords)

            for keyword in self.list_date_keywords:
                if keyword in date_keyword_string:
                    keyword_detected = keyword

            #appointments_for_period = getAppointmentsForPeriods(keywordDetected)
            appointment_list = self.get_appointments_list_names_dates(appointments_for_period)
            self.speak(appointment_list)'''

        if "liste des rendez-vous" in audiosource:
            appointment_list = self.get_appointments_list_names_dates()
            self.speak(appointment_list)

        if "liste moi les événements" in audiosource:
            appointment_list = self.get_appointments_list_names_dates()
            self.speak(appointment_list)

        if "liste les événements" in audiosource:
            appointment_list = self.get_appointments_list_names_dates()
            self.speak(appointment_list)

        if "liste des événements" in audiosource:
            appointment_list = self.get_appointments_list_names_dates()
            self.speak(appointment_list)

        # CREATE APPOINTMENT

        if "créer un rendez-vous" in audiosource:
            appointment_infos = self.split_once_appointment_infos(audiosource)
            first_guess = self.guess_date(appointment_infos)
            actually_guessed_year = first_guess[0]
            actually_guessed_month = first_guess[1]
            actually_guessed_day = first_guess[2]

            actually_guessed_name = first_guess[3]

            try:
                appointment_date = datetime.date(actually_guessed_year, actually_guessed_month, actually_guessed_day)
            except ValueError:
                print("Oops!  That was no valid date.  Try again...")
                second_guess = self.guess_date_and_name_with_dates_keywords(appointment_infos)
                appointment_date = second_guess[0]
                actually_guessed_name = second_guess[1]
                actually_guessed_day = str(appointment_date.day)
            except AttributeError:
                print("Oops!  That was no valid date.  Try again...")
                second_guess = self.guess_date_and_name_with_dates_keywords(appointment_infos)
                appointment_date = second_guess[0]
                actually_guessed_name = second_guess[1]
                actually_guessed_day = str(appointment_date.day)

            appointment = appointment_date, actually_guessed_name
            self.post_appointment(appointment)
            self.speak("J'ai créé un rendez vous, " + actually_guessed_name + " le " + str(appointment_date.strftime('%A ')) + str(actually_guessed_day) + str(appointment_date.strftime('%B' '%Y')))

        elif "nouveau rendez-vous" in audiosource:
            appointment_infos = self.split_once_appointment_infos(audiosource)
            first_guess = self.guess_date(appointment_infos)
            actually_guessed_year = first_guess[0]
            actually_guessed_month = first_guess[1]
            actually_guessed_day = first_guess[2]

            actually_guessed_name = first_guess[3]

            try:
                appointment_date = datetime.date(actually_guessed_year, actually_guessed_month, actually_guessed_day)
            except ValueError:
                print("Oops!  That was no valid date.  Try again...")
                second_guess = self.guess_date_and_name_with_dates_keywords(appointment_infos)
                appointment_date = second_guess[0]
                actually_guessed_name = second_guess[1]
                actually_guessed_day = str(appointment_date.day)
            except AttributeError:
                print("Oops!  That was no valid date.  Try again...")
                second_guess = self.guess_date_and_name_with_dates_keywords(appointment_infos)
                appointment_date = second_guess[0]
                actually_guessed_name = second_guess[1]
                actually_guessed_day = str(appointment_date.day)

            appointment = appointment_date, actually_guessed_name
            self.post_appointment(appointment)
            self.speak("J'ai créé un rendez vous, " + actually_guessed_name + " le " + str(appointment_date.strftime('%A ')) + str(actually_guessed_day) + str(appointment_date.strftime('%B' '%Y')))

    @staticmethod
    def split_once_appointment_infos(full_message):
        # process
        split_first_time = full_message.split("rendez-vous")[1]
        if split_first_time[0] == " ":
            split_first_time = split_first_time[1:len(split_first_time)]
            # we have all infos said after word "rendez-vous"

        appointment_infos = split_first_time.split(" ")
        return appointment_infos

#            /////* GUESS PART */

    def guess_date(self, appointment_infos):
        print(appointment_infos)
        year_founded_parsed = 0
        year_founded = ""

        # each time there is a parsed version (to esealy convert to date)
        # and a non parsed to store what's left

        month_founded_parsed = 0
        month_founded = ""

        day_founded_parsed = 0
        day_founded = ""

        weekday_founded = ""

        name_founded_array = []
        name_founded = ""

        ignored_words_founded = {}

        # found year in appointment infos
        for i in range(0, len(appointment_infos)):
            for year in self.years:
                if appointment_infos[i] in year:
                    print("year found : " + appointment_infos[i])
                    year_founded_parsed = int(appointment_infos[i])
                    year_founded = appointment_infos[i]
                    break

        # found month in appointment infos
        for i in range(0, len(appointment_infos)):
            for month in self.months:
                if appointment_infos[i] in month:
                    print("month found : " + appointment_infos[i])
                    month_founded_parsed = month.index(appointment_infos[i]) + 1
                    month_founded = appointment_infos[i]
                    break

        # found day in appointment infos
        for i in range(0, len(appointment_infos)):
            for day in self.days_in_numbers:
                if appointment_infos[i] in day:
                    # print("day found : " + appointment_infos[i])
                    day_founded_parsed = int(appointment_infos[i])
                    day_founded = appointment_infos[i]
                    break

        # found weekday (litteral) in appointment infos
        for i in range(0, len(appointment_infos)):
            for day in self.weekdays:
                if appointment_infos[i] in day:
                    weekday_founded = appointment_infos[i]
                    break

        # store name
        for i in range(0, len(appointment_infos)):
            if year_founded in appointment_infos[i]:
                # print(appointment_infos[i])
                continue
            elif month_founded in appointment_infos[i]:
                #print(appointment_infos[i])
                continue
            elif day_founded in appointment_infos[i]:
                #print(appointment_infos[i])
                continue
            elif weekday_founded != "" and weekday_founded in appointment_infos[i]:
                print(appointment_infos[i])
                continue
            else:
                name_founded_array.append(appointment_infos[i])

        # Handles if there is no year in given date (store today's year implicitly)
        if year_founded_parsed == 0:
            year_founded_parsed = int(datetime.date.today().year)

        # handles ignored words
        name_founded = self.name_sorted_by_ignored_keywords(name_founded_array)

        return year_founded_parsed, month_founded_parsed, day_founded_parsed, name_founded

    def guess_date_and_name_with_dates_keywords(self, appointment_infos):
        full_query = ""
        common_date_keyword_detected = ""
        appointment_date = datetime.date.today()

        for i in range(0, len(appointment_infos)):
            full_query += appointment_infos[i] + " "

        for word in self.common_date_keywords:
            if word in full_query:
                # TODO optimise this crappy check
                if word == "demain":
                    if "après demain" in full_query:
                        common_date_keyword_detected = "après demain"
                        break
                    else:
                        common_date_keyword_detected = "demain"
                else:
                    print(word)
                    common_date_keyword_detected = word
                    break

        # handles appointment said before keyword date
        name_detected = full_query.split(common_date_keyword_detected)[1]
        if name_detected == " " or name_detected == "":
            name_detected = full_query.split(common_date_keyword_detected)[0]

        name_detected = " ".join(name_detected.split())

        def next_weekday(d, weekday):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            return d + datetime.timedelta(days_ahead)

        if self.common_date_keywords.index(common_date_keyword_detected) == 0:
            pass
            # today
        elif self.common_date_keywords.index(common_date_keyword_detected) == 1:
            print("tomorrow detected")
            # tomorrow
            appointment_date += datetime.timedelta(days=1)
        elif self.common_date_keywords.index(common_date_keyword_detected) == 2 or self.common_date_keywords.index(common_date_keyword_detected) == 3:
            appointment_date += datetime.timedelta(days=2)
            # in 2 days
        elif self.common_date_keywords.index(common_date_keyword_detected) == 4:
            print("dans 3 jours detected")
            appointment_date += datetime.timedelta(days=3)
            # in 3 days
        elif self.common_date_keywords.index(common_date_keyword_detected) == 5 or self.common_date_keywords.index(common_date_keyword_detected) == 6:
            appointment_date += datetime.timedelta(days=7)
            # in one week
        elif self.common_date_keywords.index(common_date_keyword_detected) == 7 or self.common_date_keywords.index(common_date_keyword_detected) == 8:
            appointment_date += datetime.timedelta(days=14)
            # in 2 weeks
        elif self.common_date_keywords.index(common_date_keyword_detected) == 9:
            appointment_date = next_weekday(appointment_date, 0)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex monday
        elif self.common_date_keywords.index(common_date_keyword_detected) == 10:
            appointment_date = next_weekday(appointment_date, 1)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex tuesday
        elif self.common_date_keywords.index(common_date_keyword_detected) == 11:
            appointment_date = next_weekday(appointment_date, 2)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex wednesday
        elif self.common_date_keywords.index(common_date_keyword_detected) == 12:
            appointment_date = next_weekday(appointment_date, 3)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex thursday
        elif self.common_date_keywords.index(common_date_keyword_detected) == 13:
            appointment_date = next_weekday(appointment_date, 4)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex friday
        elif self.common_date_keywords.index(common_date_keyword_detected) == 14:
            appointment_date = next_weekday(appointment_date, 5)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex saturday
        elif self.common_date_keywords.index(common_date_keyword_detected) == 15:
            appointment_date = next_weekday(appointment_date, 6)  # 0 = Monday, 1=Tuesday, 2=Wednesday...
            # nex sunday
        return appointment_date, name_detected

#            /////* INIT PART */
    def get_dates_keywords(self):
        date = datetime.date.fromtimestamp(1483311600) # Lundi 2 Janvier 2017, has a ref to produce date arrays
        weekdays = []
        months = []
        years = []
        days_in_numbers = []
        for i in range(0, 7):
            newdate = date.replace(date.year, date.month, date.day + i)
            weekdays.append(str(newdate.strftime('%A')))

        for i in range(0, 12):
            newdate = date.replace(date.year, date.month + i, date.day)
            months.append(newdate.strftime('%B'))

        for i in range(0, 31):
            days_in_numbers.append(str(i + 1))

        for i in range(0, 5): ## 2017 - 2021
            newdate = date.replace(date.year + i, date.month, date.day)
            years.append(str(newdate.strftime('%Y')))

        return weekdays, months, years, days_in_numbers

#            /////* CRUD PART */

    def get_appointments_for_period(self, period):
        for key, value in self.dict_date_keywords.items():
            if key in period:
                period = value
                print("period detected : " + period)
                break

        if period == "":
            # get all appointments
            conn.request("GET", "/api/appointments")
        else:
            # get appointments by period
            conn.request("GET", "/api/appointments/period="+period) # period dates in body
        response = conn.getresponse()
        appointments = json.loads(response.read())
        return appointments

    @staticmethod
    def post_appointment(appointment_infos):
        headers = {'Content-type': 'application/json'}

        appointment = {'date': appointment_infos[0].strftime('%s'), # timestamp format
                       'name': appointment_infos[1],
                       'created_date': datetime.date.today().strftime('%s')}

        json_appointment = json.dumps(appointment)

        conn.request("POST", "/api/appointments", json_appointment, headers)
        response = conn.getresponse()
        return print(response.status)

    @staticmethod
    def get_appointments_list_names_dates(appointments):
        appointment_list_with_name_date = ""
        for i in range(0, len(appointments)):
            appointments[i]["name"] = " ".join(appointments[i]["name"].split()) # badly handled spaces for better diction
            appointment_date = datetime.date.fromtimestamp(int(appointments[i]["date"]))
            appointment_list_with_name_date += appointments[i]["name"] + ", " + appointment_date.strftime('%A ' '%d ' '%B ' '%Y') + ". "
        return appointment_list_with_name_date

#       TOOLS
    def list_sorted_by_ignored_keywords(self, list_by_keywords):
        ignored_words_founded = {}
        date_keyword_string = ""

        for i in range(0, len(list_by_keywords)):
            for word in self.ignored_words:
                if word == list_by_keywords[i] and word != "la" and word != "le":
                    ignored_words_founded.update({word: i})
                elif list_by_keywords[i] == "":
                    ignored_words_founded.update({"": i})
                elif list_by_keywords[i] == " ":
                    ignored_words_founded.update({" ": i})

        # print(ignored_words_founded)

        index = 0

        for key, value in ignored_words_founded.items():
            list_by_keywords.pop(value - index)
            index += 1

        for i in range(0, len(list_by_keywords)):
            date_keyword_string += list_by_keywords[i] + " "

        return date_keyword_string

    def name_sorted_by_ignored_keywords(self, name_founded_array):
        ignored_words_founded = {}
        name_founded = ""

        for i in range(0, len(name_founded_array)):
            for word in self.ignored_words:
                if word == name_founded_array[i]:
                    ignored_words_founded.update({word: i})
                elif name_founded_array[i] == "":
                    ignored_words_founded.update({"": i})
                elif name_founded_array[i] == " ":
                    ignored_words_founded.update({" ": i})

        # print(ignored_words_founded)

        index = 0

        for key, value in ignored_words_founded.items():
            name_founded_array.pop(value - index)
            index += 1

        for i in range(0, len(name_founded_array)):
            name_founded += name_founded_array[i] + " "

        return name_founded
