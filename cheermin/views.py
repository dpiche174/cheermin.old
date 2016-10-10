"""Cheermin views."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Python Standard Library
import calendar
import datetime
import logging
from io import BytesIO
from operator import itemgetter

# - Other Libraries or Frameworks
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mass_mail
from django.core.validators import validate_email
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache
from django.views.generic.edit import FormView
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# - Local application
from .models import FeeBase, Fee, MonthlyFeeVariable, Team
from .models.athlete import Athlete, photo_height, photo_width

# Get an instance of a logger
logger = logging.getLogger(__name__)

@login_required
def index(request):
    return render(request, 'views/index.html')

@login_required
def athletes(request):
    return render(
        request,
        'views/athletes.html',
        {'athletes': Athlete.objects.all().order_by('last_name')},
    )

@login_required
def athlete_detail(request, athlete_id):
    query = Q(team__membership__primary=True) & Q(team__membership__athlete__id=athlete_id)
    fees = FeeBase.objects.filter(query).order_by('-amount')

    # Calculate the total.
    total = 0
    for fee in fees:
        total += fee.amount

        # Subtract applicable credits.
        for credit in fee.credit.filter(athlete__id=athlete_id):
            total -= credit.amount

    # Calculate the depot.
    depot = sum(fee.depot or 0 for fee in fees)

    # Compute the terms of payment.
    terms_of_payment = []
    for fee in Fee.objects.filter(query):
        amount = fee.amount - (fee.depot or 0)
        for credit in fee.credit.filter(athlete__id=athlete_id).order_by('-amount'):
            amount -= credit.amount
        terms_of_payment.append(('%s dû le ' % fee.name, fee.due_date, amount))

    # for fee in MonthlyFee.objects.filter(query):
    #     amount = fee.amount - (fee.depot or 0)
    #     for credit in fee.credit.filter(athlete__id=athlete_id).order_by('-amount'):
    #         amount -= credit.amount

    #     for month, payment in enumerate(divide(amount, fee.monthly_payment)):
    #         terms_of_payment.append((
    #             'Versement pour %s dû le ' % fee.name.lower(),
    #             add_months(fee.start_date, month),
    #             payment,
    #         ))

    for fee in MonthlyFeeVariable.objects.filter(query):
        amount = fee.amount - (fee.depot or 0)
        for credit in fee.credit.filter(athlete__id=athlete_id).order_by('-amount'):
            amount -= credit.amount

        for payment in range(fee.number_of_payments):
            terms_of_payment.append((
                'Versement pour %s dû le ' % fee.name.lower(),
                add_months(fee.start_date, payment),
                round_to_05(amount / fee.number_of_payments),
            ))

    terms_of_payment = sorted(terms_of_payment, key=itemgetter(1))

    return render(
        request,
        'views/athlete_detail.html',
        {
            'athlete': Athlete.objects.get(id=athlete_id),
            'fees': fees,
            'total': total,
            'depot': depot,
            'terms_of_payment': terms_of_payment
        },
    )

def round_to(n, precision):
    correction = 0.5 if n >= 0 else -0.5
    return int(n / precision + correction) * precision

def round_to_05(n):
    return round_to(n, 0.05)

def divide(number, divider):
    for _ in range(int(float(number) / float(divider))):
        yield divider
    remain = number % divider
    if remain:
        yield remain

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = int(sourcedate.year + month / 12)
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return datetime.date(year, month, day)

@login_required
def athlete_print(request, athlete_id):
    """Create a PDF version of the requested athlete file."""
    # Get the athlete information.
    athlete = Athlete.objects.filter(id=athlete_id)[0]

    pdf_filename = '{}, {}.pdf'.format(athlete.last_name, athlete.first_name)

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(pdf_filename)

    # Create the PDF object, using the BytesIO object as its "file."
    with BytesIO() as buffer:
        _create_pdf(buffer, athlete)

        # Get the value of the BytesIO buffer and write it to the response.
        response.write(buffer.getvalue())

    return response

def _create_pdf(buffer, athlete):
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter

    # Move the origin up and to the left.
    pdf.translate(inch / 1.2, height - inch)

    # Draw some lines.
    # pdf.line(0, 0, 0, 1.7 * inch)
    # pdf.line(0, 0, 1 * inch, 0)

    # Change color.
    # pdf.setFillColorRGB(0, 0, 0.77)

    pos_x, pos_y = 0, 0

    pdf.setFont("Helvetica", 14)
    pdf.drawString(pos_x, pos_y, ugettext("Athlete Personal Information"))
    pos_y -= 24

    pdf.setFont("Helvetica", 10)
    pdf.drawString(pos_x, pos_y, '{}:'.format(ugettext('Name')))
    pdf.drawString(pos_x + (2 * inch), pos_y, str(athlete))

    # Add photo.
    pdf.drawInlineImage(
        athlete.photo.path,
        width - ((photo_width / 1.5) + inch * 1.5),
        pos_y - (photo_height / 1.5) + 8,
        width=photo_width / 1.5,
        height=photo_height / 1.5
    )
    pos_y -= 16

    pdf.drawString(pos_x, pos_y, '{}:'.format(ugettext('Address')))
    pdf.drawString(pos_x + (2 * inch), pos_y, athlete.street)
    pos_y -= 16
    pdf.drawString(pos_x + (2 * inch), pos_y, '{}, {}'.format(athlete.city, athlete.province))
    pos_y -= 16
    pdf.drawString(pos_x + (2 * inch), pos_y, athlete.country)
    pos_y -= 16
    pdf.drawString(pos_x + (2 * inch), pos_y, athlete.postal_code)
    pos_y -= 16

    pdf.drawString(pos_x, pos_y, '{}:'.format(ugettext('Age on September 1st')))
    pdf.drawString(pos_x + (2 * inch), pos_y, str(athlete.birthday))
    pos_y -= 16

    pdf.drawString(pos_x, pos_y, '{}:'.format(ugettext('Phone number')))
    pdf.drawString(pos_x + (2 * inch), pos_y, athlete.phone_number)
    pos_y -= 16

    pdf.drawString(pos_x, pos_y, '{}:'.format(ugettext('Email address')))
    pdf.drawString(pos_x + (2 * inch), pos_y, athlete.email)
    pos_y -= 16


#     <div class="row">
#       <div class="col-sm-12">
#         <h3>Fiche de santé</h3>
#       </div>
#     </div>
#     <div class="row">
#       <div class="col-sm-8">
#         <div class="row">
#           <div class="col-sm-4"><strong>Numéro d'assurance maladie:</strong></div>
#           <div class="col-sm-8">{{ athlete.health_insurance_number }}</div>
#         </div>
#         <div class="row">
#           <div class="col-sm-4"><strong>Date d'expiration:</strong></div>
#           <div class="col-sm-8">{{ athlete.health_insurance_expiration_date }}</div>
#         </div>
#         <div class="row">
#           <div class="col-sm-4"><strong>Problèmes de santé:</strong></div>
#           <div class="col-sm-8">{{ athlete.health_problems }}</div>
#         </div>
#         <div class="row">
#           <div class="col-sm-4"><strong>Allergies:</strong></div>
#           <div class="col-sm-8">{{ athlete.allergies }}</div>
#         </div>
#       </div>
#       <div class="col-sm-4"></div>
#     </div>
#   </div>
# {% endblock %}

    # Close the PDF object cleanly.
    pdf.save()

@login_required
@never_cache
def photos(request):
    """Show list of athletes that are missing a photo."""
    athletes = Athlete.objects.exclude(active=False).filter(Q(photo='') | Q(health_insurance_card_photo='') | Q(secondary_id_card='')).order_by('first_name')

    if request.method == 'POST':
        for input_name, photo in request.FILES.items():
            field, athlete_id = input_name.rsplit('_', 1)
            athlete = Athlete.objects.filter(pk=athlete_id)[0]

            if field == 'photo':
                if athlete.photo:
                    error_message = ugettext("Athlete '%(athlete_id)s' already has a picture" % {'athlete_id': athlete_id})
                    return HttpResponseBadRequest('<html><body>%s</body></html>' % error_message)
                athlete.photo = photo
                athlete.save()
            elif field == 'health_insurance_card_photo':
                if athlete.health_insurance_card_photo:
                    error_message = ugettext("Athlete '%(athlete_id)s' already has a health insurance card photo" % {'athlete_id': athlete_id})
                    return HttpResponseBadRequest('<html><body>%s</body></html>' % error_message)
                athlete.health_insurance_card_photo = photo
                athlete.save()
            elif field == 'secondary_id_card':
                if athlete.secondary_id_card:
                    error_message = ugettext("Athlete '%(athlete_id)s' already has a secondary ID card photo" % {'athlete_id': athlete_id})
                    return HttpResponseBadRequest('<html><body>%s</body></html>' % error_message)
                athlete.secondary_id_card = photo
                athlete.save()
            else:
                return HttpResponseBadRequest('<html><body>Unexpected field received: %s</body></html>' % field)

    return render(
        request,
        'views/photos.html',
        {'athletes': athletes},
    )

# -----------------------------------------------------------------------------
# notifications.py
# ----------------
#
class UserMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return '{} {}'.format(obj.first_name, obj.last_name)

class MultipleEmailField(forms.CharField):
    """Text input field letting the user enter multiple email addresses separated be a comma."""
    def clean(self, value):
        email_addresses = []
        value = super(MultipleEmailField, self).clean(value)
        if value:
            for email in value.split(','):
                email = email.strip()
                validate_email(email)
                email_addresses.append(email)
        return email_addresses

class NotificationsForm(forms.Form):
    sent_to_all = forms.BooleanField(
        label=ugettext('Sent to all'),
        required=False,
        widget=forms.CheckboxInput(attrs={
            'onchange': 'recipients_changed(this.checked);',
        }),
    )
    teams = forms.ModelMultipleChoiceField(
        queryset=Team.objects.all().order_by('name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.exclude(active=False).exclude(email__isnull=True).exclude(email='').order_by('first_name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    coaches = UserMultipleChoiceField(
        queryset=User.objects.exclude(email__isnull=True).exclude(email='').order_by('first_name'),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
    )
    additional_emails = MultipleEmailField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
    )
    subject = forms.CharField(
        required=True,
        error_messages={'required': ugettext('Please enter a subject.')},
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ugettext('Subject'),
        }),
    )
    message = forms.CharField(
        required=False,
        initial='\n\nSpirit Cheer 07\ninfo@cheer07.com\nwww.cheer07.com',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': ugettext('Message'),
        }),
    )

    def send_email(self):
        """Send email to selected athletes."""
        email_addresses = set(self.cleaned_data['additional_emails'])
        if self.cleaned_data['sent_to_all']:
            for athlete in Athlete.objects.exclude(active=False).exclude(email__isnull=True).exclude(email=''):
                email_addresses.update(athlete.email_addresses)
            for coach in User.objects.exclude(email__isnull=True).exclude(email=''):
                email_addresses.add(coach.email)
        else:
            for athlete in self.cleaned_data['athletes']:
                email_addresses.update(athlete.email_addresses)
            for team in self.cleaned_data['teams']:
                for athlete in team.athletes.exclude(active=False).exclude(email__isnull=True).exclude(email=''):
                    email_addresses.update(athlete.email_addresses)
            for coach in self.cleaned_data['coaches']:
                email_addresses.add(coach.email)

        if not email_addresses:
            raise Exception('No email selected')

        email_addresses.add('Spirit Cheer 07 <info@cheer07.com>')

        for email in email_addresses:
            logger.info('Sending email to {}'.format(email))

        send_mass_mail((self.cleaned_data['subject'], self.cleaned_data['message'], 'Spirit Cheer 07 <info@cheer07.com>', (email,)) for email in email_addresses)

class NotificationsView(LoginRequiredMixin, FormView):

    template_name = 'views/notifications.html'
    form_class = NotificationsForm
    success_url = '/notifications/sent/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.send_email()
        return super(NotificationsView, self).form_valid(form)

@login_required
def notification_sent(request):
    return render(request, 'views/notification_sent.html')
