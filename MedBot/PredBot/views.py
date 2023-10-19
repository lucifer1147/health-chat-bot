from django.shortcuts import render, redirect
from .symptomInput import related_symptoms, get_features, related_symptoms_names, related_symptoms_descriptions
from .modelFunction import pred_with_model, load_model

displayLi = list(related_symptoms_names.values())
nameLi = list(related_symptoms.values())
descriptionLi = list(related_symptoms_descriptions.values())

feats = list([] for _ in range(len(displayLi)))


def intro(request):
    return redirect('/PredBot/0')


def home(request, step):
    global feats, displayLi, nameLi
    next_value = 'Next' if step != 16 else 'Get Results'

    activeLi = list("" for _ in range(16))

    previous_active = ''
    next_active = ''
    if step == 1:
        previous_active = 'disabled'
    if step == 16:
        next_active = 'disabled'

    stepsLi = list(range(1, 17))

    if step == 0:
        feats = list([] for _ in range(len(displayLi)))
        return render(request, 'predbotpages/formhome.html', {'pb_active': 'active'})

    elif step > 0:
        temp_feats = []
        for name in nameLi[step - 1]:
            if request.GET.get(name) == 'on':
                temp_feats.append(name)

        feats[step - 1] = temp_feats

        tli = []
        for li in feats:
            tli.extend(li.copy())

        if step <= 16:
            activeLi[step - 1] = 'active'

            return render(request, 'predbotpages/forms.html',
                          {
                              'nameLi': zip(nameLi[step], displayLi[step], descriptionLi[step]),
                              'step_next': step + 1,
                              'step_before': step - 1,
                              'pb_active': 'active',
                              'next_value': next_value, 'paginationLi': zip(activeLi, stepsLi),
                              'previous': previous_active,
                              'next': next_active,
                              'temp_feats': tli
                          })
        else:
            feats_temp = []
            for li in feats:
                feats_temp.extend(li)

            symptoms_input = []
            for names, displays in zip(nameLi, displayLi):
                for name, display in zip(names, displays):
                    if name in feats_temp:
                        names.index(name)
                        symptoms_input.append(display)

            features = get_features(feats_temp)
            model, labelEnc, diseases = load_model('pb_views')
            predictions = pred_with_model(features, model, labelEnc, diseases)

            if len(predictions) == 1:
                bot_response = f"\nYou most likely suffer from {predictions[0]}"
            elif len(predictions) == 2:
                bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {predictions[-1]}"
            else:
                bot_response = f"\nYou most likely suffer from {predictions[0]} with otherwise a small chance of suffering from {', '.join(predictions[1:-1])} or {predictions[-1]}"

            return render(request, 'predbotpages/result.html',
                          {
                              'content': bot_response,
                              'pb_active': 'active',
                              'symptoms_input': feats_temp
                          })
    else:
        return render(request, 'predbotpages/formhome.html')
