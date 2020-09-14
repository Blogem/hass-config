# for a group of entities, return item current+1 or if not exists, item 0
# do something with the entity, based on type

def pulse(entity_id):
  try:
    # pulse: go to 100%, then 1% brightness, then back to original
    state = hass.states.get(entity_id)
    original_status = state.state

    logger.info('Pulsing '+entity_id+'...')

    if original_status == 'off':
      data = { "entity_id": entity_id }
      hass.services.call('light', 'turn_on', data)
      time.sleep(1/10)

    state = hass.states.get(entity_id)
    original_brightness = state.attributes["brightness"]

    logger.info('Original state: '+original_status+', original brightness: '+str(original_brightness)+')')
      
    # 100%
    data = { "entity_id": entity_id, "brightness_pct": 100, "transition": 1}
    hass.services.call('light', 'turn_on', data)
    time.sleep(1)
 
    # 1%
    data = { "entity_id": entity_id, "brightness_pct": 1, "transition": 1}
    hass.services.call('light', 'turn_on', data)
    time.sleep(1)

    # original reset
    data = { "entity_id": entity_id, "brightness": original_brightness, "transition": 1}
    hass.services.call('light', 'turn_on', data)
    time.sleep(1)


    if original_status == 'off':
      data = { "entity_id": entity_id }
      hass.services.call('light', 'turn_off', data)

    return True

  except Exception as e:
    logger.error('Failed pulsing light!')
    logger.info(e)
    return False
        

current_tracker = 'input_text.current_active_light'
groupname = data.get('groupname')
counter = data.get('counter')
direction = data.get('direction')

# get next index in counter
data = { "entity_id": counter }

if direction == 'forward':
  hass.services.call('input_number', 'increment', data, True)
else: # reverse
  hass.services.call('input_number', 'decrement', data, True)

index = int(float(hass.states.get(counter).state))

# see if we have to loop
group = hass.states.get(groupname)
num_entities = len(group.attributes["entity_id"])

# loop forward
if index >= num_entities and direction == 'forward':
  index = 0
  data = { "entity_id": counter, "value": 0}
  hass.services.call('input_number', 'set_value', data)

# loop backwards
if index == 0 and direction == 'reverse':
  data = { "entity_id": counter, "value": num_entities}
  hass.services.call('input_number', 'set_value', data)

logger.info('Fetch next entity from group '+str(groupname)+' (index: '+str(index)+')')

entity_id = group.attributes["entity_id"][index]
entity_type = entity_id.split('.')[0]
entity_name = entity_id.split('.')[1]

logger.info('Entity: '+str(entity_id)+', type:'+entity_type)

# in case of switch or light, save the name of the entity so we can use it in hass later on
if entity_type in ('switch', 'light'):
  data = { "entity_id": current_tracker, "value": entity_id}
  hass.services.call('input_text', 'set_value', data)

# let the light announce itself
status = hass.states.get(entity_id).state
if entity_type == 'switch':
  if status == 'on':
    # off-on
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_off', data)
    time.sleep(1/5)
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_on', data)
  else:
    # on-off
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_on', data)
    time.sleep(1/5)
    data = { "entity_id": entity_id }
    hass.services.call('switch', 'turn_off', data)

elif entity_type == 'light':
  # pulse the light
  pulse(entity_id)

elif entity_type == 'script':
  # execute the script
  hass.services.call('script', entity_name, None, True)


