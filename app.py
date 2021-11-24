import fdb
from flask import Flask, abort, request, render_template, json, render_template_string, url_for

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
    and (it_rasp.ntv=1)
    order by it_rasp.lpu,notd,nmpp"""

tv1str2n1 = """select np_otd.notd,n_mpp.nmpp,
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
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=16
    and (it_rasp.ntv=1)
    order by it_rasp.lpu,notd,nmpp"""


tv1str2n2 = """select np_otd.notd,n_mpp.nmpp,
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
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=14
    and (it_rasp.ntv=1)
    order by it_rasp.lpu,notd,nmpp"""


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
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=15
    and (it_rasp.ntv=2)
    order by it_rasp.lpu,notd,nmpp"""


tv2str1n2 = """select np_otd.notd,n_mpp.nmpp,
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
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=14
    and (it_rasp.ntv=2)
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
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=12
    and (it_rasp.ntv=1)
    order by it_rasp.lpu,notd,nmpp"""


def db_select(sql):
    con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB', user='sysdba', password='masterkey', charset="utf-8")
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    del cur
    return result


@app.route('/', methods=['GET'])
def home():

    return render_template('index.html')


@app.route('/tv11', methods=['GET'])
def tv11():
    result_tv1str1n1 = db_select(tv1str1n1)

    return render_template('tv11.html', my_list=result_tv1str1n1)


@app.route('/tv12', methods=['GET'])
def tv12():
    result_tv1str2n1 = db_select(tv1str2n1)
    result_tv1str2n2 = db_select(tv1str2n2)

    return render_template('tv12.html', my_list=result_tv1str2n1, my_list2=result_tv1str2n2)


@app.route('/tv21', methods=['GET'])
def tv21():
    result_tv2str1n1 = db_select(tv2str1n1)
    result_tv2str1n2 = db_select(tv2str1n2)

    return render_template('tv21.html', mylist=result_tv2str1n1, my_list2=result_tv2str1n2)


@app.route('/tv22', methods=['GET'])
def tv22():
    result_tv2str2n1 = db_select(tv2str2n1)
    print(result_tv2str2n1)

    return render_template('tv22.html', mylist=result_tv2str2n1)


@app.route('/nohead', methods=['GET'])
def nohead():

    return render_template('nohead.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="3000")
