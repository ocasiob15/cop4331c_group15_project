from wtforms.widgets import FileInput

class MultipleFileInput(FileInput):

  # safe to assume most uses will be for images. user can overwrite at
  # call-time
  def __init__(self, accept="image/jpg, image/png"):
    super(MultipleFileInput, self).__init__()
    self.accept = accept

  def __call__(self, field, **kwargs):
    kwargs['multiple'] = 'multiple'
    kwargs['accept']   = self.accept
    return super(MultipleFileInput, self).__call__(field, **kwargs)

# tada! that was it. all this to change:
#   <input type=file />
# to
#   <input type=file multiple />
#

# also, wtforms describes a 'filter' type of interface when defining
# form fields (to transform input), but there is no actual docs on
# how this is done. Turns out you can define your own callables, which
# just transform the form input
def field_to_lower (val):
    return val.lower() if type(val) is str else val

def field_to_title (val):
    return val.title() if type(val) is str else val
