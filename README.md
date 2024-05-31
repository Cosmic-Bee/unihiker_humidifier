# unihiker_humidifier
DFRobot Unihiker application as a control screen for an Humidifier ESPHome Device

This project has two elements. It has Xiao ESP32S3 acting as the humidifier setup via ESPHome and then the DFRobot Unihiker acting as a control surface for the humidifier when the application has been loaded.

## Setup

### Xiao ESP32S3

The Xiao ESP32S3 has a few elements hooked up here to get the entire project working.

The primary elements are as followed:
- Of course a [Xiao ESP32S3](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/)
- A [Grove Base for Xiao](https://www.seeedstudio.com/Grove-Shield-for-Seeeduino-XIAO-p-4621.html) - optional but the HY2.0 4P connectors make setup fairly easy
- A [Grove DHT11 Temperature and Humidity Sensor](https://wiki.seeedstudio.com/Grove-TemperatureAndHumidity_Sensor/)
- A [Grove 4 Digit Display](https://wiki.seeedstudio.com/Grove-4-Digit_Display/)
- A [Grove Water Atomization Module](https://wiki.seeedstudio.com/Grove-Water_Atomization/)
- A [Bidirectional Level Shifter](https://www.sparkfun.com/products/12009)

Let's get started with the setup, from here it's actually not too bad outside of the level shifter and even that is fairly simple.

First connect the DHT11 via its Grove cable to the connector with the D0 as the outer pin. Given the DHT11 is a 1 wire interface you can see the Seeed folks set the other pin to NC meaning it's not connected and can be ignored.

Next connect the 4 digit display. It's connected to the Grove connector that shows D1 and D2 as the available signal pins. The D1 from the last connector is repeated here but it's safe to use as we didn't attach anything to D1 with the last connection per the NC.

With this setup we only need to connect the atomization module. I find having a couple Grove to Dupont cables helps for this step as it allows me to still rely on the connectors for the end devices. For my own use I relied on two of these [conversion cables](https://www.seeedstudio.com/Grove-4-pin-Male-Jumper-to-Grove-4-pin-Conversion-Cable-5-PCs-per-Pack.html) along with some dupont male to male cables.

On the Xiao Grove Expansion board it's possible to solder male or female pins to be able to use dupont cables directly from a pin. In this way I soldered female headers and used that male dupont cable to connect to the VBUS for the high voltage. From the VBUS pin I connected directly to HV pin on the level shifter.

With the HV setup you can then use the Grove to dupont cable connector, attach the red pin (3v3) to the LV pin on the level shifter. Attach the black pin to the common ground of your breadboard. Use dupont cables to then attach that common ground to the gnd inputs on the level shifter. Like the DHT11 the Atomization module only uses one signal wire so the additional wire can be plugged into an unused port on the breadboard to be kept out of the way. Connect the signal wire to one of the LV1-LV4 inputs. For the other Grove to dupont cable connect the NC signal wire to a random location, the signal wire to the corresponding HV# to the one you used (ie HV1 if you selected LV1), the red wire to the HV pin, and the black wire to the common GND.

In this way you will have setup the humidifier circuit. The screen is used for displaying the humidity, the DHT11 is used to return the humidity and temperature to ESPHome, and the atomization module is used for creating humidity.

Note: I'm not responsible if you destroy your electronics with humidity. I'd heavily suggest using an enclosure with a wire grommet and keeping your electronics away from moisture where possible.

For setup you'll need to go through the [normal ESPHome procedures for install](https://esphome.io/guides/getting_started_hassio.html). On my local machine I use the CLI to install the initial program and use my Home Assistant install to update OTA.

### DFRobot Unihiker

The Unihiker here is fairly straightforward to setup as it's only relying on a few components.

I opted to [use my stand with built in ringlight](https://www.printables.com/model/894852-unihiker-stand) for this project. The STL for 3D printing is available on printables if interested. It's a super simple stand for the Unihiker with a slot for the Micro:Bit connector, a backing piece to support the device which leaves the connectors free for use, and a ringlight for 8 LEDs for "night mode."

Here I had only a minimal set of components:
- A [DFRobot Unihiker](https://www.unihiker.com/)
- A [Grove SHT31 Temperature and Humidity Module](https://wiki.seeedstudio.com/Grove-TempAndHumi_Sensor-SHT31/)
- A 8 LED ring with 28mm screw spacing (unfortunately not sure on my source for this one, just had on hand)

I soldered a SMD connector to the LED ring allowing me to connect it directly to the Unihiker. To do this I confirmed the pin orientation out of the Unihiker and positioned the connector such that the same pins would connect to the cable.

The SHT31 I connected via a Grove to dupont cable connection followed by a similar cable connecting back to the Unihiker port i2c port. Seeed and DFRobot use different pinouts for their i2c so pay attention to the signal wires to ensure the SDA and SCL are properly connected.

For installation you can follow the normal [getting started procedures](https://www.unihiker.com/wiki/get-started). For my own setup I used VSCode remote SSH extension they discuss allowing access to the filesystem. To install the script in my case I simply created a `unihiker_humidifier.py` script at the root. From there you can run programs, find the script, and run it to enable this logic. I like in a sense how this makes the Unihiker versatile for running all sorts of applications.
