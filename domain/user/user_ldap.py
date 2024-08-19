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

def ldap_search(usernames: list[str], connect=None):
    if connect is None:
        connect = ldap_initialize()
        connect.simple_bind_s("addhost", "1qaz2wsx")

    results = connect.search_s(
        "ou=LGE Users,dc=LGE,dc=NET",
        ldap.SCOPE_SUBTREE, # type: ignore
        f"(|{''.join([f'(name={username})' for username in usernames])})",
    )
    
    users = [ldap_parser(result[1]) for result in results] # type: ignore
    return users

def ldap_auth(username: str, password: str):
    connect = ldap_initialize()
    connect.simple_bind_s(username + "@lge.com", password)
    return ldap_search([username], connect)[0]

#print(ldap_auth("myoungou.oh", "oh1554$$")['username'])
#print(ldap_auth("myoungou.oh", "oh1554$$"))