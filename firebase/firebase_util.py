import os
import sys
sys.path.append('../')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

class FirebaseUtil:
    
    #コンストラクタ
    def __init__(self)->None:
        self._db = self.init_firebase()
    
    #デストラクタ
    def __del__(self)->None:
        try:
            firebase_admin.delete_app(firebase_admin.get_app())
        except Exception as e:
            print(e)
    
    #接続されたDBオブジェクトを返却する関数
    def get_db(self)->firestore.client:
        return self._db
    
    #接続されたDBオブジェクトを返却する関数
    def init_firebase(self)->firestore.client:
        """_summary_

        Returns:
            firestore.client: _description_ Firestoreのクライアントオブジェクト
        """
        try:
            print("Initializing Firebase...")
            cred = credentials.Certificate(config.FIREBASE_CREDENTIALS_ABS_PATH)
            firebase_admin.initialize_app(cred)
            db = firestore.client()
            print("Firebase initialized successfully.")
            return db
        except Exception as e:
            print(f"Failed to initialize Firebase: {e}")
            return None

    #READ:全てのドキュメントを取得
    def read_all_documents(self, collection_name)->list[dict]:
        """_summary_

        Args:
            collection_name (_type_): _description_ コレクションの名前

        Returns:
            list[dict]: _description_ ドキュメントのリストデータ
        """
        try:
            a = self.get_db()
            print(a)
            collection_ref = self._db.collection(collection_name)
            print(11,collection_ref)
            documents = collection_ref.get()
            print(22,documents)
            data = [doc.to_dict() for doc in documents]
            return data
        except Exception as e:
            print(e)
            return None
    
    #READ:IDを使用して特定のドキュメントを取得
    def read_document_by_id(self, collection_name:str, document_id:str)->dict:
        """_summary_

        Args:
            collection_name (str): _description_ コレクションの名前
            document_id (str): _description_ ドキュメントのID

        Returns:
            dict: _description_ ドキュメントのデータ
        """
        try:
            data = self._db.collection(collection_name).document(document_id).get()
            return data.to_dict()
        except Exception as e:
            print(e)
            return None
        
    #READ:特定のキーに対応するドキュメントを検索して取得
    def read_documents_by_word(self, collection_name:str, key:str, word:str)->list[dict]:
        """_summary_

        Args:
            collection_name (str): _description_ コレクションの名前
            key (str): _description_ 検索するキー
            word (str): _description_ 検索する値

        Returns:
            list[dict]: _description_ ドキュメントのデータ
        """
        try:
            data = self._db.collection(collection_name).where(filter=firestore.FieldFilter(key, '==', word)).get()
            return [doc.to_dict() for doc in data]
        except Exception as e:
            print(e)
            return None
        
    #CREATE:ドキュメントを作成
    def create_document(self, collection_name:str,document_id:str,datum:dict)->bool:
        """_summary_

        Args:
            collection_name (str): _description_ コレクションの名前
            document_id (str): _description_ ドキュメントのID
            datum (dict): _description_ ドキュメントのデータ

        Returns:
            bool: _description_ 成功したかどうか
        """
        try:
            self._db.collection(collection_name).document(document_id).set(datum)
            print(f'Created document with ID: {document_id}')
            return True
        except Exception as e:
            print(e)
            return False
    
    #UPDATE:ドキュメントを更新
    def update_document(self, collection_name:str,document_id:str,key:str,value:dict)->bool:
        """_summary_

        Args:
            collection_name (str): _description_ コレクションの名前
            document_id (str): _description_ ドキュメントのID
            key (str): _description_ 更新するキー
            value (dict): _description_ 更新する値

        Returns:
            bool: _description_ 成功したかどうか
        """
        try:
            self._db.collection(collection_name).document(document_id).update({key: value})
            print(f'Updated document with ID: {document_id}')
            return True
        except Exception as e:
            print(e)
            return False
    
    def update_document_array(self, collecion_name: str, document_id: str, key: str, value: dict) -> bool:
        """_summary_

        Args:
            collecion_name (str): _description_ コレクションの名前
            document_id (str): _description_ ドキュメントのID
            key (str): _description_ 更新するキー
            value (dict): _description_ 更新する値

        Returns:
            bool: _description_
        """

        try:
            # Firestore の配列に辞書を直接追加
            self._db.collection(collecion_name).document(document_id).update({key: firestore.ArrayUnion([value])})
            print(f'Updated document with ID: {document_id}')
            return True
        except Exception as e:
            print(f"Error updating document: {e}")
            return False
        
    #DELETE:ドキュメントを削除
    def delete_document(self, collection_name:str,document_id:str)->bool:
        """_summary_

        Args:
            collection_name (str): _description_ コレクションの名前
            document_id (str): _description_ ドキュメントのID

        Returns:
            bool: _description_ 成功したかどうか
        """
        try:
            self._db.collection(collection_name).document(document_id).delete()
            print(f'Deleted document with ID: {document_id}')
            return True
        except Exception as e:
            print(e)
            return False

if __name__ == '__main__':
    fb = FirebaseUtil()
    data = fb.read_document_by_id(collection_name='userdata',document_id='VFOaSm9vLVlYYQ9qP7o')
    print(data)
    datum = {
        'name': 'test',
        'age': 20
    }
