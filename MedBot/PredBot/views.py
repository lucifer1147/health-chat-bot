from django.shortcuts import render, redirect
from .models import Instance, Message
from django.http import HttpResponse, JsonResponse
from .symptomInput import get_feature_input, related_symptoms, get_features
from .modelFunction import pred_with_model
# Create your views here.


def home(request):
    return render(request, 'home.html', {'bot_name': 'PredBot', 'cb_active': "", 'pb_active': 'active'})


def instance(request, instance):
    username = request.GET.get('username')
    instance_details = Instance.objects.get(name=instance)
    return render(request, 'room.html', {
        'username': username,
        'room': instance,
        'room_details': instance_details,
        'base_app': "/PredBot",
        'bot_name': "PredBot",
        'cb_active': "",
        'pb_active': 'active'
    })


def checkview(request):
    instance = request.POST['room_name']
    username = request.POST['username']

    if Instance.objects.filter(name=instance).exists():
        return redirect('/PredBot/'+instance+'/?username='+username)
    else:
        new_instance = Instance.objects.create(name=instance)
        new_instance.save()

        message = f"Hey {username}!\n"+"Please enter the corresponding numbers for the symptoms that apply to you in the following 16 categories as asked (Ex: 1, 2, 5 if they apply to you or just Enter None if nothing applies to you)"

        default_message = Message.objects.create(value=message, user="MedBot", instance=new_instance.id)
        default_message.save()
        return redirect('/PredBot/'+instance+'/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.POST['username']
    instance_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, instance=instance_id)
    new_message.save()

    bot_response, i = get_feature_input(message)

    if i >= len(related_symptoms)+1:
        features = get_features()
        predictions = pred_with_model(features)

        print(features, predictions)

        if len(predictions) == 1:
            bot_response = f"\nYou most likely suffer from {predictions[0]}"
        elif len(predictions) == 2:
            bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[-1]}"
        else:
            bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {', '.join(predictions[1:-1])} or {predictions[-1]}"

        bot_response += "\nThe process will keep repeating, you may leave if your query has been resolved."
    bot_message = Message.objects.create(value=bot_response, user='MedBot', instance=instance_id)
    bot_message.save()

    return HttpResponse("Success!")


def getMessages(request, instance):
    instance_details = Instance.objects.get(name=instance)

    messages = Message.objects.filter(instance=instance_details.id)
    return JsonResponse({"messages": list(messages.values())})
