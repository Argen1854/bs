from django.db import models
from user.models import User



class BusinessAccount(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_time = models.CharField(max_length=5)
    end_time = models.CharField(max_length=5)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to="")
    
    def __str__(self):
        return self.title

    @property
    def services(self):
        review = SalonService.objects.filter(businessaccounts = self)
        return [{'id': i.id, 'title': i.title,} for i in review]

    @property
    def rating(self):
        p = 0
        for i in self.salon_reviews.all():
            p += int(i.stars)
        return p/self.salon_reviews.all().count()
        # return SalonReviews.objects.filter(businessaccounts = self).aggregate(Avg('stars'))


    @property
    def reviews(self):
        reviews = SalonReview.objects.filter(businessaccounts = self)
        return [{'id': i.id, 'text': i.text, 'stars': i.stars, 'user_id': i.user.id, 'user_name': i.user.name} for i in reviews]
    
    

STARS = [
        ('1', 1),
        ('2', 2),
        ('3', 3),
        ('4', 4),
        ('5', 5)
    ]
class SalonReview(models.Model):
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, related_name='salon_reviews')
    text = models.TextField()
    stars = models.CharField(max_length=100, choices=STARS, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)


# SERVICE_TITLE =[
#     ('B', 'B'),
#     ('C', 'C')
# ]
SERVICE_TYPE = [
    ('Фиксированная','Фиксированная'),
    ('Динамеческая', 'Динамечиская')
]
class SalonService(models.Model):
    title = models.CharField(max_length=100)
    type = models.CharField(max_length=100, choices=SERVICE_TYPE)
    duration = models.TimeField()
    price = models.IntegerField() 
    price_2 = models.IntegerField(null=True, blank=True)
    # Цена зависит от типа если динамическая то цена от и до а если фиксированная тогда фиксированная
    # Поэтому две цены если фиксированная тогда выводим только 1 а если динамическая тогда 2 от и до 

    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, related_name='salon_services')

    def __str__(self):
        return self.title

class Staff(models.Model):
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to="")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=50)
    service_type = models.CharField(max_length=100)
    work_experience = models.CharField(max_length=100)
    review = models.TextField()

    def __str__(self):
        return self.name

    def workday(self):
        workday = StaffTimetable.objects.all()
        # return

    @property
    def reviews(self):
        reviews = StaffReview.objects.filter(staff = self)
        return [{'id': i.id, 'text': i.text, 'stars': i.stars, 'user_id': i.user.id, 'user_name': i.user.name} for i in reviews]


Monday = 0
Tuesday = 1
Wednesday = 2
Thursday = 3
Friday = 4
Saturday = 5
Sunday = 6
class StaffTimetable(models.Model):
    DAYS_OF_WEEK = (
        (Monday, 'Monday'),
        (Tuesday, 'Tuesday'),
        (Wednesday, 'Wednesday'),
        (Thursday, 'Thursday'),
        (Friday, 'Friday'),
        (Saturday, 'Saturday'),
        (Sunday, 'Sunday')
    )
    DAY_TYPES = (
        ('weekday', 'weekday'),
        ('holiday', 'holiday'),
    )
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    day_week = models.PositiveIntegerField(choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_type = models.CharField(max_length=255,choices=DAY_TYPES)


class Interior(models.Model):
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")

class StaffWork(models.Model):
    salon = models.ForeignKey(BusinessAccount, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="")

class StaffReview(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff_reviews')
    text = models.TextField()

    stars = models.CharField(max_length=100, choices=STARS, null=True)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)