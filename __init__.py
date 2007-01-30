import AccessControl.AuthEncoding
from AccessControl.AuthEncoding import _schemes

import logging
logger = logging.getLogger('SecurityInfo')

def pw_validate(reference, attempt):
    """Validate the provided password string, which uses LDAP-style encoding
    notation.  Reference is the correct password, attempt is clear text
    password attempt."""
    
    logger.warn("%s %s" % (reference, attempt))
    
    for id, prefix, scheme in _schemes:
        lp = len(prefix)
        if reference[:lp] == prefix:
            # a significant tweak to handle our pre-encoded passwords
            if attempt[:lp] == prefix:
                logger.warn("non-traditional")

                return reference == attempt
            else:
                return scheme.validate(reference[lp:], attempt)
    # Assume cleartext.
    return (reference == attempt)

AccessControl.AuthEncoding.pw_validate = pw_validate
