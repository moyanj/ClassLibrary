from datetime import datetime, timedelta

import jwt
from flask import Flask, render_template, request, url_for
from pypinyin import Style, lazy_pinyin

import moyansdk as m

app = Flask(__name__, template_folder="./datas", static_folder="./datas/statics")

config = m.rjson("config.json")
app.config['SECRET_KEY'] = config["secret_key"]
if config["HTTPS"] == "Ture":
    url = "https://{}".format(config["host"])
else:
    url = "http://{}".format(config["host"])
@app.errorhandler(404)
def error_404(e):
    return render_template('error/404.html', path=e, indexpage=url)

@app.get("/")
@app.route("/path:<err404>")
def index(err404=200):
    if err404 == 200:
        return render_template('index.html', url=url)
    else:
        return render_template('error/404.html', path=err404, indexpage=url)


@app.route('/data')
@app.get("/data/<name>")
def homepages(name="无"):
    if name == "无":
        return render_template('data.html')
    else:
        info_data_name = name
        try:
            info = m.rjson("./datas/info/{}.json".format(info_data_name))
            selfie = url_for('static', filename="image/{}.jpg".format(info_data_name))
        except IOError:
            return render_template('error/404.html', path=name, indexpage="{}/data/{}".format(url, name))
        else:
            return render_template('info.html', names=info["name"], birthday=info["birthday"], QQ=info["QQ"],
                                   net_name=info["net_name"], dingtalk=info["dingtalk"], wechat=info["wechat"],
                                   TEL=info["TEL"], LRB=info["LRB"], gender=info["gender"], tiktok=info["tiktok"],
                                   kuaishou=info["kuaishou"], address=info["address"], email=info["email"],
                                   selfie=selfie, url=url, id=info_data_name)


@app.get("/login")
def login():
    return render_template("login.html", urls=url)


@app.get("/img")
def photo():
    pass


@app.get("/token")
def get_token():
    uesrname = request.args.get("pass")
    payload = {
        'exp': datetime.now() + timedelta(days=int(config["Token_expiration_time"])),
        'username': uesrname
    }
    token = jwt.encode(payload, config["secret_key"], algorithm='HS256')
    return token


@app.route("/token/verify", methods=["GET"])
def token_verification():
    token = request.args.get("token")
    try:
        json_data = jwt.decode(token, config["secret_key"], algorithms=['HS256'], verify=False)["username"]
    except jwt.exceptions.ExpiredSignatureError:
        print("jwt.exceptions.ExpiredSignatureError")
        return "No"
    except jwt.exceptions.InvalidSignatureError:
        print("jwt.exceptions.InvalidSignatureError")
        return "No"
    except jwt.exceptions.DecodeError:
        print("jwt.exceptions.DecodeError")
        return "No"
    else:
        password = m.rfile("datas/pass.dt")
        if json_data not in password:
            return "No"
        elif json_data in password:
            return "Yes"


@app.route("/group")
def group():
    return render_template('group.html')


@app.route("/getpy")
def getpy():
    data = request.args.get("text")
    initial = ''.join(lazy_pinyin(data, style=Style.FIRST_LETTER))
    return initial


if __name__ == '__main__':
    app.run(host=config["host"], port=int(config["port"]), debug=True)
