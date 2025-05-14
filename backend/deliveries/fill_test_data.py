import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import django
import random
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from deliveries.models import (
    TransportModel, PackagingType, DeliveryService, DeliveryStatus, CargoType, Delivery
)

# Создание пользователей
user, _ = User.objects.get_or_create(username='testuser', defaults={'is_staff': True, 'is_superuser': True})
user.set_password('testpass123')
user.save()
ivan, _ = User.objects.get_or_create(username='Иван')
ivan.set_password('12345')
ivan.save()
sergey, _ = User.objects.get_or_create(username='sergey')
sergey.set_password('sergey123')
sergey.save()

# Справочники
transport_models = ['V01', 'X20', 'REX', 'Спринтер', 'Газель', 'Лада Груз', 'ЭлектроМобиль']
packagings = ['Пакет до 1 кг', 'Целофан', 'Коробка', 'Бумажный пакет', 'Пластиковый контейнер', 'Ящик', 'Нет упаковки']
services = ['До клиента', 'Перемещение между складами', 'Физ. лицо', 'Юр. лицо', 'Мед. товары', 'Хрупкий груз', 'Температурный режим']
statuses = ['В ожидании', 'Проведено']
cargos = ['Документы', 'Мед.товары', 'Особые товары', 'Другое']

transport_objs = [TransportModel.objects.get_or_create(name=n)[0] for n in transport_models]
packaging_objs = [PackagingType.objects.get_or_create(name=n)[0] for n in packagings]
service_objs = [DeliveryService.objects.get_or_create(name=n)[0] for n in services]
status_objs = [DeliveryStatus.objects.get_or_create(status=n)[0] for n in statuses]
cargo_objs = [CargoType.objects.get_or_create(name=n)[0] for n in cargos]

# Удаляем старые тестовые доставки
Delivery.objects.all().delete()

# Создаём 20 тестовых доставок
for i in range(20):
    d = Delivery(
        delivery_date=date.today() - timedelta(days=random.randint(0, 14)),
        distance_km=random.uniform(1, 100),
        transport_model=random.choice(transport_objs),
        packaging=random.choice(packaging_objs),
        service=random.choice(service_objs),
        status=random.choice(status_objs),
        cargo_type=random.choice(cargo_objs),
        created_by=user
    )
    d.save()

print('Тестовые данные и пользователи успешно добавлены!') 