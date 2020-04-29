import datetime
import logging
from . import getdataevn

import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_DISPLAY_OPTIONS, CONF_TYPE, CONF_SCAN_INTERVAL, CONF_USERNAME, CONF_NAME)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

DOMAIN = "evnhanoi"
customerId = ''
name = ''
SENSOR_TYPES = {
    'customerId': ['Mã khách hàng', 'mdi:account-search'],
    'month': ['Tháng', 'mdi:account-search'],
    'year': ['Năm', 'mdi:account-search'],
    'power': ['Công suất', 'mdi:account-search'],
    'totalMoney': ['Tổng tiền', 'mdi:account-search']
}
DEFAULT_TYPE_ = 'customerId'

SCAN_INTERVAL = datetime.timedelta(seconds=300)  # 5 minutes

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Optional(CONF_NAME, default={CONF_TYPE: name}): cv.string,
    vol.Optional(CONF_DISPLAY_OPTIONS, default={CONF_TYPE: DEFAULT_TYPE_}):
        vol.All(
            cv.ensure_list, [vol.In(SENSOR_TYPES)]
        )
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the system monitor sensors."""
    global customerId, name
    devices = []
    customerId = config.get(CONF_USERNAME)     
    name = config.get(CONF_NAME)
    for variable in config[CONF_DISPLAY_OPTIONS]:
        device = evnhanoiclass(variable)
        devices.append(device)

    add_entities(devices, True)


class evnhanoiclass(Entity):

    def __init__(self, sensor_type):
        global customerId, name
        self._name = SENSOR_TYPES[sensor_type][0] + name
        self.type = sensor_type
        self._state = None
        self._author = 'Tiến Dũng: GooseCapital'
        self._description = 'Version 1.1 - 29-04-2020'
        self.update()
        
    @property
    def name(self):
        return self._name.rstrip()

    @property
    def state(self):
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor"""
        return SENSOR_TYPES[self.type][1]

    @property
    def device_state_attributes(self):
        return {'Chú thích': self._description, 'Tác giả': self._author}

    @Throttle(SCAN_INTERVAL)
    def update(self):
        global customerId
        _LOGGER.debug('Ma khach hang: ' + customerId)
        data_evn = getdataevn.getlastestmonth(customerId, datetime.datetime.now().year)
        if self.type == 'customerId':
            self._state = data_evn['customerId']
        elif self.type == 'month':
            self._state = data_evn['month']
        elif self.type == 'year':
            self._state = data_evn['year']
        elif self.type == 'power':
            self._state = data_evn['power']
        elif self.type == 'totalMoney':
            self._state = data_evn['totalMoney']