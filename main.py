#!/usr/bin/env python3

# Original author:
# Author: seigneurfuo
# Creation date: 2021.11.11
# Latest modification date: 2021.11.11

# This script is a Python port of this one: https://github.com/Shintensu/Okami-HD-speed/tree/master/C%2B%2B%20Code/OkamiSaveFileSlicerAndMerger
# It allow to split Okami save file as saveslots and merge saveslots to a save file

import sys
import os
from hashlib import md5

save_file_filename = "OKAMI"
save_slot_folder = "SaveSlots"
saveSlotString = "SaveSlot"

save_slot_count = 30
save_slot_size = 0x1729F + 1
saveFileSize = save_slot_size * save_slot_count


def split_save_file():
    # TODO: Check save file size + if file exists ?
    size_ok = True

    if not os.path.isfile(save_file_filename):
        msg = "Invalid file size or non existing file: {}".format(save_file_filename)
        print(msg)

    elif size_ok:
        if not os.path.isdir(save_slot_folder):
            os.makedirs(save_slot_folder)

        save_file = open(save_file_filename, "rb")

        for slot_id in range(0, save_slot_count):
            save_slot_filename = os.path.join(save_slot_folder, saveSlotString + str(slot_id + 1))
            save_slot_file = open(save_slot_filename, "wb")

            save_file.seek((save_slot_size * slot_id))
            buffer = save_file.read(save_slot_size)
            save_slot_file.write(buffer)

            save_slot_file.close()

            hash = md5(buffer).hexdigest()
            msg = "Writing: {} \tMD5: [{}]".format(save_slot_filename, hash)
            print(msg)

        save_file.close()

    else:
        print("Invalid file size or non existing file !")


def merge_save_slots():
    # TODO: Check save file size + if file exists ?

    save_file = open(save_file_filename, "wb")

    for slot_id in range(0, save_slot_count):
        save_slot_filename = os.path.join(save_slot_folder, saveSlotString + str(slot_id + 1))

        save_slot_file = open(save_slot_filename, "rb")
        buffer = save_slot_file.read(save_slot_size)

        hash = md5(buffer).hexdigest()
        msg = "Reading: {} \tMD5: [{}]".format(save_slot_filename, hash)
        print(msg)

        save_file.write(buffer)
        save_slot_file.close()

    save_file.close()

    msg = "\nWrinting save file: {}".format(save_file_filename)
    print(msg)


def main():
    # TODO: Argsparser
    if len(sys.argv) == 2 and sys.argv[1] == "split":
        split_save_file()

    elif len(sys.argv) == 2 and sys.argv[1] == "merge":
        merge_save_slots()

    else:
        usage = f"""
    {sys.argv[0]} split: 
    {sys.argv[0]} merge: 
        """
        print(usage)


if __name__ == "__main__":
    main()
