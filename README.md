# ACE BOT Server
이름은 아직 가칭입니다.

# Install
### pip install
pip install -r requirements.txt
### 마이그레이션 파일 생성
python manage.py makemigrations
### 마이그레이션 적용
python manage.py migrate
### 실행
python manage.py runserver

# 대화 추가 방법
### 1. conversation 디렉토리에 질문에 해당하는 내용을 작성합니다.
conversation 하위 파일의 이름에 대한 값은 반환 되므로 중복이 불가능합니다.
### 2. api/views.py에 있는 if문과 동일하게 작성해줍니다.
여기서 conversation 하위 파일에 있는 이름 값이 반환되므로 동일하게 작성하도록 합니다.
### 3. answer 디렉토리에는 답변에 해당하는 내용을 작성합니다.
answer 하위 파일들은 각각 여러가지 답변을 작성할 수 있습니다.
한 파일에 작성된 답변은 랜덤적으로 추출되어 답변하게 됩니다. 그러므로 한 파일에 작성된 내용은 같은 의미로서 작성되어야 합니다.
