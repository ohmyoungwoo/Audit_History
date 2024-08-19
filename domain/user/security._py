import hashlib
import hmac
import json
import ldap
import bcrypt
from jose import jwe
from math import ceil

# from app.core.config import settings
from app.core.config import cp_settings, settings

hash_len = 32


def hmac_sha256(key, data):
    return hmac.new(key, data, hashlib.sha256).digest()


def hkdf(length: int, ikm, salt: bytes = b"", info: bytes = b"") -> bytes:
    if len(salt) == 0:
        salt = bytes([0] * hash_len)
    prk = hmac_sha256(salt, ikm)
    t = b""
    okm = b""
    for i in range(ceil(length / hash_len)):
        t = hmac_sha256(prk, t + info + bytes([1 + i]))
        okm += t
    return okm[:length]


def decrypt_token(token: str):
    key = hkdf(hash_len, settings.JWT_SECRET, "", b"NextAuth.js Generated Encryption Key")
    decrypt_token = jwe.decrypt(token, key)
    return json.loads(decrypt_token.decode())


# def ldap_auth(username: str, password: str):
#     l = ldap.initialize(settings.LDAP_URL)
#     l.set_option(ldap.OPT_NETWORK_TIMEOUT, 3.0)
#     l.simple_bind_s(username + "@lge.com", password)
#     l_search = l.search(
#         "dc=LGE,dc=NET", ldap.SCOPE_SUBTREE, f"(sAMAccountName={username})"
#     )
#     result_status, result_data = l.result(l_search, 0)

#     res = result_data[0][1]
#     dn = res["distinguishedName"][0].decode()
#     ldap_res = {
#         "username": username,
#         "password": get_password_hash(password),
#         "name": res["description"][0].decode(),
#         "en_name": res["displayNamePrintable"][0].decode()
#         if "displayNamePrintable" in res
#         else res["description"][0].decode(),
#         "title": res["title"][0].decode(),
#         "employeeNumber": res["employeeNumber"][0].decode()
#         if "employeeNumber" in res
#         else None,
#         "department": res["department"][0].decode(),
#         "office": res["physicalDeliveryOfficeName"][0].decode(),
#         "mobile": res["mobile"][0].decode(),
#         "is_staff": "306507" in dn,
#     }
#     return ldap_res

def ldap_initialize():
    connect = ldap.initialize(settings.LDAP_URL)
    connect.set_option(ldap.OPT_REFERRALS, 0)
    connect.set_option(ldap.OPT_NETWORK_TIMEOUT, 5.0)
    connect.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
    connect.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW)
    connect.set_option(ldap.OPT_X_TLS_NEWCTX, 0)
    return connect


def ldap_auth(username: str, password: str):
    l = ldap_initialize()
    l.simple_bind_s(username + "@lge.com", password)
    return ldap_search([username], l)[0]


def ldap_search(usernames: list[str], connect=None):
    if connect is None:
        connect = ldap_initialize()
        connect.simple_bind_s("addhost", "1qaz2wsx")

    results = connect.search_s(
        "ou=LGE Users,dc=LGE,dc=NET",
        ldap.SCOPE_SUBTREE,
        f"(|{''.join([f'(name={username})' for username in usernames])})",
    )
    users = [ldap_parser(result[1]) for result in results]
    return users

def ldap_parser(data):
    dn = data["distinguishedName"][0].decode()
    res = {
        "username": data["cn"][0].decode(),
        "password": "",
        "name": data["description"][0].decode(),
        "en_name": data["displayNamePrintable"][0].decode()
        if "displayNamePrintable" in data
        else data["description"][0].decode(),
        "title": data["title"][0].decode(),
        "employeeNumber": data["employeeNumber"][0].decode() if "employeeNumber" in data else None,
        "department": data["department"][0].decode(),
        "office": data["physicalDeliveryOfficeName"][0].decode(),
        "mobile": data["mobile"][0].decode(),
        "is_staff": "306507" in dn,
    }
    return res

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def get_password_hash(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
