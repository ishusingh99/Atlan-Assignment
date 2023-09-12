import os
import json
import gspread
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import Form, Question, Response
from oauth2client.service_account import ServiceAccountCredentials


@csrf_exempt
def create_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data['title']
        description = data['description']
        questions = data['questions']
        form = Form.objects.create(title=title, description=description)
        for question_text in questions:
            Question.objects.create(form=form, text=question_text)
        return JsonResponse({'message':'Form Created'}, status=200)

    return JsonResponse({'message':'Error'}, status=404)

@csrf_exempt
def get_response(request):
    if request.method =='POST':
        ques_ans = {}
        data = json.loads(request.body)
        responses = data['responses']
        for idx in responses:
            question = Question.objects.get(id = idx)  
            print(question.form)    
            ques_ans[question.text] = responses[idx]
        print(ques_ans)
        ques = list(ques_ans.keys())
        ans = list(ques_ans.values())
        print(ques)
        print(ans)
        dicti = json.dumps(ques_ans)
        response = Response.objects.create(form=question.form, data = dicti)

        current_dir = os.path.dirname(__file__) 
        json_file_path = os.path.join(current_dir, "keys.json")
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_file_path, scope)
        client = gspread.authorize(creds)

        new_sheet = client.create("Your Responses")
        new_sheet.share('ishusingh99@gmail.com', perm_type = 'user', role = 'writer')
        worksheet = new_sheet.get_worksheet(0)
        values_to_insert = [ques, ans]
        worksheet.insert_rows(values_to_insert, 1)

        sheet_url = new_sheet.url

        return JsonResponse({'message':'Your responses have been recieved. You can access the Google Sheet for your responses in the link below', 'Link': sheet_url}, status=200)

    return JsonResponse({'message':'Error'}, status=404)

@csrf_exempt
def send_sms_notification(request):
    if request.method =='POST':
        data = json.loads(request.body)
        form_id = data['form_id']
        phone_number = data['phone_number']

        account_sid = "ACa3212790a66098cd63be597d521ff5d8"
        auth_token = "e01ced4d5ecdce8a59346d377e1bbd1b"
        client = Client(account_sid, auth_token)
        
        form = Form.objects.get(id = form_id)
        print(form)
        print(form.id)
        response = Response.objects.filter(form = form).values()
        response_dict = list(response)
        print(response)
        final_response = {"title": form.title, "description":form.description, "response": response_dict}
        message = client.messages \
                        .create(
                            body=json.dumps(final_response),
                            from_='+15803660855',
                            to = phone_number
                        )

        print(message.sid)
        return JsonResponse({'message':f"SMS has been sent to {phone_number}", 'data': response_dict}, status=200)

    return JsonResponse({'message':'Error'}, status=404)