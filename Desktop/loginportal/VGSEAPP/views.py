from django.shortcuts import render

# Create your views here.
def Home(request):
    return render(request,'index.html')
def freighter(request):
    return render(request,'freighter.html')
def Register(request):
    return render(request,'Register.html')
import pymysql

def SignUpAction(request):
    full_name=request.POST["full_name"]
    email=request.POST["email"]
    contact_no=request.POST["contact_no"]
    gender=request.POST["gender"]
    username=request.POST["username"]
    password=request.POST["password"]

    con=pymysql.connect(host='localhost',user='root',password='root', database='loginportal', charset='utf8')
    cur=con.cursor()
    i=cur.execute("insert into freighter values('"+full_name+"','"+email+"','"+contact_no+"','"+gender+"','"+username+"','"+password+"')")
    con.commit()
    if i>0:
        context={'data':'Registration successful'}
        return render(request, 'freighter.html',context)
    else:
        context={'data':'registration failed'}
        return render(request, 'Register.html',context)

def LoginAction(request):
    username=request.POST["username"]
    password=request.POST["password"]

    con=pymysql.connect(host='localhost',user='root',password='root',database='loginportal',charset='utf8')
    cur=con.cursor()
    i=cur.execute("select * from freighter where username='"+username+"' and password='"+password+"' ")
    con.commit()
    if i>0:
        context={'data':'login successful'}
        return render(request, 'index.html',context)
    else:
        context={'data':'login failed'}
        return render(request, 'freighter.html',context)
