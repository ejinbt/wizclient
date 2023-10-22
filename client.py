import asyncio
import time
from dataclasses import dataclass
from pywizlight import wizlight,PilotBuilder,discovery


@dataclass
class Light():
    name:str
    ip:str
    #brightness:int
    kelvin_range:tuple
    color_tmp_supported:bool
    brightness_supported:bool
    color_supported:bool
    effect:bool


class Client():
    @classmethod
    async def create(self,ip_range:str):
        self = Client()
        self.ip_range = ip_range
        self.devices = await discovery.discover_lights(broadcast_space=self.ip_range)
        ''' 
        self.lights = []
        for device in self.devices:
            device_type = await device.get_bulbtype()
            name = device_type.name
            ip = device.ip
            kelvin_range = (device_type.kelvin_range.min,device_type.kelvin_range.max) 
            color_tmp_supported = device_type.features.color_tmp
            brightness_supported = device_type.features.brightness
            color_supported = device_type.features.color
            effect = device_type.features.effect

            light = Light(name=name,ip=ip,kelvin_range=kelvin_range,color_tmp_supported=color_tmp_supported,brightness_supported=brightness_supported,color_supported=color_supported,effect=effect)
            self.lights.append(light)
        '''
        return self
    async def turn_on(self,ip):
        bulb = self.get_light(ip)
        if bulb:
            await bulb.turn_on(PilotBuilder())
    async def turn_off(self,ip):
        bulb = self.get_light(ip)
        if bulb:

            await bulb.turn_off()

    def list_devices(self):
        lights_ip = [x.ip for x in self.devices]
        return lights_ip
        
    async def change_brightness(self,value,ip):
        bulb =  self.get_light(ip)
        if bulb:
            await bulb.turn_on(PilotBuilder(brightness=value))
        else:
            return False
    async def get_features(self,ip):
        light = self.get_light(ip)
        light_type = await light.get_bulbtype()
        name = light_type.name
        kelvin_range = (light_type.kelvin_range.min,light_type.kelvin_range.max)
        color_tmp_supported = light_type.features.color_tmp
        brightness_supported = light_type.features.brightness
        color_supported = light_type.features.color
        effect = light_type.features.effect
        return name,kelvin_range,color_tmp_supported,brightness_supported,color_supported,effect

    async def update_state(self,ip):
        light = self.get_light(ip)
        state = await light.updateState()
        print(state.get_scene())

    def get_light(self,ip):
        for light in self.devices:
            if light.ip == ip:
                return light
        return None 
    
    async def change_color(self,ip:str,color:str):
        bulb = await self.get_device(ip)
        if bulb:
            print(color[0],color[1],color[2])
            await bulb.turn_on(PilotBuilder(color[0],color[1],color[2]))

    async def change_scene(self,ip:str,scene:int):
        light = self.get_light(ip)
        if light:
            await light.turn_on(PilotBuilder(scene=scene))
            await self.update_state(ip)
        else:
            print("Error occured")
            return False

async def wiz_run():
    bulbs = await discovery.discover_lights(broadcast_space="192.168.68.255")
    print(f"Bulb IP address: {bulbs[0].ip}")

    for bulb in bulbs:
        print(bulb.__dict__)
        await bulb.turn_on()
        time.sleep(5)
        # await bulb.turn_off()
