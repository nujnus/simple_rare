import django
from faker import Faker
import datetime
import pytz
import pandas as pd
import random
from . import data

fake = Faker()


class RareGenerator():

    # private:
    def __IntegerField_generator(self, field, unique):
        if unique:
            ints = iter(data.unique_int)
            for value in self.values:
                value[field] = next(ints)
        else:
            for value in self.values:
                value[field] = fake.random_int(0, 1024)

    def __BigIntegerField_generator(self, field, unique):
        self.__IntegerField_generator(field, unique)

    def __PositiveIntegerField_generator(self, field, unique):
        self.__IntegerField_generator(field, unique)

    def __BooleanField_generator(self, field, unique):
        if unique:
            bools = iter(data.unique_bool)
            for value in self.values:
                value[field] = next(bools)
        else:
            for value in self.values:
                value[field] = fake.pybool()

    def __NullBooleanField_generator(self, field, unique):
        self.__BooleanField_generator(field, unique)

    def __FloatField_generator(self, field, unique):
        if unique:
            floats = iter(data.unique_float)
            for value in self.values:
                value[field] = next(floats)
        else:
            for value in self.values:
                value[field] = fake.pyfloat()

    def __DecimalField_geneartor(self, field, unique):
        if unique:
            decimals = iter(data.unique_decimal)
            for value in self.values:
                value[field] = next(decimals)
        else:
            for value in self.values:
                value[field] = fake.pydecimal(left_digits=3, right_digits=3)

    def __CharField_generator(self, field, unique):
        if unique:
            strings = iter(data.unique_string)
            for value in self.values:
                value[field] = next(strings)
        else:
            for value in self.values:
                value[field] = fake.pystr(min_chars=20, max_chars=50)

    def __TextField_generator(self, field, unique):
        self.__CharField_generator(field, unique)

    def __URLField_generator(self, field, unique):
        if unique:
            urls = iter(data.unique_url)
            for value in self.values:
                value[field] = next(urls)
        else:
            for value in self.values:
                value[field] = fake.url()

    def __UUIDField_generator(self, field, unique):
        if unique:
            uuids = iter(data.unique_uuid)
            for value in self.values:
                value[field] = next(uuids)
        else:
            for value in self.values:
                value[field] = fake.uuid4()

    def __DateField_generator(self, field, unique):
        delta = datetime.timedelta(days=len(self.values) - 1)
        end = datetime.date.today()
        start = end - delta

        if unique == True:

            dates = [d.to_pydatetime() for d in pd.date_range(start=start, end=end)]

            random.shuffle(dates)

            for value in self.values:
                value[field] = dates.pop()
        else:
            for value in self.values:
                value[field] = fake.date_between_dates(date_start=start, date_end=end)

    def __DateTimeField_generator(self, field, unique):
        delta = datetime.timedelta(days=len(self.values) - 1)
        end = datetime.date.today()
        start = end - delta

        for value in self.values:
            value[field] = fake.date_time_between_dates(
                datetime_start=start,
                datetime_end=end).replace(tzinfo=(pytz.timezone('Asia/Shanghai')))

    def __DurationField_generator(self, field, unique):
        deltas = [datetime.timedelta(days=x) for x in range(len(self.values))]
        for value in self.values:
            value[field] = random.sample(deltas, 1)[0]

    def __TimeField_generator(self, field, unique):
        if unique:
            times = iter(data.unique_time)
            for value in self.values:
                value[field] = next(times)
        for value in self.values:
            value[field] = fake.time(pattern='%H:%M:%S', end_datetime=None)

    def __EmailField_generator(self, field, unique):
        if unique:
            emails = iter(data.unique_email)
            for value in self.values:
                value[field] = next(emails)
        else:
            for value in self.values:
                value[field] = fake.email()

    def __GenericIPAddressField_generator(self, field, unique):
        if unique:
            ips = iter(data.unique_ipv4)
            for value in self.values:
                value[field] = next(ips)
        else:
            for value in self.values:
                value[field] = fake.ipv4()

    def __SlugField_generator(self, field, unique):
        if unique:
            slugs = iter(data.unique_slug)
            for value in self.values:
                value[field] = next(slugs)
        else:
            for value in self.values:
                value[field] = fake.slug()

    def __FileField_generator(self, field, unique):
        if unique:
            files = iter(data.unique_file_name)
            for value in self.values:
                value[field] = next(files)
        else:
            for value in self.values:
                value[field] = fake.file_name()

    def __FilePathField_generator(self, field, unique):
        if unique:
            file_paths = iter(data.unique_file_path)
            for value in self.values:
                value[field] = next(file_paths)
        else:
            for value in self.values:
                value[field] = fake.file_path()

    def __ImageField_generator(self, field, unique):
        if unique:
            image_paths = iter(data.unique_image_path)
            for value in self.values:
                value[field] = next(image_paths)
        else:
            for value in self.values:
                value[field] = fake.file_name(extension='png')

    def __BinaryField_generator(self, field, unique):
        assert unique ==  False,  "BinaryField_generator不支持unique"
        for value in self.values:
            value[field] = fake.binary(length=64)

    def __ForeignKey_generator(self, field, unique):
        raise Exception("无法自动生成ForeignKey:{} 的值".format(field))

    def __OneToOneField_generator(self, field, unique):
        raise Exception("无法自动生成OneToOneField:{} 的值".format(field))

    __default_generators = {
        django.db.models.fields.IntegerField: __IntegerField_generator,
        django.db.models.fields.BigIntegerField: __BigIntegerField_generator,
        django.db.models.fields.PositiveIntegerField: __PositiveIntegerField_generator,
        django.db.models.fields.BooleanField: __BooleanField_generator,
        django.db.models.fields.NullBooleanField: __NullBooleanField_generator,
        django.db.models.fields.FloatField: __FloatField_generator,
        django.db.models.fields.DecimalField: __DecimalField_geneartor,
        django.db.models.fields.CharField: __CharField_generator,
        django.db.models.fields.TextField: __TextField_generator,
        django.db.models.fields.URLField: __URLField_generator,
        django.db.models.fields.UUIDField: __UUIDField_generator,
        django.db.models.fields.DateField: __DateField_generator,
        django.db.models.fields.DateTimeField: __DateTimeField_generator,
        django.db.models.fields.DurationField: __DurationField_generator,
        django.db.models.fields.TimeField: __TimeField_generator,
        django.db.models.fields.EmailField: __EmailField_generator,
        django.db.models.fields.GenericIPAddressField: __GenericIPAddressField_generator,
        django.db.models.fields.SlugField: __SlugField_generator,
        django.db.models.fields.FilePathField: __FilePathField_generator,
        django.db.models.fields.BinaryField: __BinaryField_generator,

        django.db.models.fields.files.ImageField: __ImageField_generator,
        django.db.models.fields.files.FileField: __FileField_generator,
        django.db.models.fields.related.ForeignKey: __ForeignKey_generator,
        django.db.models.fields.related.OneToOneField: __OneToOneField_generator,
    }

    # 用户不应该直接调用这个函数
    # protected:
    def _generate_data(self, field, unique=False):
        field_type = self.field_types[field]
        assert field_type in self.__default_generators.keys(), "__default_generators中缺少对应类型的generator"
        self.__default_generators[field_type](self, field, unique)
