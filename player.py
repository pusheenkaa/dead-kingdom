import pygame
from random import randint
import sys 
import os
from main import window, Chest
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, height, width, img, direction, status, room, directory_stand, directory_run) -> None: 
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
        self.textures_stand = self.get_files_names(directory_stand)
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
                '''if self.direction == 'left' and self.x > obj.x:
                    self.x += 1
                if self.direction == 'right' and self.x < obj.x:
                    self.x -= 1'''

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
