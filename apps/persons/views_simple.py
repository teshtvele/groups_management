from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'persons/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Управление персонами'
        return context


class PersonCreateView(TemplateView):
    """Страница создания персоны"""
    template_name = 'persons/create_person.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить персону'
        # Пока без подключения к базе - просто статичные группы
        context['groups'] = [
            {'id': 1, 'name': 'Группа 1'},
            {'id': 2, 'name': 'Группа 2'},
            {'id': 3, 'name': 'Группа 3'},
        ]
        return context


class PersonListView(TemplateView):
    """Список персон"""
    template_name = 'persons/list_persons.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список персон'
        # Пока без подключения к базе - статичные данные
        context['persons'] = [
            {
                'id': 1,
                'first_name': 'Иван',
                'last_name': 'Иванов',
                'middle_name': 'Иванович',
                'birth_date': '1990-01-01',
                'gender': 'М',
                'address': 'г. Москва, ул. Примерная, д. 1',
                'phone': '+7(123)456-78-90',
                'email': 'ivan@example.com'
            }
        ]
        return context


@require_http_methods(["POST"])
def api_person_create(request):
    """API для создания персоны"""
    try:
        data = json.loads(request.body)
        # Здесь будет логика сохранения в базу
        return JsonResponse({
            'success': True,
            'message': 'Персона создана успешно',
            'person_id': 1,
            'group_id': 1,
            'data': data
        })
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Неверный формат JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


def api_person_list(request):
    """API для получения списка персон"""
    persons = [
        {
            'id': 1,
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'middle_name': 'Иванович',
            'birth_date': '1990-01-01',
            'gender': 'М',
            'address': 'г. Москва, ул. Примерная, д. 1',
            'phone': '+7(123)456-78-90',
            'email': 'ivan@example.com'
        }
    ]
    
    return JsonResponse({
        'success': True,
        'data': persons
    })
