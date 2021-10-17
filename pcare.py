from pymongo import MongoClient
# from pymongo.cursor import CursorType
import numpy as np
import time
import pandas as pd
from pandas import DataFrame
import json
import re
from datetime import date, datetime, timedelta

cluster = MongoClient('mongodb+srv://<username>:<password>@paprika.mxbzv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')
db = cluster["paprika"]
collection_prescription = db["prescription"]
collection_drug = db["drug"]
collection_disease = db['disease']

while True :
    print('='*80)
    s_time = time.time( ) # 시작시간
    user_input = input("원하는 작업을 입력해주세요: \n [A] 'drug.csv' 시스템에 추가, \n [B] 'disease.csv' 시스템에 추가, \n [C] 처방전 추가, \n [D] 사용자 맞춤 서비스, \n [Q] 시스템 종료")
    user_input = user_input.upper()

    if user_input == "A" :
        # 약 정보에 대한 데이터(csv 파일) 시스템에 입력
        # 약 정보에 대한 데이터(csv 파일) 시스템에 입력
        user_input2 = input('입력하실 csv파일의 이름을 입력해주세요.')
        
        if '.csv' in user_input2 :
            pass
        else :
            user_input2 = user_input2+'.csv'
        try :
            insert_df = pd.read_csv(user_input2)
            print('[1] 파일이 존재합니다.')
            original_df = DataFrame(list(collection_drug.find({})))
            orilen = len(original_df)
            if orilen < 1 :
                # 테이블이 비어있으므로 그냥 넣기.
                print('[2] processing...')
                pass
            else :
                df_merge = pd.merge(insert_df, original_df)
                dlen1 = len(df_merge)
                print('[2] 데이터 중복 검사를 하겠습니다.')
                df_merge = df_merge.drop_duplicates(subset=['drug_name'], keep='last')
                df_merge.to_csv('new_drug.csv',index=False, encoding="utf-8-sig")
                print('[3] processing...')
                insert_df = pd.read_csv('new_drug.csv')
            drug_to_json = json.loads(insert_df.to_json(orient='records'))
            collection_disease.insert_many(drug_to_json)
            print('Data inserted')
        except:
            print('파일 이름을 다시 확인해주세요.')
        print('** 초기 화면으로 돌아갑니다.**')

        

    elif user_input == "B" :

        user_input5 = input('입력하실 csv파일의 이름을 입력해주세요.')
        
        if '.csv' in user_input5 :
            pass
        else :
            user_input5 = user_input5+'.csv'
        try :
            insert_df = pd.read_csv(user_input5)
            print('[1] 파일이 존재합니다.')
            original_df = DataFrame(list(collection_disease.find({})))
            orilen = len(original_df)
            if orilen < 1 :
                # 테이블이 비어있으므로 그냥 넣기.
                print('[2] processing...')
                pass
            else :
                df_merge = pd.merge(insert_df, original_df)
                dlen1 = len(df_merge)
                print('[2] 데이터 중복 검사를 하겠습니다.')
                df_merge = df_merge.drop_duplicates(subset=['disease_code'], keep='last')
                df_merge.to_csv('new_disease.csv',index=False, encoding="utf-8-sig")
                print('[3] processing...')
                insert_df = pd.read_csv('new_disease.csv')
            disease_to_json = json.loads(insert_df.to_json(orient='records'))
            # drug_to_json = df_merge.to_json(orient='records')
            collection_disease.insert_many(disease_to_json)
            print('Data inserted')
        except:
            print('파일 이름을 다시 확인해주세요.')
        print('**초기 화면으로 돌아갑니다.**')

    elif user_input == "C" :
        # 처방전 추가
        user_name = input('사용자 성함을 입력해 주세요.') 
        print('[1]',user_name,'님, 안녕하세요.')

        prescription = input('%s 님, 처방전을 입력해 주세요.' % user_name)

        # 발급 날짜 패턴 : 'YYYY년 MM월 DD일.
        try :
            year_info = re.search('\d{4}년',prescription)
            year = year_info.group()[:-1]

            month_info = re.search('\d{1,2}월',prescription)
            month = month_info.group()[:-1]

            day_info = re.search('월\s\d{1,2}일',prescription)
            day = day_info.group()[2:-1]
           
            datetime_string = year+'-'+month+'-'+day

            insert_date = datetime.strptime(datetime_string, '%Y-%m-%d')
            print('[2] insert_date',insert_date,'done.')

            prescription = re.sub(r'\s\d{4}년\s\d{1,2}월\s\d{1,2}일', '', prescription)
            
        except:
            datetime_string = str(date.today())
            print('[2] no date. filled with system date.')

        # 질병 코드 패턴 : 질병분류기호의 다음 문자열로 '.' 이 생략되거나 중간에 의미없는 스페이스가 입력될 수 있음.
        try :
            pres_for_disease = prescription.replace(" ","")
            disease_info = re.search('질병분류기호\w{1,10}\d{1,10}',pres_for_disease)
            disease_code = disease_info.group()[6:]
            
            # 추출 후 테이블에 넣기 전 DB와 같은 형식으로 변환해주기.
            
            cursor = collection_disease.find({})
            disease_df = DataFrame(list(cursor))
            disease_df["disco_new"] = disease_df['disease_code'].str.replace(pat=r'[^\w]', repl=r'', regex=True)
            disco_new = list(disease_df["disco_new"])

            for index, x in enumerate(disco_new) :
                if x != disease_code :
                    pass
                else:
                    new_disease_code = disease_df['disease_code'][index]
                    print('[3] disease_code identified.',new_disease_code)
                    break

        # 질병코드가 없는 경우에 - 넣기.
        except :
            new_disease_code = '-'
            print('[3] no disease identified. filled with',new_disease_code)
        
        # 약 이름 패턴 : '약 이름' 의 다음 문자열이 약 이름. 띄어쓰기가 이어진 후 총 투약일수 + '일'
        # 그러나 처방전 예시를 보면 약 이름의 previous string 이 꼭 '약 이름' 이 아닌것 같음.
        # 규칙에 '약 이름' 이 생략될 수 있다는 설명이 없으므로 앞으로의 처방전에 '약 이름' 이 꼭 포함될 것이라는 전제.

        while True :
            try:
                try: 
                    drug_info = re.search('약\s\이름\s\w{1,20}\s\d{1,3}일',prescription).group()
                    drug_info = drug_info[5:]
                    drug_name = re.sub('\s\d{1,5}일',"",drug_info)
                    dlen = len(drug_name)
                    duration = drug_info[dlen:-1]
                    prescription = re.sub(r'약\s\이름\s\w{1,20}\s\d{1,3}일','약 이름',prescription)
                    
                except:
                    drug_info = re.search('약\s\이름\s\w{1,20}\(\w{1,20}\)\s\d{1,3}일',prescription).group()
                    drug_info = drug_info[5:]
                    drug_name = re.sub('\s\d{1,5}일',"",drug_info)
                    dlen = len(drug_name)
                    duration = drug_info[dlen:-1]
                    prescription = re.sub(r'약\s\이름\s\w{1,20}\(\w{1,20}\)\s\d{1,3}일', '약 이름', prescription)
            except :
                break

            # 추출 완료. db 의 drug 테이블에 저장된 이름과 정확히 일치할 것이므로 변환 작업 스킵.
            print('[4] drug_name and duration identified.',drug_name,':',duration,'일')

            # 약 이름 추출시마다 DB 에 저장하기
            if len(drug_name) < 1 :
                break
            
            pdict = {'insert_date': datetime_string,'user_name':user_name,'disease_code':new_disease_code,'drug_name':drug_name,'duration':duration}
            collection_prescription.insert_one(pdict)

            print('[5] 1 row inserted.')
        
        print('*** 초기 화면으로 돌아갑니다. ***')

    elif user_input == 'D' :
        while True :
            user_name = input('사용자 성함을 입력해 주세요.')
            user_input3 = input('%s 님, 원하는 서비스를 선택해 주세요. \n [A] 나의 질병명과 유용한 정보 알기, \n [B] 나의 오늘 복용할 약의 이름과 투약 횟수 알기, \n [Q] 돌아가기' % user_name)
            user_input3 = user_input3.upper()
            if user_input3 == 'A' :
                # 사용자의 가장 처방 기록 조회
                cursor = collection_prescription.find({"user_name": user_name})
                cursorlist = list(cursor)
                clen = (len(cursorlist))
                c = 0
                Dc = list()
                while c < clen :
                    dc = cursorlist[c]['disease_code']
                    Dc.append(dc)
                    c += 1
                # 중복 제거
                Dc = set(Dc)
                print('chickcheck',Dc)
                Dname = list() # dname 담을 리스트
                Udata = list() # udata 담을 리스트
                for dc in Dc :
                    cursor2 = collection_disease.find({"disease_code": dc})
                    cursorlist = list(cursor2)
                    dname = cursorlist[0]['disease_name']
                    udata = cursorlist[0]['useful_data']
                    Dname.append(dname)
                    Udata.append(udata)
                dinfo_df = DataFrame({'data_name' : Dname, 'useful_data': Udata}, columns=['data_name','useful_data'])
                dlen = len(dinfo_df)
                dno = 0
                print(user_name,'님의 내역이',dlen,'건 있습니다.')
                while dno < dlen :
                    print('[병명]',dinfo_df['data_name'][dno],': [설명]',dinfo_df['useful_data'][dno])
                    dno +=1
                break
                
            elif user_input3 == 'B' :
                # 오늘 먹어야 할 약?
                cursor3 = collection_prescription.find({"user_name": user_name})
                cursorlist2 = list(cursor3)
                drug_df = DataFrame(cursorlist2)
                dlen = len(drug_df)
                dno = 0
                print(user_name,'님의 모든 처방 내역은',dlen,'건 입니다.')

                while dno < dlen :
                    datetime_string = drug_df['insert_date'][dno]
                    duration = drug_df['duration'][dno]
                    drug_name = drug_df['drug_name'][dno]
                    date = datetime.strptime(datetime_string, '%Y-%m-%d')
                    end_date = date + timedelta(int(duration))
                    ispast = (datetime.today() - end_date).days # 남은 투약횟수 (하루에 한번씩만 복용하는 약이라고 가정) 계산 위함.
                    if ispast < 0 :
                        print('[약명]:',drug_name,'[남은 복용 횟수]:',abs(ispast),'회')
                    else :
                        print('[약명]:',drug_name,'은 복용기간이 지났습니다.')
                    dno += 1
                break

            elif user_input3 == 'Q' :
                print('이전 화면으로 돌아갑니다.')
                break
            else :
                print('***올바른 알파벳을 입력해주세요.***')

    elif user_input == "Q" :
        user_input2 = input('시스템을 정말 종료하려면 [Q], 이전 화면으로 돌아가려면 아무 키나 눌러주세요.')
        user_input2 = user_input2.upper()
        if user_input2 == 'Q' :
            e_time = time.time( ) # 종료 시간
            t_time = e_time - s_time #작업 소요 시간
            print("=" *80)
            print("총 사용시간은 %s 초 입니다 " %round(t_time,1))
            print('시스템을 종료합니다.')
            break
        else :
            print('이전 화면으로 돌아갑니다.')

    else :
        print('***올바른 알파벳을 입력해주세요. 초기 화면으로 돌아갑니다.***')