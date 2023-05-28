import json
import time

from fastapi import FastAPI
from starlette.websockets import WebSocketDisconnect, WebSocket

from notifier import notifier

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    mavlink_message_id = None
    packet_type = None
    mode = None
    autopilot = None
    sys_status = None
    cmd_val = None
    cmd_progress = None
    cmd_result = None
    mission_ack_type = None
    mission_success = None
    gps_status_v = None
    gps_fix_type = 0
    satellites_visible = 0
    lat = 0
    lon = 0
    alt = 0
    vel = 0
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message_type = data_json["hb_t"]
            message_time_stamp = data_json["timestamp"] if "timestamp" in data_json else 0
            system_timestamp = time.time()
            if message_type is not None:
                mavlink_message_id = message_type
                if message_type == "MAVLINK_MSG_ID_HEARTBEAT":
                    packet_type = data_json["packet_type"]
                    mode = data_json["mode"]
                    autopilot = data_json["autopilot"]
                    sys_status = data_json["sys_status"]
                elif message_type == "MAVLINK_MSG_ID_COMMAND_ACK":
                    cmd_val = data_json["command"]
                    cmd_result = data_json["result"]
                    cmd_progress = data_json["progress"]
                elif message_type == "MAVLINK_MSG_ID_MISSION_ACK":
                    mission_ack_type = data_json["mission_ack_type"]
                    mission_success = data_json["success"]
                elif message_type == "MAVLINK_MSG_ID_GPS_RAW_INT":
                    print(data_json)
                    gps_status_v = data_json["gps_status_v"]
                    gps_fix_type = data_json["gps_fix_type"]
                    lat = data_json["lat"]
                    lon = data_json["lon"]
                    alt = data_json["alt"] if "alt" in data_json else None
                    satellites_visible = data_json["satellites_visible"] if "satellites_visible" in data_json else 0
                    vel = data_json["vel"] if "vel" in data_json else None

            print("|===================-----------> RECEIVED {system_timestamp} <-----------===================|\n"
                  "| MAVLINK_MESSAGE_ID: {mavlink_message_id} \n"
                  "| PACKET_TYPE: {packet_type}\n"
                  "| ----> FLIGHT MODE INFO: \n"
                  "| MODE: {mode} | AUTOPILOT: {autopilot} \n"
                  "| SYSTEM_STATUS: {sys_status} \n"
                  "| ----> CMD STATUS: \n"
                  "| COMMAND: {cmd_val} | PROGRESS: {cmd_progress} | RESULT: {cmd_result} \n"
                  "| ----> MISSION OPS STATUS: \n"
                  "| MISSION_ACK_TYPE: {mission_ack_type} |  SUCCESS: {mission_success} \n"
                  "| ----> GPS INFO: \n"
                  "| GPS_FIX_TYPE: {gps_status_v} - ({gps_fix_type}) | SATELLITES: {satellites_visible} \n"
                  "| LATITUDE: {lat} \n"
                  "| LONGITUDE: {lon}\n"
                  "| VEL: {gps_speed}\n"
                  "| ALT: {alt} \n"
                  "|==================-----------> END {message_timestamp} <-----------===================|\n"
                  .format(mavlink_message_id=mavlink_message_id, packet_type=packet_type, autopilot=autopilot,
                          sys_status=sys_status, cmd_val=cmd_val, cmd_progress=cmd_progress, cmd_result=cmd_result,
                          mission_ack_type=mission_ack_type, mission_success=mission_success, gps_status_v=gps_status_v,
                          satellites_visible=satellites_visible, gps_fix_type=gps_fix_type, lat=lat, lon=lon,
                          gps_speed=vel, alt=alt, message_timestamp=message_time_stamp,
                          system_timestamp=system_timestamp, mode=mode))
            # await websocket.send_text(f"Message text was: {data}")
            await websocket.send_text("Socket")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.on_event("startup")
async def startup():
    # await db_init()
    await notifier.generator.asend(None)
    print("SYS UP")
    # await client.start(bot_token=bot_token)
    # uvicorn.run("main:start_dg_listener")


@app.on_event("shutdown")
async def shut_down():
    print('POWER OFF')
    # await client.disconnect()
