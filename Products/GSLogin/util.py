import logging
logger = logging.getLogger()

def getDivisionObjects( context, user ):
    site_root = context.site_root()

    # if the user is an unverified member, they don't officially belong
    # to anything other than the unverified division until they
    # confirm their registration
    if user and 'unverified_member' in user.getGroups():
        division = getattr(site_root.Content, 'unverified', None)
        if division:
            return [division]
        return []
    
    objects = []
    for object_id in site_root.Content.objectIds(('Folder', 'Folder (Ordered)')):
        object = site_root.Content.restrictedTraverse(object_id, None)
        if object:
            try:
                if object.getProperty('is_division', 0):
                    objects.append(object)
            except:
                pass

    return objects

def getCurrentUserDivision( context, user ):
    curr_did = user.getProperty('currentDivision', '')
    
    division_objects = getDivisionObjects(context, user)
    division_ids = map(lambda x: x.getId(), division_objects)
    
    division_object = None
    # if we have a currentDivision, return the corresponding object
    if curr_did in division_ids:
        for obj in division_objects:
            if obj.getId() == curr_did:
                division_object = obj
                break
    
    # otherwise return the first division object, preferring non-public first
    elif division_objects:
        division_object = None
        for div_obj in division_objects:
            division_object = div_obj
            if not div_obj.getProperty('is_public', False):
                break
    
    # otherwise, well, not much we can do
    return division_object

def isGSUser( user ):
    try:
        cd = user.getProperty('currentDivision', None)
    except:
        cd = None
    
    if cd != None:
        return True
    return False
