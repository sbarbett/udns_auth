# USAGE.md

## Table of Contents
- [Create Domain (`create_domain.py`)](#create_domain\.py)
- [Delete Domains (`delete_domains.py`)](#delete_domains\.py)
- [Update RRSET (`update_rrset_put.py`)](#update_rrset_put\.py)

---

### create_domain.py

This script creates a domain with associated A and CNAME records. 

**Usage**:

```
python create_domain.py [DOMAIN] -u [USERNAME] -p [PASSWORD]
```

**Arguments**:
- `DOMAIN`: The domain name you want to create.
- `-u`: Your username.
- `-p`: Your password.

**Example**:

```
python create_domain.py example.com -u myUsername -p myPassword
```

---

### delete_domains.py

This script deletes a specified domain.

**Usage**:

```
python delete_domains.py [DOMAIN] -u [USERNAME] -p [PASSWORD]
```

**Arguments**:
- `DOMAIN`: The domain name you want to delete.
- `-u`: Your username.
- `-p`: Your password.

**Example**:

```
python delete_domains.py example.com -u myUsername -p myPassword
```

---

### update_rrset_put.py

This script updates a the A record for a specified domain. If you used the create script, it will naturally update the A
record for the domain you created from 192.0.2.1 to 192.0.2.2 and up the TTL from 300 to 600.

**Usage**:

```
python update_rrset_put.py [DOMAIN] -u [USERNAME] -p [PASSWORD]
```

**Arguments**:
- `DOMAIN`: The domain name you want to update.
- `-u`: Your username.
- `-p`: Your password.

**Example**:

```
python update_rrset_put.py example.com -u myUsername -p myPassword
```
