import time 
import json
from bs4 import BeautifulSoup
import py_vncorenlp
import requests
import nltk
import re
import html2text
# nltk.download('stopwords')
from nltk.corpus import  stopwords



# You can find the Gemini API key on: https://makersuite.google.com/app/apikey

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent" 

def complete_gemini(prompt, key):
    data = {
        "contents": [{
            "parts": [{"text": 'Hãy paraphrase đoạn văn này'+ prompt}]
        }],
        "generationConfig": {
            "stopSequences": ["Title"],
            "temperature": 1.0,
            "maxOutputTokens": 5000,
            "topP": 0.8,
            "topK": 10
        }
    }
    params = {'key': key}
    headers = {"Content-Type": "application/json"}

    try:
       
        result = requests.post(GEMINI_URL, params=params, json=data, headers=headers)
        result.raise_for_status()  # Raise an exception for bad responses (4xx, 5xx)
        if "content" in result.json()["candidates"][0]:
            return result.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return prompt
    except requests.RequestException as e:
        print(f"Error making Gemini API request: {e}")
        raise

def remove_stopwords(text, language):
    stop_words = set(stopwords.words(language))
    word_tokens = text.split()
    filtered_text = [word for word in word_tokens if word not in stop_words]
    join_filtered = ' '.join(filtered_text)
    return  join_filtered
def remove_urls(text):
    url_pattern = re.compile(r'https?://\S+|www\.\S+')
    return url_pattern.sub(r'', text)
def html_to_markdown(dataRaw):
   

    # Chuyển HTML sang Markdown sử dụng thư viện html2text
    markdown_content = html2text.html2text(dataRaw)

    return markdown_content
def remove_html_tags(input_text):
    input_text_str = str(input_text)
    clean_text = re.sub(r'<.*?>', '', input_text_str)
    return clean_text
def clean_words(word):
    simpleWord = word.lower()
    remove_urls_transform = remove_urls(simpleWord)
    punctuation_pattern = r'[^\w\s]'
    text_cleaned = re.sub(punctuation_pattern, '', remove_urls_transform)
    remove_stopwords_transform = remove_stopwords(text_cleaned,'english')
    return remove_stopwords_transform

def format_text(text):
    # Kiểm tra độ dài của văn bản và thêm dấu xuống dòng mỗi 10 ký tự
    max_line_length = 80
    lines = [text[i:i+max_line_length] for i in range(0, len(text), max_line_length)]
    formatted_text = "\n".join(lines)
    return formatted_text
def check_exist_object(data,course, index):
    if len(course) > 0:
        
        for href in course[index]['href']:
            if data in href['children']:
                return  False
    if len(course) == 0:
        return True
    return True
# vncorenlp_path = "C:/Users/envidi/Documents/Python/Crawl_VietJack/" 
# py_vncorenlp.download_model(save_dir='C:/Users/envidi/Documents/Python/Crawl_VietJack/')
# model = py_vncorenlp.VnCoreNLP(annotators=["wseg", "pos", "ner", "parse"],save_dir=vncorenlp_path)



def crawl_vietJack():
    course = []
    try:  
        arrayDict = []
        links = []
        # html_text = requests.get('https://www.vietjack.com').text
        html_text_first = requests.get('https://www.vietjack.com/').text
        soupFirst = BeautifulSoup(html_text_first, 'lxml')
        title_homepage = soupFirst.find_all('div', class_ = 'panel panel-default')

        # name_links = title_homepage[-1].find_all('ul')[1:]
        name_links = title_homepage[-1].find_all('ul')[1:]
        # name_links = name_links[:1]


        




        for index_name_link, name_link in enumerate(name_links):
            course_dict = {}
            
            # link_a_hrefs = name_link.find_all('li')[:1]
            link_a_hrefs = name_link.find_all('li')
            # result_array = link_a_hrefs[:1] + link_a_hrefs[-1:]
            
            h4 = name_link.find_previous_sibling("h4")
            course_dict['id'] = index_name_link+1
            course_dict['title'] = h4.text
            link_array = []
            for link in link_a_hrefs:
                link_dict_first = {}
                link_dict_first['name'] = link.a.text
                link_dict_first['href_first'] = link.a['href'].replace("./", "https://www.vietjack.com/")
                html_text_second = requests.get(link_dict_first['href_first']).text
                soupSecond = BeautifulSoup(html_text_second, 'lxml')
                sidebar_links = soupSecond.find_all('ul', class_ = 'nav nav-list primary left-menu')
                # sidebar_links = soupSecond.find_all('ul', class_ = 'nav nav-list primary left-menu')[1:2]
                
                
                for index_sidebar_link,sidebar_link in enumerate(sidebar_links) :
                    li_sidebar_links = sidebar_link.find_all('li',lambda x: x != 'heading')
                    for index,li_sidebar_link in enumerate(li_sidebar_links) : 
                    
                        dictionary = {}
                        
                        lesson_content = {}
                        
                        dictionary['id'] =  str(index+1)+str(index_sidebar_link+1)
                        dictionary['name'] = li_sidebar_link.a.text        
                        dictionary['href'] = li_sidebar_link.a['href'].replace("../", "https://www.vietjack.com/")   
                        html_text_third = requests.get(dictionary['href']).text
                        soupThird = BeautifulSoup(html_text_third, 'lxml')  
                        tables = soupThird.find_all('table')
                        arrayTable = []
                        if tables is not None:
                            for table in tables:
                                arrayTable.append(table.text.strip())
                                
                        h1_titled = soupThird.find_all('h1')
                        h1_not_in_nav = [h1 for h1 in h1_titled if not h1.find_parent('nav')]
                        exeption_div = soupThird.find('div',class_="vj-note")
                        ul_list = soupThird.find_all('ul',class_="list")

                        lesson_content['title'] = ''
                        if h1_not_in_nav[0] is not None:
                            lesson_content['title'] =  h1_not_in_nav[0].text.lower().replace("vietjack", "imta")
                        if len(ul_list) > 0:
                            ul_list = ul_list[-1]
                            contents = ul_list.find_all_previous('p')
                            if exeption_div is not None : 
                                contents = exeption_div.find_all_previous('p') 
                            else: 
                                contents = ul_list.find_all_previous('p')   
                        else:
                            contents = []
                        examples = soupThird.find_all('pre')
                        example_array = []
                        lesson_array = []
                        if len(contents) > 0:
                            for content in contents:
                                if not content.find_parents(class_="vj-note"):
                                    if not content.find_parents(class_="footer"):   
                                        clean_word = clean_words(content.text.strip()) 
                                        clean_word = clean_word.replace("vietjack", "imta")
                                        lesson_array.append(clean_word)

                               
                        stringTable = ''     
                        if len(arrayTable) > 0:                            
                            stringTable = complete_gemini(", ".join(arrayTable),"AIzaSyBXQReus4HN2jn2U57b9svjyxK71_Yh0B8") 
                                    
                        completion = ''
                        if len(lesson_array) > 0:
                            completion = complete_gemini(", ".join(lesson_array),"AIzaSyBXQReus4HN2jn2U57b9svjyxK71_Yh0B8")
                        lesson_content['content'] = completion + stringTable
                        

                        stringCode=''
                        for example in examples:
                            converMd = remove_html_tags(example)
                            convertMd = html_to_markdown(converMd)
                            example_array.append(convertMd)
                            stringCode = ", ".join(example_array) 
                        lesson_content['id'] = dictionary['id'] + "1"               
                        lesson_content['content'] = completion + stringTable+stringCode
                        dictionary['lesson'] = lesson_content   
                        if dictionary not in arrayDict:
                            arrayDict.append(dictionary)
                        with open('output.json', 'w', encoding='utf-8') as json_file:
                            json.dump(arrayDict, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
                link_dict_first['children'] = arrayDict
                
                link_array.append(link_dict_first)
            course_dict['href'] = link_array
            course.append(course_dict)
           
        # print(course)
    except Exception as e:
            with open('output_error.json', 'w', encoding='utf-8') as json_file:
                json.dump(course, json_file, ensure_ascii=False, indent=2, separators=(',', ': '))
crawl_vietJack()
# link data đã crawl được : https://drive.google.com/file/d/1kV-w-5_CcVllqW4t1tXjgoAoNeaN8CIj/view?usp=sharing









































































































































































































































































































































































































































































































































# for sidebar_link in sidebar_links:
#     li_sidebar_links = sidebar_link.find_all('li',lambda x: x != 'heading')
#     for li_sidebar_link in li_sidebar_links: 
#         dictionary = {}
#         dictionary['href'] = li_sidebar_link.a['href']
#         dictionary['name'] = li_sidebar_link.a.text        
#         arrayDict.append(dictionary)
#         links.append(li_sidebar_link.a['href'])


# for i in range(len(links)):
#     links[i] = links[i].replace("../", "https://www.vietjack.com/")

# final_data = []

# for index, link in enumerate(links):
#     html_text = requests.get(link).text
#     soup = BeautifulSoup(html_text, 'lxml')

#     h1 = soup.find('h1', class_='title')
#     arrayH2 = []
#     h2_list = soup.find_all('h2')
#     arrayImg = []

#     for img in soup.find_all('img'):
#         arrayImg.append(img['src'].replace('../', 'https://www.vietjack.com/'))

#     for h2 in h2_list:
#         h2_dict = {}
#         next_examples = h2.find_next_siblings("pre", class_='result notranslate')
#         array_examples = []

#         for next_example in next_examples:
#             array_examples.append(next_example.text)

#         next_sibling = h2.find_next_siblings("p")
#         h2_dict['name'] = h2.text

#         if next_sibling:
#             h2_dict['content'] = next_sibling[0].text

#         if array_examples:
#             h2_dict['example'] = array_examples

#         arrayH2.append(h2_dict)

#     current_data = {'href': links[index].replace('../', 'https://www.vietjack.com/'),
#                     'name': arrayDict[index]['name'],
#                     'h1': h1.text if h1 else None,
#                     'image': arrayImg,
#                     'h2': arrayH2}

#     final_data.append(current_data)

# # Chuyển dữ liệu thành JSON và lưu vào file
# with open('output.json', 'w', encoding='utf-8') as json_file:
#     json.dump(final_data, json_file, ensure_ascii=False, indent=2)
    


# arrayDict = []

# for sidebar_link in sidebar_links:
#     li_sidebar_links = sidebar_link.find_all('li', lambda x: x != 'heading')
#     for li_sidebar_link in li_sidebar_links:
#         dictionary = {}
#         dictionary['href'] = li_sidebar_link.a['href']
#         dictionary['name'] = li_sidebar_link.a.text
#         arrayDict.append(dictionary)
#         links.append(li_sidebar_link.a['href'])

# for i in range(len(links)):
#     links[i] = links[i].replace("../", "https://www.vietjack.com/")

# for index, value in enumerate(links):
#     html_text = requests.get(value).text
#     soup = BeautifulSoup(html_text, 'lxml')
#     h1 = soup.find('h1', class_='title')
#     arrayH2 = []
#     h2 = soup.find_all('h2')
#     img = soup.find_all('img')
#     arrayImg = []
#     originalLinks = soup.find_all('ul', class_='list')
#     if originalLinks:
#         popularLinks = originalLinks[-2].find_all('li')
#         popular_links_list = []
#         for popularLink in popularLinks:
#             link_dict = {}
#             link_dict['nameLink'] = popularLink.a.text
#             link_dict['linkHref'] = popularLink.a['href']
#             popular_links_list.append(link_dict)

#     for i in range(len(img)):
#         arrayImg.append(img[i]['src'].replace('../', 'https://www.vietjack.com/'))

#     for i in range(len(h2)):
#         h2Dict = {}
#         if h2[i] is not None:
#             nextExamples = h2[i].find_next_siblings("pre", class_='result notranslate')
#             arrayExamples = []
#             for nextExam in nextExamples:
#                 arrayExamples.append(nextExam.text)
#             nextSibling = h2[i].find_next_siblings("p")
#             h2Dict['name'] = h2[i].text
#             if nextSibling:
#                 h2Dict['content'] = nextSibling[0].text
#             if nextExamples:
#                 h2Dict['example'] = arrayExamples
#         arrayH2.append(h2Dict)

#     page_data = {
#         'href': links[index].replace('../', 'https://www.vietjack.com/'),
#         'h1': h1.text if h1 else None,
#         'image': arrayImg,
#         'h2': arrayH2,
#         'id': index,
#         'popular': popular_links_list if popular_links_list else None
#     }

#     # Thêm dữ liệu của trang vào danh sách
#     arrayDict[index].update(page_data)

# Chuyển danh sách thành JSON và lưu vào file
# with open('output.json', 'w', encoding='utf-8') as json_file:
#     json.dump(arrayDict, json_file, ensure_ascii=False, indent=2)
    

