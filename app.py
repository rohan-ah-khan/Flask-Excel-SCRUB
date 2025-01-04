from flask import Flask, render_template, url_for, request, redirect
import pandas as pd

app = Flask(__name__)

df = pd.read_excel('data.xlsx')

columns = ['name', 'image', 'collect']

id_list = df['name'].to_list()
url_list = df['image'].to_list()
collect_list = df['collect'].to_list()



@app.route('/', methods=['GET', 'POST'])
def index():
    rows_per_page = 5  # Rows per page
    page = int(request.args.get('page', 1))  # Get current page from query string, default to 1

    if request.method == 'POST':
        # Get the form data
        item_index = int(request.form['item_index'])

        # Check if 'collect_value' is in the form (checkbox is checked)
        collect_value = 1 if 'collect_value' in request.form else 0

        # Update the DataFrame only if the value changes
        if df.at[item_index, 'collect'] != collect_value:
            df.at[item_index, 'collect'] = collect_value
            df.to_excel('data.xlsx', index=False)  # Save changes to the Excel file

        # Redirect to the same page
        return redirect(f'/?page={page}')

    # Prepare data for pagination
    records = df.to_dict('records')
    start = (page - 1) * rows_per_page * 6
    end = start + rows_per_page * 6
    page_data = records[start:end]

    # Add item_index to each record
    for i, record in enumerate(page_data, start=start):
        record['item_index'] = i

    # Group into rows of 6 items each
    grouped_data = [page_data[i:i + 6] for i in range(0, len(page_data), 6)]

    # Calculate total pages
    total_rows = len(records) // 6
    total_pages = (total_rows + rows_per_page - 1) // rows_per_page

    return render_template(
        'index.html',
        data=grouped_data,
        page=page,
        total_pages=total_pages
    )




    
if __name__ == "__main__":
        app.run(debug=True)
