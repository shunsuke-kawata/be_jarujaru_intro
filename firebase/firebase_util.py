import sys
sys.path.append('../')
import config
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

class FirebaseUtil:
    def __init__(self):
        self._db = self.init_firebase()
    
    #接続されたDBオブジェクトを返却する関数
    def init_firebase(self)->firestore.client:
        try:
            cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            return db
        except Exception as e:
            return None

    #READ:全てのドキュメントを取得
    def read_all_documents(self, collection_name)->dict:
        try:
            collection_ref = self._db.collection(collection_name)
            documents = collection_ref.get()
            data = [doc.to_dict() for doc in documents]
            return data
        except Exception as e:
            print(e)
            return None
    
    #READ:IDを使用して特定のドキュメントを取得
    def read_document_by_id(self, collection_name:str, document_id:str)->dict:
        try:
            data = self._db.collection(collection_name).document(document_id).get()
            return data.to_dict()
        except Exception as e:
            print(e)
            return None
    
    #CREATE:ドキュメントを作成
    def create_document(self, collection_name:str,document_id:str,datum:dict)->bool:
        try:
            self._db.collection(collection_name).document(document_id).set(datum)
            print(f'Created document with ID: {document_id}')
            return True
        except Exception as e:
            print(e)
            return False
    
    #UPDATE:ドキュメントを更新
    def update_document(self, collection_name:str,document_id:str,key:str,value:dict)->bool:
        try:
            self._db.collection(collection_name).document(document_id).update({key: value})
            print(f'Updated document with ID: {document_id}')
            return True
        except Exception as e:
            print(e)
            return False

    #DELETE:ドキュメントを削除
    def delete_document(self, collection_name:str,document_id:str)->bool:
        try:
            self._db.collection(collection_name).document(document_id).delete()
            print(f'Deleted document with ID: {document_id}')
            return True
        except Exception as e:
            print(e)
            return False

'''
実際にアプリからFirebaseUtilを使うときに使用する関数
''' 

if __name__ == '__main__':
    fb = FirebaseUtil()
    data = fb.read_document_by_id(collection_name='userdata',document_id='VFOaSm9vLVlYYQ9qP7o')
    print(data)
    datum = {
        'name': 'test',
        'age': 20
    }
    # fb.add_datum_to_collection('users', datum)
    # data = fb.get_all_collection_data('users')
    # for d in data:
    #     print(d.to_dict())