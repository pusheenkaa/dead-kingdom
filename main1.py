import pygame
from random import randint
import sys 
import os

pygame.init()

#создание окна
window = pygame.display.set_mode((1300, 900)) 
background_image = pygame.image.load('w.jpeg')
background_image = pygame.transform.scale(background_image, (1400, 800 )) 
clock =  pygame.time.Clock()

#главный класс всего
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, img, direction, status, room, directory_stay, directory_run) -> None: 
        super().__init__()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.direction = direction
        self.animation_counter = 5
        self.counter = 0
        self.speed = 5
        self.room = room #только перс
        self.active_zone = 70 #только перс
        #получение изображения
        self.image = pygame.image.load(img) 
        self.image = pygame.transform.scale(self.image, (height, width)) 
        self.image_mask = pygame.mask.from_surface(self.image)
        self.textures_stand = self.get_files_names(directory_stay)
        self.textures_run = self.get_files_names(directory_run) 
        self.textures_stand = self.load_textures(self.textures_stand) 
        self.textures_run = self.load_textures(self.textures_run)
        self.status = status 
        self.rect = self.image.get_rect()

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
    
    def load_textures(self, textures):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                '''print(texture)'''
                #загрузка изброжения
                image = pygame.image.load(texture)
                #отзеркаливание изображения
                image = pygame.transform.scale(image, (self.height, self.width))
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
    
    def collision(self, safe_x, safe_y ):
        can_move_x = True
        can_move_y = True
        for obj in self.room.objs:
            offsetx = obj.x - safe_x
            offsety = obj.y - self.y
            #отталкивание
            if self.image_mask_run.overlap_area(obj.image_mask, (offsetx, offsety)):
                can_move_x = False
                if self.direction == 'left' and self.x > obj.x:
                    self.x += 1
                if self.direction == 'right' and self.x < obj.x:
                    self.x -= 1 

                break
        for obj in self.room.objs:
            offsetx = obj.x - self.x
            offsety = obj.y - safe_y
            if self.image_mask_run.overlap_area(obj.image_mask, (offsetx, offsety)):
                can_move_y = False
                break
        self.interact_with_items() 
        return can_move_x, can_move_y
    
    def interact_with_items(self):
        keys = pygame.key.get_pressed() 
        for obj in self.room.objs:
            obj_centerx = obj.x+obj.width/2
            obj_centery = obj.y+obj.height/2
            player_centerx = self.x+obj.width/2
            player_centery = self.y+obj.height/2
            if isinstance(obj, Chest):
                offsetx = abs(player_centerx - obj_centerx)
                offsety = abs(player_centery - obj_centery)
                if offsetx <= self.active_zone and offsety <= self.active_zone:
                    if keys[pygame.K_e]:
                        if obj.status == 'close':
                            obj.a_f = True
        return obj_centerx, obj_centery, player_centerx, player_centery
#класс монстров
class Monster():
    def __init__(self, x, y, height, width, img, direction, status, directory_stay, directory_run, road) -> None:
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.direction = direction
        self.status = status
        self.animation_counter = 5
        self.counter = 0
        self.speed = 1
        self.attention_zone = 500
        self.road = road
        self.dot = 0
        self.direction_road = 1  # Начальное направление изменения точки

        #получение изображения
        self.image = pygame.image.load(img) 
        self.image = pygame.transform.scale(self.image, (height, width)) 
        self.image_mask = pygame.mask.from_surface(self.image)
        self.textures_stand = self.get_files_names(directory_stay)
        self.textures_run = self.get_files_names(directory_run) 
        self.textures_stand = self.load_textures(self.textures_stand) 
        self.textures_run = self.load_textures(self.textures_run)
        self.status = status 
        self.attention_flag = False

    def monster_walk(self):
        if self.x < self.road[self.dot][0]:
            self.x += self.speed
            self.direction = 'right'
        elif self.x > self.road[self.dot][0]:
            self.x -= self.speed
            self.direction = 'left'
        # движение вверх
        if self.y < self.road[self.dot][1]:
            self.y += self.speed
        elif self.y > self.road[self.dot][1]:
            self.y -= self.speed
        if self.y in range(self.road[self.dot][1]-10, self.road[self.dot][1]+10) and self.x in range(self.road[self.dot][0]-10, self.road[self.dot][0]+10):
            # Проверяем, достигли ли мы конца или начала списка
            if (self.dot == len(self.road) - 1 and self.direction_road == 1) or (self.dot == 0 and self.direction_road == -1):
                # Меняем направление
                self.direction_road *= -1
            self.dot += self.direction_road

    def monster_follow(self):
        if self.x < player.x:
            self.x += self.speed
            self.direction = 'right'
        elif self.x > player.x:
            self.x -= self.speed
            self.direction = 'left'
        # движение вверх
        if self.y < player.y:
            self.y += self.speed
        elif self.y > player.y:
            self.y -= self.speed
        if self.y in range(player.y-10, player.y+10) and self.x in range(player.x-10, player.x+10):
            pass



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

    def load_textures(self, textures):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                '''print(texture)'''
                #загрузка изброжения
                image = pygame.image.load(texture)
                #отзеркаливание изображения
                image = pygame.transform.scale(image, (self.height, self.width))
                if direction == 'left':                   
                    image = pygame.transform.flip(image, True, False)  
                image_mask = pygame.mask.from_surface(image)
                loaded_textures[direction].append([image, image_mask]) 
        return loaded_textures

    def show_image(self):
        #self.monster_walk()
        self.monster_follow()
        if self.status == 'stand':
            self.animation(self.textures_stand)
        elif self.status == 'run':
            self.animation(self.textures_run) 
        else:
            print(self.status)
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
    def __init__(self, x, y, height, width, img, direction, status, room, directory_stay, directory_run, directory_attack) -> None:
        super().__init__(x, y, height, width, img, direction, status, room, directory_stay, directory_run)
        self.textures_attack = self.get_files_names(directory_attack) 
        self.textures_attack = self.load_textures(self.textures_attack)
        self.sword_right = pygame.image.load('textures/utils/sword.png') 
        self.sword_right = pygame.transform.scale(self.image, (height, width)) 
        self.sword_mask_right = pygame.mask.from_surface(self.image)
        self.sword_left = pygame.transform.flip(self.image, True, False) 
        self.sword_mask_left = pygame.mask.from_surface(self.image)

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
            self.a_f = False 
            self.status = 'stay' 

    def interact_with_items(self):
        super().interact_with_items()
        for obj in self.room.objs:
            obj_centerx = obj.x+obj.width/2
            obj_centery = obj.y+obj.height/2
            player_centerx = self.x+obj.width/2
            player_centery = self.y+obj.height/2
            if isinstance(obj, Monster):
                offsetx = abs(player_centerx - obj_centerx)
                offsety = abs(player_centery - obj_centery) 
                if offsetx <= 100 and offsety <= 100:
                    print(offsetx, offsety)
                    #атака
                    if self.status == 'attack':
                        if self.direction == 'right':
                            if self.sword_mask_right.overlap_area(obj.image_mask,(offsetx, offsety)) > 0 and self.counter == 4:
                                self.room.objs.remove(obj)  
                        if self.direction == 'left':
                            if self.sword_mask_left.overlap_area(obj.image_mask,(offsetx, offsety)) > 0 and self.counter == 4:
                                self.room.objs.remove(obj)                         
#класс комнаты
class Room():
    '''комната'''
    def __init__(self, objs, land) -> None:
        self.objs = objs
        self.land = land 
        self.load_land = []

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
    def __init__(self, x, y, height, width, status, loot, directory_chest) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.status = status
        self.loot = loot
        self.textures = self.get_files_names(directory_chest)
        self.textures = self.load_textures(self.textures)
        self.counter = 0
        self.animation_counter = 5
        self.direction = 'left'
        self.a_f = False
        #получение изображения
        if self.status == 'open':
            self.image = self.textures['left'][len(self.textures)-4][0]
        elif self.status == 'close':
            self.image = self.textures['left'][0][0]
        self.image_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect() 

    def show_image(self):
        if self.a_f == False:
            if self.status == 'open':
                self.image = self.textures['left'][len(self.textures)-4][0] 
            elif self.status == 'close':
                self.image = self.textures['left'][0][0]
        elif self.a_f == True:
            self.animation() 
        window.blit(self.image, (self.x, self.y))

    #подгузка текстур
    def load_textures(self, textures):
        loaded_textures = {'left':[], 'right':[]}
        for direction in loaded_textures:
            for texture in textures:
                '''print(texture)'''
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
            self.a_f = False 
            self.status = 'open' 

class GUI():
    def __init__(self, height, width) -> None:
        self.rect_background = pygame.Rect(0, 0, width, height)

    def show_image(self):
        pygame.draw.rect(window, (0, 0, 0), self.rect_background)

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

#отоброжение текстур
chest2 = Chest(x=300, y=300, height=100, width=90, status='close', loot=None, directory_chest='textures/chest/chest.png/')
monster_mistake = Monster(x=675, y=650, height=150, width=100, img='textures/mistake_stay.png/0.png', direction='right',
                          status='run', directory_stay='textures/mistake_stay.png', directory_run='textures/mistake_walk',
                          road=[(500, 650), (675, 650), (675, 150)])
monster_mistake2 = Monster(x=875, y=650, height=150, width=100, img='textures/mistake_stay.png/0.png', direction='right',
                          status='run', directory_stay='textures/mistake_stay.png', directory_run='textures/mistake_walk',
                          road=[(900, 650), (1100, 650), (1100, 150)])
test_room = Room(objs=[chest2, monster_mistake, monster_mistake2], land='test_room.csv') 
hero = Player(x=675, y=550, height=150, width=100, img='textures/stay_no_weapon/1.png', direction='right',
               status='run', room=test_room, directory_stay='textures/stay_no_weapon/',
                        directory_run='textures/run_no_weapon/') 
sword_hero = Sword_player(
                        x=75, y=200, height=150, width=100, img='textures/stay_with_weapon/1.png', 
                        direction='right', status='run', room=test_room, directory_stay='textures/stay_with_weapon/',
                        directory_run='textures/run_with_weapon/', directory_attack='textures/sword_attack/' )
player = sword_hero
test_room.build()
gui = GUI(100, 1400)
test_label = Label(x=30, y=30, height=30, font='font.ttf', color=(255, 255, 255), text='тест текст')
#основной игровой цикл (абстракция)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    window.blit(background_image, (0, 0)) 

    test_room.show()
    for obj in hero.room.objs:
        obj.show_image()
    player.show_image()
    #hero.show_image()
    gui.show_image() 
    test_label.show_image()
    clock.tick(60)
    pygame.display.update() 

