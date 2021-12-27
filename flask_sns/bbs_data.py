import os,json,datetime

# set a file that is set
BASE_DIR = os.path.dirname(__file__)
SAVE_FILE = BASE_DIR + "/data/log.json"

# read file to return data as list by decoding Json dat
def load_data():
	if not os.path.exists(SAVE_FILE):
		return []
	
	with open(SAVE_FILE,"rt",encoding ="utf-8") as f:
		return json.load(f)

# decode data and write in file
def save_data(data_list):
	with open(SAVE_FILE,"wt",encoding="utf-8") as f:
		json.dump(data_list,f)

# put data in top of file
def save_data_append(user,text):
	tm = get_datetime_now()
	data = {"name":user,"text":text,"date":tm}
	data_list = load_data()
	data_list.insert(0,data)
	save_data(data_list)

# read all data from file to record the data in file
def get_datetime_now():
	now = datetime.datetime.now()
	return "{0:%Y/%m/%d %H: %M}".format(now)