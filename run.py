from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
import datetime
import pickle
userdata = { "admin":"adminhahahaha"}
data = []


class LoginHandler(RequestHandler):
    def get(self):
        self.render("html/login/login.html")

class RegisterPageHandler(RequestHandler):
    def get(self):
        self.render("html/register/register.html")

class RegisterHandler(RequestHandler):
    def post(self):
        id_ = self.get_body_argument('id')
        password = self.get_body_argument('password')
        password_confirm = self.get_body_argument('password_confirm')
        
        output_mesg = ""
        success_flag = 0
        
        if id_ == "":
            output_mesg = "error: you must input id"
        elif password == "":
            output_mesg = "error: you must input password"
        elif password != password_confirm:
            output_mesg = "error: password and confirm password is not same"
        elif id_ in userdata:
            output_mesg = "error: already registered id"
        else:
            userdata[id_] = password
            output_mesg = "register success!"
            success_flag = 1
        if success_flag == 0:
            self.render("html/register/register_confirm.html", output_mesg=output_mesg)
        else:
            self.render("html/register/register_success.html", output_mesg=output_mesg)

class LoginProcessHandler(RequestHandler):
    def post(self):
        id_  = self.get_body_argument('id')
        password = self.get_body_argument('password')
    
        output_mesg = ""
        success_flag = 0

        if id_ == "":
            output_mesg = "input id please"
        elif id_ not in userdata:
            output_mesg = "unable id or invaild password"
        elif password != userdata[id_]:
            output_mesg = 'unable id or unvalid password'
        else:
            output_mesg = "Login success!"
            success_flag = 1

        if success_flag == 0:
            self.render("html/login/login_process.html", output_mesg = output_mesg)
        
        if id_ == 'admin':
            self.render("html/login/login_admin.html")
            
        else:
            self.render("html/login/login_success.html", output_mesg = output_mesg, id = id_)

class TalkHandler(RequestHandler):
    def post(self):
        user = self.get_body_argument('user')
        mesg = self.get_body_argument('mesg')
        dt = datetime.datetime.now()
        date = dt.strftime("%A %B %d %H:%M:%S %Y")
        ip = self.request.remote_ip
        userdata = user
        if mesg != "":
            data.append((user,mesg, date, ip))
        self.render("html/talk/talk.html", data = data, time = date, userdata = user)


class AdminHandler(RequestHandler):
    def post(self):
        cmd = ""
        cmd = self.get_body_argument('cmd')
        flag = 0
        if cmd == "dump":
            f = open("dump.hist", "wb")
            pickle.dump(data, f)
            f.close()
        elif cmd == "load":
            tmp_data = pickle.load(open("dump.hist", "rb"))
            flag = 1
        if flag == 0:
            self.render("html/talk/admin.html", alldata = data)
        else:
            self.render("html/talk/admin.html", alldata = tmp_data)


class LogoutHandler(RequestHandler):
    def post(self):
        dt = datetime.datetime.now()
        date = dt.strftime("%A %B %d %H:%M:%S %Y")
        ip = self.request.remote_ip
        user=self.get_body_argument('user')
        
        data.append((user, "loggouted", date, ip))
        self.render("html/talk/logout.html")

def make_app():
    handler_list = []
    handler_list.append((r"/", LoginHandler))
    handler_list.append((r"/register", RegisterPageHandler))
    handler_list.append((r"/register_process", RegisterHandler))
    handler_list.append((r"/login_process", LoginProcessHandler))
    handler_list.append((r"/talk", TalkHandler))
    handler_list.append((r"/asfdasfqwecaxsdfargqwdcsadfasf", AdminHandler))
    handler_list.append((r"/logout", LogoutHandler))
    return Application(handler_list)

if __name__ == '__main__':
    app = make_app()
    app.listen(8080)
    IOLoop.current().start()
