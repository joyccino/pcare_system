# prescription_system

* 환경 : MacOS Catalina, python 3.8
* DB : pymongo atlas

#1 create and activate a virtual environment: <br>
<img width="453" alt="Screen Shot 2021-10-16 at 12 03 42 PM" src="https://user-images.githubusercontent.com/67300266/137571377-aed3ee82-ef4b-4036-aa25-b0672b385f31.png">

#2 download required libraries from requirements.txt by pip install -r requirements.txt <br>

#3 run program by 'python3 pcare.py' <br>
![Screen Shot 2021-10-17 at 4 14 12 AM](https://user-images.githubusercontent.com/67300266/137599549-a688b580-d5e4-46f6-a59a-0d7afcf9d5c8.png)

#4 press keys to navigate:
- press a or A to insert 'drug.csv' file into current database. (<- 차후에 데이터 중복 확인하는 작업이 필요할것.)
- press b or B to insert 'disease.csv' file into current database. (<- 차후에 데이터 중복 확인하는 작업이 필요할것.)
- press c or C to insert 'prescription string' into current database. 
<br> 규칙 활용한 파싱 작업 추가됨: 질병명은 생략될 수 있거나 '.' 이 생략될 수 있으며 중간에 의미 없이 빈 문자열을 포함 할 수 있음.
<br> 약 정보는 반드시 1개 이상 입력 되어야 하고 Drug 테이블의 drug_name 과 정확히 일치해야 하며,
<br> '약 이름' 다음 문자열로 '총 투약일수 정보가 '일' 문자열과 붙어서 입력됨.
<br> 처방전 발급 날짜는 생략된 경우 '오늘' 로 입력됨.
- press d or D for personalised service:
<br> a or A for '나의 질병명과 유용한 정보 알기'
<br> b or B for ' 나의 오늘 복용할 약의 이름과 투약 횟수 알기'
