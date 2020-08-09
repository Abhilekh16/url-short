from flask import Flask,render_template, request,redirect, url_for, flash, abort, session, jsonify
import json
import os.path
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = '123hoola456'

@app.route('/')
def Home():
	return render_template('home.html',codes = session.keys())

@app.route('/short-url',methods=['GET','POST'])
def shortUrl():
	if request.method == 'POST':
		urls = {}

		if os.path.exists('urls.json'):
			with open('urls.json') as urls_file:
				urls = json.load(urls_file)

		if request.form['code'] in urls.keys():
			flash("This code has already been taken")
			return redirect(url_for('Home'))

		if 'url' in request.form.keys():
			urls[request.form['code']] = {'url':request.form['url']}

		else:
			f = request.files['file']
			full_name = request.form['code'] + secure_filename(f.filename)
			f.save("E:/Programs/url-short/static/userfile/" + full_name)
			urls[request.form['code']] = {'file':full_name}

		with open('urls.json','w') as url_file:
			json.dump(urls,url_file)
			session[request.form['code']] = True

		return render_template('short-url.html', code=request.form['code'])
	
	else:

		return redirect(url_for('Home'))

@app.route('/<string:code>')
def redirect_to_url(code):
	if os.path.exists('urls.json'):
		with open('urls.json') as urls_file:
			url = json.load(urls_file)
			if code in url.keys():
				if 'url' in url[code].keys():
					return redirect(url[code]['url'])
				else:
					return redirect(url_for('static',filename='userfile/'+url[code]['file']))
	return abort(404)

@app.errorhandler(404)
def page_not_found(error):
	return render_template('page_not_found.html'),404

@app.route('/api')
def api():
	return jsonify(list(session.keys()))