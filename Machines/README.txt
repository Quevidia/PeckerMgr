DO NOT TOUCH ANY OF THE MACHINES UNLESS YOU HAVE READ BELOW AND YOU KNOW WHAT YOU ARE DOING.

PECKERMGR, MADE BY QUEVIDIA

----------------------------------------------------------------------------------------------------------------------------------

Welcome to the machines folder. As you can see, each CPU architecture, machine and hardware are all organised in directories and .cfg files, rather than just making a list of CPU architectures, machine and hardware in the scripts of PeckerMgr, Here's how everything is sorted.

PeckerMgr
---> Machines (you are here)
--------> CPU architecture (ARM for example)
-------------> Machine 1
----------------------------> config.cfg (see point 1)
-------------> Machine 2
----------------------------> config.cfg (see point 1)
-------------> Machine 3
----------------------------> config.cfg (see point 1)
-------------> config.cfg (see point 2)

----------------------------------------------------------------------------------------------------------------------------------

Point 1: This configuration file is intended for listing the name for the machine that QEMU uses. These values aren't case-sensitive.

----------------------------------------------------------------------------------------------------------------------------------

Point 2: This configuration file is intended for listing the QEMU application name, without the "qemu-system-" bit. For example, for ARM you may use "Arch=aarch64;". If adding a new QEMU application and a 64-bit emulation option is available, opt for the 64-bit architecture. This also specifies all necessary hardware. The following must be in the configuration file otherwise PeckerMgr will fail to load:

CPU=
Network=
Video=
Sound=
Accel=

Due to how QEMU works, all of these values have to be case-sensitive and must be spelled correctly. Some devices may have to be specified even further. To specify the model of the device with QEMU's ",model=" parameter, specify ":-:" and then the model name. To include a separate device to be used with the device being specified, include " - ". In order to get the values for each option, you can do -cpu/-accel ? for the CPU= and Accel= options, and you will want to use -device ? and look for all network, video and sound devices to specify. Device models and additional devices to be bundled with another will have to be researched further on the internet.

If you are specifying CPUs with the CPU= variable, you do not need to add quotes around each CPU - whether they have any spaces or not - since PeckerMgr appends quotes automatically. If you do qemu-system-arch -cpu ? and the CPU listing looks something like this:

arch THIS_IS_CPU_1 IO 123456789
arch          CPU2 IO 123456789
arch     NOT_CPU_3 IO 123456789

Do not specify both the arch and the specifications AFTER the CPU name, otherwise QEMU will not launch properly when using any of the CPUs you have specified.

----------------------------------------------------------------------------------------------------------------------------------

General rules for modifying configuration files:

Always end a statement with a syntax point (;). For example, "CPU=QEMU;".

When adding variables, never add spaces between variable name and the equal sign. Always stick to simply doing "VARIABLENAME=".

If adding multiple options to a variable, should you be modifying an existent machine configuration, use commas. DO NOT SPACE EACH OPTION OUT UNLESS THERE ARE SPACES IN THE OPTION'S NAME. For example, "CPU=QEMU,Max;"