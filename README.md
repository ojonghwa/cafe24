cafe24, Django4 설치

git clone https://github.com/ojonghwa/cafe24.git

python 3.11
cafe24/python -m venv venv

.\venv\Scripts\activate

pip install Django==4.2.*
pip install braintree
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install social-auth-app-django
pip install django-cors-headers 
sudo apt install default-libmysqlclient-dev build-essential   #리눅스에서
pip install mysqlclient
pip install numpy
pip install pandas
pip install weasyprint	        #추가작업 필요할 수 있음 
sudo apt install fonts-nanum    #리눅스에서 한글 글꼴 

settings.py 복사하기 
myshop.sqlite3 복사하기 


#admin 계정생성
python manage.py createsuperuser 
- Username, Email, Password 입력

#슈퍼유저 비밀번호 초기화, changepassword 명령어로 비밀번호 초기화
#python manage.py changepassword <유저이름>

python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000    #외부접속 허용하기 위함

sudo apt-get update
sudo apt-get upgrade

sudo apt-get install sqlite3
sqlite3 myshop.sqlite3
