from django.db import models
from django.core.exceptions import ValidationError, PermissionDenied
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from voting.models import Voting
from datetime import date


class Census(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    class Meta:
        unique_together = (('voting_id', 'voter_id'),)

    @classmethod
    def create(cls, voting_id, voter_id):

        census = cls(voting_id=voting_id, voter_id=voter_id)

        return census

    @staticmethod
    def check_restrictions_multiple_voters(voting_id, voters):
        """
        This method checks all the conditions that must be satisfied in order for the census objects to be created:

        1. The voting id must exist.
        2. All the voters ids must exist.
        3. All the census objects must not already exist in the database.
        4. All the voters must pass the voting age and gender restricctions if any.

        :return: True if all conditions are passed, an Exception is raised otherwise.
        """

        # This will fail if any of the elements does not exist
        voting = Voting.objects.get(id=voting_id)
        users = [User.objects.get(id=voter_id) for voter_id in voters]

        for voter_id in voters:
            if Census.objects.filter(voting_id=voting_id, voter_id=voter_id).count():
                raise IntegrityError(
                    'Conflict: The census (voting_id:{},voter_id:{}) already exists'.format(voting_id, voter_id))

        for user in users:
            Census.gender_and_age(voting, user)

        return True

    @staticmethod
    def gender_and_age(voting, voter):
        """
        Given a voting and user object, checks the gender and age restrictions.
        :return: True if the conditions are passed, and Exception should be raised otherwise.
        """

        if voting.gender and voter.userprofile.gender != voting.gender:
            raise ValidationError(
                'The user "{}" with id "{}" does not pass the gender restriction'.format(voter.username, voter.id))

        birthdate = voter.userprofile.birthdate

        age = None
        if birthdate:
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

        if voting.min_age and age and age < voting.min_age:
            raise ValidationError(
                'The user "{}" with id "{}" does not pass the minimum age restriction'.format(voter.username, voter.id))

        if voting.max_age and age and age > voting.max_age:
            raise ValidationError(
                'The user "{}" with id "{}" does not pass the maximum age restriction'.format(voter.username, voter.id))

        return True

    @staticmethod
    def public_or_private(voting_id, voter_ids, user):
        res = voter_ids
        voting = Voting.objects.get(id=voting_id)

        if voting.public_voting:
            if not user.is_staff:
                res = [user.id]
        elif not user.is_staff:
            raise PermissionDenied("This voting is private and you are not a staff member.")

        return res
