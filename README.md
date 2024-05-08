# OTA updates for Finder Opta using PLC IDE

This example contains a fully functional project that provides guidance on how
to implement OTA updates on the Finder Opta using Arduino PLC IDE. In
particular, the C++ sketch in this project downloads and applies a remote
update on the Finder Opta, while the Ladder diagram notifies the status of
the operation using the LEDs of the device.

## Usage

Once you have a server that can serve a `.ota` file to the Finder Opta via
Ethernet, extract the `.zip` file and open the project in PLC IDE. Next, edit
the update path in the sketch:

```cpp
#include <Arduino.h>
#include <Portenta_Ethernet.h>
#include <Arduino_Portenta_OTA.h>

const char *filename = "http://your.server:port/your_file.OTA";

void setup()
{
    ...
```

Now you can upload the code to the Finder Opta and see the update take place in
real time!

### Running an update server

If you do not have a server that can provide OTA updates but you still would
like to test out this example, we provide a `.ota` in the `assets` subfolder of
this directory. The easiest way to serve this file to the Finder Opta would be
the barebone Python HTTP server. To do so, execute the following command in the
root directory of this project:

```bash
python3 -m http.server -d ./assets -b <IP_ADDRESS>
```

Now simply edit the update path in the sketch using the same IP address provided in the above
command. The provided `.ota` file, contains a sketch that will make the LEDs
blink, so that you can easily tell when the update has been applied.

### Creating your own `.ota` file

To create a custom `.ota` file, start from a sketch and follow these steps:

1. In Arduino IDE select *Sketch->Export* compiled Binary from the menu or, if
   using `arduino-cli` use the `--export-binaries` command line option.
2. From the command line, execute the `bin2ota.py` program that can be found in
   the `extras/make-ota` folder:

```cpp
python3 extras/make-ota/bin2ota.py OPTA yoursketch.bin yoursketch.OTA
```

Finally, remember to update the path in the updater sketch.

## Resources

* [Arduino PLC IDE Setup & Device License
  Activation](https://opta.findernet.com/it/tutorial/plc-ide-setup-license)

## Contact

For communication reach out to <iot@dndg.it>.
