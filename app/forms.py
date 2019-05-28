from flask_wtf import FlaskForm
from wtforms import FieldList
from wtforms import FormField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms import Form as NoCsrfForm
from wtforms.widgets import HiddenInput
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError


class AddressForm(NoCsrfForm):
    """The form for an individual recipient address."""
    address_type = StringField(widget=HiddenInput())
    address = TextAreaField(
        'Address',
        validators=[InputRequired(message='Address required')],
    )

    def validate_address(self, field):
        """Validate number of lines and characters in the address."""
        address_lines = field.data.split('\n')
        if len(address_lines) > 6:
            raise ValidationError('Address must contain fewer than 7 lines.')
        if any(line for line in address_lines if len(line) > 45):
            raise ValidationError(
                'Address line must be 45 characters or fewer.')


class ProprietorForm(NoCsrfForm):
    """The form for an individual proprietor."""
    prop_name = StringField()
    addresses = FieldList(FormField(AddressForm))


class RecipientsForm(FlaskForm):
    """Allow users to select proprietors and modify their addresses."""
    proprietors = FieldList(FormField(ProprietorForm))
    submit_button = SubmitField('Save and continue')
