import ckan.model.domain_object as domain_object
import ckan.model.meta as meta
import ckan.model.types as _types
import ckan.model.tracking as tracking
import datetime

from ckan import model
from sqlalchemy import types, Column, Table, ForeignKey, orm, func
from sqlalchemy.orm import mapper

class Status(object):
    OPEN = u'Open'
    PENDING = u'Pending information'
    SOLVED = u'Solved'
    
    @staticmethod
    def as_array():
        return [Status.OPEN, Status.PENDING, Status.SOLVED]
        

problem_type_table = Table('problem_type', meta.metadata,
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('name', types.UnicodeText))
    
problem_table = Table('problem', meta.metadata,
                Column('id', types.UnicodeText, primary_key=True, default=_types.make_uuid),
                Column('package_id', types.UnicodeText, ForeignKey('package.id')),
                Column('title', types.UnicodeText),
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
                Column('status_changed', types.Boolean, default=False),
                Column('date', types.DateTime, default=datetime.datetime.now),
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
    def all(cls, limit = -1):
        
        q = meta.Session.query(cls).\
            order_by(cls.date_created.desc())
        
        if limit > 0:
            return q.limit(limit).all()
        else:
            return q.all()
            
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
        
    @classmethod     
    def by_type(cls, problem_type):
        q = model.Session.query(cls).\
            filter_by(problem_type = problem_type)
        return q.all()
        
    @classmethod     
    def by_package_and_type(cls, package_id, problem_type):
        q = model.Session.query(cls).\
            filter_by(package_id = package_id).\
            filter_by(problem_type = problem_type)
        return q.all()
        
    @classmethod
    def in_packages(cls, package_ids, status = -1, problem_type = None, limit = -1):
        q = meta.Session.query(cls).\
            filter(cls.package_id.in_(package_ids))
            
        if type:
            q.filter(problem_type == problem_type)
            
        if status != -1:
            q.filter(cls.current_status != status)
            
        if limit > 0:
            return q.limit(limit).all()
        else:
            return q.all()
        
    @classmethod
    def open(cls, limit = -1):
        
        q = meta.Session.query(cls).\
            filter(cls.current_status != Status.SOLVED).\
            order_by(cls.date_created.desc())
        
        if limit > 0:
            return q.limit(limit).all()
        else:
            return q.all()
            
    
class ProblemUpdate (domain_object.DomainObject):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            
    @classmethod     
    def by_problem(cls, problem_id):
        q = model.Session.query(cls, model.user.User).\
            join(model.user.User).\
            filter(cls.problem_id == problem_id).\
            order_by(cls.date.asc())
        return q.all()
        
       
class TrackingSummary (tracking.TrackingSummary):

    @classmethod
    def get_by_date (cls, start_date, end_date, package_ids=None):
    
        if not package_ids:
            q = model.Session.query(tracking.TrackingSummary.tracking_date, func.sum(tracking.TrackingSummary.count)).\
                group_by(tracking.TrackingSummary.tracking_date).\
                order_by(tracking.TrackingSummary.tracking_date)
        
        else:
            q = model.Session.query(tracking.TrackingSummary.tracking_date, func.sum(tracking.TrackingSummary.count)).\
                filter(tracking.TrackingSummary.package_id.in_(package_ids)).\
                group_by(tracking.TrackingSummary.tracking_date).\
                order_by(tracking.TrackingSummary.tracking_date)

        return q.all()
        
        

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
    