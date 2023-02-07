# ie-databus
This module makes reading from the IE Databus as simple as possible, allowing access to all of the data streamed through MQTT in real-time. The latest update also allows for writing to the IE Databus, which means data can be written from an edge app to the PLC. This module can even be used on flaskboard-lite.

This README is a word-for-word copy of my original User Guide which can be found [here](https://docs.google.com/document/d/18cB2fuYv82PcP7jc-YH7LVFJVVjQgwY-N9QI7hZKu7A/edit?usp=sharing).

The ie-databus module itself can be found [here](ie_databus.py).

Actual documentation can be found [here](https://sites.google.com/view/ie-databus-docs/home).

The example code used throughout this guide can be found [here](examples.py).

## Basic Usage
Only three lines are necessary to set up and get connected to the edge device’s IE Databus.
```python
from ie_databus import IEDatabus
databus = IEDatabus('edge', 'edge')
databus.start()
```

1. Pretty straightforward - simply imports the [`IEDatabus`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L37) class from the [`ie_databus`](ie_databus.py) package.
2. This line initializes the [`IEDatabus`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L37) class and prepares the MQTT client for connection. The two parameters are the username and password for the IE Databus, respectively.
3. Calling the [`start()`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L116) method connects to the edge device’s IE Databus and processes the tag headers. This method blocks until tag data is available.

***Note: The rest of this guide assumes that the above code snippet is already included.***

## Tags Overview
Data received from the IE Databus is organized in a dictionary of Tag objects. Tag objects expose all of the key-value pairs from the raw MQTT JSON data as object attributes.

Accessing this dictionary is simple:
```python
print(databus.tags)
```
```
{'Q_VFD1_Temperature': Tag(name='Q_VFD1_Temperature', id='101', data_type='Real', qc=3, ts='2022-08-02T18:02:50.430Z', [...]
```

The output is a Python `dict`, specifically of type `Dict[str, `[`Tag`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L10)`]`. The keys represent the name of a PLC tag and the value is a [`Tag`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L10) object with data about its respective tag.

[`Tag`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L10) objects have 7 relevant attributes:
| Name | Type | Description |
| :--: | :--: | ----------- |
| `name` | `str` | The name of the PLC tag |
| `id` | `str` | The ID of the PLC tag |
| `data_type` | `str` | The original data type of the `val` attribute |
| `qc` | `int` |
| `qx` | `int` |
| `ts` | `str` | The timestamp of when this data was received |
| `val` | `float` | The current value of the PLC tag |

See [**Reading PLC Tags**](#reading-plc-tags) for more info on how to use [`Tag`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L10) objects.

## Reading PLC Tags
Reading a specific PLC tag is simple; all you need is the name of the PLC tag you’re trying to read.
```python
print(databus.tags['Q_VFD3_Temperature'].val)
```
```
68.12994384765625
```
The example above prints out the current value of Conveyor 3’s temperature.

You can easily read multiple tags too.

```python
current_tags = databus.tags
tag_names = ['M_R01_S', 'M_R01_L', 'M_R01_U', 'M_R01_R', 'M_R01_B', 'M_R01_T']
for tag in tag_names:
    print(current_tags[tag].val)
```
```
0.0018717440543696284
0.0007486974936909974
89.99854278564453
0.0012352190678939223
-90.00113677978516
0.001852828892879188
```

The example above will print out the values for each tag listed in `tag_names`. Notice how the [`tags`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L87) attribute of the databus is only accessed once – otherwise, it is possible that a new set of data could come in and newer values would be accessed. Having tags with different timestamps could potentially create undesirable effects.

Values aren’t the only thing that can be read from PLC tags. Any of the attributes of the [`Tag`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L10) class can be accessed using the [`databus.tags`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L87) dictionary.

```python
print(databus.tags['I_R03_GripperLoad'])
print(databus.tags['I_Conveyor1Status_NIST_A'].ts)
```
```
Tag(name='I_R03_GripperLoad', id='112', data_type='Int', qc=3, ts='2022-08-02T18:15:38.178Z', val=1691)
2022-08-02T18:18:28.180Z
```

## Writing to PLC Tags
Writing data to a PLC tag is also very simple. Similar to reading data, all you need is the name of the PLC tag and the data you want to write.

```python
databus.write_to_tag('I_TwoWayCommunicator', True)
```

The example above writes `True` to the I_TwoWayCommunicator tag. Data written can be of any type that is serializable.

***Note: the PLC tag itself must be writable; otherwise, this function will do nothing.***

IEDatabus has a default write topic, but if you need to write to a tag under a different MQTT topic, you can.

```python
databus.write_topic = 'new/mqtt/topic'
databus.write_to_tag('I_TwoWayCommunicator', True)
```

## Advanced Usage
To disable listening for incoming MQTT data:

```python
databus.stop()
```

While the databus is stopped, you can still read from [`databus.tags`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L87), however the data will be the same as it was when [`stop()`](https://github.com/FutureFactoriesIE/ie-databus/blob/e89676e1649876402c247fbbc90e08ef1b8172cb/ie_databus.py#L122) was called. Basically, the data will not be up-to-date.

To re-enable listening for incoming MQTT data:

```python
databus.start()
```


## Examples
To get an overview of all of the available tags and their values:

```python
from ie_databus import IEDatabus
databus = IEDatabus('edge', 'edge')
databus.start()

for key, tag in databus.tags.items():
   print(f'{key}: {tag.val}')
```
```
Q_VFD1_Temperature: 32.064971923828125
Q_VFD2_Temperature: 68.12994384765625
Q_VFD3_Temperature: 68.12994384765625
[...]
```

Combining reading and writing together to notify the PLC if Conveyor 4’s temperature goes above 100 degrees:

```python
from ie_databus import IEDatabus
databus = IEDatabus('edge', 'edge')
databus.start()

import time
while True:
    if databus.tags['Q_VFD4_Temperature'].val > 100:
        databus.write_to_tag('I_TwoWayCommunicator', True)
        break
    time.sleep(1)
```
