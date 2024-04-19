import pygame
from random import randint
import sys 
import os

pygame.init()

#создание окна
window = pygame.display.set_mode((1300, 900)) 
clock =  pygame.time.Clock()

#класс мира
class World():
    def __init__(self) -> None:
        self.hero = Player(x=150, y=200, height=150, width=100, img='textures/stand_no_weapon/1.png', direction='right',
               status='run', room=self.room1(), directory_stand='textures/stand_no_weapon/',
                        directory_run='textures/run_no_weapon/', health=100, world=self, speed=5) 
        self.sword_hero = Sword_player(
                        x=75, y=200, height=150, width=100, img='textures/stand_with_weapon/1.png', 
                        direction='right', status='run', room=self.hero.room, directory_stand='textures/stand_with_weapon/',
                        directory_run='textures/run_with_weapon/', directory_attack='textures/sword.png/', health=100, world=self, speed=4)
   
    def room1(self):

        sword = Sword(height=40, width=40, x=340, y=340, img='pixel.sword.png')

        monster_mistake = Monster(x=675, y=650, height=150, width=100, img='textures/mistake_stand.png/0.png', direction='right',
                          status='run', directory_stand='textures/mistake_stand.png', directory_run='textures/mistake_walk',
                          directory_attack='textures/mistake_attack.png',
                          road=[(500, 650), (675, 650), (675, 150)], health=8, directory_health='textures/hp', health_width=100, shift_health=35, speed=1, attention_zone=300, damage=1)

        monster_mistake2 = Monster(x=975, y=650, height=150, width=100, img='textures/mistake_stand.png/0.png', direction='right',
                          status='run', directory_stand='textures/mistake_stand.png', directory_run='textures/mistake_walk',
                          directory_attack='textures/mistake_attack.png',
                          road=[(900, 650), (1100, 650), (1100, 150)], health=8, directory_health='textures/hp', health_width=100, shift_health=35, speed=1, attention_zone=300, damage=1)

        slizn = Monster(x=350, y=350, height=50, width=50, img='textures/slizn/0.png', direction='right',
                          status='run', directory_stand='textures/slizn', directory_run='textures/slizn',
                          directory_attack='textures/slizn',
                          road=[(400, 400), (450, 450), (450, 450)], health=4, directory_health='textures/hp', health_width=50, shift_health=0, speed=0.5, attention_zone=200, damage=0.5)

        chest = Chest(x=300, y=300, height=100, width=90, status='close', loot=sword, directory='textures/chest/chest.png/')

        room = Room(objs=[chest, monster_mistake, monster_mistake2, slizn], land='test_room.csv', respawn=(150, 200)) 

        door1 = Door(x=950, y=710, height=90, width=100, status='close', directory='textures/doors/tree_door.png/', teleport=self.room2())
        room.objs.append(door1)

        room.build()

        return room
    
    def room2(self):
        wall_door = Wall_door(x=900, y=600, height=100, width=100, status='close', directory='textures/door.png/', teleport=None, key_index=1)

        slizn = Monster(x=350, y=350, height=50, width=50, img='textures/slizn/0.png', direction='right',
                          status='run', directory_stand='textures/slizn', directory_run='textures/slizn',
                          directory_attack='textures/slizn',
                          road=[(400, 400), (450, 450), (450, 450)], health=4, directory_health='textures/hp', health_width=50, shift_health=0, speed=0.5, attention_zone=100, damage=1)
        
        pawn = Monster(x=350, y=150, height=80, width=50, img='textures/pawn_stay.png/0.png', direction='right', 
                       status='run', directory_stand='textures/pawn_stay.png', directory_run='textures/pawn_walk.png', 
                       directory_attack='textures/pawn_attack.png', 
                       road=[(0, 150), (800, 150)], health=15, directory_health='textures/hp', health_width=50, shift_health=35, speed=5, attention_zone=500, damage=3, shift_health_y=-10)

        monster_purple = Monster(x=274, y=750, height=150, width=100, img='textures/purple_stay.png/0.png', direction='right',
                          status='run', directory_stand='textures/purple_stay.png', directory_run='textures/purple_walk.png',
                          directory_attack='textures/purple_attack.png',
                          road=[(450, 350), (0, 350), (5, 750), (450, 750)], health=8, directory_health='textures/hp', health_width=100, shift_health=35, speed=2, attention_zone=400, damage=2)

        key = Key(height=100, width=100, x=340, y=340, img='key.png', index=1)

        chest = Chest(x=1000, y=150, height=100, width=90, status='close', loot=key, directory='textures/chest/chest.png/')

        room = Room(objs=[chest, monster_purple, slizn, wall_door, pawn], land='test_room2.csv', respawn=(950, 710))
        


        room.build()

        return room

#класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, img, direction, status, room, directory_stand, directory_run, health, world, speed) -> None: 
        super().__init__()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.direction = direction
        self.animation_counter = 5 #замедляющий счетчик
        self.counter = 0
        self.speed = speed
        self.room = room #только перс
        self.active_zone = 70 #только перс
        self.health = health
        self.max_health = health
        self.world = world
        self.key_inventory = []
        self.weapon_inventory = []
        self.gui = GUI(100, 1400, self, 500, 'textures/hp/')
        #получение изображения
        self.image = pygame.image.load(img) 
        self.image = pygame.transform.scale(self.image, (height, width)) 
        self.image_mask = pygame.mask.from_surface(self.image)
        self.textures_stand = self.get_files_names(directory_stand)
        self.textures_run = self.get_files_names(directory_run) 
        self.textures_stand = self.load_textures(self.textures_stand, height, width) 
        self.textures_run = self.load_textures(self.textures_run, height, width)
        self.status = status

    def animation(self, textures):
        try:
            self.image = textures[self.direction][self.counter][0]
            self.image_mask = textures[self.direction][self.counter][1]
            self.image_mask_run = textures[self.direction][4][1] 

        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(textures[self.direction]):
            self.counter = 0 
    
    def load_textures(self, textures, height, width):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                #загрузка изброжения
                image = pygame.image.load(texture)
                #отзеркаливание изображения
                image = pygame.transform.scale(image, (height, width))
                if direction == 'left':                   
                    image = pygame.transform.flip(image, True, False)  
                image_mask = pygame.mask.from_surface(image)
                loaded_textures[direction].append([image, image_mask]) 
        return loaded_textures
    
    def get_files_names(self, directory):
        # Список, который будет содержать имена файлов
        files_list = []

        # Проходим по всем элементам в директории
        for filename in os.listdir(directory):
            # Полный путь к файлу
            path = os.path.join(directory, filename) #складываем папка+название файла

        # Проверяем, является ли элемент файлом, и если да, добавляем его в список
            if os.path.isfile(path): 
                files_list.append(path) 
        files_list.sort()
        return files_list
    
    def control(self):
        keys = pygame.key.get_pressed() 
        safe_x, safe_y = self.x, self.y
        if keys[pygame.K_a]:
            safe_x -= self.speed
            self.direction = 'left'
            self.status = 'run'
        elif keys[pygame.K_d]:
            safe_x += self.speed 
            self.direction = 'right'
            self.status = 'run'
        if keys[pygame.K_w]:
            safe_y -= self.speed 
            self.status = 'run'
        elif keys[pygame.K_s]:
            safe_y += self.speed
            self.status = 'run'
        if not any(keys):
            self.status = 'stand'
        if keys[pygame.K_1]:
            w_f = False
            for weapon in self.weapon_inventory:
                if isinstance(weapon, Sword):
                    w_f = True
            if w_f == True:
                self.transform_to_sword() 

        can_move_x, can_move_y = self.collision(safe_x, safe_y) 
        if can_move_x:
            self.x = safe_x
        if can_move_y:
            self.y = safe_y
    
    def show_image(self):
        if self.status == 'stand':
            self.animation(self.textures_stand)
        elif self.status == 'run':
            self.animation(self.textures_run)
        self.control()  
        window.blit(self.image, (self.x, self.y))
    
    def collision(self, safe_x, safe_y):
        can_move_x = True
        can_move_y = True
        for obj in self.room.objs:
            if not isinstance(obj, Sword):
                offsetx = obj.x - safe_x
                offsety = obj.y - self.y
                if self.image_mask_run.overlap_area(obj.image_mask, (offsetx, offsety)):
                    can_move_x = False
                    break
        for obj in self.room.objs:
            if not isinstance(obj, Sword):
                offsetx = obj.x - self.x
                offsety = obj.y - safe_y
                if self.image_mask_run.overlap_area(obj.image_mask, (offsetx, offsety)):
                    can_move_y = False
                    break
        self.interact_with_items() 
        if safe_x <= -50:
            can_move_x = False
        if safe_y <= 80:
            can_move_y = False
        if safe_x >= 1200:
            can_move_x = False
        if safe_y >= 750:
            can_move_y = False
        return can_move_x, can_move_y
    
    def interact_with_items(self):
        keys = pygame.key.get_pressed() 
        for obj in self.room.objs:
            obj_centerx = obj.x+obj.width/2
            obj_centery = obj.y+obj.height/2
            player_centerx = self.x+self.width/2
            player_centery = self.y+self.height/2
            offsetx = abs(player_centerx - obj_centerx)
            offsety = abs(player_centery - obj_centery)
            if isinstance(obj, Chest): #если obj-объект класса Chest
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                    if keys[pygame.K_e]:
                        if obj.status == 'close':
                            obj.chest_open = True
            #взаимодействие с дверью
            if isinstance(obj, Door) and not isinstance(obj, Wall_door):
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                    if keys[pygame.K_e]:
                        if obj.status == 'close':
                            obj.door_open = True
                        if obj.status == 'open':
                            self.room = obj.teleport

            #взаимодействие с механической дверью           
            if isinstance(obj, Wall_door):
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                    if keys[pygame.K_e]:
                        k_f = False
                        for key in self.key_inventory:
                            if key.index == obj.key_index:
                                k_f = True
                                
                        if obj.status == 'close' and k_f == True:
                            obj.door_open = True
                if obj.status == 'open':
                    self.room.objs.remove(obj)
                    obj = Floor(texture=obj.texture_name[-1], x=obj.x, y=obj.y, height=obj.height, width=obj.width)
                    obj.image = pygame.transform.flip(obj.image, flip_x=True, flip_y=False)
                    self.room.load_land.append(obj)

            #взаимодействие с ключом
            if isinstance(obj, Key):
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                   if keys[pygame.K_e]:
                       self.key_inventory.append(obj)
                       self.room.objs.remove(obj)     
            #взаимодействие с мечом
            if isinstance(obj, Sword) and not isinstance(obj, Key):
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                    if keys[pygame.K_e]:
                        self.weapon_inventory.append(obj)
                        self.room.objs.remove(obj)
     
    def transform_to_sword(self):
        global player
        self.world.sword_hero.x, self.world.sword_hero.y = player.x, player.y
        self.world.sword_hero.room = player.room
        self.world.sword_hero.health = player.health
        self.world.sword_hero.gui = player.gui
        player = self.world.sword_hero
    
    def transform_to_player(self):
        global player
        self.world.hero.x, self.world.hero.y = player.x, player.y
        self.world.hero.room = player.room
        self.world.hero.health = player.health
        self.world.hero.gui = player.gui
        player = self.world.hero
    
    def rebirth(self):
        self.x = self.room.respawn[0]
        self.y = self.room.respawn[1]

#класс монстров
class Monster():
    def __init__(self, x, y, height, width, img, direction, status, directory_stand, directory_run, directory_attack,road, health, directory_health, health_width, shift_health, speed, attention_zone, damage, shift_health_y=0) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.direction = direction
        self.status = status
        self.animation_counter = 5
        self.counter = 0
        self.speed = speed
        self.safe_speed = speed
        self.attention_zone = attention_zone
        self.road = road
        self.dot = 0
        self.health = health
        self.max_health = health
        self.health_width = health_width
        self.shift_health = shift_health
        self.damage = damage
        self.shift_health_y = shift_health_y
        self.direction_road = 1  # Начальное направление изменения точки

        #получение изображения
        self.image = pygame.image.load(img) 
        self.image = pygame.transform.scale(self.image, (height, width)) 
        self.image_mask = pygame.mask.from_surface(self.image)
        self.textures_stand = self.get_files_names(directory_stand)
        self.textures_run = self.get_files_names(directory_run) 
        self.textures_attack = self.get_files_names(directory_attack)
        self.textures_stand = self.load_textures(self.textures_stand, height, width) 
        self.textures_run = self.load_textures(self.textures_run, height, width)
        self.textures_attack = self.load_textures(self.textures_attack, height, width)
        self.textures_health = self.get_files_names(directory_health)
        self.textures_health = self.load_textures(self.textures_health, height=health_width, width=10)
        self.attack_mask = pygame.mask.from_surface(self.textures_attack['left'][2][0])
        self.attack_mask_right = pygame.mask.from_surface(self.textures_attack['right'][2][0]) 
        self.status = status 
        self.attention_flag = False

#ходьба по маршруту
    def monster_walk(self):
        safe_x, safe_y = self.x, self.y
        if self.x < self.road[self.dot][0]:
            safe_x += self.speed
            self.direction = 'right'
        elif self.x > self.road[self.dot][0]:
            safe_x -= self.speed
            self.direction = 'left'
        # движение вверх
        if self.y < self.road[self.dot][1]:
            safe_y += self.speed
        elif self.y > self.road[self.dot][1]:
            safe_y -= self.speed
        if self.y in range(self.road[self.dot][1]-10, self.road[self.dot][1]+10) and self.x in range(self.road[self.dot][0]-10, self.road[self.dot][0]+10):
            #Проверяем, достигли ли мы конца или начала списка
            if (self.dot == len(self.road) - 1 and self.direction_road == 1) or (self.dot == 0 and self.direction_road == -1):
                # Меняем направление
                self.direction_road *= -1
            self.dot += self.direction_road
        can_move_x, can_move_y = self.collision(safe_x, safe_y)
        if can_move_x:
            self.x = safe_x
        if can_move_y:
            self.y = safe_y  

#следование за игроком
    def monster_follow(self):
        safe_x, safe_y = self.x, self.y
        if safe_x < player.x:
            safe_x += self.speed
            self.direction = 'right'
        elif safe_x > player.x:
            safe_x -= self.speed
            self.direction = 'left'
        # движение вверх
        if safe_y < player.y:
            safe_y += self.speed
        elif safe_y > player.y:
            safe_y -= self.speed
        if safe_y in range(player.y-100, player.y+100) and safe_x in range(player.x-100, player.x+100):
            self.speed = 0
            self.status = 'attack'
        else:
            self.speed = self.safe_speed
            self.status = 'run'
        can_move_x, can_move_y = self.collision(safe_x, safe_y)
        if can_move_x:
            self.x = safe_x
        if can_move_y:
            self.y = safe_y  

#интеллект
    def intelekt(self):
        monster_centerx = self.x+self.width/2
        monster_centery = self.y+self.height/2
        player_centerx = player.x+player.width/2
        player_centery = player.y+player.height/2
        offsetx = abs(player_centerx - monster_centerx)
        offsety = abs(player_centery - monster_centery)
        if offsetx <= self.attention_zone and offsety <= self.attention_zone:
            self.monster_follow()
        else:
            self.monster_walk()

    def collision(self, safe_x, safe_y ):
        can_move_x = True
        can_move_y = True
        for obj in player.room.objs:
            if  isinstance(obj, (Wall, Wall_door)):
                offsetx = obj.x - safe_x
                offsety = obj.y - self.y
                #отталкивание
                if self.image_mask.overlap_area(obj.image_mask, (offsetx, offsety)):
                    can_move_x = False
                    break
        for obj in player.room.objs:
            if  isinstance(obj, (Wall, Wall_door)):
                offsetx = obj.x - self.x
                offsety = obj.y - safe_y
                if self.image_mask.overlap_area(obj.image_mask, (offsetx, offsety)):
                    can_move_y = False
                    break
        return can_move_x, can_move_y

    def animation(self, textures):
        try:
            self.image = textures[self.direction][self.counter][0]
            self.image_mask = textures[self.direction][self.counter][1]
            

        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(textures[self.direction]):
            self.counter = 0 

    def attack(self):
        try:
            self.image = self.textures_attack[self.direction][self.counter][0]
        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(self.textures_attack[self.direction]):
            self.a_f = False 
            self.status = 'stand' 
        offsetx = int(player.x - self.x)
        offsety = int(player.y - self.y) 
        if self.direction == 'left':
            overlap_area = self.attack_mask.overlap_area(player.image_mask, (offsetx, offsety))
            if overlap_area > 0 and self.counter == 2:
                player.health -= self.damage
                if player.health < 0:
                    player.rebirth()
                    player.health = player.max_health
                    self.a_f = False
                    self.status = 'run'
                    self.speed = 1
                player.gui.textures_health['left'][0][0] = pygame.transform.scale(player.gui.textures_health['left'][0][0], (player.gui.health_width/player.max_health*player.health, 50))

        if self.direction == 'right':
            overlap_area = self.attack_mask_right.overlap_area(player.image_mask, (offsetx, offsety))
            if overlap_area > 0 and self.counter == 2:
                player.health -= 1
                if player.health < 0:
                    player.rebirth()
                    player.health = player.max_health
                    self.a_f = False
                    self.status = 'run'
                    self.speed = 1
                player.gui.textures_health['left'][0][0] = pygame.transform.scale(player.gui.textures_health['left'][0][0], (player.gui.health_width/player.max_health*player.health, 50))

    def load_textures(self, textures, height, width):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                #загрузка изброжения
                image = pygame.image.load(texture)
                #отзеркаливание изображения
                image = pygame.transform.scale(image, (height, width))
                if direction == 'left':                   
                    image = pygame.transform.flip(image, True, False)  
                image_mask = pygame.mask.from_surface(image)
                loaded_textures[direction].append([image, image_mask]) 
        return loaded_textures

    def show_image(self):
        self.intelekt()
        if self.status == 'stand':
            self.animation(self.textures_stand)
        elif self.status == 'run':
            self.animation(self.textures_run) 
            self.image_mask_run = self.textures_run[self.direction][4][1] 
        elif self.status == 'attack':
            self.attack()

        #полоска здоровья
        if self.direction == 'left':
            window.blit(self.textures_health['left'][1][0], (self.x, self.y+self.shift_health_y))
            window.blit(self.textures_health['left'][0][0], (self.x, self.y+self.shift_health_y))
        elif self.direction == 'right':
            window.blit(self.textures_health['left'][1][0], (self.x+self.shift_health, self.y+self.shift_health_y))
            window.blit(self.textures_health['left'][0][0], (self.x+self.shift_health, self.y+self.shift_health_y))
        window.blit(self.image, (self.x, self.y))

    def get_files_names(self, directory):
        # Список, который будет содержать имена файлов
        files_list = []

        # Проходим по всем элементам в директории
        for filename in os.listdir(directory):
            # Полный путь к файлу
            path = os.path.join(directory, filename)

        # Проверяем, является ли элемент файлом, и если да, добавляем его в список
            if os.path.isfile(path): 
                files_list.append(path) 
        files_list.sort()
        return files_list

#класс персонажа с мечом
class Sword_player(Player):
    def __init__(self, x, y, height, width, img, direction, status, room, directory_stand, directory_run, directory_attack, health, world, speed) -> None:
        super().__init__(x, y, height, width, img, direction, status, room, directory_stand, directory_run, health, world, speed) 
        self.textures_attack = self.get_files_names(directory_attack) 
        self.textures_attack = self.load_textures(self.textures_attack, height, width)
        self.sword_right = pygame.image.load('textures/utils/sword.png') 
        self.sword_right = pygame.transform.scale(self.sword_right, (height, width)) 
        self.sword_mask_right = pygame.mask.from_surface(self.sword_right)
        self.sword_left = pygame.transform.flip(self.sword_right, True, False) 
        self.sword_mask_left = pygame.mask.from_surface(self.sword_left)

    def animation(self, textures):
        try:
            self.image = textures[self.direction][self.counter][0]
            self.image_mask = textures[self.direction][self.counter][1]
            self.image_mask_run = textures[self.direction][6][1] 

        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(textures[self.direction])-1:
            self.counter = 0 
            
    def control(self):
        keys = pygame.key.get_pressed() 
        safe_x, safe_y = self.x, self.y
        if self.status != 'attack':
            if keys[pygame.K_a]:
                safe_x -= self.speed
                self.direction = 'left'
                self.status = 'run'
            elif keys[pygame.K_d]:
                safe_x += self.speed 
                self.direction = 'right'
                self.status = 'run'
            if keys[pygame.K_w]:
                safe_y -= self.speed 
                self.status = 'run'
            elif keys[pygame.K_s]:
                safe_y += self.speed
                self.status = 'run'
            if not any(keys):
                self.status = 'stand'
        can_move_x, can_move_y = self.collision(safe_x, safe_y) 
        if keys[pygame.K_SPACE]:
            self.status = 'attack' 
        if self.status == 'attack':
            can_move_x, can_move_y = False, False
        if keys[pygame.K_0]:
            self.transform_to_player()
        if can_move_x:
            self.x = safe_x
        if can_move_y:
            self.y = safe_y
    
    def show_image(self):
        if self.status == 'stand':
            self.animation(self.textures_stand)
        elif self.status == 'run':
            self.animation(self.textures_run)
        elif self.status == 'attack':
            self.attack()
        self.control()  
        window.blit(self.image, (self.x, self.y))

    def attack(self):
        try:
            self.image = self.textures_attack[self.direction][self.counter][0]
        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(self.textures_attack[self.direction]):
            self.a_f= False 
            self.status = 'stand' 

    def interact_with_items(self):
        super().interact_with_items()
        for obj in self.room.objs:
            if isinstance(obj, Monster):
                # Исправление: Расчёт смещений без использования abs и относительно верхнего левого угла
                offsetx = int(obj.x - self.x)
                offsety = int(obj.y - self.y)                    
                if self.status == 'attack':
                    #удар по монстру(слева)
                    if self.direction == 'left':
                        overlap_area = self.sword_mask_left.overlap_area(obj.image_mask_run, (offsetx, offsety))
                        if overlap_area > 0 and self.counter == 4:
                            obj.health -= 1
                            obj.textures_health['left'][0][0] = pygame.transform.scale(obj.textures_health['left'][0][0], (obj.health_width/obj.max_health*obj.health, 10))
                            if obj.health == 0:
                                self.room.objs.remove(obj)
                            break
                        #удар по монстру(справа)
                    elif self.direction == 'right':
                        overlap_area = self.sword_mask_right.overlap_area(obj.image_mask_run, (offsetx, offsety))
                        if overlap_area > 0 and self.counter == 4:
                            obj.health -= 1
                            obj.textures_health['left'][0][0] = pygame.transform.scale(obj.textures_health['left'][0][0], (obj.health_width/obj.max_health*obj.health, 10))
                            if obj.health == 0:
                                self.room.objs.remove(obj)
                            break             

#класс комнаты
class Room():
    '''комната'''
    def __init__(self, objs, land, respawn) -> None:
        self.objs = objs
        self.land = land 
        self.load_land = []
        self.respawn = respawn

    def show(self):
        for floor in self.load_land:
            floor.show_image() 

    def build(self):
        with open(self.land, 'r') as file:
            lines = file.readlines()
            y = 0
            for line in lines:
                line = line.rstrip('\n')
                line = line.split(',')
                x = 0
                for el in line:
                    if el == 'F':
                        self.load_land.append(Floor(texture='textures/floor/dirt_3.png', x=x, y=y, height=50, width=50))
                    elif el == 'W':
                        self.objs.append(Wall(texture='textures/wall/wood_floor.png', x=x, y=y, height=50, width=50))
                    elif el == 'S':
                        self.load_land.append(Floor(texture='textures/floor/dirt_8.png', x=x, y=y, height=50, width=50))
                    elif el == 'R':
                        self.objs.append(Wall(texture='textures/wall/R_wall.png', x=x, y=y, height=50, width=50))
                    x += 50
                y += 50

#класс пола
class Floor():
    '''пол'''
    def __init__(self, texture, x, y, height, width) -> None:
        self.texture = texture
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        #получение изображения
        self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (self.height, self.width)) 

    def show_image(self):
        window.blit(self.image, (self.x, self.y))

#класс стены
class Wall(Floor):
    def __init__(self, texture, x, y, height, width) -> None:
        super().__init__(texture, x, y, height, width)
        self.image_mask = pygame.mask.from_surface(self.image) 

#класс сундука
class Chest(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, status, loot, directory) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.status = status
        self.loot = loot
        self.textures = self.get_files_names(directory)
        self.textures = self.load_textures(self.textures)
        self.counter = 0
        self.animation_counter = 5
        self.direction = 'left'
        self.chest_open = False
        #получение изображения
        if self.status == 'open':
            self.image = self.textures['left'][len(self.textures)-4][0]
        elif self.status == 'close':
            self.image = self.textures['left'][0][0]
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect() 

    def show_image(self):
        if self.chest_open == False:
            if self.status == 'open':
                self.image = self.textures['left'][len(self.textures)-4][0] 
            elif self.status == 'close':
                self.image = self.textures['left'][0][0]
        elif self.chest_open == True:
            self.animation() 
        window.blit(self.image, (self.x, self.y))

    #подгузка текстур
    def load_textures(self, textures):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                #загрузка изброжения
                image = pygame.image.load(texture)
                #отзеркаливание изображения
                image = pygame.transform.scale(image, (self.height, self.width))
                if direction == 'left':                   
                    image = pygame.transform.flip(image, True, False)  
                image_mask = pygame.mask.from_surface(image)
                loaded_textures[direction].append([image, image_mask]) 
        return loaded_textures
    
    #получение имён файлов
    def get_files_names(self, directory):
        # Список, который будет содержать имена файлов
        files_list = []
        # Проходим по всем элементам в директории
        for filename in os.listdir(directory):
            # Полный путь к файлу
            path = os.path.join(directory, filename)
        # Проверяем, является ли элемент файлом, и если да, добавляем его в список
            if os.path.isfile(path): 
                files_list.append(path) 
        '''Эта функция использует lambda-функцию в качестве ключа для сортировки. 
        Она извлекает число из имени файла и сортирует список по этим числам.'''
        files_list = sorted(files_list, key=lambda x: int(x.split("/")[-1].split(".")[0][5:]))

        return files_list
    
    #анимация сундука
    def animation(self):
        try:
            self.image = self.textures[self.direction][self.counter][0]
        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(self.textures[self.direction]):
            self.chest_open = False 
            self.status = 'open'
        #лут
            player.room.objs.append(self.loot)
            self.loot.x = self.x + 100
            self.loot.y = self.y + 0 

#графический интерфейс
class GUI():
    def __init__(self, height, width, player, health_width, directory_health) -> None:
        self.rect_background = pygame.Rect(0, 0, width, height)
        self.player = player
        self.health_width = health_width
        self.label = Label(x=550, y=25, height=50, font='font.ttf', color=(255, 255, 255), text='HP:')

        self.textures_health = player.get_files_names(directory_health)
        self.textures_health = player.load_textures(self.textures_health, height=500, width=50) 
    def show_image(self):
        pygame.draw.rect(window, (0, 0, 0), self.rect_background)
        self.label.show_image()
        window.blit(self.textures_health['left'][1][0], (600, 25))
        window.blit(self.textures_health['left'][0][0], (600, 25))

#класс меча
class Sword():
    def __init__(self, height, width, x, y, img) -> None:
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        #получение изображения
        self.image = pygame.image.load(img)
        self.image = pygame.transform.scale(self.image, (height, width))
        self.image_mask = pygame.mask.from_surface(self.image)

    def show_image(self):
        window.blit(self.image, (self.x, self.y))

#класс ключа
class Key(Sword):
    def __init__(self, height, width, x, y, img, index) -> None:
        super().__init__(height, width, x, y, img)
        self.index = index
#класс текста
class Label():
    def __init__(self, x, y, height, font, color, text) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.font = pygame.font.Font(font, self.height)
        self.color = color
        self.text = self.font.render(text, True, self.color)

    def show_image(self):
        window.blit(self.text, (self.x, self.y))

#класс двери
class Door():
    def __init__(self, x, y, height, width, status, directory, teleport) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.status = status
        self.counter = 0
        self.animation_counter = 5
        self.door_open = False
        self.teleport = teleport
        self.direction = 'left'

        #получение изобажения
        self.texture_name = self.get_files_names(directory)
        self.texture = self.load_textures(self.texture_name, height, width)
        if self.status == 'open':
            self.image = self.texture['left'][-1][0]
        elif self.status == 'close':
            self.image = self.texture['left'][0][0]
        self.image_mask = pygame.mask.from_surface(self.image)


    def load_textures(self, textures, height, width):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                #загрузка изброжения
                image = pygame.image.load(texture)
                #отзеркаливание изображения
                image = pygame.transform.scale(image, (height, width))
                if direction == 'left':                   
                    image = pygame.transform.flip(image, True, False)  
                image_mask = pygame.mask.from_surface(image)
                loaded_textures[direction].append([image, image_mask]) 
        return loaded_textures
    
    def show_image(self):
        window.blit(self.image, (self.x, self.y))
        if self.door_open == True:
            self.animation() 

    def get_files_names(self, directory):
        # Список, который будет содержать имена файлов
        files_list = []

        # Проходим по всем элементам в директории
        for filename in os.listdir(directory):
            # Полный путь к файлу
            if filename == '.DS_Store':
                continue
            path = os.path.join(directory, filename)

        # Проверяем, является ли элемент файлом, и если да, добавляем его в список
            if os.path.isfile(path): 
                files_list.append(path) 
        files_list.sort()
        return files_list

    def animation(self):
        try:
            self.image = self.texture[self.direction][self.counter][0]
        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(self.texture[self.direction]):
            self.door_open = False 
            self.status = 'open'     

#дверь механизм 
class Wall_door(Door):
    def __init__(self, x, y, height, width, status, directory, teleport, key_index) -> None:
        super().__init__(x, y, height, width, status, directory, teleport)
        self.key_index = key_index

    def animation(self):
        try:
            self.image = self.texture[self.direction][self.counter][0]
        except IndexError:
            self.counter = 0
        self.animation_counter -= 1
        if self.animation_counter == 0:
            self.counter += 1
            self.animation_counter = 5
        if self.counter == len(self.texture[self.direction]):
            self.door_open = False 
            self.status = 'open' 
    
    def show_image(self):
        window.blit(self.image, (self.x, self.y))
        if self.door_open == True:
            self.animation() 
            

    
#отоброжение текстур
world = World()           

player = world.hero
#основной игровой цикл (абстракция)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    player.room.show()
    for obj in player.room.objs:
        obj.show_image()
    player.show_image()
    #hero.show_image()
    player.gui.show_image() 
    clock.tick(60)
    pygame.display.update() 

