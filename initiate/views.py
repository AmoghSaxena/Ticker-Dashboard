from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
# -----------------------new added-----------------------
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from initiate.gadget import datagetter


#  ---------------------------------------------------------------------------
# @login_required
def index(request):
    return render(request, 'index.html')


# @login_required
def createticker(request):

    data = {
            'pos_box':[
                'top-right',
                'top-left',
                'bottom-right',
                'bottom-left',
                'center',
                'fullscreen'
                ],
            
            'font_style':[
                'TimesNewRoman',
                'MyriadProFont',
                'Ubuntu',
                'Russian',
                'Chinese',
                'Japanese',
                'Arabic',
                'Turkish',
                'Spanish',
                'French',
                'Hindi'
                ],

            'font_size':[
                'X-Large',
                'Large',
                'Normal',
                'Small'
                ],

            'position':[
                'up',
                'down'
                ],

            'logo_position':[
                'left',
                'right'
                ],

            'speed':[
                'fast',
                'normal',
                'slow',
                'very-slow'
                ],
            
            'motion':[
                'left',
                'right'
                ],

            'location':[
                'small',
                'normal',
                'large'
                ],
                
            'emergency_ticker_list':[
                'Earthquake',
                'Fire',
                'Active Shooting',
                'General Evacuation',
                'Custom'
            ]
        }
    
    if request.method == 'POST':
        print("static_upload",request.POST.get('static_upload'))
        if (request.POST.get('static_ticker_enabler')=='' or request.POST.get('primary_ticker_enabler')=='' or 
           request.POST.get('secondary_ticker_enabler')=='' or request.POST.get('animation_ticker_enabler')=='' or 
           request.POST.get('emergency_ticker_enabler')==''):
            return render(request, 'preview.html',datagetter(request))
        else:
            return render(request, 'createticker.html', data)
    else:
        return render(request, 'createticker.html', data)

#@login_required
def active(request):
    return render(request, 'active.html') 

#@login_required
def pending(request):
    return render(request, 'pending.html')   

#@login_required
def history(request):
    return render(request, 'history.html') 

#@login_required
def preview(request):
    return render(request, 'preview.html') 

#@login_required
def schedule(request):
    return render(request, 'schedule.html')  

def login(request):
    return render(request, 'login.html')

def registerfor(request):
	return render(request, 'register.html')


class RegisterView(SuccessMessageMixin, CreateView):
	model = User
	fields = ['username', 'password', 'email']
	template_name = 'register.html'
	success_url = reverse_lazy('registerform')
	success_message = "Account was created successfull"

	def form_valid(self, form):
		form.instance.password = make_password(form.instance.password)
		return super().form_valid(form)


from django.utils.deprecation import MiddlewareMixin
from django.urls import resolve, reverse
from django.http import HttpResponseRedirect
from Ticker import settings

class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings by setting a tuple of routes to ignore
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), """
        The Login Required middleware needs to be after AuthenticationMiddleware.
        Also make sure to include the template context_processor:
        'django.contrib.auth.context_processors.auth'."""

        if not request.user.is_authenticated:
            current_route_name = resolve(request.path_info).url_name

            if not current_route_name in settings.AUTH_EXEMPT_ROUTES:
                return HttpResponseRedirect(reverse(settings.AUTH_LOGIN_ROUTE))



