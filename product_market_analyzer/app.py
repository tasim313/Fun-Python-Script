import os
import uuid
from flask import Flask, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
from utils.image_recognition import identify_product_from_image
from utils.scrapers import scrape_all_platforms
from utils.analysis import analyze_data
from utils.database import store_data, get_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form['product_name']
        image = request.files['product_image']

        filename = secure_filename(image.filename)
        unique_id = str(uuid.uuid4())
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
        image.save(filepath)

        refined_product_name = identify_product_from_image(filepath, product_name)
        scraped_data = scrape_all_platforms(refined_product_name)
        analysis_report = analyze_data(scraped_data)
        store_data(unique_id, refined_product_name, scraped_data, analysis_report)

        return redirect(url_for('results', report_id=unique_id))

    return render_template('index.html')

@app.route('/results/<report_id>')
def results(report_id):
    report = get_report(report_id)
    return render_template('results.html', report=report)

if __name__ == '__main__':
    app.run(debug=True)
