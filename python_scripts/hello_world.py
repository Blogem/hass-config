name = data.get('name', 'world')
logger.error("Hello {}".format(name))
hass.bus.fire(name, { "wow": "from a Python script!" })