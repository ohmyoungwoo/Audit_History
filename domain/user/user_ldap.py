import ldap

LDAP_URL="ldaps://lgesaads02.lge.net"

def ldap_initialize():
    connect = ldap.initialize(LDAP_URL)
    connect.set_option(ldap.OPT_REFERRALS, 0) # type: ignore
    connect.set_option(ldap.OPT_NETWORK_TIMEOUT, 5.0) # type: ignore
    connect.set_option(ldap.OPT_PROTOCOL_VERSION, 3) # type: ignore
    connect.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_ALLOW) # type: ignore
    connect.set_option(ldap.OPT_X_TLS_NEWCTX, 0) # type: ignore
    return connect

def ldap_search(usernames: list[str], connect=None):
    if connect is None:
        connect = ldap_initialize()
        connect.simple_bind_s("addhost", "1qaz2wsx")

    results = connect.search_s(
        "ou=LGE Users,dc=LGE,dc=NET",
        ldap.SCOPE_SUBTREE, # type: ignore
        f"(|{''.join([f'(name={username})' for username in usernames])})",
    )
    users = [ldap_parser(result[1]) for result in results]
    return users

"""
def ldap_search2(username: str, connect=None):
    if connect is None:
        connect = ldap_initialize()
        connect.simple_bind_s("addhost", "1qaz2wsx")

    result = connect.search_s(
        "ou=LGE Users,dc=LGE,dc=NET",
        ldap.SCOPE_SUBTREE, # type: ignore
        f"(name={username})",
    )
    return result
"""

def ldap_auth(username: str, password: str):
    connect = ldap_initialize()
    connect.simple_bind_s(username + "@lge.com", password)
    return ldap_search([username], connect)[0]
    #return ldap_search2(username, connect)

print(ldap_auth("myoungou.oh", "oh1554$$"))