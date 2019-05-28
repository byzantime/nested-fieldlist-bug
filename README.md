# nested-fieldlist-bug
A minimal reproduction of the WTForms nested FieldList bug

The data model is of a list of proprietors, each of whom have a list of associated addresses of different types (postal, email, dx).

To create this using WTForms, I created three forms in `forms.py`:
* `RecipientsForm`, which has `FieldList(FormField(ProprietorForm))`
* `ProprietorForm`, which also has a `FieldList(FormField(AddressForm))`
* `AddressForm`, which has two input fields and a validation function.

The data is inserted to the form in the `GET` in the usual way:

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

However when the page is displayed the nested FieldList fields (`address_type` and `address`, belonging to `AddressForm`) contain HTML code instead of the expected values.

This can be fixed when rendering the form by using `field.data` instead of `ield()`, but that then causes the validation to fail on the nested form fields.
