from src.models.user_story import UserStory, PriorityEnum
from src.db import db

class UserStoryManager:
    def add_user_story(self, data):
        user_story = UserStory.from_dict(data)
        db.session.add(user_story)
        db.session.commit()
        return user_story

    def get_user_story(self, user_story_id):
        return UserStory.query.get(user_story_id)

    def get_all_user_stories(self):
        return UserStory.query.all()

    def update_user_story(self, user_story_id, updates):
        user_story = UserStory.query.get(user_story_id)
        if not user_story:
            return None
        # Ignorar campos que no deben actualizarse
        updates = {k: v for k, v in updates.items() if k not in ('id', 'created_at')}
        for key, value in updates.items():
            if hasattr(user_story, key):
                setattr(user_story, key, value)
        db.session.commit()
        return user_story

    def delete_user_story(self, user_story_id):
        user_story = UserStory.query.get(user_story_id)
        if not user_story:
            return False
        db.session.delete(user_story)
        db.session.commit()
        return True
