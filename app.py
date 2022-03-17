import fdb
import datetime
from flask import Flask, request, render_template
from datetime import date, datetime
import calendar

app = Flask(__name__)

ip = "192.168.100.19"
# ip = "192.168.100.192"


sql_rasp_template = """select distinct np_otd.notd,n_mpp.nmpp,
  (select nspz as ndlj from n_spz where it_rasp.spz=n_spz.spz),
  (select nroom_kr as rname from room where room.id=it_rasp.room),
  CASE 
     when (EXTRACT(WEEK from dateoff)=EXTRACT(WEEK from Cast('NOW' as Date)))
     and (it_rasp.dateoff>=Cast('NOW' as Date)) then NULL 
  ELSE 
     (select interval_time from it_rasp_time where it_rasp.id_interval2=it_rasp_time.id) 
  END as even_day,
  CASE 
     when (EXTRACT(WEEK from dateoff)=EXTRACT(WEEK from Cast('NOW' as Date)))
     and (it_rasp.dateoff>=Cast('NOW' as Date)) then NULL  
  ELSE 
     (select interval_time from it_rasp_time where it_rasp.id_interval1=it_rasp_time.id)
  END as noeven_day,
  (select distinct TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6)
   and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
   (select distinct TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7)
    and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu={lpu} and n_doc.otd={otd}
    and (it_rasp.ntv={ntv}) and (it_rasp.nlist={nlist})
    order by IT_RASP.PS, nmpp"""


def sql_rasp(lpu, ntv, otd, nlist):
    sql_rasp_done = sql_rasp_template.format(
        lpu=lpu, ntv=ntv, otd=otd, nlist=nlist)
    return sql_rasp_done


def even_or_odd():
    d = datetime.today()
    if d.day % 2 == 0:
        return True

    else:
        return False


def style_evenday():
    if calendar.day_name[date.today().weekday()] != "Saturday" and calendar.day_name[date.today().weekday()] != "Sunday":
        if even_or_odd():
            return "today"
        else:
            return ""
    else:
        return ""


def style_noevenday():
    if calendar.day_name[date.today().weekday()] != "Saturday" and calendar.day_name[date.today().weekday()] != "Sunday":
        if even_or_odd():
            return ""
        else:
            return "today"
    else:
        return ""


def style_saturday():
    if calendar.day_name[date.today().weekday()] == "Saturday":
        return "today"
    else:
        return ""


def style_sunday():
    if calendar.day_name[date.today().weekday()] == "Sunday":
        return "today"
    else:
        return ""


def db_select(sql):
    con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB',
                      user='sysdba', password='masterkey', charset="utf-8")
    cur = con.cursor()
    cur.execute(sql)
    result_select = cur.fetchall()
    cur.close()
    del cur
    return result_select


def list_to_int(list_result):
    string_result = ''.join(str(e) for e in list_result)
    string_result = string_result.replace('(', '')
    string_result = string_result.replace(')', '')
    string_result = string_result.replace(',', '')
    string_result = int(string_result)
    return string_result


lpu = 165

print("Конфигурация для ЛПУ: ", lpu)

sql_max_tv = "select max(NTV) from IT_RASP_CONFIGOTD where lpu=%s" % lpu
max_tv = db_select(sql_max_tv)
ntv_max = list_to_int(max_tv)
for i in range(1, ntv_max+1):
    sql_maximum_str_template = """select max(nlist) from IT_RASP_CONFIGOTD where lpu={lpu} and ntv={ntv}"""
    sql_maximum_str = sql_maximum_str_template.format(lpu=lpu, ntv=i)
    max_str = db_select(sql_maximum_str)
    max_str = list_to_int(max_str)
    # print("Телевизор: ", i, "Максимум страниц: ", max_str)
    for p in range(1, max_str+1):
        sql_maximum_otd_template = """select count(otd) from IT_RASP_CONFIGOTD where lpu={lpu} and ntv={ntv} and nlist={nlist}"""
        sql_maximum_otd = sql_maximum_otd_template.format(
            lpu=lpu, ntv=i, nlist=p)
        max_otd = db_select(sql_maximum_otd)
        max_otd = list_to_int(max_otd)

        print("Телевизор: ", i, "Страница: ", p, "Отделений: ", max_otd)


def tv_config(lpu_number, tv_number):
    sql_maximum_str_template = """select max(nlist) from IT_RASP_CONFIGOTD where lpu={lpu} and ntv={ntv}"""
    sql_maximum_str = sql_maximum_str_template.format(
        lpu=lpu_number, ntv=tv_number)
    max_str = db_select(sql_maximum_str)
    max_str = list_to_int(max_str)
    for p in range(1, max_str+1):
        sql_maximum_otd_template = """select count(otd) from IT_RASP_CONFIGOTD where lpu={lpu} and ntv={ntv} and nlist={nlist}"""
        sql_maximum_otd = sql_maximum_otd_template.format(
            lpu=lpu_number, ntv=tv_number, nlist=p)
        max_otd = db_select(sql_maximum_otd)
        max_otd = list_to_int(max_otd)
        return


@app.route('/', methods=['GET'])
def home():
    lpu = request.args.get('lpu')
    print(lpu)
    ntv = request.args.get('ntv')
    print(ntv)
    return render_template('index.html', ip=ip)


@app.route('/tv11', methods=['GET'])
def tv11():
    result1 = db_select(sql_rasp(165, 1, 12, 1))
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv11.html', my_list=result1, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/tv12', methods=['GET'])
def tv12():
    result1 = db_select(sql_rasp(165, 1, 16, 2))
    result2 = db_select(sql_rasp(165, 1, 14, 2))
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv12.html', my_list=result1, my_list2=result2, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


# @app.route('/tv21', methods=['GET'])
# def tv21():
#     result = db_select(tv2str1n1)
#     style_evenday_var = style_evenday()
#     style_noevenday_var = style_noevenday()
#     style_saturday_var = style_saturday()
#     style_sunday_var = style_sunday()
#
#     return render_template('tv21.html', my_list=result, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/tv22', methods=['GET'])
def tv22():
    result1 = db_select(sql_rasp(165, 2, 15, 1))
    result2 = db_select(sql_rasp(165, 2, 13, 1))
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv22.html', my_list1=result1, my_list2=result2, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/nohead', methods=['GET'])
def nohead():
    return render_template('nohead.html', ip=ip)


if __name__ == '__main__':
    app.run(host=ip, port="3000")
