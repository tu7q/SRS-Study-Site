from django.db import models
from django.db.models.base import ModelBase
from typing import Dict


class MultiField:
    """
    Also Dumb
    """

    @staticmethod
    def join(attr_name, name):
        return attr_name + "_" + name

    def __init__(self, get, set, **fields: Dict[str, models.Field]):
        self.getter = get
        self.setter = set
        self.fields = fields

    def init_fields(self, attr: str) -> Dict[str, models.Field]:
        return {self.join(attr, field_name): field for field_name, field in self.fields.items()}

    def as_property(self, attr: str) -> property:
        def _get(model):
            return self.getter(**{field: getattr(model, self.join(attr, field)) for field in self.fields.keys()})

        def _set(model, value):
            values = self.setter(value)
            for k, v in values.items():
                setattr(model, self.join(attr, k), v)

        return property(
            fget=_get,
            fset=_set  # ,
            # doc=''
        )


class MultiFieldMeta(ModelBase):
    """
    Really Dumb
    """

    def __new__(cls, name, bases, old_attrs, **kwargs):
        multifields = []
        attrs = {}
        for attr_name, attr in old_attrs.items():
            if isinstance(attr, MultiField):
                attrs.update(attr.init_fields(attr_name))
                attrs[attr_name] = attr.as_property(attr_name)

                multifields.append(attr_name)
            else:
                attrs[attr_name] = attr

        attrs["multifields"] = multifields

        return super().__new__(cls, name, bases, attrs, **kwargs)


class MultiFieldBase(models.Model, metaclass=MultiFieldMeta):
    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        updates = []
        for field_name in self.multifields:
            value = kwargs.pop(field_name, None)
            if value:
                # it will override any manually specified value supplied for the automatically generated field
                updates.append((field_name, value))

        super().__init__(self, *args, **kwargs)

        for name, value in updates:
            setattr(self, name, value)
