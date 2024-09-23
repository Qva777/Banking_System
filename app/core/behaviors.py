import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from app import db


class Timestampable(db.Model):
    """ Abstract model adds fields to the inheriting model """
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class SoftDeletionModel(db.Model):
    """ Abstract model for adding with support for soft deletion via the 'deleted_at' field """
    __abstract__ = True
    deleted_at = db.Column(db.DateTime, nullable=True)

    def delete(self):
        """ Soft delete: set the deletion time. """
        self.deleted_at = datetime.now()
        db.session.commit()

    def recover(self):
        """ Recovery: Reset 'deleted_at' """
        self.deleted_at = None
        db.session.commit()

    def hard_delete(self):
        """ Complete removal of an object """
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def query_alive(cls):
        """ Query only for 'live' (not deleted) records """
        return cls.query.filter(cls.deleted_at.is_(None))

    @classmethod
    def query_dead(cls):
        """ Query for 'deleted' records only """
        return cls.query.filter(cls.deleted_at.isnot(None))
