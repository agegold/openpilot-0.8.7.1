#include <time.h>
#include <dirent.h>
#include <sys/types.h>
#include <sys/stat.h>

static void ui_draw_extras_limit_speed(UIState *s)
{
    auto car_state = (*s->sm)["carState"].getCarState();
    int activeNDA = 1;

    if(activeNDA > 0)
    {
        int w = 120;
        int h = 54;
        int x = (s->fb_w + (bdr_s*2))/2 - w/2 - bdr_s;
        int y = 40 - bdr_s;

        const char* img = activeNDA == 1 ? "img_nda" : "img_hda";
        ui_draw_image(s, {x, y, w, h}, img, 1.f);
    }

}

static void ui_draw_extras(UIState *s)
{
    ui_draw_extras_limit_speed(s);
}