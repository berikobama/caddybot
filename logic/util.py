def collect_fields(func, site, inst, fields):
    data = func(site,inst).get("records").get("data")
    val_str = "Age: {AGE}\n".format(AGE=data.get("secondsAgo").get("valueFormattedWithUnit"))
    for field in fields:
        val_str = val_str + "{ATTR}: {VAL}\n".format(ATTR=data.get(field).get("dataAttributeName"), VAL=data.get(field).get("valueFormattedWithUnit"))
    return val_str

def get_google_maps_url(api):
    loc = api.gps_widget(50134).get("records").get("data").get("attributes")
    lat = loc.get("4").get("valueFormattedValueOnly")
    lon = loc.get("5").get("valueFormattedValueOnly")
    return "https://maps.google.com/?q={LAT},{LON}".format(LAT=str(lat), LON=str(lon))


def handle_status(api, bot, chat_id, solar_id, site_id, bmv_id):
	val_str = collect_fields(
        api.battery_summary_widget,
        site_id,
        bmv_id,
        ["47", "49", "50", "51", "115"])
	bot.sendMessage(chat_id, val_str)

def handle_solar(api, bot, chat_id, solar_id, site_id, bmv_id):
	val_str = collect_fields(
        api.solar_charger_summary_widget,
        site_id,
        solar_id,
        ["85", "94", "96", "107"])
	bot.sendMessage(chat_id, val_str)

def handle_maps(api, bot, chat_id, solar_id, site_id, bmv_id):
	bot.sendMessage(chat_id, get_google_maps_url(api))

def get_help(api, bot, chat_id, solar_id, site_id, bmv_id):
	bot.sendMessage(chat_id, "not implemented yet.")