from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from service.models import UserProfile, MechanicService


class Command(BaseCommand):
    help = 'Create demo data: 2 mechanics, 2 users and services'

    def handle(self, *args, **options):
        # Mechanics
        if not User.objects.filter(username='mech1').exists():
            u1 = User.objects.create_user('mech1', password='password123', first_name='Mike', last_name='One')
            p1 = UserProfile.objects.create(user=u1, is_mechanic=True, city='Springfield', phone='1234567890', latitude=40.0, longitude=-75.0)
            MechanicService.objects.create(mechanic=p1, service_name='Oil Change', price=25.00, description='Quick oil change')
            MechanicService.objects.create(mechanic=p1, service_name='Brake Repair', price=120.00, description='Brake pad replacement')
            self.stdout.write('Created mechanic mech1')
        else:
            self.stdout.write('mech1 exists')

        if not User.objects.filter(username='mech2').exists():
            u2 = User.objects.create_user('mech2', password='password123', first_name='Sara', last_name='Two')
            p2 = UserProfile.objects.create(user=u2, is_mechanic=True, city='Shelbyville', phone='0987654321', latitude=41.0, longitude=-74.0)
            MechanicService.objects.create(mechanic=p2, service_name='Tire Change', price=40.00, description='Tire mount and balance')
            MechanicService.objects.create(mechanic=p2, service_name='Battery Replacement', price=90.00, description='New battery installation')
            self.stdout.write('Created mechanic mech2')
        else:
            self.stdout.write('mech2 exists')

        # Additional mechanics
        if not User.objects.filter(username='mech3').exists():
            u3 = User.objects.create_user('mech3', password='password123', first_name='Alan', last_name='Three')
            p3 = UserProfile.objects.create(user=u3, is_mechanic=True, city='Capital City', phone='2223334444', latitude=39.5, longitude=-76.0)
            MechanicService.objects.create(mechanic=p3, service_name='Engine Tune-up', price=150.00, description='Full engine tune-up')
            MechanicService.objects.create(mechanic=p3, service_name='AC Recharge', price=60.00, description='AC refrigerant top-up')
            self.stdout.write('Created mechanic mech3')
        else:
            self.stdout.write('mech3 exists')

        if not User.objects.filter(username='mech4').exists():
            u4 = User.objects.create_user('mech4', password='password123', first_name='Linda', last_name='Four')
            p4 = UserProfile.objects.create(user=u4, is_mechanic=True, city='Ogdenville', phone='7778889999', latitude=38.9, longitude=-77.1)
            MechanicService.objects.create(mechanic=p4, service_name='Transmission Repair', price=500.00, description='Transmission diagnostics and repair')
            MechanicService.objects.create(mechanic=p4, service_name='Wheel Alignment', price=70.00, description='4-wheel alignment')
            self.stdout.write('Created mechanic mech4')
        else:
            self.stdout.write('mech4 exists')

        # Users
        if not User.objects.filter(username='user1').exists():
            uu1 = User.objects.create_user('user1', password='password123', first_name='User', last_name='One')
            UserProfile.objects.create(user=uu1, is_mechanic=False, city='Springfield', phone='1112223333')
            self.stdout.write('Created user user1')
        else:
            self.stdout.write('user1 exists')

        if not User.objects.filter(username='user2').exists():
            uu2 = User.objects.create_user('user2', password='password123', first_name='User', last_name='Two')
            UserProfile.objects.create(user=uu2, is_mechanic=False, city='Shelbyville', phone='4445556666')
            self.stdout.write('Created user user2')
        else:
            self.stdout.write('user2 exists')

        self.stdout.write(self.style.SUCCESS('Demo data created.'))
