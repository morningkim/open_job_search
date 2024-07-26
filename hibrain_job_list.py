# %%
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# 크롤링할 웹 페이지 URL
base_url = 'https://www.hibrain.net/recruitment/recruits?listType=ING&page='
base_link = 'https://www.hibrain.net'

# 오늘 날짜
today = datetime.today().strftime('%y.%m.%d')

# 페이지 번호 초기화
page_number = 1
recruitments = []

while True:
    # 현재 페이지 URL
    url = base_url + str(page_number)
    
    # 웹 페이지 요청
    response = requests.get(url)
    
    # 페이지의 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 채용 공고 리스트 추출
    class_names = ['td_title listTypeRecruit PLAT', 'td_title listTypeRecruit BRNZ', 'td_title listTypeRecruit GOLD', 'td_title listTypeRecruit LINE', 'td_title listTypeRecruit SIVR', 'td_title listTypeRecruit']
    page_recruitments = []
    
    for class_name in class_names:
        page_recruitments.extend(soup.find_all('span', class_=class_name))
    
    # 페이지에 더 이상 공고가 없으면 종료
    if not page_recruitments:
        break
    
    # 각 채용 공고의 제목, 링크, 시작일, 마감일 출력
    for recruitment in page_recruitments:
        title = recruitment.find('a').get_text()
        link = base_link + recruitment.find('a')['href']
        date_spans = recruitment.find_all_next('span', class_='number')
        start_date = date_spans[0].get_text().strip()
        deadline = date_spans[1].get_text().strip()
        
        # 마감일이 오늘 이후인 공고만 추가
        if deadline >= today:
            recruitments.append({'title': title, 'link': link, 'start_date': start_date, 'deadline': deadline})
    
    # 다음 페이지로 이동
    page_number += 1

# 결과 출력
# for recruitment in recruitments:
#     print(f'Title: {recruitment["title"]}\nLink: {recruitment["link"]}\nStart Date: {recruitment["start_date"]}\nDeadline: {recruitment["deadline"]}\n')


# 데이터프레임 생성
df = pd.DataFrame(recruitments)

# CSV 파일로 저장
df.to_csv('open_job_list.csv', index=False, encoding='utf-8-sig')

# 제외할 키워드 리스트
exclude_keywords = ["교수","교원", "연구원 모집", "직원 모집", "보건", "의료","의사", "강사", "계약직","석사후", "전문연구원", "학생", "변호사","약사","시간제","약무직","입학사정관","보건소","과장","조교","전문의","보건소장","보조원","연구생","회계사","총장", "약제"]

# 제외할 키워드가 포함된 행의 인덱스 찾기
drop_indices = df[df['title'].apply(lambda x: any(keyword in x for keyword in exclude_keywords))].index

# 해당 인덱스의 행 삭제
df.drop(drop_indices, inplace=True)

print(df)

# 필터링된 데이터프레임을 CSV 파일로 저장
df.to_csv('selected_list.csv', index=False, encoding='utf-8-sig')

# %%
# job list를 한번 다 확인하고 update한 후 새로 추가된 list만 확인하는 코드

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

# 크롤링할 웹 페이지 URL
base_url = 'https://www.hibrain.net/recruitment/recruits?listType=ING&page='
base_link = 'https://www.hibrain.net'

# 오늘 날짜
today = datetime.today().strftime('%y.%m.%d')

# 페이지 번호 초기화
page_number = 1
recruitments = []

# 기존 채용 공고 리스트 읽기
existing_jobs = pd.read_csv('open_job_list.csv')

while True:
    # 현재 페이지 URL
    url = base_url + str(page_number)
    
    # 웹 페이지 요청
    response = requests.get(url)
    
    # 페이지의 HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 채용 공고 리스트 추출
    class_names = ['td_title listTypeRecruit PLAT', 'td_title listTypeRecruit BRNZ', 'td_title listTypeRecruit GOLD', 'td_title listTypeRecruit LINE', 'td_title listTypeRecruit SIVR', 'td_title listTypeRecruit']
    page_recruitments = []
    
    for class_name in class_names:
        page_recruitments.extend(soup.find_all('span', class_=class_name))
    
    # 페이지에 더 이상 공고가 없으면 종료
    if not page_recruitments:
        break
    
    # 각 채용 공고의 제목, 링크, 시작일, 마감일 출력
    for recruitment in page_recruitments:
        title = recruitment.find('a').get_text()
        link = base_link + recruitment.find('a')['href']
        date_spans = recruitment.find_all_next('span', class_='number')
        start_date = date_spans[0].get_text().strip()
        deadline = date_spans[1].get_text().strip()
        
        # 마감일이 오늘 이후인 공고만 추가
        if deadline >= today:
            recruitments.append({'title': title, 'link': link, 'start_date': start_date, 'deadline': deadline})
    
    # 다음 페이지로 이동
    page_number += 1

# DataFrame으로 변환
new_jobs_df = pd.DataFrame(recruitments)

# 기존 채용 공고와 비교하여 새로운 공고만 필터링
new_jobs = new_jobs_df[~new_jobs_df['title'].isin(existing_jobs['title'])]

# 새로운 공고를 새로운 CSV 파일에 저장
new_jobs.to_csv('new_jobs_list.csv', index=False)

# 새로운 공고를 기존 CSV 파일에 추가
updated_jobs = pd.concat([existing_jobs, new_jobs], ignore_index=True)
updated_jobs.to_csv('open_job_list.csv', index=False)


# # 결과 출력
# for index, recruitment in new_jobs.iterrows():
#     print(f'Title: {recruitment["title"]}\nLink: {recruitment["link"]}\nStart Date: {recruitment["start_date"]}\nDeadline: {recruitment["deadline"]}\n')

# %%
