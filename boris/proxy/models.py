from django.db import models
from django.template import Context,Template

from proxy.fields import JSONField
from proxy.views import partner_proxy

class CustomForm(models.Model):
    #a model to stub out the whitelabel api locally
    partner_id = models.IntegerField()
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="partner_logos")
    logo_link = models.URLField(null=True,blank=True)
    powered_by_logo = models.ImageField(upload_to="partner_logos",null=True,blank=True,
                    help_text="if defined, this logo will appear next to RTV's in the bottom of the widget")
    powered_by_logo_link = models.URLField(null=True,blank=True)
    sms_optin_text = models.CharField(max_length=255,null=True,blank=True,
        help_text="If not defined, defaults to: 'Send me txt messages from {{partner_name}}'")
    email_optin_text = models.CharField(max_length=255,null=True,blank=True,
        help_text="If not defined, defaults to: 'Receive Email Updates from {{partner_name}}'")
    show_volunteer_box = models.BooleanField(default=False)
    show_sms_box = models.BooleanField(default=True)

    privacy_policy_link = models.URLField()
    question_1 = models.CharField(max_length=255,null=True,blank=True)
    question_2 = models.CharField(max_length=255,null=True,blank=True)

    facebook_share_text = models.CharField(null=True,blank=True,max_length=255)
    twitter_share_text = models.CharField(null=True,blank=True,max_length=120)

    list_signup_endpoint = models.URLField(null=True,blank=True,
        help_text="url to join partner list, should expect POST")
    list_signup_template = JSONField(null=True,blank=True,
        help_text="dictionary of values to POST to list_signup_endpoint.<br> run through django template with submitted_form context")

    def __unicode__(self):
        return self.name

    def cleaned_list_signup_template(self):
        if not self.list_signup_template:
            return None
        else:
            cleaned_template = self.list_signup_template.replace('\n','')
            cleaned_template = cleaned_template.replace('\r','')
            return cleaned_template

    def clean(self):
        from django.core.exceptions import ValidationError
        
        try:
            eval(self.cleaned_list_signup_template())
        except SyntaxError:
            raise ValidationError('list_signup_template not validating as dictionary')

    def submit(self,context):
        #render list_signup_template to values dictionary
        t = Template(self.cleaned_list_signup_template())
        values = t.render(Context(context))
        values_dict = eval(values)
        return partner_proxy("POST",self.list_signup_endpoint,values_dict)

show_logo_choices = (('t','top'),('b','bottom'),('','hide'))

class CoBrandForm(models.Model):
    toplevel_org = models.ForeignKey(CustomForm)
    partner_id = models.IntegerField()
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to="partner_logos")
    show_logo = models.CharField(null=True,blank=True,max_length=1,choices=show_logo_choices,default='t')
    logo_link = models.URLField(null=True,blank=True)
    show_email_optin = models.BooleanField(default=True)
    default_email_optin = models.BooleanField(default=True)
    privacy_policy_link = models.URLField(default="http://example.com/privacy")
    email_optin_text = models.CharField(max_length=255,null=True,blank=True,
        help_text="If not defined, defaults to: 'Receive Email Updates from {{partner_name}}'")

    question_1 = models.CharField(max_length=255,null=True,blank=True)
    question_1_customhtml = models.TextField(null=True,blank=True,help_text="custom html for the response")
    question_2 = models.CharField(max_length=255,null=True,blank=True)
    question_2_customhtml = models.TextField(null=True,blank=True,help_text="custom html for the response")

    def __unicode__(self):
        return self.name
