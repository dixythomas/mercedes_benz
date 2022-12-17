from fpdf import FPDF
import requests
import sys
import os
import shutil


class Web_users(object):
    FAIL = 1
    SUCCESS = 0
    user_list = []
    html = {}

    def __init__(self, url=''):
        # This is the constructor
        self.url = url

    def get_url(self):
        # this is a function
        request_site = requests.get(self.url)
        if not request_site.status_code == 200:
            print('The response recieved is not 200,wrong response')
            return False
        self.html = request_site.json()
        return True

    def print_data(self, param=''):
        # print the data
        try:
            self.user_data = self.html[param]
        except KeyError as e:
            print('Raised error', e)
            return False
        counter = 0
        for user_info in self.user_data:
            counter += 1
            self.user_list.append('{} {}'.format(user_info['first_name'], user_info['last_name']))
        print('the number of users are', counter)
        print('The full name of the users are', self.user_list)
        return True

    def create_file(self):
        if os.path.isdir('pdf_document'):
            shutil.rmtree('pdf_document')
        pdf = FPDF()
        try:
            pdf.add_page()
        except RuntimeError as e:
            print('Raised error', e)
            return False
        pdf.set_font("Arial", size=10)
        for user_info in self.user_data:
            request_site = requests.get(user_info['avatar'],stream=True)
            if not request_site.status_code == 200:
                print('The response recieved is not 200,wrong response')
                return False
            end=user_info['avatar'].split('/')
            if os.path.isfile(end[5]):
                os.remove(end[5])
            with open(end[5], 'wb') as out_file:
                shutil.copyfileobj(request_site.raw, out_file)
            pdf.cell(200, 10, txt=user_info['first_name'], ln=1, align='C')
            pdf.cell(200, 10, txt=user_info['email'], ln=1, align='C')
            pdf.image(end[5])
        try:
            os.mkdir('pdf_document')
        except OSError as e:
            print('error creating document folder')
            print(e)
            return False
        pdf.output("pdf_document/newfile.pdf","F")
        return True

    def main(self):
        if not self.get_url():
            print('Getting data from url failed')
            return self.FAIL
        if not self.print_data(param='data'):
            print('printing user info failed')
            return self.FAIL
        if not self.create_file():
            print('creating user file failed')
            return self.FAIL
        return self.SUCCESS


if __name__ == '__main__':  # pragma: no cover
    USER = Web_users('https://reqres.in/api/users')
    sys.exit(USER.main())
