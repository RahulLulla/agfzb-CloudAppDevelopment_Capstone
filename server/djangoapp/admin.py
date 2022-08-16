from django.contrib import admin
from .models import CarMake,CarModel


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'dealer_id','year')
    list_filter = ['year']
    search_fields = ['name', 'dealer_id']
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]    
    list_display = ('id','name','description')
    list_filter = ['name']
    search_fields = ['name', 'description']
# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)