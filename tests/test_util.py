import sys
sys.path.append('../')
import config

import pytest
from unittest.mock import patch, MagicMock
from utils.util import generate_fernet_key_from_env,encrypt_string,decrypt_string

@pytest.fixture
def test_encrypt_string():

    string = 'aaaaa'
    answer = b'gAAAAABncQrmFfS59VJV6ou2-snN96QixFqF2EPxRxyM7GX2yo_X3Mgtqaqaas_fkUcsN6s-ir6vEg9oBWKFxHbbkc4hNEy14A=='
    # テスト対象の関数を実行
    encrypted_string = encrypt_string(string, generate_fernet_key_from_env())
    assert encrypted_string == answer

def test_decrypt_string():
    encrypted_string = b'gAAAAABncQrmFfS59VJV6ou2-snN96QixFqF2EPxRxyM7GX2yo_X3Mgtqaqaas_fkUcsN6s-ir6vEg9oBWKFxHbbkc4hNEy14A=='
    answer = 'aaaaa'
    # テスト対象の関数を実行
    decrypted_string = decrypt_string(encrypted_string, generate_fernet_key_from_env())
    assert decrypted_string == answer