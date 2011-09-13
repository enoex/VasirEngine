"""=============================================================================
    Entity.py
    ------------
    Contains the entity class definition.  An entity could be a character, 
    monster, etc. The various attributes affect how the entity interacts
    with the world and other entities.
============================================================================="""
"""=============================================================================

IMPORTS

============================================================================="""
#----------------------------------------
#Vasir Engine Imports
#----------------------------------------
import Entity

#----------------------------------------
#Third Party Imports
#----------------------------------------
import zmq


"""=============================================================================

FUNCTIONS

============================================================================="""
def run_server():
    '''run_server:
    --------------
    Starts up a basic server that will listen for messages (sent from django)
    using ZeroMQ.  When receiving messages, certain things will happen, allowing
    clients to interact with the engine'''

    print 'Server Started!'
    print '-' * 42

    #Get context for ZeroMQ
    context = zmq.Context()
    #Get a socket. Use the REP method of zmq
    socket = context.socket(zmq.REP)
    #Bind the socket to a port
    socket.bind('tcp://127.0.0.1:5000')

    #Server / Game Loop
    while True:
        #When the socket receives a message, get it
        msg = socket.recv()
        #Print the message
        print 'Received Message: %s' % (msg)

        #---------------------------------------------------------------------
        #
        #Perform actions based on message
        #
        #---------------------------------------------------------------------  
        #--------------------------------
        #Create Entity
        #--------------------------------
        if msg == 'create_entity':
            #Create a new entity and return its ID (We don't need to
            #   save the context or reference to it because it's handled
            #   through the class for us)
            temp_entity = Entity.Entity()

            print 'Created entity'
            
            #Send the message with the entity ID
            socket.send("({'entity_id': '%s'})" % (temp_entity.id))
        #--------------------------------
        #Get Entity Info
        #--------------------------------
        elif 'get_info_' in msg:
            #The msg will look like 'get_info_entityXYZ', so grab the entity
            #   by looking at the Class' _entities dict and the key is just
            #   the message with 'get_info_' replaced with '' so it would only
            #   contain the entity ID
            entity_id = msg.replace('get_info_', '')
            temp_entity = Entity.Entity._entities[entity_id]

            print 'Got entity info: %s' % (entity_id)

            #Send the entity info
            socket.send('%s' % (temp_entity.get_info_json()) )

        #--------------------------------
        #Get ALL entities
        #--------------------------------
        elif 'get_entities' in msg:
            #Get all entities
            entities = Entity.Entity._entities

            print 'Retrieved all %s entities' % (len(entities))

            #Create an array which we'll use to get all the entities and
            #   stuff in JSON text
            entities_json = []

            for entity in entities:
                #Get the current JSON, but remove the first and trailing ( )'s
                #   Because we'll want to return a list, not an individual
                #   object
                entities_json.append( entities[entity].get_info_json()[1:-1] )

            entities_json = ','.join(entities_json)
    
            #Send the entity info
            socket.send('([%s])' % (entities_json) )



"""=============================================================================

INITIALIZE

============================================================================="""
if __name__ == '__main__':
    run_server()
