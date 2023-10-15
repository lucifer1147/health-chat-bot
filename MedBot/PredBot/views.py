from django.shortcuts import render, redirect
from .models import Instance, Message
from django.http import HttpResponse, JsonResponse
from .symptomInput import get_feature_input, related_symptoms, get_features, related_symptoms_names
from .modelFunction import pred_with_model, load_model

# Create your views here.

displayLi = list(related_symptoms_names.values())
nameLi = list(related_symptoms_names.values())

feats = list([] for _ in range(len(displayLi)))

def intro(request):
    return redirect('/PredBot/0')


def home(request, step):
    global feats, displayLi, nameLi
    # return render(request, 'home.html', {'bot_name': 'PredBot', 'cb_active': "", 'pb_active': 'active'})

    if step > 0:
        temp_feats = []
        for name in nameLi[step - 1]:
            if request.GET.get(name) == 'on':
                temp_feats.append(name)
        feats[step-1] = temp_feats

        if step <= 16:
            return render(request, 'forms.html', {'nameLi': zip(nameLi[step], displayLi[step]), 'step_next': step + 1, 'step_before': step - 1})
        else:
            feats_temp = []
            for li in feats:
                feats_temp.extend(li)
            feats = feats_temp

            features = get_features(feats)
            model, labelEnc, diseases = load_model('pb_views')
            predictions = pred_with_model(features, model, labelEnc, diseases)

            if len(predictions) == 1:
                bot_response = f"\nYou most likely suffer from {predictions[0]}"
            elif len(predictions) == 2:
                bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[-1]}"
            else:
                bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {', '.join(predictions[1:-1])} or {predictions[-1]}"

            bot_response += "\n<br>If you wish to know more about the disease, You may visit <a href=\"/ChatBot\">ChatBot<a> and resolve any further queries there."
            return render(request, 'result.html', {'content': bot_response, 'pb_active': 'active'})
    else:
        return render(request, 'formhome.html')


def instance(request, instance):
    return render(request, 'forms.html')
    # username = request.GET.get('username')
    # instance_details = Instance.objects.get(name=instance)
    # return render(request, 'room.html', {
    #     'username': username,
    #     'room': instance,
    #     'room_details': instance_details,
    #     'base_app': "/PredBot",
    #     'bot_name': "PredBot",
    #     'cb_active': "",
    #     'pb_active': 'active'
    # })


def checkview(request):
    instance = request.POST['room_name']
    username = request.POST['username']

    global model, labelEnc, diseases
    model, labelEnc, diseases = load_model('pb_views')

    if Instance.objects.filter(name=instance).exists():
        return redirect('/PredBot/' + instance + '/?username=' + username)
    else:
        new_instance = Instance.objects.create(name=instance)
        new_instance.save()

        message = f"Hey {username}!\n" + "Please enter the corresponding numbers for the symptoms that apply to you in the following 16 categories as asked (Ex: 1, 2, 5 if they apply to you or just Enter None if nothing applies to you)"

        default_message = Message.objects.create(value=message, user="MedBot", instance=new_instance.id)
        default_message.save()
        return redirect('/PredBot/' + instance + '/?username=' + username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    instance_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, instance=instance_id)
    new_message.save()

    bot_response, i = get_feature_input(message)

    if i >= len(related_symptoms) + 1:
        features = get_features()
        predictions = pred_with_model(features, model, labelEnc, diseases)

        print(features, predictions)

        if len(predictions) == 1:
            bot_response = f"\nYou most likely suffer from {predictions[0]}"
        elif len(predictions) == 2:
            bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[-1]}"
        else:
            bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {', '.join(predictions[1:-1])} or {predictions[-1]}"

        bot_response += "\n<br>If you wish to know more about the disease, You may visit <a href=\"/ChatBot\">ChatBot<a> and resolve any further queries there.\n<br>The process will keep repeating, you may leave if your query has been resolved."
    bot_message = Message.objects.create(value=bot_response, user='MedBot', instance=instance_id)
    bot_message.save()

    return HttpResponse("Success!")


def getMessages(request, instance):
    instance_details = Instance.objects.get(name=instance)

    messages = Message.objects.filter(instance=instance_details.id)
    return JsonResponse({"messages": list(messages.values())})
