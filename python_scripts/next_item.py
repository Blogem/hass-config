# for a group of entities, return item current+1 or if not exists, item 0
# do something with the entity, based on typ

current_tracker = 'input_text.current_active_light'
groupname = data.get('groupname')
counter = data.get('counter')


data = { "entity_id": counter }
hass.services.call('input_number', 'increment', data)
next = int(float(hass.states.get(counter).state))

logger.info('Fetch next entity from group '+str(groupname)+' (next: '+str(next)+')')

group = hass.states.get(groupname)

# loop around
if next == len(group.attributes["entity_id"]):
  next = 0

entity_id = group.attributes["entity_id"][next]
entity_type = entity_id.split('.')[0]
entity_name = entity_id.split('.')[1]
logger.info('Entity: '+str(entity_id)+', type:'+entity_type)

# save the name of the entity so we can use it in hass
if entity_type in ('switch', 'light'):
  data = { "entity_id": current_tracker, "value": entity_id}
  hass.services.call('input_text', 'set_value', data)

# let the light announce itself
if entity_type == 'switch':
  if hass.states.get(entity_id).state == 'on':
    # on-off
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_off', data)
    time.sleep(1)
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_on', data)
  else:
    # off-on
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_on', data)
    time.sleep(1)
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_off', data)

elif entity_type == 'light':
  if hass.states.get(entity_id).state == 'on':
    # pulse
    pass
  else:
    # on-pulse-off
    data = { "entity_id": entity_id }
    hass.services.call('light', 'turn_on', data)
    # pulse
    time.sleep(1)
    data = { "entity_id": entity_id }
    hass.services.call('light', 'turn_off', data)

elif entity_type == 'script':
  # execute the script
  hass.services.call('script', entity_name)


# update counter to the next
data = { "entity_id": counter, "value": next}
hass.services.call('input_number', 'set_value', data)

