from django.db import transaction
from django.utils import timezone
from django.db.models import Q
from .models import ChangeSet, PersonGroup, Person, PersonHistory


class PersistencyService:
    """
    Сервис для реализации персистентности для отслеживания состава групп.
    Позволяет просматривать, как группы изменяются со временем с версионированием на основе наборов изменений.
    """
    
    @staticmethod
    def create_changeset(description="", author=None):
        """
        Создать новый набор изменений для отслеживания группы изменений.
        Аналогично Git коммиту.
        """
        changeset = ChangeSet.objects.create(
            reason=description,
            author=author or "System"
        )
        return changeset
    
    @staticmethod
    def get_group_history(group_id, limit=None):
        """
        Получить историю изменений для группы по ID.
        """
        try:
            # Получаем историю изменений для группы
            query = PersonHistory.objects.filter(group_id=group_id).select_related('change').order_by('-valid_from')
            
            if limit:
                query = query[:limit]
                
            history = []
            for record in query:
                history.append({
                    'id': record.id,
                    'timestamp': record.change.authored_at.isoformat() if record.change else record.valid_from.isoformat(),
                    'author': record.change.author if record.change else 'System',
                    'reason': record.change.reason if record.change else 'History record',
                    'person': {
                        'last_name': record.last_name,
                        'first_name': record.first_name,
                        'middle_name': record.middle_name,
                        'full_name': f"{record.last_name} {record.first_name} {record.middle_name or ''}".strip()
                    },
                    'valid_from': record.valid_from.isoformat(),
                    'valid_to': record.valid_to.isoformat()
                })
            
            return history
            
        except Exception as e:
            return []
    
    @staticmethod
    def get_group_at_time(group_id, timestamp):
        """
        Получить состав группы на определенное время.
        """
        try:
            # Находим запись в истории, которая была активна в указанное время
            history_record = PersonHistory.objects.filter(
                group_id=group_id,
                valid_from__lte=timestamp,
                valid_to__gt=timestamp
            ).select_related('change').first()
            
            if history_record:
                return [{
                    'last_name': history_record.last_name,
                    'first_name': history_record.first_name,
                    'middle_name': history_record.middle_name,
                    'birth_date': history_record.birth_date,
                    'gender': history_record.gender,
                    'address': history_record.address,
                    'phone': history_record.phone,
                    'email': history_record.email,
                    'change_info': {
                        'timestamp': history_record.change.authored_at.isoformat() if history_record.change else None,
                        'author': history_record.change.author if history_record.change else None,
                        'reason': history_record.change.reason if history_record.change else None
                    } if history_record.change else None
                }]
            
            return []
            
        except Exception as e:
            return None
    
    @staticmethod
    def get_all_changesets(limit=None):
        """
        Получить все наборы изменений в системе.
        """
        try:
            query = ChangeSet.objects.all().order_by('-authored_at')
            
            if limit:
                query = query[:limit]
                
            changesets = []
            for changeset in query:
                # Подсчитываем количество изменений в этом changeset
                changes_count = Person.objects.filter(change=changeset).count()
                
                changesets.append({
                    'id': changeset.id,
                    'timestamp': changeset.authored_at.isoformat(),
                    'author': changeset.author,
                    'reason': changeset.reason,
                    'description': changeset.reason, 
                    'changes_count': changes_count
                })
            
            return changesets
            
        except Exception as e:
            return []
    
    @staticmethod
    def get_changeset_details(changeset_id):
        """
        Получить детали конкретного набора изменений.
        """
        try:
            changeset = ChangeSet.objects.get(id=changeset_id)
            
            history_records = PersonHistory.objects.filter(change=changeset)
            
            details = {
                'id': changeset.id,
                'timestamp': changeset.authored_at.isoformat(),
                'author': changeset.author,
                'reason': changeset.reason,
                'changes': []
            }
            
            for record in history_records:
                details['changes'].append({
                    'group_id': record.group_id,
                    'person': {
                        'last_name': record.last_name,
                        'first_name': record.first_name,
                        'middle_name': record.middle_name,
                        'full_name': f"{record.last_name} {record.first_name} {record.middle_name or ''}".strip()
                    },
                    'valid_from': record.valid_from.isoformat(),
                    'valid_to': record.valid_to.isoformat()
                })
            
            return details
            
        except ChangeSet.DoesNotExist:
            return None
        except Exception as e:
            return None
