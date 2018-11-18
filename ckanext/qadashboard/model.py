import ckan.model.domain_object as domain_object
import ckan.model.meta as meta
import ckan.model.types as _types
import datetime

from ckan import model
from sqlalchemy import types, Column, Table, ForeignKey, orm
from sqlalchemy.orm import mapper

class Status(object):
    OPEN = u'Open'
    PENDING = u'Pending information'
    SOLVED = u'Solved'

problem_type_table = Table('problem_type', meta.metadata,
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('name', types.UnicodeText))
    
problem_table = Table('problem', meta.metadata,
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('package_id', types.UnicodeText, ForeignKey('package.id')),
                #Column('title', types.UnicodeText),
                Column('problem_type', types.UnicodeText, ForeignKey('problem_type.id')),
                Column('current_status', types.UnicodeText, default=Status.OPEN),
                Column('creator_id', types.UnicodeText, ForeignKey('user.id')),
                Column('date_created', types.DateTime, default=datetime.datetime.now),
                Column('date_modified', types.DateTime, default=datetime.datetime.now),
                Column('description', types.UnicodeText))
                
problem_update_table = Table('problem_update', meta.metadata,
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('problem_id', types.UnicodeText, ForeignKey('problem.id')),
                Column('user_id', types.UnicodeText, ForeignKey('user.id')),
                Column('status_id', types.UnicodeText),
                Column('notes', types.UnicodeText))
                
class ProblemType (domain_object.DomainObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    
    @classmethod 
    def all (cls):
        q = model.Session.query(cls)
        return q.all()
        
class Problem (domain_object.DomainObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    @classmethod
    def get(cls, id):
        if not id:
            return None
        
        problem = meta.Session.query(cls).get(id)
        return problem
            
    @classmethod
    def get_related(cls, id):
        if not id:
            return None
        
        problem = meta.Session.query(cls, model.user.User).join(model.user.User).filter(cls.id == id)
        return problem.one()
    
    @classmethod     
    def by_package(cls, package_id):
        q = model.Session.query(cls).\
            filter_by(package_id = package_id)
        return q.all()
            
    
class ProblemUpdate (domain_object.DomainObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

mapper(ProblemType, problem_type_table)
mapper(Problem, problem_table, properties={
            'user': orm.relation(model.user.User,
                backref=orm.backref('problems',
                cascade='all, delete, delete-orphan'
                )),
            'package': orm.relation(model.package.Package,
                backref=orm.backref('problems',
                cascade='all, delete, delete-orphan'
                )),
})
mapper(ProblemUpdate, problem_update_table)
            
def init_tables():
    meta.metadata.create_all(model.meta.engine)
    model.Session.add(ProblemType(name='Broken link'))
    model.Session.add(ProblemType(name='Wrong data'))
    model.Session.add(ProblemType(name='Insufficient information'))
    model.Session.add(ProblemType(name='Other'))
    model.Session.commit()
    