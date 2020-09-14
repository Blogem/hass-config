# change attribute of a light smoothly. Currently supported: brightness, color_temp and rgb_color
# based on script by xaviml mentioned here: https://community.home-assistant.io/t/please-help-automation-for-ikea-tradfri-remote-control-e1524-e1810/142707/2

input_boolean = data.get("input_boolean")
entity_id = data.get("entity_id")
delta = data.get("delta")
attribute_id = data.get("light_attribute", "brightness")
delay = data.get("delay", 350)

attribute_mapping = {
    "brightness": {"min": 1, "max": 255},
    "color_temp": {"min": 250, "max": 454},
    "rgb_color": {"min": 0, "max": 255}
}

# turn on the light, just in case it wasn't on yet
data = { "entity_id": entity_id }
hass.services.call("light", "turn_on", data)

exit_service = False
while True:
    logger.info("Changing "+attribute_id+" for "+entity_id)
    switch_input = hass.states.get(input_boolean).state
    if switch_input == "off":
        break
    
    light = hass.states.get(entity_id)
    attr_value = light.attributes[attribute_id]

    logger.info("HASS REPORTS: "+str(attr_value))

    if attribute_id == 'rgb_color':
        # dit werkt nog niet. Uitzoeken hoe je mooi door de kleuren heen kan lopen.
        # idee:
        # - huidige kleur benaderen in buitenste ring (= volledige saturatie) door laagste getal naar 0 te veranderen
        # - positie in kleurenwiel bepalen: bij welke van de lijst licht-ie het dichtste? => hoe?
        # - vanaf die positie het kleurenwiel aflopen op basis van een vooraf bepaalde lijst.
        rgb = [0, 0, 0]
        # since list() doesn't work in hass
        for i in range(len(attr_value)):
            rgb[i] = attr_value[i]
            
        for i in range(len(attr_value)):
            old_rgb = rgb
            c = attr_value[i] + delta
            if c < attribute_mapping[attribute_id]["min"]:
                c = attribute_mapping[attribute_id]["max"]
            if c > attribute_mapping[attribute_id]["max"]:
                c = attribute_mapping[attribute_id]["min"]
            rgb[i] = c

            logger.info("Old color: "+str(old_rgb)+" | New color: "+str(rgb))

            service_data = {"entity_id": entity_id, attribute_id: rgb}
            logger.info(f"Service data: {service_data}")
            hass.services.call("light", "turn_on", service_data)

            time.sleep(delay / 1000)

    else:
        attr_value = attr_value + delta
        if attr_value < attribute_mapping[attribute_id]["min"]:
            attr_value = attribute_mapping[attribute_id]["min"]
            exit_service = True
            logger.info("Reached min")
        elif attr_value > attribute_mapping[attribute_id]["max"]:
            attr_value = attribute_mapping[attribute_id]["max"]
            exit_service = True
            logger.info("Reached max")

        service_data = {"entity_id": entity_id, attribute_id: attr_value}
        logger.info(f"Service data: {service_data}")
        hass.services.call("light", "turn_on", service_data)

        time.sleep(delay / 1000)

    if exit_service:
        break
