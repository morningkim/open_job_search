
# %%
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


# 크롤링할 웹 페이지 URL
base_url = 'https://www.hibrain.net/recruitment/recruits?listType=ING&page='

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
    
    # 각 채용 공고의 제목, 링크, 마감일 출력
    for recruitment in page_recruitments:
        title = recruitment.find('a').get_text()
        link = recruitment.find('a')['href']
        deadline = recruitment.find_next('span', class_='number').get_text()
        
        # 마감일이 오늘 이후인 공고만 추가
        if deadline >= today:
            recruitments.append({'title': title, 'link': link, 'deadline': deadline})
    
    # 다음 페이지로 이동
    page_number += 1

# 데이터프레임 생성
df = pd.DataFrame(recruitments)

# CSV 파일로 저장
df.to_csv('open_job_list.csv', index=False, encoding='utf-8-sig')

# %%
# 특정 직위 제외한 리스트 출력
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv("open_job_list.csv")

# 제외할 키워드 리스트
exclude_keywords = ["교수","교원", "연구원 모집", "직원 모집", "의사", "강사"]

# 제외할 키워드가 포함된 행의 인덱스 찾기
drop_indices = df[df['title'].apply(lambda x: any(keyword in x for keyword in exclude_keywords))].index

# 해당 인덱스의 행 삭제
df.drop(drop_indices, inplace=True)

print(df)

# 필터링된 데이터프레임을 CSV 파일로 저장
df.to_csv('selected_list.csv', index=False, encoding='utf-8-sig')
