import os
import sys
from typing import List
sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import APIRouter,status,Query
import json
from fastapi.responses import JSONResponse
from firebase.firebase_user import FirebaseUser

# エンドポイントの作成
users_endpoint = APIRouter()

#GET:全てのユーザを取得
@users_endpoint.get("/users", tags=["users"])
async def get_all_users(skip: int = Query(0), limit: int = Query(10)):
    try: 
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        print(firebase_user)
        
        # ユーザ情報を取得
        users = firebase_user.read_all_users()
        print(users)
        return JSONResponse(status_code=status.HTTP_200_OK,content=users[skip:skip+limit])
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})

#GET:IDを使用してユーザを取得
@users_endpoint.get("/users/{user_id}", tags=["users"])
async def get_user_by_id(user_id:str):
    try:
        if not user_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"User ID is required"})
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # ユーザ情報を取得
        user = firebase_user.read_user_by_id(user_id)
        return JSONResponse(status_code=status.HTTP_200_OK,content=user)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})
#GET:ユーザ名を使用してユーザを取得
@users_endpoint.get("/users/username/{username}", tags=["users"])
async def get_user_by_username(username:str):
    try:
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # ユーザ情報を取得
        user = firebase_user.read_user_by_username(username)
        
        if user is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"User not found"})
        
        return JSONResponse(status_code=status.HTTP_200_OK,content=user)
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})

#POST:ユーザを作成
@users_endpoint.post("/users", tags=["users"])
async def create_user(username:str,password:str):
    try:
        if not username or not password:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"Username and password are required"})
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # ユーザを作成
        result = firebase_user.create_user(username,password)
        if result:
            return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"User created successfully"})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"Failed to create user"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})
    
#PUT:ユーザを更新
@users_endpoint.put("/users/{user_id}", tags=["users"])
async def update_user(user_id:str,username:str,password:str):
    try:
        if not user_id or not username or not password:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"User ID, username and password are required"})
        
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # ユーザを更新
        result = firebase_user.update_user(user_id,username,password)
        if result:
            return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"User updated successfully"})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"Failed to update user"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})

#DELETE:ユーザを削除
@users_endpoint.delete("/users/{user_id}", tags=["users"])
async def delete_user(user_id:str):
    try:
        if not user_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"User ID is required"})
        
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # ユーザを削除
        result = firebase_user.delete_user(user_id)
        if result:
            return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"User deleted successfully"})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"Failed to delete user"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})
    
#GET:プレイデータを取得
@users_endpoint.get("/users/{user_id}/playdata", tags=["users"])
async def get_play_data(user_id:str):
    try:
        if not user_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"User ID is required"})
        
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # プレイデータを取得
        user = firebase_user.read_user_by_id(user_id)
        if user is None:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,content={"message":"User not found"})
        
        return JSONResponse(status_code=status.HTTP_200_OK,content=user.get('playdata',[]))
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})

#POST:プレイデータを追加
@users_endpoint.post("/users/{user_id}/playdata", tags=["users"])
async def add_play_data(user_id:str,play_datum:dict):
    try:
            
        if not user_id or not play_datum:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"User ID and play data are required"})
        
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # プレイデータを追加
        result = firebase_user.add_play_data(user_id,play_datum)
        if result:
            return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"Play data added successfully"})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"Failed to add play data"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})

#DELETE:プレイデータを削除
@users_endpoint.delete("/users/{user_id}/playdata", tags=["users"])
async def delete_play_data(user_id:str):
    try:
        if not user_id:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"message":"User ID is required"})
        
        # FirebaseUserクラスのインスタンスを生成
        firebase_user = FirebaseUser()
        
        # プレイデータを削除
        result = firebase_user.update_user(user_id,'playdata',[])
        if result:
            return JSONResponse(status_code=status.HTTP_200_OK,content={"message":"Play data deleted successfully"})
        else:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":"Failed to delete play data"})
    except Exception as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,content={"message":str(e)})
    