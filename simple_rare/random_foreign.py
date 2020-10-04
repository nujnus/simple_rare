import random
import itertools
from .util import partition


class RandomForeign:

    def foreign(self, field, target_number=1):
        assert field in self.fields.keys(), "不存在的field"
        field_obj = self.fields[field]
        target_model = field_obj.related_model
        target_field = field_obj.target_field

        assert len(self.values) >= target_number, "target_number必须小于等于len(self.values)"
        partition_step = len(self.values) // target_number
        target_objects = list(target_model.objects.all()[:target_number])
        assert len(target_objects) == target_number, "target_objects 数量未达到 target_number 指定值"

        self.field_names_remained.remove(field)
        part_values = partition(self.values, partition_step)

        for target_object in target_objects:
            for fb in part_values[target_objects.index(target_object)]:
                fb[field] = target_object
        values = list(itertools.chain(*part_values))
        random.shuffle(values)
        self.values = values
        return self.values

    def foreign_to_one(self, field):
        assert field in self.fields.keys(), "不存在的field"
        field_obj = self.fields[field]
        target_model = field_obj.related_model
        target_field = field_obj.target_field

        target_objects = list(target_model.objects.all()[:len(self.values)])
        assert len(self.values) == len(target_objects), "target_objects的数量不足"
        self.field_names_remained.remove(field)
        random.shuffle(target_objects)

        for i in range(len(self.values)):
            self.values[i][field] = target_objects[i]
        return self.values

    def auto_many_to_many(self, field, sample_number=1, total_number=1):
        field_obj = getattr(self.model, field).field
        target_model = field_obj.related_model

        from_objs = list(self.model.objects.all()[:total_number])
        target_objs = list(target_model.objects.all()[:total_number])

        assert sample_number <= len(from_objs), "sample_number 不能大于self.model的实例数"
        from_objs_groups = [random.sample(from_objs, sample_number) for _ in range(total_number)]

        for i in range(total_number):
            for f_obj in from_objs_groups[i]:
                getattr(f_obj, field).add(target_objs[i])
                f_obj.save()
