"""Cheermin views."""
# -----------------------------------------------------------------------------
# Import
# ------
#
# - Python Standard Library
from io import BytesIO

# - Other Libraries or Frameworks
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# - Local application
from .models.athlete import Athlete, photo_height, photo_width

@login_required
def index(request):
    return render(request, 'views/index.html')

@login_required
def athletes(request):
    return render(
        request,
        'views/athletes.html',
        {'athletes': Athlete.objects.all()},
    )

@login_required
def athlete_detail(request, athlete_id):
    return render(
        request,
        'views/athlete_detail.html',
        {'athlete': Athlete.objects.filter(id=athlete_id)[0]},
    )

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
    athletes = Athlete.objects.filter(Q(photo='') | Q(health_insurance_card_photo='') | Q(secondary_id_card=''))

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
