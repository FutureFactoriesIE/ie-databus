# Setup for the following examples
from ie_databus import IEDatabus
databus = IEDatabus('edge', 'edge')
databus.start()


# Example 1 - reading the value of a PLC tag
print(databus.tags['Q_VFD3_Temperature'].val)


# Example 2 - reading multiple PLC tags
current_tags = databus.tags
tag_names = ['M_R01_S', 'M_R01_L', 'M_R01_U', 'M_R01_R', 'M_R01_B', 'M_R01_T']
for tag in tag_names:
    print(current_tags[tag].val)


# Example 3 - reading other attributes of a PLC tag
print(databus.tags['I_R03_GripperLoad'])
print(databus.tags['I_Conveyor1Status_NIST_A'].ts)


# Example 4 - writing data to a PLC tag
databus.write_to_tag('I_TwoWayCommunicator', True)


# Example 5 - writing data via a different MQTT topic
databus.write_topic = 'new/mqtt/topic'
databus.write_to_tag('I_TwoWayCommunicator', True)


# Example 6 - disable listening for incoming MQTT data
databus.stop()


# Example 6 - re-enable listening for incoming MQTT data
databus.start()


# Example 8 - getting an overview of all of the available tags and their values
for key, tag in databus.tags.items():
    print(f'{key}: {tag.val}')


# Example 9 - combining reading and writing to tags
import time
while True:
    if databus.tags['Q_VFD4_Temperature'].val > 100:
        databus.write_to_tag('I_TwoWayCommunicator', True)
        break
    time.sleep(1)
