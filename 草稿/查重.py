def check_duplicates(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    unique_users = set()
    duplicates = set()
    
    for line in lines:
        user_id = line.strip()
        if user_id in unique_users:
            duplicates.add(user_id)
        else:
            unique_users.add(user_id)
    
    if duplicates:
        print("重复的用户数据如下：")
        for user_id in duplicates:
            print(user_id)
    else:
        print("没有重复的用户数据。")

# 调用函数并传入文件路径
check_duplicates("followers_list.txt")
