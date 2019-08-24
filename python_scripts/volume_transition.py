# based on: mouth4war's script in https://community.home-assistant.io/t/volume-transition-feature-for-media-player/13091/6
#
# 2019-08-20: 
#  - added transition_duration, base step on that
#  - bit more verbose logging
#  - always start at start_level

#{
#"entity_id": "media_player.chromebitch",
#"transition_duration": 900, #in seconds
#"sleep_delay": 1, #in seconds
#"start_level": 0.1,
#"end_level": 0.8,
#}

entity_id  = data.get('entity_id') #media_player.name
transition_duration = float(data.get('transition_duration')) #in seconds
sleep_delay = int(data.get('sleep_delay')) #in seconds
start_level = float(data.get('start_level')) #(0 .. 1)
end_level = float(data.get('end_level')) #(0 .. 1)
step = (end_level-start_level)/(transition_duration/float(sleep_delay))


logger.info('Start volume transition.\nentity_id: '+str(entity_id)+'\nsleep_delay: '+str(sleep_delay)+'\nstart_level: '+str(start_level)+'\nend_level: '+str(end_level)+'\ntransition_duration: '+str(transition_duration)+'\nstep: '+str(step)+'\nSet volume to start level ' + str(start_level))

# set level to start level
data = { "entity_id": entity_id, "volume_level": start_level}
hass.services.call('media_player', 'volume_set', data)
time.sleep(sleep_delay)

# start transitioning from start_level to end_level
new_level = start_level + step
while new_level < end_level :
  states = hass.states.get(entity_id)
  current_level = states.attributes.get('volume_level') or 0
  if (current_level > new_level) :
    logger.info('Exiting Fade In (current level: '+str(current_level)+', new level: '+ str(new_level))
    break;
  else :
    logger.info('Setting volume of ' + str(entity_id) + ' from ' + str(current_level) + ' to ' + str(new_level))
    data = { "entity_id" : entity_id, "volume_level" : new_level }
    hass.services.call('media_player', 'volume_set', data)
    new_level = new_level + step
    time.sleep(sleep_delay)
logger.info('Stop volume transition')
