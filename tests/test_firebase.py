import sys
sys.path.append('../')

import pytest
from unittest.mock import patch, MagicMock
from firebase_user import FirebaseUser  # クラス定義があるファイル名に置き換えてください

@pytest.fixture
@patch("firebase_util.FirebaseUtil")
def firebase_user(mock_firebase_util):
    # FirebaseUtilのモックを注入
    fb_util_instance = MagicMock()
    mock_firebase_util.return_value = fb_util_instance
    return FirebaseUser(), fb_util_instance

def test_create_user(firebase_user):
    fb_user, mock_util = firebase_user

    # モックの動作を設定
    mock_util.read_all_documents.return_value = []
    mock_util.create_document.return_value = True

    # ユーザーを作成
    result = fb_user.create_user("test_user", "test_password")

    # アサーション
    assert result is True
    mock_util.read_all_documents.assert_called_once_with(collection_name="userdata")
    mock_util.create_document.assert_called_once()

def test_create_user_duplicate(firebase_user):
    fb_user, mock_util = firebase_user

    # モックの動作を設定: 同じユーザー名のデータが既に存在する
    mock_util.read_all_documents.return_value = [{"username": "test_user"}]

    # ユーザーを作成
    result = fb_user.create_user("test_user", "test_password")

    # アサーション
    assert result is False
    mock_util.read_all_documents.assert_called_once_with(collection_name="userdata")
    mock_util.create_document.assert_not_called()

def test_read_user_by_username(firebase_user):
    fb_user, mock_util = firebase_user

    # モックの動作を設定
    mock_util.read_all_documents.return_value = [
        {"username": "user1", "id": "id1"},
        {"username": "test_user", "id": "id2"}
    ]

    # ユーザーを検索
    result = fb_user.read_user_by_username("test_user")

    # アサーション
    assert result == {"username": "test_user", "id": "id2"}
    mock_util.read_all_documents.assert_called_once_with(collection_name="userdata")

def test_add_play_data(firebase_user):
    fb_user, mock_util = firebase_user

    # モックの動作を設定
    mock_util.read_document_by_id.return_value = {
        "id": "test_id",
        "data": []
    }
    mock_util.update_document.return_value = True

    # プレイデータを追加
    result = fb_user.add_play_data("test_id", {"id": "play1"})

    # アサーション
    assert result is True
    mock_util.read_document_by_id.assert_called_once_with(
        collection_name="userdata", document_id="test_id"
    )
    mock_util.update_document.assert_called_once_with(
        collection_name="userdata", document_id="test_id", key="data", value={"id": "play1"}
    )

def test_delete_user(firebase_user):
    fb_user, mock_util = firebase_user

    # モックの動作を設定
    mock_util.delete_document.return_value = True

    # ユーザーを削除
    result = fb_user.delete_user("test_id")

    # アサーション
    assert result is True
    mock_util.delete_document.assert_called_once_with(
        collection_name="userdata", document_id="test_id"
    )