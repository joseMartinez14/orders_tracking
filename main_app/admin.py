from django.contrib import admin

from .models import User
from .models import Company
from .models import Mapping_Usuario_Empresa
from .models import Company_Process
from .models import Company_Process_step_template
from .models import Company_Order
from .models import Process_Step_Client
from .models import Session

# Register your models here.

admin.site.register(User)
admin.site.register(Company)
admin.site.register(Mapping_Usuario_Empresa)
admin.site.register(Company_Process)
admin.site.register(Company_Process_step_template)
admin.site.register(Company_Order)
admin.site.register(Process_Step_Client)
admin.site.register(Session)


