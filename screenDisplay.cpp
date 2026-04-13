#include <lvgl.h>
#include <Arduino_GFX_Library.h>
#include "TCA9554.h"
#include "TouchDrvFT6X36.hpp"

// Pin definitions
#define GFX_BL    6
#define SPI_MISO  2
#define SPI_MOSI  1
#define SPI_SCLK  5
#define LCD_CS   -1
#define LCD_DC    3
#define LCD_RST  -1
#define I2C_SDA   8
#define I2C_SCL   7

// UART to Pi
#define PI_TX    44
#define PI_RX    43

TCA9554 TCA(0x20);

Arduino_DataBus *bus = new Arduino_ESP32SPI(LCD_DC, LCD_CS, SPI_SCLK, SPI_MOSI, SPI_MISO);
Arduino_GFX *gfx = new Arduino_ST7796(bus, LCD_RST, 0, true, 320, 480);

TouchDrvFT6X36 touch;

uint32_t screenWidth, screenHeight, bufSize;
lv_disp_draw_buf_t draw_buf;
lv_color_t *disp_draw_buf1;
lv_color_t *disp_draw_buf2;
lv_disp_drv_t disp_drv;

// Game state
String gameMode = "";
int playerCount = 0;

// Forward declarations
void showTitleScreen();
void showPlayerCountScreen();
void showGameScreen();
void sendCommandToPi();

// ─── LVGL callbacks ───────────────────────────────────────

void my_disp_flush(lv_disp_drv_t *disp_drv, const lv_area_t *area, lv_color_t *color_p) {
  uint32_t w = (area->x2 - area->x1 + 1);
  uint32_t h = (area->y2 - area->y1 + 1);
  gfx->draw16bitRGBBitmap(area->x1, area->y1, (uint16_t *)&color_p->full, w, h);
  lv_disp_flush_ready(disp_drv);
}

void my_touchpad_read(lv_indev_drv_t *indev_drv, lv_indev_data_t *data) {
  int16_t x[1], y[1];
  uint8_t touched = touch.getPoint(x, y, 1);
  if (touched) {
    data->state = LV_INDEV_STATE_PR;
    data->point.x = y[0];
    data->point.y = 320 - x[0];
  } else {
    data->state = LV_INDEV_STATE_REL;
  }
}

void lcd_reset(void) {
  TCA.write1(1, 1);
  delay(10);
  TCA.write1(1, 0);
  delay(10);
  TCA.write1(1, 1);
  delay(200);
}

// ─── Game select callbacks ─────────────────────────────────

static void btn_holdem_cb(lv_event_t *e) {
  gameMode = "holdem";
  Serial.println("Selected: Hold Em");
  showPlayerCountScreen();
}

static void btn_5card_cb(lv_event_t *e) {
  gameMode = "5card";
  Serial.println("Selected: 5 Card Poker");
  showPlayerCountScreen();
}

static void btn_blackjack_cb(lv_event_t *e) {
  gameMode = "blkjk";
  Serial.println("Selected: Blackjack");
  showPlayerCountScreen();
}

// ─── Player count callback ─────────────────────────────────

static void btn_player_cb(lv_event_t *e) {
  playerCount = (int)(intptr_t)lv_event_get_user_data(e);
  Serial.print("Player count: ");
  Serial.println(playerCount);
  showGameScreen();
}

// ─── Send command to Pi ────────────────────────────────────

void sendCommandToPi() {
  String cmd = "GAME:" + gameMode + ",PLAYERS:" + String(playerCount) + "\n";
  Serial2.print(cmd);
  Serial.print("Sent to Pi: ");
  Serial.print(cmd);
}

// ─── Screens ──────────────────────────────────────────────

void showTitleScreen() {
  lv_obj_clean(lv_scr_act());
  lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  lv_obj_t *title = lv_label_create(lv_scr_act());
  lv_label_set_text(title, "V.E.G.A.S.");
  lv_obj_set_style_text_color(title, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 15);

  lv_obj_t *sub = lv_label_create(lv_scr_act());
  lv_label_set_text(sub, "Select a game:");
  lv_obj_set_style_text_color(sub, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(sub, LV_ALIGN_TOP_MID, 0, 40);

  // 3 buttons side by side
  lv_obj_t *btn1 = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btn1, 140, 80);
  lv_obj_set_pos(btn1, 10, 110);
  lv_obj_add_event_cb(btn1, btn_holdem_cb, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lbl1 = lv_label_create(btn1);
  lv_label_set_text(lbl1, "Hold 'em");
  lv_obj_center(lbl1);

  lv_obj_t *btn2 = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btn2, 140, 80);
  lv_obj_set_pos(btn2, 170, 110);
  lv_obj_add_event_cb(btn2, btn_5card_cb, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lbl2 = lv_label_create(btn2);
  lv_label_set_text(lbl2, "5 Card Poker");
  lv_obj_center(lbl2);

  lv_obj_t *btn3 = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btn3, 140, 80);
  lv_obj_set_pos(btn3, 330, 110);
  lv_obj_add_event_cb(btn3, btn_blackjack_cb, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lbl3 = lv_label_create(btn3);
  lv_label_set_text(lbl3, "Blackjack");
  lv_obj_center(lbl3);
}

void showPlayerCountScreen() {
  lv_obj_clean(lv_scr_act());
  lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  lv_obj_t *title = lv_label_create(lv_scr_act());
  lv_label_set_text(title, "How many players?");
  lv_obj_set_style_text_color(title, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 15);

  int nums[] = {2, 3, 4, 5, 6, 7, 8, 9, 10};
  int btnW = 140;
  int btnH = 70;
  int startX = 10;
  int startY = 50;
  int gapX = 10;
  int gapY = 10;

  for (int i = 0; i < 9; i++) {
    int col = i % 3;
    int row = i / 3;
    int x = startX + col * (btnW + gapX);
    int y = startY + row * (btnH + gapY);

    lv_obj_t *btn = lv_btn_create(lv_scr_act());
    lv_obj_set_size(btn, btnW, btnH);
    lv_obj_set_pos(btn, x, y);
    lv_obj_add_event_cb(btn, btn_player_cb, LV_EVENT_CLICKED, (void *)(intptr_t)nums[i]);
    lv_obj_t *lbl = lv_label_create(btn);
    lv_label_set_text_fmt(lbl, "%d Players", nums[i]);
    lv_obj_center(lbl);
  }
}

void showGameScreen() {
  lv_obj_clean(lv_scr_act());                    // Clear the current screen
  lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  // Route to the correct game-specific screen based on gameMode
  if (gameMode == "5card") {
    showPokerScreen();      // 5 Card Poker
  }
  else if (gameMode == "holdem") {
    showHoldScreen();       // Texas Hold'em
  }
  else if (gameMode == "blkjk") {
    showBlackjackScreen();  // Blackjack
  }
  else {
    // Fallback in case of error
    lv_obj_t *label = lv_label_create(lv_scr_act());
    lv_label_set_text(label, "Unknown Game Mode");
    lv_obj_set_style_text_color(label, lv_color_hex(0xFF0000), 0);
    lv_obj_align(label, LV_ALIGN_CENTER, 0, 0);
  }
}

// ─── 5 Card Poker Screen ─────────────────────────────────────
void showPokerScreen() {
  lv_obj_clean(lv_scr_act());
  lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  // Title
  lv_obj_t *title = lv_label_create(lv_scr_act());
  lv_label_set_text(title, "5 Card Poker");
  lv_obj_set_style_text_color(title, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 20);

  // Status / Info
  lv_obj_t *info = lv_label_create(lv_scr_act());
  lv_label_set_text_fmt(info, "Players: %d", playerCount);
  lv_obj_set_style_text_color(info, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(info, LV_ALIGN_TOP_MID, 0, 55);

  // "New Cards" button goes to screen where current user can swap cards in hand
  lv_obj_t *btnNewCards = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btnNewCards, 220, 80);
  lv_obj_set_pos(btnNewCards, 130, 120);
  lv_obj_add_event_cb(btnNewCards, [](lv_event_t *e) {
    showCardSwapScreen();        // Go to card swap selection
  }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lbl1 = lv_label_create(btnNewCards);
  lv_label_set_text(lbl1, "New Cards");
  lv_obj_center(lbl1);

  // "Next Player" button
  lv_obj_t *btnNextPlayer = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btnNextPlayer, 220, 80);
  lv_obj_set_pos(btnNextPlayer, 130, 220);
  lv_obj_add_event_cb(btnNextPlayer, [](lv_event_t *e) {
    Serial.println("5 Card: Next Player");
    // TODO: Send command to Pi if needed
  }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lbl2 = lv_label_create(btnNextPlayer);
  lv_label_set_text(lbl2, "Next Player");
  lv_obj_center(lbl2);

  // Back button to Main Menu
  lv_obj_t *backBtn = lv_btn_create(lv_scr_act());
  lv_obj_set_size(backBtn, 160, 55);
  lv_obj_set_pos(backBtn, 160, 320);
  lv_obj_add_event_cb(backBtn, [](lv_event_t *e) { showTitleScreen(); }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *backLbl = lv_label_create(backBtn);
  lv_label_set_text(backLbl, "Main Menu");
  lv_obj_center(backLbl);
}


// ─── Texas Hold'em Screen ───────────────────────────────────
void showHoldScreen() {
    lv_obj_clean(lv_scr_act());
    lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  // Title
  lv_obj_t *title = lv_label_create(lv_scr_act());
  lv_label_set_text(title, "Texas Hold'em");
  lv_obj_set_style_text_color(title, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 20);

  // Status / Info
  lv_obj_t *info = lv_label_create(lv_scr_act());
  lv_label_set_text_fmt(info, "Players: %d", playerCount);
  lv_obj_set_style_text_color(info, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(info, LV_ALIGN_TOP_MID, 0, 55);

  // Single large button
  lv_obj_t *btnDeal = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btnDeal, 280, 90);
  lv_obj_set_pos(btnDeal, 100, 140);
  lv_obj_add_event_cb(btnDeal, [](lv_event_t *e) {
    Serial.println("Hold'em: Deal next game phase");
    // TODO: Send command to Pi which deals cards based on current phase of hand
  }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lbl = lv_label_create(btnDeal);
  lv_label_set_text(lbl, "Deal Next Game Phase");
  lv_obj_center(lbl);

  // Back button
  lv_obj_t *backBtn = lv_btn_create(lv_scr_act());
  lv_obj_set_size(backBtn, 160, 55);
  lv_obj_set_pos(backBtn, 160, 320);
  lv_obj_add_event_cb(backBtn, [](lv_event_t *e) { showTitleScreen(); }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *backLbl = lv_label_create(backBtn);
  lv_label_set_text(backLbl, "Main Menu");
  lv_obj_center(backLbl);
}


// ─── Blackjack Screen ───────────────────────────────────────
void showBlackjackScreen() {

    lv_obj_clean(lv_scr_act());
    lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  // Title
  lv_obj_t *title = lv_label_create(lv_scr_act());
  lv_label_set_text(title, "Blackjack");
  lv_obj_set_style_text_color(title, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 20);

  // Status / Info
  lv_obj_t *info = lv_label_create(lv_scr_act());
  lv_label_set_text_fmt(info, "Players: %d", playerCount);
  lv_obj_set_style_text_color(info, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(info, LV_ALIGN_TOP_MID, 0, 55);

  // Hit and Stand buttons side by side
  lv_obj_t *btnHit = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btnHit, 140, 90);
  lv_obj_set_pos(btnHit, 80, 140);
  lv_obj_add_event_cb(btnHit, [](lv_event_t *e) {
    Serial.println("Blackjack: HIT");
    // TODO: Send command to Pi
  }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lblHit = lv_label_create(btnHit);
  lv_label_set_text(lblHit, "HIT");
  lv_obj_center(lblHit);

  lv_obj_t *btnStand = lv_btn_create(lv_scr_act());
  lv_obj_set_size(btnStand, 140, 90);
  lv_obj_set_pos(btnStand, 260, 140);
  lv_obj_add_event_cb(btnStand, [](lv_event_t *e) {
    Serial.println("Blackjack: STAND");
    // TODO: Send command to Pi
  }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *lblStand = lv_label_create(btnStand);
  lv_label_set_text(lblStand, "STAND");
  lv_obj_center(lblStand);

  // Back button
  lv_obj_t *backBtn = lv_btn_create(lv_scr_act());
  lv_obj_set_size(backBtn, 160, 55);
  lv_obj_set_pos(backBtn, 160, 320);
  lv_obj_add_event_cb(backBtn, [](lv_event_t *e) { showTitleScreen(); }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *backLbl = lv_label_create(backBtn);
  lv_label_set_text(backLbl, "Main Menu");
  lv_obj_center(backLbl);
}

// ─── Card Swap Screen (for 5 Card Poker) ─────────────────────
void showCardSwapScreen() {
  lv_obj_clean(lv_scr_act());
  lv_obj_set_style_bg_color(lv_scr_act(), lv_color_hex(0x1a1a2e), 0);

  // Title
  lv_obj_t *title = lv_label_create(lv_scr_act());
  lv_label_set_text(title, "How many cards do you want to swap?");
  lv_obj_set_style_text_color(title, lv_color_hex(0xFFFFFF), 0);
  lv_obj_align(title, LV_ALIGN_TOP_MID, 0, 20);

  // Info line
  lv_obj_t *info = lv_label_create(lv_scr_act());
  lv_label_set_text(info, "Select number of cards to change out");
  lv_obj_set_style_text_color(info, lv_color_hex(0xAAAAAA), 0);
  lv_obj_align(info, LV_ALIGN_TOP_MID, 0, 55);

  // Numbered buttons 1 to 4
  int nums[] = {1, 2, 3, 4};
  int btnW = 100;
  int btnH = 100;
  int startX = 70;
  int startY = 110;
  int gapX = 25;

  for (int i = 0; i < 4; i++) {
    int x = startX + i * (btnW + gapX);

    lv_obj_t *btn = lv_btn_create(lv_scr_act());
    lv_obj_set_size(btn, btnW, btnH);
    lv_obj_set_pos(btn, x, startY);

    // Store the number in user data and attach callback
    lv_obj_add_event_cb(btn, [](lv_event_t *e) {
      int numCards = (int)(intptr_t)lv_event_get_user_data(e);
      
      // Send command to Pi
      String cmd = "SWAP:" + String(numCards) + "\n";
      Serial2.print(cmd);
      
      Serial.print("Sent to Pi: SWAP:");
      Serial.println(numCards);

      // Return to the 5 Card Poker screen
      showPokerScreen();
    }, LV_EVENT_CLICKED, (void*)(intptr_t)nums[i]);

    lv_obj_t *lbl = lv_label_create(btn);
    lv_label_set_text_fmt(lbl, "%d", nums[i]);
    lv_obj_center(lbl);
    lv_obj_set_style_text_font(lbl, &lv_font_montserrat_28, 0); // Larger number
  }

  // Back button (returns to Poker screen, not main menu, to give user a chance to change their mind on their hand)
  lv_obj_t *backBtn = lv_btn_create(lv_scr_act());
  lv_obj_set_size(backBtn, 160, 55);
  lv_obj_set_pos(backBtn, 160, 320);
  lv_obj_add_event_cb(backBtn, [](lv_event_t *e) { 
    showPokerScreen(); 
  }, LV_EVENT_CLICKED, NULL);
  lv_obj_t *backLbl = lv_label_create(backBtn);
  lv_label_set_text(backLbl, "Cancel");
  lv_obj_center(backLbl);
}

// ─── Setup ────────────────────────────────────────────────

void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("Boot OK");
  Serial2.begin(115200, SERIAL_8N1, PI_RX, PI_TX);

  Wire.begin(I2C_SDA, I2C_SCL);
  TCA.begin();
  TCA.pinMode1(1, OUTPUT);
  lcd_reset();

  if (!touch.begin(Wire, FT6X36_SLAVE_ADDRESS)) {
    Serial.println("Touch init failed!");
  }

  if (!gfx->begin()) {
    Serial.println("Display init failed!");
  }

  gfx->setRotation(1);
  gfx->fillScreen(RGB565_BLACK);

  pinMode(GFX_BL, OUTPUT);
  digitalWrite(GFX_BL, HIGH);

  lv_init();

  screenWidth = 480;
  screenHeight = 320;
  bufSize = screenWidth * 40;

  disp_draw_buf1 = (lv_color_t *)heap_caps_malloc(bufSize * 2, MALLOC_CAP_DEFAULT | MALLOC_CAP_8BIT);
  disp_draw_buf2 = (lv_color_t *)heap_caps_malloc(bufSize * 2, MALLOC_CAP_DEFAULT | MALLOC_CAP_8BIT);
  lv_disp_draw_buf_init(&draw_buf, disp_draw_buf1, disp_draw_buf2, bufSize);

  lv_disp_drv_init(&disp_drv);
  disp_drv.hor_res = 480;
  disp_drv.ver_res = 320;
  disp_drv.flush_cb = my_disp_flush;
  disp_drv.draw_buf = &draw_buf;
  lv_disp_drv_register(&disp_drv);

  static lv_indev_drv_t indev_drv;
  lv_indev_drv_init(&indev_drv);
  indev_drv.type = LV_INDEV_TYPE_POINTER;
  indev_drv.read_cb = my_touchpad_read;
  lv_indev_drv_register(&indev_drv);

  showTitleScreen();

  Serial.println("Setup done");
}

void loop() {
  lv_timer_handler();
  delay(1);
}