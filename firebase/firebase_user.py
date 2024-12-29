import os
import sys
import uuid

sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firebase.firebase_util import FirebaseUtil

#FirebaseUtilクラスを使用してユーザー管理を行うクラス
class FirebaseUser:
    def __init__(self)->None:
        self._fb_util = FirebaseUtil()
    
    #ドキュメントのIDかユーザーネームを使用してユーザーが存在するか確認する関数
    def is_exist_user(self, identifier:str)->bool:
        r_data = self._fb_util.read_document_by_id(collection_name='userdata',document_id=identifier)
        if r_data is not None:
            return True
        r_data = self._fb_util.read_documents_by_word(collection_name='userdata',key='username',word=identifier)
        return r_data is not None and len(r_data)>0 
    
    #ユーザーを作成する関数
    def create_user(self, username:str, encrypted_password:str)->bool:
        
        is_exist = self.is_exist_user(username)
        if is_exist:
            return False
        
        #ドキュメント管理用のユーザーIDを生成
        user_id = str(uuid.uuid4())
        #ユーザーデータの初期化
        init_user_data = {
            'id':user_id,
            'username' :username,
            'encrypted_password': encrypted_password,
            'playdata' : [],
        }
        
        return self._fb_util.create_document(collection_name='userdata',document_id=user_id, datum=init_user_data)
    
    def read_all_users(self)->list[dict]:
        return self._fb_util.read_all_documents(collection_name='userdata')
    
    def read_user_by_id(self, user_id:str)->dict:
        return self._fb_util.read_document_by_id(collection_name='userdata',document_id=user_id)
    
    #ユーザー名を使用してユーザー情報を取得する関数
    def read_user_by_username(self, username:str)->dict:
        r_data = self._fb_util.read_documents_by_word(collection_name='userdata',key='username',word=username)
        if r_data is not None and len(r_data)>0:
            return r_data[0]
        return None
    
    def update_user(self, user_id:str, key:str, value:dict)->bool:
        return self._fb_util.update_document(collection_name='userdata',document_id=user_id,key=key,value=value)
    
    def add_play_data(self, user_id:str, play_datum:dict)->bool:
        user_data = self._fb_util.read_document_by_id(collection_name='userdata',document_id=user_id)
        if user_data is None:
            return False
        
        return self._fb_util.update_document(collection_name='userdata',document_id=user_id,key='data',value=play_datum)

    def delete_user(self, user_id:str)->bool:
        return self._fb_util.delete_document(collection_name='userdata',document_id=user_id)
    
if __name__ == '__main__':
    fb_user = FirebaseUser()
    print(fb_user.read_user_by_username('test_user'))
    print(fb_user.delete_user('f94040b5-4480-4912-9d6b-11d80bc2a444'))