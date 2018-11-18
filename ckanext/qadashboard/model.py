import domain_object
import meta
import types as _types

from ckan import model

problem_table = Table('problem', meta.metadata
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('package_id', types.UnicodeText, ForeignKey('package.id')),
                Column('problem_type', types.UnicodeText),
                Column('current_status', types.UnicodeText),
                Column('creator_id', types.UnicodeText, ForeignKey('user.id')),
                Column('date_created', types.DateTime, default=datetime.datetime.now),
                Column('date_modified', types.DateTime, default=datetime.datetime.now),
                Column('description', types.UnicodeText))
                
problem_update_table = Table('problem_update', meta.metadata
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('problem_id', types.UnicodeText, ForeignKey('problem.id')),
                Column('user_id', types.UnicodeText, ForeignKey('user.id')),
                Column('status_id', types.UnicodeText),
                Column('notes', types.UnicodeText))
                
problem_type_table = Table('problem_type', meta.metadata
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('name', types.UnicodeText))

class Problem (domain_object.DomainObject):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    
class ProblemUpdate (domain_object.DomainObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
class ProblemType (domain_object.DomainObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def init_tables():
    metadata.create_all(model.meta.engine)