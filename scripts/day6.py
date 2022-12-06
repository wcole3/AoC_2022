"""
AoC 2022 Day 6 script
"""

# iterate over the input string and find the first occurrence of 4 unique characters
def find_start_packet(packet: str):
    # iterate over the string
    for i in range(len(packet)):
        # check if the next 4 characters are unique
        if len(set(packet[i:i+4])) == 4:
            return i+4, packet[i:i+4]
    return None

# same as above but find first 14 unique characters
def find_start_message(packet: str):
    # iterate over the string
    for i in range(len(packet)):
        # check if the next 4 characters are unique
        if len(set(packet[i:i+14])) == 14:
            return i+14, packet[i:i+14]
    return None

if __name__ == "__main__":
    print("Running AoC 2022 day 6")
    with open("../data/day6.txt", "r") as f:
        # read the file line by line
        for line in f.readlines():
            # get the packet
            packet = line.strip()
            # find the start of the packet
            start_idx, packet_str = find_start_packet(packet)
            if start_idx is not None:
                print(f"Start of packet: {start_idx}")
                print(f"Packet: {packet_str}")
            else:
                print("No packet found")
            # find the start of the message
            start_msg_idx, message_str = find_start_message(packet)
            if start_msg_idx is not None:
                print(f"Start of message: {start_msg_idx}")
                print(f"Message: {message_str}")
            else:
                print("No message found")