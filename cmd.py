import asyncio
import sys

import httpx

client = httpx.AsyncClient(http2=False)
api_url = "http://192.168.1.37"
headers = {
    "content-type": "application/json"
}
mission_list = []


async def set_flight_mode() -> None:
    mode_value = int(input("Provide mode number or inc: "))
    params = {
        "value": mode_value
    }
    try:
        r = await client.get(api_url + "/set_mode", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
            # print(response_json)
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def arm() -> None:
    params = {
        # "cmd": 1
    }
    try:
        r = await client.get(api_url + "/arm", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def disarm() -> None:
    params = {
        # "cmd": 0
    }
    try:
        r = await client.get(api_url + "/disarm", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def take_off() -> None:
    alt_value = int(input("Provide alt value or inc: "))
    params = {
        "alt": alt_value
    }
    try:
        r = await client.get(api_url + "/take_off", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def set_home() -> None:
    params = {}
    is_current_point = int(input("Do you want set home as current (1 [yes] | 0 [no]): "))
    if is_current_point == 1:
        params["lat"] = 0
        params["lon"] = 0
        params["current"] = 1
    else:
        lat = float(input("Please provide lat: "))
        lon = float(input("Please provide lon: "))
        params["lat"] = lat
        params["lon"] = lon
        params["current"] = 0
    try:
        r = await client.get(api_url + "/set_home", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def move_to_waypoint() -> None:
    lat = float(input("Provide lat: "))
    lon = float(input("Provide lon: "))
    alt = int(input("Provide alt value: "))
    params = {
        "lat": lat,
        "lon": lon,
        "alt": alt
    }
    try:
        r = await client.get(api_url + "/move_to_waypoint", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def land() -> None:
    params = {
        "cmd": 4
    }
    try:
        r = await client.get(api_url + "/land", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def mission_start() -> None:
    params = {
        "mission": 1
    }
    try:
        r = await client.get(api_url + "/", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def clear_all_missions() -> None:
    params = {
        "mission": 0
    }
    try:
        r = await client.get(api_url + "/", params=params, headers=headers)
        # response_json = r.json()
        print(r.status_code)
        if r.status_code >= 400:
            print("Status code is {status_code}".format(status_code=r.status_code))
        else:
            print("Command successfully sent via HTTP, ESP server responded...\n"
                  "Please view result in WS terminal")
            await root()
    except Exception as e:
        print("Where was an error during sending request\n")
        print(e)
    finally:
        pass


async def append_to_missions(lat: float, lon: float, alt: float, loiter_time: float) -> int:
    is_home = False
    if len(mission_list) == 0:
        is_home = True
    else:
        is_home = False
    mission_list.append({
        "id": len(mission_list) + 1,
        "order_index": len(mission_list),
        "is_home": is_home,
        "lat": lat,
        "lon": lon,
        "alt": alt,
        "loiter_time": loiter_time
    })
    return len(mission_list)


async def prepare_mission() -> None:
    print("There are {mission_item_count} mission items".format(mission_item_count=len(mission_list)))
    print("Add more (1) or continue (0)")
    s = int(input("Provide an option: "))
    if s == 1:
        lat = float(input("lat: "))
        lon = float(input("lon: "))
        alt = float(input("alt: "))
        loiter_time = int(input("loiter time: "))
        if lat is not None and lon is not None and alt is not None and loiter_time is not None:
            result = await append_to_missions(lat=lat, lon=lon, alt=alt, loiter_time=loiter_time)
            if result > 0:
                print("Mission item appended successfully.")
                await prepare_mission()
    elif s == 0:
        request_body = {
            "items": mission_list
        }
        try:
            r = await client.post(api_url + "/upload_mission", json=request_body, headers=headers)
            # response_json = r.json()
            print(r.status_code)
            if r.status_code >= 400:
                print("Status code is {status_code}".format(status_code=r.status_code))
                # print("Response is: ")
                # print(response_json)
            else:
                print("Command successfully sent via HTTP, ESP server responded...\n"
                      "Please view result in WS terminal")
                await root()
        except Exception as e:
            print("Something went wrong during making request...\n")
            print(e)
        finally:
            pass


async def root():
    cmd_val = input("A_D_O_R_A_M_U_S-> (Provide a command and hit return): ")
    parsed_cmd = "_".join(cmd_val.split()).lower()
    if parsed_cmd == "set_mode":
        await set_flight_mode()
    elif parsed_cmd == "arm":
        await arm()
    elif parsed_cmd == "disarm":
        await disarm()
    elif parsed_cmd == "takeoff":
        await take_off()
    elif parsed_cmd == "land":
        await land()
    elif parsed_cmd == "clear_missions":
        await clear_all_missions()
    elif parsed_cmd == "mission_start":
        await mission_start()
    elif parsed_cmd == "prepare_mission":
        await prepare_mission()
    else:
        print("Unknown or not implemented command\n"
              "Exiting system")
        sys.exit(0)


if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(join_platform_request())
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(root())
    except KeyboardInterrupt:
        pass
