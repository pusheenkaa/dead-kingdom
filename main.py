import pygame
from random import randint, choice
import sys 
import os
import math
from dialogue import Dialogue
from multiline_text import MultiLineText
from alicjo_dialogue import dialogue_tree
from chicken_dialogue import dialogue_tree as chicken_tree

pygame.init()

#создание окна
window = pygame.display.set_mode((1300, 900), pygame.FULLSCREEN)
clock =  pygame.time.Clock()

#класс мира
class World():
    def __init__(self) -> None:
        self.hero = Player(x=150, y=300, height=150, width=100, img='textures/stand_no_weapon/1.png', direction='right',
               status='run', room=self.chicken_village(), directory_stand='textures/stand_no_weapon/',
                        directory_run='textures/run_no_weapon/', health=100, world=self, speed=5) 
        self.sword_hero = Sword_player(
                        x=75, y=200, height=150, width=100, img='textures/stand_with_weapon/1.png', 
                        direction='right', status='run', room=self.hero.room, directory_stand='textures/stand_with_weapon/',
                        directory_run='textures/run_with_weapon/', directory_attack='textures/sword.png/', health=100, world=self, speed=4)
   
    def room1(self):
        '''коричная комната'''
        sword = Sword(height=40, width=40, x=340, y=340, img='pixel.sword.png')

        key = Key(height=100, width=100, x=340, y=340, img='key.png', index=1)

        monster_mistake = Monster(x=675, y=650, height=150, width=100, img='textures/mistake_stand.png/0.png', direction='right',
                          status='run', directory_stand='textures/mistake_stand.png', directory_run='textures/mistake_walk',
                          directory_attack='textures/mistake_attack.png',
                          road=[(500, 650), (675, 650), (675, 150)], health=15, directory_health='textures/hp', health_width=100, shift_health=35, speed=1, attention_zone=300, damage=1, loot=key)

        monster_mistake2 = Monster(x=975, y=650, height=150, width=100, img='textures/mistake_stand.png/0.png', direction='right',
                          status='run', directory_stand='textures/mistake_stand.png', directory_run='textures/mistake_walk',
                          directory_attack='textures/mistake_attack.png',
                          road=[(900, 650), (1100, 650), (1100, 150)], health=15, directory_health='textures/hp', health_width=100, shift_health=35, speed=1, attention_zone=300, damage=1)

        slizn = Monster(x=350, y=350, height=50, width=50, img='textures/slizn/0.png', direction='right',
                          status='run', directory_stand='textures/slizn', directory_run='textures/slizn',
                          directory_attack='textures/slizn',
                          road=[(400, 400), (450, 450), (450, 450)], health=4, directory_health='textures/hp', health_width=50, shift_health=0, speed=0.5, attention_zone=200, damage=0.5)

        chest = Chest(x=300, y=300, height=100, width=90, status='close', loot=sword, directory='textures/chest/chest.png/')

        room = Room(objs=[chest, monster_mistake, monster_mistake2, slizn], land='test_room.csv', block_size=50,respawn=(150, 200), zones=[], room_id=1) 

        door1 = Door(x=950, y=710, height=90, width=100, status='close', directory='textures/doors/tree_door.png/', teleport=2, new_x=150, new_y=200)
        room.objs.append(door1)

        room.build()
        return room
    
    def room2(self):
        '''комната с пешкой'''
        wall_door = Wall_door(x=900, y=600, height=100, width=100, status='close', directory='textures/door.png/', teleport=None, key_index=1, world=self)

        wall_door2 = Wall_door(x=850, y=700, height=100, width=100, status='close', directory='textures/door.png/', teleport=None, key_index=1, angle=90, world=self)

        slizn = Monster(x=350, y=350, height=50, width=50, img='textures/slizn/0.png', direction='right',
                          status='run', directory_stand='textures/slizn', directory_run='textures/slizn',
                          directory_attack='textures/slizn',
                          road=[(400, 400), (450, 450), (450, 450)], health=4, directory_health='textures/hp', health_width=50, shift_health=0, speed=0.5, attention_zone=100, damage=1)
        
        pawn = Monster(x=350, y=150, height=80, width=50, img='textures/pawn_stay.png/0.png', direction='right', 
                       status='run', directory_stand='textures/pawn_stay.png', directory_run='textures/pawn_walk.png', 
                       directory_attack='textures/pawn_attack.png', 
                       road=[(0, 150), (800, 150)], health=50, directory_health='textures/hp', health_width=50, shift_health=35, speed=5, attention_zone=500, damage=3, shift_health_y=-10)

        monster_purple = Monster(x=274, y=750, height=150, width=100, img='textures/purple_stay.png/0.png', direction='right',
                          status='run', directory_stand='textures/purple_stay.png', directory_run='textures/purple_walk.png',
                          directory_attack='textures/purple_attack.png',
                          road=[(450, 350), (0, 350), (5, 750), (450, 750)], health=20, directory_health='textures/hp', health_width=100, shift_health=35, speed=2, attention_zone=400, damage=2)

        key = Key(height=100, width=100, x=340, y=340, img='key.png', index=1)

        chest = Chest(x=1000, y=150, height=100, width=90, status='close', loot=key, directory='textures/chest/chest.png/')

        room = Room(objs=[chest, monster_purple, slizn, wall_door, pawn, wall_door2], land='test_room2.csv', block_size=50,respawn=(950, 710), zones=[], room_id=2)
        
        telezone = Telezone(x=0, y=250, height=1, width=1, teleport=4, texture='textures/floor/dirt_8.png', new_x=1181, new_y=150, angle=90)
        telezone2 = Telezone(x=715, y=860, height=1, width=1, teleport=1, texture='textures/floor/dirt_8.png', new_x=150, new_y=200, angle=90)
        room.zones.append(telezone2)

        room.zones.append(telezone)

        room.build()
        return room

    def room3(self):
        '''комната с Аликджо'''
        trees = []
        sosnas_coord = [(1100, 300), (178, 603), (752, 440), (1105, 598)]
        oaks_coord = [(393, 605), (868, 590), (824, 130)]
        for x,y in sosnas_coord:
            trees.append(Tree(texture='textures/tree/sosna.png', x=x, y=y, height=488/4, width=800/4, tree_mask='textures/tree/sosna_mask.png'))
        for x,y in oaks_coord:
            trees.append(Tree(texture='textures/tree/oak.png', x=x, y=y, height=606/4, width=800/4, tree_mask='textures/tree/oak_mask.png'))
        phrases = dialogue_tree
        
        alicjo_npc = Dialogue_npc(x=629, y=644, height=840/4, width=444/4, direction='left',
                                 directory_stand='textures/alicjo-animated.png', 
                                 text=phrases, dialogue_status='sit', shift_x=130, shift_y=100, attention_zone=300,
                                   dialogue_x=50, dialogue_y=550, dialogue_height=250, dialogue_width=300)
        
        room = Room(objs=[], land='test_room3.csv', block_size=50, respawn=(850, 810), zones=[], room_id=3)
        room.objs += trees
        room.objs.append(alicjo_npc)
        room.build()
        x=700
        for i in range(7):
            path = Floor(texture='textures/floor/path.png', x=x, y=310, height=130, width=130, angle=90)
            room.load_land.append(path) 
            x+=130 
        telezone = Telezone(x=0, y=350, height=1, width=1, teleport=4, texture='textures/floor/dirt_8.png', new_x=1181, new_y=683, angle=90)
        path_telezone = Telezone(x=1411, y=370, height=1, width=1, teleport=5, texture='textures/floor/path.png', new_x=40, new_y=400, angle=90)
        room.zones.append(path_telezone)
        room.zones.append(telezone)
        return room

    def room4(self):
        '''корридор'''
        room = Room(objs=[], land='corridor.csv', block_size=50, respawn=(850, 100), zones=[], room_id=4)
        room.build()
        telezone = Telezone(x=37, y=148, height=1, width=1, teleport=2, texture='textures/floor/dirt_8.png', new_x=1180, new_y=650, angle=90)
        telezone2 = Telezone(x=1332, y=813, height=1, width=1, teleport=3, texture='textures/floor/dirt_8.png', new_x=165, new_y=355, angle=90)
        room.zones.append(telezone)
        room.zones.append(telezone2)
        return room
    
    def village_enter(self):
        '''вход в деревню'''
        room = Room(objs=[], land='village_enter.csv', block_size=150, respawn=(250, 100), zones=[], room_id=5)

        pink_house2 = House(texture='textures/pink_house.png', x=583, y=120, height=232*1.5, width=210*1.5)
        pink_house3 = House(texture='textures/pink_house.png', x=1058, y=120, height=232*1.5, width=210*1.5)
        pink_house5 = House(texture='textures/pink_house.png', x=583, y=550, height=232*1.5, width=210*1.5)
        pink_house6 = House(texture='textures/pink_house.png', x=1058, y=550, height=232*1.5, width=210*1.5)
        black_men_npc = Talking_npc(x=179, y=293, height=128, width=128, direction='left', directory_stand='textures/npc/black_men.png', 
                                    attention_zone=100, text={'start':{'text':'хорошая погодка сегодня,\n надо бы поработать на поле'}}, text_size=25, shift_x=120, shift_y=100)

        room.objs.append(black_men_npc)
        room.objs.append(pink_house2)
        room.objs.append(pink_house3)
        room.objs.append(pink_house5)
        room.objs.append(pink_house6)

        telezone = Telezone(x=1330, y=474, height=1, width=1, teleport=6, texture='textures/floor/dirt_8.png', new_x=40, new_y=400, angle=90)
        room.zones.append(telezone)
        room.build()

        x=0
        for i in range(7):
            path = Floor(texture='textures/floor/path.png', x=x, y=360, height=230, width=230, angle=90)
            room.load_land.append(path) 
            x+=230
        return room

    def chicken_village(self):
        '''локация с курицами'''
        phrases = chicken_tree
        chickens = []
        chickens_coord = [(100, 300), (178, 603), (752, 440), (705, 598), (200, 200), (341, 703), (654, 400), (588, 250), (197, 690)]
        room = Room(objs=[], land='chicken_village.csv', block_size=150, respawn=(250, 100), zones=[], room_id=6)
        for x,y in chickens_coord:
            chickens.append(Chicken(x=x, y=y, height=60, width=70, direction='left', directory_stand='textures/animals/chicken_stay.png',
                          directory_run='textures/animals/chicken_run.png', directory_walk='textures/animals/chicken_walk.png',
                            directory_eat='textures/animals/chicken_eat.png', attention_zone=100, speed=0.5))
        
        chicken_seller = Chicken_mission(x=1100, y=300, height=300, width=300, direction='right', directory_stand='textures/chicken_seller/chicken0',
                                      attention_zone=300, text=phrases, shift_x=100, shift_y=150, dialogue_status='dialogue_stand', dialogue_x=1000, dialogue_y=650, 
                                      dialogue_height=200, dialogue_width=400, text_size=25, dialogue_cloud=(400, 250))

        room.objs.append(chicken_seller)
        room.objs += chickens


        room.build()
        return room

#класс персонажа
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, img, direction, status, room, directory_stand, directory_run, health, world, speed) -> None: 
        super().__init__()
        self.dialogue_counter = 0
        self.x = x
        self.y = y
        self.dialogue = Dialogue(window=window, text='', x=0, y=0, height=0, width=0)
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
        self.gui = GUI(100, 1500, self, 500, 'textures/hp/')
        #получение изображения
        self.image = pygame.image.load(img) 
        self.image = pygame.transform.scale(self.image, (height, width)) 
        self.image_mask = pygame.mask.from_surface(self.image)
        self.textures_stand = self.get_files_names(directory_stand)
        self.textures_run = self.get_files_names(directory_run) 
        self.textures_stand = self.load_textures(self.textures_stand, height, width) 
        self.textures_run = self.load_textures(self.textures_run, height, width)
        self.textures_sit = self.get_files_names('textures/bonfire_sit/')
        self.textures_sit = self.load_textures(self.textures_sit, height, width)
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
            if os.path.isfile(path) and path[-3::]=='png':
                files_list.append(path) 
        files_list.sort()
        return files_list
    
    def control(self):
        keys = pygame.key.get_pressed() 
        safe_x, safe_y = self.x, self.y
        if keys[pygame.K_v]:
            sys.exit()
        if self.status not in ('sit', 'dialogue_stand'):
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
        if self.status == 'stand' or self.status == 'dialogue_stand':
            self.animation(self.textures_stand)
        elif self.status == 'run':
            self.animation(self.textures_run)
        elif self.status == 'sit':
            self.animation(self.textures_sit)

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
        if safe_x >= 1320:
            can_move_x = False
        if safe_y >= 800:
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
                            self.x = obj.new_x
                            self.y = obj.new_y
                            if obj.teleport == 1:
                                self.room = world.room1()
                            elif obj.teleport == 2:
                                self.room = world.room2()
                            elif obj.teleport == 3:
                                self.room = world.room3()
                            elif obj.teleport == 4:
                                self.room = world.room4()
                            
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
                    '''obj = Floor(texture=obj.texture_name[-1], x=obj.x, y=obj.y, height=obj.height, width=obj.width)
                    obj.image = pygame.transform.flip(obj.image, flip_x=True, flip_y=False)
                    self.room.load_land.append(obj)'''

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
            #взаимодействие с диалоговым нпс
            if isinstance(obj, Dialogue_npc):
                if offsetx <= obj.attention_zone and offsety <= obj.attention_zone:
                    if keys[pygame.K_e] and self.status != 'sit':
                        obj.status = 'dialogue'
                        self.status = obj.dialogue_status
                        self.dialogue_status = 'start'
                    if obj.status == 'dialogue':
                        self.dialogue_switch(obj)

            #взаимодействие с обычным НПС
            elif isinstance(obj, Talking_npc):
                if offsetx <= obj.attention_zone and offsety <= obj.attention_zone:
                    if keys[pygame.K_e]:
                        obj.status = 'dialogue'
        
        
        for zone in self.room.zones:
            zone_centerx = zone.x+zone.width/2
            zone_centery = zone.y+zone.height/2
            offsetx = abs(player_centerx - zone_centerx)
            offsety = abs(player_centery - zone_centery)
            #взаимодействие с телепорт зоной
            if isinstance(zone, Telezone):
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                    self.x = zone.new_x
                    self.y = zone.new_y
                    if zone.teleport == 1:
                        self.room = world.room1()
                    elif zone.teleport == 2:
                        self.room = world.room2()
                    elif zone.teleport == 3:
                        self.room = world.room3()
                    elif zone.teleport == 4:
                        self.room = world.room4()
                    elif zone.teleport == 5:
                        self.room = world.village_enter()
                    elif zone.teleport == 6:
                        self.room = world.chicken_village()

    def dialogue_switch(self, obj):
        try:
            npc_text = obj.text[self.dialogue_status]['text']
        except KeyError:
            self.dialogue_status = 'end'
            npc_text = obj.text[self.dialogue_status]['text']
        keys = pygame.key.get_pressed() 
        self.phrase = []
        self.variants = obj.text[self.dialogue_status]['options']
        for choice in self.variants:
            self.phrase.append(str(choice)+'. '+self.variants[choice]['response'])
        self.phrase = '\n\n'.join(self.phrase)
        if obj.dialogue_counter == len(npc_text):
            if self.dialogue_counter < len(self.phrase):
                self.dialogue_counter += 1
        self.dialogue = Dialogue(window=window, x=obj.dialogue_x, y=obj.dialogue_y, height=obj.dialogue_height, width=obj.dialogue_width, text=self.phrase[0:self.dialogue_counter])
        
        if self.dialogue_counter == len(self.phrase):
            #dialogue_level БОЛЬШЕ НЕ НУЖЕН!!!!!!!!!!!
            if keys[pygame.K_1] and 'end' in self.dialogue_status:
                obj.status = 'sit' 
                self.status = 'stand'
            elif keys[pygame.K_1]:
                obj.dialogue_level += 1
                obj.dialogue_counter = 0
                self.dialogue_counter = 0
                if 'next' in obj.text[self.dialogue_status]['options'][1]:
                    self.dialogue_status = obj.text[self.dialogue_status]['options'][1]['next'] #всегда теперь вот так
                else:
                    self.dialogue_status = 'end'
            elif keys[pygame.K_2]:
                obj.dialogue_level += 1
                obj.dialogue_counter = 0
                self.dialogue_counter = 0
                if 'next' in obj.text[self.dialogue_status]['options'][2]:
                    self.dialogue_status = obj.text[self.dialogue_status]['options'][2]['next']
                else:
                    self.dialogue_status = 'end'
            elif keys[pygame.K_3]:
                obj.dialogue_level += 1
                obj.dialogue_counter = 0
                self.dialogue_counter = 0
                if 'next' in obj.text[self.dialogue_status]['options'][3]:
                    self.dialogue_status = obj.text[self.dialogue_status]['options'][3]['next']
                else:
                    self.dialogue_status = 'end'
            
        obj.label = MultiLineText(x=obj.x-obj.shift_x, y=obj.y-obj.shift_y,
                                    height=22, font='font.ttf', color=(0, 0, 0), 
                                    text=npc_text[0:obj.dialogue_counter], window=window)
        if obj.dialogue_counter < len(npc_text):
            obj.dialogue_counter += 1

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
    def __init__(self, x, y, height, width, img, direction, status, directory_stand, directory_run, directory_attack,road, health, directory_health, health_width, shift_health, speed, attention_zone, damage, loot=None, shift_health_y=0) -> None:
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
        self.loot = loot

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
                                if obj.loot:
                                    player.room.objs.append(obj.loot)
                                    obj.loot.x = obj.x + 100
                                    obj.loot.y = obj.y + 0 
                                self.room.objs.remove(obj)
                            
                            break
                        #удар по монстру(справа)
                    elif self.direction == 'right':
                        overlap_area = self.sword_mask_right.overlap_area(obj.image_mask_run, (offsetx, offsety))
                        if overlap_area > 0 and self.counter == 4:
                            obj.health -= 1
                            obj.textures_health['left'][0][0] = pygame.transform.scale(obj.textures_health['left'][0][0], (obj.health_width/obj.max_health*obj.health, 10))
                            if obj.health == 0:
                                if obj.loot:
                                    player.room.objs.append(obj.loot)
                                    obj.loot.x = obj.x + 100
                                    obj.loot.y = obj.y + 0 
                                self.room.objs.remove(obj)
                            break             

#класс комнаты
class Room():
    '''комната'''
    def __init__(self, objs, land, respawn, zones, room_id, block_size) -> None:
        self.objs = objs
        self.block_size = block_size
        self.zones = zones
        self.land = land 
        self.load_land = []
        self.respawn = respawn
        self.room_id = room_id

    def show(self):
        for floor in self.load_land:
            floor.show_image() 
        for zone in self.zones:
            zone.show_image()
        

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
                        self.load_land.append(Floor(texture='textures/floor/dirt_3.png', x=x, y=y, height=self.block_size, width=self.block_size))
                    elif el == 'W':
                        self.objs.append(Wall(texture='textures/wall/wood_floor.png', x=x, y=y, height=self.block_size, width=self.block_size))
                    elif el == 'S':
                        self.load_land.append(Floor(texture='textures/floor/dirt_8.png', x=x, y=y, height=self.block_size, width=self.block_size))
                    elif el == 'R':
                        self.objs.append(Wall(texture='textures/wall/R_wall.png', x=x, y=y, height=self.block_size, width=self.block_size))
                    elif el == 'G':
                        self.load_land.append(Floor(texture='textures/floor/forest_grass.jpg', x=x, y=y, height=self.block_size, width=self.block_size))
                    elif el == 'PS':
                        self.load_land.append(Floor(texture='textures/floor/grass1.jpeg', x=x, y=y, height=self.block_size, width=self.block_size))
                    x += self.block_size
                y += self.block_size

#класс пола
class Floor():
    '''пол'''
    def __init__(self, texture, x, y, height, width, angle=0) -> None:
        self.texture = texture
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        #получение изображения
        self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (self.height, self.width)) 
        self.image = pygame.transform.rotate(self.image, angle)

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
        self.label = Label(x=850, y=25, height=50, font='font.ttf', color=(255, 255, 255), text='HP:')

        self.textures_health = player.get_files_names(directory_health)
        self.textures_health = player.load_textures(self.textures_health, height=500, width=50) 
    def show_image(self):
        pygame.draw.rect(window, (0, 0, 0), self.rect_background)
        self.label.show_image()
        window.blit(self.textures_health['left'][1][0], (900, 25)) #свойство для x 
        window.blit(self.textures_health['left'][0][0], (900, 25))

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
    def __init__(self, x, y, height, width, status, directory, teleport, new_x, new_y, angle=0) -> None:
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
        self.new_x = new_x
        self.new_y = new_y
        self.angle = angle

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
                image = pygame.transform.rotate(image, self.angle)
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
    def __init__(self, x, y, height, width, status, directory, teleport, key_index, world, new_x=None, new_y=None, angle=0) -> None:
        super().__init__(x, y, height, width, status, directory, teleport, new_x, new_y, angle)
        self.key_index = key_index
        self.world = world
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
            a = self
            self = Floor(texture=obj.texture_name[-1], x=obj.x, y=obj.y, height=obj.height, width=obj.width)
            self.image = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
            self.image = pygame.transform.rotate(self.image, a.angle)
            player.room.load_land.append(self)
    
    def show_image(self):
        window.blit(self.image, (self.x, self.y))
        if self.door_open == True:
            self.animation() 

#зона перехода
class Telezone():
    def __init__(self, x, y, height, width, teleport, texture, new_x, new_y, angle=0) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.teleport = teleport
        self.new_x = new_x
        self.new_y = new_y
        #получение изображения
        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (self.height, self.width)) 
        self.image = pygame.transform.rotate(self.image, angle)
    def show_image(self):
        window.blit(self.image, (self.x, self.y))
    
#деревья
class Tree(Floor):
    def __init__(self, texture, x, y, height, width, tree_mask, angle=0) -> None:
        super().__init__(texture, x, y, height, width, angle)
    
        self.tree_mask = pygame.image.load(tree_mask) 
        self.tree_mask = pygame.transform.scale(self.tree_mask, (height, width)) 
        self.image_mask = pygame.mask.from_surface(self.tree_mask)

#НПС
class Npc():
    def __init__(self, x, y, height, width, direction, directory_stand, attention_zone) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.direction = direction
        self.animation_counter = 5
        self.counter = 0
        self.attention_zone = attention_zone
        

        #получение изображения
        self.textures_stand = self.get_files_names(directory_stand)
        self.textures_stand = self.load_textures(self.textures_stand, height, width) 
        self.image = self.textures_stand[self.direction][0][0]
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

    def get_files_names(self, directory):
        # Список, который будет содержать имена файлов
        files_list = []
        # Проходим по всем элементам в директории
        for filename in os.listdir(directory):
            # Полный путь к файлу
            path = os.path.join(directory, filename)
        # Проверяем, является ли элемент файлом, и если да, добавляем его в список
            if os.path.isfile(path) and path[-3::]=='png':

                files_list.append(path) 
        '''Эта функция использует lambda-функцию в качестве ключа для сортировки. 
        Она извлекает число из имени файла и сортирует список по этим числам.'''
        files_list = sorted(files_list, key=lambda x: int(x.split("/")[-1].split(".")[0][49:]))

        return files_list

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

    def show_image(self):
        window.blit(self.image, (self.x, self.y))
        self.animation(self.textures_stand)

#НПС с одной фразой
class Talking_npc(Npc):
    def __init__(self, x, y, height, width, direction, directory_stand, attention_zone, text, shift_x, shift_y, text_size=22, dialogue_cloud=(400, 200)) -> None:
        super().__init__(x, y, height, width, direction, directory_stand, attention_zone)
        self.dialogue_cloud = 'textures/pixel_dialog.png'    
        self.dialogue_image = pygame.image.load(self.dialogue_cloud)
        self.dialogue_image = pygame.transform.scale(self.dialogue_image, dialogue_cloud)
        self.dialogue_counter = 0
        self.status = None
        self.text = text
        self.shift_x, self.shift_y = shift_x, shift_y
        self.label = MultiLineText(x=self.x-self.shift_x, y=self.y-self.shift_y,
                                    height=text_size, font='font.ttf', color=(0, 0, 0), text=self.text['start']['text'], window=window)

    def show_image(self):
        self.show_dialogue()
        window.blit(self.image, (self.x, self.y))
        self.animation(self.textures_stand)
    
    def show_dialogue(self):
        if self.status == 'dialogue':
            self.dialogue_counter += 1
            window.blit(self.dialogue_image, (self.x-25-self.shift_x, self.y-50-self.shift_y))
            self.label.show_image()
            if self.dialogue_counter >= 300:
                self.dialogue_counter = 0
                self.status = None

#НПС с диалогами
class Dialogue_npc(Talking_npc):
    def __init__(self, x, y, height, width, direction, directory_stand, attention_zone, text, shift_x, shift_y,
                  dialogue_status, dialogue_x, dialogue_y, dialogue_height, dialogue_width, text_size=22, dialogue_cloud=(400,200)) -> None:
        super().__init__(x, y, height, width, direction, directory_stand, attention_zone, text, shift_x, shift_y, text_size, dialogue_cloud)
        self.dialogue_counter = 0
        self.dialogue_level  = 0
        self.dialogue_status = dialogue_status
        self.dialogue_x, self.dialogue_y, self.dialogue_height, self.dialogue_width = dialogue_x, dialogue_y, dialogue_height, dialogue_width
    def show_dialogue(self):
        if self.status == 'dialogue':
            window.blit(self.dialogue_image, (self.x-30-self.shift_x, self.y-70-self.shift_y))
            self.label.show_image()

#миссия с курицами
class Chicken_mission(Dialogue_npc):
    def __init__(self, x, y, height, width, direction, directory_stand, attention_zone, text, shift_x, shift_y,
                  dialogue_status, dialogue_x, dialogue_y, dialogue_height, dialogue_width, text_size=22, dialogue_cloud=(400, 200)) -> None:
        super().__init__(x, y, height, width, direction, directory_stand, attention_zone, text, shift_x,
                          shift_y, dialogue_status, dialogue_x, dialogue_y, dialogue_height, dialogue_width, text_size, dialogue_cloud)
        self.chicken_counter = 0
        self.catch_zone = 200
        
    def interact_with_chickens(self):
        for obj in player.room.objs:
            if isinstance(obj, Chicken):
                chicken_centerx = obj.x+obj.width/2
                chicken_centery = obj.y+obj.height/2
                seller_centerx = self.x+self.width/2
                seller_centery = self.y+self.height/2
                offsetx = abs(seller_centerx - chicken_centerx)
                offsety = abs(seller_centery - chicken_centery)
                if offsetx <= self.catch_zone and offsety <= self.catch_zone:
                    player.room.objs.remove(obj)

    def show_image(self):
        self.show_dialogue()
        self.interact_with_chickens()
        window.blit(self.image, (self.x, self.y))
#дома
class House(Floor):
    def __init__(self, texture, x, y, height, width, angle=0) -> None:
        super().__init__(texture, x, y, height, width, angle)
        self.image_mask = pygame.mask.from_surface(self.image)
    
#курица 
class Chicken(Npc):
    def __init__(self, x, y, height, width, direction, directory_stand, directory_run, directory_walk, directory_eat, attention_zone, speed) -> None:
        super().__init__(x, y, height, width, direction, directory_stand, attention_zone)
        self.speed = speed
        self.status = 'walk'
        self.borderx = [10, 890]
        self.bordery = [115, 880]
        self.dot = [randint(self.borderx[0], self.borderx[1]), randint(self.bordery[0], self.bordery[1])]
        #получение изображения
        self.textures_run = self.get_files_names(directory_run)
        self.textures_run = self.load_textures(self.textures_run, height, width) 
        self.textures_walk = self.get_files_names(directory_walk)
        self.textures_walk = self.load_textures(self.textures_walk, height, width) 
        self.textures_eat = self.get_files_names(directory_eat)
        self.textures_eat = self.load_textures(self.textures_eat, height, width) 
        self.image = self.textures_stand[self.direction][0][0]
        self.image_mask = pygame.mask.from_surface(self.image)
    
    def show_image(self):
        self.chicken_AI()
        if self.status == 'walk':
            self.chicken_walk()
            textures = self.textures_walk
        elif self.status == 'run':
            self.chicken_run()
            textures = self.textures_run
        
        self.animation(textures)
        window.blit(self.image, (self.x, self.y))

    def chicken_walk(self):
        #хотьба курицы
        self.angle = math.atan2(self.y - self.dot[1], self.dot[0] - self.x)
        self.x += self.speed * math.cos(self.angle)
        self.y -= self.speed * math.sin(self.angle)

        if self.x < self.dot[0]:
            self.direction = 'right'
        elif self.x > self.dot[0]:
            self.direction = 'left'
        if int(self.y) in list(range(self.dot[1]-10, self.dot[1]+10)) and int(self.x) in list(range(self.dot[0]-10, self.dot[0]+10)):
            self.dot[0] = randint(self.borderx[0], self.borderx[1])
            self.dot[1] = randint(self.bordery[0], self.bordery[1])

    def chicken_run(self):
        chicken_centerx = self.x+self.width/2
        chicken_centery = self.y+self.height/2
        player_centerx = player.x+player.width/2
        player_centery = player.y+player.height/2

        if player_centerx < chicken_centerx:
            self.x += 5
            self.direction = 'right'
            if player_centerx < self.borderx[1]:
                self.dot[0] = randint(int(player_centerx), self.borderx[1])
        if player_centerx > chicken_centerx:
            self.x -= 5
            self.direction = 'left'
            self.dot[0] = randint(self.borderx[0]-50, int(player_centerx))
        if player_centery < chicken_centery:
            self.y += 5
        if player_centery > chicken_centery:
            self.y -= 5

    def chicken_AI(self):
        chicken_centerx = self.x+self.width/2
        chicken_centery = self.y+self.height/2
        player_centerx = player.x+player.width/2
        player_centery = player.y+player.height/2
        offsetx = abs(player_centerx - chicken_centerx)
        offsety = abs(player_centery - chicken_centery)
        if offsetx <= self.attention_zone and offsety <= self.attention_zone:
            self.status = 'run'
        else:
            self.status = 'walk'


#отоброжение текстур
world = World()        
player = world.hero
#основной игровой цикл (абстракция)
while True: 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            print(f'{x=}, {y=}')
                
        if event.type == pygame.QUIT:
            sys.exit()
    player.room.show()
    player.show_image()
    for obj in player.room.objs:
        obj.show_image()
        if player.status in ('sit', 'dialogue_stand'):
            player.dialogue.show_rect()
    player.interact_with_items()
    player.gui.show_image() 
    clock.tick(60)
    pygame.display.update() 

