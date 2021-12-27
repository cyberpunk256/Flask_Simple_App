from flask import session, redirect

USERLIST = {
	"taro": "aaa",
	"jiro": "bbb",
	"sabu": "ccc",
}

def is_login():
	return "login" in session

def try_login(user,password):
	if user not in USERLIST: return False
	if USERLIST[user] != password: return False
	session["login"] = user
	return True

def try_logout():
	session.pop("login",None)
	return True

def get_user():
	if is_login(): return session["login"]
	return "not login"