# BLEHub
A hub process run on Raspberry Pi to receive BLE signal

# How to run for development
`sudo python gattServer.py`

# Notes
- GATT server: BLE peripherals.
- GATT client: User's phone or in this case, the RBPi
- BLE peripherals (GATT Server) has only two states:
    - Connected:
        - Attached to a GATT client.
        - Cannot be discovered by other GATT clients
    - Waiting to be connected:
        - Boardcasting to all nearby GATT client.
        - Can be discovered by all GATT clients.
- To determine if a patient is leaving his/her assigned room:
    - If the corresponding RBPi lost the signal from the peripherals for the next x(5) scanning rounds. Send alerting info "LOST POSITIVE" to the cloud server.
    - AND, other RBPi discovered this braceletfor the next x scanning rounds. Send "FOUND NEGATIVE" to the cloud server.
    - On the cloud server, if received both "LOST POSITIVE" and "FOUND NEGATIVE" on the same bracelet. Send alert to doctors to informing patient is leaving the room.
- To determine if a patient's bracelet is out of battery:
    - If the corresponding RBPi lost he signal for the next x scanning rounds. Send "LOST POSITIVE".
    - On the cloud server, if received only "LOST POSITIVE" twice, informing the doctors that the patient's bracelet is out of battery.
- To determine the coarse-location.
    - If the patient is leaving the room:
        - Other RBPi's would discover it and report "FOUND NEGATIVE". Use this info to determine the location.
    - Else. The patient is located in the room.
- Two approaches to implement this:
    - One websocket channel handles one nursing home.
        - won't touch the database.
    - Communicate with the database.
        - Evertime a request is comming in: determine if the bracelet is:
            - Leaving the room
            - Out of battery.
        - Table schema:
            - bracelet_id
            - patient_id
            - nursing_home_id
            - room_id
            - assigned
            - lost_found
            - pos_neg
        - Alert will be sent through websocket and email.
