from flask import Flask, render_template, request, redirect, url_for, send_file
from io import BytesIO
from lab_analyzer import LabWorkflowAnalyzer
import pandas as pd
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv', 'xlsx'}

analyzer = LabWorkflowAnalyzer()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            analyzer.import_data(file_path=filename)
            return redirect(url_for('analyze'))
    
    return render_template('index.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if analyzer.df is None:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'clean':
            handle_missing = request.form.get('handle_missing', 'drop')
            outlier_method = request.form.get('outlier_method', 'zscore')
            analyzer.clean_data(handle_missing=handle_missing, outlier_method=outlier_method)
        
        elif action == 'descriptive':
            columns = request.form.getlist('columns')
            stats = analyzer.descriptive_stats(columns)
            return render_template('analyze.html', 
                                 df=analyzer.df,
                                 numeric_cols=analyzer.numeric_cols,
                                 categorical_cols=analyzer.categorical_cols,
                                 stats=stats.to_html())
        
        elif action == 'inferential':
            test_type = request.form.get('test_type')
            target_col = request.form.get('target_col')
            group_col = request.form.get('group_col', None)
            predictors = request.form.get('predictors', None)
            
            if predictors:
                predictors = predictors.split(',')
            
            results = analyzer.inferential_stats(test_type, target_col, group_col, predictors)
            return render_template('analyze.html', 
                                 df=analyzer.df,
                                 numeric_cols=analyzer.numeric_cols,
                                 categorical_cols=analyzer.categorical_cols,
                                 inferential_results=results)
        
        elif action == 'visualize':
            plot_type = request.form.get('plot_type')
            x_col = request.form.get('x_col')
            y_col = request.form.get('y_col', None)
            group_col = request.form.get('group_col', None)
            
            # Save plot to a temporary file
            plot_path = 'static/plot.png'
            analyzer.visualize_data(plot_type, x_col, y_col, group_col, show=False)
            plt.savefig(plot_path)
            plt.close()
            
            return render_template('analyze.html', 
                                 df=analyzer.df,
                                 numeric_cols=analyzer.numeric_cols,
                                 categorical_cols=analyzer.categorical_cols,
                                 plot_path=plot_path)
        
        elif action == 'advanced':
            analysis_type = request.form.get('analysis_type')
            target_col = request.form.get('target_col_adv', None)
            feature_cols = request.form.get('feature_cols', None)
            
            if feature_cols:
                feature_cols = feature_cols.split(',')
            
            results = analyzer.advanced_analytics(analysis_type, target_col, feature_cols)
            return render_template('analyze.html', 
                                 df=analyzer.df,
                                 numeric_cols=analyzer.numeric_cols,
                                 categorical_cols=analyzer.categorical_cols,
                                 advanced_results=results)
        
        elif action == 'export':
            output_type = request.form.get('output_type')
            output_filename = f"results.{output_type}"
            
            if output_type == 'excel':
                output = BytesIO()
                with pd.ExcelWriter(output) as writer:
                    analyzer.df.to_excel(writer, sheet_name='Data', index=False)
                output.seek(0)
                return send_file(output, 
                               mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                               as_attachment=True, 
                               download_name=output_filename)
            
            elif output_type == 'csv':
                output = BytesIO()
                analyzer.df.to_csv(output, index=False)
                output.seek(0)
                return send_file(output, 
                               mimetype="text/csv", 
                               as_attachment=True, 
                               download_name=output_filename)
    
    return render_template('analyze.html', 
                         df=analyzer.df,
                         numeric_cols=analyzer.numeric_cols,
                         categorical_cols=analyzer.categorical_cols)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs('static', exist_ok=True)
    app.run(debug=True)