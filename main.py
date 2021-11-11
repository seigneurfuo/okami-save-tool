#!/usr/bin/env python3

# Original author:
# Author: seigneurfuo
# Creation date: 2021.11.11
# Latest modification date: 2021.11.11

# This script is a Python port of this one: https://github.com/Shintensu/Okami-HD-speed/tree/master/C%2B%2B%20Code/OkamiSaveFileSlicerAndMerger
# It allow to split Okami save file as saveslots and merge saveslots to a save file
import copy
import os
import sys
import argparse

from hashlib import md5

save_file_filename = "OKAMI"
save_slot_folder = "SaveSlots"
saveSlotString = "SaveSlot"

class SaveSlot:
    size = 0x1729F + 1
    empty_hash = "f2c67259f08ffd35d3a56a6935c19fa9"
    data = None
    hash = None
    copied_from_slot = None

    def __init__(self):
        pass

    def __repr__(self):
        return "Hash: {}".format(self.get_hash())

    def get_data(self, save_file):
        pass

    def get_hash(self):
        return md5(self.data).hexdigest()

    def is_empty(self):
        return True if self.get_hash() == self.empty_hash else False

    def write_to_file(self):
        pass

    def load_from_file(self):
        pass


class SaveFile:
    filename = "OKAMI"
    save_slot_count = 30
    slots = []
    size = SaveSlot.size * save_slot_count

    def __init__(self):
        pass

    def read(self, filename=None):
        if filename:
            self.filename = filename

        if not os.path.isfile(self.filename):
            msg = "Invalid file size or non existing file: {}".format(self.filename)
            print(msg)
            # TODO: Error

        else:
            with open(save_file_filename, "rb") as save_file:
                # TODO: Checksize ?

                for slot_id in range(0, self.save_slot_count):
                    save_file.seek((SaveSlot.size * slot_id))

                    save_slot = SaveSlot()
                    buffer = save_file.read(SaveSlot.size)
                    save_slot.data = buffer
                    self.slots.append(save_slot)

    def write(self, filename=None, backup=True):
        if filename:
            self.filename = filename

        with open(self.filename, "wb") as save_file:
            for slot in self.slots:
                save_file.write(slot.data)

        msg = "Writing {}".format(self.filename)
        print(msg)


    def list_slots(self):
        hash_list = []
        for slot_index, slot in enumerate(self.slots):
            hash = slot.get_hash()

            if hash in hash_list:
                state_string = "not unique"
            else:
                state_string = "unique"

            if slot.is_empty():
                state_string += " - empty"

            if slot.copied_from_slot:
                state_string += " - (copied from slot: {})".format(slot.copied_from_slot)

            msg = "Slot {slot}\t\t MD5: {hash} \t\t{existing_string}".format(slot=slot_index + 1, hash=hash, existing_string=state_string)
            print(msg)

            if (slot_index +1) % 5 == 0: print()

            hash_list.append(hash)


    def split_save_file(self):
        pass

    def move_slot(self, slot_id, new_slot):
        if slot_id == 0 and slot_id >= self.save_slot_count and new_slot == 0 and new_slot >= self.save_slot_count:
            # TODO: Error
            pass

        # Moving current slot to position
        self.slots.insert(new_slot - 1, self.slots.pop(slot_id - 1))


    def copy_slot(self, slot_id, new_slot):
        if slot_id == 0 and slot_id > self.save_slot_count and new_slot == 0 and new_slot > self.save_slot_count:
            # TODO: Error
            pass

        slot = copy.copy(self.slots[slot_id - 1])
        slot.copied_from_slot = slot_id
        self.slots[new_slot - 1] = slot

        hash = slot.get_hash()
        msg = "Slot {slot} [{hash}] copied to slot {new_slot}".format(slot=slot_id, new_slot=new_slot, hash=hash)
        print(msg)

    # Dont Work
    def clear_slot(self, slot_id):
        slot = self.slots[slot_id -1]
        slot.data = bytes(SaveSlot.size) # Create 0x00 data


    def set_save_slot_data(self):
        pass

    def merge_save_slots(self):
        # TODO: Check save file size + if file exists ?

        save_file = open(save_file_filename, "wb")

        for slot_id in range(0, self.save_slot_count):
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
    argument_parser = argparse.ArgumentParser(description="Okami Save Tool")
    argument_parser.add_argument("filename", help="")

    argument_parser.add_argument("--from", help="")
    argument_parser.add_argument("--to", help="")


    actions_group = argument_parser.add_mutually_exclusive_group()
    actions_group.add_argument("--list", action="store_true", required=False, help="Display the list of slots")


    actions_group.add_argument("--copy")
    actions_group.add_argument("--move")
    actions_group.add_argument("--extract-slots", help="Extract each slot file", action="store_true")

    args = argument_parser.parse_args()

    save_file = SaveFile()

    if args.filename:
        save_file.read(args.filename)

    if args.list:
        save_file.list_slots()

    elif args.copy:
        print(args.copy)
        #save_file.copy_slot()

    elif args.move:
        print(args.move)
        #save_file.move_slot()

    else:
        argument_parser.print_help(sys.stderr)



if __name__ == "__main__":
    main()
