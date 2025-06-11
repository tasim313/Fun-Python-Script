import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer
import argparse
import sys
from IPython.display import display
import openpyxl
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import sqlite3
import psycopg2
import warnings

warnings.filterwarnings('ignore')

class LabWorkflowAnalyzer:
    def __init__(self):
        self.df = None
        self.numeric_cols = []
        self.categorical_cols = []
        
    def import_data(self, file_path=None, db_config=None, table_name=None):
        """
        Import data from various sources (Excel, CSV, SQL databases)
        """
        if file_path:
            if file_path.endswith('.csv'):
                self.df = pd.read_csv(file_path)
            elif file_path.endswith('.xlsx'):
                self.df = pd.read_excel(file_path, engine='openpyxl')
            else:
                raise ValueError("Unsupported file format. Please use CSV or Excel.")
        elif db_config:
            try:
                if db_config['type'].lower() == 'postgres':
                    conn = psycopg2.connect(
                        host=db_config['host'],
                        database=db_config['database'],
                        user=db_config['user'],
                        password=db_config['password']
                    )
                elif db_config['type'].lower() in ['sql', 'sqlite']:
                    conn = sqlite3.connect(db_config['database'])
                else:
                    raise ValueError("Unsupported database type")
                
                query = f"SELECT * FROM {table_name}"
                self.df = pd.read_sql(query, conn)
                conn.close()
            except Exception as e:
                print(f"Database connection error: {e}")
                return False
        
        if self.df is not None:
            self._identify_column_types()
            return True
        return False
    
    def _identify_column_types(self):
        """Identify numeric and categorical columns"""
        self.numeric_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        self.categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    def clean_data(self, handle_missing='drop', outlier_method='zscore', z_threshold=3):
        """
        Clean data by handling missing values and outliers
        """
        # Handle missing data
        if handle_missing == 'drop':
            self.df.dropna(inplace=True)
        elif handle_missing == 'mean':
            for col in self.numeric_cols:
                self.df[col].fillna(self.df[col].mean(), inplace=True)
        elif handle_missing == 'median':
            for col in self.numeric_cols:
                self.df[col].fillna(self.df[col].median(), inplace=True)
        elif handle_missing == 'mode':
            for col in self.categorical_cols:
                self.df[col].fillna(self.df[col].mode()[0], inplace=True)
        
        # Handle outliers
        if outlier_method == 'zscore':
            for col in self.numeric_cols:
                z_scores = np.abs(stats.zscore(self.df[col]))
                self.df = self.df[(z_scores < z_threshold)]
        elif outlier_method == 'iqr':
            for col in self.numeric_cols:
                Q1 = self.df[col].quantile(0.25)
                Q3 = self.df[col].quantile(0.75)
                IQR = Q3 - Q1
                self.df = self.df[~((self.df[col] < (Q1 - 1.5 * IQR)) | 
                                  (self.df[col] > (Q3 + 1.5 * IQR)))]
        
        self._identify_column_types()
    
    def merge_datasets(self, other_df, on=None, how='inner'):
        """
        Merge with another dataset
        """
        if on is None:
            raise ValueError("Please specify column(s) to merge on")
        self.df = pd.merge(self.df, other_df, on=on, how=how)
        self._identify_column_types()
    
    def descriptive_stats(self, columns=None):
        """
        Generate descriptive statistics for selected columns
        """
        if columns is None:
            columns = self.numeric_cols
        else:
            columns = [col for col in columns if col in self.numeric_cols]
        
        if not columns:
            print("No numeric columns selected for analysis")
            return None
        
        stats_df = self.df[columns].describe(include='all').transpose()
        stats_df['mode'] = self.df[columns].mode().transpose()[0]
        stats_df['skewness'] = self.df[columns].skew()
        stats_df['kurtosis'] = self.df[columns].kurtosis()
        
        return stats_df
    
    def inferential_stats(self, test_type, target_col, group_col=None, predictor_cols=None):
        """
        Perform inferential statistical tests
        """
        if test_type.lower() == 't-test':
            if group_col is None or len(self.df[group_col].unique()) != 2:
                raise ValueError("For t-test, group_col must have exactly 2 categories")
            
            group1 = self.df[self.df[group_col] == self.df[group_col].unique()[0]][target_col]
            group2 = self.df[self.df[group_col] == self.df[group_col].unique()[1]][target_col]
            
            t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
            return {'Test': 'Independent t-test', 
                    'Groups': self.df[group_col].unique().tolist(),
                    't-statistic': t_stat, 
                    'p-value': p_value}
        
        elif test_type.lower() == 'anova':
            if group_col is None or len(self.df[group_col].unique()) < 2:
                raise ValueError("For ANOVA, group_col must have at least 2 categories")
            
            model = ols(f'{target_col} ~ C({group_col})', data=self.df).fit()
            anova_table = sm.stats.anova_lm(model, typ=2)
            return {'Test': 'One-way ANOVA', 
                    'Group Variable': group_col,
                    'ANOVA Table': anova_table}
        
        elif test_type.lower() == 'chi-square':
            if group_col is None:
                raise ValueError("For chi-square test, group_col must be specified")
            
            contingency_table = pd.crosstab(self.df[target_col], self.df[group_col])
            chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
            return {'Test': 'Chi-square test',
                    'Chi-square statistic': chi2,
                    'p-value': p,
                    'Degrees of freedom': dof,
                    'Contingency table': contingency_table}
        
        elif test_type.lower() == 'regression':
            if predictor_cols is None:
                raise ValueError("For regression, predictor_cols must be specified")
            
            X = self.df[predictor_cols]
            y = self.df[target_col]
            
            X = sm.add_constant(X)  # Add constant for intercept
            model = sm.OLS(y, X).fit()
            return model.summary()
        
        else:
            raise ValueError("Unsupported test type. Choose from: t-test, anova, chi-square, regression")
    
    def visualize_data(self, plot_type, x_col, y_col=None, group_col=None, **kwargs):
        """
        Create various visualizations
        """
        plt.figure(figsize=kwargs.get('figsize', (10, 6)))
        
        if plot_type == 'histogram':
            if x_col not in self.numeric_cols:
                raise ValueError("Histogram requires a numeric column")
            sns.histplot(data=self.df, x=x_col, kde=True, hue=group_col)
            plt.title(f'Distribution of {x_col}')
        
        elif plot_type == 'bar':
            if group_col:
                sns.barplot(data=self.df, x=x_col, y=y_col, hue=group_col)
                plt.title(f'{y_col} by {x_col} grouped by {group_col}')
            else:
                sns.barplot(data=self.df, x=x_col, y=y_col)
                plt.title(f'{y_col} by {x_col}')
        
        elif plot_type == 'scatter':
            if x_col not in self.numeric_cols or y_col not in self.numeric_cols:
                raise ValueError("Scatter plot requires two numeric columns")
            sns.scatterplot(data=self.df, x=x_col, y=y_col, hue=group_col)
            plt.title(f'{y_col} vs {x_col}')
        
        elif plot_type == 'box':
            sns.boxplot(data=self.df, x=group_col, y=x_col)
            plt.title(f'Distribution of {x_col} by {group_col}')
        
        elif plot_type == 'interactive':
            if plot_type == 'interactive':
                if y_col:
                    fig = px.scatter(self.df, x=x_col, y=y_col, color=group_col, 
                                    title=f'{y_col} vs {x_col}', **kwargs)
                else:
                    fig = px.histogram(self.df, x=x_col, color=group_col, 
                                     title=f'Distribution of {x_col}', **kwargs)
                fig.show()
                return
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        if kwargs.get('show', True):
            plt.show()
    
    def advanced_analytics(self, analysis_type, target_col=None, feature_cols=None, n_clusters=3, n_factors=2):
        """
        Perform advanced analytics like clustering and predictive modeling
        """
        if analysis_type == 'cluster':
            if not feature_cols:
                feature_cols = self.numeric_cols
            
            # Standardize the data
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(self.df[feature_cols])
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Add cluster labels to dataframe
            self.df['Cluster'] = clusters
            
            # Visualize clusters (first two features)
            if len(feature_cols) >= 2:
                plt.figure(figsize=(10, 6))
                sns.scatterplot(data=self.df, x=feature_cols[0], y=feature_cols[1], 
                                hue='Cluster', palette='viridis')
                plt.title(f'K-means Clustering (k={n_clusters})')
                plt.show()
            
            return {'Cluster Centers': kmeans.cluster_centers_,
                    'Cluster Labels': clusters}
        
        elif analysis_type == 'logistic':
            if not target_col or not feature_cols:
                raise ValueError("For logistic regression, target_col and feature_cols must be specified")
            
            # Convert target to binary if needed
            if len(self.df[target_col].unique()) > 2:
                median_val = self.df[target_col].median()
                y = (self.df[target_col] > median_val).astype(int)
            else:
                y = self.df[target_col]
            
            X = self.df[feature_cols]
            
            # Standardize features
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Fit logistic regression model
            model = LogisticRegression(random_state=42)
            model.fit(X_scaled, y)
            
            # Calculate predictions and probabilities
            y_pred = model.predict(X_scaled)
            y_prob = model.predict_proba(X_scaled)[:, 1]
            
            # Add predictions to dataframe
            self.df[f'{target_col}_Predicted'] = y_pred
            self.df[f'{target_col}_Probability'] = y_prob
            
            return {'Model Coefficients': dict(zip(feature_cols, model.coef_[0])),
                    'Intercept': model.intercept_[0],
                    'Accuracy': (y_pred == y).mean()}
        
        elif analysis_type == 'factor':
            if not feature_cols:
                feature_cols = self.numeric_cols
            
            # Check for missing values
            if self.df[feature_cols].isnull().any().any():
                raise ValueError("Factor analysis cannot handle missing values")
            
            # Perform factor analysis
            fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
            fa.fit(self.df[feature_cols])
            
            # Get factor loadings
            loadings = pd.DataFrame(fa.loadings_, 
                                   index=feature_cols, 
                                   columns=[f'Factor{i+1}' for i in range(n_factors)])
            
            return {'Factor Loadings': loadings,
                    'Variance Explained': fa.get_factor_variance()}
        
        else:
            raise ValueError("Unsupported analysis type. Choose from: cluster, logistic, factor")
    
    def export_results(self, output_type, output_path, stats_results=None, plot_path=None):
        """
        Export results to various formats
        """
        if output_type == 'excel':
            with pd.ExcelWriter(output_path) as writer:
                self.df.to_excel(writer, sheet_name='Data', index=False)
                if stats_results:
                    if isinstance(stats_results, pd.DataFrame):
                        stats_results.to_excel(writer, sheet_name='Statistics')
                    else:
                        pd.DataFrame.from_dict(stats_results, orient='index').to_excel(
                            writer, sheet_name='Statistics')
        
        elif output_type == 'pdf':
            doc = SimpleDocTemplate(output_path, pagesize=letter)
            elements = []
            
            # Add title
            styles = getSampleStyleSheet()
            elements.append(Paragraph("Laboratory Workflow Analysis Report", styles['Title']))
            
            # Add data summary
            elements.append(Paragraph("Data Summary", styles['Heading2']))
            summary_data = [
                ["Number of Records", str(len(self.df))],
                ["Numeric Columns", ", ".join(self.numeric_cols)],
                ["Categorical Columns", ", ".join(self.categorical_cols)]
            ]
            summary_table = Table(summary_data)
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
                ('GRID', (0, 0), (-1, -1), 1, '#000000')
            ]))
            elements.append(summary_table)
            
            # Add statistical results if provided
            if stats_results:
                elements.append(Paragraph("Statistical Results", styles['Heading2']))
                if isinstance(stats_results, pd.DataFrame):
                    stats_data = [stats_results.columns.tolist()] + stats_results.values.tolist()
                else:
                    stats_data = [[k, str(v)] for k, v in stats_results.items()]
                
                stats_table = Table(stats_data)
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), '#CCCCCC'),
                    ('GRID', (0, 0), (-1, -1), 1, '#000000')
                ]))
                elements.append(stats_table)
            
            # Add plot if provided
            if plot_path:
                elements.append(Paragraph("Visualization", styles['Heading2']))
                # Note: ReportLab would need an image reader to embed the plot
                # This is a simplified version
                elements.append(Paragraph(f"See attached plot at: {plot_path}", styles['Normal']))
            
            doc.build(elements)
        
        else:
            raise ValueError("Unsupported output type. Choose from: excel, pdf")
    
    def interactive_dashboard(self):
        """
        Launch an interactive Plotly Dash dashboard
        Note: This would typically be in a separate file
        """
        try:
            import dash
            from dash import dcc, html
            from dash.dependencies import Input, Output
            
            app = dash.Dash(__name__)
            
            app.layout = html.Div([
                html.H1("Laboratory Workflow Dashboard"),
                
                dcc.Dropdown(
                    id='x-axis',
                    options=[{'label': col, 'value': col} for col in self.df.columns],
                    value=self.numeric_cols[0] if self.numeric_cols else None
                ),
                
                dcc.Dropdown(
                    id='y-axis',
                    options=[{'label': col, 'value': col} for col in self.df.columns],
                    value=self.numeric_cols[1] if len(self.numeric_cols) > 1 else None
                ),
                
                dcc.Dropdown(
                    id='plot-type',
                    options=[
                        {'label': 'Scatter', 'value': 'scatter'},
                        {'label': 'Histogram', 'value': 'histogram'},
                        {'label': 'Box Plot', 'value': 'box'}
                    ],
                    value='scatter'
                ),
                
                dcc.Graph(id='workflow-plot')
            ])
            
            @app.callback(
                Output('workflow-plot', 'figure'),
                [Input('x-axis', 'value'),
                 Input('y-axis', 'value'),
                 Input('plot-type', 'value')]
            )
            def update_plot(x_col, y_col, plot_type):
                if plot_type == 'scatter':
                    return px.scatter(self.df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
                elif plot_type == 'histogram':
                    return px.histogram(self.df, x=x_col, title=f"Distribution of {x_col}")
                elif plot_type == 'box':
                    return px.box(self.df, x=x_col, y=y_col, title=f"Box Plot of {y_col} by {x_col}")
            
            print("Dashboard running on http://127.0.0.1:8050/")
            app.run_server(debug=True)
        except ImportError:
            print("Dash not installed. Please install with: pip install dash")


def main():
    parser = argparse.ArgumentParser(description="Pathological Laboratory Workflow Analysis Tool")
    parser.add_argument('--input', help='Input file path (CSV or Excel)')
    parser.add_argument('--db-type', help='Database type (postgres, sql, sqlite)')
    parser.add_argument('--db-name', help='Database name')
    parser.add_argument('--db-host', help='Database host')
    parser.add_argument('--db-user', help='Database user')
    parser.add_argument('--db-pass', help='Database password')
    parser.add_argument('--table', help='Database table name')
    parser.add_argument('--clean', action='store_true', help='Clean the data')
    parser.add_argument('--stats', help='Generate descriptive stats for columns (comma separated)')
    parser.add_argument('--test', help='Statistical test to perform (t-test, anova, chi-square, regression)')
    parser.add_argument('--target', help='Target column for statistical tests')
    parser.add_argument('--group', help='Grouping column for statistical tests')
    parser.add_argument('--predictors', help='Predictor columns for regression (comma separated)')
    parser.add_argument('--plot', help='Plot type (histogram, bar, scatter, box)')
    parser.add_argument('--x', help='X-axis column for plots')
    parser.add_argument('--y', help='Y-axis column for plots')
    parser.add_argument('--analysis', help='Advanced analysis type (cluster, logistic, factor)')
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--output-type', help='Output type (excel, pdf)')
    parser.add_argument('--dashboard', action='store_true', help='Launch interactive dashboard')
    
    args = parser.parse_args()
    
    analyzer = LabWorkflowAnalyzer()
    
    # Import data
    if args.input:
        if not analyzer.import_data(file_path=args.input):
            print("Failed to import data from file")
            sys.exit(1)
    elif args.db_type:
        db_config = {
            'type': args.db_type,
            'database': args.db_name,
            'host': args.db_host if args.db_host else 'localhost',
            'user': args.db_user,
            'password': args.db_pass if args.db_pass else ''
        }
        if not analyzer.import_data(db_config=db_config, table_name=args.table):
            print("Failed to import data from database")
            sys.exit(1)
    else:
        print("No input source specified")
        sys.exit(1)
    
    # Clean data if requested
    if args.clean:
        analyzer.clean_data()
    
    # Perform requested analyses
    results = None
    
    if args.stats:
        columns = args.stats.split(',') if args.stats else None
        results = analyzer.descriptive_stats(columns)
        print("\nDescriptive Statistics:")
        print(results)
    
    if args.test:
        if not args.target:
            print("Target column required for statistical tests")
            sys.exit(1)
        
        predictors = args.predictors.split(',') if args.predictors else None
        results = analyzer.inferential_stats(
            test_type=args.test,
            target_col=args.target,
            group_col=args.group,
            predictor_cols=predictors
        )
        print(f"\n{args.test} Results:")
        print(results)
    
    if args.plot:
        if not args.x:
            print("X-axis column required for plots")
            sys.exit(1)
        
        analyzer.visualize_data(
            plot_type=args.plot,
            x_col=args.x,
            y_col=args.y,
            group_col=args.group,
            show=True
        )
    
    if args.analysis:
        feature_cols = args.predictors.split(',') if args.predictors else None
        results = analyzer.advanced_analytics(
            analysis_type=args.analysis,
            target_col=args.target,
            feature_cols=feature_cols
        )
        print(f"\n{args.analysis} Results:")
        print(results)
    
    # Export results if requested
    if args.output and args.output_type:
        analyzer.export_results(
            output_type=args.output_type,
            output_path=args.output,
            stats_results=results
        )
        print(f"\nResults exported to {args.output}")
    
    # Launch dashboard if requested
    if args.dashboard:
        analyzer.interactive_dashboard()

if __name__ == '__main__':
    main()