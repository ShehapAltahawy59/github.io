from NewsSphere.models.Models import User,Saved_news
from flask import render_template,request,redirect,url_for,jsonify
from NewsSphere.Forms.auth import regestration,Login
from NewsSphere import app,db,bcrypt
from requests import get
from flask_login import login_user,current_user,logout_user,login_required
import requests

key = "e856559f037147cabf276a4bd5135e02"
url = "https://newsapi.org/v2/top-headlines?country=eg&"
# business_response = get(url+"category=business&apiKey={}".format(key)).json()
# health_response = get(url+"category=health&apiKey={}".format(key)).json()
# general_response = get(url+"category=general&apiKey={}".format(key)).json()
# sports_response = get(url+"category=sports&apiKey={}".format(key)).json()
# technology_response = get(url+"category=technology&apiKey={}".format(key)).json()

# Function to fetch news articles
def fetch_news(category, query=None, page=1, page_size=5):
    url = f"https://newsapi.org/v2/top-headlines?country=eg&category={category}&page={page}&pageSize={page_size}&apiKey={key}"
    if query:
        
        url = f"https://newsapi.org/v2/top-headlines?q={query}&page={page}&pageSize={page_size}&apiKey={key}"
    response = requests.get(url).json()
    return response

@app.route("/")
def landing_page():
    
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    general_response = fetch_news(category="general", page=page, page_size=page_size)
    total_results = general_response.get('totalResults', 0)
    
    return render_template("landing_page.html", general_response=general_response['articles'], current_page=page, page_size=page_size, total_results=total_results)

@app.route('/Business')
def business():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    business_response = fetch_news(category="business", page=page, page_size=page_size)
    total_results = business_response.get('totalResults', 0)
    return render_template('landing_page.html', general_response=business_response['articles'], current_page=page, page_size=page_size, total_results=total_results)

@app.route('/Health')
def health():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    health_response = fetch_news(category="health", page=page, page_size=page_size)
    total_results = health_response.get('totalResults', 0)
    return render_template('landing_page.html', general_response=health_response['articles'], current_page=page, page_size=page_size, total_results=total_results)

@app.route('/Sports')
def sports():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    sports_response = fetch_news(category="sports", page=page, page_size=page_size)
    total_results = sports_response.get('totalResults', 0)
    return render_template('landing_page.html', general_response=sports_response['articles'], current_page=page, page_size=page_size, total_results=total_results)

@app.route('/Technology')
def technology():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('pageSize', 10, type=int)
    technology_response = fetch_news(category="technology", page=page, page_size=page_size)
    total_results = technology_response.get('totalResults', 0)
    return render_template('landing_page.html', general_response=technology_response['articles'], current_page=page, page_size=page_size, total_results=total_results)



@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    page = request.args.get('page', 1, type=int)  # Get the current page, default to 1
    page_size = request.args.get('pageSize', 10, type=int)  # Number of results per page, default to 10
    search_response =fetch_news(category=None,query=query,page=page,page_size=page_size)
    total_results = search_response.get('totalResults', 0)
    print(search_response)

    return render_template(
        'landing_page.html',
        general_response=search_response['articles'],
        query=query,
        current_page=page,
        page_size=page_size,
        total_results=total_results
    )


@app.route('/about')
def about_me():
    
    return render_template('about_me.html')

@app.route('/sources')
def sources():
   
    return render_template('sources.html')


@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('landing_page'))
    form = regestration()
    error = None
    if request.method == "POST":
        if (form.password.data != form.confirmed_password.data):
            error = "Passwords must match"
            
            return render_template('register.html', title = 'register',form =form,password_error=error)

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,password=hashed_password,email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', title = 'register',form =form,password_error=error)

@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('landing_page'))
    form = Login()
    error = None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user=user,remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page :
                print(next_page)
                return redirect((next_page))
            return redirect(url_for('landing_page'))
        else:
            error="please check Email and Password "
    return render_template('login.html', title = 'login',form =form, error=error)

@app.route('/logout',methods=["POST","GET"])
def logout():
    logout_user()
    return redirect(url_for('landing_page'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/save_news', methods=['POST'])
@login_required
def save_news():
    print("here")
    data = request.get_json()
    title = data['title']
    description = data.get('description', '')
    url = data['url']
    urlToImage = data['urlToImage']
    
    existing_news = Saved_news.query.filter_by(user_id=current_user.id, url=url).first()
    if existing_news:
        return jsonify(success=False, message='the news already saved.')

    new_news = Saved_news(title=title, description=description, url=url,urlToImage=urlToImage, user_id=current_user.id)
    db.session.add(new_news)
    db.session.commit()
    print("saved")
    return jsonify(success=True)


@app.route('/del_news', methods=['POST'])
@login_required
def del_news():
    print("here")
    data = request.get_json()
    url = data['url']
    
    existing_news = Saved_news.query.filter_by(user_id=current_user.id, url=url).first()

    if existing_news:
        db.session.delete(existing_news)
        db.session.commit()
        
        return jsonify(success=True)
    else:
        return jsonify(success=False, message='The news article does not exist.')


@app.route('/is_saved', methods=['GET'])
@login_required
def is_saved():
    url = request.args.get('url')

    saved_article = Saved_news.query.filter_by(user_id=current_user.id, url=url).first()
    is_saved = saved_article is not None

    return jsonify({'is_saved': is_saved})


@app.route('/Saved_News')
@login_required
def Saved_News():
    
    saved_news = Saved_news.query.filter_by(user_id=current_user.id)
    return render_template('saved_news.html',saved_news=saved_news)

if __name__ == '__main__':
    app.run(debug=True)
