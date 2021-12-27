from flask import Flask, redirect, request
from flask import render_template,send_file
import os,json,time
import fs_data

app = Flask(__name__)
MASTER_PW = "abcd"

# top page
@app.route("/")
def index():
	return render_template("index.html")

# meta info will be in database that contains download time, file name 
@app.route("/upload",methods=["POST"])
def upload():
	upfile = request.files.get("upfile",None)
	if upfile is None: return msg("Upload Fail")
	if upfile.filename == "": return msg("Upload fail")
	# get meta info
	meta = {
		"name": request.form.get("name","no name"),
		"memo": request.form.get("memo","none"),
		"pw": request.form.get("pw",""),
		"limit":int(request.form.get("limit","1")),
		"count": int(request.form.get("count","0")),
		"filename": upfile.filename
	}
	if (meta["limit"] == 0) or (meta["pw"] == ""):
		return msg("parameter not right")
	fs_data.save_file(upfile,meta)
	return render_template("info.html",meta=meta,mode="upload",url=request.host_url + "download/" + meta["id"])

# page about showing meta info
@app.route("/download/<id>")
def download(id):
	meta = fs_data.get_data(id)
	if meta is None: return msg("Parameter not right")
	return render_template("info.html", meta=meta, mode="download",url=request.host_url + "download_go/" + id)


@app.route("/download_go/<id>",methods=["POST"])
def download_go(id):
	meta = fs_data.get_data(id)
	if meta is None: return msg("Parameter not correct")
	pw = request.form.get("pw","")
	if pw != meta["pw"]: return msg("password not correct")
	meta["count"] = meta["count"] - 1
	if meta["count"] < 0:
		return msg("download over")
	fs_data.set_data(id,meta)
	if meta["time_limit"] < time.time():
		return msg("download time is over")
	return send_file(meta["path"],as_attachment=True,attachment_filename=meta["filename"])

@app.route("/admin/list")
def admin_list():
	if request.args.get("pw","") != MASTER_PW:
		return msg("Master Password is not correct")
	return render_template("admin_list.html",files=fs_data.get_all(),pw=MASTER_PW)

@app.route("/admin/remove/<id>")
def admin_remove(id):
	if request.args.get("pw","") != MASTER_PW:
		return msg("Master Password is not correct")
	fs_data.remove_data(id)
	return msg("deleted")

def msg(s):
	return render_template("error.html",message=s)

def filter_datetime(tm):
	return time.strftime(
		"%Y/%m/%d %H: %M:%S", time.localtime(tm))


app.jinja_env.filters["datetime"] = filter_datetime

if __name__ == "__main__":
	app.run(debug=True,host="0.0.0.0")