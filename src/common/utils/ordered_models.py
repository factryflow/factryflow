"""Utility functions for OrderedModel objects."""


def change_obj_priority(model_class, id: int, direction: str):
    try:
        max_order_count = model_class.objects.count() - 1
        ordered_obj = model_class.objects.get(id=id)

        if direction == "up" and ordered_obj.order > 0:
            ordered_obj.up()

        elif direction == "down" and ordered_obj.order < max_order_count:
            ordered_obj.down()

    except model_class.DoesNotExist as e:
        raise e
