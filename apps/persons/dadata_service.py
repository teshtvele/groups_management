from dadata import Dadata
from django.conf import settings
from typing import List, Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DaDataService:
    """Сервис для работы с API DaData"""
    
    def __init__(self):
        self.token = settings.DADATA_TOKEN
        
        if not self.token:
            raise ValueError("DaData API токен не настроен. Проверьте переменную окружения DADATA_TOKEN")
        
        # Для подсказок адресов используем только токен
        self.dadata = Dadata(self.token)
    
    def suggest_addresses(self, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Получение подсказок адресов по запросу
        
        Args:
            query: Строка запроса для поиска адреса
            count: Количество подсказок (максимум 20)
            
        Returns:
            Список словарей с адресами
        """
        try:
            if not query or len(query.strip()) < 3:
                return []
            
            result = self.dadata.suggest("address", query, count=min(count, 20))
            
            addresses = []
            for item in result:
                address_data = {
                    'value': item['value'],  # Полный адрес
                    'unrestricted_value': item['unrestricted_value'],  # Полный адрес с почтовым индексом
                    'data': {
                        'postal_code': item['data'].get('postal_code'),
                        'country': item['data'].get('country'),
                        'region': item['data'].get('region_with_type'),
                        'city': item['data'].get('city_with_type'),
                        'street': item['data'].get('street_with_type'),
                        'house': item['data'].get('house'),
                        'flat': item['data'].get('flat'),
                        'geo_lat': item['data'].get('geo_lat'),
                        'geo_lon': item['data'].get('geo_lon'),
                        'fias_id': item['data'].get('fias_id'),
                        'fias_level': item['data'].get('fias_level'),
                        'kladr_id': item['data'].get('kladr_id'),
                    }
                }
                addresses.append(address_data)
            
            return addresses
            
        except Exception as e:
            logger.error(f"Ошибка при запросе к DaData API: {e}")
            return []
    
    def clean_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Стандартизация и очистка адреса
        
        Args:
            address: Адрес для очистки
            
        Returns:
            Словарь с очищенным адресом или None
        """
        try:
            if not address or len(address.strip()) < 3:
                return None
            
            result = self.dadata.clean("address", address)
            
            if result:
                return {
                    'source': address,
                    'result': result.get('result'),
                    'postal_code': result.get('postal_code'),
                    'country': result.get('country'),
                    'region': result.get('region_with_type'),
                    'city': result.get('city_with_type'),
                    'street': result.get('street_with_type'),
                    'house': result.get('house'),
                    'flat': result.get('flat'),
                    'geo_lat': result.get('geo_lat'),
                    'geo_lon': result.get('geo_lon'),
                    'fias_id': result.get('fias_id'),
                    'qc': result.get('qc'),  # Код качества
                    'qc_complete': result.get('qc_complete'),  # Код пополноты
                    'qc_house': result.get('qc_house'),  # Код качества дома
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Ошибка при очистке адреса через DaData API: {e}")
            return None
    
    def geolocate_by_address(self, address: str) -> Optional[Dict[str, Any]]:
        """
        Получение координат по адресу
        
        Args:
            address: Адрес для геокодирования
            
        Returns:
            Словарь с координатами или None
        """
        try:
            cleaned = self.clean_address(address)
            if cleaned and cleaned.get('geo_lat') and cleaned.get('geo_lon'):
                return {
                    'address': cleaned.get('result'),
                    'latitude': float(cleaned.get('geo_lat')),
                    'longitude': float(cleaned.get('geo_lon')),
                    'quality': cleaned.get('qc'),
                }
            return None
            
        except Exception as e:
            logger.error(f"Ошибка при геокодировании адреса: {e}")
            return None
    
    def suggest_cities(self, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Получение подсказок городов
        
        Args:
            query: Строка запроса для поиска города
            count: Количество подсказок
            
        Returns:
            Список словарей с городами
        """
        try:
            if not query or len(query.strip()) < 2:
                return []
            
            # Ограничиваем поиск только городами
            result = self.dadata.suggest("address", query, 
                                       count=min(count, 20),
                                       locations=[{"city_type_full": "город"}])
            
            cities = []
            for item in result:
                if item['data'].get('city'):
                    city_data = {
                        'value': item['data'].get('city_with_type', item['data'].get('city')),
                        'region': item['data'].get('region_with_type'),
                        'data': {
                            'city': item['data'].get('city'),
                            'city_with_type': item['data'].get('city_with_type'),
                            'region': item['data'].get('region'),
                            'region_with_type': item['data'].get('region_with_type'),
                            'geo_lat': item['data'].get('geo_lat'),
                            'geo_lon': item['data'].get('geo_lon'),
                        }
                    }
                    cities.append(city_data)
            
            return cities
            
        except Exception as e:
            logger.error(f"Ошибка при запросе городов к DaData API: {e}")
            return []
