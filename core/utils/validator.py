from InquirerPy.validator import EmptyInputValidator
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError


class NumericValidator(Validator):
    def validate(self, document: Document) -> None:
        try:
            float(document.text)
        except ValueError as e:
            raise ValidationError(message="Please enter a valid number.") from e


class IntegerValidator(Validator):
    def validate(self, document: Document) -> None:
        if not document.text.isdigit():
            raise ValidationError(message="Please enter a valid integer.")


TYPE_VALIDATORS = {
    str: EmptyInputValidator(),
    float: NumericValidator(),
    int: IntegerValidator(),
}
