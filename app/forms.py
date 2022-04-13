from flask_wtf import FlaskForm

from werkzeug.datastructures import FileStorage

from wtforms import StringField, DateField, MultipleFileField, Field
from wtforms.validators import InputRequired, Optional, StopValidation, ValidationError


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


class ResetPasswordForm(FlaskForm):
    email = StringField('email', validators=[InputRequired()])
    password = StringField('password', validators=[InputRequired()])
    code = CustomIntegerField('code', validators=[InputRequired()])


class LogoutForm(FlaskForm):
    user_id = CustomIntegerField('user_id', validators=[InputRequired()])


class ChangePasswordForm(FlaskForm):
    user_id = CustomIntegerField('user_id', validators=[InputRequired()])
    old_password = StringField('old_password', validators=[InputRequired()])
    new_password = StringField('new_password', validators=[InputRequired()])


class VerifyEmailForm(FlaskForm):
    user_id = CustomIntegerField('user_id', validators=[InputRequired()])
    code = CustomIntegerField('code', validators=[InputRequired()])


class WarrantyPostForm(FlaskForm):
    user_id = CustomIntegerField('user_id', validators=[InputRequired()])
    name = StringField('name', validators=[InputRequired()])
    shop_name = StringField('shop_name', validators=[InputRequired()])
    category_id = CustomIntegerField('category_id', validators=[InputRequired()])
    date_of_purchase = DateField('date_of_purchase', validators=[InputRequired()])
    type_warranty_period = StringField('type_warranty_period', validators=[InputRequired()])
    warranty_period = CustomIntegerField('warranty_period', validators=[InputRequired()])
    files = MultipleFileField('files', validators=[FilesRequired()])


class WarrantyPatchForm(FlaskForm):
    user_id = CustomIntegerField('user_id', validators=[InputRequired()])
    warranty_id = CustomIntegerField('warranty_id', validators=[InputRequired()])
    name = StringField('name', validators=[Optional()], default=DefaultFormValue())
    shop_name = StringField('shop_name', validators=[Optional()], default=DefaultFormValue())
    category_id = CustomIntegerField('category_id', validators=[Optional()], default=DefaultFormValue())
    date_of_purchase = DateField('date_of_purchase', validators=[Optional()], default=DefaultFormValue())
    type_warranty_period = StringField('type_warranty_period', validators=[Optional()], default=DefaultFormValue())
    warranty_period = CustomIntegerField('warranty_period', validators=[Optional()], default=DefaultFormValue())
    archived = CustomBooleanField('archived', validators=[Optional()], default=DefaultFormValue())
    files_delete = ListField('files_delete', validators=[Optional()], default=DefaultFormValue())
    files_add = MultipleFileField('files_add', validators=[FilesOptional()])
    expertise = CustomBooleanField('expertise', validators=[Optional()], default=DefaultFormValue())
    date_end_expertise = DateField('date_end_expertise', validators=[Optional()], default=DefaultFormValue())
    money_returned = CustomBooleanField('money_returned', validators=[Optional()], default=DefaultFormValue())
    item_replaced = CustomBooleanField('item_replaced', validators=[Optional()], default=DefaultFormValue())


class WarrantyDeleteForm(FlaskForm):
    user_id = CustomIntegerField('user_id', validators=[InputRequired()])
    warranty_id = CustomIntegerField('warranty_id', validators=[InputRequired()])
