_data_store = {}

def store_data(report_id, product_name, scraped_data, analysis_report):
    _data_store[report_id] = {
        "product_name": product_name,
        "scraped_data": scraped_data,
        "analysis": analysis_report
    }

def get_report(report_id):
    return _data_store.get(report_id, {})
