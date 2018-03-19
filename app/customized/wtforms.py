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
