

from flask import Blueprint, send_file


staticpages = Blueprint('staticpages', __name__, template_folder='templates')
@staticpages.route("/admin.html", methods=["GET"])
def adminhtml():
    return send_file("./22widissisnu/" + "admin.html")

@staticpages.route("/board.html", methods=["GET"])
def boardhtml():
    return send_file("./22widissisnu/" + "board.html")

@staticpages.route("/medialog.html", methods=["GET"])
def medialoghtml():
    return send_file("./22widissisnu/" + "medialog.html")

@staticpages.route("/login.html", methods=["GET"])
def loginhtml():
    return send_file("./22widissisnu/" + "login.html")

@staticpages.route("/index.html", methods=["GET"])
def indexhtml():
    return send_file("./22widissisnu/" + "index.html")

@staticpages.route("/reply.html", methods=["GET"])
def replyhtml():
    return send_file("./22widissisnu/" + "reply.html")

@staticpages.route("/pages/login/login.css", methods=["GET"])
def pagesloginlogincss():
    return send_file("./22widissisnu/" + "pages/login/login.css")

@staticpages.route("/pages/login/login.js", methods=["GET"])
def pagesloginloginjs():
    return send_file("./22widissisnu/" + "pages/login/login.js")

@staticpages.route("/pages/board/board.js", methods=["GET"])
def pagesboardboardjs():
    return send_file("./22widissisnu/" + "pages/board/board.js")

@staticpages.route("/pages/board/board.css", methods=["GET"])
def pagesboardboardcss():
    return send_file("./22widissisnu/" + "pages/board/board.css")

@staticpages.route("/pages/admin/admin.css", methods=["GET"])
def pagesadminadmincss():
    return send_file("./22widissisnu/" + "pages/admin/admin.css")

@staticpages.route("/pages/admin/admin.js", methods=["GET"])
def pagesadminadminjs():
    return send_file("./22widissisnu/" + "pages/admin/admin.js")

@staticpages.route("/pages/index/index.css", methods=["GET"])
def pagesindexindexcss():
    return send_file("./22widissisnu/" + "pages/index/index.css")

@staticpages.route("/pages/index/images/login.png", methods=["GET"])
def pagesindeximagesloginpng():
    return send_file("./22widissisnu/" + "pages/index/images/login.png")

@staticpages.route("/pages/index/images/board.png", methods=["GET"])
def pagesindeximagesboardpng():
    return send_file("./22widissisnu/" + "pages/index/images/board.png")

@staticpages.route("/pages/medialog/medialog.css", methods=["GET"])
def pagesmedialogmedialogcss():
    return send_file("./22widissisnu/" + "pages/medialog/medialog.css")

@staticpages.route("/pages/reply/reply.js", methods=["GET"])
def pagesreplyreplyjs():
    return send_file("./22widissisnu/" + "pages/reply/reply.js")

@staticpages.route("/images/light.svg", methods=["GET"])
def imageslightsvg():
    return send_file("./22widissisnu/" + "images/light.svg")

@staticpages.route("/images/favicon.png", methods=["GET"])
def imagesfaviconpng():
    return send_file("./22widissisnu/" + "images/favicon.png")

@staticpages.route("/images/dark.svg", methods=["GET"])
def imagesdarksvg():
    return send_file("./22widissisnu/" + "images/dark.svg")

@staticpages.route("/images/youtube.png", methods=["GET"])
def imagesyoutubepng():
    return send_file("./22widissisnu/" + "images/youtube.png")

@staticpages.route("/styles/styles_dark.css", methods=["GET"])
def stylesstyles_darkcss():
    return send_file("./22widissisnu/" + "styles/styles_dark.css")

@staticpages.route("/styles/global.css", methods=["GET"])
def stylesglobalcss():
    return send_file("./22widissisnu/" + "styles/global.css")

@staticpages.route("/styles/styles_light.css", methods=["GET"])
def stylesstyles_lightcss():
    return send_file("./22widissisnu/" + "styles/styles_light.css")

@staticpages.route("/scripts/candyland.js", methods=["GET"])
def scriptscandylandjs():
    return send_file("./22widissisnu/" + "scripts/candyland.js")

@staticpages.route("/scripts/theme.js", methods=["GET"])
def scriptsthemejs():
    return send_file("./22widissisnu/" + "scripts/theme.js")

@staticpages.route("/scripts/init.js", methods=["GET"])
def scriptsinitjs():
    return send_file("./22widissisnu/" + "scripts/init.js")

@staticpages.route("/scripts/hash.js", methods=["GET"])
def scriptshashjs():
    return send_file("./22widissisnu/" + "scripts/hash.js")

@staticpages.route("/scripts/login.js", methods=["GET"])
def scriptsloginjs():
    return send_file("./22widissisnu/" + "scripts/login.js")

@staticpages.route("/scripts/header.js", methods=["GET"])
def scriptsheaderjs():
    return send_file("./22widissisnu/" + "scripts/header.js")

@staticpages.route("/forgotpasswd.html", methods=["GET"])
def forgotpasswdhtml():
    return send_file("./22widissisnu/" + "forgotpasswd.html")

@staticpages.route("/pages/forgotpasswd/forgotpasswd.js", methods=["GET"])
def forgotpasswdjs():
    return send_file("./22widissisnu/" + "pages/forgotpasswd/forgotpasswd.js")
