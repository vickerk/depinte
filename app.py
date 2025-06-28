from flask import Flask, render_template, jsonify, request, url_for
import match_parser
import os
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename
import json
import errno
from datetime import datetime, timedelta


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit
ACTIVITIES_FILE = 'activities.json'
CONTENT_FILE_HOME = 'saved_content_home.html'
CONTENT_FILE_EDITOR = 'saved_content_editor.html'
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
IMAGE_FOLDER = os.path.join(app.root_path, 'static', 'images')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
CONTENT_FILE_ABOUT = 'saved_content_about.html'
SIZE_FILE = "image_size.txt"
TRAINING_TABLE_FILE = 'training_table.json'


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route('/api/training-table', methods=['GET', 'POST'])
def training_table():
    if request.method == 'GET':
        if os.path.exists(TRAINING_TABLE_FILE):
            with open(TRAINING_TABLE_FILE, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({"headers": [], "rows": []})

    elif request.method == 'POST':
        data = request.json
        with open(TRAINING_TABLE_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return jsonify({"message": "Table saved successfully"}), 200



@app.route("/image_size_delete", methods=["GET", "POST"])
def image_size_delete():
    if request.method == "POST":
        activity_id = request.json.get("activityId")
        sizes = read_image_sizes()
        del sizes["activities"][activity_id]

        with open(SIZE_FILE, "w") as f:
            json.dump(sizes, f, indent=2)
        print(sizes)
        return


def read_image_sizes():
    default = {
        "home": "medium",
        "activities": {}
    }
    try:
        with open(SIZE_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_image_size(page, size, activity_id=None):
    sizes = read_image_sizes()

    if page == "activities" and activity_id:
        print("succes")
        sizes.setdefault("activities", {})[activity_id] = size
    elif page == "home":
        sizes["home"] = size
    else:
        raise ValueError("Invalid page or missing activity ID")

    with open(SIZE_FILE, "w") as f:
        json.dump(sizes, f, indent=2)


@app.route("/image_size", methods=["GET", "POST"])
def image_size():
    if request.method == "POST":
        page = request.json.get("page")
        size = request.json.get("size")
        activity_id = request.json.get("activityId")

        if size not in {"small", "medium", "big"}:
            return jsonify({"status": "error", "message": "Invalid size"}), 400

        try:
            write_image_size(page, size, activity_id)
            return jsonify({"status": "success"})
        except ValueError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

    # GET request
    sizes = read_image_sizes()
    return jsonify(sizes)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Add to hoster.py

@app.route('/api/image-config')
def get_image_config():
    """Return the image configuration with resolved URLs"""
    image_config = {
          "TTCjeugd": {
              "src": url_for('static', filename='images/TTCjeugd.jpg'),
              "alt": "Jeugd foto",
              "attrs": {'data-editable': 'true'}
          },
          "volwassenen": {
              "src": url_for('static', filename='images/volwassenen.jpg'),
              "alt": "Volwassenen foto",
              "attrs": {'data-editable': 'true'}
          },
          "sponsor_1": {
              "src": url_for('static', filename='images/sponsor_1.jpg'),
              "alt": "sponsor_1",
              "attrs": {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "sponsor_2": {
              "src": url_for('static', filename='images/sponsor_2.jpg'),
              "alt": "sponsor_2",
              "attrs": {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "sponsor_3": {
              "src": url_for('static', filename='images/sponsor_3.jpg'),
              "alt": "sponsor_3",
              'attrs': {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "sponsor_4": {
              "src": url_for('static', filename='images/sponsor_4.jpg'),
              "alt": "sponsor_4",
              "attrs": {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "sponsor_5": {
              "src": url_for('static', filename='images/sponsor_5.png'),
              "alt": "sponsor_5",
              "attrs": {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "sponsor_6": {
              "src": url_for('static', filename='images/sponsor_6.jpg'),
              "alt": "sponsor_6",
              "attrs": {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "sponsor_7": {
              "src": url_for('static', filename='images/sponsor_7.png'),
              "alt": "sponsor_7",
              "attrs": {'class': 'sponsor-image', 'data-editable': 'true'}
          },
          "board_1": {
              "src": url_for('static', filename='images/board_1.jpg'),
              "alt": "benny",
              "attrs": {'data-editable': 'true'}
          },
          "board_2": {
              "src": url_for('static', filename='images/board_2.jpg'),
              "alt": "david",
              "attrs": {'data-editable': 'true'}
          },
          "board_3": {
              "src": url_for('static', filename='images/board_3.jpg'),
              "alt": "felix",
              "attrs": {'data-editable': 'true'}
          },
          "board_4": {
              "src": url_for('static', filename='images/board_4.jpg'),
              "alt": "jan",
              "attrs": {'data-editable': 'true'}
          },
          "board_5": {
              "src": url_for('static', filename='images/board_5.jpg'),
              "alt": "johan",
              "attrs": {'data-editable': 'true'}
          },
          "board_6": {
              "src": url_for('static', filename='images/board_6.jpg'),
              "alt": "pascal",
              "attrs": {'data-editable': 'true'}
          },
          "board_7": {
              "src": url_for('static', filename='images/board_7.jpg'),
              "alt": "roland",
              "attrs": {'data-editable': 'true'}
          },
          "board_8": {
              "src": url_for('static', filename='images/board_8.jpg'),
              "alt": "rudy",
              "attrs": {'data-editable': 'true'}
          },
          "board_9": {
              "src": url_for('static', filename='images/board_9.jpg'),
              "alt": "rudy",
              "attrs": {'data-editable': 'true'}
          }
    }

    return jsonify(image_config)


@app.route('/upload_image', methods=['POST'])
def upload_image():
    print("upload tried to upload")
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        image_key = request.form.get('key')
        print(f"DEBUG - Received key: {image_key}")

        if not image_key:
            return jsonify({'error': 'No key provided'}), 400

        # Get file extension (preserve original extension)
        ext = file.filename.rsplit('.', 1)[1].lower()
        new_filename = secure_filename(f"{image_key}.{ext}")
        save_path = os.path.join(IMAGE_FOLDER, new_filename)

        # Overwrite the existing file with this key
        file.save(save_path)

        file_url = url_for('static', filename=f'images/{new_filename}')
        return jsonify({'url': file_url})

    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'error': 'Server error processing file'}), 500




@app.route('/upload', methods=['POST'])
def upload():
    print("upload tried to upload")
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        image_key = request.form.get('key')
        if image_key:
            # Non-editor image: save to static/images with key-based name
            ext = os.path.splitext(file.filename)[1].lower()
            if ext not in {'.jpg', '.jpeg'}:
                return jsonify({'error': 'Non-editor images must be JPG'}), 400

            filename = f"{image_key}.jpg"
            filepath = os.path.join(app.root_path, 'static', 'images', filename)
            file.save(filepath)
            file_url = url_for('static', filename=f'images/{filename}')
        else:
            # Editor image: save to uploads
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            file_url = url_for('static', filename=f'uploads/{filename}')

        return jsonify({'url': file_url})

    except Exception as e:
        print(f"Upload error: {e}")
        return jsonify({'error': 'Server error processing file'}), 500


def load_content_home():
    if os.path.exists(CONTENT_FILE_HOME):
        with open(CONTENT_FILE_HOME, 'r', encoding='utf-8') as file:
            return file.read()
    return ''


def load_content_editor():
    if os.path.exists(CONTENT_FILE_EDITOR):
        with open(CONTENT_FILE_EDITOR, 'r', encoding='utf-8') as file:
            return file.read()
    return ''


@app.route('/info/admin')
def info_a():
    content = load_content_editor()
    return render_template('info.html', content=content)


@app.route('/info')
def info():
    content = load_content_editor()
    return render_template('info_u.html', content=content)


@app.route('/save_home', methods=['POST'])
def save_home():
    content = request.form.get('content', '')
    with open(CONTENT_FILE_HOME, 'w', encoding='utf-8') as file:
        file.write(content)
        print(content)
    return "Auto-save successful", 200


@app.route('/save_editor', methods=['POST'])
def save_editor():
    content = request.form.get('content', '')
    with open(CONTENT_FILE_EDITOR, 'w', encoding='utf-8') as file:
        file.write(content)
        print(content)
    return "Auto-save successful", 200


def loading_activities():
    """Load activities from the JSON file."""
    if os.path.exists(ACTIVITIES_FILE):
        with open(ACTIVITIES_FILE, 'r') as file:
            return json.load(file)
    return []


@app.route('/api/top-activities', methods=['GET'])
def top_activities():
    activities = loading_activities()

    for activity in activities:
        for field in ['details', 'name']:
            soup = BeautifulSoup(activity.get(field, ''), 'html.parser')

            # Remove all image tags
            for img in soup.find_all('img'):
                img.decompose()

            # Remove style attributes
            for tag in soup.find_all(True):
                if 'style' in tag.attrs:
                    del tag.attrs['style']

            activity[field] = str(soup)

    activities.sort(key=lambda x: x['date'], reverse=True)
    return jsonify(activities[:3])


def load_activities():
    """Load activities from the JSON file."""
    if os.path.exists(ACTIVITIES_FILE):
        with open(ACTIVITIES_FILE, 'r') as file:
            return json.load(file)
    return []


def save_activities(activities):
    """Save activities to the JSON file."""
    with open(ACTIVITIES_FILE, 'w') as file:
        json.dump(activities, file)


@app.route('/cleanup_uploads', methods=['POST'])
def cleanup_uploads():
    try:
        now = datetime.now()
        cutoff = now - timedelta(days=7)

        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            # Skip directories
            if not os.path.isfile(filepath):
                continue

            # Check file age
            creation_time = datetime.fromtimestamp(os.path.getctime(filepath))
            if creation_time > cutoff:
                continue

            try:
                # Attempt to delete the file
                os.remove(filepath)
            except OSError as e:
                # Handle file-in-use errors specifically
                if e.errno == errno.EBUSY or e.errno == errno.EPERM:
                    print(f"Skipping in-use file: {filename}")
                # Handle file-not-found (already deleted)
                elif e.errno == errno.ENOENT:
                    continue
                else:
                    raise  # Re-raise unexpected errors

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Add new endpoint for saving about content
@app.route('/save_about', methods=['POST'])
def save_about():
    content = request.form.get('content', '')
    with open(CONTENT_FILE_ABOUT, 'w', encoding='utf-8') as file:
        file.write(content)
    return "Auto-save successful", 200


# Add new loader function
def load_content_about():
    if os.path.exists(CONTENT_FILE_ABOUT):
        with open(CONTENT_FILE_ABOUT, 'r', encoding='utf-8') as file:
            return file.read()
    return ''


# Update home route to load both content files
@app.route('/admin')
def home_a():
    sizes = read_image_sizes()
    content_home = load_content_home()
    content_about = load_content_about()  # New content
    return render_template(
        'home.html',
        content=content_home,
        content_about=content_about,  # Pass to template
        image_size=sizes['home']
    )


# Also update the home_u route similarly
@app.route('/')
def home():
    sizes = read_image_sizes()
    content_home = load_content_home()
    content_about = load_content_about()
    return render_template(
        'home_u.html',
        content=content_home,
        content_about=content_about,
        image_size=sizes['home']
    )


@app.route('/training')
def training():
    return render_template("training.html")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/activities/admin')
def activities_readonly():
    return render_template('activities.html')


@app.route('/activities')
def activities():
    return render_template('activities_u.html')


@app.route('/api/activities', methods=['GET', 'POST'])
def api_activities():
    if request.method == 'GET':
        return jsonify(load_activities())
    elif request.method == 'POST':
        activities = request.json
        save_activities(activities)
        return jsonify({"message": "Activities saved successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)