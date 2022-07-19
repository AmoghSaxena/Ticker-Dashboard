from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from colorfield.fields import ColorField

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class ChangePassword(forms.Form):
    oldPassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter Old Password",
                "class": "form-control"
            }
        ))
    newPassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter New Password",
                "class": "form-control"
            }
        ))
    confirmPassword = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirmation New Password",
                "class": "form-control"
            }
        ))


values_logo_position = [
    ('left','left'),
    ('right','right')
]

values_scrolling = [
    ('scrolling', 'Scrolling Ticker'),
    ('media', 'Media Ticker'),
    ('emergency', 'Emergency Ticker'),
]

values_frequency= [
    ('15 minutes', '15 minutes'),
    ('30 minutes', '30 minutes'),
    ('45 minutes', '45 minutes'),
    ('1 hour','1 hour'),
    ('75 minutes','75 minutes'),
    ('90 minutes','90 minutes'),
    ('105 minutes','105 minutes'),
    ('2 hour','2 hour'),
    ('3 hour','3 hour'),
    ('4 hour','4 hour'),
    ('5 hour','5 hour'),
    ('6 hour','6 hour'),
    ('7 hour','7 hour'),
    ('8 hour','8 hour'),
    ('12 hour','12 hour'),
    ('24 hour','24 hour')
]

values_pos_box =[
    ('top-right','top-right'),
    ('top-left','top-left'),
    ('bottom-right','bottom-right'),
    ('bottom-left','bottom-left'),
    ('center','center'),
    ('fullscreen','fullscreen')
]
values_Fonttype= [
                ('TimesNewRoman','TimesNewRoman'),
                ('MyriadProFont','MyriadProFont'),
                ('Ubuntu','Ubuntu'),
                ('Russian','Russian'),
                ('Chinese','Chinese'),
                ('Japanese','Japanese'),
                ('Arabic','Arabic'),
                ('Turkish','Turkish'),
                ('Spanish','Spanish'),
                ('French','French'),
                ('Hindi','Hindi')
]

values_Fontsize= [
                ('x-large','x-large'),
                ('large','large'),
                ('normal','normal'),
                ('small','small')
                ]

values_PositionBox=[
    ('up','up'),
    ('down','down')
]

values_TickerSpeed=[
    ('fast','fast'),
    ('normal','normal'),
    ('slow','slow'),
    ('very-slow','very-slow')
]

values_TickerMotion=[
    ('left','left'),
    ('right','right')
]             

values_location=[
                ('small','small'),
                ('normal','normal'),
                ('large','large')
                ]

values_emergency_ticker_list=[
                ('Earthquake','Earthquake'),
                ('Fire','Fire'),
                ('Active Shooting','Active Shooting'),
                ('General Evacuation','General Evacuation'),
                ('Custom','Custom')
                ]

values_priority=[
                ('High','High'),
                ('Medium','Medium'),
                ('Low','Low')
            ]

values_days=[('Sunday','Sunday'),
            ('Monday','Monday'),
            ('Tuesday','Tuesday'),
            ('Wednesday','Wednesday'),
            ('Thursday','Thursday'),
            ('Friday','Friday'),
            ('Saturday','Saturday')]

class tickerSelecter(forms.Form):
    Select_Ticker = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_scrolling,
    )

    # ############################ Ticker title ###################################

    scrollingTickerTitle = forms.CharField(max_length=20)  
    ############################ primary scroller #####################################  
    primaryScrollingTicker = forms.BooleanField( )
    primaryTickerMessage= forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    primaryFontColor= ColorField(default='#000000') 
    primaryBgColor= ColorField(default='#F15412')
    primaryFontStyle= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_Fonttype,
    )
    primaryFontSize= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_Fontsize,
    )
    primaryPositionBox= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_PositionBox,
    )
    primaryTickerSpeed= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_TickerSpeed,
    )
    primaryTickerMotion= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_TickerMotion,
    )
    # set on primary ticker logo checkbox
    primaryTickerLogoEnabler = forms.BooleanField( )
    # primaryTickerLogo = forms.ImageField(upload_to='images')  
    primaryTickerLogoPosition = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_TickerMotion
    )
    # set on secondary ticker logo checkbox
    secondaryScrollingEnable = forms.BooleanField( )
    secondaryTickerMessage = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))  
    secondaryFontColor = ColorField(default='#000000')
    secondaryBgColor = ColorField(default='#F15412')
    secondaryFontType = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_Fonttype
    )
    secondaryPositionBox = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_PositionBox
    )
    secondaryTickerSpeed = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_TickerSpeed
    )
    secondaryTickerMotion = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_TickerMotion
    )
    scrollingTickerTimeInterval=forms.IntegerField(min_value=1)
    scrollingTickerPriority= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_priority
    )

    ############################ media scroller #####################################  

    mediaTickerTitle = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    # static
    staticTickerEnabler = forms.BooleanField( )
    staticTickerMessage = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    staticFontColor = ColorField(default='#000000')
    staticBgColor = ColorField(default='#F15412')
    staticFontType = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_Fonttype
    )
    staticFontSize = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_Fontsize
    )
    staticPositionBox = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_pos_box
    )
    staticTickerLogoEnabler = forms.BooleanField( )
    # staticTickerLogo = forms.ImageField(upload_to='images')

    # dynamic  
    dynamicTickerEnabler = forms.BooleanField( )
    # dynamicTickerVideo = forms.ImageField(upload_to='images')
    
    dynamicTickerPosition= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_pos_box
    )
    dynamicTickerLocation= forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_location
    )
    mediaTickerTimeInterval= forms.IntegerField(min_value=1)
    mediaTickerPriority = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_priority
    )


    ############################ emergency scroller #####################################
    emergencyTickerTitle = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    emergencySelecter = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_emergency_ticker_list
    )
    # emergencyTickerFile = forms.ImageField(upload_to='images')


######################### Page 3 ############################
CHOICES=[('One-Time','One-Time'),
         ('Recurring','Recurring')]

class schedule(forms.Form):
    wingselection = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    floorselection = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    roomselection = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    scheduleEnabler = forms.BooleanField()
    occurancy = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    startDate=forms.DateTimeField( )
    endDate = forms.DateTimeField( )
    Display_Frequency = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=values_frequency
    )
    days =forms.BooleanField()
    