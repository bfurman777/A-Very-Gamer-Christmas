from copy import copy

from entities.EntityBase import EntityBase
from entities.Item import Item
from classes.Collider import Collider
from classes.EntityCollider import EntityCollider

class Door(EntityBase):
    def __init__(self, screen, spriteCollection, x, y, sound, level, gravity=0):
        super(Door, self).__init__(x, y, gravity)
        self.screen = screen
        self.spriteCollection = spriteCollection
        self.animation = copy(self.spriteCollection.get("Door").animation)
        self.type = "Mob"
        self.screen = screen
        self.dashboard = level.dashboard
        self.collision = Collider(self, level)
        self.EntityCollider = EntityCollider(self)
        self.levelObj = level
        self.sound = sound

    def update(self, camera):
        if self.alive:
            self.checkEntityCollision()
        else:
            self.onDead(camera)
            
    def checkEntityCollision(self):
        for ent in self.levelObj.entityList:
            if ent is not self:
                collisionState = self.EntityCollider.check(ent)
                if collisionState.isColliding:
                    print('collide')
                    if ent.type == 'Player':
                        self._onCollisionWithMob(ent, collisionState)
    
    def _onCollisionWithMob(self, mob, collisionState):
        if collisionState.isColliding:
            self.alive = False
            self.sound.play_sfx(self.sound.brick_bump)
            
    def onDead(self, camera):
        print('AAA')