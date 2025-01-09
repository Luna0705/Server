import asyncio
import websockets
import os
import json
PORT = int(os.getenv("PORT", 8080))
clients = set()
rooms=dict()
log=dict()

prooms = dict()

def add_player(room_name, player_name):
    if room_name not in prooms:
        prooms[room_name] = []  
    if player_name not in prooms[room_name]:
        prooms[room_name].append(player_name) 
    else:
        print(f"{player_name} is already in {room_name}.")
def remove_player(room_name, player_name):
    if room_name in prooms and player_name in prooms[room_name]:
        prooms[room_name].remove(player_name)  
    else:
        print(f"{player_name} is not in {room_name}.")
async def handle_connection(websocket):
    print("New client connected")
    clients.add(websocket)
    try:
        async for message in websocket:
            #print(message)
            data=json.loads(message)
            action = data['action']
            if action=='createroom':
                #print(data)
                rooms[data['roomname']] = {'Capacity': data['Capacity'], 'fcap': 0} 
            if action=='r':
                for room, info in rooms.items():
                    rd = {  
                            'a':1,
                            'r': room,
                            'c': info['Capacity'],
                            'f': info['fcap']
                        }
                    for client in clients:
                        await client.send(json.dumps(rd))

                    #print(json.dumps(rd))
            if action=='selectroom':
                room=rooms[data['roomname']]
                add_player(data['roomname'],data['player'])
                dat=prooms[data['roomname']]
                print(dat)
                rd = {'a':3,'roomID':data['roomname']}
                for client in clients:
                        await client.send(json.dumps(rd))
                rd = {  
                        'a':2,
                        'p': dat,
                        'roomID':data['roomname']
                    }
                for client in clients:
                    await client.send(json.dumps(rd))
                room['fcap']+=1
            if action=='exitroom':
                room=rooms[data['roomname']]
                remove_player(data['roomname'],data['player'])
                dat=prooms[data['roomname']]
                print(dat)
                rd = {'a':3,'roomID':data['roomname']}
                for client in clients:
                        await client.send(json.dumps(rd))
                rd = {  
                        'a':2,
                        'p': dat,
                        'roomID':data['roomname']
                    }
                for client in clients:
                    await client.send(json.dumps(rd))
                room['fcap']-=1
            if action=='opensesame':
                log[websocket]=data['name']
                #print(log)
            if action=='p':
                dat=prooms[data['roomname']]
                for info in dat:
                    rd = {  
                            'a':2,
                            'p': info
                        }
                    for client in clients:
                        await client.send(json.dumps(rd))
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Client disconnected: {e}")
    finally:
        print(f"Client disconnected:{log[websocket]}")
        clients.remove(websocket)
        log.pop(websocket)

async def main():
    print(f"WebSocket server is running on ws://localhost:{PORT}")
    async with websockets.serve(handle_connection, "localhost", PORT):
        await asyncio.Future()  

if __name__ == "__main__":
    asyncio.run(main())
    
