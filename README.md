### **Udemy Flask course project :shipit:**

**Setup:**
 - Clone the repo
   - `$git clone https://github.com/ruiheinonen/Flask_course_project.git`
   - `$cd Flask_course_project*`
   
 - Set up SQLite database
   - `$flask db init`
   - `$flask db migrate -m 'my first migration'`
   - `$flask db upgrade`
 
 - Create and activate virtual environment
   - `$virtualenv  flaskblogenv`
   - `$source flaskblogenv/bin/activate`
 - Install dependencies 
   - `$pip install -r requirements.txt`

**Run the application:**
- `$python app.py`\
`*Running on http://localhost:5000/`


***

### Project description

Simple blog page where multiple users can each log in with their uesr credentials. Each user can view other users' blog posts, create new posts and delete their own posts as well. Each user can update their username, email address, profile picture and background image. By default the site hosts its own profile and background images. Users can also cyckle through pages: whenever there is more than five blog posts the website just shift those over to another page. The SQLite database has two tables: `User` with columns id, profile_image, bg_image, email, username and password_hash and `BlogPost`with columns id, user_id, date, text and title.
