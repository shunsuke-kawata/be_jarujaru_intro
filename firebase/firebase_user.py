import sys
import uuid
sys.path.append('../')

from firebase_util import FirebaseUtil

#FirebaseUtilクラスを使用してユーザー管理を行うクラス
class FirebaseUser:
    def __init__(self):
        self._fb_util = FirebaseUtil()
    
    #ユーザーを作成する関数
    def create_user(self, username:str, password:str)->bool:
        r_data = self.read_user_by_username(username)
        if r_data is not None:
            return False
        
        #ドキュメント管理用のユーザーIDを生成
        user_id = str(uuid.uuid4())
        #ユーザーデータの初期化
        init_user_data = {
            'id':user_id,
            'username' :username,
            'password': password,
            'data' : [],
        }
        
        return self._fb_util.create_document(collection_name='userdata',document_id=user_id, datum=init_user_data)
    
    def read_user_by_id(self, user_id:str)->dict:
        return self._fb_util.read_document_by_id(collection_name='userdata',document_id=user_id)
    
    #ユーザー名を使用してユーザー情報を取得する関数
    def read_user_by_username(self, username:str)->dict:
        r_data = self._fb_util.read_all_documents(collection_name='userdata')
        for datum in r_data:
            if datum['username'] == username:
                return datum
        return None
    
    def add_play_data(self, user_id:str, play_datum:dict)->bool:
        user_data = self._fb_util.read_document_by_id(collection_name='userdata',document_id=user_id)
        if user_data is None:
            return False
        
        return self._fb_util.update_document(collection_name='userdata',document_id=user_id,key='data',value=play_datum)

    def delete_user(self, user_id:str)->bool:
        return self._fb_util.delete_document(collection_name='userdata',document_id=user_id)

if __name__ == '__main__':
    fb_user = FirebaseUser()
    # print(fb_user.create_user('test_user','test_password'))
    print(fb_user.read_user_by_username('test_user'))
    # print(fb_user.add_play_data('f94040b5-4480-4912-9d6b-11d80bc2a444',{'id': 'aaaaaa', 'answer_array': [{'is_correct': True, 'id': 'id'}]}))
    print(fb_user.delete_user('f94040b5-4480-4912-9d6b-11d80bc2a444'))