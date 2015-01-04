from serializers.stage import normal, extras, default_values
from serializers.stage import show_select_order, positional_order
from serializers.stage import events, geometry
from serializers import groups


def flat():
    return {
        'normal': normal.create_flat(),
        'common': extras.create()['common'],
        'show_select_order': show_select_order.create(),
        'positional_order': positional_order.create(),
        'geometry': geometry.create_flat(),
        'default_values': default_values.create_flat()
    }


def recursive():
    return {
        'normal': normal.create_recursive(),
        'default_values': default_values.create_recursive(),
        'events': events.create(),
        'geometry': geometry.create_recursive()
    }


# This is to sort serializers in the same order each time, as dictionaries don't have order
def all_by_category():
    flat_sz = flat()
    flat_keys = ['common', 'normal', 'show_select_order', 'positional_order', 'geometry', 'default_values']
    rec_sz = recursive()
    rec_keys = ['normal', 'default_values', 'events', 'geometry']

    return {
        'flat': groups.Composite([flat_sz[k] for k in flat_keys]),
        'recursive': groups.Composite([rec_sz[k] for k in rec_keys])
    }
