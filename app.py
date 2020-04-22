from flask import Flask, request, redirect, url_for
from flask import render_template
from werkzeug.utils import secure_filename
import shutil
import os

app = Flask(__name__, static_folder='public')

members = [ {'userid': 'blackdew', 'pw': '111111'},
        {'userid': 'duru', "pw": "222222"}]

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error" + directory)

def createimage(path):
    template = get_template('create.html')
    menu = get_menu()
    with open(f"./html/content/{request.form['title']}", 'w', encoding='utf-8') as f:
        f.write(request.form['desc'])
def get_template(text):
    with open("html/"+text, 'r', encoding='utf-8') as f:
        html = f.read()
    return html
def get_myfamily_menu():
    menu=[e for e in os.listdir('public/myfamily') if e[0] != '.']
    menu_temp = "<li><a href='../gallery.html?foldername={0}' target='iframe_content' >{0}</a></li>"
    return "\n".join([menu_temp.format(m) for m in menu])

def make_myfamily_folder():
    menu_temp = "<li><a href='{0}' target='iframe_content' >{0}</a></li>"
    return "\n".join([menu_temp.format(m) for m in menu])
    
    
@app.route('/')
def index_html():
    print("route / path")
    with open("html/index.html", 'r', encoding='utf-8') as f:
        html = f.read()
    junyuk_id = request.args.get('userid', ' ')
    return html.format("?userid=" + junyuk_id)

@app.route("/create", methods=['GET', 'POST'])
def create():
    template = get_template('create.html')
    menu = get_menu()
    if request.method == 'GET': 
        return template.format('', menu) + "GET"
    elif request.method == 'POST': 
        with open(f"./html/content/{request.form['title']}", 'w', encoding='utf-8') as f:
            f.write(request.form['desc'])
        return redirect('/')

@app.route('/<path>')
def read_page(path):
    print("route <path> path")
    junyuk_id = request.args.get('userid', ' ')
    with open(f"html/{path}", 'r', encoding='utf-8') as f:
        html = f.read()
    if path == "Welcome.html":
        return html.format(junyuk_id)
    return html

@app.route('/gallery.html')
def read_page_gallery():
    folder_name = request.args.get('foldername', ' ')
    with open(f"html/gallery.html", 'r', encoding='utf-8') as f:
        html = f.read()
    script= """
            function toggleImg(e) {
                document.getElementById("img").src = e
            }
            """
    gallery_html= f"""앨범 사진 추가 삭제 <form action="http://localhost:5000/fileupload?foldername={folder_name}" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <input type="submit" value="추가">
            </form>"""
    gallery_delete_html=f""" <form action="/delete_file?foldername={folder_name}" method="POST">
            <input type = "text" name="delete_file_name" placeholder="삭제할 파일 이름을 입력 하세요">
            <input type="submit" value="삭제">
            </form> """
    menu=[e for e in os.listdir('public/myfamily/'+folder_name) if e[0] != '.']
    gallery_infor =""
    if len(menu) > 0:
        menu_temp = "<li class='font_white'><img src='/public/myfamily/"+folder_name+"/{0}' height='200px' width='200px' onclick=toggleImg('/public/myfamily/"+folder_name+"/{0}')><font color='white'>{0}</font></li>"
        gallery_menu = "\n".join([menu_temp.format(m) for m in menu])
        gallery_infor="<h2> 아래 사진을 클릭 하시면 사진이 확대 되어 보입니다. <h2>"
    else:
        gallery_infor=""
        gallery_menu = ""
            
#     아래 사진을 클릭 하시면 사진이 확대 되어 보입니다.
    if len(menu) > 0:
        gallery_main = "<img id ='img' src='/public/myfamily/"+folder_name+"/"+menu[0] +"' height='400px' width='400px'>"
    else:
        gallery_main = "<H2> 사진이 없습니다. 사진을 추가해 주세요</H2>"
    return html.format(script,gallery_html, gallery_delete_html,gallery_infor,gallery_menu,gallery_main)
    
@app.route('/MyBaby/left2.html')

def read_page_MyBaby():
    menu = get_myfamily_menu()
    with open(f"html/Mybaby/left2.html", 'r', encoding='utf-8') as f:
        html = f.read()
    return html.format(menu)

@app.route('/MyBaby/create')
def create_Myfamily_menu(path):
    menu = get_myfamily_menu()
    with open(f"html/Mybaby/{path}", 'r', encoding='utf-8') as f:
        html = f.read()        
    return html.format(menu)

@app.route('/MyBaby/make_family_menu.html')
def make_family_menu():
    print("route make_family_menu ")
    with open(f"html/MyBaby/make_family_menu.html", 'r', encoding='utf-8') as f:
        html = f.read()
    return html
    
#     html = get_template("make_familiy_menu")
#     return html
@app.route('/MyBaby/delete_family_menu.html')
def delete_family_menu():
    with open(f"html/MyBaby/delete_family_menu.html", 'r', encoding='utf-8') as f:
        html = f.read()
    return html
    
#     html = get_template("make_familiy_menu")
#     return html


@app.route('/upload')
def render_file():
    return render_template('upload.html')

@app.route('/fileupload', methods=["GET", "POST"])
def upload_file():
    folder_name = request.args.get('foldername', ' ')
    if request.method == 'POST':
        f = request.files['file']
        #저장할 경로 + 파일명
        route = 'C:/Users/user/Desktop/web/3일차/수업내용/MyProject/public/myfamily/'+folder_name+"/"
        f.save(route + secure_filename(f.filename))
        return 'uploads 디렉토리 -> 파일 업로드 성공!'

@app.route('/delete_file',methods=["GET", "POST"])
def delete_image_file():
    if request.method == 'POST':
        folder_name = request.args.get('foldername', ' ')
        route = 'C:/Users/user/Desktop/web/3일차/수업내용/MyProject/public/myfamily/'+folder_name+"/"
        os.remove(route+request.form['delete_file_name'])
        return "삭제가 정상적으로 완료 되었습니다."

@app.route("/create", methods=['GET', 'POST'])
def make_image():
    template = get_template('create.html')
    menu = get_menu()
    if request.method == 'GET': 
        return template.format('', menu) + "GET"
    elif request.method == 'POST': 
        with open(f"./html/content/{request.form['title']}", 'w', encoding='utf-8') as f:
            f.write(request.form['desc'])
        return redirect('/')
    return 0
@app.route('/make_folder', methods=["GET", "POST"])
def make_folder():
    print("route make_folder ")
    dir_path = ""
    html = get_template("MyBaby/make_family_menu.html")
    print("-"*100)
    if request.method == 'GET':
        return html.format("")
    else:
        createFolder("public/myfamily/"+request.form['foldername'])
        return html + request.form['foldername'] +"생성이 완료 되었습니다."

@app.route("/delete_folder", methods=['GET', 'POST'])
def delete_folder():
    html = get_template("MyBaby/delete_family_menu.html")
    if request.method == 'GET':
        return html.format("GET") + "GET"
    else:
        print("*"*100)
        print(os.path.isdir('public/myfamily/'+request.form['foldername']))
        print("*"*100)
        if os.path.isdir('public/myfamily/'+request.form['foldername']):
            shutil.rmtree('public/myfamily/'+request.form['foldername'])
            return html.format("POST") + "메뉴가 정상적으로 삭제 되었습니다.<br>더이상 삭제할 내용이 없다면 재 접속 부탁 드립니다."  
#             return html + request.form['foldername']"삭제가 완료 되었습니다.<br> 재접속 부탁 드립니다."
        return html.format("POST") + "삭제할 메뉴가 없읍니다. 왼쪽의 메뉴 확인 부탁 드립니다." 
    return "폴더가 정상적으로 삭제 되었습니다.<br> 재 접속 부탁 드립니다."