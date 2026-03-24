import pygame
import random
from enum import Enum

pygame.init()

# 상수 정의
SCREEN_WIDTH = 600
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = SCREEN_WIDTH // GRID_WIDTH  # 60
INFO_PANEL_HEIGHT = 100
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE + INFO_PANEL_HEIGHT  # 1300

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# 테트로미노 정의 (7가지)
TETROMINOES = {
    'I': {
        'shape': [[1, 1, 1, 1]],
        'color': CYAN
    },
    'O': {
        'shape': [[1, 1], [1, 1]],
        'color': YELLOW
    },
    'T': {
        'shape': [[0, 1, 0], [1, 1, 1]],
        'color': PURPLE
    },
    'S': {
        'shape': [[0, 1, 1], [1, 1, 0]],
        'color': GREEN
    },
    'Z': {
        'shape': [[1, 1, 0], [0, 1, 1]],
        'color': RED
    },
    'J': {
        'shape': [[1, 0, 0], [1, 1, 1]],
        'color': BLUE
    },
    'L': {
        'shape': [[0, 0, 1], [1, 1, 1]],
        'color': ORANGE
    }
}


class Tetromino:
    def __init__(self, shape_type):
        self.type = shape_type
        self.shape = [row[:] for row in TETROMINOES[shape_type]['shape']]
        self.color = TETROMINOES[shape_type]['color']
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        """시계방향으로 90도 회전"""
        self.shape = [[self.shape[len(self.shape) - 1 - j][i] 
                      for j in range(len(self.shape))]
                      for i in range(len(self.shape[0]))]

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_down(self):
        self.y += 1


class TetrisGame:
    def __init__(self, width=GRID_WIDTH, height=GRID_HEIGHT):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = Tetromino(random.choice(list(TETROMINOES.keys())))
        self.next_piece = Tetromino(random.choice(list(TETROMINOES.keys())))
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.clock = pygame.time.Clock()
        self.fall_speed = 30  # 프레임 수

    def is_collision(self, piece=None, x=None, y=None):
        """충돌 감지"""
        if piece is None:
            piece = self.current_piece
        if x is None:
            x = piece.x
        if y is None:
            y = piece.y

        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = x + j
                    new_y = y + i

                    # 경계 체크
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return True

                    # 바닥만 체크 (위로는 통과 가능)
                    if new_y >= 0 and new_y < self.height:
                        if new_x >= 0 and new_x < self.width:
                            if self.board[new_y][new_x]:
                                return True

        return False

    def lock_piece(self):
        """현재 피스를 보드에 고정"""
        piece = self.current_piece
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = piece.x + j
                    y = piece.y + i
                    if 0 <= y < self.height and 0 <= x < self.width:
                        self.board[y][x] = piece.color

        self.clear_lines()
        self.current_piece = self.next_piece
        self.next_piece = Tetromino(random.choice(list(TETROMINOES.keys())))

        # 게임 오버 체크
        if self.is_collision():
            self.game_over = True

    def clear_lines(self):
        """완성된 라인 제거"""
        lines_to_clear = []
        for i in range(self.height):
            if all(self.board[i]):
                lines_to_clear.append(i)

        for line in lines_to_clear:
            del self.board[line]
            self.board.insert(0, [0 for _ in range(self.width)])

        # 점수 계산
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            points = [0, 100, 300, 500, 800]
            self.score += points[len(lines_to_clear)] * self.level
            self.level = 1 + self.lines_cleared // 10

    def move_piece_left(self):
        """피스를 왼쪽으로 이동"""
        test_piece = Tetromino(self.current_piece.type)
        test_piece.shape = [row[:] for row in self.current_piece.shape]
        test_piece.x = self.current_piece.x - 1
        test_piece.y = self.current_piece.y

        if not self.is_collision(test_piece, test_piece.x, test_piece.y):
            self.current_piece.move_left()

    def move_piece_right(self):
        """피스를 오른쪽으로 이동"""
        test_piece = Tetromino(self.current_piece.type)
        test_piece.shape = [row[:] for row in self.current_piece.shape]
        test_piece.x = self.current_piece.x + 1
        test_piece.y = self.current_piece.y

        if not self.is_collision(test_piece, test_piece.x, test_piece.y):
            self.current_piece.move_right()

    def rotate_piece(self):
        """피스를 회전"""
        test_piece = Tetromino(self.current_piece.type)
        test_piece.shape = [row[:] for row in self.current_piece.shape]
        test_piece.x = self.current_piece.x
        test_piece.y = self.current_piece.y
        test_piece.rotate()

        if not self.is_collision(test_piece, test_piece.x, test_piece.y):
            self.current_piece.rotate()

    def drop_piece(self):
        """피스를 한칸 아래로"""
        test_piece = Tetromino(self.current_piece.type)
        test_piece.shape = [row[:] for row in self.current_piece.shape]
        test_piece.x = self.current_piece.x
        test_piece.y = self.current_piece.y + 1

        if self.is_collision(test_piece, test_piece.x, test_piece.y):
            self.lock_piece()
        else:
            self.current_piece.move_down()

    def update(self):
        """게임 상태 업데이트"""
        if not self.game_over:
            self.drop_piece()

    def draw_board(self, surface):
        """게임 보드 그리기"""
        # 배경
        pygame.draw.rect(surface, BLACK, (0, INFO_PANEL_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - INFO_PANEL_HEIGHT))

        # 그리드
        for i in range(self.height + 1):
            pygame.draw.line(surface, GRAY, (0, INFO_PANEL_HEIGHT + i * BLOCK_SIZE),
                           (SCREEN_WIDTH, INFO_PANEL_HEIGHT + i * BLOCK_SIZE))
        for j in range(self.width + 1):
            pygame.draw.line(surface, GRAY, (j * BLOCK_SIZE, INFO_PANEL_HEIGHT),
                           (j * BLOCK_SIZE, SCREEN_HEIGHT))

        # 보드의 블록들
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j]:
                    pygame.draw.rect(surface, self.board[i][j],
                                   (j * BLOCK_SIZE, INFO_PANEL_HEIGHT + i * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE))
                    pygame.draw.rect(surface, BLACK,
                                   (j * BLOCK_SIZE, INFO_PANEL_HEIGHT + i * BLOCK_SIZE,
                                    BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self, surface):
        """현재 피스 그리기"""
        piece = self.current_piece
        for i, row in enumerate(piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    x = piece.x + j
                    y = piece.y + i
                    if y >= 0:
                        pygame.draw.rect(surface, piece.color,
                                       (x * BLOCK_SIZE, INFO_PANEL_HEIGHT + y * BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE))
                        pygame.draw.rect(surface, BLACK,
                                       (x * BLOCK_SIZE, INFO_PANEL_HEIGHT + y * BLOCK_SIZE,
                                        BLOCK_SIZE, BLOCK_SIZE), 2)

    def draw_info(self, surface):
        """정보 패널 그리기"""
        font_large = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        pygame.draw.rect(surface, GRAY, (0, 0, SCREEN_WIDTH, INFO_PANEL_HEIGHT))
        pygame.draw.line(surface, WHITE, (0, INFO_PANEL_HEIGHT), (SCREEN_WIDTH, INFO_PANEL_HEIGHT), 2)

        # 점수
        score_text = font_large.render(f'Score: {self.score}', True, WHITE)
        surface.blit(score_text, (10, 10))

        # 레벨
        level_text = font_small.render(f'Level: {self.level}', True, WHITE)
        surface.blit(level_text, (10, 50))

        # 라인
        lines_text = font_small.render(f'Lines: {self.lines_cleared}', True, WHITE)
        surface.blit(lines_text, (250, 50))

        # 다음 피스
        next_text = font_small.render('Next:', True, WHITE)
        surface.blit(next_text, (450, 10))

        # 다음 피스 미리보기
        for i, row in enumerate(self.next_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(surface, self.next_piece.color,
                                   (450 + j * 20, 40 + i * 20, 20, 20))
                    pygame.draw.rect(surface, BLACK,
                                   (450 + j * 20, 40 + i * 20, 20, 20), 1)

    def draw_game_over(self, surface):
        """게임 오버 화면"""
        font = pygame.font.Font(None, 72)
        game_over_text = font.render('GAME OVER', True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        
        pygame.draw.rect(surface, BLACK, (text_rect.x - 20, text_rect.y - 20,
                                         text_rect.width + 40, text_rect.height + 40))
        pygame.draw.rect(surface, RED, (text_rect.x - 20, text_rect.y - 20,
                                       text_rect.width + 40, text_rect.height + 40), 3)
        surface.blit(game_over_text, text_rect)

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render('Press SPACE to Restart or Q to Quit', True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        surface.blit(restart_text, restart_rect)

    def reset(self):
        """게임 리셋"""
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.current_piece = Tetromino(random.choice(list(TETROMINOES.keys())))
        self.next_piece = Tetromino(random.choice(list(TETROMINOES.keys())))
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    
    game = TetrisGame()
    fall_counter = 0
    
    running = True
    while running:
        game.clock.tick(60)  # 60 FPS

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece_left()
                elif event.key == pygame.K_RIGHT:
                    game.move_piece_right()
                elif event.key == pygame.K_UP:
                    game.rotate_piece()
                elif event.key == pygame.K_DOWN:
                    game.drop_piece()
                elif event.key == pygame.K_SPACE and game.game_over:
                    game.reset()
                elif event.key == pygame.K_q and game.game_over:
                    running = False

        # 게임 업데이트
        if not game.game_over:
            fall_counter += 1
            if fall_counter >= game.fall_speed - (game.level - 1) * 2:
                game.update()
                fall_counter = 0

        # 화면 그리기
        screen.fill(BLACK)
        game.draw_board(screen)
        game.draw_piece(screen)
        game.draw_info(screen)
        
        if game.game_over:
            game.draw_game_over(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
