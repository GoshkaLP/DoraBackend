from flask_wtf import FlaskForm

from werkzeug.datastructures import FileStorage

from wtforms import StringField, Field, FileField, FloatField
from wtforms.validators import InputRequired, Optional, StopValidation, ValidationError


# Проверка валидность формы
def is_form_valid(form):
    return form.validate_on_submit()


# Проверка строки на то является ли она числом или нет
def is_digit(n):
    try:
        int(n)
        return True
    except Exception:
        return False


# Класс затычка для запроса об изменении талона
class DefaultFormValue:
    pass


# Класс массива для формы
class ListField(Field):
    def process_formdata(self, valuelist):
        self.data = valuelist


# Класс булевой пермеменной для формы
class CustomBooleanField(Field):
    def process_formdata(self, valuelist):
        if not valuelist:
            self.data = self.default
        elif valuelist[0] in {False, 'false', 0, '0'}:
            self.data = False
        elif valuelist[0] in {True, 'true', 1, '1'}:
            self.data = True


# Класс целого числа для формы
class CustomIntegerField(Field):
    def process_formdata(self, valuelist):
        if not valuelist:
            self.data = self.default
        elif not is_digit(valuelist[0]):
            self.data = self.default
        else:
            self.data = int(valuelist[0])


# Классы проверки файлов
def is_file_empty(stream):
    first_byte = stream.read(1)
    stream.seek(0)
    if not first_byte:
        return True
    return False


class FilesRequired(object):
    def __call__(self, form, field):
        if not field.data \
                or not all(isinstance(file, FileStorage) and is_file_empty(file) is False for file in field.data):
            raise ValidationError


class FilesOptional(object):
    def __call__(self, form, field):
        if not field.data:
            raise StopValidation
        elif not all(isinstance(file, FileStorage) and is_file_empty(file) is False for file in field.data):
            raise ValidationError


class RegisterAuthEmailForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = StringField('oldPassword', validators=[InputRequired()])
    new_password = StringField('newPassword', validators=[InputRequired()])


class CreateManufacturer(FlaskForm):
    name = StringField('name', validators=[InputRequired()])


class CreateProductType(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    warranty_period = CustomIntegerField('warrantyPeriod', validators=[InputRequired()])


class CreateModel(FlaskForm):
    model_name = StringField('modelName', validators=[InputRequired()])
    product_type_id = CustomIntegerField('productTypeId', validators=[InputRequired()])
    photo = FileField('photo', validators=[InputRequired()])


class CreateUnit(FlaskForm):
    model_id = CustomIntegerField('modelId', validators=[InputRequired()])
    serial_number = StringField('serialNumber', validators=[InputRequired()])


class AddCustomerUnit(FlaskForm):
    qr = StringField('qr', validators=[InputRequired()])


class CreateServiceCenter(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    latitude = FloatField('latitude', validators=[InputRequired()])
    longitude = FloatField('longitude', validators=[InputRequired()])
    address = StringField('address', validators=[InputRequired()])


class CreateWarrantyClaim(FlaskForm):
    unit_id = CustomIntegerField('unitId', validators=[InputRequired()])
    service_center_id = CustomIntegerField('serviceCenterId', validators=[InputRequired()])
    problem = StringField('problem', validators=[InputRequired()])


class ChangeWarrantyClaim(FlaskForm):
    claim_id = CustomIntegerField('claimId', validators=[InputRequired()])
    status = StringField('status', validators=[InputRequired()])
