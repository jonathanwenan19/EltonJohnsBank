from asyncio.windows_events import NULL
from hashlib import blake2b
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import profileregisterform, transactionforms, picupdateform, userupdateform, nodefluxphotoform
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile, payments, profilepic, photos
#import mysql.connector
from django.contrib.auth.decorators import login_required
import requests
from requests.structures import CaseInsensitiveDict
import base64
from django.core.files.storage import FileSystemStorage
from django.conf import settings
 
# Create your views here.

def homepage(request):
    return render(request,'home.html')


def login(request):
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
                user = account_user.user_objects.get(username=username,password=password)
                if user is not None:               
                    return render(request, 'home.html', {})
                else:
                    print("Someone tried to login and failed.")
                    print("They used username: {} and password: {}".format(username,password))
     
                    return redirect('/')
        except Exception as identifier:
                
                return redirect('/')
     
    else:
            return render(request, 'base.html')
            '''
   # conn = mysql.connector.connect(host = "localhost", user = "",passwd = "",database = "wads_project")
    return render(request,'login.html')
     

def camerainput(request):
    return HttpResponse("<h1>Input Camera</h1>")

def signup(request):
   if request.method == 'POST': 
        form1 = UserCreationForm(request.POST)
        form2 = profileregisterform(request.POST)
        form3 = picupdateform()
        if form1.is_valid() and form2.is_valid():
            username = form1.cleaned_data.get('username')
            messages.success(request, f'Successfully created an account for {username}')
            new_user = form1.save()
            newdata = form2.save(commit=False)
            newpic =form3.save(commit= False)
            if newdata.user_id is NULL or newdata.user_id is None:
                newdata.user =   new_user
            if newpic.user_id is NULL or newdata.user_id is None:
                newdata.user = new_user
            newdata.save()
            p = profilepic(user = form1.save())
            p.save()
            return redirect("bank-login")
   else:
        form1 = UserCreationForm()
        form2 = profileregisterform()
   context= {'userdata': form1,
                'bankdata':form2 }
   return render(request, 'signin.html',context)

def transaction(request):
    if request.method == 'POST':
        payforms = transactionforms(request.POST)
        confirm_pin = request.POST.get('pin')
        if payforms.is_valid():
            
           # if request.user.is_authenticated():
                sender_profile = request.user.profile
                sender_balance = request.user.profile.balance
                sender_pin = request.user.profile.pin
                input_pin = request.POST.get('pin')
                print(input_pin)

                # if sender id matches the input
                if input_pin != sender_pin : 
                    messages.error(request,"Pleasae input the correct PIN")
                    redirect('bank-transactions')
                elif payforms.cleaned_data.get('amount') > sender_balance:
                    messages.error(request,"Your balance is not enough!")
                    redirect('bank-transaction')
                else:
                    balance = payforms.cleaned_data.get('amount')
                    receiver_no = payforms.cleaned_data.get('receiver_no')
                    
                    
                    print(receiver_no)
                    receiver_profile = profile.objects.filter(card_no = receiver_no).first()
                    if receiver_profile is None:
                        messages.error(request, "Wrong Sender's ID")
                        redirect('bank-transactions')
                        print(receiver_profile)
                    else:
                        receiver_amount = receiver_profile.balance
                        new_amount_receiver = receiver_amount + balance
                        new_amount_sender = sender_balance - balance
                        receiver_profile.balance = new_amount_receiver
                        sender_profile.balance = new_amount_sender
                        sender_profile.save()
                        receiver_profile.save()
                        new_transaction = payforms.save(commit = False)
                        # for initialising sender id 
                        if new_transaction.sender_id is NULL or new_transaction.sender_id is None:
                            new_transaction.sender =   request.user 
                        new_transaction.save()
                        return redirect('bank-home')
                   
    else:
        payforms = transactionforms()
    
    return render(request,'transaction.html',{'forms':payforms} )

def logout(request):
    return render(request, 'logout.html')

#@login_required
def profiles(request):
    if request.method == 'POST':
        user_form = userupdateform(request.POST,instance = request.user)
        pic_form = picupdateform(request.POST, request.FILES, instance = request.user.profilepic)
        if pic_form.is_valid() and user_form.is_valid():
             
            newprofilepic = pic_form.save(commit = False)
            if newprofilepic.user_id is NULL or newprofilepic.user_id is None:
                newprofilepic.user = request.user
            newprofilepic.save()
            messages.success(request, "Your profile picture has been updated!")
            return redirect("bank-home")
    else:
        user_form = userupdateform()
        pic_form = picupdateform()
    data = {
        'user_form':user_form,
        'pic_form':pic_form
    }
    return render(request, 'profile.html', data)

def history(request):
    if request.user.is_authenticated:
        giver_id = request.user.id
        giver_transactions = payments.objects.filter(sender_id = giver_id)
        context ={
         'trans': giver_transactions   
        #'Payment_id': giver_transactions.payment_id,
        #'Receiver_no': giver_transactions.receiver_no,
        #'amount_tranfer': giver_transactions.amount,
        #'notes_given': giver_transactions.notes

        }
        return render(request,'history.html',context)
    else:
        return render(request,'history.html')

#def profiles(request):
    
 #   return render(request, 'profile.html')


def nodeflux(request):
    if request.method == "POST":
        payforms = transactionforms(request.POST)
        nodeflux_pho = nodefluxphotoform(request.POST, request.FILES)
        if nodeflux_pho.is_valid() and payforms.is_valid():
            nodeflux_pho.save()
            new_transaction = payforms.save(commit = False)
                # for initialising sender id 
            if new_transaction.sender_id is NULL or new_transaction.sender_id is None:
                new_transaction.sender =   request.user 
                new_transaction.save()
            user_photo = request.user.profilepic.image.path
            with open(user_photo, "rb") as img_file:
                b64_string = base64.b64encode(img_file.read()).decode('UTF-8')
            
            photo = nodeflux_pho.cleaned_data.get('image')
            photo_url = "nodeflux_photos/" + str(photo)
            print(photo)
            get_photo = photos.objects.filter(image = photo_url).first().image.path
            print(get_photo)
            with open(get_photo, "rb") as img_file:
                b64_string2 = base64.b64encode(img_file.read()).decode('UTF-8')
            

            
            # first post req for authentication
            url = "https://backend.cloud.nodeflux.io/auth/signatures"
            headers = CaseInsensitiveDict()
            headers["Accept"] = "application/json"
            headers["Content-Type"] = "application/json"

            data = """
                {
            "access_key": "D2T9B8LF1SN3W5XT941E0KBPD",
            "secret_key": "l-sF4ZytDRO5tfCO0iEhKFzF5M9aERBNFYfg0A_CIOIMKgFAPUNSOqSHzpBVuFOL"
                }
                """

            resp = requests.post(url, headers=headers, data=data)

            # second post req for double image comparison
            access_key = "D2T9B8LF1SN3W5XT941E0KBPD"
            date = resp.json()['headers']['x-nodeflux-timestamp'][0:8]
            token = resp.json()['token']
            timestamp = resp.json()['headers']['x-nodeflux-timestamp']



            url1 = "https://api.cloud.nodeflux.io/v1/analytics/face-match"
            headers1 = CaseInsensitiveDict()
            headers1["Content-Type"] = "application/json"
            headers1["Authorization"] = "NODEFLUX-HMAC-SHA256 Credential="+access_key+"/"+date+"/nodeflux.api.v1beta1.ImageAnalytic/StreamImageAnalytic,SignedHeaders=x-nodeflux-timestamp, Signature=" + token
            headers1["x-nodeflux-timestamp"] = timestamp
            data1 =  '{"images":["data:image/jpeg;base64,'+str(b64_string)+ '" ,"data:image/jpeg;base64,' +str(b64_string2)+'" ]}'
            resp1 = requests.post(url1, headers=headers1, data=data1)
            job_id = resp1.json()['job']['id']


            #3rd get submission token by using post function
            url2 = "https://backend.cloud.nodeflux.io/auth/v2/submission_tokens"
            headers2 = CaseInsensitiveDict()
            headers2['Authorization'] = "NODEFLUX-HMAC-SHA256 Credential="+access_key+"/"+date+"/nodeflux.api.v1beta1.ImageAnalytic/StreamImageAnalytic,SignedHeaders=x-nodeflux-timestamp, Signature=" + token
            headers2['x-nodeflux-timestamp'] = timestamp
            req_getsubmissiontoken = requests.post(url = url2, headers = headers2)

            submission_token = req_getsubmissiontoken.json()['submission_token']


            # 4th using get method to get the request body

            url3 = "https://api.cloud.nodeflux.io/v1/jobs/" + job_id
            headers3 = CaseInsensitiveDict()
            #headers2["Content-Type"] = "application/json"
            headers3["Authorization"] = submission_token
            #headers2["x-nodeflux-timestamp"] = timestamp

            r = requests.get(url = url3 , headers = headers3)
            print(r.json)
            if r.json()['job']['result']['result'][0]['face_match']['similarity'] >= 0.9:
              
                    sender_profile = request.user.profile
                    sender_balance = request.user.profile.balance
                    balance = payforms.cleaned_data.get('amount')
                    receiver_no = payforms.cleaned_data.get('receiver_no')
                    receiver_profile = profile.objects.filter(card_no = receiver_no).first()
                    if receiver_profile is None:
                        messages.error(request, "Wrong Sender's ID")
                        redirect('bank-nodeflux')
                        print(receiver_profile)
                    else:
                        receiver_amount = receiver_profile.balance
                        if payforms.cleaned_data.get('amount') > sender_balance:
                            messages.error(request,"Your balance is not enough!")
                            redirect('bank-nodeflux')
                        elif r.status_code == 400 or r.status_code == 401:
                            messages.error(request, "Please give a better picture.")
                    
                        else:
                            new_amount_receiver = receiver_amount + balance
                            new_amount_sender = sender_balance - balance
                            receiver_profile.balance = new_amount_receiver
                            sender_profile.balance = new_amount_sender
                            sender_profile.save()
                            receiver_profile.save()
                            new_transaction = payforms.save(commit = False)
                            # for initialising sender id 
                            if new_transaction.sender_id is NULL or new_transaction.sender_id is None:
                                new_transaction.sender =   request.user 
                            new_transaction.save()
                            messages.success(request,"The faces are similar")
                            return redirect('bank-home')
                
              
            else:
                messages.error(request,"The faces are different")
                return redirect('bank-nodeflux')
            

    else:
            payforms = transactionforms()
            nodeflux_pho = nodefluxphotoform()
   
    return render(request, "nodeflux.html",{"nodeflux_form":nodeflux_pho,"payforms":payforms})