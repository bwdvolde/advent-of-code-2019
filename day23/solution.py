import threading
import time
from collections import defaultdict, deque

from intcode.intcode import VM, read_program

packet_queues = defaultdict(deque)
program = read_program("input.txt")
nat_package = None


def input_generator(network_address):
    packet_queue = packet_queues[network_address]

    yield network_address
    while True:
        if len(packet_queue):
            packet = packet_queue.popleft()
            x, y = packet
            yield x
            yield y
        else:
            yield -1


def start_network_interface_controller(network_address):
    global nat_package

    vm = VM(program)
    generator = input_generator(network_address)
    vm.set_input_generator(generator)

    while True:
        try:
            destination_address = vm.get_output()
            x = vm.get_output()
            y = vm.get_output()

            if destination_address == 255:
                if not nat_package:
                    print("Part 1:", y)
                nat_package = (x, y)
                # print("Package for NAT:", nat_package)
            else:
                packet_queues[destination_address].append((x, y))
        except StopIteration:
            print("VM with network address {} has stopped".format_map(network_address))
            break
        except Exception as e:
            print("Thread {}:  {}".format(network_addres, e))


def start_nat():
    print("NAT: starting...")
    vm = VM(program)
    vm.set_input(255)

    previous_delivery = None
    while True:
        try:
            if all([len(packet_queue) == 0 for packet_queue in packet_queues.values()]):
                print("Idle network...")
                if previous_delivery and previous_delivery[1] == nat_package[1]:
                    print("Part 2:", nat_package[1])
                    exit()
                print("Delivering:", nat_package)
                packet_queues[0].append(nat_package)
                previous_delivery = nat_package
            time.sleep(0.1)
        except StopIteration:
            print("NAT has stopped")
            break
        except Exception as e:
            print("NAT:  {}".format(e))


for network_addres in range(50):
    thread = threading.Thread(target=start_network_interface_controller, args=(network_addres,))
    thread.start()

thread = threading.Thread(target=start_nat, args=())
thread.start()
