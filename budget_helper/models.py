from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


from budget_helper.validators import username_validator, password_validator


class Account(models.Model):

    username = models.CharField(max_length=24,
                                validators=[username_validator],
                                )
    password = models.CharField(max_length=16,
                                validators=[
                                    password_validator,
                                    MinLengthValidator(8, message='Password must be at least  8 characters long'),
                                ])
    email = models.EmailField()
    first_name = models.CharField(max_length=24)
    last_name = models.CharField(max_length=24)
    date_of_birth = models.DateField()
    balance = models.DecimalField(max_digits=10,
                                  decimal_places=2,
                                  default=0)

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'

class Category(models.Model):

    class CategoryChoices(models.TextChoices):
        INC = 'INC', 'Income'
        EXP = 'EXP', 'Expense'

    name = models.CharField(max_length=24)
    type = models.CharField(choices=CategoryChoices.choices)
    description = models.TextField(null=True,
                                   blank=True)

    def __str__(self):
        return f'{self.name} ({self.get_type_display()})'

class Transaction(models.Model):
    name = models.CharField(max_length=24)
    description = models.TextField(null=True,
                                   blank=True)
    amount = models.DecimalField(max_digits=10,
                                 decimal_places=2)
    date = models.DateField(default=timezone.now)
    category = models.ForeignKey('Category',
                                 on_delete=models.CASCADE)
    user = models.ForeignKey('Account',
                             on_delete=models.CASCADE)


    @property
    def balance(self):

        transactions = (
            Transaction.objects
            .order_by('-date', '-id')
        )
        total = 0
        started = False

        for t in transactions:
            if t == self:
                started = True

            if started:
                if t.category.type == 'INC':
                    total += t.amount
                else:
                    total -= t.amount

        return total

    @property
    def type(self):
        return self.category.get_type_display()

    def __str__(self):
        return f'{self.name} - {self.amount} ({self.type})'

