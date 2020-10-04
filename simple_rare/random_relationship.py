import random
import itertools
from .rare_generator import RareGenerator
from .random_foreign import RandomForeign
from .util import partition

class RandomBuilder(RareGenerator, RandomForeign):
    def __init__(self, total_number, model, remove_field_name='id'):
        self.model = model
        self.field_names_remained = [field.name for field in model._meta.fields]
        self.field_names_remained.remove(remove_field_name)
        self.field_types = {field.name: type(field) for field in model._meta.fields}
        self.fields = {field.name: field for field in model._meta.fields}

        self.values = self.init_from_field_names(total_number)
        self.objects = []

    def print_type_map(self):
        obj = self.model.objects.first()
        for f in self.model._meta.fields:
            print("{:>20s}|{:>55s}|{}".format(f.name, str(type(f)), type(getattr(obj, str(f.name)))))

    def create(self):
        for field_name in self.field_names_remained.copy():
            #print(str(self.model) + '  create:' + field_name)
            self.generate_data(field=field_name)
        for value in self.values:
            self.objects.append(self.model.objects.create(**value))
        return self.objects

    def get_field_names_remained(self):
        return self.field_names_remained

    def get_field_type(self, field_name):
        if field_name in self.field_types:
            return self.field_types(field_name)

    def get_values(self):
        return self.values

    def init_from_field_names(self, total_number):
        assert total_number > 0, '总数不能小于0'
        assert len(self.field_names_remained) > 0, '没有足够的field_name'
        values = []
        for _ in range(total_number):
            values.append(dict.fromkeys(self.field_names_remained))
        return values

    #def generate_together(self, field, generator=None, fake_args=[], fake_kwargs={}, unique=False):


    def generate_data(self, field, generator=None, fake_args=[], fake_kwargs={}, unique=False):
        assert field != None, "参数field不能为None"
        self.field_names_remained.remove(field)
        if generator != None:
            for value in self.values:
                value[field] = generator(*fake_args, **fake_kwargs)
        else:
            self._generate_data(field, unique=unique)
        return self.values

    def set_value(self, field, value=None):
        assert field != None, "参数field不能为None"
        self.field_names_remained.remove(field)
        for value in self.values:
            value[field] = value
        return self.values

    def one_to_one(self, field=None, target_model=None, target_field='id'):
        target_objects = list(target_model.objects.all()[:len(self.values)])
        assert len(self.values) == len(target_objects), "target_objects的数量不足"
        self.field_names_remained.remove(field)
        random.shuffle(target_objects)

        for i in range(len(self.values)):
            self.values[i][field] = getattr(target_objects[i], target_field)
        return self.values

    def many_to_one(self, field=None, target_model=None, target_field='id', target_number=1):
        assert len(self.values) >= target_number, "target_number必须小于等于len(self.values)"
        partition_step = len(self.values) // target_number
        target_objects = list(target_model.objects.all()[:target_number])
        assert len(target_objects) == target_number, "target_objects 数量未达到 target_number 指定值"

        self.field_names_remained.remove(field)
        part_values = partition(self.values, partition_step)

        for target_object in target_objects:
            for fb in part_values[target_objects.index(target_object)]:
                fb[field] = getattr(target_object, target_field)

        values = list(itertools.chain(*part_values))
        random.shuffle(values)
        self.values = values
        return self.values

    def many_to_many(self, through_model=None, target_model=None,
                     from_through_field=None, target_through_field=None,
                     sample_number=1, total_number=1,
                     field='id', target_field='id'):

        from_objs = list(self.model.objects.all()[:total_number])
        target_objs = list(target_model.objects.all()[:total_number])

        assert sample_number <= len(from_objs), "sample_number 不能大于self.model的实例数"
        from_objs_groups = [list(set(random.sample(from_objs, sample_number))) for _ in range(total_number)]

        for i in range(total_number):
            for f_obj in from_objs_groups[i]:
                through_model.objects.get_or_create(
                    **{from_through_field: getattr(f_obj, field),
                       target_through_field: getattr(target_objs[i], target_field)})


