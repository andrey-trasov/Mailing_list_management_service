from django.forms import BooleanField, ModelForm

from mailings.models import Client, Message, Newsletter


class StyleFormMixin:
    """
     Форма для стализации
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = 'form-check-input'
            else:
                fild.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, ModelForm):

   class Meta:
       model = Client
       exclude = ('owner',)


class MessageForm(StyleFormMixin, ModelForm):

   class Meta:
       model = Message
       exclude = ('owner',)



class NewsletterForm(StyleFormMixin, ModelForm):

   class Meta:
       model = Newsletter
       exclude = ('owner',)


# class ClientForm(StyleFormMixin, ClientCreateView):
#
#    class Meta:
#        model = Client
#        exclude = ('owner',)