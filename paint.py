import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

radius = 10              
color = (0, 0, 255)      
tool = "brush"            
start_pos = None         
drawing = False           


def draw_rectangle(screen, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
    pygame.draw.rect(screen, color, rect, width)

def draw_circle(screen, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    radius = int(((x2-x1)**2 + (y2-y1)**2)**0.5)
    pygame.draw.circle(screen, color, start, radius, width)

def draw_square(screen, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2-x1), abs(y2-y1))


    sign_x = 1 if x2 - x1 >= 0 else -1
    sign_y = 1 if y2 - y1 >= 0 else -1

    rect = pygame.Rect(x1, y1, sign_x*side, sign_y*side)
    pygame.draw.rect(screen, color, rect, width)

def draw_right_triangle(screen, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end
    points = [(x1,y1), (x2,y1), (x1,y2)]
    pygame.draw.polygon(screen, color, points, width)

def draw_equilateral_triangle(screen, start, end, color, width=2):
    
    x1, y1 = start
    x2, y2 = end

    side = abs(x2 - x1)   

    h = side * (3**0.5) / 2  


    p1 = (x1, y1)
    p2 = (x1 + side, y1)
    p3 = (x1 + side/2, y1 - h)

    pygame.draw.polygon(screen, color, [p1, p2, p3], width)

def draw_rhombus(screen, start, end, color, width=2):
    x1, y1 = start
    x2, y2 = end

    dx = x2 - x1
    dy = y2 - y1

    points = [
        (x1, y1 - abs(dy)),  
        (x1 + abs(dx), y1),  
        (x1, y1 + abs(dy)),   
        (x1 - abs(dx), y1)    
    ]
    pygame.draw.polygon(screen, color, points, width)


def main():
    global color, radius, tool, start_pos, drawing

    canvas = pygame.Surface(screen.get_size())
    canvas.fill((0,0,0))

    while True:
        screen.blit(canvas, (0,0))
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            #Выбор инструментов
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: tool = "brush"
                elif event.key == pygame.K_2: tool = "rect"
                elif event.key == pygame.K_3: tool = "circle"
                elif event.key == pygame.K_4: tool = "eraser"
                elif event.key == pygame.K_5: tool = "square"
                elif event.key == pygame.K_6: tool = "tri_right"
                elif event.key == pygame.K_7: tool = "tri_eq"
                elif event.key == pygame.K_8: tool = "rhombus"

                #Выбор цвета
                elif event.key == pygame.K_r: color = (255,0,0)
                elif event.key == pygame.K_g: color = (0,255,0)
                elif event.key == pygame.K_b: color = (0,0,255)
                elif event.key == pygame.K_w: color = (255,255,255)
                elif event.key == pygame.K_k: color = (0,0,0)

            #Мышь
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if tool == "rect":
                    draw_rectangle(canvas, start_pos, event.pos, color, 3)
                elif tool == "circle":
                    draw_circle(canvas, start_pos, event.pos, color, 3)
                elif tool == "square":
                    draw_square(canvas, start_pos, event.pos, color, 3)
                elif tool == "tri_right":
                    draw_right_triangle(canvas, start_pos, event.pos, color, 3)
                elif tool == "tri_eq":
                    draw_equilateral_triangle(canvas, start_pos, event.pos, color, 3)
                elif tool == "rhombus":
                    draw_rhombus(canvas, start_pos, event.pos, color, 3)

                drawing = False

        #Рисование кистью или ластиком
        if drawing:
            if tool == "brush":
                pygame.draw.circle(canvas, color, mouse, radius)
            elif tool == "eraser":
                pygame.draw.circle(canvas, (0,0,0), mouse, radius)

        
        if drawing and tool in ["rect", "circle", "square", "tri_right", "tri_eq", "rhombus"]:
            temp = canvas.copy()

            if tool == "rect": draw_rectangle(temp, start_pos, mouse, color, 2)
            elif tool == "circle": draw_circle(temp, start_pos, mouse, color, 2)
            elif tool == "square": draw_square(temp, start_pos, mouse, color, 2)
            elif tool == "tri_right": draw_right_triangle(temp, start_pos, mouse, color, 2)
            elif tool == "tri_eq": draw_equilateral_triangle(temp, start_pos, mouse, color, 2)
            elif tool == "rhombus": draw_rhombus(temp, start_pos, mouse, color, 2)

            screen.blit(temp, (0,0))

        
        show_text = pygame.font.SysFont("Arial", 18).render(
            f"Tool: {tool.upper()} | 1-Brush 2-Rect 3-Circle 4-Eraser 5-Square 6-RightTri 7-EqTri 8-Rhombus | Colors: R,G,B,W,K",
            True, (255,255,255))
        screen.blit(show_text, (10, 10))

        pygame.display.update()
        clock.tick(60)


main()