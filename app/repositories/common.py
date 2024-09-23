from app import db


class CommonRepository:
    """ Requests to user database """

    @staticmethod
    def save_instance(model_instance):
        """ Save database instance """
        db.session.add(model_instance)
        db.session.commit()

    @staticmethod
    def commit_changes():
        """ Commit changes to the database """
        db.session.commit()

    @staticmethod
    def delete_instance(model, instance):
        """ Soft deletion a model_instance from the database """
        model.delete(instance)

    @staticmethod
    def hard_delete_instance(model, instance):
        """ Hard deletion a model_instance from the database """
        model.hard_delete(instance)

    @staticmethod
    def recover_instance(model):
        """ Recover deleted instance """
        model.recover()

    @staticmethod
    def get_deleted_instance(model):
        """ Get deleted instance """
        return model.query_dead().all()
