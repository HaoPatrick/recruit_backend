API Document
===================

[![build status](https://git.zjuqsc.com/recruit/Recruit-backend-2016/badges/master/build.svg)](https://git.zjuqsc.com/recruit/Recruit-backend-2016/commits/master)
[![coverage report](https://git.zjuqsc.com/recruit/Recruit-backend-2016/badges/master/coverage.svg)](https://git.zjuqsc.com/recruit/Recruit-backend-2016/commits/master)

* A complete new recruitment system, using Python (django actually) as backend server.
* This project was intended to provide easy-to-use **api** for frontend developers
* Not test-driven-developement, but I have provided lots of **essensial test** to ensure the program was bacially functioning.
*  I was intended to use QSC general passport, however, it was not convenient for me to debug when developing during the summer vocation. I'm studying HTTP authentication in the same time, so I implemented the simple **Digest Authentication**.

----------

API Usage
-------------

#### Handle a new post
Receieve a new post is the only method that do not require login token.
```
https://servername.com/api/save
method: POST
data:
'name': 'hao',
'student_id': '315010xxxx',
'gender': '',
'major': 'CS',
'phone_number': '1320802xxxx',
'self_intro': 'Hello World.',
'question_one': 'Hello World.',
'question_two': 'Hello World.',
'inclination_one': '技术研发中心',
'inclination_two': '人力资源部门',
'share_work': 'box token',
'photo': 'box token',
'user_agent': '',
'time_spend': ''

-----
Error 110: You missed a important param.
Error 233: Invalid post.
```

#### User Authentication
Before you send a post or get request, you should first get a token from the server.
```
https://servername.com/api/auth
method: POST
data:
	user_name:username
	pass_word:password
```
If the user name and password is correct, the server will return the token and status.
```
content-type:'application/json'
login:'OK'
response_token:TOKEN
```
The token should be valid for the next 24 hours


设定1:
可以修改报名表，重复提交即可，但是不可以修改部门

设定2:
直接保存所有的报名表，不覆盖已有的


