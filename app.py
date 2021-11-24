import fdb
import datetime
from flask import Flask, abort, request, render_template, json, render_template_string, url_for
from datetime import date, datetime
import calendar

app = Flask(__name__)

tv1str1n1 = """select np_otd.notd,n_mpp.nmpp,
  (select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),
  (select nroom_kr as rname from room where room.id=it_rasp.room),
  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.even_day
  END as even_day,

  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.noeven_day
  END as noeven_day,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=12
    and (it_rasp.ntv=1) and (it_rasp.nlist=1)"""

tv1str2n1 = """  select np_otd.notd,n_mpp.nmpp,
  (select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),
  (select nroom_kr as rname from room where room.id=it_rasp.room),
  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.even_day
  END as even_day,

  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.noeven_day
  END as noeven_day,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=12
    and (it_rasp.ntv=1) and (it_rasp.nlist=2)"""

# tv1str2n2 = """select np_otd.notd,n_mpp.nmpp,
#   (select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),
#   (select nroom_kr as rname from room where room.id=it_rasp.room),
#   CASE
#      when it_rasp.dateoff>=Cast('NOW' as Date) then NULL
#   ELSE
#      it_rasp.even_day
#   END as even_day,
#
#   CASE
#      when it_rasp.dateoff>=Cast('NOW' as Date) then NULL
#   ELSE
#      it_rasp.noeven_day
#   END as noeven_day,
# (select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
# (select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
#     from it_rasp,np_otd,n_doc,n_mpp
#     where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
#     and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=14
#     and (it_rasp.ntv=1)
#     order by it_rasp.lpu,notd,nmpp"""


tv2str1n1 = """select np_otd.notd,n_mpp.nmpp,
  (select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),
  (select nroom_kr as rname from room where room.id=it_rasp.room),
  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.even_day
  END as even_day,

  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.noeven_day
  END as noeven_day,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=13
    and (it_rasp.ntv=2) and (it_rasp.nlist=1)
    order by it_rasp.lpu,notd,nmpp"""


tv2str2n1 = """select np_otd.notd,n_mpp.nmpp,
  (select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),
  (select nroom_kr as rname from room where room.id=it_rasp.room),
  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.even_day
  END as even_day,

  CASE 
     when it_rasp.dateoff>=Cast('NOW' as Date) then NULL 
  ELSE 
     it_rasp.noeven_day
  END as noeven_day,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
(select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=15
    and (it_rasp.ntv=2) and (it_rasp.nlist=2)"""

#
# tv2str2n2 = """select np_otd.notd,n_mpp.nmpp,
#   (select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),
#   (select nroom_kr as rname from room where room.id=it_rasp.room),
#   CASE
#      when it_rasp.dateoff>=Cast('NOW' as Date) then NULL
#   ELSE
#      it_rasp.even_day
#   END as even_day,
#
#   CASE
#      when it_rasp.dateoff>=Cast('NOW' as Date) then NULL
#   ELSE
#      it_rasp.noeven_day
#   END as noeven_day,
# (select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=6) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as saturday,
# (select TIME_DUTY from it_rasp_duty where (it_rasp_duty.doc=it_rasp.doc) and (it_rasp_duty.NDAY=7) and EXTRACT(WEEK from DATE_DUTY)=EXTRACT(WEEK from Cast('NOW' as Date))) as sunday
#     from it_rasp,np_otd,n_doc,n_mpp
#     where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
#     and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=13
#     and (it_rasp.ntv=2)
#     order by it_rasp.lpu,notd,nmpp"""


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
    con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB', user='sysdba', password='masterkey', charset="utf-8")
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


# @app.route('/head', methods=['GET'])
# def home():
#     tv = request.args.get('tv')
#     print(tv)
#     password = request.args.get('page')
#     print(password)
#
#     return render_template('index.html')

@app.route('/', methods=['GET'])
def home():
    tv = request.args.get('tv')
    print(tv)
    password = request.args.get('page')
    print(password)

    return render_template('index.html')


@app.route('/tv11', methods=['GET'])
def tv11():
    result = db_select(tv1str1n1)
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv11.html', my_list=result, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/tv12', methods=['GET'])
def tv12():
    result1 = db_select(tv1str2n1)
    # result2 = db_select(tv1str2n2)
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv12.html', my_list=result1, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/tv21', methods=['GET'])
def tv21():
    result = db_select(tv2str1n1)
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv21.html', my_list=result, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/tv22', methods=['GET'])
def tv22():
    result1 = db_select(tv2str2n1)
    # result2 = db_select(tv2str2n2)
    style_evenday_var = style_evenday()
    style_noevenday_var = style_noevenday()
    style_saturday_var = style_saturday()
    style_sunday_var = style_sunday()

    return render_template('tv22.html', my_list1=result1, style_evenday_var=style_evenday_var, style_noevenday_var=style_noevenday_var, style_saturday_var=style_saturday_var, style_sunday_var=style_sunday_var)


@app.route('/nohead', methods=['GET'])
def nohead():
    return render_template('nohead.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3000")
