from flask import Flask, send_from_directory,render_template,request
import os

# 用当前脚本名称实例化Flask对象，方便flask从该脚本文件中获取需要的内容
app = Flask(__name__)

#程序实例需要知道每个url请求所对应的运行代码是谁。
#所以程序中必须要创建一个url请求地址到python运行函数的一个映射。
#处理url和视图函数之间的关系的程序就是"路由"，在Flask中，路由是通过@app.route装饰器(以@开头)来表示的
@app.route("/")
#url映射的函数，要传参则在上述route（路由）中添加参数申明
def index():
    return "Hello World!"

@app.route("/calendar",methods=['GET','POST'])
#url映射的函数，要传参则在上述route（路由）中添加参数申明
def calendar():
    if request.method == 'GET':
        # 想要html文件被该函数访问到，首先要创建一个templates文件，将html文件放入其中
        # 该文件夹需要被标记为模板文件夹，且模板语言设置为jinja2
        return render_template('课表.ics')
    # 此处欲发送post请求，需要在对应html文件的form表单中设置method为post
    # elif request.method == 'POST':
    #     name = request.form.get('name')
    #     password = request.form.get('password')
    #     print(name)
    #     print(password)
    #     return name+" "+password

UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'results')
 
@app.route('/download/<string:filename>/')
def download_file(filename):
    # return send_from_directory(UPLOAD_PATH, filename)
    return send_from_directory(UPLOAD_PATH, filename, as_attachment=True)

# 直属的第一个作为视图函数被绑定，第二个就是普通函数
# 路由与视图函数需要一一对应
# def not():
#     return "Not Hello World!"

# 启动一个本地开发服务器，激活该网页
app.run()