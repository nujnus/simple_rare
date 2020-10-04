# simple_rare

## 简介: simple random relationship 
为模型批量生成随机数据, 并根据为model预设的关系, 随机组织数据之间的关联.

## install
```
python setup.py install
```

## 注意:
rare对django model中各类型字段, 提供了一套默认的随机数据生成方式, 
但是,目前默认的fake的数据生成的参数很多是写死的,
可能会和model的字段参数不兼容,
所以当生成的数据长度(max_length)或其他条件无法满足时, 
建议使用generate_data和fake来自定义数据生成方式.

例如:
```
rr = RandomBuilder(1000, ModelB)
rr.generate_data(field='c', generator=fake.random_int, fake_args=(0, 100))
rr.create()
```

## example:
model.py
```
class ModelB(models.Model):
    b = models.IntegerField()
    b2 = models.BigIntegerField()
    b3 = models.PositiveIntegerField()
    b4 = models.IntegerField()
    b5 = models.BooleanField()
    b6 = models.NullBooleanField()
    b7 = models.FloatField()
    b8 = models.DecimalField(max_digits=5, decimal_places=2)
    b9 = models.CharField(max_length=100)
    b10 = models.TextField()
    b11 = models.URLField()
    b12 = models.UUIDField()
    b13 = models.DateField()
    b14 = models.DateTimeField()
    b15 = models.DurationField()
    b16 = models.TimeField()
    b17 = models.EmailField()
    b18 = models.FileField()
    b19 = models.FilePathField()
    b20 = models.ImageField()
    b21 = models.GenericIPAddressField()
    b22 = models.BinaryField()
    b23 = models.SlugField()


class ModelX(models.Model):
    x = models.IntegerField()

class ModelO(models.Model):
    o = models.IntegerField()

class ModelM(models.Model):
    m = models.IntegerField()

class ModelC(models.Model):
    c = models.IntegerField()

class ModelA(models.Model):
    a = models.IntegerField()
    b = models.IntegerField()
    c = models.IntegerField()
    x = models.ForeignKey(ModelX, on_delete = models.CASCADE)
    o = models.OneToOneField(ModelO, on_delete=models.DO_NOTHING)
    m = models.ManyToManyField('ModelM')

class ModelF(models.Model):
    f = models.IntegerField()


class ModelA_F(models.Model):
    a_id = models.IntegerField()
    f_id = models.IntegerField()

    class Meta:
        unique_together = ('a_id', 'f_id',)
```

demo.py
```
import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_django_demo.settings.dev")
django.setup()

from faker import Faker
fake = Faker()  # English

from app_demo_2EC6E023F4.models import ModelB
from app_demo_2EC6E023F4.models import ModelX
from app_demo_2EC6E023F4.models import ModelO
from app_demo_2EC6E023F4.models import ModelM
from app_demo_2EC6E023F4.models import ModelC
from app_demo_2EC6E023F4.models import ModelA
from app_demo_2EC6E023F4.models import ModelF
from app_demo_2EC6E023F4.models import ModelA_F


b = RandomBuilder(1000, ModelB)
b.generate_data(field='b', generator=fake.random_int, fake_args=(0, 1000))
b.generate_data(field='b2')
b.create()


c = RandomBuilder(1000, ModelC)
c.generate_data(field='c', generator=fake.random_int, fake_args=(0, 100))
c.create()
    
f = RandomBuilder(1000, ModelF)
f.generate_data(field='f', generator=fake.random_int, fake_args=(0, 100))
f.create()


x = RandomBuilder(1000, ModelX)
x.create()

o = RandomBuilder(1000, ModelO)
o.create()


m = RandomBuilder(1000, ModelM)
m.create()


a = RandomBuilder(1000, ModelA)
a.generate_data(field='a', generator=fake.random_int, fake_args=(0, 100))
a.one_to_one(field='b', target_model=ModelB, target_field='id')
a.many_to_one(field='c', target_model=ModelC, target_field='id', target_number=10)
a.foreign(field='x', target_number=10)
a.foreign_to_one(field='o')
a.create()
a.auto_many_to_many('m',sample_number=10, total_number=100)

    
a.many_to_many(through_model=ModelA_F, target_model=ModelF,
                from_through_field='a_id', target_through_field='f_id',
                sample_number=10, total_number=100)

```

仅支持单个字段的unique (暂时不提供对 unique_together 的支持)
```
import os
import django
import sys

sys.path.append(r'../a_django_demo')  # 引入实际的项目目录
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_django_demo.settings.dev")
django.setup()

from simple_rare.random_relationship import RandomBuilder

from faker import Faker
fake = Faker()  # English

from app_demo_2EC6E023F4.models import ModelB
from app_demo_2EC6E023F4.models import ModelX
from app_demo_2EC6E023F4.models import ModelO
from app_demo_2EC6E023F4.models import ModelM
from app_demo_2EC6E023F4.models import ModelC
from app_demo_2EC6E023F4.models import ModelA
from app_demo_2EC6E023F4.models import ModelF
from app_demo_2EC6E023F4.models import ModelA_F


b = RandomBuilder(1000, ModelB)
b.generate_data(field='b', generator=fake.random_int, fake_args=(0, 1000))
b.generate_data(field='b2')
b.generate_data(field='b3', unique=True)
b.generate_data(field='b4', unique=True)
b.generate_data(field='b5', unique=True)
b.generate_data(field='b6', unique=True)
b.generate_data(field='b7', unique=True)
b.generate_data(field='b8', unique=True)
b.generate_data(field='b9', unique=True)
b.generate_data(field='b10', unique=True)
b.generate_data(field='b11', unique=True)
b.generate_data(field='b12', unique=True)
b.generate_data(field='b13', unique=True)
b.generate_data(field='b14', unique=True)
b.generate_data(field='b15', unique=True)
b.generate_data(field='b16', unique=True)
b.generate_data(field='b17', unique=True)
b.generate_data(field='b18', unique=True)
b.generate_data(field='b19', unique=True)
b.generate_data(field='b20', unique=True)
b.generate_data(field='b21', unique=True)
b.generate_data(field='b23', unique=True)
b.create()


c = RandomBuilder(1000, ModelC)
c.generate_data(field='c', generator=fake.random_int, fake_args=(0, 100))
c.create()
    
f = RandomBuilder(1000, ModelF)
f.generate_data(field='f', generator=fake.random_int, fake_args=(0, 100))
f.create()


x = RandomBuilder(1000, ModelX)
x.create()

o = RandomBuilder(1000, ModelO)
o.create()


m = RandomBuilder(1000, ModelM)
m.create()


a = RandomBuilder(1000, ModelA)
a.generate_data(field='a', generator=fake.random_int, fake_args=(0, 100))
a.one_to_one(field='b', target_model=ModelB, target_field='id')
a.many_to_one(field='c', target_model=ModelC, target_field='id', target_number=10)
a.foreign(field='x', target_number=10)
a.foreign_to_one(field='o')
a.create()
a.auto_many_to_many('m',sample_number=10, total_number=100)

    
a.many_to_many(through_model=ModelA_F, target_model=ModelF,
                from_through_field='a_id', target_through_field='f_id',
                sample_number=10, total_number=100)
```
