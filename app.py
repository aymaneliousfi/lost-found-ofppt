import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)

# إعداد قاعدة البيانات الجديدة
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ofppt_lostfound.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# البلاصة فين غيتخزنو التصاور
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)

# تحديث الجدول باش يقبل اسم التصويرة
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(200), nullable=True) # خانة التصويرة

with app.app_context():
    db.create_all()

# الصفحة الرئيسية (كاتعرض وكاتستقبل المعلومات فدقة وحدة)
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # كنجبدو المعلومات من الفورميلار
        title = request.form['title']
        description = request.form['description']
        item_type = request.form['item_type']
        contact = request.form['contact']
        
        # التعامل مع التصويرة
        image = request.files['image']
        filename = None
        if image:
            filename = secure_filename(image.filename)
            # كنتأكدو واش المجلد كاين
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # كنسجلو كلشي فقاعدة البيانات
        new_item = Item(title=title, description=description, item_type=item_type, contact=contact, image_filename=filename)
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('home'))

    # كنجبدو ڭاع داكشي لي مخزن باش نعرضوه
    items = Item.query.order_by(Item.id.desc()).all()
    return render_template('index.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, port=5000)