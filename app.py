import fdb
from flask import Flask, abort, request, render_template, json, render_template_string

app = Flask(__name__)
# Соединение
# con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB', user='sysdba', password='masterkey')
# Объект курсора
# cur = con.cursor()
# # Выполняем запрос
# try:
#     # Выборка данных
#     cur.execute("""select np_otd.notd,n_mpp.nmpp,(select ndlj from n_dlj where n_doc.dolj=n_dlj.dlj),(select nroom_kr as rname from room where room.id=it_rasp.room),it_rasp.even_day,it_rasp.noeven_day,saturday,sunday
# from it_rasp,np_otd,n_doc,n_mpp
# where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc) and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=12
# and (it_rasp.ntv=1)
# order by it_rasp.lpu,notd,nmpp""")
#     # Обработка строк выборки
#     result = cur.fetchall()
#     for x in result:
#         print(x);
# except:
#     con.rollback()
tv1 = """select np_otd.notd,n_mpp.nmpp,(select ndlj from n_dlj
    where n_doc.dolj=n_dlj.dlj),(select nroom_kr as rname from room
    where room.id=it_rasp.room),it_rasp.even_day,it_rasp.noeven_day,saturday,sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=12
    and (it_rasp.ntv=1)
    order by it_rasp.lpu,notd,nmpp"""

tv2 = """select np_otd.notd,n_mpp.nmpp,(select ndlj from n_dlj
    where n_doc.dolj=n_dlj.dlj),(select nroom_kr as rname from room
    where room.id=it_rasp.room),it_rasp.even_day,it_rasp.noeven_day,saturday,sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=16
    and (it_rasp.ntv=2)
    order by it_rasp.lpu,notd,nmpp"""

tv3 = """select np_otd.notd,n_mpp.nmpp,(select ndlj from n_dlj
    where n_doc.dolj=n_dlj.dlj),(select nroom_kr as rname from room
    where room.id=it_rasp.room),it_rasp.even_day,it_rasp.noeven_day,saturday,sunday
    from it_rasp,np_otd,n_doc,n_mpp
    where (it_rasp.otd=np_otd.otd) and (it_rasp.doc=n_doc.doc)
    and (n_doc.mpp=n_mpp.mpp) and (n_doc.pv=1) and it_rasp.lpu=165 and n_doc.otd=14
    and (it_rasp.ntv=2)
    order by it_rasp.lpu,notd,nmpp"""


def db_select(ntv) -> object:
    con4 = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB', user='sysdba', password='masterkey')
    cur4 = con4.cursor()
    cur4.execute(ntv)
    result4 = cur4.fetchall()
    cur4.close()
    return result4


result = db_select(tv1)
result2 = db_select(tv2)
result3 = db_select(tv3)


# con = fdb.connect(dsn='192.168.100.9:C:/DB/ARENA.GDB', user='sysdba', password='masterkey')
# cur = con.cursor()
# cur.execute(tv1)
# result = cur.fetchall()
# cur.execute(tv2)
# result2 = cur.fetchall()
# cur.close()
#
# result = db_select(tv1)
# del cur


@app.route('/', methods=['GET'])
def hello():  # put application's code here
    return render_template('index.html')


@app.route('/tv1', methods=['GET'])
def tv1():
    return render_template('tv1.html', my_list=result)


@app.route('/tv2', methods=['GET'])
def tv2():
    return render_template('tv2.html', my_list=result2, my_list2=result3)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8080")
