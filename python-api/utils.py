

def get_json_file_content(file_path):
    current_dir = os.path.dirname(__file__)
    with open(f'{current_dir}/{file_path}', 'r') as file:
        return json.load(file)
