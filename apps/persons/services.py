from django.db import connection, transaction
from django.utils import timezone
from .models import Person, PersonGroup, ChangeSet, PersonHistory
from typing import Optional, List, Dict, Any


class PersonService:
    """Сервис для работы с людьми и дедубликацией"""

    @staticmethod
    def create_change_set(author: str = None, reason: str = None) -> ChangeSet:
        """Создание нового набора изменений"""
        return ChangeSet.objects.create(author=author, reason=reason)

    @staticmethod
    def find_matching_group(person_data: Dict[str, Any]) -> Optional[int]:
        """Поиск подходящей группы для человека"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT find_matching_group(%s, %s, %s, %s, %s, %s, %s)
            """, [
                person_data['last_name'],
                person_data['first_name'],
                person_data.get('middle_name'),
                person_data['gender'],
                person_data['address'],
                person_data.get('phone'),
                person_data.get('email')
            ])
            result = cursor.fetchone()
            return result[0] if result and result[0] else None

    @staticmethod
    @transaction.atomic
    def create_person(person_data: Dict[str, Any], change_set: ChangeSet = None) -> Person:
        """Создание нового человека с дедубликацией"""
        if not change_set:
            change_set = PersonService.create_change_set(
                author='system',
                reason='API person creation'
            )

        # Поиск группы
        group_id = PersonService.find_matching_group(person_data)
        
        if group_id:
            group = PersonGroup.objects.get(id=group_id)
        else:
            group = PersonGroup.objects.create()

        # Создание записи
        person = Person.objects.create(
            group=group,
            change=change_set,
            **person_data
        )

        return person

    @staticmethod
    def search_persons_vitrine(search_params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Поиск в витрине"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM person_vitrine_search(
                    p_last_name := %s,
                    p_first_name := %s, 
                    p_middle_name := %s,
                    p_address := %s,
                    p_phone := %s,
                    p_email := %s,
                    p_limit := %s,
                    p_offset := %s
                )
            """, [
                search_params.get('last_name'),
                search_params.get('first_name'),
                search_params.get('middle_name'),
                search_params.get('address'),
                search_params.get('phone'),
                search_params.get('email'),
                search_params.get('limit', 100),
                search_params.get('offset', 0)
            ])
            
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results

    @staticmethod
    def get_person_as_of(group_id: int, timestamp: timezone.datetime) -> Optional[Dict[str, Any]]:
        """Получение состояния человека на определенный момент времени"""
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM person_as_of(%s, %s)
            """, [group_id, timestamp])
            
            result = cursor.fetchone()
            if result:
                columns = [col[0] for col in cursor.description]
                return dict(zip(columns, result))
            return None

    @staticmethod
    def get_all_current_persons() -> List[Person]:
        """Получение всех текущих записей людей"""
        return Person.objects.filter(is_current=True).select_related('group', 'change')

    @staticmethod
    def get_person_history(group_id: int) -> List[PersonHistory]:
        """Получение истории изменений для группы"""
        return PersonHistory.objects.filter(group_id=group_id).order_by('valid_from')


class DatabaseInitService:
    """Сервис для инициализации базы данных"""

    @staticmethod
    def execute_sql_script(sql_content: str):
        """Выполнение SQL скрипта"""
        with connection.cursor() as cursor:
            # Разбиваем скрипт на отдельные команды
            statements = sql_content.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement and not statement.startswith('--'):
                    try:
                        cursor.execute(statement)
                    except Exception as e:
                        print(f"Error executing statement: {statement[:100]}...")
                        print(f"Error: {e}")
                        raise

    @staticmethod
    def load_sql_script_from_file(file_path: str):
        """Загрузка и выполнение SQL скрипта из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                sql_content = file.read()
                DatabaseInitService.execute_sql_script(sql_content)
                print(f"SQL script from {file_path} executed successfully")
        except Exception as e:
            print(f"Error loading SQL script: {e}")
            raise
