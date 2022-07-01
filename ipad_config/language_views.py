# Django Imports
from django.shortcuts import render, redirect, reverse

# Project Imports
from .models import DVLanguageCode, DVLanguage
from .middlewares import permission_required
from .forms import DVLanguageCodeForm, DVLanguageForm
from .utils import paginate


@permission_required("ipad_config.change_dvlanguagecode")
def dv_language_code_edit(request, language_code_id=None):
    form = DVLanguageCodeForm()
    language_code = None
    if language_code_id:
        language_code = DVLanguageCode.objects.get(pk=language_code_id)
        form = DVLanguageCodeForm(instance=language_code)
    is_add_action_failed = False
    if request.POST:
        if language_code_id:
            form = DVLanguageCodeForm(request.POST, instance=language_code)
        else:
            is_add_action_failed = True
            form = DVLanguageCodeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('import_language_seed', kwargs={}))
        else:
            items = DVLanguage.objects.all()
            code_items = DVLanguageCode.objects.all()
            items = paginate(request, items, 20)
            template = 'pages/upload_language.html' if is_add_action_failed else 'pages/dv_langauge_code_form.html'
            return render(request, template, {
                'items': items,
                'code_items': code_items,
                'form': form,
                'language_code': language_code,
                'is_code_add_action_failed': is_add_action_failed
            })

    return render(request, 'pages/dv_language_code_form.html',
                  {
                      'language_code_form': form,
                      'language_code': language_code
                  }
                  )


@permission_required("ipad_config.delete_dvlanguagecode")
def dv_language_code_delete(request, language_code_id):
    language = DVLanguageCode.objects.get(pk=language_code_id)
    language.delete()

    return redirect(reverse('import_language_seed', kwargs={}))


@permission_required("ipad_config.change_dvlanguage")
def dv_language_edit(request, language_id=None):
    form = DVLanguageForm()
    dvlanguage = None
    if language_id:
        dvlanguage = DVLanguage.objects.get(pk=language_id)
        form = DVLanguageForm(instance=dvlanguage)
    is_add_action_failed = False
    if request.POST:
        if language_id:
            form = DVLanguageForm(request.POST, instance=dvlanguage)
        else:
            is_add_action_failed = True
            form = DVLanguageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('import_language_seed', kwargs={}))
        else:
            items = DVLanguage.objects.all()
            code_items = DVLanguageCode.objects.all()
            items = paginate(request, items, 20)
            template = 'pages/upload_language.html' if is_add_action_failed else 'pages/dv_langauge_form.html'
            return render(request, template, {
                'items': items,
                'code_items': code_items,
                'form': form,
                'dvlanguage': dvlanguage,
                'is_code_add_action_failed': is_add_action_failed
            })

    return render(request, 'pages/dv_language_form.html',
                  {
                      'language_form': form,
                      'dvlanguage': dvlanguage
                  }
                  )


@permission_required("ipad_config.delete_dvlanguage")
def dv_language_delete(request, language_id):
    """

    @param language_id:
    @type request: object
    """
    language = DVLanguage.objects.get(pk=language_id)
    language.delete()
    return redirect(reverse('import_language_seed', kwargs={}))
