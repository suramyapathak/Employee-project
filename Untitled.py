from flask import Flask, request

app = Flask(__name__)

@app.route('/')

def index():
    import pandas as pd
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    import yagmail

    class employees:
        def __init__(self):
            self.sheet = None
            self.credentials = None
            self.scope = None
            self.gc = None
            self.data_all_sheet = None
            self.data_all = None
            self.data_new_sheet = None

        def read_data_from_sheets(self):
            self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

            self.credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scopes=self.scope)

            self.gc = gspread.authorize(self.credentials)
            self.sheet = self.gc.open_by_url(
                'https://docs.google.com/spreadsheets/d/1fD3tmLqW9FjoX65cx0xmzkXejAIPwp6lOTR66sKcUhI/edit?pli=1#gid=0')

            self.data_new_sheet = self.sheet.get_worksheet(0)
            data_new = pd.DataFrame(self.data_new_sheet.get_all_records())
            self.data_all_sheet = self.sheet.get_worksheet(1)
            self.data_all = pd.DataFrame(self.data_all_sheet.get_all_records())

            return data_new, self.data_all

        def create_username(self, name, existing_userID):
            username = f'{name.split()[0].lower()}.{name.split()[-1].lower()}'
            if username in existing_userID.to_list():
                i = 1
                while username + str(i) in existing_userID.to_list():
                    i += 1
                username += str(i)
            return username

        '''def send_welcome_email(self, email, name, resources_link):
            yag = yagmail.SMTP('senderemail, "password")
            with open('email.txt', 'r') as f:
                email_body = f.read('email.txt').replace('[name]', name).replace('[resources_link]', resources_link)
            yag.send('suramya.tset@gmail.com', 'Welcome to the Team!', email_body)  # using my email for testing purpose
        '''
        def append_data_to_sheet(self, row):
            self.data_all_sheet.append_row(row)

        def clear_worksheet(self):
            row = ["Name", "Email ID", "Department"]
            self.data_new_sheet.clear()
            self.data_new_sheet.append_row(row)


    # Main function
    def main():
        employee = employees()
        data_new, data_all = employee.read_data_from_sheets()

        userID = data_all['userID']

        resources_link = 'https://docs.gspread.org'
        for i, row in data_new.iterrows():
            items = []
            name = row['Name']
            email = row['Email ID']
            department = row['Department']
            username = employee.create_username(name, userID)
            items = [name, email, department, username]
            employee.append_data_to_sheet(items)
            #send_welcome_email(email, name, resources_link)
        employee.clear_worksheet()
        print("pass")

    return 'Code executed successfully!'






if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)