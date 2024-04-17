from datetime import time

import factory
from common.utils.tests import faker
from resource_calendar.models import WeeklyShiftTemplate, WeeklyShiftTemplateDetail, DaysOfWeek


class WeeklyShiftTemplateDetailFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeeklyShiftTemplateDetail

    day_of_week = factory.lazy_attribute(lambda _: faker.random_element(DaysOfWeek))
    start_time = factory.lazy_attribute(lambda _: time(hour=faker.random_int(5, 11)))
    end_time = factory.lazy_attribute(lambda _: time(hour=faker.random_int(12, 23)))


class WeeklyShiftTemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = WeeklyShiftTemplate

    name = factory.lazy_attribute(lambda _: faker.unique.catch_phrase())
    description = factory.lazy_attribute(lambda _: faker.sentence())
    external_id = ""
    notes = ""
    weekly_shift_template_details = factory.RelatedFactoryList(
        WeeklyShiftTemplateDetailFactory, factory_related_name="weekly_shift_template", size=7
    )