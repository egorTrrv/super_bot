from functions.work_with_sql import *
import datetime

def scheduling(sb, us):
    text = "введите команду:"
    sb.launch_schedule_keyboard(us.id, text)
    msg = sb.input_message_from_user()
    while(True):
        if msg[0] == "на сегодня":
            shed = on_today(us)
            sb.send_message_to_user(us.id, shed)
        elif msg[0] == "на завтра":
            shed = on_tomorrow(us)
            sb.send_message_to_user(us.id, shed)
        elif msg[0] == "на текущую неделю":
            shed = on_week(us)
            sb.send_message_to_user(us.id, shed)
        elif msg[0] == "на следующую неделю":
            shed = on_week(us, 1)
            sb.send_message_to_user(us.id, shed)
        elif msg[0] == "вернуться в главное меню":
            break
        else:
            sb.send_message_to_user(us.id, "Введите команду!")
        msg = sb.input_message_from_user()

def on_week(us, smesh = 0):
    group = us.student_group
    week = datetime.datetime.today().isocalendar()[1]-5 + smesh
    msg = ""
    days = ["\n	&#127761; Понедельник:\n",
            "\n &#127762; Вторник:\n",
            "\n &#127763; Среда:\n",
            "\n &#127764; Четверг:\n",
            "\n &#127765; Пятница:\n",
            "\n &#127766; Суббота:\n",            ]
    for i in range(1, 7):
        subs = find_subjects_by_group(group, i)

        subs = choose_subs(subs, week)

        msg += days[i-1]
        msg += build_msg(subs, week)
    return msg


def on_today(us):
    group = us.student_group
    day = datetime.datetime.today().weekday()+1
    subs = find_subjects_by_group(group, day)
    week = datetime.datetime.today().isocalendar()[1]-5
    subs = choose_subs(subs, week)
    days = ["понедельник:\n",
            "вторник:\n",
            "среда:\n",
            "четверг:\n",
            "пятница:\n",
            "суббота:\n",
            "воскресение\n"]

    return f"Сегодня {days[day-1]}\n" + build_msg(subs, week)

def choose_subs(subs, week):
    for i in range(12):
        if "Военная" in subs[i]:
            for j in range(8):
                subs[i+j] = "военная подготовка;;занятие;;;;;;"
    if (week%2)==0:
        subs = subs[1:12:2]
    else:
        subs = subs[0:12:2]
    return subs

def on_tomorrow(us):
    group = us.student_group
    day = datetime.datetime.today().weekday()+1
    days = ["понедельник:\n",
            "вторник:\n",
            "среда:\n",
            "четверг:\n",
            "пятница:\n",
            "суббота:\n",
            "воскресение\n"]
    week = datetime.datetime.today().isocalendar()[1]-5
    if day == 7:
        day = 1
        week += 1
    else:
        day += 1
    subs = find_subjects_by_group(group, day)
    subs = choose_subs(subs, week)
    return  f"Завтра {days[day-1]}"+build_msg(subs, week)

def build_msg(subs, week):
    msg = ""
    time = ["9:00 - 10:40", "10:40 - 12:10", "12:40 - 14:10", "14:20 - 15:50", "16:20 - 17:50", "18:00 - 19:30"]

    for i in range(6):
        if subs[i] == "":
            continue
        if "…" in subs[i]:
            continue
        flesh = subs[i].split(";;")
        if flesh[3] == "Д":
            flesh[3] = "Дистанционно"
        flesh_royal = []
        if '\n' in flesh[0]:
            for j in range(4):
                if '\n' in flesh[j]:
                    flesh_royal += [flesh[j].split('\n')]
                else:
                    flesh_royal += [[flesh[j] for d in range(len(flesh_royal[0]))]]
        if not flesh_royal == []:
            flesh = []
            for j in range(len(flesh_royal[0])):
                flesh += [[flesh_royal[0][j], flesh_royal[1][j], flesh_royal[2][j], flesh_royal[3][j]]]
        else:
            flesh = [flesh]
        msg1 = ""


        for j in range(len(flesh)):
            if "н." in flesh[j][0]:

                if not str(week) in flesh[j][0]:
                    continue
                else:
                    flesh[j][0] = flesh[j][0][flesh[j][0].find("н.")+3::]
            msg1+=f"\n{flesh[j][0]} ({flesh[j][1]})\n\t{flesh[j][3]}, {flesh[j][2]}\n"
        if msg1 != "":
            msg += f"\nПара {i + 1}&#8419;({time[i]})"
            msg += msg1
    if msg == "":
        msg = "Выходной! Пар нет!"
    return msg