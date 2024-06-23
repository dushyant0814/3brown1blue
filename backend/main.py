import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from hume import HumeStreamClient
from hume.models.config import FaceConfig, LanguageConfig
import os 
from dotenv import load_dotenv
import tempfile
import time
import sys

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello world"}

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     client = HumeStreamClient(api_key=os.getenv("HUME_API_KEY"))
#     config = FaceConfig(identify_faces=True)
    
#     async with client.connect([config]) as socket:
#         while True:
#             data = await websocket.receive_text()
#             frame_data = base64.b64decode(data.split(",")[1])
            
#             result = await socket.send_file(frame_data)
#             await websocket.send_json(result)


# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     client = HumeStreamClient(api_key=os.getenv("HUME_API_KEY"))
#     config = FaceConfig(identify_faces=True)
    
#     async with client.connect([config]) as socket:
#         while True:
#             data = await websocket.receive_text()
#             frame_data = base64.b64decode(data.split(",")[1])
            
#             # Save frame data to a temporary file
#             with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#                 tmp_file.write(frame_data)
#                 tmp_file_path = tmp_file.name

#             try:
#                 result = await socket.send_file(tmp_file_path)
#                 await websocket.send_json(result)
#             finally:
#                 os.remove(tmp_file_path)



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client = HumeStreamClient(api_key=os.getenv("HUME_API_KEY"))
    # config = FaceConfig(identify_faces=True)
    config = LanguageConfig()
    
    async with client.connect([config]) as socket:
        try:
            while True:
                # data = await websocket.receive_text()
                image_bytes = await websocket.receive_text()    
                print(image_bytes)
                frame_data = base64.b64decode(image_bytes.split(",")[1])
                
                # Save frame data to a temporary file
                with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                    tmp_file.write(frame_data)
                    tmp_file_path = tmp_file.name

                try:
                    result = await socket.send_file(tmp_file_path)
                    print(result)
                    await websocket.send_json(result)
                finally:
                    os.remove(tmp_file_path)
                    time.sleep(0.1)

        except WebSocketDisconnect as e:
            print("WebSocket connection closed")
            print(f"Error: {e}", sys.exc_info())
        except Exception as e:
            print(f"Error: {e}", sys.exc_info())