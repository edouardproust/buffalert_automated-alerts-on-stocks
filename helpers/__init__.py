# If called by CLI
if __name__ == "helpers":
    from . import _email, _number, _stock, _string

# If called by `flask run`
else:
    from . import _form, _session, _stock, _string