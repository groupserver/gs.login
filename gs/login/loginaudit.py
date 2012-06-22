# coding=utf-8
"""The audit-trails component for login

CONSTANTS
    SUBSYSTEM: 'groupserver.Login' (*Must* be the same as the factory 
        named in the ZCML configuration.)
    UNKNOWN:     '0' (*String*)
    LOGIN:       '1' (*String*)
    LOGOUT:      '2' (*String*)
    BADPASSWORD: '3' (*String*)
    BADUSERID:   '4' (*String*)
"""
from pytz import UTC
from datetime import datetime
from xml.sax.saxutils import escape as xml_escape
from base64 import b64decode
from zope.component import createObject
from zope.component.interfaces import IFactory
from zope.interface import implements, implementedBy
from Products.CustomUserFolder.interfaces import IGSUserInfo
from Products.CustomUserFolder.userinfo import userInfo_to_anchor
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent, \
  AuditQuery, event_id_from_data
from Products.XWFCore.XWFUtils import munge_date

# Create a logger for this audit-trail component that dumps 
SUBSYSTEM = 'groupserver.Login'
import logging
log = logging.getLogger(SUBSYSTEM) #@UndefinedVariable

UNKNOWN        = '0'  # Unknown is always "0"
LOGIN          = '1'
LOGOUT         = '2'
BADPASSWORD    = '3'
BADUSERID      = '4'

class LoginAuditEventFactory(object):
    """A Factory for login events
    
    DESCRIPTION
        An instantiated factory creates instances of *things*. In 
        this case, it creates events relating to login. The 
        factory itself is instantiated in two ways. First, the
        auditor for this subsystem (see LoginAuditor below) creates
        a factory so it can log events. Second, the Zope 3
        "createObject" utility instantiates the factory in order to
        create events for displaying. The event factory is a named
        factory because of the latter use.
    """
    implements(IFactory)

    title=u'GroupServer Login Audit Event Factory'
    description=u'Creates a GroupServer audit event for login'

    def __call__(self, context, event_id,  code, date,
        userInfo, instanceUserInfo,  siteInfo,  groupInfo = None,
        instanceDatum='', supplementaryDatum='', subsystem=''):
        """Create an event
        
        DESCRIPTION
            The factory is called to create event instances. It
            expects all the arguments that are required to create an
            event instance, though it ignores some. The arguments to
            this method *must* be the same for *all* event
            factories, no matter the subsystem, and the argument 
            names *must* match the fields returned by the 
            getter-methods of the audit trail query.
            
        ARGUMENTS
            context
                The context used to create the event.
                
            event_id
                The identifier for the event.
                
            code
                The code used to determine the event that is 
                instantiated.
                
            date
                The date the event occurred.
                
            userInfo
                The user who caused the event. Always set for 
                login events.
                
            instanceUserInfo
                The user who had an event occurred to them. Always
                set for login events.
                
            siteInfo
                The site where the event occurred. Always set for
                login events.
                
            groupInfo
                The group where the event occurred. Can be None.
                
            instanceDatum
                Data about the event. Can be ''.
                
            supplementaryDatum
                More data about the event. Can be ''.
                
            subsystem
                The subsystem (should be this one).
        RETURNS
            An event, that conforms to the IAuditEvent interface.
            
        SIDE EFFECTS
            None
        """
        assert subsystem == SUBSYSTEM, 'Subsystems do not match'
        
        # The process of picking the class used to create an event
        #   not a pretty one: use the code in a big if-statement.
        #   Not all data-items are passed to the constructors of
        #   the classes that represent the events: they do not need
        #   the code or subsystem, for example.
        if (code == LOGIN):
            event = LoginEvent(context, event_id, date, 
              userInfo, siteInfo, instanceDatum, supplementaryDatum)
        elif (code == BADPASSWORD):
            event = BadPasswordEvent(context, event_id, date, 
              userInfo, siteInfo)
        elif (code == BADUSERID):
            event = BadUserIdEvent(context, event_id, date,
              siteInfo, instanceDatum)
        else:
            # If we get something odd, create a basic event with all
            #  the data we have. All call methods for audit-event
            #  factories will end in this call.
            event = BasicAuditEvent(context, event_id, UNKNOWN, date, 
              userInfo, instanceUserInfo, siteInfo, groupInfo, 
              instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event
    
    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)

class LoginEvent(BasicAuditEvent):
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo, 
        instanceDatum, supplementaryDatum):
        BasicAuditEvent.__init__(self, context, id, 
          LOGIN, d, None, userInfo, siteInfo, None,  
          instanceDatum, supplementaryDatum, SUBSYSTEM)
       
    def __str__(self):
        retval = u'%s (%s) logged in to %s (%s). Redirecting to '\
                    u'<%s> with remember me set to "%s"'%\
                    (self.instanceUserInfo.name, self.instanceUserInfo.id,
                    self.siteInfo.name, self.siteInfo.id,
                    self.supplementaryDatum, self.instanceDatum)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event groupserver-login-event-%s' % self.code
        retval = u'<span class="%s">Logged in, and visited '\
          u'<a href="%s"><code class="url">%s</code></a>'%\
          (cssClass, self.supplementaryDatum, self.supplementaryDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
          
        return retval

class BadPasswordEvent(BasicAuditEvent):
    implements(IAuditEvent)

    def __init__(self, context, id, d, userInfo, siteInfo):
        BasicAuditEvent.__init__(self, context, id, 
          BADPASSWORD, d, userInfo, None, siteInfo, None,  
          None, None, SUBSYSTEM)
       
    def __str__(self):
        retval = u'%s (%s) failed to log in to %s (%s) because '\
                    u'the password is incorrect'%\
                    (self.userInfo.name, self.userInfo.id,
                    self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event groupserver-login-event-%s' % self.code
        retval = u'<span class="%s"><strong>Failed</strong> to log '\
          u'in because of an incorrect password.'% (cssClass)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
          
        return retval

class BadUserIdEvent(BasicAuditEvent):
    implements(IAuditEvent)

    def __init__(self, context, id, d, siteInfo, instanceDatum):
        BasicAuditEvent.__init__(self, context, id, 
          BADUSERID, d, None, None, siteInfo, None,  
          instanceDatum, None, SUBSYSTEM)
       
    def __str__(self):
        retval = u'Failed to log in (%s) to %s (%s) because no '\
                    u'email or user ID matched.'%\
                    (self.instanceDatum, 
                    self.siteInfo.name, self.siteInfo.id)
        retval = retval.encode('ascii', 'ignore')
        return retval
    
    @property
    def xhtml(self):
        cssClass = u'audit-event groupserver-login-event-%s' % self.code
        retval = u'<span class="%s"><strong>Failed</strong> to log '\
          u'in <code>%s</code> because no email or user-identifer '\
          u'matched.' % (cssClass, self.instanceDatum)
        retval = u'%s (%s)' % \
          (retval, munge_date(self.context, self.date))
          
        return retval

class AnonLoginAuditor(object):
    def __init__(self, context, siteInfo):
        self.context = context
        self.siteInfo = siteInfo
        self.userInfo = createObject('groupserver.UserFromId', 
          context, '')
        self.queries = AuditQuery()
      
        self.factory = LoginAuditEventFactory()
        
    def info(self, code, instanceDatum = '', supplementaryDatum = ''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.userInfo, self.userInfo,
          self.siteInfo, code, instanceDatum, supplementaryDatum)
          
        e =  self.factory(self.userInfo.user, eventId,  code, d,
          self.userInfo, None, self.siteInfo, None,
          instanceDatum, supplementaryDatum, SUBSYSTEM)
          
        self.queries.store(e)
        log.info(e)


class LoginAuditor(object):
    """An Auditor for Login
    
    DESCRIPTION
        An auditor (sometimes called an auditer) creates an audit 
        trail for a specific subsystem. In this case login. The
        work of creating the actual events is carried out by the
        audit-event factory, in this case "LoginAuditEventFactory".
        Every subsystem will (should) have its own auditor.
    """
    def __init__(self, siteInfo, user):
        """Create an login auditor.
        
        DESCRIPTION
            The constructor for an auditor is passed all the data 
            that will be the same for the events that are created
            during one use of the auditor by a Zope 3 page-view.
        
        ARGUMENTS
            "userInfo"
            "siteInfo"
            
        SIDE EFFECTS
        """
        self.user = user
        self.userInfo = IGSUserInfo(user)
        self.siteInfo = siteInfo
        
        self.queries = AuditQuery()
      
        self.factory = LoginAuditEventFactory()
        
    def info(self, code, instanceDatum = '', supplementaryDatum = ''):
        """Log an info event to the audit trail.

        DESCRIPTION
            This method logs an event to the audit trail. It is
            named after the equivalent method in the standard Python
            logger, which it also writes to. The three arguments 
            (other than self) are combined to form the arguments to
            the factory, which creates the event that is then 
            recorded.
                
        ARGUMENTS
            "code"    The code that identifies the event that is 
                      logged. Sometimes this is enough.
                      
            "instanceDatum"
                      Data about the event. Each event class has its
                      own way to interpret this data.
                      
            "supplementaryDatum"
                      More data about an event.
        
        SIDE EFFECTS
            * Creates an ID for the new event,
            * Writes the instantiated event to the audit-table, and
            * Writes the event to the standard Python log.
        
        RETURNS
            None
        """
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.userInfo, self.userInfo,
          self.siteInfo, code, instanceDatum, supplementaryDatum)
          
        e =  self.factory(self.userInfo.user, eventId,  code, d,
          self.userInfo, None, self.siteInfo, None,
          instanceDatum, supplementaryDatum, SUBSYSTEM)

        self.queries.store(e)
        log.info(e)



