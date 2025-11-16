from django.contrib import admin

from budget_helper.models import Category, Account, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category information', {
            'fields':['name', 'description', 'type']
        })
    ]
    list_display = ['name', 'type']
    ordering = ['type']

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Account information', {
            'fields': ['username','password']
        }),
        ('Personal information', {
            'fields': ['first_name','last_name','email', 'date_of_birth']
        })
    ]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Transaction information', {
            'fields': ['name', 'description','date','amount','user','category']
        })
    ]
    list_display = ('name', 'category', 'amount', 'date', 'user','balance')
    ordering = ['-date']
