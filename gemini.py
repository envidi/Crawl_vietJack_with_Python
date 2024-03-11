import requests

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
        return result.json()["candidates"][0]["content"]["parts"][0]["text"]
    except requests.RequestException as e:
        print(f"Error making Gemini API request: {e}")
        raise

# Example usage:
content = ['vì babydog không ghi đè phương thức eat đó phương thức eat của lớp dog được triệu hồi', 'và', 'bạn theo dõi ví dụ sau', 'qui tắc đa hình tại runtime không thể có được bởi thành viên dữ liệu', 'phương thức bị ghi đè không là thành viên dữ liệu vì thế đa hình tại runtime không thể có được bởi thành viên dữ liệu trong ví dụ sau đây cả hai lớp có một thành viên dữ liệu là speedlimit chúng ta truy cập thành viên dữ liệu bởi biến tham chiếu của lớp cha mà tham chiếu tới đối tượng lớp con khi chúng ta truy cập thành viên dữ liệu mà không bị ghi đè thì nó sẽ luôn luôn truy cập thành viên dữ liệu của lớp cha', 'giả sử bank là một lớp cung cấp phương thức để lấy lãi suất nhưng lãi suất lại khác nhau giữa từng ngân hàng ví dụ các ngân hàng vcb agr và ctg có thể cung cấp các lãi suất lần lượt là 8 7 và 9 ví dụ này cũng có trong chương ghi đè phương thức nhưng không có upcasting', 'khi việc gọi phương thức được quyết định bởi jvm chứ không phải compiler vì thế đó là đa hình tại runtime', 'trong ví dụ chúng ta tạo hai lớp bike và splendar lớp splendar kế thừa lớp bike và ghi đè phương thức run của nó chúng ta gọi phương thức run bởi biến tham chiếu của lớp cha khi nó tham chiếu tới đối tượng của lớp con và phương thức lớp con ghi đè phương thức của lớp cha phương thức lớp con được triệu hồi tại runtime', 'khi biến tham chiếu của lớp cha tham chiếu tới đối tượng của lớp con thì đó là upcasting ví dụ', 'trước khi tìm hiểu về đa hình tại runtime chúng ta cùng tìm hiểu về upcasting', 'đa hình tại runtime là một tiến trình mà trong đó một lời gọi tới một phương thức được ghi đè được xử lý tại runtime thay vì tại compile time trong tiến trình này một phương thức được ghi đè được gọi thông qua biến tham chiếu của một lớp cha việc quyết định phương thức được gọi là dựa trên đối tượng nào đang được tham chiếu bởi biến tham chiếu', 'một biến tham chiếu có thể được hướng đến bất kì đối tượng với kiểu khai báo hoặc bất kì kiểu con nào của kiểu khai báo một biến tham chiếu có thể được khai báo như là một class hoặc một interface', 'biến tham chiếu có thể được gán cho những đối tượng khác được cung cấp mà không được khai báo final kiểu của biến tham chiếu sẽ xác định phương thức mà có thể được triệu hồi trên đối tượng', 'điều quan trọng để biết là có cách nào truy cập một đối tượng qua các biến tham chiếu một biến tham chiếu có thể chỉ là một kiểu khi được khai báo kiểu của biến tham chiếu này không thể thay đổi', 'nếu bạn nạp chồng phương thức static trong java thì đó là ví dụ về đa hình tại compile time ở chương này chúng sẽ tập trung vào đa hình tại runtime trong java', 'tính đa hình trong java là một khái niệm mà từ đó chúng ta có thể thực hiện một hành động đơn theo nhiều cách khác nhau tính đa hình được suy ra từ hai từ hy lạp là poly và morphs poly nghĩa là nhiều và morphs nghĩa là hình dạng có hai kiểu đa hình trong java đa hình tại compile time và đa hình runtime chúng ta có thể thực hiện tính đa hình trong java bởi nạp chồng phương thức và ghi đè phương thức'  'trong ví dụ trên kiểu đối tượng không thể được quyết định bởi compiler bởi vì sự thể hiện của dog cũng là một sự thể hiện của animal vì thế compiler không biết kiểu nào của nó chỉ biết đến kiểu cơ sở', 'khi kiểu của đối tượng được quyết định tại runtime thì đó là gắn kết động dynamic binding', 'khi kiểu của đối tượng được quyết định tại compile time bởi compiler thì đó là static binding nếu có bất cứ phương thức private final hoặc static nào trong một lớp thì đó là gắn kết tĩnh đó không thể có chuyện ghi đè overloading kết quả đối với lập trình hướng đối tượng trong static binding', 'ở đây d1 là một sự thể hiện của lớp dog nhưng nó cũng là một sự thể hiện của animal', '3 đối tượng có một kiểu đối tượng là một instance sự thể hiện của lớp java cụ thể nhưng nó cũng là một instance của lớp cha', '2 tham chiếu có một kiểu', 'ở đây biến data là một kiểu int', '1 biến có một kiểu nó có thể là kiểu gốc hoặc kiểu khác không phải là kiểu gốc', 'trước khi đi vào thảo luận về binding chúng ta cần làm rõ type là gì', 'binding gắn kết là kết nối một lời gọi phương thức tới thân phương thức có hai kiểu binding là static binding hay early binding gắn kết tĩnh và dynamic binding hay late biding gắn kết động']
completion = complete_gemini(", ".join(content),"AIzaSyBlMrPQVBVDyJtihrIz31EAxpbGA89ybOM")
print(completion)
