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
    
    # if we have a currentDivision, return the corresponding object
    if curr_did in division_ids:
        for obj in division_objects:
            if obj.getId() == curr_did:
                return obj
    
    # otherwise return the first division object
    elif division_objects:
        return division_objects[0]
    
    # otherwise, well, not much we can do
    return None

def isGSUser( user ):
    try:
        cd = user.getProperty('currentDivision', None)
    except:
        cd = None
    
    if cd != None:
        return True
    return False
