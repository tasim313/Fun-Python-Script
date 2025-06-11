#!/usr/bin/env python3
"""
PathLab Analytics - Pathological Laboratory Workflow Analysis Tool
A comprehensive SPSS-like tool for managing, analyzing, and visualizing lab workflow data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
from scipy import stats
from scipy.stats import chi2_contingency, pearsonr, spearmanr
import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.decomposition import PCA
import sqlite3
import psycopg2
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os
from datetime import datetime, timedelta
import threading
import io
import base64

class PathLabAnalytics:
    """Main class for pathological laboratory workflow analysis"""
    
    def __init__(self):
        self.data = None
        self.original_data = None
        self.analysis_results = {}
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        self.root = tk.Tk()
        self.root.title("PathLab Analytics - Laboratory Workflow Analysis Tool")
        self.root.geometry("1200x800")
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.setup_data_tab()
        self.setup_descriptive_tab()
        self.setup_inferential_tab()
        self.setup_visualization_tab()
        self.setup_advanced_tab()
        self.setup_automation_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready - Import data to begin analysis")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_data_tab(self):
        """Setup data management tab"""
        self.data_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_frame, text="Data Management")
        
        # Import section
        import_frame = ttk.LabelFrame(self.data_frame, text="Data Import")
        import_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(import_frame, text="Import CSV", command=self.import_csv).pack(side='left', padx=5, pady=5)
        ttk.Button(import_frame, text="Import Excel", command=self.import_excel).pack(side='left', padx=5, pady=5)
        ttk.Button(import_frame, text="Connect Database", command=self.connect_database).pack(side='left', padx=5, pady=5)
        
        # Data info section
        info_frame = ttk.LabelFrame(self.data_frame, text="Data Information")
        info_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Text widget for data info
        self.data_info_text = tk.Text(info_frame, height=15)
        scrollbar = ttk.Scrollbar(info_frame, orient="vertical", command=self.data_info_text.yview)
        self.data_info_text.configure(yscrollcommand=scrollbar.set)
        self.data_info_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Data cleaning section
        clean_frame = ttk.LabelFrame(self.data_frame, text="Data Cleaning")
        clean_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(clean_frame, text="Handle Missing Data", command=self.handle_missing_data).pack(side='left', padx=5, pady=5)
        ttk.Button(clean_frame, text="Remove Outliers", command=self.remove_outliers).pack(side='left', padx=5, pady=5)
        ttk.Button(clean_frame, text="Reset Data", command=self.reset_data).pack(side='left', padx=5, pady=5)
    
    def setup_descriptive_tab(self):
        """Setup descriptive statistics tab"""
        self.desc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.desc_frame, text="Descriptive Statistics")
        
        # Column selection
        col_frame = ttk.LabelFrame(self.desc_frame, text="Column Selection")
        col_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(col_frame, text="Select Columns:").pack(side='left', padx=5)
        self.desc_columns_var = tk.StringVar()
        self.desc_columns_combo = ttk.Combobox(col_frame, textvariable=self.desc_columns_var, width=30)
        self.desc_columns_combo.pack(side='left', padx=5, pady=5)
        
        ttk.Button(col_frame, text="Generate Statistics", command=self.generate_descriptive_stats).pack(side='left', padx=5, pady=5)
        ttk.Button(col_frame, text="All Columns", command=self.descriptive_all_columns).pack(side='left', padx=5, pady=5)
        
        # Results display
        results_frame = ttk.LabelFrame(self.desc_frame, text="Statistical Results")
        results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.desc_results_text = tk.Text(results_frame, height=20)
        desc_scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.desc_results_text.yview)
        self.desc_results_text.configure(yscrollcommand=desc_scrollbar.set)
        self.desc_results_text.pack(side="left", fill="both", expand=True)
        desc_scrollbar.pack(side="right", fill="y")
    
    def setup_inferential_tab(self):
        """Setup inferential statistics tab"""
        self.inf_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inf_frame, text="Inferential Statistics")
        
        # Test selection
        test_frame = ttk.LabelFrame(self.inf_frame, text="Statistical Tests")
        test_frame.pack(fill='x', padx=5, pady=5)
        
        # T-test section
        ttest_frame = ttk.Frame(test_frame)
        ttest_frame.pack(fill='x', pady=2)
        ttk.Label(ttest_frame, text="T-Test:").pack(side='left', padx=5)
        self.ttest_col1_var = tk.StringVar()
        self.ttest_col2_var = tk.StringVar()
        ttk.Combobox(ttest_frame, textvariable=self.ttest_col1_var, width=15).pack(side='left', padx=2)
        ttk.Combobox(ttest_frame, textvariable=self.ttest_col2_var, width=15).pack(side='left', padx=2)
        ttk.Button(ttest_frame, text="Run T-Test", command=self.run_ttest).pack(side='left', padx=5)
        
        # ANOVA section
        anova_frame = ttk.Frame(test_frame)
        anova_frame.pack(fill='x', pady=2)
        ttk.Label(anova_frame, text="ANOVA:").pack(side='left', padx=5)
        self.anova_dep_var = tk.StringVar()
        self.anova_indep_var = tk.StringVar()
        ttk.Combobox(anova_frame, textvariable=self.anova_dep_var, width=15).pack(side='left', padx=2)
        ttk.Combobox(anova_frame, textvariable=self.anova_indep_var, width=15).pack(side='left', padx=2)
        ttk.Button(anova_frame, text="Run ANOVA", command=self.run_anova).pack(side='left', padx=5)
        
        # Chi-square section
        chi_frame = ttk.Frame(test_frame)
        chi_frame.pack(fill='x', pady=2)
        ttk.Label(chi_frame, text="Chi-Square:").pack(side='left', padx=5)
        self.chi_col1_var = tk.StringVar()
        self.chi_col2_var = tk.StringVar()
        ttk.Combobox(chi_frame, textvariable=self.chi_col1_var, width=15).pack(side='left', padx=2)
        ttk.Combobox(chi_frame, textvariable=self.chi_col2_var, width=15).pack(side='left', padx=2)
        ttk.Button(chi_frame, text="Run Chi-Square", command=self.run_chi_square).pack(side='left', padx=5)
        
        # Correlation section
        corr_frame = ttk.Frame(test_frame)
        corr_frame.pack(fill='x', pady=2)
        ttk.Label(corr_frame, text="Correlation:").pack(side='left', padx=5)
        ttk.Button(corr_frame, text="Correlation Matrix", command=self.correlation_matrix).pack(side='left', padx=5)
        
        # Results display
        inf_results_frame = ttk.LabelFrame(self.inf_frame, text="Test Results")
        inf_results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.inf_results_text = tk.Text(inf_results_frame, height=15)
        inf_scrollbar = ttk.Scrollbar(inf_results_frame, orient="vertical", command=self.inf_results_text.yview)
        self.inf_results_text.configure(yscrollcommand=inf_scrollbar.set)
        self.inf_results_text.pack(side="left", fill="both", expand=True)
        inf_scrollbar.pack(side="right", fill="y")
    
    def setup_visualization_tab(self):
        """Setup data visualization tab"""
        self.viz_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.viz_frame, text="Data Visualization")
        
        # Plot selection
        plot_frame = ttk.LabelFrame(self.viz_frame, text="Plot Generation")
        plot_frame.pack(fill='x', padx=5, pady=5)
        
        # Plot type selection
        plot_type_frame = ttk.Frame(plot_frame)
        plot_type_frame.pack(fill='x', pady=2)
        ttk.Label(plot_type_frame, text="Plot Type:").pack(side='left', padx=5)
        self.plot_type_var = tk.StringVar()
        plot_types = ["Histogram", "Box Plot", "Scatter Plot", "Bar Chart", "Time Series", "Heatmap"]
        ttk.Combobox(plot_type_frame, textvariable=self.plot_type_var, values=plot_types, width=15).pack(side='left', padx=5)
        
        # Column selection for plots
        plot_col_frame = ttk.Frame(plot_frame)
        plot_col_frame.pack(fill='x', pady=2)
        ttk.Label(plot_col_frame, text="X Column:").pack(side='left', padx=5)
        self.plot_x_var = tk.StringVar()
        ttk.Combobox(plot_col_frame, textvariable=self.plot_x_var, width=15).pack(side='left', padx=2)
        ttk.Label(plot_col_frame, text="Y Column:").pack(side='left', padx=5)
        self.plot_y_var = tk.StringVar()
        ttk.Combobox(plot_col_frame, textvariable=self.plot_y_var, width=15).pack(side='left', padx=2)
        
        ttk.Button(plot_frame, text="Generate Plot", command=self.generate_plot).pack(pady=5)
        ttk.Button(plot_frame, text="Dashboard", command=self.create_dashboard).pack(pady=5)
        
        # Plot display area
        plot_display_frame = ttk.LabelFrame(self.viz_frame, text="Plot Display")
        plot_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.plot_info_text = tk.Text(plot_display_frame, height=10)
        self.plot_info_text.pack(fill='both', expand=True)
    
    def setup_advanced_tab(self):
        """Setup advanced analytics tab"""
        self.adv_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.adv_frame, text="Advanced Analytics")
        
        # Analysis selection
        analysis_frame = ttk.LabelFrame(self.adv_frame, text="Advanced Analysis")
        analysis_frame.pack(fill='x', padx=5, pady=5)
        
        # Clustering
        cluster_frame = ttk.Frame(analysis_frame)
        cluster_frame.pack(fill='x', pady=2)
        ttk.Label(cluster_frame, text="Clustering:").pack(side='left', padx=5)
        self.n_clusters_var = tk.StringVar(value="3")
        ttk.Entry(cluster_frame, textvariable=self.n_clusters_var, width=5).pack(side='left', padx=2)
        ttk.Button(cluster_frame, text="K-Means Clustering", command=self.perform_clustering).pack(side='left', padx=5)
        
        # PCA
        pca_frame = ttk.Frame(analysis_frame)
        pca_frame.pack(fill='x', pady=2)
        ttk.Label(pca_frame, text="PCA:").pack(side='left', padx=5)
        self.n_components_var = tk.StringVar(value="2")
        ttk.Entry(pca_frame, textvariable=self.n_components_var, width=5).pack(side='left', padx=2)
        ttk.Button(pca_frame, text="Principal Component Analysis", command=self.perform_pca).pack(side='left', padx=5)
        
        # Regression
        reg_frame = ttk.Frame(analysis_frame)
        reg_frame.pack(fill='x', pady=2)
        ttk.Label(reg_frame, text="Regression:").pack(side='left', padx=5)
        self.reg_target_var = tk.StringVar()
        ttk.Combobox(reg_frame, textvariable=self.reg_target_var, width=15).pack(side='left', padx=2)
        ttk.Button(reg_frame, text="Logistic Regression", command=self.perform_logistic_regression).pack(side='left', padx=5)
        
        # Results display
        adv_results_frame = ttk.LabelFrame(self.adv_frame, text="Analysis Results")
        adv_results_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.adv_results_text = tk.Text(adv_results_frame, height=15)
        adv_scrollbar = ttk.Scrollbar(adv_results_frame, orient="vertical", command=self.adv_results_text.yview)
        self.adv_results_text.configure(yscrollcommand=adv_scrollbar.set)
        self.adv_results_text.pack(side="left", fill="both", expand=True)
        adv_scrollbar.pack(side="right", fill="y")
    
    def setup_automation_tab(self):
        """Setup automation and reproducibility tab"""
        self.auto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.auto_frame, text="Automation & Export")
        
        # Script generation
        script_frame = ttk.LabelFrame(self.auto_frame, text="Script Generation")
        script_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(script_frame, text="Generate Analysis Script", command=self.generate_script).pack(side='left', padx=5, pady=5)
        ttk.Button(script_frame, text="Save Current Session", command=self.save_session).pack(side='left', padx=5, pady=5)
        ttk.Button(script_frame, text="Load Session", command=self.load_session).pack(side='left', padx=5, pady=5)
        
        # Export options
        export_frame = ttk.LabelFrame(self.auto_frame, text="Export Results")
        export_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Button(export_frame, text="Export to Excel", command=self.export_to_excel).pack(side='left', padx=5, pady=5)
        ttk.Button(export_frame, text="Export to PDF", command=self.export_to_pdf).pack(side='left', padx=5, pady=5)
        ttk.Button(export_frame, text="Export Data", command=self.export_data).pack(side='left', padx=5, pady=5)
        
        # Script display
        script_display_frame = ttk.LabelFrame(self.auto_frame, text="Generated Script")
        script_display_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.script_text = tk.Text(script_display_frame, height=15)
        script_scrollbar = ttk.Scrollbar(script_display_frame, orient="vertical", command=self.script_text.yview)
        self.script_text.configure(yscrollcommand=script_scrollbar.set)
        self.script_text.pack(side="left", fill="both", expand=True)
        script_scrollbar.pack(side="right", fill="y")
    
    # Data Management Methods
    def import_csv(self):
        """Import CSV file"""
        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.data = pd.read_csv(file_path)
                self.original_data = self.data.copy()
                self.update_data_info()
                self.update_column_lists()
                self.status_var.set(f"CSV imported: {file_path}")
                messagebox.showinfo("Success", "CSV file imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import CSV: {str(e)}")
    
    def import_excel(self):
        """Import Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            try:
                self.data = pd.read_excel(file_path)
                self.original_data = self.data.copy()
                self.update_data_info()
                self.update_column_lists()
                self.status_var.set(f"Excel imported: {file_path}")
                messagebox.showinfo("Success", "Excel file imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import Excel: {str(e)}")
    
    def connect_database(self):
        """Connect to database"""
        # Simple dialog for database connection
        db_window = tk.Toplevel(self.root)
        db_window.title("Database Connection")
        db_window.geometry("400x300")
        
        ttk.Label(db_window, text="Database Type:").pack(pady=5)
        db_type_var = tk.StringVar(value="SQLite")
        ttk.Combobox(db_window, textvariable=db_type_var, values=["SQLite", "PostgreSQL", "MySQL"]).pack(pady=5)
        
        ttk.Label(db_window, text="Connection String or File Path:").pack(pady=5)
        conn_var = tk.StringVar()
        ttk.Entry(db_window, textvariable=conn_var, width=50).pack(pady=5)
        
        ttk.Label(db_window, text="SQL Query:").pack(pady=5)
        query_text = tk.Text(db_window, height=5, width=50)
        query_text.pack(pady=5)
        
        def connect():
            try:
                if db_type_var.get() == "SQLite":
                    conn = sqlite3.connect(conn_var.get())
                    self.data = pd.read_sql_query(query_text.get("1.0", tk.END), conn)
                    conn.close()
                else:
                    engine = create_engine(conn_var.get())
                    self.data = pd.read_sql_query(query_text.get("1.0", tk.END), engine)
                
                self.original_data = self.data.copy()
                self.update_data_info()
                self.update_column_lists()
                self.status_var.set("Database connected successfully")
                messagebox.showinfo("Success", "Database connected and data imported!")
                db_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Database connection failed: {str(e)}")
        
        ttk.Button(db_window, text="Connect", command=connect).pack(pady=10)
    
    def update_data_info(self):
        """Update data information display"""
        if self.data is not None:
            info = f"Dataset Shape: {self.data.shape}\n\n"
            info += "Column Information:\n"
            info += f"{'Column':<20} {'Type':<15} {'Non-Null':<10} {'Missing':<10}\n"
            info += "-" * 65 + "\n"
            
            for col in self.data.columns:
                dtype = str(self.data[col].dtype)
                non_null = self.data[col].count()
                missing = self.data[col].isnull().sum()
                info += f"{col:<20} {dtype:<15} {non_null:<10} {missing:<10}\n"
            
            info += f"\nMemory Usage: {self.data.memory_usage(deep=True).sum() / 1024**2:.2f} MB\n"
            
            # Basic statistics for numeric columns
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                info += "\nNumeric Columns Summary:\n"
                info += self.data[numeric_cols].describe().to_string()
            
            self.data_info_text.delete(1.0, tk.END)
            self.data_info_text.insert(1.0, info)
    
    def update_column_lists(self):
        """Update all column selection comboboxes"""
        if self.data is not None:
            columns = list(self.data.columns)
            numeric_columns = list(self.data.select_dtypes(include=[np.number]).columns)
            categorical_columns = list(self.data.select_dtypes(include=['object', 'category']).columns)
            
            # Update descriptive statistics combo
            self.desc_columns_combo['values'] = columns
            
            # Update inferential statistics combos
            for widget in [self.ttest_col1_var, self.ttest_col2_var, self.anova_dep_var, 
                          self.anova_indep_var, self.chi_col1_var, self.chi_col2_var]:
                if hasattr(self, widget.get().split('_')[0] + '_combo'):
                    getattr(self, widget.get().split('_')[0] + '_combo')['values'] = columns
            
            # Update plot combos
            self.plot_x_var.set('')
            self.plot_y_var.set('')
            
            # Update advanced analytics combos
            self.reg_target_var.set('')
    
    def handle_missing_data(self):
        """Handle missing data in the dataset"""
        if self.data is None:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        
        missing_window = tk.Toplevel(self.root)
        missing_window.title("Handle Missing Data")
        missing_window.geometry("400x300")
        
        ttk.Label(missing_window, text="Missing Data Strategy:").pack(pady=5)
        strategy_var = tk.StringVar(value="Drop rows")
        strategies = ["Drop rows", "Drop columns", "Fill with mean", "Fill with median", "Fill with mode", "Forward fill"]
        ttk.Combobox(missing_window, textvariable=strategy_var, values=strategies).pack(pady=5)
        
        def apply_strategy():
            try:
                if strategy_var.get() == "Drop rows":
                    self.data = self.data.dropna()
                elif strategy_var.get() == "Drop columns":
                    self.data = self.data.dropna(axis=1)
                elif strategy_var.get() == "Fill with mean":
                    numeric_cols = self.data.select_dtypes(include=[np.number]).columns
                    self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].mean())
                elif strategy_var.get() == "Fill with median":
                    numeric_cols = self.data.select_dtypes(include=[np.number]).columns
                    self.data[numeric_cols] = self.data[numeric_cols].fillna(self.data[numeric_cols].median())
                elif strategy_var.get() == "Fill with mode":
                    for col in self.data.columns:
                        self.data[col] = self.data[col].fillna(self.data[col].mode().iloc[0] if not self.data[col].mode().empty else 0)
                elif strategy_var.get() == "Forward fill":
                    self.data = self.data.fillna(method='ffill')
                
                self.update_data_info()
                self.status_var.set(f"Missing data handled: {strategy_var.get()}")
                messagebox.showinfo("Success", "Missing data handled successfully!")
                missing_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to handle missing data: {str(e)}")
        
        ttk.Button(missing_window, text="Apply", command=apply_strategy).pack(pady=10)
    
    def remove_outliers(self):
        """Remove outliers from numeric columns"""
        if self.data is None:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        
        try:
            numeric_cols = self.data.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                self.data = self.data[(self.data[col] >= lower_bound) & (self.data[col] <= upper_bound)]
            
            self.update_data_info()
            self.status_var.set("Outliers removed using IQR method")
            messagebox.showinfo("Success", "Outliers removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove outliers: {str(e)}")
    
    def reset_data(self):
        """Reset data to original state"""
        if self.original_data is not None:
            self.data = self.original_data.copy()
            self.update_data_info()
            self.status_var.set("Data reset to original state")
            messagebox.showinfo("Success", "Data reset successfully!")
    
    # Descriptive Statistics Methods
    def generate_descriptive_stats(self):
        """Generate descriptive statistics for selected column"""
        if self.data is None:
            messagebox.showwarning("Warning", "No data loaded!")
            return
        
        column = self.desc_columns_var.get()
        if not column:
            messagebox.showwarning("Warning", "Please select a column!")
            return
        
        try:
            results = f"Descriptive Statistics for '{column}':\n"
            results += "=" * 50 + "\n\n"
            
            if self.data[column].dtype in ['object', 'category']:
                # Categorical data
                results += f"Data Type: Categorical\n"
                results += f"Unique Values: {self.data[column].nunique()}\n"
                results += f"Missing Values: {self.data[column].isnull().sum()}\n\n"
                results += "Value Counts:\n"
                results += self.data[column].value_counts().to_string()
                results += "\n\nRelative Frequencies:\n"
                results += (self.data[column].value_counts(normalize=True) * 100).round(2).to_string()
            else:
                # Numeric data
                results += f"Data Type: Numeric\n"
                results += f"Count: {self.data[column].count()}\n"
                results += f"Missing Values: {self.data[column].isnull().sum()}\n\n"
                
                desc_stats = self.data[column].describe()
                for stat, value in desc_stats.items():
                    results += f"{stat.title()}: {value:.4f}\n"
                
                # Additional statistics
                results += f"\nAdditional Statistics:\n"
                results += f"Variance: {self.data[column].var():.4f}\n"
                results += f"Skewness: {stats.skew(self.data[column].dropna()):.4f}"

                # Show the result in a textbox or print it (depending on your UI)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, results)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while generating statistics:\n{str(e)}")