from django import forms


class TitledCheckboxInput(forms.CheckboxInput):
    """
    A checkbox input widget with an optional title.
    """

    def __init__(self, attrs=None, check_test=None, title=None):
        super().__init__(attrs)
        self.title = title
