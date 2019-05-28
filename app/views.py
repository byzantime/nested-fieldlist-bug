from flask import redirect, render_template, request, url_for

from app import app
from .forms import AddressForm
from .forms import RecipientsForm
from .forms import ProprietorForm


class CandidateRecipients():

    def get_proprietors(self):
        """Return a list of proprietors from among candidate recipients."""
        return [
            {'name': 'Paddington Bear', 'addresses': [
                {'address': '32 Windsor gardens, London', 'type': 'postal'},
                {'address': 'foo@bar.com', 'type': 'email'},
                {'address': 'Example DX address', 'type': 'DX'},
            ]},
            {'name': 'Tom', 'addresses': []},
            {'name': 'Dick', 'addresses': []},
            {'name': 'Harry', 'addresses': []},
        ]


@app.route('/', methods=['GET', 'POST'])
def index():
    """Select and save recipients (proprietors & chargees)."""
    form = RecipientsForm()

    # Populate RecipientForm with proprietors.
    if request.method == 'GET':
        # Fetch list of candidate recipients.
        proprietors = list(
            CandidateRecipients().get_proprietors())
        for proprietor in proprietors:
            proprietor_form = ProprietorForm()
            # Set proprietor name in hidden input field.
            proprietor_form.prop_name = proprietor['name']
            # populate and append addresses to proprietor form.
            for address in proprietor['addresses']:
                address_form = AddressForm()
                address_form.address = address['address']
                address_form.address_type = address['type']
                proprietor_form.addresses.append_entry(address_form)
            form.proprietors.append_entry(proprietor_form)

    # Will fire on POST request if form validates.
    if form.validate_on_submit():
        recipients = []
        for proprietor in form.proprietors.data:
            recipients.append({
                'name': proprietor['prop_name'],
                'type': 'proprietor',
            })
        # Send data off to external API.
        # TODO
        return redirect(url_for('task_list'))

    return render_template(
        'index.html',
        form=form,
    )


@app.route('/task_list')
def task_list():
    return 'task_list'
